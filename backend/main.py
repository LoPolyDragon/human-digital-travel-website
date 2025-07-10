from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from pathlib import Path
import json
from typing import List, Dict, Optional
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting data loading...")
    load_excel_data()
    print("Data loading completed.")
    yield
    # Shutdown
    pass

app = FastAPI(title="唐代诗人游历地图 API", description="提供唐代诗人游历地点和路线数据的API", lifespan=lifespan)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 数据缓存
places_data = {}
coordinates_data = {}

# 手动创建城市坐标映射（基于常见城市坐标）
def load_coordinates():
    """加载城市坐标数据"""
    # 手动创建主要城市的坐标映射
    coordinates_dict = {
        "邢台": {"coordinates": [37.0682, 114.5086], "province": "河北"},
        "延安": {"coordinates": [36.5853, 109.4897], "province": "陕西"},
        "漯河": {"coordinates": [33.5817, 114.046], "province": "河南"},
        "哈密": {"coordinates": [42.833, 93.513], "province": "新疆"},
        "扬州": {"coordinates": [32.3932, 119.4215], "province": "江苏"},
        "北京": {"coordinates": [39.9042, 116.4074], "province": "北京"},
        "天津": {"coordinates": [39.1042, 117.2], "province": "天津"},
        "上海": {"coordinates": [31.2304, 121.4737], "province": "上海"},
        "重庆": {"coordinates": [29.5647, 106.5507], "province": "重庆"},
        "西安": {"coordinates": [34.3416, 108.9398], "province": "陕西"},
        "长安": {"coordinates": [34.3416, 108.9398], "province": "陕西"},  # 古代长安即今西安
        "洛阳": {"coordinates": [34.6197, 112.4540], "province": "河南"},
        "南京": {"coordinates": [32.0603, 118.7969], "province": "江苏"},
        "金陵": {"coordinates": [32.0603, 118.7969], "province": "江苏"},  # 古代金陵即今南京
        "杭州": {"coordinates": [30.2741, 120.1551], "province": "浙江"},
        "苏州": {"coordinates": [31.2989, 120.5853], "province": "江苏"},
        "成都": {"coordinates": [30.5728, 104.0668], "province": "四川"},
        "广州": {"coordinates": [23.1291, 113.2644], "province": "广东"},
        "深圳": {"coordinates": [22.5431, 114.0579], "province": "广东"},
        "武汉": {"coordinates": [30.5928, 114.3055], "province": "湖北"},
        "郑州": {"coordinates": [34.7466, 113.6254], "province": "河南"},
        "济南": {"coordinates": [36.6512, 117.1201], "province": "山东"},
        "青岛": {"coordinates": [36.0986, 120.3719], "province": "山东"},
        "石家庄": {"coordinates": [38.0428, 114.5149], "province": "河北"},
        "太原": {"coordinates": [37.8706, 112.5489], "province": "山西"},
        "沈阳": {"coordinates": [41.8057, 123.4315], "province": "辽宁"},
        "大连": {"coordinates": [38.9140, 121.6147], "province": "辽宁"},
        "长春": {"coordinates": [43.8171, 125.3235], "province": "吉林"},
        "哈尔滨": {"coordinates": [45.8038, 126.5349], "province": "黑龙江"},
        "昆明": {"coordinates": [25.0389, 102.7183], "province": "云南"},
        "贵阳": {"coordinates": [26.5783, 106.7135], "province": "贵州"},
        "拉萨": {"coordinates": [29.6516, 91.172], "province": "西藏"},
        "兰州": {"coordinates": [36.0611, 103.8343], "province": "甘肃"},
        "西宁": {"coordinates": [36.6171, 101.7782], "province": "青海"},
        "银川": {"coordinates": [38.4872, 106.2309], "province": "宁夏"},
        "乌鲁木齐": {"coordinates": [43.8256, 87.6168], "province": "新疆"},
        "呼和浩特": {"coordinates": [40.8214, 111.6562], "province": "内蒙古"},
        "福州": {"coordinates": [26.0745, 119.2965], "province": "福建"},
        "厦门": {"coordinates": [24.4798, 118.0894], "province": "福建"},
        "南昌": {"coordinates": [28.6829, 115.8579], "province": "江西"},
        "合肥": {"coordinates": [31.8209, 117.2264], "province": "安徽"},
        "长沙": {"coordinates": [28.2282, 112.9388], "province": "湖南"},
        "南宁": {"coordinates": [22.8167, 108.3669], "province": "广西"},
        "海口": {"coordinates": [20.0444, 110.1999], "province": "海南"},
    }
    
    print(f"Loaded {len(coordinates_dict)} coordinate entries from manual mapping")
    return coordinates_dict

def load_excel_data():
    """加载所有Excel文件的数据"""
    global coordinates_data
    coordinates_data = load_coordinates()
    
    # 使用绝对路径
    base_dir = Path(__file__).parent.parent
    excel_dir = base_dir / "地理区分2.21"
    
    print(f"Loading Excel files from: {excel_dir}")
    print(f"Excel directory exists: {excel_dir.exists()}")
    
    excel_files = list(excel_dir.glob("*.xlsx"))
    print(f"Found {len(excel_files)} Excel files")
    
    for excel_file in excel_files:
        try:
            df = pd.read_excel(excel_file)
            city_name = excel_file.stem
            places_data[city_name] = df.to_dict('records')
            print(f"Loaded {city_name}: {len(df)} records")
        except Exception as e:
            print(f"Error loading {excel_file}: {e}")
    
    total_records = sum(len(records) for records in places_data.values())
    print(f"Total loaded {len(places_data)} cities with {total_records} records")


@app.post("/api/reload-data")
async def reload_data():
    """手动重新加载数据"""
    print("Manual data reload triggered...")
    load_excel_data()
    total_records = sum(len(records) for records in places_data.values())
    return {"status": "success", "cities": len(places_data), "total_records": total_records}

@app.get("/api/places")
async def get_places(
    poet: Optional[str] = None,
    period: Optional[str] = None,
    category: Optional[str] = None
):
    """获取地点数据，支持按诗人、时期和类别筛选"""
    try:
        filtered_data = []
        
        for city, records in places_data.items():
            # 获取城市坐标
            coordinates = coordinates_data.get(city, {}).get("coordinates", None)
            if not coordinates:
                continue
                
            for record in records:
                poet_name = record.get('作家', record.get('诗人', ''))
                # 只有当指定了诗人时才进行过滤
                if poet and str(poet_name).strip() != poet:
                    continue
                # 暂时不过滤时期和类别，因为Excel结构不同
                # if period and str(record.get('时期', '')).strip() != period:
                #     continue
                # if category and str(record.get('类别', '')).strip() != category:
                #     continue
                
                # 处理NaN值，确保JSON序列化不会出错
                def clean_value(value):
                    if pd.isna(value):
                        return ""
                    return str(value) if value is not None else ""
                
                filtered_data.append({
                    'city': city,
                    'poet': clean_value(poet_name),
                    'period': clean_value(record.get('皇帝纪年', '')),
                    'year': clean_value(record.get('公元年', '')),
                    'place': clean_value(record.get('地点名胜', '')),
                    'activity': clean_value(record.get('活动', '')),
                    'poem': clean_value(record.get('系年作品', '')),
                    'coordinates': coordinates
                })
        
        return filtered_data
    except Exception as e:
        print(f"Error in get_places: {e}")
        raise

@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "ok",
        "loaded_cities": len(places_data),
        "total_records": sum(len(records) for records in places_data.values())
    }

@app.get("/api/poets")
async def get_poets():
    """获取所有诗人列表"""
    poets = set()
    for records in places_data.values():
        for record in records:
            poet_name = record.get('作家', record.get('诗人', ''))
            if poet_name:
                poets.add(str(poet_name).strip())
    return sorted(list(poets))

@app.get("/api/periods")
async def get_periods():
    """获取所有时期列表"""
    periods = set()
    for records in places_data.values():
        for record in records:
            if '时期' in record and record['时期']:
                periods.add(str(record['时期']).strip())
    return sorted(list(periods))

@app.get("/api/categories")
async def get_categories():
    """获取所有诗人类别列表"""
    categories = set()
    for records in places_data.values():
        for record in records:
            if '类别' in record and record['类别']:
                categories.add(str(record['类别']).strip())
    return sorted(list(categories))

@app.get("/api/routes/{poet}")
async def get_poet_routes(poet: str):
    """获取指定诗人的游历路线，按年代排序"""
    try:
        visited_cities = []
        
        for city, records in places_data.items():
            coordinates = coordinates_data.get(city, {}).get("coordinates", None)
            if not coordinates:
                continue
                
            for record in records:
                poet_name = record.get('作家', record.get('诗人', ''))
                if str(poet_name).strip() == poet:
                    # 处理年份数据，确保JSON兼容
                    def clean_value(value):
                        if pd.isna(value):
                            return ""
                        if isinstance(value, float):
                            if value != value:  # NaN check
                                return ""
                            return int(value) if value.is_integer() else 0
                        return str(value) if value is not None else ""
                    
                    year_str = record.get('公元年', '')
                    try:
                        year = int(float(year_str)) if year_str and str(year_str).strip() and not pd.isna(year_str) else 0
                    except:
                        year = 0
                    
                    city_data = {
                        'city': city,
                        'coordinates': coordinates,
                        'year': year,
                        'period': clean_value(record.get('皇帝纪年', '')),
                        'activity': clean_value(record.get('活动', '')),
                        'poem': clean_value(record.get('系年作品', '')),
                        'place': clean_value(record.get('地点名胜', ''))
                    }
                    visited_cities.append(city_data)
        
        # 按年份排序
        visited_cities.sort(key=lambda x: x['year'] if x['year'] > 0 else 9999)
        
        # 去重，保留最早的记录
        unique_cities = {}
        for city_data in visited_cities:
            city_name = city_data['city']
            if city_name not in unique_cities or (city_data['year'] > 0 and city_data['year'] < unique_cities[city_name]['year']):
                unique_cities[city_name] = city_data
        
        ordered_cities = list(unique_cities.values())
        ordered_cities.sort(key=lambda x: x['year'] if x['year'] > 0 else 9999)
        
        # 创建路线
        routes = []
        if len(ordered_cities) > 1:
            route_coordinates = [city['coordinates'] for city in ordered_cities]
            routes.append(route_coordinates)
        
        return {
            'poet': poet,
            'cities': ordered_cities,
            'routes': routes,
            'total_cities': len(ordered_cities)
        }
    except Exception as e:
        print(f"Error in get_poet_routes: {e}")
        return {
            'poet': poet,
            'cities': [],
            'routes': [],
            'total_cities': 0
        }

@app.get("/api/city/{city_name}")
async def get_city_details(city_name: str):
    """获取特定城市的详细信息，包括诗人作品"""
    try:
        # 尝试从Excel文件读取详细数据
        excel_path = f"../地理区分2.21/{city_name}.xlsx"
        
        if not os.path.exists(excel_path):
            # 如果没有对应的Excel文件，返回基本信息
            city_records = places_data.get(city_name, [])
            coordinates = coordinates_data.get(city_name, {}).get("coordinates", None)
            
            return {
                'city': city_name,
                'coordinates': coordinates,
                'found_excel': False,
                'total_records': len(city_records),
                'basic_records': city_records[:10],  # 只返回前10条基本记录
                'poets': list(set([r.get('作家', r.get('诗人', '')) for r in city_records if r.get('作家', r.get('诗人', ''))])),
                'detailed_records': []
            }
        
        # 读取Excel文件获取详细信息
        df = pd.read_excel(excel_path)
        
        # 清理数据
        def clean_value(value):
            if pd.isna(value) or value is None:
                return ""
            if isinstance(value, (int, float)):
                if pd.isna(value):
                    return ""
                return str(int(value)) if isinstance(value, float) and value.is_integer() else str(value)
            return str(value).strip()
        
        detailed_records = []
        poets_works = {}
        
        for _, row in df.iterrows():
            poet = clean_value(row.get('作家', ''))
            work = clean_value(row.get('系年作品', ''))
            year = clean_value(row.get('公元年', ''))
            period = clean_value(row.get('皇帝纪年', ''))
            activity = clean_value(row.get('活动', ''))
            genre = clean_value(row.get('体裁', ''))
            
            if poet:
                if poet not in poets_works:
                    poets_works[poet] = []
                
                if work:  # 只有当有作品时才添加
                    poets_works[poet].append({
                        'work': work,
                        'year': year,
                        'period': period,
                        'activity': activity,
                        'genre': genre
                    })
        
        # 构建详细记录
        for poet, works in poets_works.items():
            if works:  # 只包含有作品的诗人
                detailed_records.append({
                    'poet': poet,
                    'works_count': len(works),
                    'works': works[:20]  # 限制每个诗人最多返回20个作品
                })
        
        # 按作品数量排序
        detailed_records.sort(key=lambda x: x['works_count'], reverse=True)
        
        coordinates = coordinates_data.get(city_name, {}).get("coordinates", None)
        
        return {
            'city': city_name,
            'coordinates': coordinates,
            'found_excel': True,
            'total_records': len(df),
            'total_poets': len(poets_works),
            'poets_with_works': len(detailed_records),
            'detailed_records': detailed_records[:10],  # 返回前10个诗人的详细信息
            'all_poets': list(poets_works.keys())
        }
        
    except Exception as e:
        print(f"Error in get_city_details for {city_name}: {e}")
        return {
            'city': city_name,
            'error': str(e),
            'found_excel': False,
            'total_records': 0,
            'detailed_records': []
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)