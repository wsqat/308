# -*- coding: utf-8 -*-

import scrapy
import re
import time
import HTMLParser
import json
from scrapy.http import Request
from bs4 import  BeautifulSoup
import scrapy
import requests, time
from pyquery import PyQuery
import re
from scrapy.http import Request
import json
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import urllib
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class DoubanMovieSpider(scrapy.Spider):
    name = "comments"
    allowed_domains = ["api.douban.com"]
    # start_urls = ['http://douyu.com/']
    prefix_url = "https://api.douban.com/v2/movie/subject/"
    suffix_url = "/reviews?apikey=0b2bdeda43b5688921839c8ecb20399b&start="
    super_suffix_url ="&count=100&client=&udid="
    # "https://api.douban.com/v2/movie/subject/1295644/reviews?apikey=0b2bdeda43b5688921839c8ecb20399b&start=&count=100&client=something&udid=dddddddddddddddddddddd"
    # start_urls=['http://open.douyucdn.cn/api/RoomApi/room/%s' % i for i in [600000,8000000,9000000,10000000]]
    # start_urls=['http://open.douyucdn.cn/api/RoomApi/room/%s' % i for i in range(15,100)]
    count = 1

    def start_requests(self):
        movieIds = [1295644,3287562]
        movieNames = ["这个杀手不太冷","神偷奶爸"]
        for movieId in movieIds:
            movieName = movieNames[movieIds.index(movieId)]
            page = 40 # 40
            for page in range(1,int(page)+1):
                url = self.prefix_url + str(movieId) + self.suffix_url + str(int(page-1)*100) + self.super_suffix_url
                # print url
                yield Request(url, dont_filter=True, callback=self.get_comments_info,meta={'movieName':movieName})

    def get_comments_info(self, response):
        movieName = response.meta['movieName']
        html = response.body
        jn = json.loads(html)
        if len(jn['reviews']) > 0:
            with codecs.open("comments/" + str(movieName) + ".txt", "ab",encoding='utf-8') as f:
                try:
                    reviews = jn['reviews']
                    for review in reviews:
                        comment = review["content"]
                        comment = comment.replace("\n","").replace("\t","").strip()
                        f.writelines(comment+"\n")
                        self.count += 1
                except Exception as e:
                    print e
            f.close()
            print "total count: "+str(self.count)
