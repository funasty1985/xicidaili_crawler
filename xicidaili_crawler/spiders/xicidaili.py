# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import XicidailiCrawlerItem



class XicidailiSpider(CrawlSpider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn/']
    rules = (Rule(LinkExtractor(allow=('/nn/*'), ), follow=True, callback='parse_items'),)

    def parse_items(self, response):
        table_selector = response.xpath('//*[@id="ip_list"]//tr')

        for row_selector in table_selector[1:]:
            item = XicidailiCrawlerItem()

            item['ip'] = row_selector.xpath('td[2]/text()').extract_first()
            item['port'] = row_selector.xpath('td[3]/text()').extract_first()
            item['protocol'] = row_selector.xpath('td[6]/text()').extract_first()
            item['speed'] = self.duration_to_millisecond(row_selector.xpath('td[7]/div/@title').extract_first())
            item['connection_time'] = self.duration_to_millisecond(row_selector.xpath('td[8]/div/@title').extract_first())
            item['ttl'] = self.duration_to_millisecond(row_selector.xpath('td[9]/text()').extract_first())



            yield item

    def duration_to_millisecond(self, val):

        if val:
            if u'秒' in val:
                return int(float(val.replace(u'秒', '')) * 1000)
            if u'分钟' in val:
                return int(float(val.replace(u'分钟', '')) * 1000 * 60)
            if u'小时' in val:
                return int(float(val.replace(u'小时', '')) * 1000 * 60 * 60)
        else:
            return 0
