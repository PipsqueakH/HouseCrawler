# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, Compose, TakeFirst
import datetime

class LjSecHand(scrapy.Item):
    strfiltdigit = lambda y: ''.join(filter(lambda x: x in '1234567890.', y))
    # define the fields for your item here like:
    source = scrapy.Field(output_processor = Join(''),)
    category = scrapy.Field(output_processor = Join(''),)
    date = scrapy.Field(output_processor = TakeFirst(),)
    title = scrapy.Field(output_processor = Join(''),)
    url = scrapy.Field(output_processor = Join(''),)
    district = scrapy.Field(output_processor = Join(''),)
    region = scrapy.Field(output_processor = Join(''),)
    total_price = scrapy.Field(output_processor = Compose(lambda v: v[0], strfiltdigit, float))
    layout = scrapy.Field(output_processor = Join(''),)
    area = scrapy.Field(output_processor = Compose(lambda v: v[0], strfiltdigit, float))
    unit_price = scrapy.Field(output_processor = Compose(lambda v: v[0], strfiltdigit, float))
    floor = scrapy.Field(output_processor = Join(''),)
    build_time = scrapy.Field(output_processor = Join(''),)
#    decoration = scrapy.Field()
    direction = scrapy.Field(output_processor = Join(''),)
#    down_payment = scrapy.Field()
#    monthly_payment = scrapy.Field()
    location = scrapy.Field(output_processor = Join(''),)
#    addr = scrapy.Field()
#    last_trade = scrapy.Field()
    subway = scrapy.Field(output_processor = Join(''),)
    taxfree = scrapy.Field(output_processor = Join(''),)
    haskey = scrapy.Field(output_processor = Join(''),)
    pass
