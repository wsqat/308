# -*- coding: utf-8 -*-

# 主播粉丝榜
# http://open.douyucdn.cn/api/RoomApi/room/

import scrapy
import requests, time
from pyquery import PyQuery
import re
from scrapy.http import Request
from anchor.items import AnchorItem
import json
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# http://api.douyutv.com/api/v1/live/ 斗鱼直播间接口
# http://open.douyucdn.cn/api/RoomApi/game 斗鱼分类接口

class DouyuAnchorSpider(CrawlSpider):
    name = 'douyu_anchuor'
    allowed_domains = ['douyu.com']
    # start_urls = ['http://douyu.com/']
    base_url = "http://www.douyu.com/"
    room = 'http://open.douyucdn.cn/api/RoomApi/room/'
    start_urls=['http://open.douyucdn.cn/api/RoomApi/room/%s' % i for i in [160000,400000,600000,8000000,9000000,10000000]]
    # start_urls=['http://open.douyucdn.cn/api/RoomApi/room/%s' % i for i in range(15,100)]
    # rules = [
    #     Rule(LinkExtractor(allow=(r'http://open.douyucdn.cn/api/RoomApi/room/\d{2,7}$')), callback="get_room_info")
    # ]

    def start_requests(self):
        maxRoomId = 10000000
        # maxRoomId = 20
        # 140986
        # for roomId in range(1,int(maxRoomId)+1):
        for roomId in range(153949,int(maxRoomId)+1):
            url = self.room + str(roomId)
            print url
            yield Request(url, dont_filter=True, callback=self.get_room_info)

    def get_room_info(self, response):
    # def parse(self, response):
        url = response.url
        # jn = self.parserURL(url)
        html = requests.get(url).text
        # soup = BeautifulSoup(html, 'lxml')
        # jn = json.loads(soup.text)
        jn = json.loads(html)

        errCode = int(jn['error'])
        # print errCode
        # print jn['data']
        if errCode == 0:
            print errCode
            try:
                data = jn['data']
                # print data['owner_name']
                if len(data):
                    anchorItem = AnchorItem()
                    anchorItem['userName'] = data['owner_name']
                    # print data['owner_name']
                    anchorItem['roomName'] = data['room_name']
                    # anchorItem['audience'] = data['']
                    anchorItem['fans'] = data['fans_num']
                    room_url = self.base_url+str( data['room_id'])
                    anchorItem['roomUrl'] = room_url
                    anchorItem['category'] = data['cate_name']
                    yield anchorItem
            except Exception as e:
                pass
