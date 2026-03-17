#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日重大新闻生成器
每天 8:50 运行，生成经济、科技相关的重大新闻 HTML 报告
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
import akshare as ak

# 输出目录
OUTPUT_DIR = Path("/root/.openclaw/workspace/reports/news")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 静态资源目录
STATIC_DIR = Path("/root/.openclaw/workspace/static")
STATIC_DIR.mkdir(parents=True, exist_ok=True)


def get_news_from_sources():
    """从多个来源获取新闻"""
    all_news = []
    
    # 1. 华尔街见闻
    try:
        result = subprocess.run(
            ["python3", "/root/.openclaw/workspace/skills/news-aggregator-skill/scripts/fetch_news.py",
             "--source", "wallstreetcn", "--limit", "20"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if isinstance(data, list):
                for item in data:
                    item['source'] = '华尔街见闻'
                    item['category'] = categorize_news(item.get('title', ''))
                all_news.extend(data[:10])
    except Exception as e:
        print(f"获取华尔街见闻失败：{e}")
    
    # 2. 36 氪
    try:
        result = subprocess.run(
            ["python3", "/root/.openclaw/workspace/skills/news-aggregator-skill/scripts/fetch_news.py",
             "--source", "36kr", "--limit", "20"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if isinstance(data, list):
                for item in data:
                    item['source'] = '36 氪'
                    item['category'] = categorize_news(item.get('title', ''))
                all_news.extend(data[:10])
    except Exception as e:
        print(f"获取 36 氪失败：{e}")
    
    # 3. Hacker News (科技)
    try:
        result = subprocess.run(
            ["python3", "/root/.openclaw/workspace/skills/news-aggregator-skill/scripts/fetch_news.py",
             "--source", "hackernews", "--limit", "15"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if isinstance(data, list):
                for item in data:
                    item['source'] = 'Hacker News'
                    item['category'] = '科技'
                all_news.extend(data[:8])
    except Exception as e:
        print(f"获取 Hacker News 失败：{e}")
    
    return all_news


def categorize_news(title):
    """根据标题分类新闻"""
    title_lower = title.lower()
    
    # 经济金融相关关键词
    econ_keywords = ['经济', '金融', '股市', '股票', '基金', '银行', '利率', '通胀', 'gdp', 'cpi', 
                     '央行', '美联储', '加息', '降息', '财报', '上市', '投资', '融资', '并购',
                     'trading', 'market', 'stock', 'finance', 'economic', 'fed', 'earnings']
    
    # 科技相关关键词
    tech_keywords = ['科技', 'ai', '人工智能', '芯片', '半导体', '互联网', '软件', '硬件',
                     '数据', '算法', '模型', 'llm', 'gpt', 'claude', '量子', '5g', '6g',
                     'tech', 'ai', 'chip', 'software', 'hardware', 'algorithm', 'data']
    
    for kw in econ_keywords:
        if kw in title_lower:
            return '经济'
    
    for kw in tech_keywords:
        if kw in title_lower:
            return '科技'
    
    return '其他'


def get_yesterday_news():
    """获取昨日重大新闻（模拟）"""
    # 由于新闻 API 通常只提供实时数据，这里使用 web_search 搜索昨日新闻
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y年%m月%d日")
    
    try:
        result = subprocess.run(
            ["python3", "-c", f'''
import sys
sys.path.insert(0, "/root/.openclaw/workspace/skills/tavily-search/scripts")
from search import search
results = search("昨日重大经济新闻 {yesterday}", max_results=5)
print(results)
'''],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return result.stdout[:2000]
    except:
        pass
    
    return "昨日重大新闻数据暂不可用，请关注今日新闻。"


def filter_important_news(news_list):
    """筛选重大新闻"""
    important = []
    
    for news in news_list:
        category = news.get('category', '其他')
        title = news.get('title', '')
        
        # 只保留经济、科技类
        if category in ['经济', '科技']:
            # 检查标题长度（太短的可能不重要）
            if len(title) > 10:
                important.append(news)
    
    # 按类别排序
    important.sort(key=lambda x: (0 if x['category'] in ['经济', '科技'] else 1))
    
    return important[:15]  # 最多 15 条


def generate_html(today_news, yesterday_news, date_str):
    """生成 HTML 报告"""
    
    # 按类别分组
    econ_news = [n for n in today_news if n.get('category') == '经济']
    tech_news = [n for n in today_news if n.get('category') == '科技']
    other_news = [n for n in today_news if n.get('category') == '其他']
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日重大新闻 - {date_str}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6; 
            color: #333; 
            max-width: 900px; 
            margin: 0 auto; 
            padding: 20px;
            background: #f5f5f7;
        }}
        .container {{ background: white; border-radius: 12px; padding: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
        h1 {{ 
            color: #1a1a1a; 
            font-size: 28px; 
            margin-bottom: 10px;
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 3px solid #007AFF;
        }}
        .meta {{ 
            text-align: center; 
            color: #666; 
            font-size: 14px; 
            margin-bottom: 30px;
        }}
        .section {{ margin-bottom: 35px; }}
        .section-title {{ 
            font-size: 22px; 
            color: #1a1a1a; 
            margin-bottom: 20px;
            padding-left: 12px;
            border-left: 4px solid #007AFF;
        }}
        .section-title.econ {{ border-left-color: #34C759; }}
        .section-title.tech {{ border-left-color: #5856D6; }}
        .news-item {{ 
            background: #f8f9fa; 
            border-radius: 8px; 
            padding: 15px 20px; 
            margin-bottom: 12px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .news-item:hover {{ 
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .news-title {{ 
            font-size: 16px; 
            font-weight: 600; 
            margin-bottom: 8px;
        }}
        .news-title a {{ 
            color: #1a1a1a; 
            text-decoration: none;
            transition: color 0.2s;
        }}
        .news-title a:hover {{ color: #007AFF; }}
        .news-meta {{ 
            font-size: 13px; 
            color: #666;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}
        .tag {{ 
            display: inline-block; 
            padding: 2px 8px; 
            border-radius: 4px; 
            font-size: 12px;
            font-weight: 500;
        }}
        .tag.econ {{ background: #d4edda; color: #155724; }}
        .tag.tech {{ background: #e2e0f9; color: #4a44b3; }}
        .tag.other {{ background: #f8f9fa; color: #666; border: 1px solid #ddd; }}
        .source {{ color: #007AFF; }}
        .time {{ color: #666; }}
        .yesterday-box {{ 
            background: #fff3cd; 
            border: 1px solid #ffc107; 
            border-radius: 8px; 
            padding: 20px;
            margin-bottom: 30px;
        }}
        .yesterday-box h3 {{ color: #856404; margin-bottom: 10px; }}
        .yesterday-box p {{ color: #856404; line-height: 1.8; }}
        .footer {{ 
            text-align: center; 
            margin-top: 40px; 
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #999;
            font-size: 13px;
        }}
        .stats {{ 
            display: flex; 
            gap: 20px; 
            justify-content: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        .stat-item {{ 
            background: #f8f9fa; 
            padding: 15px 25px; 
            border-radius: 8px;
            text-align: center;
        }}
        .stat-num {{ font-size: 24px; font-weight: bold; color: #007AFF; }}
        .stat-label {{ font-size: 13px; color: #666; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📰 每日重大新闻</h1>
        <div class="meta">
            生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")} | 数据日期：{date_str}
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-num">{len(econ_news)}</div>
                <div class="stat-label">经济新闻</div>
            </div>
            <div class="stat-item">
                <div class="stat-num">{len(tech_news)}</div>
                <div class="stat-label">科技新闻</div>
            </div>
            <div class="stat-item">
                <div class="stat-num">{len(today_news)}</div>
                <div class="stat-label">总计</div>
            </div>
        </div>
        
        <div class="yesterday-box">
            <h3>📅 昨日重大事件回顾</h3>
            <p>{yesterday_news}</p>
        </div>
        
        <div class="section">
            <h2 class="section-title econ">💰 经济金融</h2>
'''
    
    # 经济新闻
    for i, news in enumerate(econ_news, 1):
        html += f'''
            <div class="news-item">
                <div class="news-title">
                    <a href="{news.get('url', '#')}" target="_blank" rel="noopener">{i}. {news.get('title', '无标题')}</a>
                </div>
                <div class="news-meta">
                    <span class="tag econ">经济</span>
                    <span class="source">{news.get('source', '未知')}</span>
                    <span class="time">{news.get('time', '')}</span>
                </div>
            </div>
'''
    
    html += '''
        </div>
        
        <div class="section">
            <h2 class="section-title tech">💻 科技创新</h2>
'''
    
    # 科技新闻
    for i, news in enumerate(tech_news, 1):
        html += f'''
            <div class="news-item">
                <div class="news-title">
                    <a href="{news.get('url', '#')}" target="_blank" rel="noopener">{i}. {news.get('title', '无标题')}</a>
                </div>
                <div class="news-meta">
                    <span class="tag tech">科技</span>
                    <span class="source">{news.get('source', '未知')}</span>
                    <span class="time">{news.get('time', '')}</span>
                </div>
            </div>
'''
    
    # 其他新闻（如果有）
    if other_news:
        html += '''
        </div>
        
        <div class="section">
            <h2 class="section-title">📋 其他新闻</h2>
'''
        for i, news in enumerate(other_news, 1):
            html += f'''
            <div class="news-item">
                <div class="news-title">
                    <a href="{news.get('url', '#')}" target="_blank" rel="noopener">{i}. {news.get('title', '无标题')}</a>
                </div>
                <div class="news-meta">
                    <span class="tag other">其他</span>
                    <span class="source">{news.get('source', '未知')}</span>
                    <span class="time">{news.get('time', '')}</span>
                </div>
            </div>
'''
    
    html += f'''
        </div>
        
        <div class="footer">
            <p>本报告由 AI 自动生成 | 数据来源：华尔街见闻、36 氪、Hacker News 等</p>
            <p>定时任务：每个工作日 8:50 更新</p>
        </div>
    </div>
</body>
</html>
'''
    
    return html


def main():
    print("=" * 50)
    print("每日重大新闻生成器 - 开始运行")
    print("=" * 50)
    
    # 获取日期
    today_str = datetime.now().strftime("%Y-%m-%d")
    date_str = datetime.now().strftime("%Y年%m月%d日")
    
    print(f"数据日期：{today_str}")
    
    # 获取今日新闻
    print("获取今日新闻...")
    today_news = get_news_from_sources()
    print(f"获取新闻数：{len(today_news)}")
    
    # 筛选重大新闻
    print("筛选重大新闻...")
    important_news = filter_important_news(today_news)
    print(f"重大新闻数：{len(important_news)}")
    
    # 获取昨日新闻
    print("获取昨日重大事件...")
    yesterday_news = get_yesterday_news()
    
    # 生成 HTML
    print("生成 HTML 报告...")
    html_content = generate_html(important_news, yesterday_news, date_str)
    
    # 保存文件
    html_file = OUTPUT_DIR / f"daily_news_{today_str}.html"
    html_file.write_text(html_content, encoding='utf-8')
    print(f"报告已保存：{html_file}")
    
    # 创建最新报道的符号链接
    latest_file = OUTPUT_DIR / "latest.html"
    if latest_file.exists() or latest_file.is_symlink():
        latest_file.unlink()
    latest_file.symlink_to(html_file.name)
    print(f"最新报道链接：{latest_file}")
    
    # 生成索引页面
    generate_index()
    
    print("\n" + "=" * 50)
    print("运行完成！")
    print("=" * 50)
    print(f"\n访问 URL: http://localhost:8080/news/latest.html")


def generate_index():
    """生成索引页面"""
    html_files = sorted(OUTPUT_DIR.glob("daily_news_*.html"), reverse=True)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日重大新闻 - 索引</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6; 
            max-width: 800px; 
            margin: 40px auto; 
            padding: 20px;
            background: #f5f5f7;
        }}
        .container {{ background: white; border-radius: 12px; padding: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
        h1 {{ color: #1a1a1a; margin-bottom: 20px; text-align: center; }}
        .list {{ list-style: none; }}
        .list li {{ 
            padding: 15px; 
            border-bottom: 1px solid #eee;
            transition: background 0.2s;
        }}
        .list li:hover {{ background: #f8f9fa; }}
        .list a {{ 
            color: #007AFF; 
            text-decoration: none;
            font-size: 16px;
        }}
        .list a:hover {{ text-decoration: underline; }}
        .date {{ color: #999; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📰 每日重大新闻</h1>
        <ul class="list">
'''
    
    for i, html_file in enumerate(html_files[:30], 1):  # 最近 30 天
        date_match = html_file.stem.replace("daily_news_", "")
        html += f'''
            <li>
                <a href="news/{html_file.name}">第{i}期 - {date_match}</a>
                <span class="date">{html_file.stat().st_mtime}</span>
            </li>
'''
    
    html += '''
        </ul>
    </div>
</body>
</html>
'''
    
    index_file = OUTPUT_DIR.parent / "news_index.html"
    index_file.write_text(html, encoding='utf-8')
    print(f"索引页面已生成：{index_file}")


if __name__ == "__main__":
    main()
