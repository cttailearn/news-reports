#!/bin/bash
echo "🧪 模型响应速度测试"
echo "===================="
API_KEY="sk-sp-aa287a8b0a194a51bae974a716cc104c"
BASE_URL="https://coding.dashscope.aliyuncs.com/v1"

test_model() {
  local model=$1
  local start=$(date +%s%N)
  curl -s -X POST "$BASE_URL/chat/completions" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"1+1=?\"}]}" > /dev/null
  local end=$(date +%s%N)
  echo "$model: $(( (end - start) / 1000000 ))ms"
}

for model in qwen3.5-plus qwen3-max-2026-01-23 qwen3-coder-next MiniMax-M2.5 glm-5 kimi-k2.5; do
  test_model "$model"
done
