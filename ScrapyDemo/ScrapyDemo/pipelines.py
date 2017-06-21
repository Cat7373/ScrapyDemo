# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from items import Proxy
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class ScrapydemoPipeline(object):
    """处理 Proxy item，将其存入数据库"""

    @classmethod
    def from_settings(cls, settings):
        params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **params)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        if isinstance(item, Proxy):
            query = self.dbpool.runInteraction(self.__insert_proxy, item)
            query.addErrback(self.__handle_error, item, spider)
        else:
            return item

    @classmethod
    def __insert_proxy(cls, tx, item):
        sql = "INSERT INTO proxy(ip, port, anonymity, `type`, location) VALUES (%s, %s, %s, %s, %s)"
        params = (item["ip"], item["port"], item["anonymity"], item["type"], item["location"])
        tx.execute(sql, params)

    @classmethod
    def __handle_error(cls, failue, item, spider):
        print failue
