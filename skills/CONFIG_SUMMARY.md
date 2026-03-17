# 技能配置总结

_最后更新：2026-03-17 11:35_

---

## 📊 技能状态总览

| 技能 | 状态 | 配置需求 | 测试结果 |
|------|------|----------|----------|
| 📰 **news-aggregator-skill** | ✅ 完全可用 | 无 | 36 氪、华尔街见闻正常 |
| 📈 **finance-news** | ✅ 完全可用 | 无（可选 API） | 晨间简报生成成功 |
| 🌤️ **weather-cn** | ✅ 完全可用 | 无 | **默认城市：贵阳花溪** |
| 📊 **stock-analysis** | ⚠️ 受限 | 无（Yahoo 限流） | Yahoo Finance 限流 |
| 📈 **tushare-finance** | ✅ Token 已配置 ⚠️ 积分不足 | ✅ Tushare Token | 需签到获取积分 |
| 📈 **finnhub** | ⚠️ 需配置 | Finnhub API Key | 依赖已安装 |
| 📈 **akshare-cn-market** | ✅ **完全免费** | 无 | **A 股/指数/宏观数据可用** ✅ |
| 📈 **yahoo-finance** | ✅ **完全免费** | 无 | 美股/全球股票可用 ✅ |

---

## ✅ 已完全配置的技能

### 1. 📰 news-aggregator-skill

**状态**: ✅ 完全可用

**测试**:
```bash
python3 scripts/fetch_news.py --source 36kr --limit 3
python3 scripts/fetch_news.py --source wallstreetcn --limit 3
```

**支持来源**:
- 36 氪、华尔街见闻、腾讯新闻
- Hacker News、GitHub Trending、Product Hunt
- V2EX、微博

**无需配置** - 直接使用

---

### 2. 📈 finance-news

**状态**: ✅ 完全可用

**测试**:
```bash
python3 scripts/briefing.py --time morning --style headlines
```

**功能**:
- ✅ RSS 新闻聚合（WSJ、Reuters、CNBC、Yahoo 等）
- ✅ 市场数据（美股/欧股/日股）
- ✅ AI 摘要生成（使用 Kimi/Gemini）
- ⚠️ WhatsApp 推送（需配置群组）

**配置位置**: `skills/finance-news/config/config.json`

**已启用来源**: WSJ, Reuters, Bloomberg, CNBC, Yahoo, MarketWatch, FT 等

---

### 3. 🌤️ weather-cn

**状态**: ✅ 完全可用

**测试**:
```bash
bash weather-cn.sh 北京
bash weather-cn.sh 上海
```

**功能**:
- ✅ 中国天气网数据
- ✅ 50+ 城市支持
- ✅ 生活指数（感冒、运动、穿衣等）
- ✅ 零 Token 消耗

**无需配置** - 直接使用

**支持城市**: 北京、上海、广州、深圳、成都、杭州等 50+ 城市

---

## ⚠️ 需要配置的技能

### 4. 📊 stock-analysis (Yahoo Finance)

**状态**: ⚠️ 受限 - Yahoo Finance 限流

**问题**: Yahoo Finance 对 IP 限流，返回 "Too Many Requests"

**替代方案**:
1. 使用 **tushare-finance** (A 股/港股/美股)
2. 使用 **finnhub** (美股实时数据)
3. 等待限流解除（通常 1 小时）

---

### 5. 📈 tushare-finance (推荐用于 A 股)

**状态**: ✅ Token 已配置 ⚠️ 积分不足

**Token**: `a17f72c790a177f96ca245d9a91106382c63021b66ab872d993dc2a5` ✅

**当前问题**: 账户积分不足，无法访问大部分接口

**解决方案**:

1. **每日签到** (5 积分/天):
   - 访问 https://tushare.pro/user/profile
   - 点击"签到"获取积分

2. **新手任务**:
   - 完善个人信息 (+10 积分)
   - 关注官方公众号 (+20 积分)

3. **充值** (可选):
   - 120 积分/年 (学生优惠)
   - 基础数据需要 120 积分

**基础数据需求**:
- 股票列表：120 积分
- 日线行情：120 积分
- 财务指标：600 积分

**测试命令**:
```bash
export TUSHARE_TOKEN="a17f72c790a177f96ca245d9a91106382c63021b66ab872d993dc2a5"
python3 -c "import tushare as ts; pro=ts.pro_api(); print(pro.stock_basic(list_status='L').head())"
```

---

### 6. 📈 finnhub (推荐用于美股)

**状态**: ⚠️ 需要 API Key

**配置步骤**:

1. **获取 API Key**:
   - 访问 https://finnhub.io 注册
   - 免费 tier: 60 次/分钟

2. **设置环境变量**:
   ```bash
   echo 'export FINNHUB_API_KEY="your_key_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **测试**:
   ```bash
   curl "https://finnhub.io/api/v1/quote?symbol=AAPL&token=YOUR_KEY"
   ```

**支持数据**:
- ✅ 美股实时股价
- ✅ 公司新闻、财报
- ✅ 技术指标（部分需付费）

---

## 🎯 使用建议

### 每日信息流配置

**推荐组合**:

| 时间 | 技能 | 命令 |
|------|------|------|
| 🌅 早上 8:00 | news-aggregator-skill | 获取隔夜新闻 |
| 🌅 早上 9:00 | finance-news | 晨间财经简报 |
| 🌤️ 随时 | weather-cn | 天气查询 |
| 📈 交易时间 | tushare-finance | A 股行情 |
| 📈 交易时间 | finnhub | 美股行情 |

### 定时任务示例

```bash
# 每日新闻简报（早上 8 点）
0 8 * * * cd ~/.openclaw/workspace/skills/news-aggregator-skill && python3 scripts/fetch_news.py --source all --limit 10

# 财经简报（早上 9 点）
0 9 * * 1-5 cd ~/.openclaw/workspace/skills/finance-news && python3 scripts/briefing.py --time morning
```

---

## 📝 待办事项

- [ ] 获取 Tushare Token 并配置（A 股数据）
- [ ] 获取 Finnhub API Key 并配置（美股数据）
- [ ] 设置定时任务自动推送
- [ ] 配置 WhatsApp/Telegram 推送（可选）

---

## 🔧 快速命令参考

### 新闻
```bash
# 36 氪快讯
python3 ~/.openclaw/workspace/skills/news-aggregator-skill/scripts/fetch_news.py --source 36kr --limit 10

# 华尔街见闻
python3 ~/.openclaw/workspace/skills/news-aggregator-skill/scripts/fetch_news.py --source wallstreetcn --limit 10
```

### 财经简报
```bash
# 晨间简报
python3 ~/.openclaw/workspace/skills/finance-news/scripts/briefing.py --time morning

# 晚间简报
python3 ~/.openclaw/workspace/skills/finance-news/scripts/briefing.py --time evening
```

### 天气
```bash
# 查询北京天气
bash ~/.openclaw/workspace/skills/weather-cn/weather-cn.sh 北京
```

### 股票
```bash
# A 股（需要 Tushare Token）
python3 -c "import tushare as ts; pro=ts.pro_api(); print(pro.daily(ts_code='000001.SZ', start_date='20241201', end_date='20241231').head())"

# 美股（需要 Finnhub Key）
curl "https://finnhub.io/api/v1/quote?symbol=AAPL&token=YOUR_KEY"
```

---

## 📞 获取帮助

- **Tushare**: https://tushare.pro/document/2
- **Finnhub**: https://finnhub.io/docs/api
- **中国天气网**: https://www.weather.com.cn/
