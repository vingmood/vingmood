#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
包含市场分析系统的各种配置参数
"""

# 微博热搜相关配置
WEIBO_CONFIG = {
    'retry_times': 3,
    'timeout': 10,
    'delay_range': (1, 3),
    'max_topics': 50
}

# 市场关键词配置
MARKET_KEYWORDS = {
    '科技': {
        'keywords': ['科技', '人工智能', 'AI', '芯片', '半导体', '5G', '互联网', '软件', '硬件', '云计算', '大数据', '区块链', '元宇宙', 'VR', 'AR', 'ChatGPT', 'OpenAI', '机器学习', '深度学习'],
        'weight': 1.0
    },
    '汽车': {
        'keywords': ['汽车', '新能源', '电动车', '特斯拉', '比亚迪', '蔚来', '小鹏', '理想', '自动驾驶', '智能汽车', '充电桩', '电池', '氢能源', '混动'],
        'weight': 1.0
    },
    '房地产': {
        'keywords': ['房地产', '房价', '楼市', '地产', '万科', '恒大', '碧桂园', '保利', '融创', '住宅', '商业地产', '物业', '土地', '建筑'],
        'weight': 1.0
    },
    '金融': {
        'keywords': ['银行', '保险', '证券', '基金', '投资', '理财', '金融', '支付', '数字货币', '央行', '利率', '汇率', '股市', '债券'],
        'weight': 1.0
    },
    '医疗': {
        'keywords': ['医疗', '医药', '疫苗', '医院', '药品', '医疗器械', '生物医药', '康美', '恒瑞', '药明康德', '爱尔眼科', '诊断', '治疗'],
        'weight': 1.0
    },
    '教育': {
        'keywords': ['教育', '学校', '培训', '在线教育', '新东方', '好未来', '猿辅导', '作业帮', '教育科技', '学习', '考试'],
        'weight': 1.0
    },
    '消费': {
        'keywords': ['消费', '零售', '电商', '淘宝', '京东', '拼多多', '美团', '饿了么', '直播', '网红', '品牌', '购物', '时尚'],
        'weight': 1.0
    },
    '能源': {
        'keywords': ['能源', '石油', '天然气', '煤炭', '电力', '新能源', '光伏', '风电', '核电', '中石油', '中石化', '太阳能'],
        'weight': 1.0
    },
    '食品': {
        'keywords': ['食品', '饮料', '白酒', '茅台', '五粮液', '伊利', '蒙牛', '康师傅', '统一', '餐饮', '外卖', '食品安全'],
        'weight': 1.0
    },
    '旅游': {
        'keywords': ['旅游', '酒店', '航空', '携程', '去哪儿', '同程', '春秋航空', '中国国旅', '景区', '度假', '出行'],
        'weight': 1.0
    }
}

# 股票代码映射配置
STOCK_SYMBOLS = {
    # 港股
    '00700.HK': {'name': '腾讯', 'market': '科技', 'sector': '互联网'},
    '09988.HK': {'name': '阿里巴巴', 'market': '科技', 'sector': '电商'},
    '09888.HK': {'name': '百度', 'market': '科技', 'sector': '搜索引擎'},
    '09618.HK': {'name': '京东', 'market': '科技', 'sector': '电商'},
    '03690.HK': {'name': '美团', 'market': '科技', 'sector': '生活服务'},
    '01810.HK': {'name': '小米', 'market': '科技', 'sector': '手机'},
    '09999.HK': {'name': '网易', 'market': '科技', 'sector': '游戏'},
    '01024.HK': {'name': '快手', 'market': '科技', 'sector': '短视频'},
    '00175.HK': {'name': '吉利汽车', 'market': '汽车', 'sector': '汽车制造'},
    '03333.HK': {'name': '恒大', 'market': '房地产', 'sector': '地产开发'},
    '02007.HK': {'name': '碧桂园', 'market': '房地产', 'sector': '地产开发'},
    '01918.HK': {'name': '融创', 'market': '房地产', 'sector': '地产开发'},
    '00960.HK': {'name': '龙湖', 'market': '房地产', 'sector': '地产开发'},
    '02319.HK': {'name': '蒙牛乳业', 'market': '食品', 'sector': '乳制品'},
    
    # A股
    '002594.SZ': {'name': '比亚迪', 'market': '汽车', 'sector': '新能源汽车'},
    '300750.SZ': {'name': '宁德时代', 'market': '汽车', 'sector': '电池'},
    '688981.SH': {'name': '中芯国际', 'market': '科技', 'sector': '半导体'},
    '601633.SH': {'name': '长城汽车', 'market': '汽车', 'sector': '汽车制造'},
    '000002.SZ': {'name': '万科', 'market': '房地产', 'sector': '地产开发'},
    '600048.SH': {'name': '保利', 'market': '房地产', 'sector': '地产开发'},
    '601398.SH': {'name': '工商银行', 'market': '金融', 'sector': '银行'},
    '601939.SH': {'name': '建设银行', 'market': '金融', 'sector': '银行'},
    '601988.SH': {'name': '中国银行', 'market': '金融', 'sector': '银行'},
    '600036.SH': {'name': '招商银行', 'market': '金融', 'sector': '银行'},
    '000001.SZ': {'name': '平安银行', 'market': '金融', 'sector': '银行'},
    '601318.SH': {'name': '中国平安', 'market': '金融', 'sector': '保险'},
    '600276.SH': {'name': '恒瑞医药', 'market': '医疗', 'sector': '制药'},
    '603259.SH': {'name': '药明康德', 'market': '医疗', 'sector': '医药服务'},
    '300015.SZ': {'name': '爱尔眼科', 'market': '医疗', 'sector': '医疗服务'},
    '300760.SZ': {'name': '迈瑞医疗', 'market': '医疗', 'sector': '医疗器械'},
    '600518.SH': {'name': '康美药业', 'market': '医疗', 'sector': '制药'},
    '600519.SH': {'name': '贵州茅台', 'market': '食品', 'sector': '白酒'},
    '000858.SZ': {'name': '五粮液', 'market': '食品', 'sector': '白酒'},
    '600887.SH': {'name': '伊利股份', 'market': '食品', 'sector': '乳制品'},
    '603288.SH': {'name': '海天味业', 'market': '食品', 'sector': '调味品'},
    '601857.SH': {'name': '中国石油', 'market': '能源', 'sector': '石油'},
    '600028.SH': {'name': '中国石化', 'market': '能源', 'sector': '石油'},
    '601088.SH': {'name': '中国神华', 'market': '能源', 'sector': '煤炭'},
    '601012.SH': {'name': '隆基绿能', 'market': '能源', 'sector': '光伏'},
    '600438.SH': {'name': '通威股份', 'market': '能源', 'sector': '光伏'},
    
    # 美股
    'TSLA': {'name': '特斯拉', 'market': '汽车', 'sector': '新能源汽车'},
    'NIO': {'name': '蔚来', 'market': '汽车', 'sector': '新能源汽车'},
    'XPEV': {'name': '小鹏', 'market': '汽车', 'sector': '新能源汽车'},
    'LI': {'name': '理想', 'market': '汽车', 'sector': '新能源汽车'}
}

# 市场龙头企业配置
MARKET_LEADERS = {
    '科技': ['腾讯', '阿里巴巴', '百度', '京东', '美团', '小米', '网易', '快手', '中芯国际'],
    '汽车': ['特斯拉', '比亚迪', '蔚来', '小鹏', '理想', '长城汽车', '吉利汽车', '宁德时代'],
    '房地产': ['万科', '恒大', '碧桂园', '保利', '融创', '龙湖'],
    '金融': ['工商银行', '建设银行', '中国银行', '招商银行', '平安银行', '中国平安'],
    '医疗': ['恒瑞医药', '药明康德', '爱尔眼科', '迈瑞医疗', '康美药业'],
    '消费': ['贵州茅台', '五粮液', '伊利股份', '蒙牛乳业', '海天味业'],
    '能源': ['中国石油', '中国石化', '中国神华', '隆基绿能', '通威股份'],
    '食品': ['贵州茅台', '五粮液', '伊利股份', '蒙牛乳业', '海天味业'],
    '旅游': ['携程', '去哪儿', '同程', '春秋航空', '中国国旅']
}

# 分析参数配置
ANALYSIS_CONFIG = {
    'default_days_before': 30,
    'default_days_after': 30,
    'min_confidence_threshold': 0.3,
    'max_topics_per_analysis': 20,
    'price_change_threshold': 5.0,  # 价格变化超过5%认为有显著影响
    'volatility_threshold': 10.0    # 波动率超过10%认为有显著变化
}

# 可视化配置
VISUALIZATION_CONFIG = {
    'chart_width': 1200,
    'chart_height': 800,
    'color_scheme': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                     '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],
    'font_size': 12,
    'title_font_size': 16,
    'save_format': 'html'  # 支持 html, png, pdf
}

# 输出配置
OUTPUT_CONFIG = {
    'output_directory': 'analysis_output',
    'create_timestamped_folders': True,
    'save_raw_data': True,
    'save_analysis_results': True,
    'save_visualizations': True,
    'generate_text_report': True
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file_encoding': 'utf-8',
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# API配置 (如果需要使用外部API)
API_CONFIG = {
    'yfinance_timeout': 30,
    'retry_attempts': 3,
    'rate_limit_delay': 1,  # 秒
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}