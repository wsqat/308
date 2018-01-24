# -*- coding: utf-8 -*-

from scrapy import cmdline
from threading import Timer  
from datetime import datetime, timedelta
from time import sleep  
import sort as st
import os

SECONDS_PER_DAY = 24 * 60 * 60  
  
def run_crawlall( enter_time ):  
    cmdline.execute("scrapy crawlall".split())
    print "now is "+str(datetime.now()) + "run_crawlall time is " + str(enter_time)

# 规定某个时候执行此函数
# def doFirst():
    # curTime = datetime.now()
    # print curTime
    # # 当前执行时间
    # desTime = curTime.replace(year=2017,month=12,day=27,hour=20, minute=43, second=30, microsecond=0)
    # print desTime
    # delta = desTime-curTime
    # sleeptime = delta.total_seconds()
    # print "Now day must sleep "+str(sleeptime)+ " seconds"
    # sleep(sleeptime)
    # run_crawlall(datetime.now())

if __name__ == "__main__":
    # 爬去小说数据
    # doFirst()
    # run_crawlall(datetime.now())

    try:
        pid = os.fork()
        if pid == 0:  # 子进程
            # run_crawlall(datetime.now())
            print "this is child process start."
            ppid = os.fork()
            if ppid == 0:
                pppid = os.fork()
                if pppid == 0:
                    print "this is child process. run qqdushu"
                    cmdline.execute("scrapy crawl qqdushu".split())
                else:
                    print "this is child process. run qidianmm"
                    cmdline.execute("scrapy crawl qidianmm".split())
            else:
                ppppid = os.fork()
                if ppppid == 0:
                    print "this is child process. run qidia"
                    cmdline.execute("scrapy crawl qidian".split())
                else:
                    print "this is child process. run xxsy"
                    cmdline.execute("scrapy crawl xxsy".split())
            # sleep(10)
            print "this is child process end."
        else:  # 父进程
            # sleep(60)
            # 排序，生成榜单
            print "this is parent process start."
            ppid1 = os.fork()
            if ppid1 == 0:
                pppid2 = os.fork()
                if pppid2 == 0:
                    print "this is child process. run zongheng"
                    cmdline.execute("scrapy crawl zongheng".split())
                else:
                    print "this is child process. run chuangshi"
                    cmdline.execute("scrapy crawl chuangshi".split())
            else:
                ppppid3 = os.fork()
                if ppppid3 == 0:
                    print "this is child process. run seventeen"
                    cmdline.execute("scrapy crawl seventeen".split())
                else:
                    sleep(128) #sleep(40000) 抓取所有页面
                    st.main()
                    print "this is parent process. exe st()"
            print "this is parent process end."
    except OSError, e:
        pass