# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import time,re,urllib2
t=time.time()
websiteurls={}
def scanpage(url):
  websiteurl=url
  t=time.time()
  n=0
  html=urllib2.urlopen(websiteurl).read()
  soup=BeautifulSoup(html)
  pageurls=[]
  Upageurls={}
  pageurls=soup.find_all("a",href=True)
  for links in pageurls:
    if websiteurl in links.get("href") and links.get("href") not in Upageurls and links.get("href") not in websiteurls:
      Upageurls[links.get("href")]=0
  for links in Upageurls.keys():
    try:
      urllib2.urlopen(links).getcode()
    except:
      print "connect failed"
    else:
      t2=time.time()
      Upageurls[links]=urllib2.urlopen(links).getcode()
      print n,
      print links,
      print Upageurls[links]
      t1=time.time()
      print t1-t2
    n+=1
  print ("total is "+repr(n)+" links")
  print time.time()-t
scanpage("http://news.163.com/")