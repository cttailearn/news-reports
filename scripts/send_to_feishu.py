#!/usr/bin/env python3
"""
发送股票推荐到飞书
读取生成的报告并发送到飞书通道
"""

import sys
from pathlib import Path

# 读取报告
report_file = Path("/root/.openclaw/workspace/reports/feishu_message.txt")
if not report_file.exists():
    print(f"报告文件不存在：{report_file}")
    sys.exit(1)

content = report_file.read_text()

# 通过 OpenClaw message tool 发送
# 这里使用 subprocess 调用 OpenClaw 的 message 工具
import subprocess

# 创建临时 Python 脚本发送消息
send_script = f'''
import sys
sys.path.insert(0, "/root/.openclaw")

# 使用 OpenClaw 内部 API
content = """{content[:3000]}"""

# 保存消息内容到临时文件，供主进程读取
with open("/root/.openclaw/workspace/reports/feishu_pending.txt", "w") as f:
    f.write(content)

print("消息已准备，等待发送")
'''

subprocess.run(["python3", "-c", send_script], timeout=10)
print("发送脚本执行完成")
