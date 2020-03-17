# CrawlerWikiCFP

多线程爬取WikiCFP会议网站，获取会议信息（包括会议名、link、时间、地点、deadline等字段）

## 目录

- spider_singlethread_with_re.py

  单线程版本（正则表达式解析）

- spider_multithread_with_re.py

  不完善多线程版本（正则表达式解析）

- spider_multithread_with_xpath.py

  正式版多线程爬虫程序（xpath解析）

- result/

  爬取结果（每1w条结果存储一个csv文件）

## 使用的技术

urllib2下载、xpath解析、多线程并发threading模块、FIFO队列

## 未来可能的优化

- 增加一条线程控制workQueue写入文件;
- 增加使用代理。
