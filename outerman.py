# encoding:utf-8

import pymongo

from com.luodongseu.conf.propertiseman import getValue


class OuterMan(object):
    def __init__(self):
        # self.datas = {}
        self.dh = DataHandler()

    def collect_question_links(self, url, data, answers):
        """
        收集question的地址
        :param url:
        :param data:
        :param answers:
        :return:
        """
        # self.datas.append(data)
        # print(data)
        print "[OuterMan collect_question_links] Get data: " + url + " == " + data
        if not self.dh.isExistKeyData("links_question", "url", url):
            self.dh.insertData("links_question", {"url": url, "text": data, 'answers': answers})

    def collect_user_links(self, url, data):
        """
        收集user的地址
        :param url:
        :param data:
        :return:
        """
        # self.datas.append(data)
        # print(data)
        print "[OuterMan collect] Get data: " + url + " == " + data;
        if not self.dh.isExistKeyData("links_user", "url", url):
            self.dh.insertData("links_user", {"url": url, "name": data})

    def print_data(self):
        # print('Len: %s' % len(self.datas))
        # print('Data: %s' % self.datas)
        print self.dh.queryData("links")

    def collect(self, table, data):
        """
        向指定表格中插入全部数据
        :param table:
        :param data:
        :return:
        """
        self.dh.insertData(str(table), data)

    def createIndexAndUnique(self, table, key, value):
        """
        为表格创建索引和唯一
        :param table:
        :param index:
        :return:
        """
        self.dh.index(str(table), {key: value}, unique=True)


class DataHandler(object):
    """
    数据处理器
    """

    def __init__(self):
        self.serverHost = getValue("db_host")
        self.serverPort = getValue("db_port")
        self.database = "test"  # getValue("db_database")
        self.db = None
        self.connectDatabase()

    def connectDatabase(self):
        """
        连接数据库
        :return:
        """
        # 创建客户端，连接服务器
        client = pymongo.MongoClient(str(self.serverHost), int(self.serverPort))
        # 连接指定数据库
        self.db = client[self.database]

    def insertData(self, table, data):
        """
        插入数据到指定数据表
        :param table:
        :param data:
        :return:
        """
        print "[DataHandler insertData] Insert table: " + str(table)
        print "[DataHandler insertData] Insert data: " + str(data)
        collection = self.db[table]
        collection.insert(data)

    def queryData(self, table):
        """
        查询表的信息
        :param table:
        :return:
        """
        print "[DataHandler queryData] Query table: " + str(table)
        collection = self.db[table]
        for item in collection.find():
            print "[ITEM]: " + str(item)

    def isExistKeyData(self, table, key, value):
        """
        判断是否存在指定key值的数据
        :param table:
        :param key:
        :param value:
        :return:
        """
        print "[DataHandler isExistKeyData] Query table: " + str(table)
        collection = self.db[table]
        rec = collection.find_one({key: value})
        return rec

    def clearData(self, table):
        """
        清空表格
        :param table:
        :return:
        """
        print "[DataHandler clearData] Start to empty table: " + str(table)
        collection = self.db[table]
        collection.drop()

    def index(self, table, data, unique=False):
        """
        创建索引
        :param table:
        :param data:
        :param unique:
        :return:
        """
        collection = self.db[table]
        collection.create_index(data, unique=unique)


if __name__ == "__main__":
    dh = DataHandler()
    # dh.insertData("test", {"xxx": "yyyy"})
    table = "info_user"
    print "clear before: "
    dh.queryData(table)
    print "clear....."
    dh.clearData(table)
    print "clear end: "
    dh.queryData(table)
