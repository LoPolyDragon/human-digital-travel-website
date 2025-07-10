import os
import pandas as pd
from glob import glob

EXCEL_DIR = "地理区分2.21"
OUTPUT_DIR = "data/sample_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sample_preview():
    excel_files = glob(os.path.join(EXCEL_DIR, '*.xlsx'))
    print(f"采样前3个Excel文件，每个取前5行，保存到 {OUTPUT_DIR}")
    for i, file in enumerate(excel_files[:3]):
        filename = os.path.basename(file)
        try:
            df = pd.read_excel(file)
            sample = df.head(5)
            out_path = os.path.join(OUTPUT_DIR, f"{filename}.csv")
            sample.to_csv(out_path, index=False, encoding='utf-8-sig')
            print(f"已保存: {out_path}")
        except Exception as e:
            print(f"读取 {filename} 出错: {e}")

if __name__ == '__main__':
    sample_preview() 