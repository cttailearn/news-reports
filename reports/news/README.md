# 每日重大新闻配置

_配置时间：2026-03-17 12:25_

---

## ✅ 配置完成

### 定时任务

| 任务 | 时间 | Cron 表达式 | 说明 |
|------|------|------------|------|
| **新闻生成** | 工作日 8:50 | `50 8 * * 1-5` | 生成 HTML 新闻报告 |
| 股票推荐 | 工作日 9:00 | `0 9 * * 1-5` | 推送股票推荐 |

---

## 📊 测试运行

**测试时间**: 2026-03-17 12:25

**运行结果**:
- ✅ 获取新闻：28 条
- ✅ 筛选重大新闻：15 条
- ✅ HTML 报告生成成功
- ✅ HTTP 服务器启动成功

---

## 🌐 访问 URL

### 新闻报告

| 页面 | URL |
|------|-----|
| **最新新闻** | http://localhost:8080/reports/news/latest.html |
| 新闻索引 | http://localhost:8080/reports/news_index.html |
| 历史新闻 | http://localhost:8080/reports/news/daily_news_YYYY-MM-DD.html |

### 股票推荐

| 页面 | URL |
|------|-----|
| 今日推荐 | http://localhost:8080/reports/stock_rec_20260317.md |

---

## 📁 文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 新闻脚本 | `scripts/daily_news_generator.py` | 主脚本 |
| HTTP 服务器 | `scripts/news_http_server.py` | Web 服务 |
| 新闻报告 | `reports/news/daily_news_YYYY-MM-DD.html` | HTML 报告 |
| 最新链接 | `reports/news/latest.html` | 符号链接 |
| 新闻索引 | `reports/news_index.html` | 索引页面 |
| 运行日志 | `logs/news_generator.log` | 运行日志 |
| 服务日志 | `logs/news_server.log` | HTTP 服务器日志 |

---

## 🔧 管理命令

```bash
# 查看定时任务
crontab -l | grep -E "(stock|news)"

# 手动运行新闻生成
cd /root/.openclaw/workspace && python3 scripts/daily_news_generator.py

# 查看最新新闻
curl http://localhost:8080/reports/news/latest.html | head -50

# 查看 HTTP 服务器状态
ps aux | grep news_http_server

# 重启 HTTP 服务器
pkill -f news_http_server
nohup python3 scripts/news_http_server.py > logs/news_server.log 2>&1 &

# 查看日志
tail -f logs/news_generator.log
tail -f logs/news_server.log
```

---

## 📰 新闻来源

### 国内新闻
- 华尔街见闻 (财经)
- 36 氪 (科技/创投)

### 国际新闻
- Hacker News (科技)

### 筛选规则
- 自动分类：经济、科技、其他
- 仅保留经济、科技类重大新闻
- 最多 15 条/天

---

## 🎨 HTML 报告特点

- 响应式设计（手机/电脑适配）
- 分类展示（经济/科技）
- 昨日重大事件回顾
- 统计信息（新闻数量）
- 美观的 UI 设计

---

## ⚠️ 注意事项

1. **HTTP 服务器**: 需要保持运行状态
2. **端口占用**: 默认使用 8080 端口
3. **网络访问**: 仅本地访问，如需外网访问需配置反向代理
4. **日志轮转**: 定期清理日志文件

---

## 🚀 外网访问配置 (可选)

### 方案 A: Nginx 反向代理

```nginx
server {
    listen 80;
    server_name news.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 方案 B: Cloudflare Tunnel

```bash
cloudflared tunnel --url http://localhost:8080
```

---

## 📋 Crontab 配置

```bash
# 每日重大新闻生成 (工作日 8:50)
50 8 * * 1-5 cd /root/.openclaw/workspace && python3 scripts/daily_news_generator.py >> logs/news_generator.log 2>&1

# 股票推荐 (工作日 9:00)
0 9 * * 1-5 cd /root/.openclaw/workspace && python3 scripts/daily_stock_recommender.py >> logs/stock_recommender.log 2>&1
```

---

## 🧪 测试验证

```bash
# 1. 运行生成器
python3 scripts/daily_news_generator.py

# 2. 检查 HTML 文件
ls -la reports/news/

# 3. 访问 URL
curl http://localhost:8080/reports/news/latest.html | head -30

# 4. 检查索引
curl http://localhost:8080/reports/news_index.html | head -20
```

---

## 🔗 相关文档

- [股票推荐配置](reports/CONFIG_FINAL.md)
- [股票过滤规则](reports/STOCK_FILTER_CONFIG.md)
- [AkShare 使用指南](skills/akshare-cn-market/USAGE.md)

---

## ✅ 总结

**配置完成！**

- ✅ 定时任务已配置 (工作日 8:50)
- ✅ HTML 报告生成成功
- ✅ HTTP 服务器已启动
- ✅ 访问 URL 可用

**访问地址**: http://localhost:8080/reports/news/latest.html

---

_星月 1 号 🌙 - 每个工作日 8:50 为你生成重大新闻报告_
