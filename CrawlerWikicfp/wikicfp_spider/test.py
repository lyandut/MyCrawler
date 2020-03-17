# coding:utf-8
'''
要爬取的页面CFPs
http://www.wikicfp.com/cfp/allcfp
每一个url格式：http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=71099&copyownerid=90512
            http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=71098&copyownerid=90512
            eventid:1-71101中间有已删除页面
'''
import urllib
import urllib2
import csv
import re
import time

# # 设置代理
# # The proxy address and port:
# proxy_info = { 'host' : '182.92.207.196','port' : 3128 }
# # Create a handler for the proxy
# proxy_support = urllib2.ProxyHandler({"http" : "http://%(host)s:%(port)d" % proxy_info})
# # Create an opener which uses this handler:
# opener = urllib2.build_opener(proxy_support)
# # Install this opener as the default opener for urllib2:
# urllib2.install_opener(opener)

# 设置headers
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
headers = {'User-Agent': user_agent}

num = 2
url = 'http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=' + str(num)
f = csv.writer(open("wikicfp.csv", "wb"))
f.writerow(["Conference", "Conference Series", "Link",
            "When", "Where", "Submission Deadline"])
try:
    time.sleep(3)
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    content = response.read()
    response.close()

    # 正则表达式：confername, conf_series, link, Categories
    conferpa = re.compile('<span property="v:description"> (.*?)</span>')
    conserpa = re.compile('<br>Conference Series : <a.*?>(.*?)</a>')
    linkpa = re.compile('Link: <a.*?>(.*?)</a>')
    confer = re.findall(conferpa, content)
    conser = re.findall(conserpa, content)
    link = re.findall(linkpa, content)

    # 正则表达式：when，where， sub_deadline
    pattern = re.compile('<th>When</th>.*?<td align="center">.*?(\\S.*?)\\n.*?</td>.*?' +
                         '<th>Where</th>.*?<td align="center">(.*?)</td>.*?' +
                         '<th>Submission Deadline</th>.*?<span property="v:startDate" content=.*?>(.*?)</span>', re.S)
    items = re.findall(pattern, content)

    for item in items:
        if conser == []:
            conser.append('null')
        if link == []:
            link.append('null')
        print confer[0], conser[0], link[0], item[0], item[1], item[2]
        line = [confer[0], conser[0], link[0], item[0], item[1], item[2]]
    f.writerow(line)
    print "成功写入第"+str(num)+"行"
except urllib2.URLError, e:
    if hasattr(e, 'code'):
        print e.code
    if hasattr(e, 'reason'):
        print e.reason
