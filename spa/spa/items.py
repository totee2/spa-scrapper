# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    short_name = scrapy.Field()
    refuge_name = scrapy.Field()
    profile_picture = scrapy.Field()
    name = scrapy.Field()
    breed = scrapy.Field()
    size = scrapy.Field()
    gender = scrapy.Field()
    birthday = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
