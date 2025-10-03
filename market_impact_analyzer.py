#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜市场影响分析系统
功能：分析微博热搜话题对市场的影响，追踪相关上市公司股价波动
作者：AI Assistant
日期：2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import jieba
import jieba.posseg as pseg
from datetime import datetime, timedelta
import logging
import json
import os
import re
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('market_analysis.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MarketImpactAnalyzer:
    """市场影响分析器"""
    
    def __init__(self):
        self.market_keywords = self._load_market_keywords()
        self.stock_symbols = self._load_stock_symbols()
        self.market_leaders = self._load_market_leaders()
        
    def _load_market_keywords(self) -> Dict[str, List[str]]:
        """加载市场关键词映射"""
        return {
            '科技': ['科技', '人工智能', 'AI', '芯片', '半导体', '5G', '互联网', '软件', '硬件', '云计算', '大数据', '区块链', '元宇宙', 'VR', 'AR'],
            '汽车': ['汽车', '新能源', '电动车', '特斯拉', '比亚迪', '蔚来', '小鹏', '理想', '自动驾驶', '智能汽车', '充电桩', '电池'],
            '房地产': ['房地产', '房价', '楼市', '地产', '万科', '恒大', '碧桂园', '保利', '融创', '住宅', '商业地产', '物业'],
            '金融': ['银行', '保险', '证券', '基金', '投资', '理财', '金融', '支付', '数字货币', '央行', '利率', '汇率'],
            '医疗': ['医疗', '医药', '疫苗', '医院', '药品', '医疗器械', '生物医药', '康美', '恒瑞', '药明康德', '爱尔眼科'],
            '教育': ['教育', '学校', '培训', '在线教育', '新东方', '好未来', '猿辅导', '作业帮', '教育科技'],
            '消费': ['消费', '零售', '电商', '淘宝', '京东', '拼多多', '美团', '饿了么', '直播', '网红', '品牌'],
            '能源': ['能源', '石油', '天然气', '煤炭', '电力', '新能源', '光伏', '风电', '核电', '中石油', '中石化'],
            '食品': ['食品', '饮料', '白酒', '茅台', '五粮液', '伊利', '蒙牛', '康师傅', '统一', '餐饮', '外卖'],
            '旅游': ['旅游', '酒店', '航空', '携程', '去哪儿', '同程', '春秋航空', '中国国旅', '景区', '度假']
        }
    
    def _load_stock_symbols(self) -> Dict[str, str]:
        """加载股票代码映射"""
        return {
            # 科技股
            '腾讯': '00700.HK', '阿里巴巴': '09988.HK', '百度': '09888.HK', '京东': '09618.HK',
            '美团': '03690.HK', '小米': '01810.HK', '网易': '09999.HK', '快手': '01024.HK',
            '比亚迪': '002594.SZ', '宁德时代': '300750.SZ', '中芯国际': '688981.SH',
            
            # 汽车股
            '特斯拉': 'TSLA', '蔚来': 'NIO', '小鹏': 'XPEV', '理想': 'LI',
            '长城汽车': '601633.SH', '吉利汽车': '00175.HK',
            
            # 房地产股
            '万科': '000002.SZ', '恒大': '03333.HK', '碧桂园': '02007.HK', '保利': '600048.SH',
            '融创': '01918.HK', '龙湖': '00960.HK',
            
            # 金融股
            '工商银行': '601398.SH', '建设银行': '601939.SH', '中国银行': '601988.SH',
            '招商银行': '600036.SH', '平安银行': '000001.SZ', '中国平安': '601318.SH',
            
            # 医疗股
            '恒瑞医药': '600276.SH', '药明康德': '603259.SH', '爱尔眼科': '300015.SZ',
            '迈瑞医疗': '300760.SZ', '康美药业': '600518.SH',
            
            # 消费股
            '贵州茅台': '600519.SH', '五粮液': '000858.SZ', '伊利股份': '600887.SH',
            '蒙牛乳业': '02319.HK', '海天味业': '603288.SH',
            
            # 能源股
            '中国石油': '601857.SH', '中国石化': '600028.SH', '中国神华': '601088.SH',
            '隆基绿能': '601012.SH', '通威股份': '600438.SH'
        }
    
    def _load_market_leaders(self) -> Dict[str, List[str]]:
        """加载各行业龙头企业"""
        return {
            '科技': ['腾讯', '阿里巴巴', '百度', '京东', '美团', '小米', '网易', '快手'],
            '汽车': ['特斯拉', '比亚迪', '蔚来', '小鹏', '理想', '长城汽车', '吉利汽车'],
            '房地产': ['万科', '恒大', '碧桂园', '保利', '融创', '龙湖'],
            '金融': ['工商银行', '建设银行', '中国银行', '招商银行', '平安银行', '中国平安'],
            '医疗': ['恒瑞医药', '药明康德', '爱尔眼科', '迈瑞医疗', '康美药业'],
            '消费': ['贵州茅台', '五粮液', '伊利股份', '蒙牛乳业', '海天味业'],
            '能源': ['中国石油', '中国石化', '中国神华', '隆基绿能', '通威股份']
        }
    
    def classify_topic_market(self, topic: str) -> Tuple[str, float]:
        """分类热搜话题到相关市场"""
        topic_lower = topic.lower()
        market_scores = {}
        
        for market, keywords in self.market_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in topic_lower:
                    score += 1
            if score > 0:
                market_scores[market] = score
        
        if not market_scores:
            return '其他', 0.0
        
        # 返回得分最高的市场
        best_market = max(market_scores.items(), key=lambda x: x[1])
        confidence = min(best_market[1] / len(self.market_keywords[best_market[0]]), 1.0)
        
        return best_market[0], confidence
    
    def identify_related_stocks(self, market: str) -> List[str]:
        """识别相关市场的上市公司"""
        if market not in self.market_leaders:
            return []
        
        return self.market_leaders[market]
    
    def get_market_leaders(self, market: str) -> List[str]:
        """获取市场龙头企业"""
        return self.market_leaders.get(market, [])
    
    def analyze_topic_impact(self, topic: str, timestamp: str) -> Dict:
        """分析话题对市场的影响"""
        logger.info(f"分析话题: {topic}")
        
        # 分类市场
        market, confidence = self.classify_topic_market(topic)
        logger.info(f"识别市场: {market}, 置信度: {confidence:.2f}")
        
        # 获取相关股票
        related_stocks = self.identify_related_stocks(market)
        market_leaders = self.get_market_leaders(market)
        
        result = {
            'topic': topic,
            'timestamp': timestamp,
            'market': market,
            'confidence': confidence,
            'related_stocks': related_stocks,
            'market_leaders': market_leaders,
            'has_impact': confidence > 0.3 and len(related_stocks) > 0
        }
        
        return result

class StockDataFetcher:
    """股票数据获取器"""
    
    def __init__(self):
        self.stock_symbols = {
            # 港股
            '00700.HK': '腾讯', '09988.HK': '阿里巴巴', '09888.HK': '百度', '09618.HK': '京东',
            '03690.HK': '美团', '01810.HK': '小米', '09999.HK': '网易', '01024.HK': '快手',
            '00175.HK': '吉利汽车', '03333.HK': '恒大', '02007.HK': '碧桂园', '01918.HK': '融创',
            '00960.HK': '龙湖', '02319.HK': '蒙牛乳业',
            
            # A股
            '002594.SZ': '比亚迪', '300750.SZ': '宁德时代', '688981.SH': '中芯国际',
            '601633.SH': '长城汽车', '000002.SZ': '万科', '600048.SH': '保利',
            '601398.SH': '工商银行', '601939.SH': '建设银行', '601988.SH': '中国银行',
            '600036.SH': '招商银行', '000001.SZ': '平安银行', '601318.SH': '中国平安',
            '600276.SH': '恒瑞医药', '603259.SH': '药明康德', '300015.SZ': '爱尔眼科',
            '300760.SZ': '迈瑞医疗', '600518.SH': '康美药业', '600519.SH': '贵州茅台',
            '000858.SZ': '五粮液', '600887.SH': '伊利股份', '603288.SH': '海天味业',
            '601857.SH': '中国石油', '600028.SH': '中国石化', '601088.SH': '中国神华',
            '601012.SH': '隆基绿能', '600438.SH': '通威股份',
            
            # 美股
            'TSLA': '特斯拉', 'NIO': '蔚来', 'XPEV': '小鹏', 'LI': '理想'
        }
    
    def fetch_stock_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """获取股票数据"""
        try:
            import yfinance as yf
            
            stock = yf.Ticker(symbol)
            data = stock.history(start=start_date, end=end_date)
            
            if data.empty:
                logger.warning(f"未获取到 {symbol} 的数据")
                return None
            
            # 添加股票名称
            data['stock_name'] = self.stock_symbols.get(symbol, symbol)
            data['symbol'] = symbol
            
            logger.info(f"成功获取 {symbol} 的 {len(data)} 条数据")
            return data
            
        except Exception as e:
            logger.error(f"获取 {symbol} 数据失败: {e}")
            return None
    
    def fetch_multiple_stocks(self, symbols: List[str], start_date: str, end_date: str) -> Dict[str, pd.DataFrame]:
        """批量获取多只股票数据"""
        results = {}
        
        for symbol in symbols:
            data = self.fetch_stock_data(symbol, start_date, end_date)
            if data is not None:
                results[symbol] = data
        
        return results

class PriceTracker:
    """股价追踪器"""
    
    def __init__(self):
        self.data_fetcher = StockDataFetcher()
    
    def track_price_changes(self, topic_analysis: Dict, days_before: int = 30, days_after: int = 30) -> Dict:
        """追踪股价变化"""
        topic = topic_analysis['topic']
        timestamp = topic_analysis['timestamp']
        market_leaders = topic_analysis['market_leaders']
        
        if not market_leaders:
            logger.warning(f"话题 {topic} 没有找到市场龙头企业")
            return {}
        
        # 计算日期范围
        topic_date = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        start_date = (topic_date - timedelta(days=days_before)).strftime('%Y-%m-%d')
        end_date = (topic_date + timedelta(days=days_after)).strftime('%Y-%m-%d')
        
        logger.info(f"追踪时间范围: {start_date} 到 {end_date}")
        
        # 获取股票数据
        stock_symbols = []
        for leader in market_leaders:
            # 这里需要根据股票名称找到对应的代码
            symbol = self._find_stock_symbol(leader)
            if symbol:
                stock_symbols.append(symbol)
        
        if not stock_symbols:
            logger.warning("未找到有效的股票代码")
            return {}
        
        stock_data = self.data_fetcher.fetch_multiple_stocks(stock_symbols, start_date, end_date)
        
        # 分析价格变化
        price_analysis = {}
        for symbol, data in stock_data.items():
            if data.empty:
                continue
            
            analysis = self._analyze_price_changes(data, topic_date)
            price_analysis[symbol] = analysis
        
        return {
            'topic': topic,
            'timestamp': timestamp,
            'market': topic_analysis['market'],
            'analysis_period': f"{start_date} 到 {end_date}",
            'stock_analysis': price_analysis
        }
    
    def _find_stock_symbol(self, stock_name: str) -> Optional[str]:
        """根据股票名称找到代码"""
        symbol_mapping = {
            '腾讯': '00700.HK', '阿里巴巴': '09988.HK', '百度': '09888.HK', '京东': '09618.HK',
            '美团': '03690.HK', '小米': '01810.HK', '网易': '09999.HK', '快手': '01024.HK',
            '比亚迪': '002594.SZ', '宁德时代': '300750.SZ', '中芯国际': '688981.SH',
            '特斯拉': 'TSLA', '蔚来': 'NIO', '小鹏': 'XPEV', '理想': 'LI',
            '长城汽车': '601633.SH', '吉利汽车': '00175.HK', '万科': '000002.SZ',
            '恒大': '03333.HK', '碧桂园': '02007.HK', '保利': '600048.SH',
            '融创': '01918.HK', '龙湖': '00960.HK', '工商银行': '601398.SH',
            '建设银行': '601939.SH', '中国银行': '601988.SH', '招商银行': '600036.SH',
            '平安银行': '000001.SZ', '中国平安': '601318.SH', '恒瑞医药': '600276.SH',
            '药明康德': '603259.SH', '爱尔眼科': '300015.SZ', '迈瑞医疗': '300760.SZ',
            '康美药业': '600518.SH', '贵州茅台': '600519.SH', '五粮液': '000858.SZ',
            '伊利股份': '600887.SH', '蒙牛乳业': '02319.HK', '海天味业': '603288.SH',
            '中国石油': '601857.SH', '中国石化': '600028.SH', '中国神华': '601088.SH',
            '隆基绿能': '601012.SH', '通威股份': '600438.SH'
        }
        
        return symbol_mapping.get(stock_name)
    
    def _analyze_price_changes(self, data: pd.DataFrame, topic_date: datetime) -> Dict:
        """分析单只股票的价格变化"""
        data = data.copy()
        data['date'] = data.index
        
        # 找到话题日期前后的数据
        before_data = data[data['date'] <= topic_date]
        after_data = data[data['date'] > topic_date]
        
        if before_data.empty or after_data.empty:
            return {'error': '数据不足'}
        
        # 计算关键指标
        before_avg_price = before_data['Close'].mean()
        after_avg_price = after_data['Close'].mean()
        price_change = (after_avg_price - before_avg_price) / before_avg_price * 100
        
        before_volatility = before_data['Close'].std() / before_data['Close'].mean() * 100
        after_volatility = after_data['Close'].std() / after_data['Close'].mean() * 100
        
        max_price_before = before_data['Close'].max()
        min_price_before = before_data['Close'].min()
        max_price_after = after_data['Close'].max()
        min_price_after = after_data['Close'].min()
        
        return {
            'stock_name': data['stock_name'].iloc[0],
            'symbol': data['symbol'].iloc[0],
            'before_avg_price': round(before_avg_price, 2),
            'after_avg_price': round(after_avg_price, 2),
            'price_change_pct': round(price_change, 2),
            'before_volatility': round(before_volatility, 2),
            'after_volatility': round(after_volatility, 2),
            'max_price_before': round(max_price_before, 2),
            'min_price_before': round(min_price_before, 2),
            'max_price_after': round(max_price_after, 2),
            'min_price_after': round(min_price_after, 2),
            'data_points_before': len(before_data),
            'data_points_after': len(after_data)
        }

class VisualizationEngine:
    """可视化引擎"""
    
    def __init__(self):
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    def create_price_analysis_chart(self, price_analysis: Dict, save_path: str = None) -> go.Figure:
        """创建股价分析图表"""
        stock_analysis = price_analysis['stock_analysis']
        
        if not stock_analysis:
            logger.warning("没有股票分析数据")
            return None
        
        # 准备数据
        stocks = []
        price_changes = []
        volatilities_before = []
        volatilities_after = []
        
        for symbol, analysis in stock_analysis.items():
            if 'error' in analysis:
                continue
            
            stocks.append(analysis['stock_name'])
            price_changes.append(analysis['price_change_pct'])
            volatilities_before.append(analysis['before_volatility'])
            volatilities_after.append(analysis['after_volatility'])
        
        if not stocks:
            logger.warning("没有有效的股票数据")
            return None
        
        # 创建子图
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('股价变化百分比', '波动率对比', '价格变化分布', '综合影响分析'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 股价变化柱状图
        fig.add_trace(
            go.Bar(
                x=stocks,
                y=price_changes,
                name='股价变化(%)',
                marker_color=['green' if x > 0 else 'red' for x in price_changes],
                text=[f'{x:.2f}%' for x in price_changes],
                textposition='auto'
            ),
            row=1, col=1
        )
        
        # 波动率对比
        fig.add_trace(
            go.Bar(
                x=stocks,
                y=volatilities_before,
                name='热搜前波动率',
                marker_color='lightblue'
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Bar(
                x=stocks,
                y=volatilities_after,
                name='热搜后波动率',
                marker_color='orange'
            ),
            row=1, col=2
        )
        
        # 价格变化分布
        fig.add_trace(
            go.Histogram(
                x=price_changes,
                nbinsx=10,
                name='价格变化分布',
                marker_color='purple'
            ),
            row=2, col=1
        )
        
        # 综合影响分析散点图
        fig.add_trace(
            go.Scatter(
                x=volatilities_before,
                y=price_changes,
                mode='markers+text',
                text=stocks,
                textposition='top center',
                name='综合影响',
                marker=dict(
                    size=10,
                    color=price_changes,
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="价格变化(%)")
                )
            ),
            row=2, col=2
        )
        
        # 更新布局
        fig.update_layout(
            title=f"热搜话题 '{price_analysis['topic']}' 对 {price_analysis['market']} 市场的影响分析",
            height=800,
            showlegend=True,
            font=dict(size=12)
        )
        
        # 更新坐标轴标签
        fig.update_xaxes(title_text="股票", row=1, col=1)
        fig.update_yaxes(title_text="价格变化(%)", row=1, col=1)
        fig.update_xaxes(title_text="股票", row=1, col=2)
        fig.update_yaxes(title_text="波动率(%)", row=1, col=2)
        fig.update_xaxes(title_text="价格变化(%)", row=2, col=1)
        fig.update_yaxes(title_text="频次", row=2, col=1)
        fig.update_xaxes(title_text="热搜前波动率(%)", row=2, col=2)
        fig.update_yaxes(title_text="价格变化(%)", row=2, col=2)
        
        if save_path:
            fig.write_html(save_path)
            logger.info(f"图表已保存到: {save_path}")
        
        return fig
    
    def create_market_impact_summary(self, analysis_results: List[Dict], save_path: str = None) -> go.Figure:
        """创建市场影响总结图表"""
        if not analysis_results:
            logger.warning("没有分析结果数据")
            return None
        
        # 准备数据
        markets = []
        topics = []
        confidences = []
        impacts = []
        
        for result in analysis_results:
            markets.append(result['market'])
            topics.append(result['topic'])
            confidences.append(result['confidence'])
            impacts.append('有影响' if result['has_impact'] else '无影响')
        
        # 创建图表
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('市场分布', '影响程度', '话题置信度', '综合分析'),
            specs=[[{"type": "pie"}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 市场分布饼图
        market_counts = pd.Series(markets).value_counts()
        fig.add_trace(
            go.Pie(
                labels=market_counts.index,
                values=market_counts.values,
                name="市场分布"
            ),
            row=1, col=1
        )
        
        # 影响程度柱状图
        impact_counts = pd.Series(impacts).value_counts()
        fig.add_trace(
            go.Bar(
                x=impact_counts.index,
                y=impact_counts.values,
                name="影响程度",
                marker_color=['green', 'red']
            ),
            row=1, col=2
        )
        
        # 话题置信度分布
        fig.add_trace(
            go.Histogram(
                x=confidences,
                nbinsx=10,
                name="置信度分布",
                marker_color='blue'
            ),
            row=2, col=1
        )
        
        # 综合分析散点图
        fig.add_trace(
            go.Scatter(
                x=confidences,
                y=[1 if impact == '有影响' else 0 for impact in impacts],
                mode='markers+text',
                text=topics,
                textposition='top center',
                name="综合分析",
                marker=dict(
                    size=10,
                    color=confidences,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="置信度")
                )
            ),
            row=2, col=2
        )
        
        # 更新布局
        fig.update_layout(
            title="微博热搜市场影响分析总结",
            height=800,
            showlegend=True,
            font=dict(size=12)
        )
        
        # 更新坐标轴
        fig.update_yaxes(title_text="话题数量", row=1, col=2)
        fig.update_yaxes(title_text="频次", row=2, col=1)
        fig.update_xaxes(title_text="置信度", row=2, col=1)
        fig.update_yaxes(title_text="是否有影响", row=2, col=2)
        fig.update_xaxes(title_text="置信度", row=2, col=2)
        
        if save_path:
            fig.write_html(save_path)
            logger.info(f"总结图表已保存到: {save_path}")
        
        return fig

def main():
    """主函数"""
    logger.info("启动微博热搜市场影响分析系统")
    
    # 初始化组件
    analyzer = MarketImpactAnalyzer()
    tracker = PriceTracker()
    visualizer = VisualizationEngine()
    
    # 示例热搜话题
    sample_topics = [
        {"title": "人工智能ChatGPT引发热议", "timestamp": "2024-01-15 10:00:00"},
        {"title": "新能源汽车销量创新高", "timestamp": "2024-01-20 14:30:00"},
        {"title": "房地产政策调整", "timestamp": "2024-01-25 09:15:00"},
        {"title": "银行降息政策出台", "timestamp": "2024-01-30 16:45:00"},
        {"title": "医疗设备采购新规", "timestamp": "2024-02-05 11:20:00"}
    ]
    
    analysis_results = []
    
    for topic_data in sample_topics:
        logger.info(f"分析话题: {topic_data['title']}")
        
        # 分析话题影响
        topic_analysis = analyzer.analyze_topic_impact(
            topic_data['title'], 
            topic_data['timestamp']
        )
        
        if topic_analysis['has_impact']:
            # 追踪股价变化
            price_analysis = tracker.track_price_changes(topic_analysis)
            
            if price_analysis and price_analysis['stock_analysis']:
                # 创建可视化图表
                chart_path = f"price_analysis_{topic_analysis['market']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                visualizer.create_price_analysis_chart(price_analysis, chart_path)
                
                logger.info(f"已生成 {topic_analysis['market']} 市场的股价分析图表")
        
        analysis_results.append(topic_analysis)
    
    # 创建总结图表
    summary_path = f"market_impact_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    visualizer.create_market_impact_summary(analysis_results, summary_path)
    
    # 保存分析结果
    results_path = f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2)
    
    logger.info("分析完成！")
    logger.info(f"分析结果已保存到: {results_path}")
    logger.info(f"总结图表已保存到: {summary_path}")

if __name__ == "__main__":
    main()