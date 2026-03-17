# 每日股票推荐定时任务配置

_配置时间：2026-03-17 11:55_

---

## ✅ 配置完成

**定时任务**: 每个工作日 (周一至周五) 上午 9:00 自动运行

**时区**: Asia/Shanghai

---

## 📋 Crontab 配置

```bash
# 每日股票推荐 (工作日 9:00)
0 9 * * 1-5 cd /root/.openclaw/workspace && python3 scripts/daily_stock_recommender.py >> logs/stock_recommender.log 2>&1
```

---

## 📁 文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 推荐脚本 | `scripts/daily_stock_recommender.py` | 主脚本 |
| 包装脚本 | `scripts/daily_stock_recommender.sh` | Shell 包装器 |
| 报告输出 | `reports/stock_rec_YYYYMMDD.md` | 每日报告 |
| 飞书消息 | `reports/feishu_message.txt` | 待发送消息 |
| 运行日志 | `logs/stock_recommender.log` | 运行日志 |

---

## 🔧 管理命令

```bash
# 查看定时任务
crontab -l | grep stock

# 编辑定时任务
crontab -e

# 手动运行测试
cd /root/.openclaw/workspace && python3 scripts/daily_stock_recommender.py

# 查看日志
tail -f logs/stock_recommender.log

# 查看最新报告
cat reports/stock_rec_$(date +%Y%m%d).md
```

---

## 📊 推荐逻辑

### 选股策略

1. **涨停板池**: 获取当日所有涨停股票
2. **筛选条件**:
   - 连板数 >= 1
   - 封板资金 > 3000 万
3. **排序逻辑**:
   - 优先高连板 (3 板以上)
   - 其次封板资金大的
   - 考虑行业热度

### 推荐数量

- 每日推荐 **5 支** 股票
- 按连板数和封板资金综合评分

### 分析维度

- 连板数 (1-10 板)
- 封板资金 (万元)
- 所属行业
- 首次封板时间
- 短线策略建议

---

## 📤 飞书发送

**当前配置**: 报告生成后保存到 `reports/feishu_message.txt`

**手动发送**:
```bash
# 查看待发送内容
cat reports/feishu_message.txt

# 通过 OpenClaw message tool 发送
# (需要在主会话中执行)
```

**自动发送配置** (可选):

1. 编辑脚本添加发送逻辑
2. 或使用 OpenClaw cron 的 --announce 选项

---

## 📈 示例输出

```markdown
# 📈 A 股短线股票推荐
_生成时间：2026-03-17 11:53 | 数据日期：20260317_

## 🎯 推荐股票 (5 支)

### 1. 亚翔集成 (603929)
- **状态**: 涨停 (+10.0%)
- **连板数**: 3 板
- **封板资金**: 147.5 万元
- **行业**: 专业工程
- **推荐理由**: 3 连板 (强势) | 封板资金 147.5 万 (强)

**短线策略**:
- ✅ 高连板龙头，关注继续强势
- ⚠️ 高位股波动大，设置止损位
- 💰 建议仓位：不超过总资金 20%
- 🛑 止损位：-5% 至 -7%
```

---

## ⚠️ 注意事项

1. **数据延迟**: 使用昨日收盘数据
2. **网络要求**: 需能访问 AkShare 数据源
3. **风险提示**: 仅供参考，不构成投资建议
4. **止损建议**: 严格执行 -5% 至 -7% 止损

---

## 🔗 相关文档

- 技能文档：`skills/akshare-cn-market/SKILL.md`
- 使用指南：`skills/akshare-cn-market/USAGE.md`
- 配置总结：`skills/CONFIG_SUMMARY.md`
