# 微博热搜市场影响分析系统

一个功能完善的Python系统，用于分析微博热搜话题对市场的影响，追踪相关上市公司的股价波动，并提供可视化分析报告。

## 功能特点

- 🔥 实时抓取微博热搜榜数据
- 📊 智能识别热搜话题相关的市场领域
- 🏢 自动识别市场龙头企业
- 📈 追踪股价在热搜前后的波动情况
- 📊 支持多种数据格式输出（JSON、CSV、TXT）
- 📈 生成交互式可视化图表
- 🛡️ 内置反爬虫机制和重试机制
- 📝 详细的日志记录和分析报告
- 🎯 智能解析多种页面结构
- ⚡ 随机延迟和User-Agent轮换

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 完整市场影响分析

```bash
python integrated_analysis.py
```

选择分析模式：
- 完整分析：获取当前热搜并分析市场影响
- 特定话题分析：分析指定话题的市场影响
- 退出

### 2. 运行使用示例

```bash
python example_usage.py
```

### 3. 作为模块使用

```python
from integrated_analysis import IntegratedMarketAnalyzer

# 创建分析器实例
analyzer = IntegratedMarketAnalyzer()

# 运行完整分析
result = analyzer.run_complete_analysis(
    max_topics=10,      # 分析前10个热搜话题
    days_before=30,     # 热搜前30天
    days_after=30       # 热搜后30天
)

# 分析特定话题
result = analyzer.analyze_specific_topic(
    topic="人工智能ChatGPT引发热议",
    timestamp="2024-01-15 10:00:00",
    days_before=30,
    days_after=30
)
```

### 4. 单独使用微博热搜抓取

```bash
python weibo_hot_search.py
```

### 5. 单独使用市场分析

```bash
python market_impact_analyzer.py
```

## 输出格式

### 1. 热搜数据格式

#### JSON格式
```json
[
  {
    "rank": 1,
    "title": "热搜标题",
    "link": "https://s.weibo.com/weibo?q=...",
    "hot_value": "1234567",
    "timestamp": "2024-01-01 12:00:00"
  }
]
```

#### CSV格式
```csv
rank,title,link,hot_value,timestamp
1,热搜标题,https://s.weibo.com/weibo?q=...,1234567,2024-01-01 12:00:00
```

### 2. 市场分析结果格式

#### 市场影响分析
```json
{
  "topic": "人工智能ChatGPT引发热议",
  "timestamp": "2024-01-15 10:00:00",
  "market": "科技",
  "confidence": 0.85,
  "related_stocks": ["腾讯", "阿里巴巴", "百度"],
  "market_leaders": ["腾讯", "阿里巴巴", "百度", "京东"],
  "has_impact": true
}
```

#### 股价分析结果
```json
{
  "topic": "人工智能ChatGPT引发热议",
  "market": "科技",
  "analysis_period": "2023-12-16 到 2024-02-14",
  "stock_analysis": {
    "00700.HK": {
      "stock_name": "腾讯",
      "symbol": "00700.HK",
      "before_avg_price": 320.50,
      "after_avg_price": 335.20,
      "price_change_pct": 4.59,
      "before_volatility": 8.5,
      "after_volatility": 12.3
    }
  }
}
```

### 3. 可视化输出

系统会生成以下可视化文件：
- `market_impact_summary.html` - 市场影响总结图表
- `price_analysis_[市场]_[序号].html` - 各市场股价分析图表
- `analysis_report.txt` - 文本格式分析报告

## 配置选项

### 1. 分析参数配置

在 `config.py` 中可以修改以下参数：

```python
ANALYSIS_CONFIG = {
    'default_days_before': 30,        # 热搜前追踪天数
    'default_days_after': 30,         # 热搜后追踪天数
    'min_confidence_threshold': 0.3,  # 最小置信度阈值
    'max_topics_per_analysis': 20,    # 每次分析的最大话题数
    'price_change_threshold': 5.0,   # 价格变化阈值
    'volatility_threshold': 10.0      # 波动率阈值
}
```

### 2. 市场关键词配置

可以自定义市场关键词映射：

```python
MARKET_KEYWORDS = {
    '科技': {
        'keywords': ['科技', '人工智能', 'AI', '芯片', '半导体', '5G'],
        'weight': 1.0
    },
    # 添加更多市场...
}
```

### 3. 股票代码配置

可以添加更多股票代码：

```python
STOCK_SYMBOLS = {
    '000001.SZ': {'name': '平安银行', 'market': '金融', 'sector': '银行'},
    # 添加更多股票...
}
```

### 4. 可视化配置

```python
VISUALIZATION_CONFIG = {
    'chart_width': 1200,
    'chart_height': 800,
    'color_scheme': ['#1f77b4', '#ff7f0e', '#2ca02c'],
    'save_format': 'html'
}
```

## 日志记录

系统会自动生成以下日志文件：
- `weibo_hot_search.log` - 微博热搜抓取日志
- `market_analysis.log` - 市场分析日志
- `integrated_analysis.log` - 整合分析日志

日志记录包括：
- 请求状态和响应
- 解析结果和数据质量
- 错误信息和异常处理
- 分析进度和结果统计
- 文件保存状态

## 注意事项

1. **遵守网站规则**：请合理使用爬虫，避免过于频繁的请求
2. **网络环境**：确保网络连接正常，能够访问微博网站和股票数据源
3. **反爬虫机制**：系统已内置多种反爬虫措施，如随机延迟、User-Agent轮换等
4. **数据准确性**：由于网站结构可能变化，解析结果可能不总是100%准确
5. **股票数据**：股价数据来源于yfinance，可能存在延迟或数据不完整的情况
6. **市场识别**：市场识别基于关键词匹配，可能无法识别所有相关市场
7. **分析结果**：分析结果仅供参考，不构成投资建议

## 故障排除

### 常见问题

1. **无法获取微博热搜数据**
   - 检查网络连接
   - 查看日志文件了解具体错误
   - 尝试增加重试次数

2. **无法获取股票数据**
   - 检查网络连接和yfinance库安装
   - 确认股票代码正确
   - 检查数据源是否可用

3. **市场识别不准确**
   - 检查config.py中的关键词配置
   - 添加更多相关关键词
   - 调整置信度阈值

4. **可视化图表无法显示**
   - 检查plotly库是否正确安装
   - 确认HTML文件生成成功
   - 在浏览器中打开HTML文件

5. **解析失败**
   - 微博页面结构可能已更新
   - 检查日志中的错误信息
   - 可能需要更新解析逻辑

6. **保存失败**
   - 检查文件权限
   - 确保磁盘空间充足
   - 检查文件名是否合法

## 技术实现

### 核心组件

- **微博热搜抓取**：使用 `requests` 和 `BeautifulSoup` 抓取和解析微博热搜数据
- **市场识别**：基于关键词匹配和机器学习算法识别相关市场
- **股票数据获取**：使用 `yfinance` 库获取股价数据
- **数据分析**：使用 `pandas` 和 `numpy` 进行数据处理和分析
- **可视化**：使用 `plotly` 和 `matplotlib` 生成交互式图表
- **文本处理**：使用 `jieba` 进行中文分词和关键词提取

### 技术栈

- **HTTP请求**：`requests` 库发送HTTP请求
- **HTML解析**：`BeautifulSoup` 解析HTML内容
- **数据处理**：`pandas`, `numpy` 进行数据分析和处理
- **可视化**：`plotly`, `matplotlib`, `seaborn` 生成图表
- **股票数据**：`yfinance` 获取股价数据
- **中文处理**：`jieba` 进行中文分词
- **数据存储**：支持JSON、CSV、TXT、HTML多种格式
- **错误处理**：完善的异常处理和重试机制
- **日志记录**：使用Python标准库 `logging` 模块

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规和网站服务条款。

## 更新日志

- v2.0.0: 完整市场影响分析系统
  - 新增市场识别和分类功能
  - 新增股价数据获取和分析
  - 新增可视化图表生成
  - 新增整合分析流程
  - 支持多种分析模式

- v1.0.0: 初始版本，支持基本的微博热搜抓取功能
  - 支持多种输出格式
  - 内置反爬虫机制
  - 完善的日志记录

## 系统架构

```
微博热搜市场影响分析系统
├── weibo_hot_search.py          # 微博热搜抓取模块
├── market_impact_analyzer.py    # 市场影响分析模块
├── integrated_analysis.py       # 整合分析主程序
├── example_usage.py            # 使用示例
├── config.py                   # 配置文件
├── requirements.txt            # 依赖包列表
└── README.md                  # 使用说明
```

## 分析流程

1. **数据获取**：抓取微博热搜榜数据
2. **市场识别**：分析热搜话题，识别相关市场领域
3. **股票筛选**：确定市场龙头企业
4. **股价追踪**：获取热搜前后股价数据
5. **数据分析**：计算价格变化和波动率
6. **可视化**：生成交互式图表和报告
7. **结果输出**：保存分析结果和可视化文件