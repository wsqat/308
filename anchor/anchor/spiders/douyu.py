# -*- coding: utf-8 -*-
import scrapy
import requests, time
from pyquery import PyQuery
import re
from scrapy.http import Request
from anchor.items import AnchorItem
import json
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# http://api.douyutv.com/api/v1/live/ 斗鱼直播间接口
# http://open.douyucdn.cn/api/RoomApi/game 斗鱼分类接口

class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyu.com']
    # start_urls = ['http://douyu.com/']
    base_url = "http://www.douyu.com/"
    start_urls = ['http://www.douyu.com/directory']

    host = 'http://api.douyutv.com/api/v1/live/'
    all_game = 'http://open.douyucdn.cn/api/RoomApi/game'
    # http://open.douyucdn.cn/api/RoomApi/live/lol?limit=90&offset=1100
    live_url = 'http://open.douyucdn.cn/api/RoomApi/live/'
    room = 'http://open.douyucdn.cn/api/RoomApi/room/'
    sort = []

    def start_requests(self):
        yield Request(url=self.all_game, dont_filter=True, callback=self.get_room_sort)

    def get_room_sort(self, response):
        url = response.url
        # jn = self.parserURL(url)
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        jn = json.loads(soup.text)

        data = jn['data']
        for item in data:
            # self.sort.append(self.host + item['short_name']) # 138个分类
            # pageNo = 100
            # offset = (pageNo-1)*limit
            # if (str(item['short_name']) == u"LOL"):
            #    maxPage = 1894
            # if (str(item['short_name']) == u"wzry"):
            maxPage = 6
            # maxPage = 2
            for pageNo in range(1,int(maxPage)+1):
                # url = self.live_url + str(item['short_name']) + "?limit=90&offset=" + str(pageNo)
                offset = (pageNo-1)*90
                url = self.host + str(item['short_name']) + "?limit=90&offset=" + str(offset)
                print url
                self.sort.append(url) # 138个分类
        yield Request(url=self.all_game, dont_filter=True, callback=self.get_room_info)


# {u'ranktype': 0, u'avatar_small': u'https://apic.douyucdn.cn/upload/avatar/025/03/62/34_avatar_small.jpg', 
# u'show_time': u'1508114207', u'vertical_src': u'https://rpic.douyucdn.cn/acrpic/171016/2237055_1110.jpg',
# u'is_noble_rec': 0, u'child_id': 454, u'room_src': u'https://rpic.douyucdn.cn/acrpic/171016/2237055_1110.jpg', 
# u'subject': u'', u'jumpUrl': u'', u'fans': u'202087', u'room_id': u'2237055', u'online': 126018, u'anchor_city': u'',
# u'specific_status': u'0', u'game_name': u'王者荣耀', u'room_name': u'鸡酱今天也要元气满满噢!', u'vod_quality': u'0',
# u'avatar_mid': u'https://apic.douyucdn.cn/upload/avatar/025/03/62/34_avatar_middle.jpg', u'game_url': u'/directory/game/wzry', 
# u'nickname': u'鸡汤叔叔i', u'owner_uid': u'25036234', u'specific_catalog': u'', u'url': u'/2237055', u'cate_id': 181,
# u'avatar': u'https://apic.douyucdn.cn/upload/avatar/025/03/62/34_avatar_big.jpg', u'isVertical': 0, u'show_status': u'1'}

    def get_room_info(self, response):
        # print "666:"+str(len(self.sort))
        for item in self.sort:
            # jn = self.parserURL(item)
            # url = response.url
            # jn = self.parserURL(url)
            html = requests.get(item).text
            # soup = BeautifulSoup(html, 'lxml')
            # jn = json.loads(soup.text)
            # soup = BeautifulSoup(html, 'lxml')
            # jn = json.loads(soup.text)
            jn = json.loads(html)
            # print jn
            try:
                dataArr = jn['data']
                if len(dataArr):
                    for data in dataArr:
                        anchorItem = AnchorItem()
                        anchorItem['userName'] = data['nickname']
                        # print data['nickname']
                        anchorItem['roomName'] = data['room_name']
                        # anchorItem['audience'] = data['']
                        anchorItem['fans'] = data['fans']
                        room_url = self.base_url+str( data['room_id'])
                        anchorItem['roomUrl'] = room_url
                        anchorItem['category'] = data['game_name']
                        anchorItem['avatar'] = data['avatar']
                        anchorItem['plateform'] = u"斗鱼"
                        # reward = data['owner_weight']
                        # 1t=1000kg=1000000g=1000000鱼丸=100W鱼丸
                        # print reward
                        # 1t = 1千
                        # if "t" in reward :
                        #     reward = float(reward[:-1])*1000
                        # elif "kg" in reward:
                        #     reward = float(reward[:-2])
                        # else :
                        #     reward = float(reward[:-1])/1000
                        # anchorItem['reward'] = reward
                        # print reward
                        # print anchorItem
                        # yield anchorItem
                        url = self.room + str( data['room_id'])

                        yield Request(url=url, dont_filter=True, callback=self.get_room_reward, meta={'anchorItem': anchorItem})
            except Exception as e:
                print "error:"
                print e
                pass


    # 获取房间信息
    def get_room_reward(self, response):
        url = response.url
        # jn = self.parserURL(url)
        html = requests.get(url).text
        # soup = BeautifulSoup(html, 'lxml')
        # jn = json.loads(soup.text)
        jn = json.loads(html)
        
        anchorItem = response.meta['anchorItem']

        errCode = int(jn['error'])
        # print errCode
        # print jn['data']
        if errCode == 0:
            # print "errCode:"+str(errCode)
            data = jn['data']
            # print data['owner_name']
            if len(data):
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
                # anchorItem = response.meta['anchorItem']
                print anchorItem
                # return ""
                yield anchorItem
