# coding:utf-8
import urllib
import urllib2
import cookielib

filename = 'cookie.txt'
# 声名一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({'zjh': '201592403', 'mm': 'xxxxxxxx'})
# 登陆教务系统URL
loginUrl = 'http://zhjw.dlut.edu.cn/loginAction.do'
# 模拟登陆，并把cookie保存到变量
result = opener.open(loginUrl, postdata)
# 保存到cookie.txt文件
cookie.save(ignore_discard=True, ignore_expires=True)

# 利用cookie请求访问成绩查询网址
gradeUrl = 'http://zhjw.dlut.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'
gradeFrame = 'http://zhjw.dlut.edu.cn/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=6745'
result = opener.open(gradeFrame)
fout = open('Grade.html', 'w')
fout.write(result.read())
fout.close()
