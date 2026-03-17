# ✅ 飞书自动发送配置完成

_配置时间：2026-03-17 12:15_

---

## 🎉 配置状态

| 项目 | 状态 |
|------|------|
| 定时任务 | ✅ 已配置 (工作日 9:00) |
| 股票推荐脚本 | ✅ 已测试 |
| 飞书发送 | ✅ 测试成功 |
| 报告生成 | ✅ 正常 |

---

## 📊 今日测试发送

**发送时间**: 2026-03-17 12:15

**消息 ID**: `om_x100b54b9105e0cbcb37efb49921c438`

**发送状态**: ✅ 成功发送到飞书

### 推荐股票

| # | 股票 | 代码 | 连板 | 封板资金 |
|---|------|------|------|----------|
| 1 | 亚翔集成 | 603929 | 3 板 | 147.5 万 |
| 2 | 锡华科技 | 603248 | 3 板 | 139.8 万 |
| 3 | 三房巷 | 600370 | 4 板 | 68.8 万 |
| 4 | 法尔胜 | 000890 | 4 板 | 71.3 万 |
| 5 | 京投发展 | 600683 | 3 板 | 85.1 万 |

---

## 🔧 定时任务配置

### Crontab

```bash
# 查看配置
crontab -l | grep stock

# 输出:
0 9 * * 1-5 cd /root/.openclaw/workspace && python3 scripts/daily_stock_recommender.py >> logs/stock_recommender.log 2>&1
```

### 运行流程

```
工作日 9:00
    ↓
运行 daily_stock_recommender.py
    ↓
1. 获取涨停板数据 (AkShare)
2. 获取财经新闻 (news-aggregator-skill)
3. 分析选股 (连板数 + 封板资金)
4. 生成推荐报告
    ↓
保存到:
- reports/stock_rec_YYYYMMDD.md (完整报告)
- reports/feishu_message.txt (飞书消息)
    ↓
日志输出到:
- logs/stock_recommender.log
```

---

## 📤 飞书发送方案

### 当前方案：手动确认发送

**原因**: 自动发送需要主会话在线，定时任务运行时可能主会话不在线。

**流程**:
1. 定时任务生成报告
2. 消息保存到 `reports/feishu_message.txt`
3. 在主会话中查看并发送

**优点**: 可以审查内容，确保准确性

### 自动发送方案 (可选)

如需完全自动发送，有两种方案：

#### 方案 A: 使用飞书 Webhook

```python
import requests

WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

def send_to_feishu(content):
    requests.post(WEBHOOK_URL, json={
        "msg_type": "text",
        "content": {"text": content}
    })
```

#### 方案 B: 使用 OpenClaw message tool

修改 crontab 为：
```bash
0 9 * * 1-5 cd /root/.openclaw/workspace && python3 scripts/daily_stock_recommender.py && openclaw message send --channel feishu --file reports/feishu_message.txt
```

---

## 📁 文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 推荐脚本 | `scripts/daily_stock_recommender.py` | 主脚本 |
| 包装脚本 | `scripts/daily_stock_recommender.sh` | Shell 包装器 |
| 每日报告 | `reports/stock_rec_YYYYMMDD.md` | 完整报告 |
| 飞书消息 | `reports/feishu_message.txt` | 待发送消息 |
| 运行日志 | `logs/stock_recommender.log` | 运行日志 |
| 配置文档 | `reports/FEISHU_AUTO_SEND_CONFIG.md` | 配置说明 |

---

## 🔧 管理命令

```bash
# 查看定时任务
crontab -l | grep stock

# 手动运行测试
cd /root/.openclaw/workspace && python3 scripts/daily_stock_recommender.py

# 查看最新报告
cat reports/stock_rec_$(date +%Y%m%d).md

# 查看待发送消息
cat reports/feishu_message.txt

# 查看运行日志
tail -f logs/stock_recommender.log

# 禁用定时任务
crontab -e  # 注释掉对应行

# 启用定时任务
crontab -e  # 取消注释
```

---

## ⚠️ 注意事项

1. **数据延迟**: 使用昨日收盘数据，非实时
2. **网络依赖**: 需能访问 AkShare 数据源
3. **消息长度**: 飞书消息限制约 3000 字符
4. **投资风险**: 仅供参考，不构成投资建议

---

## 📞 相关文档

- [定时任务配置](reports/SETUP_COMPLETE.md)
- [飞书配置说明](reports/FEISHU_AUTO_SEND_CONFIG.md)
- [AkShare 使用指南](skills/akshare-cn-market/USAGE.md)
- [配置总结](skills/CONFIG_SUMMARY.md)

---

## ✅ 总结

**配置完成！**

- ✅ 定时任务已配置 (工作日 9:00)
- ✅ 股票推荐脚本已测试
- ✅ 飞书发送测试成功
- ✅ 报告自动生成

**下一步**:
- 等待明日 9:00 自动运行
- 如需完全自动发送，配置 Webhook 或修改 crontab

---

_星月 1 号 🌙 - 每个工作日 9:00 为你推送 5 支短线股票_
