# -*- coding: utf-8 -*-
from urllib import parse
import datetime
import time


import scrapy
from scrapy.http import Request


from blog_spider.tools.config_reader import ConfigReader
from blog_spider.items import BlogSpiderItem


class MonitorBlogSpider(scrapy.Spider):

    name = 'monitor_blog'

    def start_requests(self):
        c = ConfigReader()
        for config in c.config_parse:
            url = config[0]
            meta = {
                        'article_url': config[1],
                        'article_title': config[2],
                        'next_button': config[4]
                    }
            yield Request(url=url, callback=self.parse, meta=meta)

    def parse(self, response):
        blog_urls = response.css("{}".format(response.meta['article_url'])).extract()
        meta = response.meta
        for blog_url in blog_urls:
            yield Request(url=parse.urljoin(response.url, blog_url), dont_filter=True, callback=self.parse_blog, meta=meta)

    def parse_blog(self, response):

        article_item = BlogSpiderItem()

        article_title_xpath = response.meta['article_title']
        next_button_xpath = response.meta['next_button']

        title = response.css("{}".format(article_title_xpath)).extract()[0]
        create_time = datetime.date.today().strftime("%Y-%m-%d")
        content = response.css("{}".format(next_button_xpath)).extract()[0]

        article_item['article_url'] = response.url
        article_item['article_title'] = title
        article_item['article_time'] = create_time
        article_item['article_content'] = content
        time.sleep(2)

        yield article_item
