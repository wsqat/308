# coding:utf-8
import scrapy
import re
from scrapy.http import Request
from xiaoshuo.items import XiaoshuoItem
from scrapy.selector import Selector
from fontTools.ttLib import TTFont

import requests
from lxml import html
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
                targentcontent['novel_name'] = novel_name.strip()
                targentcontent['author'] = author.strip()
                targentcontent['novelurl'] = novelurl
                targentcontent['category'] = category
                targentcontent['serialnumber'] = serialnumber
                targentcontent['serialstatus'] = serialstatus
                # print targentcontent
                if novelurl is not None:
                    yield Request(str(novelurl), dont_filter=True, callback=self.get_novelcontent, meta={'targentcontent': targentcontent,'url':novelurl})

    def get_novelcontent(self, response):
        myPgae = response.body
        targentcontent = response.meta['targentcontent']
        unicodePage = myPgae.decode('utf-8')
        selector = Selector(response)
        url = response.meta['url']
        # 获取页面内容
        r = requests.get(url)
        response = html.fromstring(r.text)
        cmp = re.compile("url\('(//.*.woff)'\) format\('woff'\)")
        rst = cmp.findall(r.text)
        fontUrl = str(rst[0]).split('\'')[8]
        fontName = fontUrl.split('/')[4].split(".")[0]
        ttf = requests.get(fontUrl, stream=True)
        with open("./font/qidianmm.woff", "wb") as pdf:
            for chunk in ttf.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)

        font = TTFont('./font/qidianmm.woff')
        cmap = font.getBestCmap()
        glyphs = font.getGlyphOrder()[2:]
        tmp_dic = {}
        for num, un_size in enumerate(glyphs):
            font_uni = un_size.replace('uni', '0x').lower()
            tmp_dic[font_uni] = num
        tmp_dic['period'] = "."

        numbers = re.findall(r'<span class="'+fontName+'">(.*?)</span>', unicodePage, re.S)  # 获取当前页面的Table
        if len(numbers) > 0:
            serialnumber = numbers[0]
            serialnumber = self.decode(serialnumber,cmap,tmp_dic)
            # 历史点击
            click_num_total = numbers[1]
            click_num_total = self.decode(click_num_total, cmap, tmp_dic)
            # 本月点击
            click_num_month = numbers[2]
            click_num_month = self.decode(click_num_month, cmap, tmp_dic)
            # 历史收藏
            collect_num_total = numbers[3]
            collect_num_total = self.decode(collect_num_total, cmap, tmp_dic)

            targentcontent['serialnumber'] = int(serialnumber)
            targentcontent['click_num_total'] = int(click_num_total)
            targentcontent['click_num_month'] = int(click_num_month) * 4
            targentcontent['collect_num_total'] = int(collect_num_total)
            yield targentcontent

    # 解密数字
    def decode(self,old,cmap,tmp_dic):
        sourcehtml = old.replace('&#', '0')
        olds = sourcehtml.split(';')
        olds = olds[0:-1]
        new = ""
        for key in olds:
            key = int(key)
            new += str(tmp_dic[cmap[key]])
        if "." in new:
            new = float(new)*10000
        return new