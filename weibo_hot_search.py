#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜抓取脚本
功能：抓取微博热搜榜数据并保存到文件
作者：AI Assistant
日期：2024
"""

import requests
import json
import csv
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
import logging
import os
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weibo_hot_search.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class WeiboHotSearchCrawler:
    """微博热搜抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(self.headers)
        
        # 热搜URL列表（多个备用）
        self.urls = [
            'https://s.weibo.com/top/summary',
            'https://s.weibo.com/top/summary?cate=realtimehot',
            'https://s.weibo.com/top/summary?cate=socialevent'
        ]
    
    def get_hot_searches(self, retry_times=3):
        """获取热搜数据"""
        for attempt in range(retry_times):
            try:
                logger.info(f"尝试获取热搜数据，第 {attempt + 1} 次")
                
                # 随机选择URL
                url = random.choice(self.urls)
                logger.info(f"使用URL: {url}")
                
                # 添加随机延迟
                time.sleep(random.uniform(1, 3))
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                # 检查响应内容
                if len(response.text) < 1000:
                    logger.warning("响应内容过短，可能被反爬虫")
                    continue
                
                # 解析HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                hot_searches = self.parse_hot_searches(soup)
                
                if hot_searches:
                    logger.info(f"成功获取 {len(hot_searches)} 条热搜数据")
                    return hot_searches
                else:
                    logger.warning("未找到热搜数据，尝试其他URL")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"请求失败: {e}")
                if attempt < retry_times - 1:
                    time.sleep(random.uniform(2, 5))
                    
            except Exception as e:
                logger.error(f"解析失败: {e}")
                if attempt < retry_times - 1:
                    time.sleep(random.uniform(2, 5))
        
        logger.error("所有尝试都失败了")
        return []
    
    def parse_hot_searches(self, soup):
        """解析热搜数据"""
        hot_searches = []
        
        try:
            # 方法1：尝试解析热搜列表
            hot_items = soup.select('tr[class*="tr"]')
            if not hot_items:
                # 方法2：尝试其他选择器
                hot_items = soup.select('.td-02 a')
            
            for i, item in enumerate(hot_items[:50]):  # 限制前50条
                try:
                    if 'tr' in item.get('class', []):
                        # 表格行格式
                        title_elem = item.select_one('a')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            link = title_elem.get('href', '')
                            if link and not link.startswith('http'):
                                link = 'https://s.weibo.com' + link
                            
                            # 获取热度值（如果有）
                            hot_value = ''
                            hot_elem = item.select_one('.td-03')
                            if hot_elem:
                                hot_value = hot_elem.get_text(strip=True)
                            
                            hot_searches.append({
                                'rank': i + 1,
                                'title': title,
                                'link': link,
                                'hot_value': hot_value,
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                    else:
                        # 链接格式
                        title = item.get_text(strip=True)
                        link = item.get('href', '')
                        if link and not link.startswith('http'):
                            link = 'https://s.weibo.com' + link
                        
                        hot_searches.append({
                            'rank': i + 1,
                            'title': title,
                            'link': link,
                            'hot_value': '',
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        
                except Exception as e:
                    logger.warning(f"解析第 {i+1} 条热搜时出错: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"解析热搜数据时出错: {e}")
        
        return hot_searches
    
    def save_to_json(self, data, filename=None):
        """保存为JSON格式"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'weibo_hot_search_{timestamp}.json'
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已保存到 {filename}")
        except Exception as e:
            logger.error(f"保存JSON文件失败: {e}")
    
    def save_to_csv(self, data, filename=None):
        """保存为CSV格式"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'weibo_hot_search_{timestamp}.csv'
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                if data:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
            logger.info(f"数据已保存到 {filename}")
        except Exception as e:
            logger.error(f"保存CSV文件失败: {e}")
    
    def save_to_txt(self, data, filename=None):
        """保存为TXT格式"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'weibo_hot_search_{timestamp}.txt'
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"微博热搜榜 - {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                
                for item in data:
                    f.write(f"{item['rank']}. {item['title']}\n")
                    if item['hot_value']:
                        f.write(f"   热度: {item['hot_value']}\n")
                    if item['link']:
                        f.write(f"   链接: {item['link']}\n")
                    f.write(f"   时间: {item['timestamp']}\n\n")
            
            logger.info(f"数据已保存到 {filename}")
        except Exception as e:
            logger.error(f"保存TXT文件失败: {e}")
    
    def print_hot_searches(self, data):
        """打印热搜数据到控制台"""
        print(f"\n微博热搜榜 - {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        print("=" * 60)
        
        for item in data[:20]:  # 只显示前20条
            print(f"{item['rank']:2d}. {item['title']}")
            if item['hot_value']:
                print(f"    热度: {item['hot_value']}")
            if item['link']:
                print(f"    链接: {item['link']}")
            print()

def main():
    """主函数"""
    print("微博热搜抓取脚本启动...")
    logger.info("微博热搜抓取脚本启动")
    
    crawler = WeiboHotSearchCrawler()
    
    # 获取热搜数据
    hot_searches = crawler.get_hot_searches()
    
    if not hot_searches:
        print("获取热搜数据失败，请检查网络连接或稍后重试")
        logger.error("获取热搜数据失败")
        return
    
    # 打印到控制台
    crawler.print_hot_searches(hot_searches)
    
    # 保存数据
    try:
        crawler.save_to_json(hot_searches)
        crawler.save_to_csv(hot_searches)
        crawler.save_to_txt(hot_searches)
        print(f"\n数据已保存，共获取 {len(hot_searches)} 条热搜数据")
    except Exception as e:
        logger.error(f"保存数据时出错: {e}")
        print(f"保存数据时出错: {e}")

if __name__ == "__main__":
    main()