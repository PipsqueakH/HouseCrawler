# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
import functools

def check_spider_pipeline(process_item_method):

    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):

        # message template for debugging
        msg = '%%s %s pipeline step' % (self.__class__.__name__,)

        # if class is in the spider's pipeline, then use the
        # process_item method normally.
        if self.__class__ in spider.pipeline:
#            spider.log(msg % 'executing', level=log.DEBUG)
            return process_item_method(self, item, spider)

        # otherwise, just return the untouched item (skip this step in
        # the pipeline)
        else:
#            spider.log(msg % 'skipping', level=log.DEBUG)
            return item

    return wrapper

class HousecrawlerPipeline(object):
    @check_spider_pipeline
    def process_item(self, item, spider):
        return item



class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'wb')

    @check_spider_pipeline
    def process_item(self, item, spider):
        print(item)
        line = json.dumps(dict(item)) + "\n"
        self.file.write(item)
        return item


class MongoPipeline(object):

    collection_name = 'house'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, 27017)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item
