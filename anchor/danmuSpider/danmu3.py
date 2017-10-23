# -*- coding: utf-8 -*-  
'''
利用第三方模块：danmu
抓取斗鱼弹幕
'''

import time, sys
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

# anchor_name = []
# anchor_roomUrl = []
anchor_roomId = []

def pp(msg):
    print(msg.encode(sys.stdin.encoding, 'ignore').
        decode(sys.stdin.encoding))
    
def addMsg(msg,roomID):
    # f=codecs.open("douyuChat"+roomID+".txt","a","utf-8");
    f=codecs.open("douyuDanmu"+roomID+".txt","a","utf-8");
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
    roomIDs = [138286, 71017, 67373, 688, 56040, 65251, 96291, 7911, 138243, 4809, 10903, 93912, 1229, 71415, 4332, 85981, 60062, 17349, 122402, 78561, 1991931]
    # print anchor_roomId
    # print len(anchor_roomId)
    args=sys.argv
    # roomIDDs = [4332, 122402, 78561, 1991931]
    # print(args)
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
    # begin(roomId)
