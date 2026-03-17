#!/bin/bash
# 每日股票推荐 - 包装脚本
# 运行股票推荐并发送到飞书

set -e

WORKSPACE="/root/.openclaw/workspace"
cd "$WORKSPACE"

echo "=========================================="
echo "每日股票推荐 - $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# 运行推荐脚本
python3 scripts/daily_stock_recommender.py

# 检查报告是否生成
if [ -f "reports/feishu_message.txt" ]; then
    echo ""
    echo "✅ 报告已生成：reports/feishu_message.txt"
    
    # 检查是否有待发送文件
    if [ -f "reports/feishu_pending_send.txt" ]; then
        echo "✅ 飞书消息已发送"
    else
        echo "⚠️ 飞书消息已保存到 reports/feishu_message.txt"
        echo "   需要手动发送"
    fi
else
    echo "❌ 报告生成失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "运行完成"
echo "=========================================="
