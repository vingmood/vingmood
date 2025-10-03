#!/bin/bash
# 微博热搜抓取脚本安装脚本

echo "微博热搜抓取脚本安装程序"
echo "=========================="

# 检查Python版本
python_version=$(python3 --version 2>&1)
if [ $? -ne 0 ]; then
    echo "❌ 错误：未找到Python3，请先安装Python3"
    exit 1
fi

echo "✅ 检测到Python版本：$python_version"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误：未找到pip3，请先安装pip3"
    exit 1
fi

echo "✅ 检测到pip3"

# 安装依赖
echo "正在安装依赖包..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ 依赖包安装成功"
else
    echo "❌ 依赖包安装失败"
    exit 1
fi

# 创建必要的目录
mkdir -p hot_searches_data
echo "✅ 创建数据保存目录"

# 设置执行权限
chmod +x weibo_hot_search.py
chmod +x scheduled_crawler.py
chmod +x run.py
chmod +x test_crawler.py
echo "✅ 设置执行权限"

echo ""
echo "🎉 安装完成！"
echo ""
echo "使用方法："
echo "  单次抓取：python3 run.py --mode once"
echo "  定时抓取：python3 run.py --mode schedule"
echo "  测试脚本：python3 test_crawler.py"
echo "  直接运行：python3 weibo_hot_search.py"
echo ""
echo "更多选项请使用：python3 run.py --help"