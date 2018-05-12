# -*- coding: utf-8 -*-

import re


import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from w3lib.html import remove_tags
from elasticsearch_dsl.connections import connections


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


es = connections.create_connection(BlogType._doc_type.using)


def gen_suggests(index, text, weight):
    used_words = set()
    suggests = []
    if text:
        words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ["lowercase"]}, body=text)
        anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
        new_words = anylyzed_words - used_words
    else:
        new_words = set()

    if new_words:
        suggests.append({"input": list(new_words), "weight": weight})

    return suggests


class ElasticsearchPipeline(object):

    def process_item(self, item, spider):

        article = BlogType()
        article.title = item['article_title']
        article.time = item['article_time']
        article.content = remove_tags(item['article_content'])
        article.url = item['article_url']

        # article.suggest = gen_suggests(index=BlogType._doc_type.index, text=article.title, weight=10)

        article.save()

        return item
