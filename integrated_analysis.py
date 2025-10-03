#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜市场影响分析系统 - 整合版本
功能：整合微博热搜抓取和市场影响分析
作者：AI Assistant
日期：2024
"""

import sys
import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 导入自定义模块
from weibo_hot_search import WeiboHotSearchCrawler
from market_impact_analyzer import MarketImpactAnalyzer, PriceTracker, VisualizationEngine

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('integrated_analysis.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IntegratedMarketAnalyzer:
    """整合的市场分析器"""
    
    def __init__(self):
        self.weibo_crawler = WeiboHotSearchCrawler()
        self.market_analyzer = MarketImpactAnalyzer()
        self.price_tracker = PriceTracker()
        self.visualizer = VisualizationEngine()
        
        # 创建输出目录
        self.output_dir = "analysis_output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def run_complete_analysis(self, max_topics: int = 10, days_before: int = 30, days_after: int = 30) -> Dict:
        """运行完整的分析流程"""
        logger.info("开始完整的微博热搜市场影响分析")
        
        # 步骤1: 获取微博热搜数据
        logger.info("步骤1: 获取微博热搜数据")
        hot_searches = self.weibo_crawler.get_hot_searches()
        
        if not hot_searches:
            logger.error("无法获取微博热搜数据")
            return {'error': '无法获取微博热搜数据'}
        
        logger.info(f"成功获取 {len(hot_searches)} 条热搜数据")
        
        # 步骤2: 分析热搜话题的市场影响
        logger.info("步骤2: 分析热搜话题的市场影响")
        market_analyses = []
        price_analyses = []
        
        for i, hot_search in enumerate(hot_searches[:max_topics]):
            topic = hot_search['title']
            timestamp = hot_search['timestamp']
            
            logger.info(f"分析话题 {i+1}/{min(max_topics, len(hot_searches))}: {topic}")
            
            # 分析市场影响
            market_analysis = self.market_analyzer.analyze_topic_impact(topic, timestamp)
            market_analyses.append(market_analysis)
            
            # 如果有市场影响，追踪股价变化
            if market_analysis['has_impact']:
                logger.info(f"话题 '{topic}' 对 {market_analysis['market']} 市场有影响，开始追踪股价")
                
                price_analysis = self.price_tracker.track_price_changes(
                    market_analysis, days_before, days_after
                )
                
                if price_analysis and price_analysis['stock_analysis']:
                    price_analyses.append(price_analysis)
                    
                    # 为每个有影响的话题创建单独的图表
                    chart_filename = f"price_analysis_{market_analysis['market']}_{i+1}.html"
                    chart_path = os.path.join(self.output_dir, chart_filename)
                    self.visualizer.create_price_analysis_chart(price_analysis, chart_path)
                    
                    logger.info(f"已生成 {market_analysis['market']} 市场的股价分析图表: {chart_filename}")
                else:
                    logger.warning(f"话题 '{topic}' 的股价数据获取失败")
            else:
                logger.info(f"话题 '{topic}' 对市场无明显影响")
        
        # 步骤3: 生成综合分析报告
        logger.info("步骤3: 生成综合分析报告")
        
        # 统计信息
        total_topics = len(market_analyses)
        impactful_topics = len([a for a in market_analyses if a['has_impact']])
        market_distribution = {}
        
        for analysis in market_analyses:
            market = analysis['market']
            market_distribution[market] = market_distribution.get(market, 0) + 1
        
        # 创建总结报告
        summary_report = {
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_topics_analyzed': total_topics,
            'impactful_topics': impactful_topics,
            'impact_rate': round(impactful_topics / total_topics * 100, 2) if total_topics > 0 else 0,
            'market_distribution': market_distribution,
            'price_analyses_count': len(price_analyses),
            'analysis_period': f"{days_before}天前 到 {days_after}天后"
        }
        
        # 步骤4: 生成可视化图表
        logger.info("步骤4: 生成可视化图表")
        
        # 市场影响总结图表
        summary_chart_path = os.path.join(self.output_dir, "market_impact_summary.html")
        self.visualizer.create_market_impact_summary(market_analyses, summary_chart_path)
        
        # 步骤5: 保存所有结果
        logger.info("步骤5: 保存分析结果")
        
        # 保存原始热搜数据
        hot_searches_path = os.path.join(self.output_dir, "hot_searches.json")
        with open(hot_searches_path, 'w', encoding='utf-8') as f:
            json.dump(hot_searches, f, ensure_ascii=False, indent=2)
        
        # 保存市场分析结果
        market_analyses_path = os.path.join(self.output_dir, "market_analyses.json")
        with open(market_analyses_path, 'w', encoding='utf-8') as f:
            json.dump(market_analyses, f, ensure_ascii=False, indent=2)
        
        # 保存股价分析结果
        if price_analyses:
            price_analyses_path = os.path.join(self.output_dir, "price_analyses.json")
            with open(price_analyses_path, 'w', encoding='utf-8') as f:
                json.dump(price_analyses, f, ensure_ascii=False, indent=2)
        
        # 保存总结报告
        summary_path = os.path.join(self.output_dir, "summary_report.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary_report, f, ensure_ascii=False, indent=2)
        
        # 生成文本报告
        self._generate_text_report(summary_report, market_analyses, price_analyses)
        
        logger.info("分析完成！")
        logger.info(f"所有结果已保存到目录: {self.output_dir}")
        
        return {
            'success': True,
            'summary': summary_report,
            'output_directory': self.output_dir,
            'files_generated': self._list_generated_files()
        }
    
    def _generate_text_report(self, summary: Dict, market_analyses: List[Dict], price_analyses: List[Dict]):
        """生成文本格式的分析报告"""
        report_path = os.path.join(self.output_dir, "analysis_report.txt")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("微博热搜市场影响分析报告\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"分析时间: {summary['analysis_time']}\n")
            f.write(f"分析话题总数: {summary['total_topics_analyzed']}\n")
            f.write(f"有影响话题数: {summary['impactful_topics']}\n")
            f.write(f"影响率: {summary['impact_rate']}%\n")
            f.write(f"股价分析数量: {summary['price_analyses_count']}\n")
            f.write(f"分析周期: {summary['analysis_period']}\n\n")
            
            f.write("市场分布:\n")
            f.write("-" * 20 + "\n")
            for market, count in summary['market_distribution'].items():
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
                        if 'error' not in stock_data:
                            f.write(f"   {stock_data['stock_name']} ({symbol}):\n")
                            f.write(f"     价格变化: {stock_data['price_change_pct']:.2f}%\n")
                            f.write(f"     热搜前平均价格: {stock_data['before_avg_price']}\n")
                            f.write(f"     热搜后平均价格: {stock_data['after_avg_price']}\n")
                            f.write(f"     波动率变化: {stock_data['before_volatility']:.2f}% -> {stock_data['after_volatility']:.2f}%\n")
                    f.write("\n")
        
        logger.info(f"文本报告已保存到: {report_path}")
    
    def _list_generated_files(self) -> List[str]:
        """列出生成的文件"""
        files = []
        if os.path.exists(self.output_dir):
            for filename in os.listdir(self.output_dir):
                files.append(filename)
        return files
    
    def analyze_specific_topic(self, topic: str, timestamp: str = None, days_before: int = 30, days_after: int = 30) -> Dict:
        """分析特定话题的市场影响"""
        if not timestamp:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info(f"分析特定话题: {topic}")
        
        # 分析市场影响
        market_analysis = self.market_analyzer.analyze_topic_impact(topic, timestamp)
        
        result = {
            'topic': topic,
            'timestamp': timestamp,
            'market_analysis': market_analysis
        }
        
        # 如果有市场影响，追踪股价变化
        if market_analysis['has_impact']:
            price_analysis = self.price_tracker.track_price_changes(
                market_analysis, days_before, days_after
            )
            
            if price_analysis and price_analysis['stock_analysis']:
                result['price_analysis'] = price_analysis
                
                # 创建图表
                chart_filename = f"specific_topic_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                chart_path = os.path.join(self.output_dir, chart_filename)
                self.visualizer.create_price_analysis_chart(price_analysis, chart_path)
                
                logger.info(f"已生成特定话题分析图表: {chart_filename}")
        
        return result

def main():
    """主函数"""
    print("微博热搜市场影响分析系统")
    print("=" * 50)
    
    analyzer = IntegratedMarketAnalyzer()
    
    # 选择分析模式
    print("\n请选择分析模式:")
    print("1. 完整分析 (获取当前热搜并分析)")
    print("2. 特定话题分析")
    print("3. 退出")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == "1":
        # 完整分析
        max_topics = input("请输入要分析的热搜话题数量 (默认10): ").strip()
        max_topics = int(max_topics) if max_topics.isdigit() else 10
        
        days_before = input("请输入热搜前追踪天数 (默认30): ").strip()
        days_before = int(days_before) if days_before.isdigit() else 30
        
        days_after = input("请输入热搜后追踪天数 (默认30): ").strip()
        days_after = int(days_after) if days_after.isdigit() else 30
        
        print(f"\n开始分析 {max_topics} 个热搜话题...")
        result = analyzer.run_complete_analysis(max_topics, days_before, days_after)
        
        if result.get('success'):
            print("\n分析完成！")
            print(f"输出目录: {result['output_directory']}")
            print(f"生成文件: {', '.join(result['files_generated'])}")
            
            summary = result['summary']
            print(f"\n分析摘要:")
            print(f"- 总话题数: {summary['total_topics_analyzed']}")
            print(f"- 有影响话题: {summary['impactful_topics']}")
            print(f"- 影响率: {summary['impact_rate']}%")
            print(f"- 股价分析数: {summary['price_analyses_count']}")
        else:
            print("分析失败，请检查日志文件")
    
    elif choice == "2":
        # 特定话题分析
        topic = input("请输入要分析的话题: ").strip()
        if topic:
            timestamp = input("请输入话题时间 (格式: YYYY-MM-DD HH:MM:SS，留空使用当前时间): ").strip()
            if not timestamp:
                timestamp = None
            
            days_before = input("请输入热搜前追踪天数 (默认30): ").strip()
            days_before = int(days_before) if days_before.isdigit() else 30
            
            days_after = input("请输入热搜后追踪天数 (默认30): ").strip()
            days_after = int(days_after) if days_after.isdigit() else 30
            
            print(f"\n开始分析话题: {topic}")
            result = analyzer.analyze_specific_topic(topic, timestamp, days_before, days_after)
            
            print("\n分析结果:")
            market_analysis = result['market_analysis']
            print(f"- 话题: {market_analysis['topic']}")
            print(f"- 相关市场: {market_analysis['market']}")
            print(f"- 置信度: {market_analysis['confidence']:.2f}")
            print(f"- 是否有影响: {'是' if market_analysis['has_impact'] else '否'}")
            
            if 'price_analysis' in result:
                print(f"- 股价分析: 已完成")
                print(f"- 相关股票: {len(result['price_analysis']['stock_analysis'])} 只")
        else:
            print("话题不能为空")
    
    elif choice == "3":
        print("退出程序")
        return
    
    else:
        print("无效选择")

if __name__ == "__main__":
    main()