# -*- coding: utf-8 -*-
import scrapy
import datetime,re
from scrapy.loader import ItemLoader
from anchor.items import AnchorItem
from anchor.utils.ListUtils import trim_list
from anchor.utils.PandaUtils import get_address, get_room_detail_json, replace_html_marker
# from PanDaTVCrawler.ItemLoader_Pack.PandaItemLoader import PandaItemLoader

import json

# http://www.panda.tv/ajax_search?token=&name=&class={category}&order_cond=fans&province={address}&pagenum=20&pageno=1
# 熊猫TV直播间接口
class PandaSpider(scrapy.Spider):
    name = 'panda'
    redis_key = 'panda:start_urls'

    start_urls = ['http://www.panda.tv/search?kw=']

    room_url = "http://www.panda.tv/ajax_search?token=&name=&class={category}&order_cond=fans" \
               "&province={address}&pagenum=20&pageno=1"

    # 在这个页面需要提取出所有分类 与 地区
    def parse(self, response):
        # print response.url
        # print response.body
        # print "xxxx"
        category_list = trim_list(response.css("a.child-title::attr(data-cate)").extract())
        address_list = tuple([""] + response.css("div.list-bar-item-dropdown-item a::attr(data-province)").extract())

        for url in (self.room_url.format(category=category, address=address)
                    for category in category_list for address in address_list):
            yield scrapy.Request(url=url, callback=self.parse_room_url, dont_filter=True)
            # return
        # url = "http://www.panda.tv/ajax_search?token=&name=&class=lol&order_cond=fans&province=&pagenum=20&pageno=1"
        # yield scrapy.Request(url=url, callback=self.parse_room_url, dont_filter=True)

    # 提取出房间信息，并且 yield 下一个页面
    def parse_room_url(self, response):

        url = response.url
        # print response.body
        address = get_address(response.url)

        json_text = json.loads(response.text)

        if len(json_text['data']['items']) == 0:
            return

        for room_host in (json_text['data']['items']):
            # itemLoader = PandaItemLoader(item=PandaItem(), response=response)

            # itemLoader.add_value("host_bamboos", room_host['bamboos'])
            # itemLoader.add_value("room_type", room_host['class'])
            # itemLoader.add_value("room_fans", room_host['fans'])
            # itemLoader.add_value("host_id", room_host['hostid'])
            # itemLoader.add_value("host_name", room_host['nickname'])
            # itemLoader.add_value("room_name", room_host['name'])
            # itemLoader.add_value("room_id", room_host['roomid'])
            # itemLoader.add_value("host_address", address)
            # itemLoader.add_value("room_label", room_host['classification'])
            # itemLoader.add_value("crawled_at", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # item = itemLoader.load_item()

            room_url = "https://www.panda.tv/" + room_host['roomid']
            anchorItem = AnchorItem()
            anchorItem['userName'] = room_host['nickname']

            anchorItem['roomName'] = room_host['name']
            # anchorItem['audience'] = room_host['fans']
            anchorItem['fans'] = room_host['fans']
            anchorItem['roomUrl'] = room_url
            # anchorItem['category'] = room_host['class']
            anchorItem['category'] = room_host['classification']
            anchorItem['plateform'] = u"熊猫"
            anchorItem['reward'] = float(room_host['bamboos'])/1000
            # yield anchorItem
            yield scrapy.Request(room_url, dont_filter=True, callback=self.get_room_info, meta={'anchorItem': anchorItem})
            # yield scrapy.Request(url=room_url, callback=self.parse_room_detail, meta={"item": item}, dont_filter=True)

        next_url = url[:url.rfind('=') + 1] + str(int(url[url.rfind('=') + 1:]) + 1)

        yield scrapy.Request(url=next_url,
                             callback=self.parse, dont_filter=True)

    # 获取主播头像
    def get_room_info(self, response):
        # print baseurl
        myPgae = response.body
        unicodePage = myPgae.decode('utf-8')
        avatar = re.findall(r'"avatar":"(.*?)","bamboos"', unicodePage, re.S)  # 获取当前页面的Table
        anchorItem = response.meta['anchorItem']
        anchorItem['avatar'] = str(avatar[0])
        # print anchorItem
        yield anchorItem



    # 提取出房间的信息，并拼接出各项API
    def parse_room_detail(self, response):
        item = response.meta['item']

        room_detail = replace_html_marker(get_room_detail_json(response.text)['details']).replace("\xa0", "").strip()
        room_detail = room_detail.replace("&gt;", ">").replace("&lt;", "<")

        itemLoader = PandaItemLoader(item=item, response=response)

        itemLoader.add_value("room_detail", room_detail)

        item = itemLoader.load_item()

        yield item
