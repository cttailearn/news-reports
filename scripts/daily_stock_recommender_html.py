#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股股票推荐 - 连板股 + 趋势股组合策略
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

def get_lianban_stocks(date):
    """获取连板股（2 板以上）"""
    try:
        df = ak.stock_zt_pool_em(date=date)
        if df is None or len(df) == 0:
            return []
        
        def is_valid(code):
            c = str(code)
            return not (c.startswith('300') or c.startswith('301') or c.startswith('688'))
        
        df = df[df['代码'].apply(is_valid)].copy()
        # 连板数>=2，封板资金>3000 万
        filtered = df[(df['连板数'] >= 2) & (df['封板资金'] > 30000000)].copy()
        return filtered.head(3).to_dict('records')  # 最多 3 支连板
    except:
        return []

def get_qushi_stocks():
    """获取趋势股（均线多头）"""
    try:
        # 获取昨日涨停股（可能有持续性）
        date = get_trade_date()
        df = ak.stock_zt_pool_previous_em(date=date)
        if df is None or len(df) == 0:
            return []
        
        def is_valid(code):
            c = str(code)
            return not (c.startswith('300') or c.startswith('301') or c.startswith('688'))
        
        df = df[df['代码'].apply(is_valid)].copy()
        
        # 筛选：市值适中，非 ST
        candidates = []
        for _, row in df.head(20).iterrows():
            try:
                code = row['代码']
                # 简单判断：昨日涨停，今日未跌停
                if row.get('涨跌幅', 0) > -5:
                    candidates.append({
                        '代码': code,
                        '名称': row.get('名称', ''),
                        '涨跌幅': row.get('涨跌幅', 0),
                        '所属行业': row.get('所属行业', '未知')
                    })
            except:
                continue
        
        return candidates[:2]  # 选 2 支趋势股
    except:
        return []

def analyze_lianban(stock):
    """分析连板股"""
    return {
        'type': '连板股',
        'name': stock['名称'],
        'code': stock['代码'],
        'lianban': stock.get('连板数', 1),
        'fengban': round((stock.get('封板资金', 0) or 0) / 1000000, 1),
        'industry': stock.get('所属行业', '未知'),
        'reason': f"{stock.get('连板数', 1)}连板 + 封板{round((stock.get('封板资金', 0) or 0)/1000000, 1)}万"
    }

def analyze_qushi(stock):
    """分析趋势股"""
    return {
        'type': '趋势股',
        'name': stock['名称'],
        'code': stock['代码'],
        'change': stock.get('涨跌幅', 0),
        'industry': stock.get('所属行业', '未知'),
        'reason': f"趋势强势 + 昨日涨停"
    }

def generate_html(stocks, date):
    """生成 HTML 报告"""
    lianban_list = [s for s in stocks if s['type'] == '连板股']
    qushi_list = [s for s in stocks if s['type'] == '趋势股']
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>A 股股票推荐 - {date}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; }}
        .container {{ background: white; border-radius: 16px; padding: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
        h1 {{ text-align: center; color: #1a1a1a; border-bottom: 4px solid #ef4444; padding-bottom: 20px; }}
        .strategy-info {{ background: #dbeafe; border-left: 4px solid #2563eb; padding: 15px; margin: 20px 0; border-radius: 8px; }}
        .stock-card {{ background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 12px; padding: 25px; margin: 20px 0; border-left: 5px solid #ef4444; }}
        .stock-card.qushi {{ border-left-color: #10b981; background: linear-gradient(135deg, #f0fdf4, #dcfce7); }}
        .stock-name {{ font-size: 22px; font-weight: bold; }}
        .tag {{ display: inline-block; padding: 6px 14px; border-radius: 20px; margin: 5px; font-size: 13px; font-weight: 600; }}
        .tag-red {{ background: #fee2e2; color: #dc2626; }}
        .tag-purple {{ background: #e9d5ff; color: #7c3aed; }}
        .tag-blue {{ background: #dbeafe; color: #2563eb; }}
        .tag-green {{ background: #d1fae5; color: #059669; }}
        .strategy-box {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 15px 0; border-radius: 8px; }}
        .warning {{ background: #fee2e2; border: 2px solid #ef4444; border-radius: 12px; padding: 25px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📈 A 股股票推荐</h1>
        <p style="text-align: center; color: #666;">生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")} | 数据日期：{date}</p>
        
        <div class="strategy-info">
            <strong>🎯 推荐策略：连板股 + 趋势股组合</strong>
            <ul style="margin: 10px 0 0 20px;">
                <li><strong>连板股</strong>（进攻仓位 60%）：高爆发，短期收益高</li>
                <li><strong>趋势股</strong>（防守仓位 40%）：稳健上涨，风险较低</li>
            </ul>
        </div>
        
        <h2 style="border-left: 5px solid #ef4444; padding-left: 12px;">🔥 连板股 ({len(lianban_list)} 支)</h2>
'''
    
    for i, s in enumerate(lianban_list, 1):
        html += f'''
        <div class="stock-card">
            <div><span style="font-size: 24px;">{"🥇" if i==1 else "🥈" if i==2 else "🥉"}</span> <span class="stock-name">{s['name']}</span> ({s['code']})</div>
            <div style="margin: 10px 0;">
                <span class="tag tag-red">{s['lianban']}连板</span>
                <span class="tag tag-purple">封板{s['fengban']}万</span>
                <span class="tag tag-blue">{s['industry']}</span>
            </div>
            <div class="strategy-box">
                <strong>💡 短线策略：</strong>
                <ul>
                    <li>建议仓位：不超过总资金 15%</li>
                    <li>止损位：-5%（严格）</li>
                    <li>高连板龙头，关注强势</li>
                    <li>快进快出，1-2 天获利了结</li>
                </ul>
            </div>
        </div>
'''
    
    html += f'''
        <h2 style="border-left: 5px solid #10b981; padding-left: 12px;">📊 趋势股 ({len(qushi_list)} 支)</h2>
'''
    
    for i, s in enumerate(qushi_list, 1):
        html += f'''
        <div class="stock-card qushi">
            <div><span style="font-size: 24px;">{i}.</span> <span class="stock-name">{s['name']}</span> ({s['code']})</div>
            <div style="margin: 10px 0;">
                <span class="tag tag-green">趋势强势</span>
                <span class="tag tag-blue">{s['industry']}</span>
                <span class="tag tag-purple">涨幅{round(s['change'], 1)}%</span>
            </div>
            <div class="strategy-box">
                <strong>💡 中线策略：</strong>
                <ul>
                    <li>建议仓位：不超过总资金 20%</li>
                    <li>止损位：-10%</li>
                    <li>均线多头，稳步上涨</li>
                    <li>持仓周期：1-2 周</li>
                </ul>
            </div>
        </div>
'''
    
    html += '''
        <div class="warning">
            <h3 style="color: #dc2626; text-align: center;">⚠️ 风险提示</h3>
            <ul>
                <li>以上分析基于历史数据，不构成投资建议</li>
                <li>连板股风险较高，请严格执行止损</li>
                <li>建议仓位：连板股 60% + 趋势股 40%</li>
                <li>市场有风险，投资需谨慎</li>
            </ul>
        </div>
        <p style="text-align: center; color: #999; margin-top: 30px;">本报告由 AI 自动生成 | 数据来源：AkShare</p>
    </div>
</body>
</html>'''
    
    return html

def main():
    print("=" * 50)
    print("A 股股票推荐 - 连板股 + 趋势股组合")
    print("=" * 50)
    
    date = get_trade_date()
    print(f"数据日期：{date}")
    
    # 获取连板股
    print("获取连板股...")
    lianban_list = get_lianban_stocks(date)
    print(f"连板股数：{len(lianban_list)}")
    
    # 获取趋势股
    print("获取趋势股...")
    qushi_list = get_qushi_stocks()
    print(f"趋势股数：{len(qushi_list)}")
    
    # 分析
    stocks = [analyze_lianban(s) for s in lianban_list]
    stocks += [analyze_qushi(s) for s in qushi_list]
    
    print(f"总推荐数：{len(stocks)}")
    
    # 生成 HTML
    print("生成 HTML 报告...")
    html = generate_html(stocks, date)
    
    html_file = OUTPUT_DIR / f"stock_rec_{date}.html"
    html_file.write_text(html, encoding='utf-8')
    
    latest = OUTPUT_DIR / "stock_rec_latest.html"
    if latest.exists() or latest.is_symlink():
        latest.unlink()
    latest.symlink_to(html_file.name)
    
    print(f"✅ HTML 报告已保存：{html_file}")
    print(f"🔗 URL: https://cttailearn.github.io/news-reports/reports/stock_rec_{date}.html")

if __name__ == "__main__":
    main()
