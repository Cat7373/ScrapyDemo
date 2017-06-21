#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from ..items import Proxy


class XiCiDaiLiSpider(scrapy.Spider):
    name = 'XiCiDaiLiSpider'
    host = 'http://www.xicidaili.com'
    allowed_domains = ['www.xicidaili.com']
    start_urls = [
        'http://www.xicidaili.com/wn/',
        'http://www.xicidaili.com/wt/',
        'http://www.xicidaili.com/qq/'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_proxy)

    # 爬每一页的代理
    def parse_proxy(self, response):
        # 找出代理列表
        proxys = response.css('#ip_list tr')[1:]
        for proxy in proxys:
            attrs = proxy.css('td')
            # [attr.css('::text').extract_first() for attr in proxy.css('td')]

            proxy = Proxy()
            proxy['ip'] = attrs[1].css('::text').extract_first()
            proxy['port'] = attrs[2].css('::text').extract_first()
            proxy['anonymity'] = attrs[4].css('::text').extract_first()
            proxy['type'] = attrs[5].css('::text').extract_first()
            if proxy['type'] == u'QQ代理':
                proxy['type'] = 'SOCKET5'
            proxy['location'] = attrs[3].css('a::text').extract_first()
            yield proxy

        # 找下一页
        next = response.css('.next_page')
        if len(next) > 0:
            href = next.css('::attr(href)').extract_first()
            yield Request(url=self.host + href, callback=self.parse_proxy)
