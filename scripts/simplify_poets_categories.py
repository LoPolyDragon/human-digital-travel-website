#!/usr/bin/env python3
import json
import pandas as pd
from collections import defaultdict
import re

def simplify_categories():
    """简化诗人身份分类"""
    input_file = "/Users/anthony/Library/Mobile Documents/com~apple~CloudDocs/[02] Dev/[06] Travel Website/data/processed/female_poems.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 创建更简化的身份分类
    simplified_categories = {
        "宫妃": ["宫妃", "妃子", "贵妃", "公主", "婕妤"],
        "诗人": ["诗人", "文人", "才女", "女诗人"],
        "道士/女冠": ["女冠", "女道士", "道士", "女尼"],
        "歌妓": ["歌妓", "姬妾", "歌女"],
        "士大夫妻女": ["士大夫妻女", "官员妻女", "贵族女子"],
        "平民": ["平民女子", "普通女子"]
    }
    
    # 按诗人分组数据
    poets_data = defaultdict(list)
    for poem in data:
        if poem.get('author') and poem.get('author') != 'NaN':
            author = poem['author']
            poets_data[author].append(poem)
    
    # 为每个诗人确定简化身份
    def get_simplified_identity(identity_text):
        if not identity_text or identity_text == 'NaN' or identity_text is None:
            return "未知"
        
        # 简单的关键词匹配
        identity_lower = str(identity_text).lower()
        
        if any(word in identity_lower for word in ["公主", "妃", "宫"]):
            return "宫妃"
        elif any(word in identity_lower for word in ["诗人", "文人", "才女"]):
            return "诗人"
        elif any(word in identity_lower for word in ["女冠", "道士", "女尼"]):
            return "道士/女冠"
        elif any(word in identity_lower for word in ["歌妓", "姬妾", "歌女"]):
            return "歌妓"
        elif any(word in identity_lower for word in ["士大夫", "官员", "贵族"]):
            return "士大夫妻女"
        elif any(word in identity_lower for word in ["平民", "普通"]):
            return "平民"
        else:
            return "其他"
    
    # 创建简化的诗人数据
    simplified_poets = defaultdict(list)
    
    for author, poems in poets_data.items():
        # 取第一首诗的身份信息
        first_poem = poems[0]
        original_identity = first_poem.get('内容', '未知')
        simplified_identity = get_simplified_identity(original_identity)
        
        poet_info = {
            'name': author,
            'identity': simplified_identity,
            'original_identity': original_identity,
            'poem_count': len(poems),
            'sample_poems': [
                {
                    'title': poem.get('title', '无题'),
                    'content': poem.get('paragraphs', ''),
                    'activities': poem.get('活动', ''),
                    'location': poem.get('地点', ''),
                    'time': poem.get('时间', ''),
                    'emotion': poem.get('情感', '')
                } for poem in poems[:3]  # 只保存前3首作为示例
            ]
        }
        
        simplified_poets[simplified_identity].append(poet_info)
    
    # 输出统计信息
    print("=== 简化后的诗人分类统计 ===")
    total_poets = sum(len(poets) for poets in simplified_poets.values())
    print(f"总诗人数: {total_poets}")
    
    for category, poets in simplified_poets.items():
        print(f"{category}: {len(poets)}位诗人")
        # 显示一些示例诗人
        for poet in poets[:3]:
            print(f"  - {poet['name']} ({poet['poem_count']}首)")
        if len(poets) > 3:
            print(f"  ... 还有{len(poets)-3}位诗人")
        print()
    
    # 保存简化数据
    output_file = "/Users/anthony/Library/Mobile Documents/com~apple~CloudDocs/[02] Dev/[06] Travel Website/data/processed/simplified_poets.json"
    
    # 转换为可序列化的格式
    serializable_data = {}
    for category, poets in simplified_poets.items():
        serializable_data[category] = poets
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_data, f, ensure_ascii=False, indent=2)
    
    print(f"简化数据已保存到: {output_file}")
    
    return serializable_data

if __name__ == "__main__":
    simplify_categories()