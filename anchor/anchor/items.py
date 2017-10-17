# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnchorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
	# 昵称 anchorName
	# 主播ID    ID
	# 观看人数 Audience
	# 粉丝数量（关注度） fansNum
	# 游戏类别 gory
	# 鱼丸重量 weight   熊猫TV是房间竹子量
	# 爬取时间 主播ID是主键和索引
	# 爬取时间 crawlTime
    userName = scrapy.Field()
    # nickId = scrapy.Field()
    # imageurl = scrapy.Field()
    # city = scrapy.Field()
    roomName =  scrapy.Field()
    category = scrapy.Field()
    # audience = scrapy.Field()
    fans = scrapy.Field()
    roomUrl =  scrapy.Field()
    # fansNum = scrapy.Field()
    
    # weight = scrapy.Field()
    # crawlTime = scrapy.Field()
	# 房间标题 => %s
	# 主播名称 => %s
	# 观众数量 => %s
	# 分类栏目 => %s
	# 房间链接 => %s



