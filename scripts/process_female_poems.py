#!/usr/bin/env python3
import json
import os
from collections import defaultdict

def process_female_poems():
    """处理女性诗作数据，正确统计每位诗人的诗作数量"""
    # 读取诗作数据
    poems_file = "data/processed/female_poems.json"
    with open(poems_file, 'r', encoding='utf-8') as f:
        poems_data = json.load(f)
    
    # 读取诗人数据
    poets_file = "data/processed/simplified_poets.json"
    with open(poets_file, 'r', encoding='utf-8') as f:
        poets_data = json.load(f)
    
    # 统计每位诗人的实际诗作数量
    poem_count_by_author = defaultdict(int)
    for poem in poems_data:
        if poem.get('author') and poem.get('title') and poem.get('paragraphs'):
            # 只统计有标题和内容的诗作
            if isinstance(poem['paragraphs'], list) or (isinstance(poem['paragraphs'], str) and poem['paragraphs'].startswith('[')):
                poem_count_by_author[poem['author']] += 1
    
    # 更新诗人数据中的诗作数量
    for category, poets in poets_data.items():
        for poet in poets:
            poet['poem_count'] = poem_count_by_author.get(poet['name'], 0)
    
    # 保存更新后的诗人数据
    with open(poets_file, 'w', encoding='utf-8') as f:
        json.dump(poets_data, f, ensure_ascii=False, indent=2)
    
    print(f"已更新诗人数据，保存到: {poets_file}")
    print("\n诗人诗作数量统计:")
    for author, count in sorted(poem_count_by_author.items(), key=lambda x: x[1], reverse=True):
        print(f"{author}: {count}首")

if __name__ == "__main__":
    process_female_poems() 