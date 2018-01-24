# -*- coding: utf-8 -*-

from scrapy import cmdline
import wordCount as wc
from threading import Timer
import threading
import os
from time import sleep

def main():
    # 生成影评文件
    cmdline.execute("scrapy crawl comments".split())

def wc_start():
    # 影评分词
    wc.startMulitThread()


if __name__ == '__main__':
    # 创建子进程之前声明的变量
    try:
        pid = os.fork()
        if pid == 0:  # 子进程
            print "this is child process. exe main()"
            main()
        else:  # 父进程
            sleep(20)
            print "this is parent process. exe wc()"
            wc_start()
    except OSError, e:
        pass