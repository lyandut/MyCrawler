# coding:utf-8

from threading import Thread
from Queue import Queue
import urllib2
import time
#import csv
import re


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
        self.getItems()
        print "exiting " + self.name

    def getPage(self, url):
        try:
            if not url.empty():
                num = url.get()
                base_url = 'http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid='
                # 构造url
                newurl = base_url+str(num)
                request = urllib2.Request(newurl, headers=self.headers)
                response = urllib2.urlopen(request)
                pageCode = response.read()
                response.close()
                return pageCode, num
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print e.code
            if hasattr(e, "reason"):
                print "错误原因", e.reason
                return None

    def getItems(self):
        while not exitFlag:
            (pageCode, num) = self.getPage(self.url)
            if not pageCode:
                print "getPage Wrong"
                return None

            # 正则表达式：confer_name, conf_series, link, Categories
            conferpa = re.compile(
                '<span property="v:description"> (.*?)</span>')
            conserpa = re.compile('<br>Conference Series : <a.*?>(.*?)</a>')
            linkpa = re.compile('Link: <a.*?>(.*?)</a>')
            confer = re.findall(conferpa, pageCode)
            conser = re.findall(conserpa, pageCode)
            link = re.findall(linkpa, pageCode)
            if conser == []:
                conser.append('null')
            if link == []:
                link.append('null')

            # 正则表达式：when，where， sub_deadline
            pattern = re.compile('<th>When</th>.*?<td align="center">.*?(\\S.*?)\\n.*?</td>.*?' +
                                 '<th>Where</th>.*?<td align="center">(.*?)</td>.*?' +
                                 '<th>Submission Deadline</th>.*?<span property="v:startDate" content=.*?>(.*?)</span>', re.S)
            items = re.findall(pattern, pageCode)
            for item in items:
                self.q.put(confer[0] + "\t" + conser[0] + "\t" + ''.join(item[0]
                                                                         ) + "\t" + ''.join(item[1]) + "\t" + ''.join(item[2]))
            print "获取第" + str(num)+"页成功"


def main():
    # 创建一个队列用来保存进程获取到的数据
    q = Queue()
    index_list = range(1, 200)
    workQueue = Queue(100000)
    threadList = ['thread-1', 'thread-2', 'thread-3', 'thread-4', 'thread-5']
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

    exitFlag = 1

    # 让主线程等待子线程执行完成
    for i in Thread_list:
        i.join()

    while not q.empty():
        print q.get()


if __name__ == "__main__":

    start = time.time()
    main()
    print '[info]耗时：%s' % (time.time()-start)
