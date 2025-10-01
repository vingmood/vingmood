#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜抓取脚本启动器
提供简单的命令行界面
"""

import sys
import argparse
from weibo_hot_search import WeiboHotSearchCrawler
from scheduled_crawler import ScheduledCrawler

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='微博热搜抓取脚本')
    parser.add_argument('--mode', choices=['once', 'schedule'], default='once',
                       help='运行模式：once=单次抓取，schedule=定时抓取')
    parser.add_argument('--output', '-o', help='输出文件名前缀')
    parser.add_argument('--format', choices=['json', 'csv', 'txt', 'all'], default='all',
                       help='输出格式')
    parser.add_argument('--retry', type=int, default=3, help='重试次数')
    parser.add_argument('--quiet', '-q', action='store_true', help='静默模式')
    
    args = parser.parse_args()
    
    if args.mode == 'once':
        # 单次抓取模式
        print("微博热搜抓取脚本 - 单次抓取模式")
        print("=" * 40)
        
        crawler = WeiboHotSearchCrawler()
        hot_searches = crawler.get_hot_searches(retry_times=args.retry)
        
        if not hot_searches:
            print("❌ 获取热搜数据失败")
            sys.exit(1)
        
        # 显示结果
        if not args.quiet:
            crawler.print_hot_searches(hot_searches)
        
        # 保存数据
        prefix = args.output or 'weibo_hot_search'
        
        if args.format in ['json', 'all']:
            crawler.save_to_json(hot_searches, f'{prefix}.json')
        if args.format in ['csv', 'all']:
            crawler.save_to_csv(hot_searches, f'{prefix}.csv')
        if args.format in ['txt', 'all']:
            crawler.save_to_txt(hot_searches, f'{prefix}.txt')
        
        print(f"✅ 抓取完成，共获取 {len(hot_searches)} 条数据")
        
    elif args.mode == 'schedule':
        # 定时抓取模式
        print("微博热搜抓取脚本 - 定时抓取模式")
        print("=" * 40)
        
        scheduled_crawler = ScheduledCrawler()
        scheduled_crawler.start_schedule()

if __name__ == "__main__":
    main()