import os
import pandas as pd
from glob import glob
import hashlib
import requests
import time

# 输入输出路径
EXCEL_DIR = os.path.abspath('地理区分2.21')
print('查找路径:', EXCEL_DIR)
OUTPUT_DIR = os.path.abspath('data/processed')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 获取所有文件名，然后过滤.xlsx文件
all_files = os.listdir(EXCEL_DIR)
excel_files = [f for f in all_files if f.endswith('.xlsx')]
print(f'找到 {len(excel_files)} 个Excel文件')

# 结果表
poets_data = []
poems_data = []
places_data = []

# 用于去重的集合
poet_names = set()
place_names = set()

def safe_str(val):
    if val is None:
        return ''
    if isinstance(val, float) and (val != val):  # NaN
        return ''
    return str(val)

def get_place_id(row):
    # 用今地名+古地名+地点名胜生成唯一编号
    key = safe_str(row.get('今活动地市、县', '')) + '_' + safe_str(row.get('古一级地名', '')) + '_' + safe_str(row.get('地点名胜', ''))
    return hashlib.md5(key.encode('utf-8')).hexdigest()

places_dict = {}

def geocode_city(city_name, fallback_city=None):
    if not city_name and not fallback_city:
        return '', ''
    query = city_name if city_name else fallback_city
    url = f'https://nominatim.openstreetmap.org/search?format=json&q={query}'
    try:
        resp = requests.get(url, headers={'User-Agent': 'travel-poetry-map/1.0'})
        data = resp.json()
        if data:
            return data[0]['lon'], data[0]['lat']
        # 降级用 fallback_city
        if fallback_city and fallback_city != city_name:
            return geocode_city(fallback_city)
    except Exception as e:
        print(f'地名 {query} 地理编码失败: {e}')
    return '', ''

# 处理每个Excel文件
for excel_file in excel_files:
    file_path = os.path.join(EXCEL_DIR, excel_file)
    print(f'处理文件: {excel_file}')
    
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 提取城市名（从文件名）
        city_name = excel_file.replace('.xlsx', '')
        
        # 遍历所有行，保留所有字段
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            row_dict['文件名'] = city_name
            # 生成 place_id
            place_id = str(get_place_id(row_dict))
            row_dict['place_id'] = place_id
            # 游历顺序字段
            row_dict['游历顺序'] = f"{safe_str(row_dict.get('作家',''))}_{safe_str(city_name)}_{index+1}"
            poems_data.append(row_dict)
            
            # 优先用今地名+地点名胜查经纬度
            geo_query = (safe_str(row_dict.get('今活动地市、县', '')) + ' ' + safe_str(row_dict.get('地点名胜', ''))).strip()
            fallback_query = safe_str(row_dict.get('今活动地市、县', ''))
            place_key = (safe_str(row_dict.get('今活动地市、县', '')), safe_str(row_dict.get('古一级地名', '')), safe_str(row_dict.get('地点名胜', '')))
            if place_key not in places_dict:
                lon, lat = geocode_city(geo_query, fallback_query)
                places_dict[place_key] = {
                    '编号': place_id,
                    '今地名': safe_str(row_dict.get('今活动地市、县', '')),
                    '古地名': safe_str(row_dict.get('古一级地名', '')),
                    '地点名胜': safe_str(row_dict.get('地点名胜', '')),
                    '经度': lon,
                    '纬度': lat
                }
                time.sleep(1)  # Nominatim免费API限流
            
            # 提取数据，处理空值
            poet_name = str(row.get('作家', '')).strip()
            year = str(row.get('公元年', '')).strip()
            poem_title = str(row.get('系年作品', '')).strip()
            ancient_place = str(row.get('古一级地名', '')).strip()
            modern_province = str(row.get('今活动地省', '')).strip()
            modern_city = str(row.get('今活动地市、县', '')).strip()
            activity = str(row.get('活动', '')).strip()
            genre = str(row.get('体裁', '')).strip()
            
            # 跳过空数据
            if not poet_name or poet_name == 'nan':
                continue
                
            # 处理诗人数据
            if poet_name not in poet_names:
                poet_names.add(poet_name)
                poets_data.append({
                    'id': len(poets_data) + 1,
                    'name': poet_name,
                    'dynasty': '唐代',  # 根据数据推测
                    'birth_year': year if year and year != 'nan' else '未知',
                    'death_year': '未知'
                })
            
            # 处理诗作数据
            if poem_title and poem_title != 'nan':
                poems_data.append({
                    'id': len(poems_data) + 1,
                    'title': poem_title,
                    'poet_id': len(poets_data),  # 当前诗人的ID
                    'content': activity if activity and activity != 'nan' else '无内容',
                    'year': year if year and year != 'nan' else '未知',
                    'genre': genre if genre and genre != 'nan' else '未知'
                })
                
                # 处理地点数据
                place_key = f"{ancient_place}_{modern_province}_{modern_city}"
                if place_key not in place_names:
                    place_names.add(place_key)
                    places_data.append({
                        'id': len(places_data) + 1,
                        'name': city_name,
                        'ancient_name': ancient_place if ancient_place and ancient_place != 'nan' else '',
                        'modern_province': modern_province if modern_province and modern_province != 'nan' else '',
                        'modern_city': modern_city if modern_city and modern_city != 'nan' else '',
                        'poem_id': len(poems_data),
                        'latitude': 0.0,  # 需要地理编码
                        'longitude': 0.0
                    })
            
    except Exception as e:
        print(f'读取文件出错: {e}')

# 保存为CSV
if poets_data:
    pd.DataFrame(poets_data).to_csv(os.path.join(OUTPUT_DIR, 'poets.csv'), index=False, encoding='utf-8-sig')
if poems_data:
    pd.DataFrame(poems_data).to_csv(os.path.join(OUTPUT_DIR, 'poems_full.csv'), index=False, encoding='utf-8-sig')
if places_dict:
    pd.DataFrame(list(places_dict.values())).to_csv(os.path.join(OUTPUT_DIR, 'places.csv'), index=False, encoding='utf-8-sig')

print(f'数据已处理并导出到 {OUTPUT_DIR}/')
print(f'诗人数据: {len(poets_data)} 条')
print(f'诗作数据: {len(poems_data)} 条')
print(f'地点数据: {len(places_data)} 条') 