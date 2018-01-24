# -*- coding: utf-8 -*-

import scrapy
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import HTMLParser
import json
from scrapy.http import Request
from datetime import datetime
from bs4 import  BeautifulSoup
import chardet
import requests
import urllib2

class MovieSpider(scrapy.Spider):
    name = "dict"
    allowed_domains = ["piaofang.baidu.com"]
    # https: // piaofang.baidu.com / movie?pagelets[] = movie - list & reqID = 0 & end_date = 2017 - 09 - 24 & date = 2015 - 01 - 04
    start_urls = [
        "https://piaofang.baidu.com/movie?pagelets[]=movie-list&reqID=0&end_date=" + datetime.now().strftime(
            '%Y-%m-%d') + "&date=2015-01-04"  # 2015-01-04
        # "https://piaofang.baidu.com/movie?pagelets[]=movie-list&reqID=0&end_date="+datetime.now().strftime('%Y-%m-%d')+"&date=2018-01-04" # 2015-01-04
    ]
    base_url = "https://piaofang.baidu.com/movie?pagelets[]=movie-list&reqID=0&"

    # 解析生成电影字典，key="movieName",value="movieId"
    def parse(self, response):
        # resp = requests.get(response.url)
        # print resp.encoding # utf-8
        # myPgae = resp.text.encode("gb18030")
        resp = response.body
        myPgae = resp.encode("gb18030")
        # print myPgae
        html = re.findall(r'"html":"(.*?)",', myPgae, re.S)
        # print html
        content = html[0].strip().replace('\n'.encode("gb18030"), ''.encode("gb18030")).strip()
        # print content
        soup = BeautifulSoup(content, "html.parser",from_encoding="GB18030")
        dds = soup.find_all('dd')
        print "total movie: " + str(len(dds))
        dict = {}
        for dd in dds:
            # print dd
            movieName = dd.find('h2').get_text()
            # print movieName
            movieId = dd['data-movie-id'].split('\\"')[1]
            # print movieId
            # movieStr = "'"+movieName+"':"+str(movieId)
            dict[""+movieName+""] = movieId
            # print movieStr
        yield dict

