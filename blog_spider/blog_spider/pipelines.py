# -*- coding: utf-8 -*-

import MySQLdb
import MySQLdb.cursors


class BlogSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipelines(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'blog_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        insert_sql = """
                        INSERT INTO blog_detail(title,url,create_time,content) 
                        VALUES (%s,%s,%s,%s);
                        """

        self.cursor.execute(insert_sql, (item["article_title"], item["article_url"], item["article_time"], item["article_content"]))
        self.conn.commit()
#
# class MysqlTwistedPipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, setting):
#         dbparms = dict(
#             host=setting["MYSQL_HOST"],
#             db=setting["MYSQL_DBNAME"],
#             user=setting["MYSQL_USER"],
#             passwd=setting["MYSQL_PASSWORD"],
#             charset='utf8',
#             cursorclass=MySQLdb.cursors.DictCursor,
#             use_unicode=True,
#         )
#
#         dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         query = self.dbpool.runInteraction(self.do_insert, item)
#         query.addErrback(self.handle_error)
#         return item
#
#     def handle_error(self, failure):
#         print(failure)
#
#     def do_insert(self, cursor, item):
#         insert_sql = """INSERT INTO blog_detail(title, url, create_time, content) VALUES (%s, %s, %s, %s);"""
#         cursor.execute(insert_sql, (item["article_title"], item["article_url"], item["article_time"], item["article_content"]))

#CREATE TABLE blog_detail(title VARCHAR(200) NOT NULL, url VARCHAR(200) NOT NULL, create_time VARCHAR(200), content LONGTEXT NOT NULL);
