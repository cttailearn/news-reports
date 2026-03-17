# 股票技能配置 - AkShare 完全免费方案

_配置时间：2026-03-17 11:45_

---

## ✅ 配置完成

**默认股票数据源**: `akshare-cn-market`（完全免费）

---

## 📊 测试结果

### 1. A 股个股行情 ✅

**测试命令**:
```bash
python3 skills/akshare-cn-market/scripts/stock.py hist 000001 --n 10
```

**测试结果** (平安银行 000001):
```json
[
  {"date": "2026-03-03", "open": 10.85, "high": 10.95, "low": 10.8, "close": 10.88},
  {"date": "2026-03-04", "open": 10.84, "high": 10.84, "low": 10.67, "close": 10.71},
  {"date": "2026-03-05", "open": 10.72, "high": 10.84, "low": 10.7, "close": 10.81}
]
```

---

### 2. 大盘指数 ✅

**测试命令**:
```bash
# 上证指数
python3 skills/akshare-cn-market/scripts/stock.py index sh000001 --n 5

# 深证成指
python3 skills/akshare-cn-market/scripts/stock.py index sz399001 --n 5
```

**测试结果** (上证指数):
```json
[
  {"date": "2026-03-16", "open": 4092.249, "high": 4096.133, "low": 4048.087, "close": 4084.786}
]
```

**深证成指**:
```
2026-03-16  14291.149  14320.096  14097.815  14307.577  753 亿股
```

---

### 3. 宏观经济数据 ✅

#### GDP 数据
```bash
python3 skills/akshare-cn-market/scripts/macro.py gdp --n 4
```

**结果**:
```
2025 年第 1-4 季度  GDP: 140.19 万亿  同比增长：5.0%
```

#### CPI 数据
```bash
python3 skills/akshare-cn-market/scripts/macro.py cpi --n 6
```

**结果**:
```
2026 年 02 月份  CPI: 101.3  同比增长：1.3%
```

---

### 4. 财务数据 ✅

**测试命令**:
```bash
python3 skills/akshare-cn-market/scripts/stock.py financial 000001
```

**结果** (平安银行):
```json
{
  "报告期": 1990,
  "净利润": "7087.50 万",
  "净利润同比增长率": "64.75%",
  "净资产收益率 - 摊薄": "29.86%",
  "资产负债率": "2.37%"
}
```

---

## 🎯 快速使用指南

### A 股个股查询

```bash
# 查询个股 K 线（默认最近 10 条）
python3 skills/akshare-cn-market/scripts/stock.py hist 000001
python3 skills/akshare-cn-market/scripts/stock.py hist 600519

# 指定日期范围
python3 skills/akshare-cn-market/scripts/stock.py hist 000001 --start 20260101 --n 30

# 查询财务数据
python3 skills/akshare-cn-market/scripts/stock.py financial 000001
```

### 大盘指数查询

```bash
# 上证指数
python3 skills/akshare-cn-market/scripts/stock.py index sh000001

# 深证成指
python3 skills/akshare-cn-market/scripts/stock.py index sz399001

# 沪深 300
python3 skills/akshare-cn-market/scripts/stock.py index sh000300

# 上证 50
python3 skills/akshare-cn-market/scripts/stock.py index sh000016
```

### 宏观经济数据

```bash
# GDP 数据
python3 skills/akshare-cn-market/scripts/macro.py gdp

# CPI 数据
python3 skills/akshare-cn-market/scripts/macro.py cpi

# PMI 数据
python3 skills/akshare-cn-market/scripts/macro.py pmi

# 货币供应量 M2
python3 skills/akshare-cn-market/scripts/macro.py money

# 中美国债收益率
python3 skills/akshare-cn-market/scripts/macro.py bond
```

### 交易日查询

```bash
# 判断今天是否交易日
python3 skills/akshare-cn-market/scripts/trade_cal.py check today

# 获取最近一个交易日
python3 skills/akshare-cn-market/scripts/trade_cal.py prev today

# 获取下一个交易日
python3 skills/akshare-cn-market/scripts/trade_cal.py next today
```

---

## 📝 Python 直接调用

```python
import akshare as ak

# A 股个股 K 线
df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20260101", adjust="qfq")
print(df.head())

# 大盘指数
df = ak.stock_zh_index_daily(symbol="sh000001")
print(df.tail())

# GDP 数据
df = ak.macro_china_gdp()
print(df.head())

# CPI 数据
df = ak.macro_china_cpi()
print(df.head())

# 涨停板池（超短复盘）
df = ak.stock_zt_pool_em(date="20260316")
print(df.head())

# 龙虎榜
df = ak.stock_lhb_detail_em(start_date="20260316", end_date="20260316")
print(df.head())

# 北向资金
df = ak.stock_hsgt_hist_em(symbol="北向资金")
print(df.tail())
```

---

## 🆚 与付费方案对比

| 功能 | AkShare (免费) | Tushare (需积分) |
|------|---------------|-----------------|
| A 股行情 | ✅ | ✅ |
| 港股行情 | ✅ | ✅ |
| 美股行情 | ❌ | ✅ |
| 宏观数据 | ✅ | ✅ |
| 财务数据 | ✅ | ✅ |
| 涨停板池 | ✅ | ❌ |
| 龙虎榜 | ✅ | ❌ |
| 北向资金 | ✅ | ✅ |
| 配置难度 | 无 | 需签到获取积分 |

---

## ⚠️ 注意事项

1. **数据延迟**: 日线数据次日更新
2. **实时行情**: 不支持实时行情（仅收盘后数据）
3. **网络要求**: 需能访问新浪财经和东方财富
4. **投资风险**: 数据仅供参考，不构成投资建议

---

## 🔗 常用指数代码

| 代码 | 名称 |
|------|------|
| sh000001 | 上证综指 |
| sz399001 | 深证成指 |
| sh000300 | 沪深 300 |
| sh000016 | 上证 50 |
| sh000905 | 中证 500 |

---

## 📞 文档

- **AkShare 官方文档**: https://akshare.akfamily.xyz/
- **技能文档**: `skills/akshare-cn-market/SKILL.md`
