#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from ..items import Proxy


class XiCiDaiLiSpider(scrapy.Spider):
    """
    自动爬取 xicidaili.com 的代理
    """

    # 代理名称
    name = 'XiCiDaiLiSpider'
    # 网站的根地址
    host = 'http://www.xicidaili.com'
    # 允许爬虫爬取的域列表
    allowed_domains = ['www.xicidaili.com']
    # 种子站点列表
    start_urls = [
        'http://www.xicidaili.com/wn/',
        'http://www.xicidaili.com/wt/',
        'http://www.xicidaili.com/qq/'
    ]

    # 将种子站点加入爬取队列
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_proxy)

    # 爬每一页的代理，并将每一个代理投递给 items pipe
    def parse_proxy(self, response):
        # 找出代理列表
        proxys = response.css('#ip_list tr')[1:]
        for proxy in proxys:
            attrs = proxy.css('td')

            proxy = Proxy(
                ip=attrs[1].css('::text').extract_first(),
                port=attrs[2].css('::text').extract_first(),
                anonymity=attrs[4].css('::text').extract_first(),
                type=attrs[5].css('::text').extract_first(),
                location=attrs[3].css('a::text').extract_first()
            )
            if proxy['type'] == u'QQ代理':
                proxy['type'] = 'SOCKET5'
            yield proxy

        # 找下一页
        next = response.css('.next_page')
        if len(next) > 0:
            href = next.css('::attr(href)').extract_first()
            yield Request(url=self.host + href, callback=self.parse_proxy)
