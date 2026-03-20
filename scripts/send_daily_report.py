#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日报告推送脚本
在新闻和股票报告生成后运行，发送 Feishu 消息推送
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

def get_latest_urls():
    """获取最新的新闻和股票报告 URL"""
    today = datetime.now().strftime("%Y-%m-%d")
    today_num = datetime.now().strftime("%Y%m%d")
    
    # 新闻 URL
    news_file = Path(f"/root/.openclaw/workspace/reports/news/daily_news_{today}.html")
    if news_file.exists():
        news_url = f"https://cttailearn.github.io/news-reports/reports/news/daily_news_{today}.html"
    else:
        # 如果今天的文件不存在，找最近的
        news_url = "https://cttailearn.github.io/news-reports/reports/news/latest.html"
    
    # 股票 URL
    stock_file = Path(f"/root/.openclaw/workspace/reports/stock_rec_{today_num}.html")
    if stock_file.exists():
        stock_url = f"https://cttailearn.github.io/news-reports/reports/stock_rec_{today_num}.html"
    else:
        # 如果今天的文件不存在，用 latest
        stock_url = "https://cttailearn.github.io/news-reports/reports/stock_rec_latest.html"
    
    return news_url, stock_url


def send_feishu_message(news_url, stock_url):
    """通过 openclaw message 工具发送 Feishu 消息"""
    today = datetime.now().strftime("%Y-%m-%d")
    weekday = datetime.now().strftime("%A")
    
    # 中文星期
    weekday_cn = {"Monday": "一", "Tuesday": "二", "Wednesday": "三", 
                  "Thursday": "四", "Friday": "五", "Saturday": "六", "Sunday": "日"}
    weekday_str = f"周{weekday_cn.get(weekday, '')}"
    
    message = f"""📰 **每日简报 - {today} {weekday_str}**

🗞️ **重大新闻**
{news_url}

📈 **股票推荐**
{stock_url}

---
_自动生成 | 工作日 9:00 更新_
_投资有风险，入市需谨慎_"""

    try:
        # 使用 openclaw message 工具发送（指定 feishu channel）
        result = subprocess.run(
            ["openclaw", "message", "send", 
             "--channel", "feishu",
             "--target", "ou_10ffc60c948cf2313f4eb6b0241cf2ed",
             "--message", message],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ Feishu 消息推送成功")
            print(f"📰 新闻：{news_url}")
            print(f"📈 股票：{stock_url}")
            return True
        else:
            print(f"⚠️ Feishu 推送失败：{result.stderr}")
            return False
            
    except Exception as e:
        print(f"⚠️ 消息推送异常：{e}")
        return False


def main():
    print("=" * 50)
    print("每日报告推送 - 开始运行")
    print("=" * 50)
    
    # 获取 URL
    print("获取最新报告 URL...")
    news_url, stock_url = get_latest_urls()
    
    print(f"新闻 URL: {news_url}")
    print(f"股票 URL: {stock_url}")
    
    # 发送消息
    print("\n发送 Feishu 消息...")
    success = send_feishu_message(news_url, stock_url)
    
    print("\n" + "=" * 50)
    if success:
        print("推送完成！")
    else:
        print("推送失败，请检查配置")
    print("=" * 50)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
