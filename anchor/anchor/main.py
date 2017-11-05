# -*- coding: utf-8 -*-

from scrapy import cmdline
import csv,os
import pandas as pd
import numpy as np
from time import sleep
import datetime
import pymysql
import sys

reload(sys)
# sys.setdefaultencoding('utf-8')
sys.setdefaultencoding('utf_8_sig')



# def sort_by_key(fname,newfname,key):
def sort_by_key(fname,newfname):
    # df = pd.read_csv('douyu3.old.csv',header=0,usecols=[0,1,2,3,4])
    df = pd.read_csv(fname,header=0,usecols=[0,1,2,3,4,5,6,7])
    # df.iloc[:,[0,1]]
    # 热门主播排行榜，
    lc=pd.DataFrame(df)
    # lc=lc.drop_duplicates(['roomUrl'])
    # lc = lc[lc['category']!=u'热血传奇']
    lc = lc[lc['category']!=u'热血传奇']
    lc = lc[lc['plateform']!=u'虎牙']
    # lc = lc[lc['roomUrl']!=u'热血传奇']
    # df[(True-df['appID'].isin([278,382]))] 
    lc=lc.drop_duplicates(['userName'])
    # lc.drop(42927)
    # lc = lc.iloc[:,[0,4]]
    new = lc.sort_values(by=['fans'],ascending=False)
    new = new.head(20)
    newfname1 = newfname+".csv" 
    new.to_csv(newfname1, sep=',', encoding='utf-8-sig')
    # sleep(100)
    filename = datetime.datetime.now().strftime('%Y%m%d')
    newfname2 = newfname+"_"+filename+".csv"
    del_cvs_col(newfname1, newfname2, [0])



# 删除指定列数
def del_cvs_col(fname, newfname, idxs, delimiter=','):
    with open(fname) as csvin, open(newfname, 'w') as csvout:
        reader = csv.reader(csvin, delimiter=delimiter)
        writer = csv.writer(csvout, delimiter=delimiter)
        rows = (tuple(item for idx, item in enumerate(row) if idx not in idxs) for row in reader)
        writer.writerows(rows)
    # 删除文件： 
    os.remove(fname)
    # 存储到数据库中
    sleep(10)
    csvToMysql(newfname)
    # 转化被文本格式
    # csvToText(newfname)


def csvToText(fname):
    filename = datetime.datetime.now().strftime('%Y-%m-%d')
    newfname = filename+".txt"
    douyu_roomId = []
    panda_roomId = []
    rank = '[["排行", "姓名", "平台", "类型", "粉丝数","打赏"],'
    with open(fname) as csvin, open(newfname, 'w') as txtout:
        reader = csv.reader(csvin, delimiter=",")
        index = 1
        for row in reader:
            if row[0] != "userName":
                userName = str(row[0]).strip()
                avatar = str(row[1]).strip()
                roomName = str(row[2]).strip()
                plateform = str(row[3]).strip()
                category = str(row[4]).strip()
                fans = row[5]
                reward = row[6]
                roomUrl = row[7]

                rank += "["+str(index)+","+'"'+userName+'"'+","+'"'+plateform+'"'+","+'"'+category+'"'+","+fans+","+reward+"],"
                index += 1
        rank += "]"
        # print rank
        # f=codecs.open(path,"w","utf-8");
        txtout.write(rank);
        txtout.close();
    



# 从文件存储到mysql中
def csvToMysql(fname):
    # 写入mysql数据库
    # 本地mysql
    conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="anchor_db")
    # 远程mysql
    # conn = pymysql.connect(host="139.199.189.124", user="ouyong", password="hello", db="douban_movie")
    conn.set_charset("utf8")
    with open(fname) as csvin:
        reader = csv.reader(csvin, delimiter=",")
        for row in reader:
            # 写入mysql
            if row[0] != "userName":
                userName = str(row[0]).strip()
                avatar = str(row[1]).strip()
                roomName = str(row[2]).strip()
                plateform = str(row[3]).strip()
                category = str(row[4]).strip()
                fans = row[5]
                reward = row[6]
                roomUrl = row[7]           
                # if "douyu" in roomUrl:
                #     plateform = u"斗鱼"
                # elif "huya" in roomUrl:
                #     plateform = u"虎牙"
                # elif "panda" in roomUrl:
                #     plateform = u"熊猫"
                keywords = ""
                time = datetime.datetime.now().strftime('%Y%m%d')

                sql = "insert into anchor(userName,avatar,roomName,plateform,category,fans,reward,roomUrl,time,keywords) " \
                      "values ('" + userName + "','"+ avatar + "','" + roomName + "','"+ plateform + "','" + category + "','" + fans + "','"+ reward + "','" + str(roomUrl) + "','" + time +"','" + keywords + "');"
                # print(sql)
                cursor = conn.cursor()
                try:
                    cursor.execute(sql)
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()
    conn.close()

def crawlall():
    # pass
    cmdline.execute("scrapy crawlall".split())
    sleep(1800)
    filename = datetime.datetime.now().strftime('%Y-%m-%d')
    folder = datetime.datetime.now().strftime('%Y-%m-%d')
    path = "/Users/shiqingwang/Desktop/308/308/anchor/"+filename+".csv"
    sort_by_key(filename+".csv",'rank_all')
    sleep(5)
    rankFile = "/Users/shiqingwang/Desktop/308/308/anchor/anchor/rank_all_"+folder+".csv"
    return rankFile
    # sleep(10)
    # csvToText("rank_all_20171031.csv")
    # csvToMysql("rank_all_20171031.csv")
    # csvToMysql("rank_all_"+filename+".csv")


# if __name__ == '__main__':
    # # cmdline.execute("scrapy crawlall".split())
    # # 1262
    # # sleep(1300)
    # filename = datetime.datetime.now().strftime('%Y-%m-%d')
    # # filename = 
    # # path = "/Users/shiqingwang/Desktop/308/308/anchor/"+filename+".csv"
    # # sort_by_key(filename+".csv",'rank_all')
    # # sleep(1000)
    # # csvToText("rank_all_20171031.csv")
    # csvToMysql("rank_all_20171031.csv")

