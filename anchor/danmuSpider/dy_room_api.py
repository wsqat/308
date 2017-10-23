# -*- coding: utf-8 -*-
# 利用斗鱼API爬取斗鱼全部房间信息保存到Mongodb.py
import json
import requests,re
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# client = MongoClient('localhost')
# db = client["DouyuTV"]
# col = db["Roominfo"]
host = 'http://api.douyutv.com/api/v1/live/'
all_game = 'http://open.douyucdn.cn/api/RoomApi/game'
# http://open.douyucdn.cn/api/RoomApi/live/lol?limit=90&offset=2000
sort = []
CONSTANT = 0
live_url = 'http://open.douyucdn.cn/api/RoomApi/live/'


def parser(url):
    html = requests.get(url).text
    # print html
    # soup = BeautifulSoup(html, 'lxml')
    # json单引号转双引号 否则报错
    # soup = soup.replace("'", "\"");
    # print soup.text
    # jn = json.loads(soup.text);
    jn = json.loads(html);
    # jn = json.loads(removedLastCommaInList);
    # print jzn
    # print soup.prettify()
    # jn = jn.replace("'", "\"");
    # print "666"
    # print jn
    return jn


def get_room_sort(url):
    jn = parser(url)
    data = jn['data']
    for item in data:
        # sort.append(host + item['short_name'])
        offset = 1100
        for pageNo in range(1,int(offset)+1):
            url = live_url + str(item['short_name']) + "?limit=90&offset=" + str(pageNo)
            print url
            sort.append(url) # 138个分类



def get_room_info():
    for item in sort:
        global CONSTANT 
        jn = parser(item)
        data = jn['data']
        try:
            if len(data):
                for item in data:
                    CONSTANT += 1
                    print "count: " + str(CONSTANT) 
                    print item['nickname']
        except Exception as e:
            continue
        
        # print "666"
        # try:
        #     col.insert(data)
        # except Exception as e:
        #     pass


if __name__ == '__main__':
    get_room_sort(all_game)
    get_room_info()
    # a = {u'data': [{u'short_name': u'wzry'}],u'error': 0}
    # jn = json.loads(soup.text);



