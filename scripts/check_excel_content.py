import os
import pandas as pd

# 查看第一个Excel文件的结构
EXCEL_DIR = os.path.abspath('地理区分2.21')
excel_files = [f for f in os.listdir(EXCEL_DIR) if f.endswith('.xlsx')]

if excel_files:
    first_file = excel_files[0]
    file_path = os.path.join(EXCEL_DIR, first_file)
    
    print(f'查看文件: {first_file}')
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
else:
    print('没有找到Excel文件') 