import pandas as pd
import json
from pathlib import Path

def process_coordinates():
    """处理城市坐标数据"""
    # 示例坐标数据（实际项目中应该从可靠的地理数据源获取）
    city_coordinates = {
        "长安": {"coordinates": [34.3416, 108.9398]},
        "洛阳": {"coordinates": [34.6321, 112.4470]},
        "扬州": {"coordinates": [32.3947, 119.4142]},
        "成都": {"coordinates": [30.5728, 104.0668]},
        "杭州": {"coordinates": [30.2741, 120.1551]},
        "苏州": {"coordinates": [31.2989, 120.5853]},
        "南京": {"coordinates": [32.0603, 118.7969]},
        "开封": {"coordinates": [34.7847, 114.3078]},
        "广州": {"coordinates": [23.1291, 113.2644]},
        "西安": {"coordinates": [34.3416, 108.9398]}  # 现代的长安
    }
    
    # 确保目录存在
    output_dir = Path("../data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存为JSON文件
    with open(output_dir / "places.json", "w", encoding="utf-8") as f:
        json.dump(city_coordinates, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    process_coordinates() 