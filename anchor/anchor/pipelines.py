# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import itertools
import codecs
import pymysql
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

count = 0
starttime = datetime.datetime.now()
print "开始时间为：" + str(starttime)

filename = datetime.datetime.now().strftime('%Y-%m-%d')
csvfile = open(filename+'.csv', 'ab')  # douyu 重新写入
# self.csvfile = open('huya.csv', 'wb')  # huya 重新写入
csvfile.write(codecs.BOM_UTF8) # 防止乱码
csvwriter = csv.writer(csvfile,  delimiter=',') #将数据作为一系列以逗号分隔的值
global count
if count == 0:
    csvwriter.writerow(['userName', 'avatar','roomName', 'plateform','category', 'fans', 'reward', 'roomUrl'])

class AnchorPipeline(object):

    # def __init__(self):
        # 写入csv文件
        # self.csvfile = open('douyu3.csv', 'ab')  # douyu 重新写入
        # self.csvwriter.writerow(['userName', 'roomName', 'category', 'fans', 'roomUrl'])
        # self.count = 0
        # 写入mysql数据库
        # self.conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="xiaoshuo_db")
        # self.conn.set_charset("utf8")
    def process_item(self, item, spider):
        # 写入csv文件
        row = [item['userName'], item['avatar'],item['roomName'],item['plateform'], item['category'],item['fans'],item['reward'], item['roomUrl']]
        csvwriter.writerow(row)
        # 写入mysql
        # name = item["novel_name"]
        # author = item["author"]
        # url = item["novelurl"]
        # category = item["category"]
        # status = item["serialstatus"]
        # number = item["serialnumber"]
        # collect = item["collect_num_total"]
        # click = item["click_num_total"]
        # month = item["click_num_month"]

        # sql = "insert into novel(name,author,url,status,number,category,collect,click,month) " \
        #       "values ('" + name + "','" + author + "','" + url + "','" + status + "','" + str(number) + "','" + category + "','" + str(collect) + "','" + str(click) + "','" + str(month) + "');"
        # print(sql)
        
        # cursor = self.conn.cursor()
        # try:
        #     cursor.execute(sql)
        #     self.conn.commit()
        # except Exception as e:
        #     print(e)
        #     self.conn.rollback()
        #     # pass
        global count
        count += 1
        print "抓取第" + str(count) + "条记录"
        return item

    def close_spider(self, spider):
        endtime = datetime.datetime.now()
        print "结束时间为：" + str(endtime)
        print "总共执行时间为："+str((endtime - starttime).seconds)+" s"