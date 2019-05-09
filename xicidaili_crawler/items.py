# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class XicidailiCrawlerItem(Item):
    ip = Field()
    port = Field()
    protocol = Field()
    speed = Field()
    connection_time = Field()
    ttl = Field()
