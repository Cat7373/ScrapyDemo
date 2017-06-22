# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import random
import re
from items import Proxy


class RandomUserAgentMiddleware(object):
    """自动换 UserAgent 的中间件"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class FilterInvalidProxyMiddleware(object):
    """过滤无效的代理的中间件"""

    ip_regex = re.compile(r'([1-9]?\d|1[\d]{2}|2[0-4]\d|25[0-5])(\.([1-9]?\d|1[\d]{2}|2[0-4]\d|25[0-5])){3}')

    def process_spider_output(self, response, result, spider):
        for r in result:
            if isinstance(r, Proxy):
                if self.__is_invalid_proxy(r):
                    spider.log('invalid Proxy item: %s' % r, level=logging.WARN)
                else:
                    yield r

    def __is_invalid_proxy(self, proxy):
        # 端口验证 0 ~ 65535
        if not proxy['port']:
            return True
        try:
            port = int(proxy['port'])
            if port <= 0 or port > 65535:
                return True
        except ValueError:
            return True

        # 代理类型验证 HTTP HTTPS SOCKET4/5
        if not proxy['type']:
            return True
        proxy['type'] = proxy['type'].upper()
        if proxy['type'] not in ('HTTP', 'HTTPS', 'SOCKET4', 'SOCKET5'):
            return True

        # 是否为有效 ip 验证
        if not proxy['ip'] or self.ip_regex.match(proxy['ip']):
            return True

        return False
