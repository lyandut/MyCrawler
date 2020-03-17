# coding:utf-8
'''
Created on 2017年12月20日
 
@author: 李研
'''
import urllib2
import csv
import re
import socket
import time
timeout = 20
socket.setdefaulttimeout(timeout)  # 对整个socket层设置超时时间
sleep_download_time = 5


class WIKICFP(object):
    def __init__(self):
        self.pageIndex = 2
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.line = []
        #self.enable = False
        self.f = csv.writer(open("wikicfp.csv", "wb"))
        self.f.writerow(["Conference", "Conference Series",
                         "Link", "When", "Where", "Submission Deadline"])

    def getPage(self, pageIndex):
        try:
            time.sleep(sleep_download_time)
            url = 'http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=' + \
                str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            response.close()
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print "错误原因", e.reason
                return None
        except socket.error:
            print "Socket Error"

    def getItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "getPage Wrong"
            return None

        # 正则表达式：confername, conf_series, link, Categories
        conferpa = re.compile('<span property="v:description"> (.*?)</span>')
        conserpa = re.compile('<br>Conference Series : <a.*?>(.*?)</a>')
        linkpa = re.compile('Link: <a.*?>(.*?)</a>')
        confer = re.findall(conferpa, pageCode)
        conser = re.findall(conserpa, pageCode)
        link = re.findall(linkpa, pageCode)

        # 正则表达式：when，where， sub_deadline
        pattern = re.compile('<th>When</th>.*?<td align="center">.*?(\\S.*?)\\n.*?</td>.*?' +
                             '<th>Where</th>.*?<td align="center">(.*?)</td>.*?' +
                             '<th>Submission Deadline</th>.*?<span property="v:startDate" content=.*?>(.*?)</span>', re.S)
        items = re.findall(pattern, pageCode)

        for item in items:
            if conser == []:
                conser.append('null')
            if link == []:
                link.append('null')
            self.line = [confer[0], conser[0],
                         link[0], item[0], item[1], item[2]]
        print "获取第"+str(self.pageIndex)+"页items成功"

    def writeCvs(self, pageIndex):
        self.getItems(pageIndex)
        self.f.writerow(self.line)
        print "写入第"+str(self.pageIndex)+"页items成功"

    def start(self):
        while self.pageIndex < 71102:
            self.writeCvs(self.pageIndex)
            self.pageIndex += 1


if __name__ == "__main__":
    spider = WIKICFP()
    spider.start()
