# -*- coding: utf-8 -*-

import re


import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from w3lib.html import remove_tags


from blog_spider.tools.es_types import BlogType


class BlogSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, setting):
        dbparms = dict(
            host=setting["MYSQL_HOST"],
            db=setting["MYSQL_DBNAME"],
            user=setting["MYSQL_USER"],
            passwd=setting["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
        return item

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):

        relcontent = item["article_content"]
        content = re.sub(r'</?\w+[^>]*>', '', relcontent).strip()

        insert_sql = """
                        INSERT INTO blog_detail(title,url,create_time,content)
                        VALUES (%s,%s,%s,%s);
                        """
        cursor.execute(insert_sql, (item["article_title"], item["article_url"], item["article_time"], content))
# CREATE TABLE blog_detail(title VARCHAR(200) NOT NULL, url VARCHAR(200) NOT NULL, create_time DATETIME NOT NULL, content LONGTEXT NOT NULL)CHARACTER SET = utf8;


class ElasticsearchPipeline(object):

    def process_item(self, item, spider):
        blog = BlogType()
        blog.title = item['article_title']
        blog.time = item['article_time']
        blog.content = remove_tags(item['article_content'])
        blog.url = item['article_url']

        blog.save()

        return item
