#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股短线股票推荐脚本 - HTML 版本
"""

import json
import akshare as ak
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_DIR = Path("/root/.openclaw/workspace/reports")
OUTPUT_DIR.mkdir(exist_ok=True)

def get_trade_date():
    try:
        today = datetime.now().strftime("%Y%m%d")
        df = ak.stock_zt_pool_em(date=today)
        if df is not None and len(df) > 0:
            return today
    except:
        pass
    return (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

def get_zt_stocks(date):
    try:
        df = ak.stock_zt_pool_em(date=date)
        if df is None or len(df) == 0:
            return []
        
        def is_valid_stock(code):
            code_str = str(code)
            return not (code_str.startswith('300') or code_str.startswith('301') or code_str.startswith('688'))
        
        df = df[df['代码'].apply(is_valid_stock)].copy()
        filtered = df[(df['连板数'] >= 1) & (df['封板资金'] > 30000000)].copy()
        return filtered.to_dict('records')
    except:
        return []

def analyze_stocks(zt_list):
    candidates = []
    for stock in sorted(zt_list, key=lambda x: x.get('连板数', 0) or 0, reverse=True)[:10]:
        try:
            candidates.append({
                'name': stock['名称'],
                'code': stock['代码'],
                'lianban': stock.get('连板数', 1) or 1,
                'fengban': round((stock.get('封板资金', 0) or 0) / 1000000, 1),
                'industry': stock.get('所属行业', '未知'),
                'first_board_time': stock.get('首次封板时间', 'N/A')
            })
        except:
            continue
    return candidates[:5]

def generate_html(stocks, date):
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>A 股短线股票推荐 - {date}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; }}
        .container {{ background: white; border-radius: 16px; padding: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
        h1 {{ text-align: center; color: #1a1a1a; border-bottom: 4px solid #ef4444; padding-bottom: 20px; }}
        .stock-card {{ background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 12px; padding: 25px; margin: 20px 0; }}
        .stock-name {{ font-size: 22px; font-weight: bold; }}
        .tag {{ display: inline-block; padding: 6px 14px; border-radius: 20px; margin: 5px; font-size: 13px; }}
        .tag-red {{ background: #fee2e2; color: #dc2626; }}
        .tag-purple {{ background: #e9d5ff; color: #7c3aed; }}
        .tag-blue {{ background: #dbeafe; color: #2563eb; }}
        .strategy-box {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 15px 0; border-radius: 8px; }}
        .warning {{ background: #fee2e2; border: 2px solid #ef4444; border-radius: 12px; padding: 25px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📈 A 股短线股票推荐</h1>
        <p style="text-align: center; color: #666;">生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")} | 数据日期：{date}</p>
        
        <h2 style="border-left: 5px solid #ef4444; padding-left: 12px;">🎯 推荐股票 ({len(stocks)} 支)</h2>
'''
    
    for i, s in enumerate(stocks, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        html += f'''
        <div class="stock-card">
            <div><span style="font-size: 24px;">{medal}</span> <span class="stock-name">{s['name']}</span> ({s['code']})</div>
            <div style="margin: 10px 0;">
                <span class="tag tag-red">{s['lianban']}连板</span>
                <span class="tag tag-purple">封板{s['fengban']}万</span>
                <span class="tag tag-blue">{s['industry']}</span>
            </div>
            <div class="strategy-box">
                <strong>💡 短线策略：</strong>
                <ul>
                    <li>建议仓位：不超过总资金 20%</li>
                    <li>止损位：-5% 至 -7%</li>
                    <li>{"高连板龙头，关注强势" if s['lianban'] >= 3 else "关注连板持续性"}</li>
                </ul>
            </div>
        </div>
'''
    
    html += '''
        <div class="warning">
            <h3 style="color: #dc2626; text-align: center;">⚠️ 风险提示</h3>
            <ul>
                <li>以上分析基于历史数据，不构成投资建议</li>
                <li>短线交易风险较高，请严格执行止损</li>
                <li>市场有风险，投资需谨慎</li>
            </ul>
        </div>
        <p style="text-align: center; color: #999; margin-top: 30px;">本报告由 AI 自动生成 | 数据来源：AkShare</p>
    </div>
</body>
</html>'''
    
    return html

def main():
    date = get_trade_date()
    zt_list = get_zt_stocks(date)
    stocks = analyze_stocks(zt_list)
    html = generate_html(stocks, date)
    
    html_file = OUTPUT_DIR / f"stock_rec_{date}.html"
    html_file.write_text(html, encoding='utf-8')
    
    latest = OUTPUT_DIR / "stock_rec_latest.html"
    if latest.exists() or latest.is_symlink():
        latest.unlink()
    latest.symlink_to(html_file.name)
    
    print(f"✅ HTML 报告已生成：{html_file}")
    print(f"🔗 访问 URL: https://cttailearn.github.io/news-reports/reports/stock_rec_{date}.html")

if __name__ == "__main__":
    main()
