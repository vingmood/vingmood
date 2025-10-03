#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜抓取脚本 (API版本)
使用微博API接口获取热搜数据
"""

import requests
import json
import csv
import time
import random
from datetime import datetime
import pandas as pd
import logging
from typing import List, Dict, Optional
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weibo_crawler_api.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WeiboHotSearchAPICrawler:
    """微博热搜爬虫类 (API版本)"""
    
    def __init__(self):
        # 微博热搜API接口
        self.api_url = "https://weibo.com/ajax/side/hotSearch"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://weibo.com/',
            'Origin': 'https://weibo.com',
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
            
            # 添加随机延迟
            time.sleep(random.uniform(1, 3))
            
            # 发送API请求
            response = self.session.get(self.api_url, timeout=10)
            
            logger.info(f"API请求状态码: {response.status_code}")
            logger.info(f"响应内容长度: {len(response.text)}")
            
            if response.status_code != 200:
                logger.error(f"API请求失败，状态码: {response.status_code}")
                return []
            
            try:
                data = response.json()
                logger.info(f"API响应数据类型: {type(data)}")
                
                # 保存响应数据用于调试
                with open('debug_api_response.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                logger.info("API响应已保存到 debug_api_response.json")
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析失败: {e}")
                # 保存原始响应用于调试
                with open('debug_api_response.txt', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                logger.info("原始响应已保存到 debug_api_response.txt")
                return []
            
            # 解析热搜数据
            hot_searches = []
            
            # 根据实际API响应结构解析
            if isinstance(data, dict) and 'data' in data:
                data_obj = data['data']
                
                # 处理实时热搜数据
                if 'realtime' in data_obj and isinstance(data_obj['realtime'], list):
                    realtime_data = data_obj['realtime']
                    logger.info(f"找到 {len(realtime_data)} 条实时热搜数据")
                    
                    for i, item in enumerate(realtime_data[:50]):  # 限制前50条
                        try:
                            if isinstance(item, dict):
                                # 提取标题
                                title = item.get('word', item.get('note', ''))
                                
                                # 提取热度值
                                hot_value = str(item.get('num', ''))
                                
                                # 生成链接
                                word_scheme = item.get('word_scheme', f"#{title}#")
                                link = f"https://s.weibo.com/weibo?q={word_scheme}"
                                
                                # 获取排名
                                rank = item.get('realpos', i + 1)
                                
                                if title:
                                    hot_searches.append({
                                        'rank': rank,
                                        'title': title,
                                        'link': link,
                                        'hot_value': hot_value,
                                        'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    })
                        except Exception as e:
                            logger.warning(f"解析第 {i+1} 条实时热搜数据时出错: {e}")
                            continue
                
                # 处理政府热搜数据
                if 'hotgovs' in data_obj and isinstance(data_obj['hotgovs'], list):
                    hotgovs_data = data_obj['hotgovs']
                    logger.info(f"找到 {len(hotgovs_data)} 条政府热搜数据")
                    
                    for i, item in enumerate(hotgovs_data):
                        try:
                            if isinstance(item, dict):
                                title = item.get('word', item.get('name', ''))
                                word_scheme = item.get('word_scheme', f"#{title}#")
                                link = f"https://s.weibo.com/weibo?q={word_scheme}"
                                pos = item.get('pos', i + 1)
                                
                                if title:
                                    hot_searches.append({
                                        'rank': pos,
                                        'title': title,
                                        'link': link,
                                        'hot_value': '政府',
                                        'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    })
                        except Exception as e:
                            logger.warning(f"解析第 {i+1} 条政府热搜数据时出错: {e}")
                            continue
            
            logger.info(f"成功抓取 {len(hot_searches)} 条热搜数据")
            return hot_searches
            
        except requests.RequestException as e:
            logger.error(f"网络请求错误: {e}")
            return []
        except Exception as e:
            logger.error(f"抓取过程中发生错误: {e}")
            return []
    
    def get_hot_searches_alternative(self) -> List[Dict[str, str]]:
        """
        备用方法：尝试其他API接口
        
        Returns:
            List[Dict]: 热搜数据列表
        """
        try:
            logger.info("尝试备用API接口...")
            
            # 备用API接口
            alt_apis = [
                "https://weibo.com/ajax/statuses/hot_band",
                "https://weibo.com/ajax/side/hotSearch",
                "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot",
            ]
            
            for api_url in alt_apis:
                try:
                    logger.info(f"尝试API: {api_url}")
                    response = self.session.get(api_url, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        logger.info(f"API {api_url} 响应成功")
                        
                        # 这里可以根据实际API响应结构进行解析
                        # 由于不同API结构可能不同，这里只是示例
                        hot_searches = []
                        
                        # 尝试解析数据
                        if isinstance(data, dict) and 'data' in data:
                            items = data['data']
                            if isinstance(items, list):
                                for i, item in enumerate(items[:50]):
                                    if isinstance(item, dict):
                                        title = item.get('word', item.get('title', ''))
                                        if title:
                                            hot_searches.append({
                                                'rank': i + 1,
                                                'title': title,
                                                'link': item.get('url', ''),
                                                'hot_value': str(item.get('hot', '')),
                                                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            })
                        
                        if hot_searches:
                            logger.info(f"备用API成功获取 {len(hot_searches)} 条数据")
                            return hot_searches
                
                except Exception as e:
                    logger.warning(f"API {api_url} 失败: {e}")
                    continue
            
            return []
            
        except Exception as e:
            logger.error(f"备用方法失败: {e}")
            return []
    
    def save_to_json(self, data: List[Dict], filename: str = None) -> str:
        """保存数据到JSON文件"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"weibo_hot_search_api_{timestamp}.json"
        
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
        """保存数据到CSV文件"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"weibo_hot_search_api_{timestamp}.csv"
        
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
    
    def print_hot_searches(self, data: List[Dict], limit: int = 20):
        """打印热搜数据到控制台"""
        if not data:
            print("没有获取到热搜数据")
            return
        
        print(f"\n{'='*60}")
        print(f"微博热搜榜 (API版本) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        for i, item in enumerate(data[:limit]):
            print(f"{item['rank']:2d}. {item['title']}")
            if item['hot_value']:
                print(f"     热度: {item['hot_value']}")
            if item['link']:
                print(f"     链接: {item['link']}")
            print("-" * 60)


def main():
    """主函数"""
    print("微博热搜抓取脚本启动 (API版本)...")
    
    # 创建爬虫实例
    crawler = WeiboHotSearchAPICrawler()
    
    # 获取热搜数据
    hot_searches = crawler.get_hot_searches()
    
    # 如果主方法失败，尝试备用方法
    if not hot_searches:
        logger.info("主API方法失败，尝试备用方法...")
        hot_searches = crawler.get_hot_searches_alternative()
    
    if not hot_searches:
        print("未能获取到热搜数据，请检查网络连接或稍后重试")
        print("提示：微博可能更新了API接口，需要更新脚本")
        return
    
    # 显示热搜数据
    crawler.print_hot_searches(hot_searches, limit=20)
    
    # 保存数据
    print("\n正在保存数据...")
    json_file = crawler.save_to_json(hot_searches)
    csv_file = crawler.save_to_csv(hot_searches)
    
    print(f"\n数据保存完成:")
    if json_file:
        print(f"JSON文件: {json_file}")
    if csv_file:
        print(f"CSV文件: {csv_file}")
    
    print("\n抓取完成！")


if __name__ == "__main__":
    main()