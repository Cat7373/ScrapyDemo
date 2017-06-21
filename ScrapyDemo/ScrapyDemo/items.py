# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Proxy(Item):
    """一个代理 item"""

    ip = Field()
    port = Field()
    anonymity = Field()
    type = Field()
    location = Field()
