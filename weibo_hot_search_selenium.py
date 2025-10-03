#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜抓取脚本 (Selenium版本)
使用Selenium模拟真实浏览器行为，绕过反爬虫机制
"""

import json
import csv
import time
import random
from datetime import datetime
import pandas as pd
import logging
from typing import List, Dict, Optional
import os

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weibo_crawler_selenium.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WeiboHotSearchSeleniumCrawler:
    """微博热搜爬虫类 (Selenium版本)"""
    
    def __init__(self, headless: bool = True):
        if not SELENIUM_AVAILABLE:
            raise ImportError("需要安装selenium库: pip install selenium")
        
        self.base_url = "https://s.weibo.com/top/summary?cate=realtimehot"
        self.headless = headless
        self.driver = None
        
    def _setup_driver(self):
        """设置Chrome驱动"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # 反检测设置
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 设置用户代理
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # 禁用图片加载以提高速度
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            # 执行反检测脚本
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Chrome驱动初始化成功")
        except Exception as e:
            logger.error(f"Chrome驱动初始化失败: {e}")
            raise
    
    def get_hot_searches(self) -> List[Dict[str, str]]:
        """
        获取微博热搜数据
        
        Returns:
            List[Dict]: 热搜数据列表
        """
        try:
            logger.info("开始抓取微博热搜数据...")
            
            # 设置驱动
            self._setup_driver()
            
            # 访问页面
            logger.info(f"访问页面: {self.base_url}")
            self.driver.get(self.base_url)
            
            # 等待页面加载
            time.sleep(random.uniform(3, 6))
            
            # 等待热搜表格加载
            try:
                wait = WebDriverWait(self.driver, 10)
                # 尝试多种可能的元素
                selectors = [
                    "tbody tr",
                    "tr[data-rank]",
                    ".td-02 a",
                    "table tr",
                    ".hot-list li"
                ]
                
                elements = []
                used_selector = None
                for selector in selectors:
                    try:
                        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
                        if elements and len(elements) > 5:  # 确保有足够的数据
                            used_selector = selector
                            logger.info(f"使用选择器 '{selector}' 找到 {len(elements)} 个元素")
                            break
                    except TimeoutException:
                        continue
                
                if not elements:
                    logger.warning("未找到热搜数据元素")
                    return []
                
            except TimeoutException:
                logger.error("页面加载超时")
                return []
            
            # 解析热搜数据
            hot_searches = []
            for i, element in enumerate(elements[:50]):  # 限制前50条
                try:
                    # 尝试多种方式获取标题和链接
                    title = ""
                    link = ""
                    hot_value = ""
                    
                    # 方法1: 查找a标签
                    try:
                        a_tag = element.find_element(By.TAG_NAME, "a")
                        title = a_tag.text.strip()
                        link = a_tag.get_attribute("href")
                    except NoSuchElementException:
                        pass
                    
                    # 方法2: 直接获取文本
                    if not title:
                        title = element.text.strip()
                    
                    # 方法3: 查找特定类名的元素
                    if not title:
                        try:
                            title_elem = element.find_element(By.CSS_SELECTOR, ".td-02 a, .hot-title, .title")
                            title = title_elem.text.strip()
                        except NoSuchElementException:
                            pass
                    
                    # 获取热度值
                    try:
                        hot_elem = element.find_element(By.CSS_SELECTOR, ".td-03, .hot-value, .heat")
                        hot_value = hot_elem.text.strip()
                    except NoSuchElementException:
                        pass
                    
                    # 处理链接
                    if link and not link.startswith('http'):
                        link = 'https://s.weibo.com' + link
                    
                    if title:  # 只有标题不为空才添加
                        hot_searches.append({
                            'rank': i + 1,
                            'title': title,
                            'link': link,
                            'hot_value': hot_value,
                            'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                
                except Exception as e:
                    logger.warning(f"解析第 {i+1} 条数据时出错: {e}")
                    continue
            
            logger.info(f"成功抓取 {len(hot_searches)} 条热搜数据")
            return hot_searches
            
        except Exception as e:
            logger.error(f"抓取过程中发生错误: {e}")
            return []
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("浏览器已关闭")
    
    def save_to_json(self, data: List[Dict], filename: str = None) -> str:
        """保存数据到JSON文件"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"weibo_hot_search_selenium_{timestamp}.json"
        
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
            filename = f"weibo_hot_search_selenium_{timestamp}.csv"
        
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
        print(f"微博热搜榜 (Selenium版本) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        for i, item in enumerate(data[:limit]):
            print(f"{item['rank']:2d}. {item['title']}")
            if item['hot_value']:
                print(f"     热度: {item['hot_value']}")
            print(f"     链接: {item['link']}")
            print("-" * 60)


def main():
    """主函数"""
    print("微博热搜抓取脚本启动 (Selenium版本)...")
    
    if not SELENIUM_AVAILABLE:
        print("错误: 需要安装selenium库")
        print("请运行: pip install selenium")
        return
    
    try:
        # 创建爬虫实例
        crawler = WeiboHotSearchSeleniumCrawler(headless=True)
        
        # 获取热搜数据
        hot_searches = crawler.get_hot_searches()
        
        if not hot_searches:
            print("未能获取到热搜数据，请检查网络连接或稍后重试")
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
        
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
        print(f"程序运行出错: {e}")


if __name__ == "__main__":
    main()