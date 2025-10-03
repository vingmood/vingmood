#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜抓取脚本
功能：抓取微博实时热搜榜数据并保存到文件
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
import pandas as pd
import logging
from typing import List, Dict, Optional
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weibo_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WeiboHotSearchCrawler:
    """微博热搜爬虫类"""
    
    def __init__(self):
        self.base_url = "https://s.weibo.com/top/summary?cate=realtimehot"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def get_hot_searches(self) -> List[Dict[str, str]]:
        """
        获取微博热搜数据
        
        Returns:
            List[Dict]: 热搜数据列表
        """
        try:
            logger.info("开始抓取微博热搜数据...")
            
            # 添加随机延迟，避免被反爬
            time.sleep(random.uniform(2, 5))
            
            # 更新请求头，模拟真实浏览器
            headers = self.headers.copy()
            headers.update({
                'Referer': 'https://s.weibo.com/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
            })
            
            response = self.session.get(self.base_url, headers=headers, timeout=15)
            response.encoding = 'utf-8'
            
            logger.info(f"请求状态码: {response.status_code}")
            logger.info(f"响应内容长度: {len(response.text)}")
            
            if response.status_code != 200:
                logger.error(f"请求失败，状态码: {response.status_code}")
                return []
            
            # 保存响应内容用于调试
            with open('debug_response.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            logger.info("响应内容已保存到 debug_response.html")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            hot_searches = []
            
            # 查找热搜列表 - 扩展选择器
            selectors = [
                'tbody tr',                    # 主要选择器
                'tr[data-rank]',              # 带排名属性的行
                '.td-02 a',                   # 备用选择器1
                'tr td a',                    # 备用选择器2
                'a[href*="weibo"]',           # 包含weibo链接的a标签
                '.m-wrap .m-main .m-box .m-table tr',  # 更具体的选择器
                'table tr',                   # 通用表格行
                '.hot-list li',               # 列表形式
                '.hot-item',                  # 热搜项目
            ]
            
            items = []
            used_selector = None
            for selector in selectors:
                items = soup.select(selector)
                if items:
                    logger.info(f"使用选择器 '{selector}' 找到 {len(items)} 个元素")
                    used_selector = selector
                    break
            
            if not items:
                logger.warning("未找到热搜数据，可能需要更新选择器")
                # 输出页面结构用于调试
                logger.info("页面标题: " + (soup.title.string if soup.title else "无标题"))
                logger.info("页面中所有链接数量: " + str(len(soup.find_all('a'))))
                return []
            
            # 解析热搜数据
            for i, item in enumerate(items[:50]):  # 限制前50条
                try:
                    if item.name == 'tr':
                        # 处理表格行
                        title_elem = item.find('a')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            link = title_elem.get('href', '')
                            if link and not link.startswith('http'):
                                link = 'https://s.weibo.com' + link
                            
                            # 获取热度值（如果有）
                            hot_value = ''
                            hot_elem = item.find('span', class_='td-03')
                            if hot_elem:
                                hot_value = hot_elem.get_text(strip=True)
                            
                            hot_searches.append({
                                'rank': i + 1,
                                'title': title,
                                'link': link,
                                'hot_value': hot_value,
                                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                    elif item.name == 'a':
                        # 处理链接元素
                        title = item.get_text(strip=True)
                        link = item.get('href', '')
                        if link and not link.startswith('http'):
                            link = 'https://s.weibo.com' + link
                        
                        hot_searches.append({
                            'rank': i + 1,
                            'title': title,
                            'link': link,
                            'hot_value': '',
                            'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                except Exception as e:
                    logger.warning(f"解析第 {i+1} 条数据时出错: {e}")
                    continue
            
            logger.info(f"成功抓取 {len(hot_searches)} 条热搜数据")
            return hot_searches
            
        except requests.RequestException as e:
            logger.error(f"网络请求错误: {e}")
            return []
        except Exception as e:
            logger.error(f"抓取过程中发生错误: {e}")
            return []
    
    def save_to_json(self, data: List[Dict], filename: str = None) -> str:
        """
        保存数据到JSON文件
        
        Args:
            data: 要保存的数据
            filename: 文件名，如果为None则自动生成
            
        Returns:
            str: 保存的文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"weibo_hot_search_{timestamp}.json"
        
        filepath = os.path.join('data', filename)
        os.makedirs('data', exist_ok=True)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已保存到: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"保存JSON文件失败: {e}")
            return ""
    
    def save_to_csv(self, data: List[Dict], filename: str = None) -> str:
        """
        保存数据到CSV文件
        
        Args:
            data: 要保存的数据
            filename: 文件名，如果为None则自动生成
            
        Returns:
            str: 保存的文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"weibo_hot_search_{timestamp}.csv"
        
        filepath = os.path.join('data', filename)
        os.makedirs('data', exist_ok=True)
        
        try:
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            logger.info(f"数据已保存到: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"保存CSV文件失败: {e}")
            return ""
    
    def save_to_excel(self, data: List[Dict], filename: str = None) -> str:
        """
        保存数据到Excel文件
        
        Args:
            data: 要保存的数据
            filename: 文件名，如果为None则自动生成
            
        Returns:
            str: 保存的文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"weibo_hot_search_{timestamp}.xlsx"
        
        filepath = os.path.join('data', filename)
        os.makedirs('data', exist_ok=True)
        
        try:
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False, engine='openpyxl')
            logger.info(f"数据已保存到: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"保存Excel文件失败: {e}")
            return ""
    
    def print_hot_searches(self, data: List[Dict], limit: int = 20):
        """
        打印热搜数据到控制台
        
        Args:
            data: 热搜数据
            limit: 显示条数限制
        """
        if not data:
            print("没有获取到热搜数据")
            return
        
        print(f"\n{'='*60}")
        print(f"微博热搜榜 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        for i, item in enumerate(data[:limit]):
            print(f"{item['rank']:2d}. {item['title']}")
            if item['hot_value']:
                print(f"     热度: {item['hot_value']}")
            print(f"     链接: {item['link']}")
            print("-" * 60)


def main():
    """主函数"""
    print("微博热搜抓取脚本启动...")
    
    # 创建爬虫实例
    crawler = WeiboHotSearchCrawler()
    
    # 获取热搜数据
    hot_searches = crawler.get_hot_searches()
    
    if not hot_searches:
        print("未能获取到热搜数据，请检查网络连接或稍后重试")
        return
    
    # 显示热搜数据
    crawler.print_hot_searches(hot_searches, limit=20)
    
    # 保存数据到不同格式
    print("\n正在保存数据...")
    
    # 保存为JSON
    json_file = crawler.save_to_json(hot_searches)
    
    # 保存为CSV
    csv_file = crawler.save_to_csv(hot_searches)
    
    # 保存为Excel
    excel_file = crawler.save_to_excel(hot_searches)
    
    print(f"\n数据保存完成:")
    if json_file:
        print(f"JSON文件: {json_file}")
    if csv_file:
        print(f"CSV文件: {csv_file}")
    if excel_file:
        print(f"Excel文件: {excel_file}")
    
    print("\n抓取完成！")


if __name__ == "__main__":
    main()