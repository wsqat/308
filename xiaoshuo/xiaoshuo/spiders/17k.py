# coding:utf-8
import scrapy
import re
from scrapy.http import Request
from xiaoshuo.items import XiaoshuoItem
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
import json
from time import sleep

class SeventeenK(scrapy.Spider):
    name = "seventeen"
    allowed_domains = ["all.17k.com/"]
    # bash_url = "http://all.17k.com/lib/book/2_0_0_0_0_0_0_0_1.html?" #1
    base_url = "http://all.17k.com/lib/book/" #2_0_0_0_0_4_0_0_1 # 总点击
    #http://chuangshi.qq.com/bk/p/2.html
    typeArr = ["2_0_0_0_0_4_0_0_", "2_3_0_0_0_4_0_0_", "2_14_0_0_0_4_0_0_", "2_21_0_0_0_4_0_0_", "2_22_0_0_0_4_0_0_",
              "2_23_0_0_0_4_0_0_", "2_24_0_0_0_4_0_0_",
              "3_0_0_0_0_4_0_0_", "3_5_0_0_0_4_0_0_", "3_17_0_0_0_4_0_0_", "3_18_0_0_0_4_0_0_", "3_20_0_0_0_4_0_0_",
              "4_0_0_0_0_4_0_0_", "4_7_0_0_0_4_0_0_", "4_16_0_0_0_4_0_0_", "4_25_0_0_0_4_0_0_", "4_26_0_0_0_4_0_0_",
              "4_27_0_0_0_4_0_0_", "4_28_0_0_0_4_0_0_"]
    start_urls = ['http://all.17k.com/lib/book/2_0_0_0_0_4_0_0_1.html']
    # start_urls = ['http://all.17k.com/lib/book/%s.html' % i for i in typeArr]
    # start_urls = ['http://all.17k.com/lib/book/2_0_0_0_0_0_0_0_1.html?']
    def start_requests(self):
        print u"当前开始爬取17K小说网……"
        for x in self.typeArr:
            url = "http://all.17k.com/lib/book/"+x+"1.html"
            response = urllib2.urlopen(url).read()
            # "<em class="books">17K全站有<strong>"
            max_num = re.findall(r'<em class="books">17K全站有<strong>(.*?)</strong>', response, re.S)[0]
            if max_num:
            # print max_num # 241789
                page_num = int(max_num) / 30    # print page_num  # 8060
            else:
                page_num = 1000
            # for i in range(1, int(page_num) + 1):
            for i in range(1, 3):
                url = "http://all.17k.com/lib/book/"+str(x)+str(i) + ".html"
                print url
                yield Request(url, dont_filter=True, callback=self.get_name)  # 将新的页面url的内容传递给get_name函数去处理
            # yield Request(url, dont_filter=True, callback=self.get_page_num)

    # def get_page_num(self, response):
    #     type_url = response.url.split("1.html")[0]
    #     # print type_url
    #     # 获取当前页面的最大页码数
    #     # 17K全站有241789部符合条件的作品
    #     max_num = response.xpath('//em[@class="books"]/strong/text()').extract_first()
    #     # print max_num # 241789
    #     page_num = int(max_num)/30
    #     print page_num # 8060
    #     for i in range(1, int(page_num)+1):
    #         url = type_url + str(i) + ".html"
    #         print url
    #         yield Request(url, dont_filter=True, callback=self.get_name)  # 将新的页面url的内容传递给get_name函数去处理

    def get_name(self, response):
        myPgae = response.body
        unicodePage = myPgae.decode('utf-8')
        # print  myPgae
        # # 根据正则表达式拿到所有的内容
        # novelsTable = re.findall(r'<ul class="main_con">(.*?)</ul>', unicodePage, re.S)  # 获取当前页面的Table
        # print novelsTable[0]
        novelsList = re.findall(r'<tr class=.*?>(.*?)</tr>', unicodePage, re.S)  # 获取当前页面的Table
        # print len(novelsList)
        # nameinfo = novelsList[0]
        if novelsList:
            for nameinfo in novelsList:
                # print nameinfo
                novelurl = re.findall(r'<a .*? href="(.*?)" target.*?', nameinfo, re.S)[0]
                # print novelurl
                info = re.findall(r'target="_blank".*?>(.*?)</a>', nameinfo, re.S)  # 小说地址
                category = info[0]
                novel_name = info[1]
                author = info[-1]
                # print novel_name+" "+ author + " " + category
                serialnumber = re.findall(r'<td class="td5">(.*?)</td>', nameinfo, re.S)[0]
                # print serialnumber
                serialstatus = re.findall(r'<em class="fc2">(.*?)</em>', nameinfo, re.S)[0]
                serialstatus = serialstatus.strip()
                targentcontent = XiaoshuoItem()
                targentcontent['novel_name'] = novel_name
                targentcontent['author'] = author
                targentcontent['novelurl'] = novelurl
                targentcontent['category'] = category
                targentcontent['serialnumber'] = serialnumber
                targentcontent['serialstatus'] = serialstatus
                # return ""
                # print targentcontent
                # novelurl = "http://www.17k.com/book/1893454.html"
                # print novelurl
                if novelurl is not None:
                    yield Request(str(novelurl), dont_filter=True, callback=self.get_novelcontent, meta={'targentcontent': targentcontent})

    def get_novelcontent(self, response):
        url = response.url
        novelId = url.split("/")[-1].split(".")[0]
        # print novelId
        # http://api.ali.17k.com/v2/book/935571/stat_info?app_key=3362611833
        newurl = "http://api.ali.17k.com/v2/book/"+str(novelId)+"/stat_info?app_key=3362611833"
        req = urllib2.Request(newurl)
        # print req
        res_data = urllib2.urlopen(req)
        # res = res_data.read()
        res = json.load(res_data)
        click_num_total = res['data']['click_info']['total_count']
        click_num_month = res['data']['click_info']['month_count']
        # 鲜花作为总收藏数
        collect_num_total = res['data']['flower_info']['total_count']

        targentcontent = response.meta['targentcontent']
        # print targentcontent
        targentcontent['click_num_total'] = int(click_num_total)
        targentcontent['collect_num_total'] = int(collect_num_total)
        targentcontent['click_num_month'] = int(click_num_month)

        # return ""
        yield targentcontent

