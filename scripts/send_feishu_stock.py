#!/usr/bin/env python3
"""
发送飞书消息 - 被 cron 调用的包装脚本
读取股票推荐报告并发送到飞书通道
"""

import sys
from pathlib import Path

# 读取报告
report_file = Path("/root/.openclaw/workspace/reports/feishu_message.txt")
if not report_file.exists():
    print(f"❌ 报告文件不存在：{report_file}")
    sys.exit(1)

content = report_file.read_text()

# 截断到飞书消息长度限制
if len(content) > 3000:
    content = content[:3000] + "\n\n... (内容过长，已截断)"

# 输出到 stdout，由 cron 捕获并处理
print("=== FEISHU_MESSAGE_START ===")
print(content)
print("=== FEISHU_MESSAGE_END ===")

# 同时保存到待发送文件
pending_file = Path("/root/.openclaw/workspace/reports/feishu_pending_send.txt")
pending_file.write_text(content)
print(f"\n✅ 消息已保存到：{pending_file}")
