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
    name = 'douyu_anchor'
    allowed_domains = ['douyu.com']
    # start_urls = ['http://douyu.com/']
    base_url = "http://www.douyu.com/"
    room = 'http://open.douyucdn.cn/api/RoomApi/room/'
    # start_urls=['http://open.douyucdn.cn/api/RoomApi/room/%s' % i for i in [600000,8000000,9000000,10000000]]
    # start_urls=['http://open.douyucdn.cn/api/RoomApi/room/%s' % i for i in range(15,100)]
    # rules = [
    #     Rule(LinkExtractor(allow=(r'http://open.douyucdn.cn/api/RoomApi/room/\d{2,7}$')), callback="get_room_info")
    # ]

    def start_requests(self):
        # maxRoomId = 10000000
        # maxRoomId = 20
        # 140986
        # for roomId in range(1,int(maxRoomId)+1):
        # 153949 475812 484338 532177,567127
        # 2371789 阿冷, 71017 冯提莫, 138286 五五开,67373 陈一发, 688 张大仙, 56040 油条, 
        # 65251 七哥张琪格, 96291 东北大鹌鹑, 7911 韦神, 138243 洞主, 4809 饼干狂魔MasterB
        # 10903 guoyun丶mini, 93912 黑白锐雯, 1229 嗨氏
        # roomIds = [2371789,71017,138286,67373,688,56040,65251,96291,7911,138243,4809,10903,93912,1229]
        # 606118 大司马, 85981 丶蛇哥colin, 
        # 64609
        # roomIds = [606118,85981,154537,507882,414818,259676,280087,318731,588380,64609,58428,24422]
        roomIds = [606118,85981,154537,507882,414818,259676,280087,318731,588380,64609,58428,24422,2371789,71017,138286,67373,688,56040,65251,96291,7911,138243,4809,10903,93912,1229]
        # roomIds = [2371789]
        # for roomId in range(567130,int(maxRoomId)+1):
        for roomId in roomIds:
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
            # print "errCode:"+str(errCode)
            try:
                data = jn['data']
                # print data['owner_name']
                if len(data):
                    # print data['owner_name']
                    anchorItem = AnchorItem()
                    anchorItem['userName'] = data['owner_name']
                    # print data['owner_name']
                    anchorItem['roomName'] = data['room_name']
                    # anchorItem['audience'] = data['']
                    anchorItem['fans'] = data['fans_num']
                    room_url = self.base_url+str( data['room_id'])
                    anchorItem['roomUrl'] = room_url
                    anchorItem['category'] = data['cate_name']
                    anchorItem['avatar'] = data['avatar']
                    anchorItem['plateform'] = u"斗鱼"
                    reward = data['owner_weight']
                    # 1t=1000kg=1000000g=1000000鱼丸=100W鱼丸
                    # print reward
                    # 1t = 1千
                    if "t" in reward :
                        reward = float(reward[:-1])*1000
                    elif "kg" in reward:
                        reward = float(reward[:-2])
                    else :
                        reward = float(reward[:-1])/1000
                    anchorItem['reward'] = reward
                    # print reward
                    # print anchorItem
                    yield anchorItem
            except Exception as e:
                print "error:"
                print e
                pass
