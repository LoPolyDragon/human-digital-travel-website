#!/usr/bin/env python3
import json
import pandas as pd
from collections import defaultdict

def analyze_poets_categories():
    """分析诗人类别和统计信息"""
    input_file = "/Users/anthony/Library/Mobile Documents/com~apple~CloudDocs/[02] Dev/[06] Travel Website/data/processed/female_poems.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 按诗人分组
    poets_data = defaultdict(list)
    identities = set()
    
    for poem in data:
        if poem.get('author') and poem.get('author') != 'NaN':
            author = poem['author']
            identity = poem.get('内容', '未知')
            if identity and identity != 'NaN' and identity is not None:
                identities.add(identity)
            poets_data[author].append(poem)
    
    print("=== 诗人类别分析 ===")
    print(f"总诗人数: {len(poets_data)}")
    print(f"总诗歌数: {len(data)}")
    print(f"身份类别数: {len(identities)}")
    print(f"身份类别: {list(identities)}")
    
    # 按身份分组诗人
    identity_poets = defaultdict(list)
    for author, poems in poets_data.items():
        # 取第一首诗的身份作为诗人身份
        identity = poems[0].get('内容', '未知')
        if identity and identity != 'NaN' and identity is not None:
            identity_poets[identity].append({
                'name': author,
                'poem_count': len(poems),
                'poems': poems
            })
        else:
            identity_poets['未知'].append({
                'name': author,
                'poem_count': len(poems),
                'poems': poems
            })
    
    print("\n=== 按身份分组统计 ===")
    for identity, poets in identity_poets.items():
        print(f"{identity}: {len(poets)}位诗人")
        for poet in poets[:5]:  # 只显示前5位
            print(f"  - {poet['name']} ({poet['poem_count']}首)")
        if len(poets) > 5:
            print(f"  ... 还有{len(poets)-5}位诗人")
        print()
    
    # 保存分类数据
    output_file = "/Users/anthony/Library/Mobile Documents/com~apple~CloudDocs/[02] Dev/[06] Travel Website/data/processed/poets_categories.json"
    
    # 转换为可序列化的格式
    categories_data = {}
    for identity, poets in identity_poets.items():
        categories_data[identity] = []
        for poet in poets:
            categories_data[identity].append({
                'name': poet['name'],
                'poem_count': poet['poem_count'],
                'sample_poems': poet['poems'][:3]  # 只保存前3首作为示例
            })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(categories_data, f, ensure_ascii=False, indent=2)
    
    print(f"分类数据已保存到: {output_file}")
    
    return categories_data

if __name__ == "__main__":
    analyze_poets_categories()