# encoding:utf-8

import urllib2
import time

from com.luodongseu.spiderman import enterman


class Downloader(object):
    def __init__(self):
        self.enter = enterman.EnterMan
        # # 网络代理设置
        self.proxy_info = {
            'http': 'http://xxx:xxx@proxyhk.huawei.com:8080',
            'https': 'https://xxx:xxx@proxyhk.huawei.com:8080'
        }
        # # 请求头设置
        self.header_user_agent = "Mozilla/5.0"
        self.headers = {'User-Agent': self.header_user_agent}

    def download(self, url, retry=3):
        if url is None:
            return None

        proxy = urllib2.ProxyHandler(self.proxy_info)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        try:
            request = urllib2.Request(url=url, headers=self.headers)
            f = urllib2.urlopen(request)
            response = f.read()
            return response
        except Exception as e:
            print e
            if retry < 0:
                print "[Downloader download] Connect nerwork failed!"
                raise Exception("Connect network failed.")
                return
            print "[Downloader download] Retry time: " + str(3 - retry)
            time.sleep(5)
            return self.download(url, retry - 1)


# self.enter.login()  # 未登录
#             return self.download(url)

if __name__ == "__main__":
    down = Downloader()
    print down.download('http://www.baidu.com/')
