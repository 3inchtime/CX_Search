# -*- coding: utf-8 -*-
from urllib import parse
import datetime


import scrapy
from scrapy.http import Request


from blog_spider.tools.config_reader import ConfigReader
from blog_spider.items import BlogSpiderItem


class MonitorBlogSpider(scrapy.Spider):

    name = 'static_blog'

    def start_requests(self):
        c = ConfigReader()
        for config in c.config_parse:
            url = config[0]
            meta = {
                        'article_url': config[1],
                        'article_title': config[2],
                        'article_content': config[3],
                        'next_button': config[4]
                    }
            yield Request(url=url, callback=self.parse, meta=meta)

    def parse(self, response):
        blog_urls = response.xpath("{}".format(response.meta['article_url'])).extract()
        meta = response.meta

        for blog_url in blog_urls:
            yield Request(url=parse.urljoin(response.url, blog_url), dont_filter=True, callback=self.parse_blog, meta=meta)

        next_url = response.xpath("{}".format(response.meta['next_button'])).extract()[0]
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), dont_filter=True, callback=self.parse, meta=meta)

    def parse_blog(self, response):

        article_item = BlogSpiderItem()

        article_title_xpath = response.meta['article_title']
        article_content_xpath = response.meta['article_content']

        try:
            title = response.xpath("{}".format(article_title_xpath)).extract()[0]
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = response.xpath("{}".format(article_content_xpath)).extract()
        except IndexError:
            print("爬取失败")

        contents = ''
        for word in content:
            contents += word

        article_item['article_url'] = response.url
        article_item['article_title'] = title
        article_item['article_time'] = create_time
        article_item['article_content'] = contents

        yield article_item
