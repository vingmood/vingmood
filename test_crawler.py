#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜抓取脚本测试
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weibo_hot_search import WeiboHotSearchCrawler

def test_crawler():
    """测试爬虫功能"""
    print("开始测试微博热搜抓取脚本...")
    
    # 创建爬虫实例
    crawler = WeiboHotSearchCrawler()
    
    # 测试获取热搜数据
    print("正在获取热搜数据...")
    hot_searches = crawler.get_hot_searches()
    
    if hot_searches:
        print(f"✅ 成功获取 {len(hot_searches)} 条热搜数据")
        
        # 显示前5条数据
        print("\n前5条热搜数据：")
        for i, item in enumerate(hot_searches[:5]):
            print(f"{i+1}. {item['title']}")
            if item['hot_value']:
                print(f"   热度: {item['hot_value']}")
        
        # 测试保存功能
        print("\n测试保存功能...")
        try:
            crawler.save_to_json(hot_searches, 'test_hot_searches.json')
            crawler.save_to_csv(hot_searches, 'test_hot_searches.csv')
            crawler.save_to_txt(hot_searches, 'test_hot_searches.txt')
            print("✅ 数据保存成功")
        except Exception as e:
            print(f"❌ 数据保存失败: {e}")
            
    else:
        print("❌ 获取热搜数据失败")
        return False
    
    return True

if __name__ == "__main__":
    success = test_crawler()
    if success:
        print("\n🎉 测试完成，脚本运行正常！")
    else:
        print("\n❌ 测试失败，请检查网络连接或脚本配置")