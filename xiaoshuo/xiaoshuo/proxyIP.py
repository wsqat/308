#-*-coding:utf-8 -*-
import urllib2
import codecs
from bs4 import  BeautifulSoup

def main():
    User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    header = {}
    header['User-Agent'] = User_Agent

    url = 'http://www.xicidaili.com/nn/1'
    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req).read()

    # soup = BeautifulSoup.BeautifulSoup(res)
    soup = BeautifulSoup(res, "html.parser")
    ips = soup.findAll('tr')
    f = codecs.open("./proxy", "w", 'utf-8')

    for x in range(1, len(ips)):
        ip = ips[x]
        tds = ip.findAll("td")
        ip_temp = tds[1].contents[0] + "\t" + tds[2].contents[0] + "\n"
        f.write(ip_temp)
    f.close()

    import urllib
    import socket
    socket.setdefaulttimeout(3)
    f = open("./proxy")
    fd_proxy = codecs.open("./access.txt", "w", 'utf-8')
    lines = f.readlines()
    proxys = []
    for i in range(0, len(lines)):
        ip = lines[i].strip("\n").split("\t")
        proxy_host = "http://" + ip[0] + ":" + ip[1]
        proxy_temp = {"http": proxy_host}
        proxys.append(proxy_temp)
    url = "http://ip.chinaz.com/getip.aspx"
    for proxy in proxys:
        try:
            res = urllib.urlopen(url, proxies=proxy).read()
            print proxy["http"]
            fd_proxy.write(proxy["http"] + "\n")
            print res
        except Exception, e:
            print proxy
            print e
            continue
    f.close()
    fd_proxy.close()

if __name__ == '__main__':
    main()
