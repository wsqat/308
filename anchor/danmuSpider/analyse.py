# -*- coding: utf-8 -*-  
#! /usr/bin/env python3
#coding=utf-8
import codecs
from pandas import Series,DataFrame,merge
import sys

def readTxtFile(path):
    file=codecs.open(path,"r","utf-8")
    rst=file.readlines()
    for line in rst:
        line=line.strip('\n')
    
    file.close()
    return rst

def writeTxtFile(path,txt):
    f=codecs.open(path,"w","utf-8");
    f.write(txt);
    f.close();

def addObjCount(obj,key):
    if key in obj:
        obj[key]=obj[key]+1
    else:
        obj[key]=1

def getListFromObj(obj):
    rst=[]
    for key in obj:
        data={}
        data["name"]=key
        data["count"]=obj[key]
        rst.append(data)
    rst.sort(key=lambda x:(x["count"]),reverse=True)
    return rst

def printList(datalist):
    dlen=len(datalist)
    msgs=[]
    for i in range(0,dlen):
        data=datalist[i]
        tstr=data["name"]+":"+str(data["count"])
        print(tstr)
        msgs.append(tstr)
    return msgs

def work(filename):       
    lines=readTxtFile(filename)
    giftO={}
    chatO={}
    for line in lines:
        arr=line.split(",")
        if len(arr)<3: continue;
        if line.find("sent a gift!")>=0:
            addObjCount(giftO,arr[1])
            pass
        else:
            addObjCount(chatO,arr[1])
            pass
        
    # gList=getListFromObj(giftO)
    cList=getListFromObj(chatO)

    # print("礼物排行榜")
    # writeTxtFile("gift.txt","\n".join(printList(gList)))
    print("聊天排行榜")
    writeTxtFile("chat.txt","\n".join(printList(cList)))
    

if __name__ == "__main__":
    args=sys.argv
    print(args)
    # filename="douyuChat592227.txt"
    filename="douyuChat4809.txt"
    if(len(args)==2):
        filename=args[1]
    print("filename:",filename);
    work(filename);
