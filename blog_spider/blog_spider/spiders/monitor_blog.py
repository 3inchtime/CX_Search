# -*- coding: utf-8 -*-
from urllib import parse


import scrapy
from scrapy.http import Request


from blog_spider.tools.config_reader import ConfigReader


class MonitorBlogSpider(scrapy.Spider):

    name = 'monitor_blog'

    def start_requests(self):
        c = ConfigReader()
        for config in c.config_parse:
            url = config[0]
            meta = {
                        'article_url': config[1],
                        'article_title': config[2],
                        'article_time': config[3],
                        'next_button': config[4]
                    }
            yield Request(url=url, callback=self.parse, meta=meta)

    def parse(self, response):
        blog_urls = response.css("{}".format(response.meta['article_url'])).extract()
        meta = response.meta
        for blog_url in blog_urls:
            yield Request(url=parse.urljoin(response.url, blog_url), dont_filter=True, callback=self.parse_blog, meta=meta)

    def parse_blog(self, response):
        title = response.css("{}".format(response.meta['article_title']))
        create_time = response.css("{}".format(response.meta['article_time']))
        content = response.css("{}".format(response.meta['next_button']))
        print(title, create_time, content)
        pass

