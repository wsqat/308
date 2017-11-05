# -*- coding: utf-8 -*-

from scrapy import cmdline
import time  
from threading import Timer  
from datetime import datetime, timedelta  
from time import sleep  

from functions import writeDanmuFile
# from danmuSpider.main import *
import sys
# from anchor.writeDanmuFile
# sys.path.append("..")
# import danmuSpider.main
  
SECONDS_PER_DAY = 24 * 60 * 60  
  
def run_crawlall( enter_time ):  
    cmdline.execute("scrapy crawlall".split())
    print "now is "+str(datetime.now()) + "run_crawlall time is " + str(enter_time)

def run_anchor( enter_time ):  
    # cmdline.execute("scrapy crawlall".split())
    writeDanmuFile()
    print "now is "+str(datetime.now()) + "run_crawlall time is " + str(enter_time)

# 规定某个时候执行此函数
def doFirst():  
    curTime = datetime.now()
    print curTime
    # 当前执行时间
    desTime = curTime.replace(year=2017,month=11,day=1,hour=18, minute=48, second=31, microsecond=0)  
    print desTime  
    delta = desTime-curTime  
    sleeptime = delta.total_seconds()  
    print "Now day must sleep "+str(sleeptime)+ " seconds"
    sleep(sleeptime)  
    # run_crawlall(datetime.now())  
    run_anchor(datetime.now())

if __name__ == "__main__":  
    doFirst()
