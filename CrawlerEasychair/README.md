# CrawlerEasychair

爬取会议网站 EasyChair Smart CFP 的简易爬虫程序

## 目录

- spider_area.py
  
  按照24个area分类爬取会议信息，主要爬取对象是网页中的表格，用到的技术有xpath模块，writeCsv()方法等。

- spider_detail.py
  
  对于每一个会议页面，爬取其所有字段，用到xpath，字典写入csv文件。

- result_1/

  包括Acronym，link, name, location, deadline, start_date, topic (7个字段)。

- result_2/

  具体每个会议页面的所有字段，但不完全包含result_1中的字段。

## 备注

- 尝试一次把result_1和result_2的字段爬下来写到一起，但这个网站反爬好像很厉害，总是断掉。
- 连接这两个表需要用Link这个键。
- 这个网站会议信息好像更新很快，两个result不是一起爬的，可能有些会议会对不上。
