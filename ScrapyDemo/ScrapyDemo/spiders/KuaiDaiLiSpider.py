#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from ..items import Proxy


class KuaiDaiLiSpider(scrapy.Spider):
    name = 'KuaiDaiLiSpider'
    host = 'http://www.kuaidaili.com'
    allowed_domains=['www.kuaidaili.com']
    start_urls = [
        'http://www.kuaidaili.com/free/'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_type)

    # 从起始页解析出来所有代理分类
    def parse_type(self, response):
        types = response.css('.tag_area2 > a')
        for type in types:
            url = self.host + type.css('::attr(href)').extract_first()
            name = type.css('::text').extract_first()
            yield Request(url=url, callback=self.parse_proxy)

    # 爬每一页的代理
    def parse_proxy(self, response):
        # 找出代理列表
        proxys = response.css('#list tbody > tr')
        for proxy in proxys:
            attrs = [attr.css('::text').extract_first() for attr in proxy.css('td')]

            proxy = Proxy()
            proxy['ip'] = attrs[0]
            proxy['port'] = attrs[1]
            proxy['anonymity'] = attrs[2]
            proxy['type'] = attrs[3]
            proxy['location'] = attrs[4]
            yield proxy

        # 找下一页
        pages = response.css('#listnav li > a')
        found = False
        for page in pages:
            cls = page.css('::attr(class)').extract_first()
            if cls == 'active':
                found = True
                continue
            if not found:
                continue

            href = page.css('::attr(href)').extract_first()
            yield Request(url=self.host + href, callback=self.parse_proxy)
            break
