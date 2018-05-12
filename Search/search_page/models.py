# -*- coding: utf-8 -*-


from elasticsearch_dsl import DocType, Date, Keyword, Text, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer


connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class BlogType(DocType):

    suggest = Completion(analyzer=ik_analyzer)
    article_url = Keyword()
    article_title = Text(analyzer="ik_max_word")
    article_time = Date()
    article_content = Text(analyzer="ik_max_word")

    class Meta:
        index = 'static_blog'
        doc_type = 'article'


if __name__ == '__main__':
    BlogType.init()

