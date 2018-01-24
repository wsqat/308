# -*- coding: utf-8 -*-
import random, base64
import urllib2
import codecs
from bs4 import  BeautifulSoup

# 使用IP代理池 =>  proxy抓取ip，然后过滤出有效ip
class ProxyMiddleware(object):
# class ProxyMiddleware():
    # [u'183.92.155.130\t80\n', u'218.15.25.153\t808\n', u'117.83.116.109\t8888\n', u'182.35.144.103\t8118\n', u'175.172.168.112\t80\n', u'211.154.132.85\t8888\n', u'116.8.80.197\t8118\n', u'117.36.103.170\t8118\n', u'122.114.31.177\t808\n', u'61.135.217.7\t80\n', u'110.250.2.202\t8118\n', u'139.210.54.32\t8118\n', u'139.199.87.42\t80\n', u'123.54.250.89\t36019\n', u'60.184.118.73\t27633\n', u'113.121.184.10\t45365\n', u'61.154.90.126\t808\n', u'121.31.150.80\t8123\n', u'60.177.224.82\t808\n', u'110.72.34.120\t8123\n', u'221.227.251.244\t26628\n', u'113.128.27.154\t30975\n', u'114.243.67.243\t8118\n', u'27.194.41.223\t8118\n', u'115.217.253.43\t28418\n', u'27.40.128.243\t61234\n', u'106.56.102.40\t808\n', u'171.38.94.214\t8123\n', u'121.31.150.247\t8123\n', u'123.163.165.162\t808\n', u'121.31.154.83\t8123\n', u'222.71.94.167\t43536\n', u'114.230.123.132\t45050\n', u'113.121.243.28\t808\n', u'1.194.145.195\t42983\n', u'115.56.176.180\t8118\n', u'123.161.153.52\t31591\n', u'27.156.149.92\t31434\n', u'171.14.208.153\t22707\n', u'113.128.29.199\t30365\n', u'114.230.127.51\t28736\n', u'116.231.63.104\t8118\n', u'115.203.171.76\t46098\n', u'114.252.165.173\t8118\n', u'113.93.17.225\t27092\n', u'121.31.153.53\t8123\n', u'59.173.211.127\t8118\n', u'112.114.95.236\t8118\n', u'223.241.116.173\t8010\n', u'113.206.153.84\t8118\n', u'180.112.125.201\t8118\n', u'27.213.107.44\t8118\n', u'122.235.238.210\t8118\n', u'27.193.4.54\t8118\n', u'182.90.91.8\t8123\n', u'223.241.119.126\t8010\n', u'110.72.39.213\t8123\n', u'202.103.14.155\t8118\n', u'123.129.4.120\t8118\n', u'27.10.232.26\t8118\n', u'112.255.5.52\t8118\n', u'124.133.72.70\t8118\n', u'49.72.163.84\t8118\n', u'14.20.183.47\t8118\n', u'182.38.104.91\t808\n', u'182.88.253.138\t8123\n', u'139.226.56.38\t8118\n', u'61.143.16.126\t39872\n', u'111.132.193.159\t8118\n', u'119.96.18.121\t8118\n', u'113.124.224.49\t808\n', u'115.58.130.164\t8118\n', u'49.85.7.177\t45781\n', u'117.86.203.160\t24332\n', u'171.11.136.24\t25498\n', u'140.250.152.204\t41582\n', u'180.113.80.171\t47130\n', u'122.4.47.211\t41709\n', u'113.121.240.105\t808\n', u'125.112.194.76\t48202\n', u'110.230.202.117\t8118\n', u'27.152.157.38\t808\n', u'140.250.166.244\t32664\n', u'110.84.176.242\t8118\n', u'113.105.200.19\t3128\n', u'223.241.118.162\t8010\n', u'221.4.133.67\t53281\n', u'219.159.66.222\t808\n', u'115.46.76.156\t8123\n', u'124.126.208.55\t80\n', u'112.81.30.60\t8118\n', u'42.86.165.199\t808\n', u'27.40.135.98\t61234\n', u'123.150.108.211\t8118\n', u'182.108.5.169\t808\n', u'125.106.22.188\t3128\n', u'27.40.148.13\t61234\n', u'60.215.236.173\t8118\n', u'118.114.77.47\t8080\n', u'223.241.78.196\t8010\n']
    totalIpList=[]
    proxyList = [u'http://175.172.168.112:80', u'http://211.154.132.85:8888', u'http://61.154.90.126:808', u'http://60.177.224.82:808', u'http://112.114.95.236:8118', u'http://27.213.107.44:8118', u'http://113.124.224.49:808', u'http://118.114.77.47:8080']

    def getUserfulIp(self):
        User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        header = {}
        header['User-Agent'] = User_Agent
        url = 'http://www.xicidaili.com/nn/1'
        req = urllib2.Request(url, headers=header)
        res = urllib2.urlopen(req).read()

        soup = BeautifulSoup(res, "html.parser")
        ips = soup.findAll('tr')
        for x in range(1, len(ips)):
            ip = ips[x]
            tds = ip.findAll("td")
            ip_temp = tds[1].contents[0] + "\t" + tds[2].contents[0] + "\n"
            self.totalIpList.append(ip_temp)
        print self.totalIpList

        import urllib
        import socket
        # socket.setdefaulttimeout(3)
        socket.setdefaulttimeout(1)
        temp_list = []
        for ip in self.totalIpList:
            ip = ip.split("\t")
            proxy_host = "http://" + ip[0] + ":" + ip[1]
            proxy_temp = {"http": proxy_host}
            temp_list.append(proxy_temp)
        url = "http://ip.chinaz.com/getip.aspx"
        for proxy in temp_list:
            try:
                res = urllib.urlopen(url, proxies=proxy).read()
                # print "proxy"
                proxy_ip = proxy['http'].strip()
                self.proxyList.append(proxy_ip)
                # print res
            except Exception, e:
                # print proxy
                # print e
                continue
        print  self.proxyList

    def process_request(self, request, spider):
        # Set the location of the proxy
        pro_adr = random.choice(self.proxyList)
        print("USE PROXY -> " + pro_adr)
        # request.meta['proxy'] = "http://" + pro_adr
        request.meta['proxy'] = pro_adr


if __name__ == '__main__':
    pro = ProxyMiddleware()
    pro.getUserfulIp()
    # print pro.proxyList
    pro_adr = random.choice(pro.proxyList)
    print pro_adr
