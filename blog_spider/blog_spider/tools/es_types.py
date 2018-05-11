# -*- coding: utf-8 -*-

from elasticsearch_dsl import DocType, Date, Keyword, Text
from elasticsearch_dsl.connections import connections


connections.create_connection(hosts=["localhost"])


class BlogType(DocType):
    article_url = Keyword()
    article_title = Text(analyzer="ik_max_word")
    article_time = Date()
    article_content = Text(analyzer="ik_max_word")

    class Meta:
        index = 'static_blog'
        doc_type = 'article'


if __name__ == '__main__':
    BlogType.init()
