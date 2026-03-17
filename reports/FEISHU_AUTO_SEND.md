# 每日股票推荐 - 自动发送到飞书

_更新时间：2026-03-17 12:10_

---

## ✅ 配置方案

### 方案 1: 使用 OpenClaw 子代理 (推荐)

创建一个子代理会话来处理飞书发送：

```python
# 在 daily_stock_recommender.py 中添加
from sessions_send import send_to_session

def send_to_feishu(content):
    # 发送到主会话，由主会话的 message tool 处理
    send_to_session(
        session_key="agent:main:main",
        message=f"📈 股票推荐已生成，请发送到飞书:\n\n{content[:2000]}"
    )
```

### 方案 2: 使用 HTTP Webhook (简单)

如果飞书有 Webhook URL，可以直接 POST 发送。

### 方案 3: 手动确认发送 (当前)

报告生成后，在主会话中查看并手动发送。

---

## 🔧 当前配置

**定时任务**: 工作日 9:00 运行

**流程**:
1. 运行 `daily_stock_recommender.py`
2. 生成报告到 `reports/stock_rec_YYYYMMDD.md`
3. 保存飞书消息到 `reports/feishu_message.txt`
4. **需要手动发送到飞书**

---

## 📤 手动发送步骤

```bash
# 1. 查看生成的消息
cat /root/.openclaw/workspace/reports/feishu_message.txt

# 2. 在 OpenClaw 主会话中发送
# (使用 message tool)
```

---

## 🚀 自动发送配置 (可选)

### 使用 OpenClaw message tool

修改 crontab 为：

```bash
# 工作日 9:00 - 生成报告并发送
0 9 * * 1-5 cd /root/.openclaw/workspace && python3 scripts/daily_stock_recommender.py && python3 scripts/send_feishu_stock.py
```

然后在主会话中监听并发送。

### 使用飞书 Webhook

1. 在飞书创建群机器人
2. 获取 Webhook URL
3. 修改脚本直接 POST 到 Webhook

```python
import requests

def send_to_feishu_webhook(content, webhook_url):
    headers = {"Content-Type": "application/json"}
    data = {
        "msg_type": "text",
        "content": {"text": content}
    }
    requests.post(webhook_url, json=data, headers=headers)
```

---

## 📋 测试命令

```bash
# 手动运行并查看输出
cd /root/.openclaw/workspace && python3 scripts/daily_stock_recommender.py

# 查看生成的消息
cat reports/feishu_message.txt

# 测试发送脚本
python3 scripts/send_feishu_stock.py
```

---

## ⚠️ 注意事项

1. **消息长度**: 飞书消息有长度限制，长报告会被截断
2. **发送时机**: 定时任务运行时，需要主会话在线
3. **权限**: 确保 message tool 有飞书发送权限

---

## 🔗 相关文件

- 推荐脚本：`scripts/daily_stock_recommender.py`
- 发送脚本：`scripts/send_feishu_stock.py`
- 报告输出：`reports/stock_rec_YYYYMMDD.md`
- 待发消息：`reports/feishu_pending_send.txt`
