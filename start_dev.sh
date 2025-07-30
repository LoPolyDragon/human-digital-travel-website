#!/bin/bash

# 唐代诗人游历轨迹网站开发服务启动脚本

echo "🚀 启动唐代诗人游历轨迹网站开发环境..."

# 检查端口8000是否被占用
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  端口8000已被占用，尝试清理..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# 检查端口3000是否被占用
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  端口3000已被占用，尝试清理..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# 启动后端服务
echo "📊 启动后端API服务 (端口8000)..."
cd "$(dirname "$0")/backend"
# 检查Python依赖
if [ ! -f "requirements.txt" ]; then
    echo "❌ 未找到requirements.txt文件"
    exit 1
fi
# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi
# 激活虚拟环境并安装依赖
source venv/bin/activate
# 确保所有依赖都已安装
pip install fastapi==0.104.1 uvicorn==0.24.0 pandas==2.1.3 openpyxl==3.1.2 python-multipart==0.0.6 >/dev/null 2>&1
# 启动后端
python main.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# 等待后端启动
echo "⏳ 等待后端服务启动..."
sleep 10

# 检查后端是否成功启动
echo "⏳ 检查后端服务状态..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:8000/api/health >/dev/null; then
        echo "✅ 后端服务启动成功"
        break
    fi
    attempt=$((attempt+1))
    if [ $attempt -eq $max_attempts ]; then
        echo "❌ 后端服务启动失败，请检查logs/backend.log"
        exit 1
    fi
    echo "⏳ 尝试 $attempt/$max_attempts... (数据加载可能需要一些时间)"
    sleep 3
done

# 启动前端服务
echo "🌐 启动前端服务 (端口3000)..."
cd frontend
# 检查Node.js依赖
if [ ! -f "package.json" ]; then
    echo "❌ 未找到package.json文件"
    exit 1
fi
# 安装依赖（如果需要）
if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi
# 启动前端
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "📝 进程信息："
echo "   后端PID: $BACKEND_PID"
echo "   前端PID: $FRONTEND_PID"

echo ""
echo "🎉 开发环境启动完成！"
echo ""
echo "📱 访问地址："
echo "   前端: http://localhost:3000"
echo "   后端API: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "📋 功能说明："
echo "   ✨ 地图视图：可视化诗人游历地点，点击查看诗作"
echo "   👥 诗人信息：按朝代分类展示诗人，查看详细信息"
echo "   🗺️  游历路线：显示诗人的时间顺序游历轨迹"
echo "   🛣️  交通图层：展示唐代主要陆路水路交通线"
echo "   🔍 筛选功能：按诗人、年份筛选显示内容"
echo ""
echo "⏹️  停止服务请运行: ./stop_dev.sh"
echo ""

# 保存PID到文件
mkdir -p logs
echo $BACKEND_PID > logs/backend.pid
echo $FRONTEND_PID > logs/frontend.pid

# 等待用户输入
echo "按 Ctrl+C 停止所有服务"
trap 'echo ""; echo "🛑 正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT

# 保持脚本运行
wait