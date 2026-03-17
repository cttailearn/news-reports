# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## API Keys

### Tavily Search
- API Key: `tvly-dev-*` (配置在 ~/.bashrc)
- 用途：AI 优化的网页搜索
- 使用：`node skills/tavily-search/scripts/search.mjs "查询内容"`

### Tushare
- Token: `a17f72c790a177f96ca245d9a91106382c63021b66ab872d993dc2a5` (配置在 ~/.bashrc)
- 用途：A 股/港股/美股行情、财务数据、宏观经济
- 使用：`python3 -c "import tushare as ts; pro=ts.pro_api(); print(pro.daily(ts_code='000001.SZ', start_date='20241201', end_date='20241231').head())"`

## User Preferences

### 居住地
- **默认天气查询城市**: 贵阳花溪
- 使用 `weather-cn` 技能时默认查询贵阳天气

### 常用技能配置

**默认数据源配置**:

- **新闻来源**: 36 氪、华尔街见闻
- **财经简报**: 晨间简报（早上 9 点）
- **股票数据**:
  - **A 股/港股**: `akshare-cn-market`（默认，完全免费）✅
  - **美股**: `stock-analysis` 或 `yahoo-finance`（yfinance 库）
  - **宏观数据**: `akshare-cn-market`（GDP/CPI/PMI/M2 等）
- **天气查询**: 贵阳花溪（默认城市）

### 快速命令

```bash
# A 股个股 K 线
python3 skills/akshare-cn-market/scripts/stock.py hist 000001

# 上证指数
python3 skills/akshare-cn-market/scripts/stock.py index sh000001

# GDP/CPI 数据
python3 skills/akshare-cn-market/scripts/macro.py gdp
python3 skills/akshare-cn-market/scripts/macro.py cpi

# 贵阳天气
bash skills/weather-cn/weather-cn.sh 贵阳
```
