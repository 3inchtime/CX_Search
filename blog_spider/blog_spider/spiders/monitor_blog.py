# -*- coding: utf-8 -*-
import scrapy

from blog_spider.tools.config_reader import ConfigReader


class MonitorBlogSpider(scrapy.Spider):
    name = 'monitor_blog'
    c = ConfigReader()

    def start_requests(self):
        pass

    def parse(self, response):
        pass

