# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # movieId = scrapy.Field()
    # movieName = scrapy.Field()
    # sexInfo =  scrapy.Field()
    # ageInfo = scrapy.Field()
    # region = scrapy.Field()
    # portrait = scrapy.Field()

    pass


class MovieCommentsItem(scrapy.Item):
    movieId = scrapy.Field() #subject_id
    rating = scrapy.Field()
    useful_count = scrapy.Field()

