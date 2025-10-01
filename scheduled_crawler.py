#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜定时抓取脚本
支持定时抓取并保存数据
"""

import time
import schedule
import logging
from datetime import datetime
from weibo_hot_search import WeiboHotSearchCrawler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduled_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ScheduledCrawler:
    """定时抓取器"""
    
    def __init__(self, save_dir='hot_searches_data'):
        self.crawler = WeiboHotSearchCrawler()
        self.save_dir = save_dir
        
        # 创建保存目录
        import os
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            logger.info(f"创建保存目录: {save_dir}")
    
    def crawl_and_save(self):
        """抓取并保存数据"""
        try:
            logger.info("开始定时抓取微博热搜...")
            
            # 获取热搜数据
            hot_searches = self.crawler.get_hot_searches()
            
            if not hot_searches:
                logger.error("获取热搜数据失败")
                return False
            
            # 生成文件名（包含时间戳）
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # 保存到指定目录
            json_file = f"{self.save_dir}/weibo_hot_search_{timestamp}.json"
            csv_file = f"{self.save_dir}/weibo_hot_search_{timestamp}.csv"
            txt_file = f"{self.save_dir}/weibo_hot_search_{timestamp}.txt"
            
            self.crawler.save_to_json(hot_searches, json_file)
            self.crawler.save_to_csv(hot_searches, csv_file)
            self.crawler.save_to_txt(hot_searches, txt_file)
            
            logger.info(f"定时抓取完成，共获取 {len(hot_searches)} 条数据")
            logger.info(f"数据已保存到: {self.save_dir}")
            
            return True
            
        except Exception as e:
            logger.error(f"定时抓取失败: {e}")
            return False
    
    def start_schedule(self):
        """启动定时任务"""
        logger.info("启动定时抓取任务...")
        
        # 设置定时任务
        # 每30分钟抓取一次
        schedule.every(30).minutes.do(self.crawl_and_save)
        
        # 每天特定时间抓取
        schedule.every().day.at("09:00").do(self.crawl_and_save)
        schedule.every().day.at("12:00").do(self.crawl_and_save)
        schedule.every().day.at("18:00").do(self.crawl_and_save)
        schedule.every().day.at("21:00").do(self.crawl_and_save)
        
        # 立即执行一次
        self.crawl_and_save()
        
        logger.info("定时任务已启动，按 Ctrl+C 停止")
        
        # 运行定时任务
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            logger.info("定时任务已停止")

def main():
    """主函数"""
    print("微博热搜定时抓取脚本")
    print("=" * 40)
    
    # 创建定时抓取器
    scheduled_crawler = ScheduledCrawler()
    
    # 启动定时任务
    scheduled_crawler.start_schedule()

if __name__ == "__main__":
    main()