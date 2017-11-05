# -*- coding: utf-8 -*-  
#!/usr/local/bin/python3
# Pass
__author__='707<707472783@qq.com>'
import urllib.request
import socket
import json
import time
import threading
import os,datetime
import platform
import re,sys,codecs

CHATINFOURL = 'http://riven.panda.tv/chatroom/getinfo?roomid='
IGNORE_LEN = 12
META_LEN = 4
CHECK_LEN = 4
FIRST_REQ = b'\x00\x06\x00\x02'
FIRST_RPS = b'\x00\x06\x00\x06'
KEEPALIVE = b'\x00\x06\x00\x00'
RECVMSG = b'\x00\x06\x00\x03'
DANMU_TYPE = '1'
BAMBOO_TYPE = '206'
AUDIENCE_TYPE = '207'
TU_HAO_TYPE = '306'
SYSINFO = platform.system()
# INIT_PROPERTIES = 'init.properties'
BASE_PATH = "/Users/shiqingwang/Desktop/308/308/anchor/"
INIT_PROPERTIES = BASE_PATH+'danmuSpider/init.properties'
MANAGER = '60'
SP_MANAGER = '120'
HOSTER = '90'

def pp(msg):
    print(msg.encode(sys.stdin.encoding, 'ignore').
        decode(sys.stdin.encoding))
    
def addMsg(msg,roomid):
    try:
        folder = datetime.datetime.now().strftime('%Y-%m-%d')
        File_Path = os.getcwd()+"/"+folder      #获取到当前文件的目录，并检查是否有report文件夹，如果不存在则自动新建report文件
        if not os.path.exists(File_Path):
            os.makedirs(File_Path)
        # os.makedirs(File_Path)
        # print ("路径被创建")
        path = File_Path+"/"+"panda_"+roomid+".txt"
        # print(path)
        file=codecs.open(path,"a","utf-8");
        file.write('\n'+msg)
        file.close()    
    except Exception as e:
        print(e)
        # raise e
    # file = open("pandaChat"+roomid+".txt", "a")
    # file = open("pandaDanmu"+roomid+".txt", "a")
    

def loadInit():
    with open(INIT_PROPERTIES, 'r') as f:
        init = f.read()
        init = init.split('\n')
        # roomid = init[0].split(':')[1]
        roomid = init[0].split(':')[1].split(' ')
        #username = init[1].split(':')[1]
        #password = init[2].split(':')[1]
        return roomid


def notify(title, message):
    pp('[%s] %s' % (title,message))
    if SYSINFO == 'Windows':
        pass
    elif SYSINFO == 'Linux':
        os.system('notify-send {}'.format(': '.join([title, message])))
    else:   #for mac
        t = '-title {!r}'.format(title)
        m = '-message {!r}'.format(message)
        os.system('terminal-notifier {} -sound default'.format(' '.join([m, t])))
        # pp('[%s] %s' % (t,m))


def getChatInfo(roomid):
    with urllib.request.urlopen(CHATINFOURL + roomid) as f:
        data = f.read().decode('utf-8')
        chatInfo = json.loads(data)
        chatAddr = chatInfo['data']['chat_addr_list'][0]
        socketIP = chatAddr.split(':')[0]
        socketPort = int(chatAddr.split(':')[1])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socketIP,socketPort))
        rid      = str(chatInfo['data']['rid']).encode('utf-8')
        appid    = str(chatInfo['data']['appid']).encode('utf-8')
        authtype = str(chatInfo['data']['authType']).encode('utf-8')
        sign     = str(chatInfo['data']['sign']).encode('utf-8')
        ts       = str(chatInfo['data']['ts']).encode('utf-8')
        msg  = b'u:' + rid + b'@' + appid + b'\nk:1\nt:300\nts:' + ts + b'\nsign:' + sign + b'\nauthtype:' + authtype
        msgLen = len(msg)
        sendMsg = FIRST_REQ + int.to_bytes(msgLen, 2, 'big') + msg
        s.sendall(sendMsg)
        recvMsg = s.recv(CHECK_LEN)
        if recvMsg == FIRST_RPS:
            print(' 成功连接房间号为['+str(roomid)+']弹幕服务器')
            recvLen = int.from_bytes(s.recv(2), 'big')
            s.recv(recvLen)
        def keepalive():
            while True:
                #print('================keepalive=================')
                s.send(KEEPALIVE)
                time.sleep(150)
        threading.Thread(target=keepalive).start()

        while True:
            recvMsg = s.recv(CHECK_LEN)
            if recvMsg == RECVMSG:
                recvLen = int.from_bytes(s.recv(2), 'big')
                recvMsg = s.recv(recvLen)   #ack:0
                totalLen = int.from_bytes(s.recv(META_LEN), 'big')
                try:
                    analyseMsg(s, totalLen, roomid)
                except Exception as e:
                    pass

def analyseMsg(s, totalLen, roomid):
    while totalLen > 0:
        s.recv(IGNORE_LEN)
        recvLen = int.from_bytes(s.recv(META_LEN), 'big')
        recvMsg = s.recv(recvLen)
        # recv the whole msg.
        while recvLen > len(recvMsg):
            recvMsg = b''.join(recvMsg, s.recv(recvLen - len(recvMsg)))
        formatMsg(recvMsg, roomid)
        totalLen = totalLen - IGNORE_LEN - META_LEN - recvLen


def formatMsg(recvMsg, roomid):
    # try:
    jsonMsg = eval(recvMsg)
    content = jsonMsg['data']['content']
    if jsonMsg['type'] == DANMU_TYPE:
        # identity = jsonMsg['data']['from']['identity']
        nickName = jsonMsg['data']['from']['nickName']
        # try:
        #     spIdentity = jsonMsg['data']['from']['sp_identity']
        #     if spIdentity == SP_MANAGER:
        #         nickName = '*超管*' + nickName
        # except Exception as e:
        #     pass
        # if identity == MANAGER:
        #     nickName = '*房管*' + nickName
        # if identity == HOSTER:
        #     nickName = '*主播*' + nickName
        #识别表情
        # emoji = re.match(r"(.*)\[:(.*)](.*)", content)
        # if emoji:
        #     content = emoji.group(1) + '*' + emoji.group(2) + '*' + emoji.group(3)
        
        # pp('[%s]: %s' % (nickName,content))
        pp('[%s]: [%s] %s' % (str(roomid),str(nickName),str(content)))
        # print(nickName + ":" + content)
        # msg=",".join([str(time.time()),nickName,content])
        msg = content
        try:
            addMsg(msg,roomid)
        except Exception as e:
            print(e)
            # print(e.message)
            # raise e
        
        
        # notify(nickName, content)

        # elif jsonMsg['type'] == BAMBOO_TYPE:
        #     nickName = jsonMsg['data']['from']['nickName']
        #     print(nickName + "送给主播[" + content + "]个竹子")
        #     notify(nickName, "送给主播[" + content + "]个竹子")
        # elif jsonMsg['type'] == TU_HAO_TYPE:
        #     nickName = jsonMsg['data']['from']['nickName']
        #     price = jsonMsg['data']['content']['price']
        #     print('*********' + nickName + "送给主播[" + price + "]个猫币" + '**********')
        #     notify(nickName, "送给主播[" + price + "]个猫币")
        # elif jsonMsg['type'] == AUDIENCE_TYPE:
        #     print('===========观众人数' + content + '==========')
        # else:
        #     pass
    # except Exception as e:
    #     print(recvMsg)
    #     pass


def testRoomid(roomid):
    if not roomid:
        roomid = input('roomid:')
        with open(INIT_PROPERTIES, 'r') as f:
            init = f.readlines()
            editInit = ''
            for i in init:
                if 'roomid' in i:
                    i = i[:-1] + str(roomid)
                editInit += i + '\n'
        with open(INIT_PROPERTIES, 'w') as f:
            f.write(''.join(editInit))
    return roomid


def main():
    roomids = loadInit()
    print(roomids)
    roomids = testRoomid(roomids)
    print(roomids)
    # getChatInfo(roomid)
    for roomid in roomids:
        threading.Thread(target=getChatInfo, args=([roomid])).start()

if __name__ == '__main__':
    main()
