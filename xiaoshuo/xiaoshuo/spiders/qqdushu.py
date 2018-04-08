# coding:utf-8
import scrapy
import re
from scrapy.http import Request
from xiaoshuo.items import XiaoshuoItem
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# QQ阅读
class QQdushu(scrapy.Spider):
    name = "qqdushu"
    allowed_domains = ["dushu.qq.com/"]
    # bash_url = "http://dushu.qq.com/store/index/sortkey/3/ps/30/p/3000.html"
    bash_url = "http://dushu.qq.com/store/index/sortkey/3/ps/30/p/"
    # 3457*30+19=103729
    # start_urls = ['http://dushu.qq.com/store/index/sortkey/3/ps/30/p/%s.html' % i for i in range(1,1000,1)]
    start_urls = ['http://dushu.qq.com/store/index/sortkey/3/ps/30/p/1.html']

    def parse(self, response):
        # print page_num
        print u"当前开始爬取起点小说网……"
        page_num = 1000
        # for i in range(1, int(page_num) + 1):
        for i in range(1, 3):
            url = self.bash_url+str(i)+".html"
            print url
            yield Request(url, dont_filter=True, callback=self.get_name)  # 将新的页面url的内容传递给get_name函数去处理

    def get_name(self, response):
        myPgae = response.body
        unicodePage = myPgae.decode('utf-8')
        # print  myPgae
        # # 根据正则表达式拿到所有的内容
        # novelsTable = re.findall(r'<ul class="main_con">(.*?)</ul>', unicodePage, re.S)  # 获取当前页面的Table
        # print novelsTable[0]
        # max_num = response.xpath('//div[@class="topbox"]/span/text()').extract_first().split(u"本")[0]
        novelsList = re.findall(r'<div class="bookdetail bg">(.*?)</div>', unicodePage, re.S)  # 获取当前页面的Table
        # print len(novelsList)
        if novelsList:
            for nameinfo in novelsList[1:31]:
                # print nameinfo
                info = re.findall(r'target="_blank".*?>(.*?)</a>', nameinfo, re.S)  # 小说地址
                novel_name = info[0]
                author = info[1]
                category = info[2]
                novelurl = re.findall(r'<a href="(.*?)" target.*?', nameinfo, re.S)[0]
                # serial = re.findall(r'<span >(.*?)</span>', nameinfo, re.S)
                # serialstatus = serial[0]
                # serialnumber = serial[1]
                targentcontent = XiaoshuoItem()
                targentcontent['novel_name'] = novel_name.strip()
                targentcontent['author'] = author.strip()
                targentcontent['novelurl'] = novelurl
                targentcontent['category'] = category
                # < span class ="book_click" > 2013-10-21 < / span >
                update = re.findall(r'<span class="book_click">(.*?)</span>', nameinfo, re.S)[0].split("-")[0]
                if update > 2017:
                    targentcontent['serialstatus'] = u"连载中"
                else:
                    targentcontent['serialstatus'] = u"已完结"
                if novelurl is not None:
                    yield Request(str(novelurl), dont_filter=True, callback=self.get_novelcontent, meta={'targentcontent': targentcontent})

    def get_novelcontent(self, response):
        selector = Selector(response)
        # 字数
        serialnumber = selector.xpath('//dd[@class="w_auth"]/text()').extract()[0]
        # print serialnumber
        if u'万字' in serialnumber :
            serialnumber = float(serialnumber.split("万字")[0]) * 10000
        # print serialnumber
        # 点击
        click_num_total = selector.xpath('//dd[@class="w_auth"]/text()').extract()[1]
        # print click_num_total
        # 收藏
        collect_num_total = selector.xpath('//span[@id="favorCount"]/text()').extract()[0]
        # print collect_num_total
        # 月票 recommendCount
        click_num_month = selector.xpath('//span[@id="recommendCount"]/text()').extract()[0]
        # print click_num_month

        targentcontent = response.meta['targentcontent']
        targentcontent['serialnumber'] = int(serialnumber)
        targentcontent['click_num_total'] = int(click_num_total)
        targentcontent['collect_num_total'] = int(collect_num_total)
        targentcontent['click_num_month'] = int(click_num_month)
        # print targentcontent
        # # return ""
        yield targentcontent

