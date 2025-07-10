import os
import pandas as pd

# 查看Excel文件的结构
EXCEL_DIR = '地理区分2.21'
excel_files = [f for f in os.listdir(EXCEL_DIR) if f.endswith('.xlsx')]

print(f'找到 {len(excel_files)} 个Excel文件')
print()

# 查看前3个文件的结构
for i, file in enumerate(excel_files[:3]):
    file_path = os.path.join(EXCEL_DIR, file)
    
    print(f'文件 {i+1}: {file}')
    print('=' * 50)
    
    try:
        df = pd.read_excel(file_path)
        print(f'行数: {len(df)}')
        print(f'列数: {len(df.columns)}')
        print(f'列名: {list(df.columns)}')
        print()
        
        if len(df) > 0:
            print('前3行数据:')
            print(df.head(3).to_string())
        else:
            print('文件为空!')
            
    except Exception as e:
        print(f'读取文件出错: {e}')
    
    print()
    print('-' * 80)
    print()