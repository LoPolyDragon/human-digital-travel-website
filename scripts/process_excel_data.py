import os
import pandas as pd
import json
from collections import defaultdict
import re

def process_excel_files():
    """处理所有Excel文件，提取诗人、地点、诗作数据"""
    
    EXCEL_DIR = '地理区分2.21'
    excel_files = [f for f in os.listdir(EXCEL_DIR) if f.endswith('.xlsx')]
    
    poets = set()
    places = []
    poems = []
    routes = defaultdict(list)
    
    place_id_counter = 1
    poem_id_counter = 1
    
    print(f'开始处理 {len(excel_files)} 个Excel文件...')
    
    for file in excel_files:
        file_path = os.path.join(EXCEL_DIR, file)
        city_name = file.replace('.xlsx', '')
        
        try:
            df = pd.read_excel(file_path)
            
            for _, row in df.iterrows():
                # 提取诗人信息
                poet_name = str(row.get('作家', '')).strip()
                if poet_name and poet_name != 'nan':
                    poets.add(poet_name)
                
                # 提取地点信息
                ancient_place = str(row.get('古二级地名', '') or row.get('古一级地名', '')).strip()
                modern_province = str(row.get('今活动地省', '')).strip()
                modern_city = str(row.get('今活动地市、县', '')).strip()
                
                if ancient_place and ancient_place != 'nan':
                    place_info = {
                        'id': place_id_counter,
                        'ancient_name': ancient_place,
                        'modern_name': f"{modern_province}{modern_city}" if modern_province != 'nan' and modern_city != 'nan' else city_name,
                        'province': modern_province if modern_province != 'nan' else '',
                        'city': modern_city if modern_city != 'nan' else city_name,
                        'lat': 0.0,  # 需要后续添加坐标
                        'lng': 0.0   # 需要后续添加坐标
                    }
                    places.append(place_info)
                    
                    # 提取诗作信息
                    poem_title = str(row.get('系年作品', '')).strip()
                    year = row.get('公元年', None)
                    activity = str(row.get('活动', '')).strip()
                    
                    if poem_title and poem_title != 'nan':
                        poem_info = {
                            'id': poem_id_counter,
                            'title': poem_title,
                            'poet': poet_name,
                            'year': int(year) if pd.notna(year) else None,
                            'place_id': place_id_counter,
                            'place_name': ancient_place,
                            'genre': str(row.get('体裁', '')).strip(),
                            'content': activity if activity != 'nan' else '',
                            'source': str(row.get('来源', '')).strip()
                        }
                        poems.append(poem_info)
                        poem_id_counter += 1
                    
                    # 为诗人游历路线收集数据
                    if poet_name and poet_name != 'nan' and pd.notna(year):
                        routes[poet_name].append({
                            'year': int(year),
                            'place_id': place_id_counter,
                            'place_name': ancient_place,
                            'activity': activity if activity != 'nan' else ''
                        })
                    
                    place_id_counter += 1
                    
        except Exception as e:
            print(f'处理文件 {file} 时出错: {e}')
    
    # 整理诗人游历路线
    processed_routes = {}
    for poet, route_data in routes.items():
        # 按年份排序
        route_data.sort(key=lambda x: x['year'])
        processed_routes[poet] = route_data
    
    print(f'处理完成：{len(poets)} 位诗人，{len(places)} 个地点，{len(poems)} 首诗作')
    
    return {
        'poets': sorted(list(poets)),
        'places': places,
        'poems': poems,
        'routes': processed_routes
    }

def save_processed_data(data):
    """保存处理后的数据"""
    
    os.makedirs('data/processed', exist_ok=True)
    
    # 保存诗人数据
    with open('data/processed/poets.json', 'w', encoding='utf-8') as f:
        json.dump(data['poets'], f, ensure_ascii=False, indent=2)
    
    # 保存地点数据
    with open('data/processed/places.json', 'w', encoding='utf-8') as f:
        json.dump(data['places'], f, ensure_ascii=False, indent=2)
    
    # 保存诗作数据
    with open('data/processed/poems.json', 'w', encoding='utf-8') as f:
        json.dump(data['poems'], f, ensure_ascii=False, indent=2)
    
    # 保存路线数据
    with open('data/processed/routes.json', 'w', encoding='utf-8') as f:
        json.dump(data['routes'], f, ensure_ascii=False, indent=2)
    
    print('数据已保存到 data/processed/ 目录')

if __name__ == '__main__':
    data = process_excel_files()
    save_processed_data(data)