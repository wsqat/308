# -*- coding: utf-8 -*-

import scrapy
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import HTMLParser
import json
from movieSpider.items import MoviespiderItem
from scrapy.http import Request
from bs4 import  BeautifulSoup
from datetime import datetime

class PiaoFangSpider(scrapy.Spider):
    name = "piaofang"
    allowed_domains = ["piaofang.baidu.com"]
    start_urls = [
        # "https://piaofang.baidu.com/detail/movie?movieId=63014&tab=portrait&sfrom=wise_film_wap&da_channel=wise&da_client=webapp&da_module=film"
        "https://piaofang.baidu.com/?pagelets[]=index-overall&reqID=8&attr=3%2C4%2C5%2C6&t=1514096529103"
        # "https://piaofang.baidu.com/detail/movie?pagelets[]=portrait&reqID=0&movieId=63014&tab=portrait&sfrom=wise_film_wap&da_channel=wise&da_client=webapp&da_module=film&date=2017-12-24&t=1514094577020"
    ]
    # 电影票房的Url
    piaofang_url = "https://piaofang.baidu.com/detail/movie?movieId="

    # 用户画像的Url
    base_url = "https://piaofang.baidu.com/detail/movie?pagelets[]=portrait&reqID=0&movieId="

    # 电影榜单的 movidNames、MovieIdList
    movidNames = []
    movidIds = []

    def parse(self, response):
        url = "https://piaofang.baidu.com"
        yield Request(url, dont_filter=True, callback=self.getMovieDict)

    # 读取字典文件，找到对应的movieId，并抓取票房数据
    def getMovieDict(self, response):
        # 读取字典
        now_date = datetime.now().strftime('%Y-%m-%d')
        now_file = "data/dict_" + now_date + ".json"
        # print now_file
        file_object = open(now_file)
        # 读取电影榜单
        top_file = "data/movieTop.txt"

        try:
            all_the_text = file_object.read()
            # import chardet
            # print chardet.detect(all_the_text)
            # print chardet.detect(open(top_file).read())
            # print type(eval(all_the_text)) # dict
            movieDict = eval(all_the_text)
            # print movieDict
            # 1、spider TopMovie
            for line in open(top_file):
                # print line.strip()
                movieName = line.strip().decode("GB2312").encode("utf-8")
                self.movidNames.append(movieName)
                movieId = movieDict[movieName]
                self.movidIds.append(movieId)
                pf_url = self.piaofang_url + str(movieId)
                # print "spider url:" + pf_url
                yield Request(url=pf_url, dont_filter=True, callback=self.parseMoviePiaoFang,
                              meta={'movieName': movieName, 'movieId': movieId})
            # 2、spider All movie
            # for movieName, movieId in movieDict.items():
            #     # print "key:" + movieName + ",value:" + str(movieId)
            #     pf_url = self.piaofang_url + str(movieId)
            #     print "spider url:" + pf_url
            #     yield Request(url=pf_url, dont_filter=True, callback=self.parseMoviePiaoFang,
            #                   meta={'movieName': movieName, 'movieId': movieId})
            # except:
            # print "请检查文件是否存在，以及电影名称是否正确！"
            # print "please check file and movie's name!"
        finally:
            file_object.close()
        return

    # 电影票房
    def parseMoviePiaoFang(self, response):
        movieName = response.meta['movieName']
        movieId = response.meta['movieId']
        # time.sleep(3)
        detailPgae = response.body
        unicodeDetailPage = detailPgae.decode('utf-8')
        # print unicodeDetailPage
        dateList = re.findall(r'\\"showDate\\":\\"(.*?)\\",\\"box\\"', unicodeDetailPage, re.S)
        print dateList
        boxList = re.findall(r'\\"box\\":\\"(.*?)\\",\\"boxRate\\"', unicodeDetailPage, re.S)
        print boxList
        jsonData = {}
        jsonData['dateList'] = dateList
        jsonData['boxList'] = boxList
        jsonData["movieName"] = movieName
        url = self.base_url + str(movieId)
        yield Request(url=url, dont_filter=True, callback=self.parseMovieDetail,meta={'jsonData': jsonData})
        # yield jsonData

    # 用户画像
    def parseMovieDetail(self, response):
        # time.sleep(3)
        jsonData = response.meta['jsonData']
        movieName = jsonData['movieName']
        # movieId = jsonData['movieId']
        detailPgae = response.body
        unicodeDetailPage = detailPgae.decode('utf-8')
        # print unicodePage
        html = re.findall(r'"html":" (.*?) ",', unicodeDetailPage, re.S)
        # html = re.findall(r'"data - portrait ="(.*?)">,', unicodePage, re.S)
        if html:
            data = re.findall(r'data-portrait=\\"(.*?)\\">', str(html[0]), re.S)
            # print str(html[0])
            # print str(data[0])
            s = str(data[0]).strip()
            html_parser = HTMLParser.HTMLParser()
            portrait = html_parser.unescape(s)
            # print portrait
            portraitData = json.loads(portrait)
            jsonData['portrait'] = portraitData
        else:
            errorMsg = movieName + "'s isnot portrait not found!"
            print errorMsg
            # pf_url = self.piaofang_url + str(jsonData['movieId'])
            # yield Request(url=pf_url, dont_filter=True,
            #               callback=self.parseMoviePiaoFang,meta={'jsonData': jsonData})
        yield jsonData