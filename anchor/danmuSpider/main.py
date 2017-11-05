# -*- coding: utf-8 -*-  
'''
利用第三方模块：danmu
抓取斗鱼弹幕
'''
import time, sys
import codecs,os
from danmu import DanMuClient
import csv,requests,json
import pandas as pd
from itertools import islice  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from danmu import DanMuClient
import threading
from time import sleep
# import datetime
import danmuSpider
import pymysql

# from wordCount import *

# import danmu_pd2
# from danmu_pd2 import main

# import time  
# from threading import Timer  
# from datetime import datetime, timedelta  

import sys
sys.path.append("..")
from anchor.main import *

# anchor_name = []
# anchor_roomUrl = []
douyu_roomIds = []
panda_roomIds = []
all_roomIds = []
INIT_PROPERTIES = 'init.properties'
BASE_PATH = "/Users/shiqingwang/Desktop/308/308/anchor/"

# 获取所有的房间号
def get_douyu_roomUrl(path):
    # input_file = open(path,"r","utf-8")
    # Python 跳过第一行读取文件内容。
    input_file = open(path)
    for line in islice(input_file, 1, None):
        keyArr = line.split(',')
        # print keyArr[7]
        roomID = keyArr[7].split('/')
        # print roomID
        roomID = int(roomID[3])
        if str(keyArr[3]) == u'斗鱼':
            douyu_roomIds.append(roomID)
            all_roomIds.append(roomID)
        else:
            panda_roomIds.append(roomID)
            all_roomIds.append(roomID)
        # print roomID
    return douyu_roomIds, panda_roomIds,all_roomIds

# 过滤所有的房间号，获取有效的房间号
def testRoomId(roomIDArr):
    tmp_roomIds = []
    for roomId in roomIDArr:
        room = 'http://open.douyucdn.cn/api/RoomApi/room/'
        url = room + str(roomId)
        # print url
        html = requests.get(url).text
        jn = json.loads(html)
        room_status = int(jn['data']['room_status'])
        if room_status == 1:
            tmp_roomIds.append(roomId)
    return tmp_roomIds

# 写入init
def write_init_proper(roomIDArr):
    file = open(INIT_PROPERTIES, "w")
    msg = "roomid:"
    for roomId in roomIDArr:
        msg += str(roomId)+" "
    # print msg.strip()
    file.write(msg.strip())
    file.close()
    
    # 抓取熊猫弹幕
    danmu_pd2.main()

    return ""


# 字典
keywords_dict = {}
# 扫描指定文件目录下所有wc.txt文件，读取前四行，写入字典
def write_keywords(folder,roomIds):
    path = os.getcwd()+"/"+folder
    #获取到当前文件的目录，并检查是否有report文件夹，如果不存在则自动新建report文件
    files = os.listdir(path)
    # s = []
    for file in files:
        if not os.path.isdir(file):# 不是文件夹才打开
            # f = open(path+"/"+file)
            # s.append(file[:-4])
            if 'wc.txt' in file:
                # print file
                name = file.split('_')
                roomId = str(name[1])
                # print roomId
                # print roomIds
                if int(roomId) in roomIds:
                    key = "http"
                    if "panda" in file:
                        key = "https://www.panda.tv/"+str(roomId)
                    else:
                        key = "http://www.douyu.com/"+str(roomId)
                    filepath = path + "/"+file
                    # print filepath
                    input_file = open(filepath)
                    keywords = ""
                    keyword_count = 0
                    for line in input_file:
                        keyword_count += 1
                        if keyword_count > 4:
                            break
                        else: 
                            keyArr = line.split()
                            # print keyArr[7]
                            keywords += str(keyArr[0])+" "
                    print keywords
                    keywords_dict[key] = keywords.strip()
    # print keywords_dict
    updateAnchor(keywords_dict)
    # print s
    # return s
    
# 修改mysql中anchor表的keyword
def updateAnchor(dict):
    # 写入mysql数据库
    # 本地mysql
    conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="anchor_db")
    # 远程mysql
    # conn = pymysql.connect(host="139.199.189.124", user="ouyong", password="hello", db="douban_movie")
    conn.set_charset("utf8")
    for key,value in dict.items():
        sql = "update anchor set keywords ='"+value+"' where roomUrl = '"+key+"'"
        print(sql)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    conn.close()

# if __name__ == "__main__":
def writeDanmuFile():
    # 1、抓取主播信息
    rankFile = crawlall()
    
    # 2、抓取弹幕
    sleep(10)
    # roomID="1991931"
    # print("roomID:",roomID);
    # begin(roomID);
    # folder = datetime.datetime.now().strftime('%Y%m%d')
    # folder = '20171031'
    # path = BASE_PATH+"anchor/rank_all_"+folder+".csv"
    # douyu_roomIds,panda_roomIds,all_roomIds = get_douyu_roomUrl(path)
    douyu_roomIds,panda_roomIds,all_roomIds = get_douyu_roomUrl(rankFile)
    print all_roomIds
    print douyu_roomIds
    print panda_roomIds
    # douyu_roomIds = [138286, 71017, 606118, 67373, 154537, 688, 288016, 56040, 65251, 96291, 7911, 138243, 4809, 2371789, 10903, 453751, 1229]
    douyu_roomIds = testRoomId(douyu_roomIds)
    print douyu_roomIds
    # [606118, 688, 288016, 138243]
    write_init_proper(panda_roomIds)

    # 3、# 分词统计
    startMulitThread()
    # write_keywords("danmuFiles",all_roomIds)

    # douyu
    # test_roomIds = [68]
    # test_roomIds = [1368050,2098459,3552471,1751899]
    # test_roomIds = [2098459,3552471,1751899]
    # danmuSpider.begin_bat(test_roomIds)
    # danmuSpider.begin_bat(test_roomIds)
    # panda
    # os.system("python3 danmu_pd2.py")
