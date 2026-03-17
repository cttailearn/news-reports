# 星月 1 号 - 用户偏好配置

_最后更新：2026-03-17 11:35_

---

## 👤 用户信息

- **称呼**: 主人
- **ID**: ou_10ffc60c948cf2313f4eb6b0241cf2ed

---

## 📍 居住地

**默认城市**: 贵阳花溪

- 天气查询默认使用贵阳
- 时区：Asia/Shanghai

---

## 🔑 API 配置

### Tushare Token
```
a17f72c790a177f96ca245d9a91106382c63021b66ab872d993dc2a5
```
- 状态：✅ 已配置
- 位置：`~/.bashrc`
- 注意：账户积分不足，需要每日签到

---

## 📊 已安装技能

### 新闻类
- `news-aggregator-skill` - 8 大平台新闻聚合
- `finance-news` - 财经简报（晨间/晚间）

### 天气类
- `weather-cn` - 中国天气网（默认贵阳）

### 股票类（免费方案）

**默认数据源**: `akshare-cn-market` ✅

- `akshare-cn-market` - **默认** A 股/指数/宏观数据（完全免费）
- `yahoo-finance` - 美股/全球股票（完全免费）
- `stock-analysis` - Yahoo Finance 分析（备用）
- `tushare-finance` - 备用（需积分）
- `finnhub` - 备用（待配置 API Key）

---

## ⏰ 定时任务配置

### 已配置任务

| 时间 | 任务 | 说明 |
|------|------|------|
| **工作日 9:00** | 股票推荐 | A 股短线股票推荐 (5 支) |
| 早上 8:00 | 新闻摘要 | 可选配置 |
| 早上 7:30 | 贵阳天气 | 可选配置 |

### 股票推荐任务
```bash
# 工作日 9:00 运行
0 9 * * 1-5 cd /root/.openclaw/workspace && python3 scripts/daily_stock_recommender.py >> logs/stock_recommender.log 2>&1
```

**输出**:
- 报告：`reports/stock_rec_YYYYMMDD.md`
- 飞书消息：`reports/feishu_message.txt`
- 日志：`logs/stock_recommender.log`

---

## 📝 待办事项

- [ ] Tushare 每日签到获取积分
- [ ] 考虑配置 Finnhub API Key（美股实时数据）
- [ ] 设置定时任务自动推送
