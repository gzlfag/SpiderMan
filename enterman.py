# encoding:utf-8

import urllib
import urllib2

import cookielib
import re
from com.luodongseu.conf.propertiseman import getValue

class EnterMan:
    def __init__(self, username, passwd):
        self.loginUrl = "https://www.zhihu.com/login/email"
        self.userName = username
        self.passWord = passwd
        # 公共文件存放路径
        self.cookiePath = getValue("cookie_path")
        self.cookieMan = cookielib.MozillaCookieJar(self.cookiePath)

        self.proxy_info = {
            'http': 'http://xxx:xxx@proxycn2.huawei.com:8080',
            'https': 'https://xxx:xxx@proxycn2.huawei.com:8080'
        }

        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            # 'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.zhihu.com',
            'DNT': '1'
        }

        self.initUrllib2()

    def updateCookie(self, cookie):
        '''更新cookie内容'''
        cookie_file = open(self.cookiePath)
        cookie_file.write(cookie)
        cookie_file.close()

    def initUrllib2(self):
        '''初始化网络请求处理器'''
        proxy = urllib2.ProxyHandler(self.proxy_info)
        cookie_proc = urllib2.HTTPCookieProcessor(self.cookieMan)
        opener = urllib2.build_opener(proxy, cookie_proc)
        urllib2.install_opener(opener)

    def getXsrf(self):
        '''读取xsrf值，用于后续引用'''
        request = urllib2.Request("https://www.zhihu.com")
        data = urllib2.urlopen(request).read()
        cer = re.compile('name="_xsrf" value="(.*)"', flags=0)
        strlist = cer.findall(data)
        print("strlist:", strlist)
        return strlist[0]

    def login(self):
        data = {
            '_xsrf': self.getXsrf(),
            'password': self.passWord,
            'email': self.userName
        }
        request = urllib2.Request(self.loginUrl, urllib.urlencode(data), self.headers)
        response = urllib2.urlopen(request).read()
        # 保存cookie
        self.cookieMan.save(ignore_discard=True, ignore_expires=True)
        
        print response
        
    def initRequest(self):
        # 读取cookie
        self.cookieMan.load(self.cookiePath, ignore_discard=True, ignore_expires=True)

if __name__ == "__main__":
#     man = EnterMan('1576848284@qq.com', '1063538305ld')
#     man.login()
    
    print getValue("cookie_path")
