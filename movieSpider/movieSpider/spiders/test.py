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


class BaiduSpider(scrapy.Spider):
    name = "baidu"
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

    def parse(self, response):
        # time.sleep(3)
        myPgae = response.body
        unicodePage = myPgae.decode('utf-8')
        # print unicodePage
        html = re.findall(r'"html":"(.*?)",', unicodePage, re.S)
        content = html[0].encode("gbk").strip().replace('\\n','').strip()
        # print content
        content =content.replace('\\"','\"')
        # print content
        soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
        dds = soup.find_all('dd')
        for dd in dds:
            # print dd
            movieName = dd.find('b').get_text()
            # print movieName
            movieId = dd['data-movie-id']
            # print dd['data-movie-id'], dd.get_text()  # 94906芳华上映10日5596万6.4万172.6万278693233.7 % 23.4 % 31.6 % 24.4 %
            # url = self.base_url + str(movieId)
            pf_url = self.piaofang_url + str(movieId)
            yield Request(url=pf_url, dont_filter=True,callback=self.parseMoviePiaoFang, meta={'movieName': movieName,'movieId': movieId})
            # yield Request(url=url, dont_filter=True, callback=self.parseMovieDetail,meta={'movieName': movieName})
            # yield Request(url="https://piaofang.baidu.com/detail/movie?movieId=95322", dont_filter=True, callback=self.parseMoviePiaoFang)

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
