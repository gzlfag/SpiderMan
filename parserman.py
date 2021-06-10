# encoding:utf-8

import urlparse

from bs4 import BeautifulSoup


class ParserMan(object):
    def parser(self, html, url):
        if url is None or html is None:
            return
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        new_urls = self.get_new_urls(url, soup)
        new_datas = self.get_new_datas(url, soup)
        return new_urls, new_datas

    def parser_by_a_class(self, html, url, cls):
        if url is None or html is None:
            return
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        new_urls = self.get_new_urls_by_a_class(url, cls, soup)
        new_datas = self.get_new_datas_by_a_class(url, cls, soup)
        return new_urls, new_datas

    def get_new_urls(self, url, soup):
        new_urls = set()
        links = soup.find_all('a', class_='question_link')
        print links
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(url, new_url)
            new_urls.add(new_full_url)
            # print(new_full_url)
        return new_urls

    def get_new_urls_by_a_class(self, url, cls, soup):
        new_urls = set()
        links = soup.find_all('a', class_=str(cls))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(url, new_url)
            new_urls.add(new_full_url)
            # print(new_full_url)
        return new_urls

    def get_new_datas(self, url, soup):
        new_datas = {}
        links = soup.find_all('a', class_='question_link')
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(url, new_url)
            new_datas[new_full_url] = link.get_text()
            # print(link.get_text())
        return new_datas

    def get_new_datas_by_a_class(self, url, cls, soup):
        new_datas = {}
        links = soup.find_all('a', class_=str(cls))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(url, new_url)
            new_datas[new_full_url] = link.get_text()
            # print(link.get_text())
        return new_datas

    def parser_text_by_label_class(self, html, label, cls):
        if label is None or cls is None or html is None:
            return
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        return soup.find(label, class_=str(cls)).get_text()

    def parser_text_by_href(self, html, href):
        if href is None or html is None:
            return
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        return soup.find('a', href=str(href)).get_text()

    def parser_next_by_label_cls_text(self, html, label, cls, text=None, next_label=None):
        """
        查找兄弟节点的值
        :param html:
        :param label:
        :param cls:
        :param text:
        :param next_label:
        :return:
        """
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        if next_label is None:
            next_label = label
        if text is None:
            tag = soup.find(str(label), class_=str(cls))
        else:
            tag = soup.find(str(label), class_=str(cls), text=str(text))
        return tag.find_next_sibling(str(next_label)).get_text()


if __name__ == "__main__":
    parser = ParserMan()
    html = '''
    <div class="SourcesOfAlpha" name="C">
    <table>
    <tbody><tr>
    <td style="width:80px;text-align:center;"><strong style="font-size:30pt;">C</strong></td>
    <td>
    <ul>
    <li class="api_href"><a href="/apidocs/apidoc?api=c3p0" class="doc_href">C3P0连接池</a></li>
    <li class="api_href"><a href="/apidocs/apidoc?api=commons-beanutils" class="doc_href">Commons-Beanutils</a></li>
    </tr>
    </tbody></table>
    <div class="clear"></div>
    </div>
    '''

    html1 = '''
    <div class="NumberBoard QuestionFollowStatus-counts"><div class="NumberBoard-item"><div class="NumberBoard-name">关注者</div><div class="NumberBoard-value">170008</div></div><div class="NumberBoard-divider"></div><div class="NumberBoard-item"><div class="NumberBoard-name">被浏览</div><div class="NumberBoard-value">9800402</div></div></div>
    '''
    # print parser.parser_text_by_label_class(str(parser.parser_text_by_label_class(html, 'li', 'api1_href')), 'a',
    #                                         'doc_href')
    # print parser.parser_text_by_href(html, "/apidocs/apidoc?api=css3")
    print parser.test(html1)
