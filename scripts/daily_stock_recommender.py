#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股短线股票推荐脚本
每天 9 点运行，分析涨停板、资金流向，推荐 5 支短线股票
过滤创业板 (300/301) 和科创板 (688)
"""

import json
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import time

# 输出目录
OUTPUT_DIR = Path("/root/.openclaw/workspace/reports")
OUTPUT_DIR.mkdir(exist_ok=True)


def get_trade_date():
    """获取最近一个交易日"""
    try:
        today = datetime.now().strftime("%Y%m%d")
        df = ak.stock_zt_pool_em(date=today)
        if df is not None and len(df) > 0:
            return today
    except:
        pass
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    return yesterday


def get_zt_stocks(date):
    """获取涨停板池 - 过滤创业板和科创板"""
    try:
        df = ak.stock_zt_pool_em(date=date)
        if df is None or len(df) == 0:
            return []
        
        # 确保列存在
        required_cols = ['代码', '名称', '涨跌幅', '封板资金', '连板数', '首次封板时间', '所属行业']
        for col in required_cols:
            if col not in df.columns:
                df[col] = None
        
        # 过滤创业板 (300/301 开头) 和科创板 (688 开头)
        def is_valid_stock(code):
            code_str = str(code)
            # 排除创业板 (300/301) 和科创板 (688)
            if code_str.startswith('300') or code_str.startswith('301'):
                return False
            if code_str.startswith('688'):
                return False
            return True
        
        df = df[df['代码'].apply(is_valid_stock)].copy()
        
        # 筛选：连板数>=1，封板资金>3000 万
        filtered = df[
            (df['连板数'] >= 1) & 
            (df['封板资金'] > 30000000)
        ].copy()
        
        return filtered.to_dict('records')
    except Exception as e:
        print(f"获取涨停板失败：{e}")
        return []


def get_fund_flow():
    """获取主力资金流向"""
    try:
        df = ak.stock_market_fund_flow()
        if df is None or len(df) == 0:
            return None
        return df.tail(5).to_dict('records')
    except Exception as e:
        print(f"获取资金流向失败：{e}")
        return []


def get_sector_flow():
    """获取板块资金流向"""
    try:
        df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流向")
        if df is None or len(df) == 0:
            return []
        return df.head(5).to_dict('records')
    except Exception as e:
        print(f"获取板块流向失败：{e}")
        return []


def get_news():
    """获取财经新闻"""
    try:
        import subprocess
        result = subprocess.run(
            ["python3", "/root/.openclaw/workspace/skills/news-aggregator-skill/scripts/fetch_news.py",
             "--source", "wallstreetcn", "--limit", "10"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data[:5] if isinstance(data, list) else []
    except Exception as e:
        print(f"获取新闻失败：{e}")
    return []


def analyze_stocks_simple(zt_list):
    """简化选股逻辑 - 不查询实时 K 线，直接用涨停板数据"""
    candidates = []
    
    # 按连板数排序，优先高连板
    sorted_zt = sorted(zt_list, key=lambda x: (x.get('连板数', 0) or 0), reverse=True)
    
    for stock in sorted_zt[:10]:  # 取前 10 个候选
        try:
            code = stock['代码']
            name = stock['名称']
            lianban = stock.get('连板数', 1) or 1
            fengban = stock.get('封板资金', 0) or 0
            industry = stock.get('所属行业', '未知')
            
            # 评分逻辑
            score = 0
            reasons = []
            
            # 连板评分
            if lianban >= 3:
                score += 30
                reasons.append(f"{lianban}连板 (强势)")
            elif lianban >= 2:
                score += 20
                reasons.append(f"{lianban}连板")
            else:
                score += 10
                reasons.append("首板")
            
            # 封板资金评分
            if fengban > 100000000:
                score += 20
                reasons.append(f"封板资金{round(fengban/1000000, 1)}万 (强)")
            elif fengban > 50000000:
                score += 15
                reasons.append(f"封板资金{round(fengban/1000000, 1)}万")
            else:
                score += 10
                reasons.append(f"封板资金{round(fengban/1000000, 1)}万")
            
            # 行业热度
            if industry and industry != '未知':
                reasons.append(f"行业：{industry}")
            
            # 板块标识 (主板/中小板)
            if code.startswith('60') or code.startswith('00'):
                reasons.append("主板")
            
            candidates.append({
                'code': code,
                'name': name,
                'price': '涨停',
                'change': round(stock.get('涨跌幅', 10), 2),
                'lianban': lianban,
                'fengban': round(fengban / 1000000, 1),  # 万元
                'industry': industry,
                'reason': ' | '.join(reasons),
                'score': score,
                'first_board_time': stock.get('首次封板时间', 'N/A')
            })
        except Exception as e:
            print(f"分析 {stock.get('代码', 'unknown')} 失败：{e}")
            continue
    
    # 按评分排序
    candidates.sort(key=lambda x: -x['score'])
    return candidates[:5]


def generate_report(selected_stocks, news_list, fund_flow, sector_flow, date):
    """生成推荐报告"""
    report = []
    report.append("# A 股短线股票推荐")
    report.append(f"_生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 数据日期：{date}_\n")
    
    # 市场概览
    report.append("## 市场概览\n")
    
    if fund_flow and len(fund_flow) > 0:
        latest = fund_flow[-1]
        net_in = latest.get('主力净流入 - 净额', 0)
        report.append(f"- **主力资金净流入**: {round(net_in/100000000, 2)} 亿元")
    
    if sector_flow and len(sector_flow) > 0:
        top_sector = sector_flow[0]
        report.append(f"- **热门板块**: {top_sector.get('板块名称', 'N/A')} (+{top_sector.get('板块 - 涨跌幅', 0):.2f}%)")
    
    report.append(f"- **涨停股票数**: {len(selected_stocks)} 支候选")
    report.append(f"- **过滤**: 已排除创业板 (300/301) 和科创板 (688)")
    report.append("")
    
    # 推荐股票
    report.append("## 推荐股票 (5 支)\n")
    
    for i, stock in enumerate(selected_stocks, 1):
        report.append(f"### {i}. {stock['name']} ({stock['code']})")
        report.append(f"- **状态**: 涨停 (+{stock['change']:.1f}%)")
        report.append(f"- **连板数**: {stock['lianban']} 板")
        report.append(f"- **封板资金**: {stock['fengban']:,} 万元")
        report.append(f"- **行业**: {stock['industry']}")
        report.append(f"- **首次封板**: {stock['first_board_time']}")
        report.append(f"- **推荐理由**: {stock['reason']}")
        
        # 短线分析
        report.append("\n**短线策略**:")
        if stock['lianban'] >= 3:
            report.append("- 高连板龙头，关注继续强势")
            report.append("- 高位股波动大，设置止损位")
        elif stock['lianban'] >= 2:
            report.append("- 连板强势，有望继续上涨")
            report.append("- 关注明日竞价情况")
        else:
            report.append("- 首板启动，关注持续性")
            report.append("- 观察明日能否连板")
        
        report.append(f"- **建议仓位**: 不超过总资金 20%")
        report.append(f"- **止损位**: -5% 至 -7%")
        report.append("")
    
    # 重要新闻
    if news_list:
        report.append("## 重要新闻\n")
        for i, news in enumerate(news_list, 1):
            title = news.get('title', '无标题')
            source = news.get('source', '未知')
            time_str = news.get('time', '')
            report.append(f"{i}. **{title}** - {source} {time_str}")
        report.append("")
    
    # 风险提示
    report.append("## 风险提示")
    report.append("- 以上分析基于历史数据，不构成投资建议")
    report.append("- 短线交易风险较高，请严格执行止损")
    report.append("- 建议仓位控制：单支股票不超过总资金的 20%")
    report.append("- 市场有风险，投资需谨慎")
    report.append("")
    report.append("---")
    report.append("*本推荐由 AI 自动生成，仅供参考*")
    
    return "\n".join(report)


def send_to_feishu(content):
    """发送到飞书通道 - 保存消息文件"""
    try:
        # 截断内容到合适长度
        if len(content) > 2800:
            content = content[:2800] + "\n\n... (内容过长，已截断)"
        
        # 保存到待发送文件
        pending_file = OUTPUT_DIR / "feishu_pending_send.txt"
        pending_file.write_text(content)
        print(f"飞书消息已保存到：{pending_file}")
        
        # 同时更新 feishu_message.txt
        feishu_file = OUTPUT_DIR / "feishu_message.txt"
        feishu_file.write_text(content)
        
        return True
    except Exception as e:
        print(f"发送飞书失败：{e}")
        return False


def main():
    print("=" * 50)
    print("A 股短线股票推荐 - 开始运行")
    print("=" * 50)
    
    # 获取交易日
    trade_date = get_trade_date()
    print(f"数据日期：{trade_date}")
    
    # 获取涨停板数据
    print("获取涨停板数据 (过滤创业板/科创板)...")
    zt_list = get_zt_stocks(trade_date)
    print(f"涨停股票数：{len(zt_list)}")
    
    # 获取资金流向
    print("获取资金流向...")
    fund_flow = get_fund_flow()
    
    # 获取板块流向
    print("获取板块流向...")
    sector_flow = get_sector_flow()
    
    # 获取新闻
    print("获取财经新闻...")
    news_list = get_news()
    print(f"新闻数：{len(news_list)}")
    
    # 选股
    print("分析选股...")
    selected = analyze_stocks_simple(zt_list)
    print(f"推荐股票数：{len(selected)}")
    
    # 生成报告
    print("生成报告...")
    report = generate_report(selected, news_list, fund_flow, sector_flow, trade_date)
    
    # 保存报告
    report_file = OUTPUT_DIR / f"stock_rec_{trade_date}.md"
    report_file.write_text(report)
    print(f"报告已保存：{report_file}")
    
    # 发送到飞书
    print("\n发送到飞书通道...")
    if send_to_feishu(report):
        print("飞书消息已准备发送")
    else:
        print("飞书发送失败，消息已保存到文件")
    
    print("\n" + "=" * 50)
    print("运行完成！")
    print("=" * 50)
    
    # 打印报告预览
    print("\n报告预览:")
    print(report[:2500])


if __name__ == "__main__":
    main()
