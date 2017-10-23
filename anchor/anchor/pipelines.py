# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import itertools
import codecs
import pymysql
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class AnchorPipeline(object):

    def __init__(self):
        # 写入csv文件
        # self.csvfile = open('data.csv', 'wb')  # douyu 重新写入
        # self.csvfile = open('anchor.csv', 'ab')  # douyu 重新写入
        # self.csvfile = open('panda.csv', 'wb')  # panda 重新写入
        # self.csvfile = open('douyu.csv', 'wb')  # douyu 重新写入
        self.csvfile = open('douyu3.csv', 'ab')  # douyu 重新写入
        # self.csvfile = open('douyu1.csv', 'wb')  # douyu 重新写入
        # self.csvfile = open('douyu3.bak.csv', 'ab')  # data 重新写入
        # self.csvfile = open('huya.csv', 'wb')  # huya 重新写入
        self.csvfile.write(codecs.BOM_UTF8) # 防止乱码
        self.csvwriter = csv.writer(self.csvfile,  delimiter=',') #将数据作为一系列以逗号分隔的值
        # self.csvwriter.writerow(['userName', 'roomName', 'category', 'fans', 'roomUrl'])
        self.count = 0
        # 写入mysql数据库
        # self.conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="xiaoshuo_db")
        # self.conn.set_charset("utf8")

    def process_item(self, item, spider):
        # 写入csv文件
        row = [item['userName'], item['roomName'], item['category'],item['fans'], item['roomUrl']]
        self.csvwriter.writerow(row)

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
        self.count = self.count + 1
        # print "抓取起点小说网第"+str(self.count)+"条记录"
        # print "抓取起点女生网第"+str(self.count)+"条记录"
        print "抓取第" + str(self.count) + "条记录"
        return item

    # def close_spider(self):
    #     # 关闭conn连接
    #     self.conn.close()
