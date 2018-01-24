# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoshuoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    novel_name = scrapy.Field()  # 小说名字
    author = scrapy.Field()  # 作者
    novelurl = scrapy.Field()  # 小说地址
    serialstatus = scrapy.Field()  # 状态
    serialnumber = scrapy.Field()  # 连载字数
    category = scrapy.Field()  # 小说类别
    collect_num_total = scrapy.Field()  # 总收藏
    click_num_total = scrapy.Field()  # 总点击
    click_num_month = scrapy.Field()  # 月点击
    # name_id = scrapy.Field()  # 小说编号
    # novel_breif = scrapy.Field()  # 小说简介
    # pass
