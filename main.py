# encoding:utf-8

import json
import time

from com.luodongseu.spiderman import urlmanager, downloader, parserman, outerman
from com.luodongseu.conf.propertiseman import getValue


class SpiderMan(object):
    def __init__(self):
        self.q_urls = urlmanager.UrlManager()  # question的URL管理器
        self.u_urls = urlmanager.UrlManager()  # user的URL管理器
        self.downloader = downloader.Downloader()
        self.parser = parserman.ParserMan()
        self.outer = outerman.OuterMan()

    def crawl(self):
        # 统计url个数
        baseUrl = getValue('base_url')

        """获取所有question的地址"""
        for i in range(1, 259230):
            print "============Start find question url: " + baseUrl + "?page=<" + str(i) + ">=============="
            # 下载网页
            try:
                html = self.downloader.download(baseUrl + "?page=" + str(i))
            except Exception as e:
                print e
                continue
            # 处理网页，返回有用的数据和与url
            urls, data = self.parser.parser(html, baseUrl)
            if not urls:
                break
            # 添加url到url管理器中
            self.q_urls.add_new_urls(urls)
            answer_num = self.parser.parser_text_by_label_class(html, 'h4', 'List-headerText')
            # 将所有数据存放在数据库中
            for (url, text) in data.items():
                self.outer.collect_question_links(url, text, answer_num)
            time.sleep(10)

        """获取每一个question下的用户"""
        while self.q_urls.has_new_url():
            # 取一个url
            url = self.q_urls.get_new_url()
            if not url:
                break
            # 下载网页
            try:
                html = self.downloader.download(url)
            except Exception as e:
                print e
                continue
            # 处理网页，返回有用的数据和与url
            urls, data = self.parser.parser_by_a_class(html, baseUrl, 'UserLink-link')
            self.u_urls.add_new_urls(urls)
            # 将所有数据存放在数据库中
            for (url, text) in data.items():
                self.outer.collect_user_links(url, text)
            time.sleep(10)

        # 创建索引
        self.outer.createIndexAndUnique(table="info_user", key="user_url", value="1")

        """解析每个用户的信息"""
        while self.u_urls.has_new_url():
            # 取一个url
            url = self.q_urls.get_new_url()
            if not url:
                break
            # 下载网页
            try:
                html = self.downloader.download(url)
            except Exception as e:
                print e
                continue
            # 处理网页，返回有用的数据
            prefix = "/people/" + str(self.get_username_by_url(url))
            user_nick = self.parser.parser_text_by_label_class(html, 'span', 'ProfileHeader-name')

            data = {
                "user_url": url,
            }
            print "Collect user :" + json.dumps(data)
            self.outer.collect(table="info_user", data=data)

    def get_username_by_url(self, url):
        return ((url.split('people/'))[1].split('/'))[0]


if __name__ == "__main__":
    spider = SpiderMan()
    spider.crawl()
    # spider.test()
