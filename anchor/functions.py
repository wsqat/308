# -*- coding: utf-8 -*-  
'''
利用第三方模块：danmu
抓取斗鱼弹幕
'''
import time, sys
import codecs,os
# from danmu import DanMuClient
import csv,requests,json
import pandas as pd
from itertools import islice  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# from danmu import DanMuClient
import threading
from time import sleep
# import datetime
# import danmuSpider
import pymysql

# from danmuSpider.wordCount import *

# import danmu_pd2
# from danmuSpider.danmu_pd2 import *
# from danmu_pd2 import main

# import time  
# from threading import Timer  
# from datetime import datetime, timedelta  

from anchor.main import *
# import danmu_pd

# anchor_name = []
# anchor_roomUrl = []
douyu_roomIds = []
panda_roomIds = []
all_roomIds = []
BASE_PATH = "/Users/shiqingwang/Desktop/308/308/anchor/"
INIT_PROPERTIES = BASE_PATH+'danmuSpider/init.properties'

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
    # danmu_pd.main()
    os.system("python3 danmu_pd2.py")

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



import sys  
reload(sys)  
  
sys.setdefaultencoding('utf-8')  
  
import jieba,datetime,os
import jieba.analyse  
# import xlwt #写入Excel表的库  
import threading
from time import ctime,sleep


def wordCount(fname,newname):
# def wordCount(oldpath,newpath):
    # wbk = xlwt.Workbook(encoding = 'ascii')  
    # sheet = wbk.add_sheet("wordCount")#Excel单元格名字
    print "I was at the %s! %s" %(fname,ctime())  
    word_lst = []  
    key_list=[]  
    for line in open(fname):#1.txt是需要分词统计的文档  
  
        item = line.strip('\n\r').split('\t') #制表格切分  
        # print item  
        jieba.analyse.set_stop_words('stopword.txt')
        tags = jieba.analyse.extract_tags(item[0],20) #jieba分词  
        for t in tags:  
            word_lst.append(t)  
  
    word_dict= {}  
    with open(newname,'w') as wf2: #打开文件  
  
        for item in word_lst:  
            if item not in word_dict: #统计数量  
                word_dict[item] = 1  
            else:  
                word_dict[item] += 1  
  
        orderList=list(word_dict.values())  
        orderList.sort(reverse=True)  
        # print orderList  
        for i in range(len(orderList)):  
            for key in word_dict:  
                if word_dict[key]==orderList[i]:  
                    wf2.write(key+' '+str(word_dict[key])+'\n') #写入txt文档  
                    key_list.append(key)  
                    word_dict[key]=0  
    
    # for i in range(len(key_list)):  
    #     sheet.write(i, 1, label = orderList[i])  
    #     sheet.write(i, 0, label = key_list[i])  
    # wbk.save('wordCount.xls') #保存为 wordCount.xls文件

# 扫描指定文件目录下所有文件
def getFileNames(folder):
    path = os.getcwd()+"/"+folder
    #获取到当前文件的目录，并检查是否有report文件夹，如果不存在则自动新建report文件
    files = os.listdir(path)
    s = []
    for file in files:
        if not os.path.isdir(file):# 不是文件夹才打开
            # f = open(path+"/"+file)
            if 'wc.txt' not in file:
                s.append(file[:-4])
    return s


# 封装wc方法
def startMulitThread():
    folder = datetime.datetime.now().strftime('%Y-%m-%d')
    # folder = "2017-10-27"
    # folder = "danmuFiles"
    filenames = getFileNames(folder)
    # filenames = ['panda_6666']
    threads = []
    for filename in filenames:
        print filename
        # newname = filename + "_wc.txt"
        # fname = filename + ".txt"
        oldpath = os.getcwd()+"/"+folder+"/"+filename + ".txt"
        newpath = os.getcwd()+"/"+folder+"/"+filename + "_wc.txt"
        t1 = threading.Thread(target=wordCount,args=(oldpath,newpath))
        threads.append(t1)

    for t in threads:
        print t
        # t.setDaemon(True)  #setDaemon(True)将线程声明为守护线程，必须在start() 方法调用之前设置，如果不设置为守护线程程序会被无限挂起。子线程启动后，父线程也继续执行下去，当父线程执行完最后一条语句print "all over %s" %ctime()后，没有等待子线程，直接就退出了，同时子线程也一同结束。
        t.start()
    
    t.join() #join()方法的位置是在for循环外的，也就是说必须等待for循环里的两个进程都结束后，才去执行主进程。
    
    print "all over %s" %ctime()