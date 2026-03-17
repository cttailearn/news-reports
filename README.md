# 每日新闻和股票报告

自动生成的每日重大新闻 HTML 报告和 A 股短线股票推荐。

## 📰 内容

- **每日重大新闻**: 经济、科技类重大事件
- **股票推荐**: 主板短线股票分析

## 🕐 更新时间

- 新闻报告：工作日 8:50 (Asia/Shanghai)
- 股票推荐：工作日 9:00 (Asia/Shanghai)

## 📁 目录结构

```
reports/
├── news/
│   ├── daily_news_YYYY-MM-DD.html  # 每日新闻报告
│   ├── latest.html                 # 最新新闻 (符号链接)
│   └── README.md                   # 配置说明
├── news_index.html                 # 新闻索引
└── stock_rec_YYYYMMDD.md          # 股票推荐
```

## 🌐 访问

- 最新新闻：`/reports/news/latest.html`
- 新闻索引：`/reports/news_index.html`

## 📊 数据来源

- 新闻：华尔街见闻、36 氪、Hacker News
- 股票：AkShare (A 股涨停板数据)

## ⚠️ 免责声明

- 新闻报告仅供参考
- 股票推荐不构成投资建议
- 市场有风险，投资需谨慎

## 📝 自动生成

本报告由 OpenClaw AI 助手自动生成。
定时任务配置为每个工作日运行。

---

**最后更新**: 2026-03-17
**生成器**: OpenClaw AI
