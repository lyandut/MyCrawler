# coding:utf-8
'''
Created on 2018年1月22日
爬取策略：
1. 从文件中读取/先爬取link，  link入队
2. link出队，爬取字段，生成字典，写入文件
3. 根据link/Acronym连接两个表格
@author: 李研
'''
import urllib2
from lxml import etree
import time
import csv
from Queue import Queue
import sys
import socket

reload(sys)
sys.setdefaultencoding('utf-8')
# socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒


class EasyChair(object):
    def __init__(self, pagenum, q):     # q 用来存链接
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        self.pagenum = pagenum
        self.q = q

    def getLink(self):
        url = 'https://easychair.org/cfp/area.cgi?area=' + str(self.pagenum)

        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            html = response.read()
            response.close()

            # lxml 抓取link  //*[starts-with(@id,"row") and @class="yellow"]/td[1]/a
            selector = etree.HTML(html)
            links = selector.xpath(
                '//*[starts-with(@id,"row") and @class="yellow"]/td[1]/a/@href')
            for link in links:
                self.q.put(link)

        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print e.code
            if hasattr(e, 'reason'):
                print e.reason

    def getItems(self):
        self.getLink()
        table_list = []
        while not self.q.empty():
            try:
                chilurl = self.q.get()
                # time.sleep(1)
                request = urllib2.Request(chilurl, headers=self.headers)
                response = urllib2.urlopen(request)
                content = response.read()
                response.close()

                # 抓取表格，生成字典      //*[@id="cfp"]/table[2]/tbody/tr[1]     //*[@id="cfp"]/table[2]/tbody/tr[1]/td[1]
                selector = etree.HTML(content)
                thead = selector.xpath(
                    '//*[@id="cfp"]/table[2]/tr/td[1]/text()')
                tcontent = selector.xpath('//*[@id="cfp"]/table[2]/tr/td[2]')
                tds = []
                for td in tcontent:
                    tds.append(td.xpath('string(.)'))
                thead.append('Link')
                tds.append(chilurl)
                table = dict(zip(thead, tds))
                print table
                table_list.append(table)

            except urllib2.URLError, e:
                if hasattr(e, 'code'):
                    print e.code
                if hasattr(e, 'reason'):
                    print e.reason

            except socket.error, e:
                if hasattr(e, 'code'):
                    print e.code
                if hasattr(e, 'reason'):
                    print e.reason
                time.sleep(10)

        return table_list

    def writeCsv(self):
        table_list = self.getItems()

        # 取key的并集，
        key_total = reduce(lambda x, y: x | y, map(dict.viewkeys, table_list))
        for key in key_total:
            print key

        # 写入csv文件
        with open('1.csv', 'wb',) as f:
            # 表头在这里传入，作为第一行数据
            writer = csv.DictWriter(f, key_total)
            writer.writeheader()
            # 写入多行数据
            writer.writerows(table_list)


if __name__ == '__main__':
    num = 1
    q = Queue()
    spider = EasyChair(num, q)
    spider.writeCsv()

# class EasyChair(object):
#     def __init__(self):
#         pass
#
#     '''
#     爬取Link，Link入队
#     '''
#     def getLink(self):
#         pass
#
#     '''
#     爬取字段，生成字典
#     '''
#     def getItems(self):
#         pass
#
#     '''
#     字典写入文件
#     '''
#     def writeCsv(self):
#         pass
