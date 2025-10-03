# 微博热搜抓取脚本

一个功能完善的Python脚本，用于抓取微博热搜榜数据并保存到多种格式的文件中。

## 功能特点

- 🔥 实时抓取微博热搜榜数据
- 📊 支持多种数据格式输出（JSON、CSV、TXT）
- 🛡️ 内置反爬虫机制和重试机制
- 📝 详细的日志记录
- 🎯 智能解析多种页面结构
- ⚡ 随机延迟和User-Agent轮换

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```bash
python weibo_hot_search.py
```

### 作为模块使用

```python
from weibo_hot_search import WeiboHotSearchCrawler

# 创建爬虫实例
crawler = WeiboHotSearchCrawler()

# 获取热搜数据
hot_searches = crawler.get_hot_searches()

# 保存数据
crawler.save_to_json(hot_searches, 'hot_searches.json')
crawler.save_to_csv(hot_searches, 'hot_searches.csv')
crawler.save_to_txt(hot_searches, 'hot_searches.txt')
```

## 输出格式

### JSON格式
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

### CSV格式
```csv
rank,title,link,hot_value,timestamp
1,热搜标题,https://s.weibo.com/weibo?q=...,1234567,2024-01-01 12:00:00
```

### TXT格式
```
微博热搜榜 - 2024年01月01日 12:00:00
==================================================

1. 热搜标题
   热度: 1234567
   链接: https://s.weibo.com/weibo?q=...
   时间: 2024-01-01 12:00:00
```

## 配置选项

### 修改重试次数
```python
crawler = WeiboHotSearchCrawler()
hot_searches = crawler.get_hot_searches(retry_times=5)  # 默认3次
```

### 自定义输出文件名
```python
crawler.save_to_json(hot_searches, 'my_hot_searches.json')
crawler.save_to_csv(hot_searches, 'my_hot_searches.csv')
crawler.save_to_txt(hot_searches, 'my_hot_searches.txt')
```

## 日志记录

脚本会自动生成日志文件 `weibo_hot_search.log`，记录运行过程中的详细信息，包括：
- 请求状态
- 解析结果
- 错误信息
- 保存状态

## 注意事项

1. **遵守网站规则**：请合理使用爬虫，避免过于频繁的请求
2. **网络环境**：确保网络连接正常，能够访问微博网站
3. **反爬虫机制**：脚本已内置多种反爬虫措施，如随机延迟、User-Agent轮换等
4. **数据准确性**：由于网站结构可能变化，解析结果可能不总是100%准确

## 故障排除

### 常见问题

1. **无法获取数据**
   - 检查网络连接
   - 查看日志文件了解具体错误
   - 尝试增加重试次数

2. **解析失败**
   - 微博页面结构可能已更新
   - 检查日志中的错误信息
   - 可能需要更新解析逻辑

3. **保存失败**
   - 检查文件权限
   - 确保磁盘空间充足
   - 检查文件名是否合法

## 技术实现

- **HTTP请求**：使用 `requests` 库发送HTTP请求
- **HTML解析**：使用 `BeautifulSoup` 解析HTML内容
- **数据存储**：支持JSON、CSV、TXT三种格式
- **错误处理**：完善的异常处理和重试机制
- **日志记录**：使用Python标准库 `logging` 模块

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规和网站服务条款。

## 更新日志

- v1.0.0: 初始版本，支持基本的微博热搜抓取功能
- 支持多种输出格式
- 内置反爬虫机制
- 完善的日志记录