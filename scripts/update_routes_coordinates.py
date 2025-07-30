import json

def update_routes_with_coordinates():
    """为路线数据添加坐标信息"""
    
    # 读取地点数据（包含坐标信息）
    with open('data/processed/places.json', 'r', encoding='utf-8') as f:
        places = json.load(f)
    
    # 创建地点ID到坐标的映射
    place_coords = {}
    for place in places:
        place_coords[place['id']] = {
            'lat': place['lat'],
            'lng': place['lng'],
            'modern_name': place.get('modern_name', place.get('city', ''))
        }
    
    # 读取路线数据
    with open('data/processed/routes.json', 'r', encoding='utf-8') as f:
        routes = json.load(f)
    
    print(f"开始为 {len(routes)} 位诗人的路线添加坐标...")
    
    # 为每个诗人的路线添加坐标
    updated_routes = {}
    for poet_name, route_data in routes.items():
        updated_route = []
        for point in route_data:
            place_id = point['place_id']
            if place_id in place_coords:
                updated_point = point.copy()
                updated_point['lat'] = place_coords[place_id]['lat']
                updated_point['lng'] = place_coords[place_id]['lng']
                updated_point['modern_name'] = place_coords[place_id]['modern_name']
                updated_route.append(updated_point)
            else:
                # 如果找不到对应的地点坐标，保留原数据但添加默认坐标
                updated_point = point.copy()
                updated_point['lat'] = 39.9042  # 北京坐标作为默认值
                updated_point['lng'] = 116.4074
                updated_point['modern_name'] = point.get('place_name', '')
                updated_route.append(updated_point)
        
        updated_routes[poet_name] = updated_route
        print(f"已处理: {poet_name} ({len(updated_route)} 个地点)")
    
    # 保存更新后的路线数据
    with open('data/processed/routes.json', 'w', encoding='utf-8') as f:
        json.dump(updated_routes, f, ensure_ascii=False, indent=2)
    
    print("路线坐标更新完成！")

if __name__ == "__main__":
    update_routes_with_coordinates()