# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from time import sleep

class DbmoivePipeline(object):
    def process_item(self, item, spider):
        # sleep(30)
        # print "I am sleepping 30s."
        return item
