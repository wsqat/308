# -*- coding: utf-8 -*-
import scrapy
import requests, time
import re
from scrapy.http import Request
from anchor.items import AnchorItem
import json
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# http://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page=1
# {
#     "status": 200,
#     "message": "",
#     "data": {
#         "page": 1,
#         "pageSize": 120,
#         "totalPage": 74,
#         "totalCount": 8843,
#         "datas": [
#             {
#                 "gameFullName": "英雄联盟",
#                 "gameHostName": "lol",
#                 "boxDataInfo": "",
#                 "totalCount": "1251000",
#                 "roomName": " 卡 尔 ¨ 最强王者 微服私访",
#                 "bussType": "1",
#                 "screenshot": "http://screenshot.msstatic.com/yysnapshot/1710ff0deb1e1aca4eff06eae4905b344799361454af",
#                 "privateHost": "kaerlol",
#                 "nick": "卡尔",
#                 "avatar180": "http://huyaimg.msstatic.com/avatar/1084/b7/896bc815db9560eabbcb4a227f62ba_180_135.jpg",
#                 "gid": "1",
#                 "introduction": "卡尔：卡一牌！AD幻影卡牌大师",
#                 "recommendStatus": "4",
#                 "recommendTagName": "超级明星",
#                 "recommendTagColor": "FF8C00",
#                 "isBluRay": "1",
#                 "screenType": "0",
#                 "liveSourceType": "0",
#                 "uid": "367138632",
#                 "channel": "77259038",
#                 "liveChannel": "2622305980"
#             },

class HuyaSpider(scrapy.Spider):
    name = 'huya'
    allowed_domains = ['www.huya.com']
    start_urls = ['http://www.huya.com/']
    host = 'http://www.huya.com/'
    all_live = 'http://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page=1'
    all_live_url = 'http://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page='
    sort = []

    # def parse(self, response):
    #     pass
    def start_requests(self):
        yield Request(url=self.all_live, dont_filter=True, callback=self.get_all_room)

    # 获取总页数
    def get_all_room(self, response):
        url = response.url
        html = requests.get(url).text
        # soup = BeautifulSoup(html, 'lxml')  
        # jn = json.loads(soup.text)
        jn = json.loads(html)
        totalPage = jn['data']['totalPage']
        print "totalPage:"+str(totalPage)
        # totalPage = 2
        for pageNo in range(1,int(totalPage)+1):
        	url = self.all_live_url + str(pageNo)
        	print url
        	yield Request(url, dont_filter=True, callback=self.get_room_sort)
    
    # 获取房间序号
    def get_room_sort(self, response):
        url = response.url
        # for item in sort:
        html = requests.get(url).text
        # soup = BeautifulSoup(html, 'lxml')  
        # jn = json.loads(soup.text)
        jn = json.loads(html)
        # totalPage = jn['data']['totalPage']
        dataArr = jn['data']['datas']
        for data in dataArr:
            room_url =  self.host + data['privateHost']
            print room_url
            # self.sort.append(room_url)
            anchorItem = AnchorItem()
            anchorItem['userName'] = data['nick']
            anchorItem['roomName'] = data['roomName']
            # anchorItem['audience'] = data['']
            # anchorItem['fans'] = data['fans']
            anchorItem['roomUrl'] = room_url
            anchorItem['category'] = data['gameFullName']
            # yield anchorItem
            yield Request(room_url, dont_filter=True, callback=self.get_room_info, meta={'anchorItem': anchorItem})
        # return "

    # 获取房间信息
    def get_room_info(self, response):
        selector = Selector(response)
        fans = selector.xpath('//div[@id="activityCount"]/text()').extract()[0]
        fans = int(fans)
        # print "fans:"+str(fans)
        anchorItem = response.meta['anchorItem']
        anchorItem['fans'] = fans
        yield anchorItem

