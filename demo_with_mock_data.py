#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用模拟数据演示微博热搜市场影响分析系统
展示完整的可视化功能
"""

import json
import os
from datetime import datetime, timedelta
from market_impact_analyzer import MarketImpactAnalyzer, PriceTracker, VisualizationEngine

def create_mock_hot_searches():
    """创建模拟热搜数据"""
    return [
        {"rank": 1, "title": "人工智能ChatGPT引发热议", "link": "https://s.weibo.com/weibo?q=ChatGPT", "hot_value": "1234567", "timestamp": "2024-01-15 10:00:00"},
        {"rank": 2, "title": "新能源汽车销量创新高", "link": "https://s.weibo.com/weibo?q=新能源汽车", "hot_value": "987654", "timestamp": "2024-01-15 10:00:00"},
        {"rank": 3, "title": "房地产政策调整", "link": "https://s.weibo.com/weibo?q=房地产政策", "hot_value": "876543", "timestamp": "2024-01-15 10:00:00"},
        {"rank": 4, "title": "银行降息政策出台", "link": "https://s.weibo.com/weibo?q=银行降息", "hot_value": "765432", "timestamp": "2024-01-15 10:00:00"},
        {"rank": 5, "title": "医疗设备采购新规", "link": "https://s.weibo.com/weibo?q=医疗设备", "hot_value": "654321", "timestamp": "2024-01-15 10:00:00"}
    ]

def create_mock_stock_data():
    """创建模拟股价数据"""
    import pandas as pd
    import numpy as np
    
    # 模拟腾讯股价数据
    dates = pd.date_range(start='2023-12-15', end='2024-02-15', freq='D')
    np.random.seed(42)
    
    # 模拟价格数据（热搜前30天，热搜后30天）
    base_price = 320.0
    prices = []
    
    for i, date in enumerate(dates):
        if i < 30:  # 热搜前
            price = base_price + np.random.normal(0, 5)
        elif i == 30:  # 热搜当天
            price = base_price + 15  # 热搜导致价格上涨
        else:  # 热搜后
            price = base_price + 20 + np.random.normal(0, 8)
        
        prices.append(max(price, 100))  # 确保价格不会太低
    
    data = pd.DataFrame({
        'Close': prices,
        'Open': [p + np.random.normal(0, 2) for p in prices],
        'High': [p + abs(np.random.normal(0, 3)) for p in prices],
        'Low': [p - abs(np.random.normal(0, 3)) for p in prices],
        'Volume': [np.random.randint(1000000, 5000000) for _ in prices]
    }, index=dates)
    
    data['stock_name'] = '腾讯'
    data['symbol'] = '00700.HK'
    
    return data

def demo_complete_analysis():
    """演示完整分析流程"""
    print("🚀 微博热搜市场影响分析系统 - 模拟数据演示")
    print("=" * 60)
    
    # 初始化组件
    analyzer = MarketImpactAnalyzer()
    tracker = PriceTracker()
    visualizer = VisualizationEngine()
    
    # 创建输出目录
    output_dir = "demo_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取模拟热搜数据
    hot_searches = create_mock_hot_searches()
    print(f"📊 获取到 {len(hot_searches)} 条模拟热搜数据")
    
    # 分析每个热搜话题
    market_analyses = []
    price_analyses = []
    
    for i, hot_search in enumerate(hot_searches):
        topic = hot_search['title']
        timestamp = hot_search['timestamp']
        
        print(f"\n🔍 分析话题 {i+1}: {topic}")
        
        # 分析市场影响
        market_analysis = analyzer.analyze_topic_impact(topic, timestamp)
        market_analyses.append(market_analysis)
        
        print(f"   📈 相关市场: {market_analysis['market']}")
        print(f"   🎯 置信度: {market_analysis['confidence']:.2f}")
        print(f"   💡 是否有影响: {'是' if market_analysis['has_impact'] else '否'}")
        
        # 如果有市场影响，使用模拟数据进行股价分析
        if market_analysis['has_impact'] or market_analysis['market'] in ['科技', '汽车']:
            print(f"   📊 开始股价分析...")
            
            # 创建模拟股价分析结果
            mock_stock_data = create_mock_stock_data()
            
            # 模拟股价分析
            topic_date = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            before_data = mock_stock_data[mock_stock_data.index <= topic_date]
            after_data = mock_stock_data[mock_stock_data.index > topic_date]
            
            if not before_data.empty and not after_data.empty:
                before_avg_price = before_data['Close'].mean()
                after_avg_price = after_data['Close'].mean()
                price_change = (after_avg_price - before_avg_price) / before_avg_price * 100
                
                before_volatility = before_data['Close'].std() / before_data['Close'].mean() * 100
                after_volatility = after_data['Close'].std() / after_data['Close'].mean() * 100
                
                mock_price_analysis = {
                    'topic': topic,
                    'timestamp': timestamp,
                    'market': market_analysis['market'],
                    'analysis_period': '2023-12-15 到 2024-02-15',
                    'stock_analysis': {
                        '00700.HK': {
                            'stock_name': '腾讯',
                            'symbol': '00700.HK',
                            'before_avg_price': round(before_avg_price, 2),
                            'after_avg_price': round(after_avg_price, 2),
                            'price_change_pct': round(price_change, 2),
                            'before_volatility': round(before_volatility, 2),
                            'after_volatility': round(after_volatility, 2),
                            'max_price_before': round(before_data['Close'].max(), 2),
                            'min_price_before': round(before_data['Close'].min(), 2),
                            'max_price_after': round(after_data['Close'].max(), 2),
                            'min_price_after': round(after_data['Close'].min(), 2),
                            'data_points_before': len(before_data),
                            'data_points_after': len(after_data)
                        }
                    }
                }
                
                price_analyses.append(mock_price_analysis)
                
                print(f"   💰 腾讯股价变化: {price_change:+.2f}%")
                print(f"   📈 波动率变化: {before_volatility:.2f}% → {after_volatility:.2f}%")
                
                # 生成可视化图表
                chart_filename = f"price_analysis_{market_analysis['market']}_{i+1}.html"
                chart_path = os.path.join(output_dir, chart_filename)
                visualizer.create_price_analysis_chart(mock_price_analysis, chart_path)
                print(f"   📊 图表已生成: {chart_filename}")
    
    # 生成总结图表
    print(f"\n📊 生成市场影响总结图表...")
    summary_chart_path = os.path.join(output_dir, "market_impact_summary.html")
    visualizer.create_market_impact_summary(market_analyses, summary_chart_path)
    
    # 保存分析结果
    print(f"\n💾 保存分析结果...")
    
    # 保存热搜数据
    hot_searches_path = os.path.join(output_dir, "hot_searches.json")
    with open(hot_searches_path, 'w', encoding='utf-8') as f:
        json.dump(hot_searches, f, ensure_ascii=False, indent=2)
    
    # 保存市场分析结果
    market_analyses_path = os.path.join(output_dir, "market_analyses.json")
    with open(market_analyses_path, 'w', encoding='utf-8') as f:
        json.dump(market_analyses, f, ensure_ascii=False, indent=2)
    
    # 保存股价分析结果
    if price_analyses:
        price_analyses_path = os.path.join(output_dir, "price_analyses.json")
        with open(price_analyses_path, 'w', encoding='utf-8') as f:
            json.dump(price_analyses, f, ensure_ascii=False, indent=2)
    
    # 生成统计报告
    total_topics = len(market_analyses)
    impactful_topics = len([a for a in market_analyses if a['has_impact']])
    market_distribution = {}
    
    for analysis in market_analyses:
        market = analysis['market']
        market_distribution[market] = market_distribution.get(market, 0) + 1
    
    summary_report = {
        'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_topics_analyzed': total_topics,
        'impactful_topics': impactful_topics,
        'impact_rate': round(impactful_topics / total_topics * 100, 2) if total_topics > 0 else 0,
        'market_distribution': market_distribution,
        'price_analyses_count': len(price_analyses),
        'analysis_period': '30天前 到 30天后'
    }
    
    summary_path = os.path.join(output_dir, "summary_report.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary_report, f, ensure_ascii=False, indent=2)
    
    # 生成文本报告
    report_path = os.path.join(output_dir, "analysis_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("微博热搜市场影响分析报告 (模拟数据演示)\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"分析时间: {summary_report['analysis_time']}\n")
        f.write(f"分析话题总数: {summary_report['total_topics_analyzed']}\n")
        f.write(f"有影响话题数: {summary_report['impactful_topics']}\n")
        f.write(f"影响率: {summary_report['impact_rate']}%\n")
        f.write(f"股价分析数量: {summary_report['price_analyses_count']}\n")
        f.write(f"分析周期: {summary_report['analysis_period']}\n\n")
        
        f.write("市场分布:\n")
        f.write("-" * 20 + "\n")
        for market, count in summary_report['market_distribution'].items():
            f.write(f"{market}: {count} 个话题\n")
        f.write("\n")
        
        f.write("详细分析结果:\n")
        f.write("-" * 20 + "\n")
        
        for i, analysis in enumerate(market_analyses, 1):
            f.write(f"{i}. 话题: {analysis['topic']}\n")
            f.write(f"   市场: {analysis['market']}\n")
            f.write(f"   置信度: {analysis['confidence']:.2f}\n")
            f.write(f"   是否有影响: {'是' if analysis['has_impact'] else '否'}\n")
            f.write(f"   相关股票: {', '.join(analysis['related_stocks']) if analysis['related_stocks'] else '无'}\n")
            f.write(f"   龙头企业: {', '.join(analysis['market_leaders']) if analysis['market_leaders'] else '无'}\n")
            f.write("\n")
        
        if price_analyses:
            f.write("股价影响分析:\n")
            f.write("-" * 20 + "\n")
            
            for i, price_analysis in enumerate(price_analyses, 1):
                f.write(f"{i}. 话题: {price_analysis['topic']}\n")
                f.write(f"   市场: {price_analysis['market']}\n")
                f.write(f"   分析周期: {price_analysis['analysis_period']}\n")
                
                for symbol, stock_data in price_analysis['stock_analysis'].items():
                    f.write(f"   {stock_data['stock_name']} ({symbol}):\n")
                    f.write(f"     价格变化: {stock_data['price_change_pct']:.2f}%\n")
                    f.write(f"     热搜前平均价格: {stock_data['before_avg_price']}\n")
                    f.write(f"     热搜后平均价格: {stock_data['after_avg_price']}\n")
                    f.write(f"     波动率变化: {stock_data['before_volatility']:.2f}% -> {stock_data['after_volatility']:.2f}%\n")
                f.write("\n")
    
    print(f"\n✅ 演示完成！")
    print(f"📁 所有文件已保存到: {output_dir}")
    print(f"📊 生成的文件:")
    
    for filename in os.listdir(output_dir):
        print(f"   • {filename}")
    
    print(f"\n🌐 可视化图表:")
    print(f"   • market_impact_summary.html - 市场影响总结")
    for i in range(len(price_analyses)):
        print(f"   • price_analysis_*.html - 股价分析图表")
    
    print(f"\n💡 使用说明:")
    print(f"   1. 在浏览器中打开HTML文件查看交互式图表")
    print(f"   2. 查看JSON文件了解详细数据")
    print(f"   3. 查看TXT文件了解分析报告")

if __name__ == "__main__":
    demo_complete_analysis()