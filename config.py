#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜抓取脚本配置文件
"""

# 抓取配置
CRAWL_CONFIG = {
    # 重试次数
    'retry_times': 3,
    
    # 请求超时时间（秒）
    'timeout': 10,
    
    # 请求间隔时间（秒）
    'delay_min': 1,
    'delay_max': 3,
    
    # 最大抓取数量
    'max_items': 50,
    
    # 保存目录
    'save_dir': 'hot_searches_data',
    
    # 日志级别
    'log_level': 'INFO',
    
    # 日志文件
    'log_file': 'weibo_hot_search.log',
}

# 定时抓取配置
SCHEDULE_CONFIG = {
    # 是否启用定时抓取
    'enabled': True,
    
    # 抓取间隔（分钟）
    'interval_minutes': 30,
    
    # 每日抓取时间点
    'daily_times': ['09:00', '12:00', '18:00', '21:00'],
    
    # 是否立即执行一次
    'run_immediately': True,
}

# 输出格式配置
OUTPUT_CONFIG = {
    # 是否保存JSON格式
    'save_json': True,
    
    # 是否保存CSV格式
    'save_csv': True,
    
    # 是否保存TXT格式
    'save_txt': True,
    
    # 是否在控制台显示
    'show_console': True,
    
    # 控制台显示数量
    'console_items': 20,
}

# 反爬虫配置
ANTI_CRAWL_CONFIG = {
    # 是否启用随机User-Agent
    'random_user_agent': True,
    
    # 是否启用随机延迟
    'random_delay': True,
    
    # 是否启用请求头轮换
    'rotate_headers': True,
    
    # 最大重试延迟（秒）
    'max_retry_delay': 5,
}

# 微博URL配置
WEIBO_URLS = [
    'https://s.weibo.com/top/summary',
    'https://s.weibo.com/top/summary?cate=realtimehot',
    'https://s.weibo.com/top/summary?cate=socialevent',
    'https://s.weibo.com/top/summary?cate=entertainment',
    'https://s.weibo.com/top/summary?cate=sports',
]

# User-Agent列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
]