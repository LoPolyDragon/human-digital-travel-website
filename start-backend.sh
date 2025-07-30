#!/bin/bash
cd "$(dirname "$0")/backend"

echo "启动后端服务器..."
echo "按 Ctrl+C 停止服务器"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

echo "📦 激活虚拟环境..."
source venv/bin/activate

echo "📦 安装所需依赖..."
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install pandas==2.1.3
pip install openpyxl==3.1.2
pip install python-multipart==0.0.6

echo "🚀 启动后端服务..."
python main.py
