# -*- coding: utf-8 -*-
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
    df = pd.read_csv(fname,header=0,usecols=[0,1,2,3,4])
    # df.iloc[:,[0,1]]
    # 热门主播排行榜，
    lc=pd.DataFrame(df)
    # lc=lc.drop_duplicates(['roomUrl'])
    # lc = lc[lc['category']!=u'热血传奇']
    lc = lc[lc['category']!=u'热血传奇']
    # df[(True-df['appID'].isin([278,382]))] 
    lc=lc.drop_duplicates(['userName'])
    # lc.drop(42927)
    # lc = lc.iloc[:,[0,4]]
    new = lc.sort_values(by=['fans'],ascending=False)
    new = new.head(20)
    # new = lc.sort_values(by=['fans'],ascending=True)
    # new = new.tail(20)
    # print new.shape
    # print new.columns
    # print new
    # new = new.drop([new.columns[[0]]], axis=1,inplace=True) 
    # new = new[['userName','roomName','fans','roomUrl']]
    # print new
    # print new.iloc[:,[0,3]]
    # new.to_csv('rank_list_all.txt', sep='\t', encoding='utf-8')
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
    csvToMysql(newfname)


# 从文件存储到mysql中
def csvToMysql(fname):
    # 写入mysql数据库
    conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="anchor_db")
    conn.set_charset("utf8")
    with open(fname) as csvin:
        reader = csv.reader(csvin, delimiter=",")
        for row in reader:
            # 写入mysql
            if row[0] != "userName":
                userName = str(row[0]).strip()
                roomName = str(row[1]).strip()
                category = str(row[2]).strip()
                if category == u"lol":
                    category = u"英雄联盟"
                fans = row[3]
                roomUrl = row[4]
                plateform = u"斗鱼"
                if "douyu" in roomUrl:
                    plateform = u"斗鱼"
                elif "huya" in roomUrl:
                    plateform = u"虎牙"
                elif "panda" in roomUrl:
                    plateform = u"熊猫"
                time = datetime.datetime.now().strftime('%Y%m%d')

                sql = "insert into anchor(userName,roomName,category,fans,roomUrl,plateform,time) " \
                      "values ('" + userName + "','" + roomName + "','" + category + "','" + fans + "','" + str(roomUrl) + "','" + plateform + "','" + time + "');"
                # print(sql)
                cursor = conn.cursor()
                try:
                    cursor.execute(sql)
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()


if __name__ == '__main__':
    sort_by_key('2017-10-28.csv','rank_list_all')
    # sleep(1000)
    # csvToMysql("rank_list_all_20171028.csv")
    
# 热门主播排行榜
# import matplotlib.pyplot as plt
# present = new.set_index('userName')
# present[:20].plot(kind='barh')
# plt.title(u'热门主播排行榜', fontsize=16)
# plt.xlabel(u'粉丝数', fontsize=16)
# plt.ylabel(u'主播', fontsize=16)
# plt.show()

