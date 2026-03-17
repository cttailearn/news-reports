# 飞书自动发送配置

_配置时间：2026-03-17 12:10_

---

## ✅ 配置完成

### 自动发送流程

```
定时任务 (9:00) 
    ↓
运行 daily_stock_recommender.py
    ↓
生成股票推荐报告
    ↓
保存到 reports/stock_rec_YYYYMMDD.md
    ↓
保存到 reports/feishu_message.txt
    ↓
调用 sessions_send 发送到主会话
    ↓
主会话使用 message tool 发送到飞书
```

---

## 📋 配置详情

### 定时任务

```bash
# 工作日 9:00 运行
0 9 * * 1-5 cd /root/.openclaw/workspace && python3 scripts/daily_stock_recommender.py >> logs/stock_recommender.log 2>&1
```

### 发送逻辑

脚本中的 `send_to_feishu()` 函数：

1. 截断报告到 2800 字符以内
2. 使用 `sessions_send` 发送到主会话
3. 主会话收到后使用 `message` tool 发送到飞书
4. 如果发送失败，保存到 `feishu_pending_send.txt`

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
cat reports/feishu_pending_send.txt

# 查看运行日志
tail -f logs/stock_recommender.log
```

---

## 📤 手动发送 (备选方案)

如果自动发送失败，可以手动发送：

```bash
# 1. 查看消息内容
cat /root/.openclaw/workspace/reports/feishu_message.txt

# 2. 在 OpenClaw 主会话中复制发送
```

---

## ⚠️ 注意事项

1. **消息长度**: 飞书消息限制约 3000 字符，长报告会被截断
2. **主会话在线**: 自动发送需要主会话在线
3. **发送失败**: 会自动保存到 `feishu_pending_send.txt`

---

## 📁 相关文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 推荐脚本 | `scripts/daily_stock_recommender.py` | 主脚本 |
| 包装脚本 | `scripts/daily_stock_recommender.sh` | Shell 包装器 |
| 发送脚本 | `scripts/send_feishu_stock.py` | 备选发送脚本 |
| 每日报告 | `reports/stock_rec_YYYYMMDD.md` | 完整报告 |
| 飞书消息 | `reports/feishu_message.txt` | 待发送消息 |
| 待发送 | `reports/feishu_pending_send.txt` | 发送失败备选 |
| 运行日志 | `logs/stock_recommender.log` | 运行日志 |

---

## 🧪 测试

```bash
# 完整测试
cd /root/.openclaw/workspace
python3 scripts/daily_stock_recommender.py

# 检查输出
ls -la reports/
cat reports/feishu_message.txt | head -30
```

---

## 📊 今日测试结果

**测试时间**: 2026-03-17 12:10

**推荐股票**:
1. 亚翔集成 (603929) - 3 连板
2. 锡华科技 (603248) - 3 连板
3. 三房巷 (600370) - 4 连板
4. 法尔胜 (000890) - 4 连板
5. 京投发展 (600683) - 3 连板

**状态**: ✅ 报告生成成功

---

## 🔗 相关文档

- [定时任务配置](reports/SETUP_COMPLETE.md)
- [AkShare 使用指南](skills/akshare-cn-market/USAGE.md)
- [配置总结](skills/CONFIG_SUMMARY.md)
