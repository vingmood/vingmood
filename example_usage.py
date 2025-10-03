#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜市场影响分析系统 - 使用示例
演示如何使用系统进行市场影响分析
"""

from integrated_analysis import IntegratedMarketAnalyzer
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def example_complete_analysis():
    """示例：完整分析流程"""
    print("=" * 60)
    print("示例1: 完整分析流程")
    print("=" * 60)
    
    # 初始化分析器
    analyzer = IntegratedMarketAnalyzer()
    
    # 运行完整分析
    result = analyzer.run_complete_analysis(
        max_topics=5,  # 分析前5个热搜话题
        days_before=30,  # 热搜前30天
        days_after=30    # 热搜后30天
    )
    
    if result.get('success'):
        print("✅ 分析完成！")
        print(f"📁 输出目录: {result['output_directory']}")
        print(f"📄 生成文件: {', '.join(result['files_generated'])}")
        
        summary = result['summary']
        print(f"\n📊 分析摘要:")
        print(f"   • 总话题数: {summary['total_topics_analyzed']}")
        print(f"   • 有影响话题: {summary['impactful_topics']}")
        print(f"   • 影响率: {summary['impact_rate']}%")
        print(f"   • 股价分析数: {summary['price_analyses_count']}")
        
        print(f"\n🏢 市场分布:")
        for market, count in summary['market_distribution'].items():
            print(f"   • {market}: {count} 个话题")
    else:
        print("❌ 分析失败")

def example_specific_topic():
    """示例：特定话题分析"""
    print("\n" + "=" * 60)
    print("示例2: 特定话题分析")
    print("=" * 60)
    
    # 初始化分析器
    analyzer = IntegratedMarketAnalyzer()
    
    # 分析特定话题
    topics_to_analyze = [
        "人工智能ChatGPT引发热议",
        "新能源汽车销量创新高",
        "房地产政策调整",
        "银行降息政策出台"
    ]
    
    for topic in topics_to_analyze:
        print(f"\n🔍 分析话题: {topic}")
        
        result = analyzer.analyze_specific_topic(
            topic=topic,
            timestamp="2024-01-15 10:00:00",
            days_before=30,
            days_after=30
        )
        
        market_analysis = result['market_analysis']
        print(f"   📈 相关市场: {market_analysis['market']}")
        print(f"   🎯 置信度: {market_analysis['confidence']:.2f}")
        print(f"   💡 是否有影响: {'是' if market_analysis['has_impact'] else '否'}")
        
        if market_analysis['related_stocks']:
            print(f"   🏢 相关股票: {', '.join(market_analysis['related_stocks'][:3])}...")
        
        if 'price_analysis' in result:
            stock_count = len(result['price_analysis']['stock_analysis'])
            print(f"   📊 股价分析: {stock_count} 只股票")
            
            # 显示股价变化最大的股票
            max_change_stock = None
            max_change = 0
            
            for symbol, stock_data in result['price_analysis']['stock_analysis'].items():
                if 'error' not in stock_data:
                    change = abs(stock_data['price_change_pct'])
                    if change > max_change:
                        max_change = change
                        max_change_stock = stock_data
            
            if max_change_stock:
                print(f"   🚀 最大变化: {max_change_stock['stock_name']} ({max_change_stock['price_change_pct']:+.2f}%)")

def example_custom_analysis():
    """示例：自定义分析参数"""
    print("\n" + "=" * 60)
    print("示例3: 自定义分析参数")
    print("=" * 60)
    
    # 初始化分析器
    analyzer = IntegratedMarketAnalyzer()
    
    # 自定义分析参数
    custom_topic = "特斯拉Model Y降价"
    custom_timestamp = "2024-01-20 14:30:00"
    custom_days_before = 60  # 更长的追踪期
    custom_days_after = 60
    
    print(f"🔍 分析话题: {custom_topic}")
    print(f"📅 分析时间: {custom_timestamp}")
    print(f"⏰ 追踪周期: {custom_days_before}天前 到 {custom_days_after}天后")
    
    result = analyzer.analyze_specific_topic(
        topic=custom_topic,
        timestamp=custom_timestamp,
        days_before=custom_days_before,
        days_after=custom_days_after
    )
    
    market_analysis = result['market_analysis']
    print(f"\n📊 分析结果:")
    print(f"   📈 相关市场: {market_analysis['market']}")
    print(f"   🎯 置信度: {market_analysis['confidence']:.2f}")
    print(f"   💡 是否有影响: {'是' if market_analysis['has_impact'] else '否'}")
    
    if 'price_analysis' in result:
        print(f"\n📈 股价影响分析:")
        for symbol, stock_data in result['price_analysis']['stock_analysis'].items():
            if 'error' not in stock_data:
                print(f"   🏢 {stock_data['stock_name']} ({symbol}):")
                print(f"      💰 价格变化: {stock_data['price_change_pct']:+.2f}%")
                print(f"      📊 热搜前平均价格: ¥{stock_data['before_avg_price']}")
                print(f"      📊 热搜后平均价格: ¥{stock_data['after_avg_price']}")
                print(f"      📈 波动率变化: {stock_data['before_volatility']:.2f}% → {stock_data['after_volatility']:.2f}%")

def main():
    """主函数"""
    print("🚀 微博热搜市场影响分析系统 - 使用示例")
    print("本示例将演示系统的各种功能")
    
    try:
        # 示例1: 完整分析流程
        example_complete_analysis()
        
        # 示例2: 特定话题分析
        example_specific_topic()
        
        # 示例3: 自定义分析参数
        example_custom_analysis()
        
        print("\n" + "=" * 60)
        print("✅ 所有示例运行完成！")
        print("📁 请查看 'analysis_output' 目录中的分析结果")
        print("📊 生成的HTML图表可以在浏览器中打开查看")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"示例运行出错: {e}")
        print(f"❌ 示例运行出错: {e}")

if __name__ == "__main__":
    main()