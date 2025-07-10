#!/usr/bin/env python3
import json
import pandas as pd
import os

def clean_female_poems():
    """清理女性诗歌数据中的NaN值"""
    input_file = "/Users/anthony/Library/Mobile Documents/com~apple~CloudDocs/[02] Dev/[06] Travel Website/data/processed/female_poems.json"
    
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 清理数据
    cleaned_data = []
    for item in data:
        cleaned_item = {}
        for key, value in item.items():
            # 处理NaN值
            if pd.isna(value) or value == 'NaN' or str(value).strip() == 'nan':
                cleaned_item[key] = None
            else:
                cleaned_item[key] = value
        cleaned_data.append(cleaned_item)
    
    # 保存清理后的数据
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    
    print(f"已清理数据并保存到: {input_file}")
    print(f"总共处理了 {len(cleaned_data)} 条记录")

if __name__ == "__main__":
    clean_female_poems()