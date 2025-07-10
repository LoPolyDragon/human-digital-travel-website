#!/bin/bash
cd "$(dirname "$0")/backend"

echo "启动后端服务器..."
echo "按 Ctrl+C 停止服务器"

python3 main.py