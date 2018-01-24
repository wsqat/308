# coding:utf-8
import scrapy
import re
from scrapy.http import Request
from xiaoshuo.items import XiaoshuoItem
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 起点女生网
class QidianMM(scrapy.Spider):
    name = "qidianmm"
    allowed_domains = ["www.qidian.com/all"]
    bash_url = "https://www.qidian.com/mm/all?orderId=8&sign=1&style=1&pageSize=20&siteid=0&hiddenField=0&page=" #1
    #http://chuangshi.qq.com/bk/p/2.html
    # start_urls = ['http://a.qidian.com/mm?orderId=&sign=1&style=1&pageSize=20&siteid=0&hiddenField=0&page=1' % i for i in [1,100]]
    start_urls = ['https://www.qidian.com/mm/all?orderId=8&sign=1&style=1&pageSize=20&siteid=0&hiddenField=0&page=1'] # 总点击

    def parse(self, response):
        # 获取当前页面的最大页码数
        page_num = response.xpath('//ul[@class="lbf-pagination-item-list"]/li[8]/a/text()').extract_first()
        # print page_num
        print u"当前开始爬取起点女生网……"
        # for i in range(1, int(page_num)+1):
        for i in range(1, 3):
            url = self.bash_url + str(i)
            # print url
            yield Request(url, dont_filter=True, callback=self.get_name)  # 将新的页面url的内容传递给get_name函数去处理

    def get_name(self, response):
        myPgae = response.body
        unicodePage = myPgae.decode('utf-8')
        # print  myPgae
        # # 根据正则表达式拿到所有的内容
        # novelsTable = re.findall(r'<ul class="main_con">(.*?)</ul>', unicodePage, re.S)  # 获取当前页面的Table
        # print novelsTable[0]
        novelsList = re.findall(r'<div class="book-mid-info">(.*?)</div>', unicodePage, re.S)  # 获取当前页面的Table
        # print novelsList
        if novelsList:
            for nameinfo in novelsList:
                info = re.findall(r'target="_blank".*?>(.*?)</a>', nameinfo, re.S)  # 小说地址
                novel_name = info[0]
                author = info[1]
                category = info[2]
                novelurl = "https:"+re.findall(r'<a href="(.*?)" target.*?', nameinfo, re.S)[0]
                serial = re.findall(r'<span >(.*?)</span>', nameinfo, re.S)
                serialstatus = serial[0]
                serialnumber = serial[1]
                targentcontent = XiaoshuoItem()
                targentcontent['novel_name'] = novel_name
                targentcontent['author'] = author
                targentcontent['novelurl'] = novelurl
                targentcontent['category'] = category
                targentcontent['serialnumber'] = serialnumber
                targentcontent['serialstatus'] = serialstatus
                # print targentcontent
                if novelurl is not None:
                    yield Request(str(novelurl), dont_filter=True, callback=self.get_novelcontent, meta={'targentcontent': targentcontent})

    def get_novelcontent(self, response):
        selector = Selector(response)
        click_num_total = selector.xpath('//div[@class="book-info "]/p[3]/em[2]/text()').extract()[0]
        click_num_total_status = selector.xpath('//div[@class="book-info "]/p[3]/cite[2]/text()').extract()[0]
        if u'万' in click_num_total_status:
            click_num_total = float(click_num_total) * 10000
        # print str(click_num_total)+" "+ click_num_total_status
        collect_num_total = selector.xpath('//div[@class="book-info "]/p[3]/em[3]/text()').extract()[0]
        collect_num_total_status = selector.xpath('//div[@class="book-info "]/p[3]/cite[3]/text()').extract()[0]
        if u'万' in collect_num_total_status:
            collect_num_total = float(collect_num_total) * 10000
        # print str(collect_num_total) + " " + collect_num_total_status

        # 月推荐票 http://book.qidian.com/info/1004608738
        click_num_month = selector.xpath('//i[@id="recCount"]/text()').extract()[0]
        click_num_month = int(click_num_month) * 4
        # print click_num_month

        targentcontent = response.meta['targentcontent']
        # print targentcontent['novelurl']
        targentcontent['click_num_total'] = int(click_num_total)
        targentcontent['collect_num_total'] = int(collect_num_total)
        targentcontent['click_num_month'] = int(click_num_month)
        # return ""
        yield targentcontent

