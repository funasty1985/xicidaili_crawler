# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from redis import StrictRedis
import time

class XicidailiCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class Proxyfilter(object):
    def process_item(self, item, spider):
        if item['speed'] > 2000 or item['ttl'] < 1800000 or item['connection_time'] > 2000:
            raise DropItem('Bad quality IP proxy%s' % item)
        else:
            return item

class RedisWriter(object):
    def __init__(self):
        self.redis = StrictRedis(port=6379)

    def process_item(self, item, spider):
        item_data_dict = dict(item)
        ip = item_data_dict.pop('ip')

        ttl = item['ttl'] / 1000

        item_val = '%s:%s:%s' % (item['protocol'], ip, item['port'])
        expire_time = time.time() + ttl
        self.redis.zadd('proxies', {item_val: expire_time})

