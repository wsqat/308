# # -*- coding: utf-8 -*-

# # 主播粉丝榜
# # http://open.douyucdn.cn/api/RoomApi/room/

# import scrapy
# import requests, time
# from pyquery import PyQuery
# import re
# from scrapy.http import Request
# from anchor.items import AnchorItem
# import json
# from bs4 import BeautifulSoup
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# # http://api.douyutv.com/api/v1/live/ 斗鱼直播间接口
# # http://open.douyucdn.cn/api/RoomApi/game 斗鱼分类接口

# class DouyuRankSpider(scrapy.Spider):
#     name = 'douyu_rank'
#     allowed_domains = ['douyu.com']
#     base_url = "http://www.douyu.com/"
#     room = 'http://open.douyucdn.cn/api/RoomApi/room'
#     # rank_url = "https://www.douyu.com/directory/rank_list/game"
#     start_urls = ['http://www.douyu.com/directory']
#     host = 'http://api.douyutv.com/api/v1/live/'
#     all_game = 'http://open.douyucdn.cn/api/RoomApi/game'
#     # http://open.douyucdn.cn/api/RoomApi/live/lol?limit=90&offset=1100
#     live_url = 'http://open.douyucdn.cn/api/RoomApi/live/'
#     sort = []

#     # def start_requests(self):
#     #     yield Request(url=self.rank_url, dont_filter=True, callback=self.get_rank_list)

#     # def get_rank_list(self, response):
#     #     myPgae = response.body
#     #     unicodePage = myPgae.decode('utf-8')
#     #     roomList = re.findall(r'href="(.*?)"', unicodePage, re.S)  # 获取当前页面的Table
#     #     print roomList
    
#     # 获取一级直播分类
#     def start_requests(self):
#         html = requests.get('http://www.douyu.com/directory').text
#         pq = PyQuery(html)
#         size = pq.find('.unit').size()
#         for index in range(size):
#             item = pq.find('.unit').eq(index)
#             name = item.find('p').text()
#             url = item.find('a').attr('href')
#             # img = item.find('img').attr('data-original')
#             directory_url = str(self.base_url+url)
#             print "directory_url: "+directory_url
#             yield Request(directory_url, dont_filter=True, callback=self.get_rooms, meta={'name': name, 'url': url})
        
#     # 获取二级分类主播房间信息
#     def get_rooms(self, response):
#         name = response.meta['name']
#         url = response.meta['url']
#         # print('[%s]Getting Directory => %s'%(directory_info['name']))
#         # html = requests.get(url).text
#         html = response.body
#         pq = PyQuery(html)
#         size = pq.find('#live-list-contentbox > li').size()
#         for index in range(size):
#             item = pq.find('#live-list-contentbox > li').eq(index)
#             title = item.find('a').attr('title')
#             url = self.room + item.find('a').attr('href')
#             print "url: "+url
#             username = item.find('.dy-name').text()
#             category = name
#             viewers = item.find('.dy-num').text()
#             anchorItem = AnchorItem()
#             anchorItem['userName'] = username
#             anchorItem['roomName'] = title
#             # anchorItem['audience'] = viewers
#             anchorItem['roomUrl'] = url
#             anchorItem['category'] = category
#             # yield anchorItem
#             # if url is not None:
#             # return ""
#             yield Request(url, dont_filter=True, callback=self.get_room_info, meta={'anchorItem': anchorItem})
#             # content = '''
#             # 房间标题 => %s
#             # 主播名称 => %s
#             # 观众数量 => %s
#             # 分类栏目 => %s
#             # 房间链接 => %s
#             # '''%(title, username, viewers, cat, url)
#             # with open('result2.txt', 'a') as f:
#             #     f.write(content)
#         # return ""

#     # 获取三级分类主播房间人气信息
#     def get_room_info(self, response):
#         url = response.url
#         anchorItem = response.meta['anchorItem']
#         # jn = self.parserURL(url)
#         html = requests.get(url).text
#         soup = BeautifulSoup(html, 'lxml')
#         jn = json.loads(soup.text)
#         # errCode = jn['error']
#         # if errCode == 0:
#         data = jn['data']
#         anchorItem['fans'] = int(data['fans_num'])
#         # print anchorItem
#         yield anchorItem

#           