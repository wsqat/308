# -*- coding: utf-8 -*-
import random, base64

# 使用IP代理池 =>  proxy抓取ip，然后过滤出有效ip
class ProxyMiddleware(object):
    proxyList = [ \
        '111.13.7.42:82', '183.62.11.242:8088', '111.13.7.42:80', '117.90.6.127:9000'
    ]

    def process_request(self, request, spider):
        # Set the location of the proxy
        pro_adr = random.choice(self.proxyList)
        print("USE PROXY -> " + pro_adr)
        request.meta['proxy'] = "http://" + pro_adr