# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class DuplicatesPipeline(object):
#     def __init__(self):
#         # self.con = redis.Redis(REDIS_HOST, port=REDIS_PORT)
#         pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
#         conn = redis.StrictRedis(connection_pool=pool)
#         self.br = PyBloomFilter(conn=conn)
#
#     def process_item(self, item, spider):
#         content = str(item)
#         tax = self.br.is_exist(content)
#         if tax:
#             print('=================================================')
#             raise DropItem("Duplicate book found:%s" % item)
#         self.br.add(content)
#         return item
import datetime
import logging

import pymysql
from twisted.enterprise import adbapi
import time


class MysqlTwistedPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            # MYSQL_HOST, MYSQL_DB, MYSQL_CHRSET, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DB"],
            user=settings["MYSQL_USER"],
            port=settings['MYSQL_PORT'],
            passwd=settings["MYSQL_PASSWORD"],
            charset=settings['MYSQL_CHRSET'],
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        logging.warning(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '----' + str(failure) + '\n')
        print('有错')

    def do_insert(self, cursor, item):
            try:
                sql = '''
                            insert ignore into `topic_government_haiguan`  (`title`, `content`, `time`,
                            `website`, `link`, `type`,`source`,`create_time`,`txt`,`spider_name`,`module_name`) 
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        '''
                parm = (
                    item['title'],
                    item['content'],
                    item['time'],
                    item['website'],
                    item['link'],
                    item['type'],
                    item['source'],
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    item['txt'],
                    item['spider_name'],
                    item['module_name']
                )
                cursor.execute(sql, parm)
                # self.db.commit()
            except Exception as e:

                logging.warning(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '----' + e.__str__() + '\n')

    def close_spider(self, spider):
        logging.warning(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '----' + '爬虫结束'+ '\n')