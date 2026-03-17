#!/usr/bin/env node
// 模型响应速度测试

const MODELS = [
    { id: 'bailian/qwen3.5-plus', name: 'Qwen3.5 Plus' },
    { id: 'bailian/qwen3-max-2026-01-23', name: 'Qwen3 Max' },
    { id: 'bailian/qwen3-coder-next', name: 'Qwen3 Coder Next' },
    { id: 'bailian/qwen3-coder-plus', name: 'Qwen3 Coder Plus' },
    { id: 'bailian/MiniMax-M2.5', name: 'MiniMax M2.5' },
    { id: 'bailian/glm-5', name: 'GLM-5' },
    { id: 'bailian/glm-4.7', name: 'GLM-4.7' },
    { id: 'bailian/kimi-k2.5', name: 'Kimi K2.5' },
];

console.log('=== OpenClaw 模型响应速度测试 ===');
console.log(`测试时间: ${new Date().toLocaleString('zh-CN')}`);
console.log('');

// 模拟测试 - 实际应该调用 API
// 这里只是展示结构
for (const model of MODELS) {
    console.log(`模型: ${model.name} (${model.id})`);
}
