#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜抓取脚本使用示例
演示如何使用WeiboHotSearchCrawler类
"""

from weibo_hot_search import WeiboHotSearchCrawler
import time

def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 创建爬虫实例
    crawler = WeiboHotSearchCrawler()
    
    # 获取热搜数据
    hot_searches = crawler.get_hot_searches()
    
    if hot_searches:
        # 显示前10条热搜
        crawler.print_hot_searches(hot_searches, limit=10)
        
        # 保存数据
        crawler.save_to_json(hot_searches, "example_hot_searches.json")
        print("数据已保存到 example_hot_searches.json")
    else:
        print("未能获取到热搜数据")

def example_custom_save():
    """自定义保存示例"""
    print("\n=== 自定义保存示例 ===")
    
    crawler = WeiboHotSearchCrawler()
    hot_searches = crawler.get_hot_searches()
    
    if hot_searches:
        # 只保存前20条数据
        top_20 = hot_searches[:20]
        
        # 保存为不同格式
        json_file = crawler.save_to_json(top_20, "top_20_hot_searches.json")
        csv_file = crawler.save_to_csv(top_20, "top_20_hot_searches.csv")
        excel_file = crawler.save_to_excel(top_20, "top_20_hot_searches.xlsx")
        
        print(f"前20条热搜已保存:")
        print(f"JSON: {json_file}")
        print(f"CSV: {csv_file}")
        print(f"Excel: {excel_file}")

def example_data_analysis():
    """数据分析示例"""
    print("\n=== 数据分析示例 ===")
    
    crawler = WeiboHotSearchCrawler()
    hot_searches = crawler.get_hot_searches()
    
    if hot_searches:
        print(f"总共获取到 {len(hot_searches)} 条热搜数据")
        
        # 统计包含特定关键词的热搜
        keywords = ['电影', '新闻', '科技', '体育']
        for keyword in keywords:
            count = sum(1 for item in hot_searches if keyword in item['title'])
            print(f"包含 '{keyword}' 的热搜数量: {count}")
        
        # 显示有热度值的数据
        hot_with_value = [item for item in hot_searches if item['hot_value']]
        print(f"有热度值的数据: {len(hot_with_value)} 条")
        
        if hot_with_value:
            print("前5条有热度值的热搜:")
            for item in hot_with_value[:5]:
                print(f"  {item['rank']}. {item['title']} (热度: {item['hot_value']})")

def example_batch_crawl():
    """批量抓取示例"""
    print("\n=== 批量抓取示例 ===")
    
    crawler = WeiboHotSearchCrawler()
    
    # 模拟每小时抓取一次，共抓取3次
    for i in range(3):
        print(f"\n第 {i+1} 次抓取...")
        
        hot_searches = crawler.get_hot_searches()
        if hot_searches:
            # 保存带时间戳的数据
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"batch_crawl_{timestamp}"
            
            crawler.save_to_json(hot_searches, f"{filename}.json")
            print(f"第 {i+1} 次抓取完成，数据已保存")
        else:
            print(f"第 {i+1} 次抓取失败")
        
        # 如果不是最后一次，等待一段时间
        if i < 2:
            print("等待60秒后进行下次抓取...")
            time.sleep(60)

if __name__ == "__main__":
    print("微博热搜抓取脚本使用示例")
    print("=" * 50)
    
    try:
        # 运行各种示例
        example_basic_usage()
        example_custom_save()
        example_data_analysis()
        
        # 批量抓取示例（注释掉，避免长时间运行）
        # example_batch_crawl()
        
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
    
    print("\n示例运行完成！")