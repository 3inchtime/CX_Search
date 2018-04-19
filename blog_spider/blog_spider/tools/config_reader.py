# -*- coding:utf-8 -*-
import os
import yaml

from blog_spider.settings import MONITOR_LIST_PATH


class ConfigReader(object):
    def __init__(self):
        self.config = {}
        self.config_parse = []
        host_path = os.path.join(MONITOR_LIST_PATH)

        try:
            with open(host_path, 'r')as f:
                self.config = yaml.load(f.read())
        except:
            print("解析配置文件失败")

        for key in self.config:
            key_words = [
                            key,
                            self.config[key]['article_url'],
                            self.config[key]['article_title'],
                            self.config[key]['article_time'],
                            self.config[key]['next_button']
                          ]
            self.config_parse.append(key_words)
