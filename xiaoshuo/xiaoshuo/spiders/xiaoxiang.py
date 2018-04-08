# coding:utf-8
import scrapy
import re
from scrapy.http import Request
from xiaoshuo.items import XiaoshuoItem
import urllib2
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# 潇湘书院
class XXSY(scrapy.Spider):
    name = "xxsy"
    allowed_domains = ["xxsy.net"]
    bash_url = "http://www.xxsy.net/search"
    baseurl = 'http://www.xxsy.net'
    # "http://www.xxsy.net/search?s_wd=&sort=1&pn=1" 总点击
    # 类别 1 - 17
    start_urls = ['http://www.xxsy.net/search?s_wd=&sort=1&pn=1']
    query = '?s_wd=&sort=1&'

    def parse(self, response):
        page_num = response.xpath('//div[@class="pages"]/a[7]/text()').extract_first()
        # print page_num
        # for i in range(1, 2):
        print u"当前开始爬取潇湘书院……"
        # # for i in range(1, 18):
        #     # url = self.bash_url + self.query + str(i)
        #     # yield Request(url, self.parse)
        for num in range(1, 3):
        # for num in range(1, int(page_num) + 1):
            newurl = self.bash_url + self.query + "pn=" + str(num)
            print newurl
            # 此处使用dont_filter和不使用的效果不一样，使用dont_filter就能够抓取到第一个页面的内容，不用就抓不到
            # scrapy会对request的URL去重(RFPDupeFilter)，加上dont_filter则告诉它这个URL不参与去重。
            if newurl is not None:
                yield Request(newurl, dont_filter=True, callback=self.get_name)  # 将新的页面url的内容传递给get_name函数去处理

    def get_name(self, response):
        # baseurl = response.url
        # print baseurl
        myPgae = response.body
        unicodePage = myPgae.decode('utf-8')
        novelsList = re.findall(r'<li>(.*?)</li>', unicodePage, re.S)  # 获取当前页面的Table
        # print len(novelsList)
        # nameinfo = novelsList[10] # 10-29
        # nameinfo2 = novelsList[1]
        # print  nameinfo
        if novelsList[10:30]:
            for nameinfo in novelsList[10:30]:
                novel_name = re.findall(r'target="_blank".*?>(.*?)</a>', nameinfo, re.S)[1]  # 小说地址
                # print name
                novelInfo = re.findall(r'target="blank".*?>(.*?)</a>', nameinfo, re.S)  # 小说地址
                # print novelInfo
                author = novelInfo[0].split(">")[2]
                category = novelInfo[1]
                novelurl = re.findall(r'href="(.*?)"', nameinfo, re.S)[0]
                novelurl = self.baseurl + novelurl
                info = re.findall(r'<span>(.*?)</span>', nameinfo, re.S)  # 小说地址
                serialstatus = info[0]
                click_num_month =  int(info[1].split("：")[1])
                serialnumber = int(info[5].split("：")[1])

                targentcontent = XiaoshuoItem()
                targentcontent['novel_name'] = novel_name.strip()
                targentcontent['author'] = author.strip()
                targentcontent['novelurl'] = novelurl
                targentcontent['serialstatus'] = serialstatus
                targentcontent['serialnumber'] = serialnumber
                targentcontent['category'] = category
                targentcontent['click_num_month'] = int(click_num_month)

                if ".html" in novelurl:
                    # print "novelurl: "+novelurl
                    yield Request(str(novelurl), dont_filter=True, callback=self.get_novelcontent, meta={'targentcontent': targentcontent})

    def get_novelcontent(self, response):
        if ".html" in response.url:
        # print response.body
            selector = Selector(response)
            # print selector
            click_num_total = selector.xpath('//p[@class="sub-data"]/span[2]/em/text()').extract()[0]
            # print click_num_total
            # print click_num_total[len(click_num_total)-1]
            if u"亿" in click_num_total :
                click_num_total = float(click_num_total[:-1])*1000000000
            elif u"万" in click_num_total:
                click_num_total = float(click_num_total[:-1]) * 10000
            click_num_total = float(click_num_total)
            # print click_num_total
            # if click_num_total[:-2] == u'万':
            collect_num_total = selector.xpath('//p[@class="sub-data"]/span[3]/em[1]/text()').extract()[0].strip()
            # print collect_num_total
            if u"亿" in collect_num_total:
                collect_num_total = float(collect_num_total[:-1])*1000000000
            elif  u"万" in collect_num_total:
                collect_num_total = float(collect_num_total[:-1]) * 10000
            else:
                collect_num_total = float(collect_num_total)

            targentcontent = response.meta['targentcontent']
            targentcontent['click_num_total'] = int(click_num_total)
            targentcontent['collect_num_total'] = int(collect_num_total)

            # print targentcontent
            # return ""
            yield targentcontent




