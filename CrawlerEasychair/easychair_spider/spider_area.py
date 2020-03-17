# coding:utf-8
'''
爬取策略：
1. 目标网站：https://easychair.org/cfp/area.cgi?area=   +   （1-24）
2. 抓取方法：lxml，先大后小，先抓行，把列属性存字典
3. 具体属性：Acronym (link), name, location, deadline, start_date, topic  (7个字段) 
'''

import urllib2
from lxml import etree
#import time
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


for num in range(1, 25):
    #num = 1
    url = 'https://easychair.org/cfp/area.cgi?area=' + str(num)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        html = response.read()
        response.close()

        '''
            lxml 抓取字段
        '''
        selector = etree.HTML(html)

        # 提取area    //*[@id="content"]/div[2]/div[@class="pagetitle"]
        area = selector.xpath(
            '//*[@id="content"]/div[2]/div[@class="pagetitle"]/text()')[0].replace('CFPs in ', '')

        # 行：  //*[@class="yellow"]
        rows = selector.xpath(
            '//*[starts-with(@id,"row") and @class="yellow"]')
        # 列
        tds = []
        for row in rows:
            tds.append(row.xpath('td'))  # tds是一个840的列表，其中每个元素td是大小为6的列表
        link = []
        acro = []
        name = []
        loca = []
        dead = []
        star = []
        topi = []
        for td in tds:
            # 下面都是长度840的列表，分别是抓取的7个字段
            link.append(td[0].xpath('a/@href')[0])
            acro.append(td[0].xpath('string(.)').replace('\n', '').strip())
            # name.append(td[1].xpath('string(.)').replace('\n','').strip())
            name.append(td[1].xpath('text()')[0])
            loca.append(td[2].xpath('string(.)').replace('\n', '').strip())
            dead.append(td[3].xpath('string(.)').replace('\n', '').strip())
            star.append(td[4].xpath('string(.)').replace('\n', '').strip())
            topi.append(td[5].xpath('a/span/text()'))

        zipped = zip(acro, name, link, loca, dead,
                     star, topi, [area]*len(acro))

        # 写入文件
        with open(str(num)+" "+area+".csv", "wb") as f:
            writer = csv.writer(f)
            # 先写入表头  Acronym (link), name, location, deadline, start_date, topic
            writer.writerow(["Acronym", "Name", "Link", "Location",
                             "Submission deadline", "Start date", "Topics", "Area"])
            # 写入多行用writerows
            writer.writerows(zipped)

        print str(num)+" write "+area + " success!"

    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            print e.code
        if hasattr(e, 'reason'):
            print e.reason
