# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import jieba, datetime, os
import jieba.analyse
# import xlwt #写入Excel表的库
import threading
from time import ctime, sleep


def wordCount(fname, newname):
    # def wordCount(oldpath,newpath):
    # wbk = xlwt.Workbook(encoding = 'ascii')
    # sheet = wbk.add_sheet("wordCount")#Excel单元格名字
    print "I was at the %s! %s" % (fname, ctime())
    word_lst = []
    key_list = []
    for line in open(fname):  # 1.txt是需要分词统计的文档
        item = line.strip('\n\r').split('\t')  # 制表格切分
        # print item
        jieba.analyse.set_stop_words('stopword.txt')
        tags = jieba.analyse.extract_tags(item[0], 20)  # jieba分词
        for t in tags:
            word_lst.append(t)
    word_dict = {}
    with open(newname, 'w') as wf2:  # 打开文件
        for item in word_lst:
            if item not in word_dict:  # 统计数量
                word_dict[item] = 1
            else:
                word_dict[item] += 1
        orderList = list(word_dict.values())
        orderList.sort(reverse=True)
        # print orderList
        for i in range(len(orderList)):
            for key in word_dict:
                if word_dict[key] == orderList[i]:
                    wf2.write(key + ' ' + str(word_dict[key]) + '\n')  # 写入txt文档
                    key_list.append(key)
                    word_dict[key] = 0

# 扫描指定文件目录下所有文件
def getFileNames(folder):
    path = os.getcwd() + "/" + folder
    # 获取到当前文件的目录，并检查是否有report文件夹，如果不存在则自动新建report文件
    files = os.listdir(path)
    s = []
    for file in files:
        if not os.path.isdir(file):  # 不是文件夹才打开
            # f = open(path+"/"+file)
            if 'wc.txt' not in file:
                s.append(file[:-4])
    return s

# 封装wc方法
def startMulitThread():
    # folder = datetime.datetime.now().strftime('%Y-%m-%d')
    folder = "comments"
    filenames = getFileNames(folder)
    # filenames = ['panda_6666']
    threads = []
    for filename in filenames:
        print filename
        # newname = filename + "_wc.txt"
        # fname = filename + ".txt"
        oldpath = os.getcwd() + "/" + folder + "/" + filename + ".txt"
        newpath = os.getcwd() + "/" + folder + "/" + filename + "_wc.txt"
        t1 = threading.Thread(target=wordCount, args=(oldpath, newpath))
        threads.append(t1)

    for t in threads:
        print t
        # t.setDaemon(True)  #setDaemon(True)将线程声明为守护线程，必须在start() 方法调用之前设置，如果不设置为守护线程程序会被无限挂起。子线程启动后，父线程也继续执行下去，当父线程执行完最后一条语句print "all over %s" %ctime()后，没有等待子线程，直接就退出了，同时子线程也一同结束。
        t.start()

    t.join()  # join()方法的位置是在for循环外的，也就是说必须等待for循环里的两个进程都结束后，才去执行主进程。

    print "all over %s" % ctime()