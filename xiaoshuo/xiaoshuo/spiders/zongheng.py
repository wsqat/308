# coding:utf-8
import scrapy
import re
from scrapy.http import Request
from xiaoshuo.items import XiaoshuoItem
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ZhongHeng(scrapy.Spider):
    name = "zongheng"
    allowed_domains = ["book.zongheng.com/"]
    bash_url = "http://book.zongheng.com/store/c0/c0/b9/u1/p"
    #http://chuangshi.qq.com/bk/p/2.html
    # start_urls = ['http://book.zongheng.com/store/c0/c0/b9/u0/p%s/v9/s9/t0/ALL.html' % i for i in [1]]
    # start_urls = ['http://book.zongheng.com/store/c0/c0/b9/u0/p%s/v9/s9/t0/ALL.html' % i for i in [1,500,999]]
    # "http://book.zongheng.com/store/c0/c0/b9/u1/p1/v9/s9/t0/ALL.html"
    # 总点击
    start_urls = ['http://book.zongheng.com/store/c0/c0/b9/u1/p1/v9/s9/t0/ALL.html']
    bashurl = '/v9/s9/t0/ALL.html'

    def parse(self, response):
        # for i in range(1,11):
        # max_num = 1000 # 获取当前页面的最大页码数
        page_num = response.xpath('//div[@class="pagenumber pagebar"]/@count').extract_first()
        print page_num
        print u"当前开始爬取纵横小说网……"
        for i in range(1, 3):
        # for i in range(1, int(page_num)+1):
        #     # print  "当前页数："+str(max_num)
            url = self.bash_url  + str(i) + self.bashurl
            print url
            yield Request(url, dont_filter=True, callback=self.get_name)  # 将新的页面url的内容传递给get_name函数去处理

    def get_name(self, response):
        myPgae = response.body
        unicodePage = myPgae.decode('utf-8')
        # print  myPgae
        # # 根据正则表达式拿到所有的内容
        # novelsTable = re.findall(r'<ul class="main_con">(.*?)</ul>', unicodePage, re.S)  # 获取当前页面的Table
        # print novelsTable[0]
        novelsList = re.findall(r'<li>(.*?)</li>', unicodePage, re.S)  # 获取当前页面的Table

        # nameinfo = novelsList[17]
        if novelsList[17:66]:
            for nameinfo in novelsList[17:66]:
                info = re.findall(r'target="_blank">(.*?)</a>', nameinfo, re.S)  # 小说地址
                # print info[1]
                category = info[0]
                novel_name = info[1]
                author = info[3]
                # print author
                novelurl = re.findall(r'<a class="fs14" href="(.*?)" title.*?', nameinfo, re.S)[0]
                serialnumber = re.findall(r'<span class="number">(.*?)</span>', nameinfo, re.S)[0]
                # print serialnumber
                # category = nameinfo.xpath('li/span[1]/a/text()').extract()[0]
                # print category
                # novel_name = nameinfo.xpath('li/span[2]/a[1]/text()').extract()[0]
                # print novel_name
                # novelurl = nameinfo.xpath('li/span[2]/a[1]/@href').extract()[0]
                # print novelurl
                # serialnumber = nameinfo.xpath('li/span[3]/text()').extract()[0]
                # print int(serialnumber)
                # author = nameinfo.xpath('li/span[4]/a/text()').extract()[0]
                # print author
                targentcontent = XiaoshuoItem()
                targentcontent['novel_name'] = novel_name.strip()
                targentcontent['author'] = author.strip()
                targentcontent['novelurl'] = novelurl
                targentcontent['category'] = category
                targentcontent['serialnumber'] = int(serialnumber)
                # print targentcontent
                if novelurl is not None:
                    yield Request(str(novelurl), dont_filter=True, callback=self.get_novelcontent, meta={'targentcontent': targentcontent})

    def get_novelcontent(self, response):
        selector = Selector(response)
        data = selector.xpath('//div[@class="vote_info"]/p/text()').extract()
        if data:
            click_num_month = data[1]
            click_num_total =  data[2]
            collect_num_total = data[3]
            targentcontent = response.meta['targentcontent']

            status = selector.xpath('//div[@class="main"]/div/span/@class').extract()[0]
            # print "status: "+str(status)
            if str(status)== 'serial':
                targentcontent['serialstatus'] = u'连载中'
            else:
                targentcontent['serialstatus'] = u'已完结'
            # author = targentcontent['author']  # 小说作者
            # novelurl = response.url  # 小说地址
            # print author+" "+novelurl
            targentcontent['click_num_total'] = int(click_num_total)
            targentcontent['collect_num_total'] = int(collect_num_total)
            targentcontent['click_num_month'] = int(click_num_month)
            # return ""
            yield targentcontent

