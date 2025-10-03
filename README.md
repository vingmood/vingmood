# 微博热搜抓取脚本

一个功能完善的Python脚本集合，用于抓取微博实时热搜榜数据并保存到多种格式的文件中。

## 脚本版本

本项目包含三个不同版本的抓取脚本：

1. **`weibo_hot_search.py`** - 基础版本（使用requests + BeautifulSoup）
2. **`weibo_hot_search_selenium.py`** - 高级版本（使用Selenium模拟浏览器）
3. **`weibo_hot_search_api.py`** - API版本（直接调用微博API接口）

## 功能特点

- 🚀 实时抓取微博热搜榜数据
- 📊 支持多种数据格式输出（JSON、CSV、Excel）
- 🛡️ 内置反爬虫机制（随机延迟、请求头伪装、浏览器模拟）
- 📝 完整的日志记录
- 🔄 错误处理和重试机制
- 🎯 灵活的数据筛选和显示
- 🌐 多种抓取方式，提高成功率

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 基础版本（推荐新手）

```bash
python weibo_hot_search.py
```

### 2. Selenium版本（推荐高级用户）

```bash
# 需要先安装Chrome浏览器和ChromeDriver
python weibo_hot_search_selenium.py
```

### 3. API版本（推荐稳定使用）

```bash
python weibo_hot_search_api.py
```

### 作为模块使用

```python
# 基础版本
from weibo_hot_search import WeiboHotSearchCrawler

# Selenium版本
from weibo_hot_search_selenium import WeiboHotSearchSeleniumCrawler

# API版本
from weibo_hot_search_api import WeiboHotSearchAPICrawler

# 创建爬虫实例
crawler = WeiboHotSearchAPICrawler()  # 推荐使用API版本

# 获取热搜数据
hot_searches = crawler.get_hot_searches()

# 保存数据
crawler.save_to_json(hot_searches)
crawler.save_to_csv(hot_searches)

# 打印数据
crawler.print_hot_searches(hot_searches, limit=10)
```

## 输出格式

### 控制台输出
```
============================================================
微博热搜榜 - 2024-01-15 14:30:25
============================================================
 1. 某明星新电影上映
     热度: 1234567
     链接: https://s.weibo.com/weibo?q=某明星新电影上映
------------------------------------------------------------
 2. 重要新闻事件
     热度: 987654
     链接: https://s.weibo.com/weibo?q=重要新闻事件
------------------------------------------------------------
...
```

### 文件输出

数据会保存到 `data/` 目录下，包含以下字段：
- `rank`: 排名
- `title`: 热搜标题
- `link`: 相关链接
- `hot_value`: 热度值（如果可用）
- `crawl_time`: 抓取时间

## 配置选项

### 修改请求头
```python
crawler = WeiboHotSearchCrawler()
crawler.headers.update({
    'User-Agent': '你的自定义User-Agent'
})
```

### 设置代理
```python
crawler.session.proxies = {
    'http': 'http://proxy:port',
    'https': 'https://proxy:port'
}
```

## 注意事项

1. **遵守法律法规**: 请确保你的使用符合相关法律法规和微博的使用条款
2. **频率控制**: 脚本已内置随机延迟，避免过于频繁的请求
3. **数据更新**: 微博热搜实时更新，建议定期运行脚本获取最新数据
4. **网络环境**: 确保网络连接正常，某些地区可能需要代理访问

## 故障排除

### 常见问题

1. **无法获取数据**
   - 检查网络连接
   - 尝试更换User-Agent
   - 检查微博网站是否有反爬虫更新

2. **数据不完整**
   - 微博页面结构可能发生变化
   - 需要更新CSS选择器

3. **保存文件失败**
   - 检查data目录权限
   - 确保有足够的磁盘空间

### 日志文件

脚本运行时会生成 `weibo_crawler.log` 日志文件，包含详细的运行信息和错误记录。

## 扩展功能

### 定时任务
可以使用cron或任务调度器定期运行脚本：

```bash
# 每小时运行一次
0 * * * * /usr/bin/python3 /path/to/weibo_hot_search.py
```

### 数据可视化
可以结合matplotlib等库对热搜数据进行可视化分析。

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规。

## 更新日志

- v1.0.0: 初始版本，支持基本抓取和多种格式输出