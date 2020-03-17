# coding:utf-8
'''
Created on 2018年1月19日

@author: 李研
'''
from threading import Thread
from Queue import Queue
import urllib2
import time
import csv
#import re
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

exitFlag = 0


class WIKICFP(Thread):
    def __init__(self, name, url, q):  # url:page列表       q:存数据队列
        # 重写写父类的__init__方法
        super(WIKICFP, self).__init__()
        self.name = name
        self.url = url
        self.q = q
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', }

    def run(self):
        print "starting " + self.name
        while not exitFlag:
            self.getPage(self.url)
        print "exiting " + self.name

    def getPage(self, url):
        if not url.empty():
            num = url.get()
            try:
                base_url = 'http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid='
                # 构造url
                newurl = base_url+str(num)
                request = urllib2.Request(newurl, headers=self.headers)
                response = urllib2.urlopen(request)
                pageCode = response.read()
                response.close()

                # xpath抓取信息

                selector = etree.HTML(pageCode)

                #处理无效页面     /html/body/div[4]/center/h3
                emptypage = selector.xpath('/html/body/div[4]/center/h3')

                if not emptypage:  # 非空页面
                    # 提取题目
                    # /html/body/div[4]/center/table/tbody/tr[2]/td/h2/span/span[7]/text()
                    #confname = selector.xpath('//span[@property="v:description"]/text()')

                    try:
                        confname = selector.xpath(
                            '//span[@property="v:description"]/text()')
                    except UnicodeDecodeError, e:
                        if hasattr(e, 'code'):
                            print "Error Code:", e.code
                        if hasattr(e, "reason"):
                            print "Error Reason:", e.reason
                        confname = []
                        confname.append("page "+str(num))

                    # 提取会议系列 Conference Series    /html/body/div[4]/center/table/tbody/tr[2]/td/a
                    try:
                        confser = selector.xpath(
                            '/html/body/div/center/table/tr/td/a[starts-with(@href,"/cfp/program")]/text()')
                        if confser == []:
                            confser.append('N/A')
                    except UnicodeDecodeError, e:
                        if hasattr(e, 'code'):
                            print "Error Code:", e.code
                        if hasattr(e, "reason"):
                            print "Error Reason:", e.reason
                        confser = []
                        confser.append("page "+str(num))

                    # 提取链接 link /html/body/div[4]/center/table/tbody/tr[3]/td/a
                    try:
                        link = selector.xpath(
                            '/html/body/div/center/table/tr/td/a[@target="_newtab"]/@href')
                        if link == []:
                            link.append('N/A')
                    except UnicodeDecodeError, e:
                        if hasattr(e, 'code'):
                            print "Error Code:", e.code
                        if hasattr(e, "reason"):
                            print "Error Reason:", e.reason
                        link = []
                        link.append("page "+str(num))

                    # 提取 when where submission_deadline 等...
                    # /html/body/div[4]/center/table/tr[5]/td/table/tr/td/table/tr[1]/td/table/tr/th
                    th = selector.xpath(
                        '/html/body/div/center/table/tr/td/table/tr/td/table/tr/td/table/tr/th/text()')
                    tddata = selector.xpath(
                        '/html/body/div/center/table/tr/td/table/tr/td/table/tr/td/table/tr/td')
                    tds = []
                    for td in tddata:
                        try:
                            td = tddata[tddata.index(td)].xpath(
                                'string(.)').replace('\n', '').strip()
                            tds.append(td)
                        except UnicodeDecodeError, e:
                            if hasattr(e, 'code'):
                                print "Error Code:", e.code
                            if hasattr(e, "reason"):
                                print "Error Reason:", e.reason
                            tds.append("page "+str(num))

                    table = dict(zip(th, tds))

                    # 提取分类 Categories   /html/body/div[4]/center/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/h5/a[2]
                    #categories = selector.xpath('/html/body/div/center/table/tr/td/table/tr/td/table/tr/td/table/tr/td/h5/a/text()')
                    try:
                        categories = selector.xpath(
                            '/html/body/div/center/table/tr/td/table/tr/td/table/tr/td/table/tr/td/h5/a/text()')
                        print categories
                    except UnicodeDecodeError, e:
                        if hasattr(e, 'code'):
                            print "Error Code:", e.code
                        if hasattr(e, "reason"):
                            print "Error Reason:", e.reason
                        categories = []
                        categories.append("page "+str(num))

                    # 写入字典 table
                    table['Conference Name'] = confname[0]
                    table['Conference Series'] = confser[0]
                    table['Link'] = link[0]
                    table['Categories'] = categories
                    print table
                    self.q.put(table)

                    print str(self.name), "getpage", str(num), "success."

                else:
                    print str(self.name), str(num)+" is empty page."

            except urllib2.URLError, e:
                if hasattr(e, 'code'):
                    print "Error Code:", e.code
                if hasattr(e, "reason"):
                    print "Error Reason:", e.reason
                    return None


def main():
    # 创建一个队列用来保存进程获取到的数据
    q = Queue()
    #index_list = range(1,73000)
    index_list = range(10000, 20000)
    workQueue = Queue(20000)
    threadList = ['thread-1', 'thread-2', 'thread-3', 'thread-4', 'thread-5',
                  'thread-6', 'thread-7', 'thread-8', 'thread-9', 'thread-10']
    # 保存线程
    Thread_list = []

    # 填充url列表
    for index in index_list:
        workQueue.put(index)

    # 创建线程，限制数目
    for tName in threadList:
        thread = WIKICFP(tName, workQueue, q)
        thread.start()
        Thread_list.append(thread)

    # 等待队列清空
    while not workQueue.empty():
        pass

    global exitFlag
    exitFlag = 1

    # 让主线程等待子线程执行完成
    for i in Thread_list:
        i.join()

    # 写入csv文件
    headers = ['Conference Name', 'Conference Series', 'Link', 'Categories',
               'When', 'Where', 'Submission Deadline', 'Notification Due', 'Final Version Due', 'Abstract Registration Due']

    with open('wikicfp.csv', 'wb',) as f:
        # 标头在这里传入，作为第一行数据
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        while not q.empty():
            writer.writerow(q.get())

        # 还可以写入多行
        # writer.writerows(datas)


if __name__ == "__main__":

    start = time.time()
    main()
    print '[info]耗时：%s' % (time.time()-start)
