# -*- coding: utf-8 -*-
import random

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from blog_spider.settings import USER_AGENT_LIST


class BlogSpiderSpiderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BlogSpiderDownloaderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=""):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        with open(USER_AGENT_LIST, 'r') as f:
            user_agent_list = f.readlines()
            agent = user_agent_list[random.randint(1, len(user_agent_list))][0:-1]
            request.headers['User_Agent'] = agent
