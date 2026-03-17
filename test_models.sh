#!/bin/bash
# 模型响应速度测试脚本

MODELS=(
    "bailian/qwen3.5-plus"
    "bailian/qwen3-max-2026-01-23"
    "bailian/qwen3-coder-next"
    "bailian/qwen3-coder-plus"
    "bailian/MiniMax-M2.5"
    "bailian/glm-5"
    "bailian/glm-4.7"
    "bailian/kimi-k2.5"
)

echo "=== OpenClaw 模型响应速度测试 ==="
echo "测试时间: $(date)"
echo ""

for model in "${MODELS[@]}"; do
    echo "测试模型: $model"
    start_time=$(date +%s%N)
    
    # 使用 session_status 测试模型切换
    result=$(openclaw sessions send main "/model $model" 2>&1)
    
    end_time=$(date +%s%N)
    elapsed=$(( (end_time - start_time) / 1000000 ))  # 转换为毫秒
    
    echo "  耗时: ${elapsed}ms"
    echo ""
done

echo "=== 测试完成 ==="
