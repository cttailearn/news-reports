#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 HTTP 服务器，用于提供新闻报告访问
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = 8080
WORKSPACE = Path("/root/.openclaw/workspace")

class NewsHandler(http.server.SimpleHTTPRequestHandler):
    """自定义请求处理器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WORKSPACE), **kwargs)
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {args[0]}")
    
    def end_headers(self):
        """添加 CORS 头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()


def main():
    print("=" * 50)
    print("新闻 HTTP 服务器")
    print("=" * 50)
    
    os.chdir(WORKSPACE)
    
    with socketserver.TCPServer(("", PORT), NewsHandler) as httpd:
        print(f"服务器运行中...")
        print(f"端口：{PORT}")
        print(f"工作目录：{WORKSPACE}")
        print(f"\n访问地址:")
        print(f"  - 最新新闻：http://localhost:{PORT}/reports/news/latest.html")
        print(f"  - 新闻索引：http://localhost:{PORT}/news_index.html")
        print(f"  - 股票推荐：http://localhost:{PORT}/reports/stock_rec_*.md")
        print(f"\n按 Ctrl+C 停止服务器")
        print("=" * 50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")
            sys.exit(0)


if __name__ == "__main__":
    main()
