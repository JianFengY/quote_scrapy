# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo

class TextPipeline(object):
    def __init__(self):
        self.limit = 50  # 制定最大长度，超过部分截去加省略号

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][:self.limit].rstrip() + '...'
                return item
        else:
            return DropItem('Missing Text')


class MongoPipeline(object):
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    # 类方法，不需要实例化，不需要 self 参数，但第一个参数需要是表示自身类的 cls 参数，
    # 可以来调用类的属性，类的方法，实例化对象等。
    def from_crawler(cls, crawler):
        """从settings获取信息给当前类初始化"""
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )#相当于返回

    def open_spider(self, spider):
        """爬虫启动时进行的操作"""
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        """数据插入MongoDB"""
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()
