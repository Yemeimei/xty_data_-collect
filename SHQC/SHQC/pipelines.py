# -*- coding: utf-8 -*-

import datetime
import logging
import time
import pymysql
from twisted.enterprise import adbapi


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

    def do_insert(self, cursor, data):
        print('insert data.......' + str(data['type']))
        try:
            item = data['item']
            if data['type'] == 'brand':
                sql = '''
                            insert into `topic_info_chanxiao_qcxl_brand`  (`code`, `brand`,`month`,`sale_num`,`unit`,`website`,
                            `link`,`tags`, `create_time`,`spider_name`,`module_name`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        '''
                parm = (
                    item['code'],
                    item['brand'],
                    item['month'],
                    item['sale_num'],
                    item['unit'],
                    item['website'],
                    item['link'],
                    item['tags'],
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    item['spider_name'],
                    item['module_name']
                )
            elif data['type'] == 'company':
                sql = '''
                    insert into `topic_info_chanxiao_qcxl_company`  (`code`, `company`,`month`,`sale_num`,`unit`,`website`,
                    `link`,`tags`, `create_time`,`spider_name`,`module_name`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                parm = (
                    item['code'],
                    item['company'],
                    item['month'],
                    item['sale_num'],
                    item['unit'],
                    item['website'],
                    item['link'],
                    item['tags'],
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    item['spider_name'],
                    item['module_name']
                )
            elif data['type'] == 'car_type':
                sql = '''
                    insert into `topic_info_chanxiao_qcxl_cartype`  (`code`, `car_type`,`month`,`sale_num`,`unit`,`website`,
                    `link`,`tags`, `create_time`,`spider_name`,`module_name`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                parm = (
                    item['code'],
                    item['car_type'],
                    item['month'],
                    item['sale_num'],
                    item['unit'],
                    item['website'],
                    item['link'],
                    item['tags'],
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    item['spider_name'],
                    item['module_name']
                )
            cursor.execute(sql, parm)
        except Exception as e:
            logging.warning(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '----' + e.__str__() + '\n')

    def close_spider(self, spider):
        logging.warning(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '----' + '爬虫结束'+ '\n')
