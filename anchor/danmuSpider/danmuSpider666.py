# -*- coding: utf-8 -*-  
'''
利用第三方模块：danmu
抓取斗鱼弹幕
'''

import datetime
import time, sys, os
import codecs
from danmu import DanMuClient
import csv,requests,json
import pandas as pd
from itertools import islice  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from danmu import DanMuClient
import threading
from time import sleep,ctime
import thread

anchor_roomId = []

def pp(msg):
    print(msg.encode(sys.stdin.encoding, 'ignore').
        decode(sys.stdin.encoding))

def mkdir(roomID):
    folder = datetime.datetime.now().strftime('%Y-%m-%d')
    File_Path = ''+folder+''      #获取到当前文件的目录，并检查是否有report文件夹，如果不存在则自动新建report文件
    if not os.path.exists(File_Path):
        os.makedirs(File_Path)
    
def addMsg(msg,roomID):
    # f=codecs.open("douyuChat"+roomID+".txt","a","utf-8");
    # filepath = mkdir(roomID)
    folder = datetime.datetime.now().strftime('%Y-%m-%d')
    File_Path = ''+folder+''      #获取到当前文件的目录，并检查是否有report文件夹，如果不存在则自动新建report文件
    if not os.path.exists(File_Path):
        os.makedirs(File_Path)
        # print os.makedirs(File_Path)
    path = os.getcwd()+"/"+folder+"/"+"douyuDanmu_"+roomID+".txt"
    # print path
    f=codecs.open(path,"a","utf-8");
    f.write('\n'+msg);
    f.close();


def begin(roomID):
    try:
        roomID = str(roomID)
        print "I was at the %s! %s" %(roomID,ctime())
        dmc = DanMuClient('http://www.douyu.com/'+roomID)
        # dmc = DanMuClient(roomUrl)
        if not dmc.isValid(): print('Url not valid')
        @dmc.danmu
        def danmu_fn(msg):
            pp('[%s]: [%s] %s' % (roomID,msg['NickName'], msg['Content']))
            # msg=",".join([str(time.time()),msg['NickName'], msg['Content']])
            msg = str(msg['Content'])
            addMsg(msg,roomID);
            
        dmc.start(blockThread = True)
        # dmc.start()
    except Exception as e:
        print(e)
    
    # dmc.start()

# 获取所有的douyu room_url    
def get_douyu_roomUrl(path):
    # input_file = open(path,"r","utf-8")
    # Python 跳过第一行读取文件内容。
    input_file = open(path)
    for line in islice(input_file, 1, None):
        keyArr = line.split('\t')
        # print keyArr[1] + " --- "+keyArr[5]
        # anchor_name.append(keyArr[1])
        # anchor_roomUrl.append(keyArr[5])
        roomID = keyArr[5].split('/')
        roomID = int(roomID[3])
        anchor_roomId.append(roomID)
        # print roomID
        # begin(str(roomID))
    return ""

def testRoomId(roomIDs):
    roomIDArr = []
    for roomId in roomIDs:
        room = 'http://open.douyucdn.cn/api/RoomApi/room/'
        url = room + str(roomId)
        # print url
        html = requests.get(url).text
        jn = json.loads(html)
        room_status = int(jn['data']['room_status'])
        if room_status == 1:
            roomIDArr.append(roomId)
    return roomIDArr
    
# roomIDs = [2371789,71017,138286,67373,688,56040,65251,96291,7911,138243,4809,10903,93912,1229]
# roomIDs = testRoomId(roomIDs)
# print roomIDs
# roomIDs = [2371789, 67373, 688, 65251, 96291, 7911, 93912, 1229]
# threads = []
# for roomId in roomIDs:
#     print roomId
#     th = threading.Thread(target=begin, args=([roomId]))  ·
#     threads.append(th)

def begin_bat(roomIDs):
    threads = []
    for roomId in roomIDs:
        # print roomId
        threading.Thread(target=begin, args=([roomId])).start()
        # thread.start_new_thread(begin,([roomId],))
        # threads.append(th)

    # for t in threads:
    #     print t
    #     # t.setDaemon(True)  #setDaemon(True)将线程声明为守护线程，必须在start() 方法调用之前设置，如果不设置为守护线程程序会被无限挂起。子线程启动后，父线程也继续执行下去，当父线程执行完最后一条语句print "all over %s" %ctime()后，没有等待子线程，直接就退出了，同时子线程也一同结束。
    #     t.start()
    
    # t.join() #join()方法的位置是在for循环外的，也就是说必须等待for循环里的两个进程都结束后，才去执行主进程。
    
    # print "all over %s" %ctime()



# if __name__ == "__main__":
    # path = "rank_list_douyu.txt"
    # get_douyu_roomUrl(path)
    # anchor_roomId.append("1991931")
    # roomIDs = [138286, 71017, 67373, 688, 56040, 65251, 96291, 7911, 138243, 4809, 10903, 93912, 1229, 71415, 4332, 85981, 60062, 17349, 122402, 78561, 1991931]
    # roomIDs = [56040]
    # 2371789 阿冷, 71017 冯提莫, 138286 五五开,67373 陈一发, 688 张大仙, 56040 油条, 
    # 65251 七哥张琪格, 96291 东北大鹌鹑, 7911 韦神, 138243 洞主, 4809 饼干狂魔MasterB
    # 10903 guoyun丶mini, 93912 黑白锐雯, 1229 嗨氏
    # roomIDs = [2371789,71017,138286,67373,688,56040,65251,96291,7911,138243,4809,10903,93912,1229]
    # roomIDs = [71017, 138286, 688, 96291, 10903, 93912, 1229]
    # print datetime.datetime.now().strftime('%Y-%m-%d')
    # print roomIDs
    # roomIDs = testRoomId(roomIDs)
    # [688, 56040, 65251, 96291, 7911, 4809, 93912, 1229]
    # print roomIDs
    
    # for t in threads:
    #     print t
    #     # t.setDaemon(True)  #setDaemon(True)将线程声明为守护线程，必须在start() 方法调用之前设置，如果不设置为守护线程程序会被无限挂起。子线程启动后，父线程也继续执行下去，当父线程执行完最后一条语句print "all over %s" %ctime()后，没有等待子线程，直接就退出了，同时子线程也一同结束。
    #     t.start()
    
    # t.join() #join()方法的位置是在for循环外的，也就是说必须等待for循环里的两个进程都结束后，才去执行主进程。
    
    # print "all over %s" %ctime()


    # for roomId in roomIDs:
    #     threading.Thread(target=begin, args=([roomId])).start()
    # for roomid in roomIDs:
    # threading.Thread(target=begin, args=([71017])).start()
    # threading.Thread(target=begin, args=([138286])).start()
    # threading.Thread(target=begin, args=([688])).start()
    #线程池  
    # threads = []
    # for roomId in roomIDs:
    #     th = threading.Thread(target=begin, args=([roomId]))  
    #     threads.append(th)
    #     sleep(100)
    #     th.start()
           
    # # 等待线程运行完毕  
    # for th in threads:  
    #     th.join()

    # threading.Thread(target=begin, args=([10903])).start()
    # threading.Thread(target=begin, args=([93912])).start()
    # threading.Thread(target=begin, args=([roomId])).start()
    # begin(roomId)