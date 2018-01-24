# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import itertools
import codecs
import pymysql
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


count = 0
starttime = datetime.now()
print "开始时间为：" + str(starttime)

class XiaoshuoPipeline(object):
    def __init__(self):
        # 写入csv文件
        now_date = datetime.now().strftime('%Y-%m-%d')
        # filename = "data/"+now_date+"_2.csv"
        # filename = "data/"+now_date+"_1.csv"
        filename = "data/"+now_date+".csv"
        # filename = "data/"+now_date+"_chuangshi.csv"
        # filename = "data/" + now_date + "_17k.csv"
        # filename = "data/" + now_date + "_zhongheng.csv"
        # filename = "data/" + now_date + "_xxsy.csv"
        # filename = "data/" + now_date + "_qidian.csv"
        # filename = "data/" + now_date + "_qidianmm.csv"
        # filename = "data/" + now_date + "_qqdushu.csv"
        self.csvfile = open(filename, 'ab')  # 小说 追加写入
        self.csvfile.write(codecs.BOM_UTF8) # 防止乱码
        self.csvwriter = csv.writer(self.csvfile,  delimiter=',') #将数据作为一系列以逗号分隔的值
        # if self.count == 0:
            # self.csvwriter.writerow(['novel_name', 'author', 'novelurl', 'serialstatus', 'serialnumber', 'category', 'collects','reviews','month'])
        # 写入mysql数据库
        # self.conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="xiaoshuo_db")
        # self.conn.set_charset("utf8")

    def process_item(self, item, spider):
        # 写入csv文件
        row = [item['novel_name'], item['author'], item['novelurl'],item['serialstatus'], item['serialnumber'], item['category'],
                    item['collect_num_total'], item['click_num_total'], item['click_num_month']]
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

        global count
        count += 1
        # print "抓取起点小说网第"+str(self.count)+"条记录"
        # print "抓取起点女生网第"+str(self.count)+"条记录"
        print "抓取第" + str(count) + "条记录"
        return item

    def close_spider(self, spider):
        endtime = datetime.now()
        print "结束时间为：" + str(endtime)
        print "总共执行时间为："+str((endtime - starttime).seconds)+" s"
    #     # 关闭conn连接
    #     self.conn.close()
