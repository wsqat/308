# -*- coding: utf-8 -*-
# import cmd
# import os
# cmd.execute("python danmu3.py 20".split())
# for x in range(1,21):
#     os.system("python danmu3.py "+str(x))

#!/usr/bin/python  
# encoding=utf-8  
# Filename: put_files_hdfs.py  
# 让多条命令并发执行,如让多条scp,ftp,hdfs上传命令并发执行,提高程序运行效率  
import datetime  
import os  
import threading  
import requests, time, json

def execCmd(cmd):  
    try:  
        print "命令 [%s]开始运行%s" % (cmd,datetime.datetime.now())  
        os.system(cmd)  
        print "命令 [%s]结束运行%s" % (cmd,datetime.datetime.now())  
    except Exception, e:  
        print '%s\t 运行失败,失败原因\r\n%s' % (cmd,e)  
  
if __name__ == '__main__':  
    # 需要执行的命令列表  
    # cmds = ['ls','pwd']
    cmds = []
    roomIDArr = [138286, 71017, 67373, 688, 56040, 65251, 96291, 7911, 138243, 4809, 10903, 93912, 1229, 71415, 4332, 85981, 60062, 17349, 122402, 78561, 1991931]
    for x in range(1,21):
        room = 'http://open.douyucdn.cn/api/RoomApi/room/'
        url = room + str(roomIDArr[x])
        # print url
        html = requests.get(url).text
        jn = json.loads(html)
        room_status = int(jn['data']['room_status'])
        if room_status == 1:
            print roomIDArr[x]
       	    # cmds.append("python danmu3.py "+str(x))
      
    #线程池  
    threads = []  
      
    print "程序开始运行%s" % datetime.datetime.now()  
  
    for cmd in cmds:  
        th = threading.Thread(target=execCmd, args=(cmd,))  
        threads.append(th)
        th.start()
           
    # 等待线程运行完毕  
    for th in threads:  
        th.join()  
           
    print "程序结束运行%s" % datetime.datetime.now()  