# encoding:utf-8


class UrlManager(object):
    def __init__(self):
        # 未抓取的页面集合 set无重复
        self.new_urls = set()
        # 抓取后的页面集合
        self.old_urls = set()

    def add_new_url(self, url):
        if url is None:
            return
        # 不重复
        if url not in self.old_urls and url not in self.new_urls:
            self.new_urls.add(url)
            print "[UrlManager add_new_url] Add a new url: *** ", url, " ***"

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            # 不重复
            self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_urls) != 0

    def get_new_url(self):
        if len(self.new_urls) == 0:
            return None
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url
