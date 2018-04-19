# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogSpiderItem(scrapy.Item):
    article_url = scrapy.Field()
    article_title = scrapy.Field()
    article_time = scrapy.Field()
    article_content = scrapy.Field()
