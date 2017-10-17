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
    base_url = "http://www.douyu.com"
    start_urls = ['http://www.douyu.com/directory']

    host = 'http://api.douyutv.com/api/v1/live/'
    all_game = 'http://open.douyucdn.cn/api/RoomApi/game'
    # http://open.douyucdn.cn/api/RoomApi/live/lol?limit=90&offset=1100
    live_url = 'http://open.douyucdn.cn/api/RoomApi/live/'
    sort = []


    # def parse(self, response):
    #     pass
    # def start_requests(self):
    #     #yield Request("http://www.douyu.com/3420253", dont_filter=True, callback=self.get_details)
    #     html = requests.get('http://www.douyu.com/directory').text
    #     pq = PyQuery(html)
    #     size = pq.find('.unit').size()
    #     for index in range(size):
    #         item = pq.find('.unit').eq(index)
    #         name = item.find('p').text()
    #         url = item.find('a').attr('href')
    #         # img = item.find('img').attr('data-original')
    #         directory_url = str(self.base_url+url)
    #         # print directory_url
    #         yield Request(directory_url, dont_filter=True, callback=self.get_rooms, meta={'name': name, 'url': url})
        
    # # 获取二级分类主播房间信息
    # def get_rooms(self, response):
    #     name = response.meta['name']
    #     url = response.meta['url']
    #     # print('[%s]Getting Directory => %s'%(directory_info['name']))
    #     # html = requests.get(url).text
    #     html = response.body
    #     pq = PyQuery(html)
    #     size = pq.find('#live-list-contentbox > li').size()
    #     for index in range(size):
    #         item = pq.find('#live-list-contentbox > li').eq(index)
    #         title = item.find('a').attr('title')
    #         url = 'http://www.douyu.com' + item.find('a').attr('href')
    #         username = item.find('.dy-name').text()
    #         category = name
    #         viewers = item.find('.dy-num').text()
    #         anchorItem = AnchorItem()
    #         anchorItem['userName'] = username
    #         anchorItem['roomName'] = title
    #         anchorItem['audience'] = viewers
    #         anchorItem['roomUrl'] = url
    #         anchorItem['category'] = category
    #         yield anchorItem
    #         # if url is not None:
    #         	# yield Request(str(url), dont_filter=True, callback=self.get_details, meta={'anchorItem': anchorItem})
    #         # content = '''
    #         # 房间标题 => %s
    #         # 主播名称 => %s
    #         # 观众数量 => %s
    #         # 分类栏目 => %s
    #         # 房间链接 => %s
    #         # '''%(title, username, viewers, cat, url)
    #         # with open('result2.txt', 'a') as f:
    #         #     f.write(content)
    #     # return ""

    # # 获取三级分类主播人气信息
    # # https://www.douyu.com/swf_api/room/2237055?cdn=&nofan=yes&_t=25134044&sign=f8ff0500d5cdf706d0a705bfd822d846
    # def get_details(self, response):
    #     html = response.body
        # # pq = PyQuery(html)
        # audience = pq.find('.num-v').text()
        # weight = pq.find('.weight-v').text()

        # myPgae = response.body
        # unicodePage = html.decode('utf-8')
        # print unicodePage
        # # 获取当前主播的关注度
        # nic = re.findall(r'<span data-anchor-info="nic">(.*?)</span>', unicodePage, re.S)
        # print "nic: "
        # print nic

        # audience = re.findall(r'<a class="num-v" data-anchor-info="ol-num">(.*?)</a>', unicodePage, re.S)
        # print "audience: "
        # print audience

        # weight = re.findall(r'<a class="weight-v" data-anchor-info="weighttit">(.*?)</a>', unicodePage, re.S)
        # print "weight: "
        # print weight
        # # print "audience: "+str(audience)+"  weight: "+str(weight)+"  nic: "+str(nic)
        # return ""

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
            offset = 100
            # if (str(item['short_name']) == u"LOL"):
            #    offset = 1894
            # if (str(item['short_name']) == u"wzry"):
            #    offset = 1761
            for pageNo in range(1,int(offset)+1):
                url = self.live_url + str(item['short_name']) + "?limit=90&offset=" + str(pageNo)
                self.sort.append(url) # 138个分类
        yield Request(url=self.all_game, dont_filter=True, callback=self.get_room_info)

    # def parserURL(url):
    #     html = requests.get(url).text
    #     soup = BeautifulSoup(html, 'lxml')
    #     jn = json.loads(soup.text)
    #     return jn

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
            html = requests.get(item).text
            # soup = BeautifulSoup(html, 'lxml')
            # jn = json.loads(soup.text)
            jn = json.loads(html)
            try:
                dataArr = jn['data']
                if len(dataArr):
                    for data in dataArr:
                        anchorItem = AnchorItem()
                        anchorItem['userName'] = data['nickname']
                        anchorItem['roomName'] = data['room_name']
                        # anchorItem['audience'] = data['']
                        anchorItem['fans'] = data['fans']
                        room_url = self.base_url+str( data['url'])
                        anchorItem['roomUrl'] = room_url
                        anchorItem['category'] = data['game_name']
                        # yield anchorItem
            except Exception as e:
                continue
           
            # dataArr = jn['data']
            # if len(dataArr):
            #     for data in dataArr:
            #         anchorItem = AnchorItem()
            #         anchorItem['userName'] = data['nickname']
            #         anchorItem['roomName'] = data['room_name']
            #         # anchorItem['audience'] = data['']
            #         anchorItem['fans'] = data['fans']
            #         room_url = self.base_url+str( data['url'])
            #         anchorItem['roomUrl'] = room_url
            #         anchorItem['category'] = data['game_name']
            #         yield anchorItem
            # try:
            #     col.insert(data)
            # except Exception as e:
            #     pass
