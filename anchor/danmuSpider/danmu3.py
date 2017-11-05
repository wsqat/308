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
import datetime

# anchor_name = []
# anchor_roomUrl = []
anchor_roomId = []

def pp(msg):
    print(msg.encode(sys.stdin.encoding, 'ignore').
        decode(sys.stdin.encoding))
    
def addMsg(msg,roomID):
    # f=codecs.open("douyuChat"+roomID+".txt","a","utf-8");
    # f=codecs.open("douyuDanmu_1023_"+roomID+".txt","a","utf-8");
    # folder = "2017-10-27"
    folder = datetime.datetime.now().strftime('%Y-%m-%d')
    File_Path = ''+folder+''      #获取到当前文件的目录，并检查是否有report文件夹，如果不存在则自动新建report文件
    if not os.path.exists(File_Path):
        print os.makedirs(File_Path)
    path = os.getcwd()+"/"+folder+"/"+"douyuDanmu_"+roomID+".txt"
    f=codecs.open(path,"a","utf-8");
    f.write('\n'+msg);
    f.close();

# roomID="641207"
# roomID="1991931"
# roomID="s7"
    
def begin(roomID):
    # for roomID in anchor_roomId:
    #     roomID = str(roomID)
    #     print roomID
    roomID = str(roomID)
    dmc = DanMuClient('http://www.douyu.com/'+roomID)
    # dmc = DanMuClient(roomUrl)
    if not dmc.isValid(): print('Url not valid')
    @dmc.danmu
    def danmu_fn(msg):
        pp('[%s]: [%s] %s' % (roomID,msg['NickName'], msg['Content']))
        # msg=",".join([str(time.time()),msg['NickName'], msg['Content']])
        msg = str(msg['Content'])
        addMsg(msg,roomID);

    # @dmc.gift
    # def gift_fn(msg):
    #     pp('[%s]:[%s] sent a gift!' % (roomId,msg['NickName']))
    #     msg=",".join([str(time.time()),msg['NickName'],"sent a gift!"])
    #     addMsg(msg);

    # @dmc.other
    # def other_fn(msg):
    #     pp('[%s]:Other message received'% msg['NickName'])
        
    dmc.start(blockThread = True)

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
    # file=codecs.open(path,"r","utf-8")
    # rst=file.readlines()
    # for line in rst:
    #     line=line.strip('\n')
    #     keyArr = line.split('\t')
    #     print keyArr[1] + " --- "+keyArr[5]
    #     anchor_name.append(keyArr[1])
    #     # anchor_roomUrl.append(keyArr[5])
    #     roomID = keyArr[5].split('/')
    #     if len(roomID) > 1:
    #         roomID = roomID[1]
    #     print roomID
    # file.close()
    # return rst
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
    

if __name__ == "__main__":
    # roomID="1991931"
    # print("roomID:",roomID);
    # begin(roomID);

    # path = "rank_list_douyu.txt"
    # get_douyu_roomUrl(path)
    # anchor_roomId.append("1991931")
    # roomIDs = [138286, 71017, 67373, 688, 56040, 65251, 96291, 7911, 138243, 4809, 10903, 93912, 1229, 71415, 4332, 85981, 60062, 17349, 122402, 78561, 1991931]
    # print anchor_roomId
    # print len(anchor_roomId)

    # roomIDs = [56040]
    # 2371789 阿冷, 71017 冯提莫, 138286 五五开,67373 陈一发, 688 张大仙, 56040 油条, 
    # 65251 七哥张琪格, 96291 东北大鹌鹑, 7911 韦神, 138243 洞主, 4809 饼干狂魔MasterB
    # 10903 guoyun丶mini, 93912 黑白锐雯, 1229 嗨氏
    # roomIDs = [2371789,71017,138286,67373,688,56040,65251,96291,7911,138243,4809,10903,93912,1229]
    # roomIDs = [71017, 138286, 688, 96291, 10903, 93912, 1229]
    args=sys.argv
    print(args)
    if(len(args)==2):
        # roomIDIndex=int(args[1])
        # roomID = str(roomIDArr[roomIDIndex])
        # roomID = str(args[1])
        roomId = int(args[1])
        begin(roomId)
    # print roomIDs
    # roomIDs = testRoomId(roomIDs)
    # print roomIDs
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
