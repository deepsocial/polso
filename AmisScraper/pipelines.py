# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
import os
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))


class AmisJsonPipeline(object):
    def __init__(self):
        self.file = open('items.json', 'wb')
        stf = open(DATA_DIR+'/stop_words.txt', 'r')
        stop_words = [line.rstrip('\n') for line in stf]
        self.stop_words = set(stop_words)

    def process_item(self, item, spider):
        item_dict = dict(item)
        if 'article' in item_dict:
            sanitized_article = [x for x in item_dict['article'] if len(x) > 2 and x not in self.stop_words]
            sanitized_article = " ".join(sanitized_article)
            item_dict['article'] = " ".join(sanitized_article)
            #item_dict['article'] = sanitized_article
        line = json.dumps(item_dict) + "\n"
        self.file.write(line)
        return item


class AmisMongoPipeline(object):

    collection_name = 'scrapy_items'

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
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item