# 定时任务配置完成

_配置时间：2026-03-17 11:56_

---

## ✅ 配置完成

### 定时任务：每日股票推荐

| 项目 | 配置 |
|------|------|
| **运行时间** | 工作日 (周一至周五) 上午 9:00 |
| **时区** | Asia/Shanghai |
| **Cron 表达式** | `0 9 * * 1-5` |
| **脚本路径** | `/root/.openclaw/workspace/scripts/daily_stock_recommender.py` |

---

## 📋 Crontab 配置

```bash
# 查看配置
crontab -l | grep stock

# 输出:
0 9 * * 1-5 cd /root/.openclaw/workspace && python3 scripts/daily_stock_recommender.py >> logs/stock_recommender.log 2>&1
```

---

## 📊 测试结果

**今日测试运行成功** ✅

### 推荐股票 (2026-03-17)

| 排名 | 股票 | 代码 | 连板 | 封板资金 | 行业 |
|------|------|------|------|----------|------|
| 1 | 亚翔集成 | 603929 | 3 板 | 147.5 万 | 专业工程 |
| 2 | 锡华科技 | 603248 | 3 板 | 139.8 万 | 风电设备 |
| 3 | 三房巷 | 600370 | 4 板 | 68.8 万 | 化学纤维 |
| 4 | 法尔胜 | 000890 | 4 板 | 71.3 万 | 环保设备 |
| 5 | 京投发展 | 600683 | 3 板 | 85.1 万 | 房地产 |

### 重要新闻

1. "存储狂潮"何时见顶？这是最有效的"领先指标" - Wall Street CN
2. 郭明錤：融入英伟达生态，LPU 产量将暴增 10 倍 - Wall Street CN
3. 澳洲联储连续第二次加息至 4.1% - Wall Street CN

---

## 📁 文件位置

| 文件 | 路径 |
|------|------|
| 推荐脚本 | `scripts/daily_stock_recommender.py` |
| 每日报告 | `reports/stock_rec_YYYYMMDD.md` |
| 飞书消息 | `reports/feishu_message.txt` |
| 运行日志 | `logs/stock_recommender.log` |
| 配置文档 | `reports/README_stock_recommender.md` |

---

## 📤 飞书发送

### 当前状态

报告已生成到 `reports/feishu_message.txt`，需要手动或自动发送到飞书。

### 方案 1: 手动发送 (当前)

```bash
# 查看消息内容
cat reports/feishu_message.txt

# 在 OpenClaw 主会话中使用 message tool 发送
```

### 方案 2: 自动发送 (可选)

修改脚本添加飞书发送逻辑，或使用 OpenClaw 的 --announce 选项。

---

## 🔧 管理命令

```bash
# 查看定时任务
crontab -l | grep stock

# 编辑定时任务
crontab -e

# 手动运行测试
cd /root/.openclaw/workspace && python3 scripts/daily_stock_recommender.py

# 查看最新报告
cat reports/stock_rec_$(date +%Y%m%d).md

# 查看运行日志
tail -f logs/stock_recommender.log

# 禁用定时任务
crontab -e  # 注释掉对应行

# 启用定时任务
crontab -e  # 取消注释
```

---

## 📈 选股逻辑

### 数据来源
- **涨停板池**: AkShare `stock_zt_pool_em`
- **财经新闻**: news-aggregator-skill (华尔街见闻)
- **资金流向**: AkShare `stock_market_fund_flow`

### 筛选条件
1. 连板数 >= 1
2. 封板资金 > 3000 万
3. 按连板数降序排序
4. 取前 5 支推荐

### 分析维度
- 连板数 (1-10 板)
- 封板资金 (万元)
- 所属行业
- 首次封板时间
- 短线策略建议

---

## ⚠️ 风险提示

1. **数据延迟**: 使用昨日收盘数据，非实时
2. **网络依赖**: 需能访问 AkShare 数据源
3. **投资风险**: 仅供参考，不构成投资建议
4. **止损建议**: 严格执行 -5% 至 -7% 止损
5. **仓位控制**: 单支股票不超过总资金 20%

---

## 📞 相关文档

- [配置详解](reports/README_stock_recommender.md)
- [AkShare 使用指南](skills/akshare-cn-market/USAGE.md)
- [技能配置总结](skills/CONFIG_SUMMARY.md)
- [用户偏好](memory/user-preferences.md)

---

## ✅ 下一步

1. **验证定时任务**: 等待明日 9:00 自动运行
2. **配置飞书发送**: 如需自动发送，联系配置 message tool
3. **调整策略**: 根据实际效果调整选股逻辑

---

_配置完成！每个工作日 9:00 自动推送 5 支短线股票推荐。_ 🌙
