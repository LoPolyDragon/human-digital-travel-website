#!/usr/bin/env python3
import pandas as pd
import json
import os
import sys

def analyze_female_poems_excel(file_path):
    """分析唐代女性诗人休闲数据Excel文件"""
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        print(f"文件: {file_path}")
        print(f"总行数: {len(df)}")
        print(f"列数: {len(df.columns)}")
        print("\n列名:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1}. {col}")
        
        print("\n前5行数据:")
        print(df.head())
        
        print("\n数据类型:")
        print(df.dtypes)
        
        # 检查是否有空值
        print("\n空值统计:")
        print(df.isnull().sum())
        
        # 保存为JSON格式以便前端使用
        output_file = "/Users/anthony/Library/Mobile Documents/com~apple~CloudDocs/[02] Dev/[06] Travel Website/data/processed/female_poems.json"
        
        # 转换为JSON格式
        poems_data = df.to_dict('records')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(poems_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n数据已保存到: {output_file}")
        
        return df
        
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def analyze_identity_excel(file_path):
    """分析不同身份诗人数据Excel文件"""
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        print(f"\n\n文件: {file_path}")
        print(f"总行数: {len(df)}")
        print(f"列数: {len(df.columns)}")
        print("\n列名:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1}. {col}")
        
        print("\n前5行数据:")
        print(df.head())
        
        # 保存为JSON格式
        output_file = "/Users/anthony/Library/Mobile Documents/com~apple~CloudDocs/[02] Dev/[06] Travel Website/data/processed/female_poems_identity.json"
        
        # 转换为JSON格式
        identity_data = df.to_dict('records')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(identity_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n数据已保存到: {output_file}")
        
        return df
        
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

if __name__ == "__main__":
    base_path = "/Users/anthony/Library/Mobile Documents/com~apple~CloudDocs/[02] Dev/[06] Travel Website/黄梦琳 女性自我书写视角下的唐朝女性的休闲研究"
    
    # 分析主要数据文件
    main_file = os.path.join(base_path, "唐代女性诗人的休闲（编码完成）.xlsx")
    df1 = analyze_female_poems_excel(main_file)
    
    # 分析身份分类数据文件
    identity_file = os.path.join(base_path, "不同身份（诗句赏析ver.）.xlsx")
    df2 = analyze_identity_excel(identity_file)