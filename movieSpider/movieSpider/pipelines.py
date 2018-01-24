# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from datetime import datetime

class MoviespiderPipeline(object):
    now_date = datetime.now().strftime('%Y-%m-%d')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode('unicode_escape'))

    def __init__(self):
        self.file = codecs.open('data/items_' + self.now_date + '.json', 'w', encoding='utf-8') # ab追加写入
        self.file.write("[\n")

    def close_spider(self, spider):
        self.file.write("]")
        self.file.close()