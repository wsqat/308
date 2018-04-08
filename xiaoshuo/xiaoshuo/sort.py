# -*- coding: utf-8 -*-
import csv
import pandas as pd
import numpy as np
import os
import sys
reload(sys)
# sys.setdefaultencoding('utf-8')
sys.setdefaultencoding('utf-8')
from datetime import datetime

# 生成cvs文件, 过滤数据, 清洗数据 
# del_cvs_row('20171023.csv', 'rank_click_month_after.csv')
# hotRowNum = 0
def pure_cvs_row(fname, newfname, delimiter=',',key='month'):
    with open(fname,'rU') as csvin, open(newfname, 'w') as csvout:
        reader = csv.reader(csvin, delimiter=delimiter)
        rows = []
        row = ['novel_name','author','novelurl','serialstatus','serialnumber','category','collects','reviews','month']
        rows.append(row)
        writer = csv.writer(csvout, delimiter=delimiter)
        for row in reader:
            row_len = len(row)
            if row_len == 9:
                rows.append(row)
        writer.writerows(rows)
    sort_by_key(newfname,"data/rank_"+key+".csv",key)

# 生成cvs文件 key按照什么排序
def sort_by_key(fname,newfname,key):
    # df = pd.read_csv('novels.csv',header=0,usecols=[0,1,6,7,8])
    # df = pd.read_csv('rank_click_month_after.csv',header=0,usecols=[0,1,6,7,8],low_memory=False)
    df = pd.read_csv(fname,header=0,usecols=[0,1,2,6,7,8],low_memory=False)
    lc = pd.DataFrame(df)
    lc = lc.dropna(axis=0)
    # lc = lc[lc['month']!=u'热血传奇']
    # df[(True-df['appID'].isin([278,382]))] 
    # lc=lc.drop_duplicates(['userName'])
    # print lc.
    # print lc.head(5)
    # print lc.__len__()
    # lc.drop_duplicates([2]) # 默认所有列，无重复记录
    # lc.ix[:, (lc != lc.ix[0]).any()]
    lc = lc.drop_duplicates(['novelurl'])
    # print lc.head(5)
    # print lc.__len__()
    # new = lc.sort_values(by=['month'],ascending=True)
    # new = new.tail(20)
    lc = lc[lc['month']>500]
    if key == 'author':
        # lc = lc.iloc[:,[1,3]]
        lc = lc.groupby(by=['author'])['collects'].sum()
        lc = lc.to_frame()
        new = lc.sort_values(by=['collects'],ascending=False)
        new = new.head(20)
        # print new
        new.to_csv('rank/热门小说作者排行榜.csv', sep=',', encoding='utf-8-sig', header=False)
    else:
        new = lc.sort_values(by=[''+key+''],ascending=False)
        new = new.head(20)
        if key == 'month':
            newfname2 = "rank/本月点击排行榜.csv"
            new.to_csv(newfname2, sep=',', encoding='utf-8-sig', header=False, index=False)
        elif key == 'reviews':
            newfname2 = "rank/历史点击排行榜.csv"
            new.to_csv(newfname2, sep=',', encoding='utf-8-sig', header=False, index=False)
        elif key == 'collects':
            newfname2 = "rank/历史收藏排行榜.csv"
            new.to_csv(newfname2, sep=',', encoding='utf-8-sig', header=False, index=False)
    os.remove(fname)
    # else:
    #    newfname2 = "热门小说作者排行榜.csv"

    # del_cvs_col(newfname, newfname2, [0])

# 生成cvs文件, 删除指定列数
# del_cvs_col('rank_click_month.csv', '本月点击排行榜.csv', [0])
def del_cvs_col(fname, newfname, idxs, delimiter=','):
    with open(fname) as csvin, open(newfname, 'w') as csvout:
        reader = csv.reader(csvin, delimiter=delimiter)
        writer = csv.writer(csvout, delimiter=delimiter)
        rows = (tuple(item for idx, item in enumerate(row) if idx not in idxs) for row in reader)
        writer.writerows(rows)


# 生成cvs文件, 加权处理，增加
# del_cvs_col('rank_click_month.csv', '本月点击排行榜.csv', [0])
# def del_cvs_col(fname, newfname, idxs, delimiter=','):
#     with open(fname) as csvin, open(newfname, 'w') as csvout:
#         reader = csv.reader(csvin, delimiter=delimiter)
#         writer = csv.writer(csvout, delimiter=delimiter)
#         rows = (tuple(item for idx, item in enumerate(row) if idx not in idxs) for row in reader)
#         writer.writerows(rows)

def main():
    # novel_name, author, novelurl, serialstatus, serialnumber, category, collects, reviews, month
    now_date = datetime.now().strftime('%Y-%m-%d')
    filename = "data/" + now_date + ".csv"
    # filename = "20171023.csv"
    # 本月点击排行榜
    pure_cvs_row(filename, 'data/pure_data_month.csv', delimiter=',', key='month')
    # 历史点击排行榜
    pure_cvs_row(filename, 'data/pure_data_reviews.csv', delimiter=',', key='reviews')
    # 热门作者
    pure_cvs_row(filename, 'data/pure_data_author.csv', delimiter=',', key='author')
    # 历史收藏榜
    pure_cvs_row(filename, 'data/pure_data_collects.csv', delimiter=',', key='collects')


if __name__ == '__main__':
    main()

# import matplotlib.pyplot as plt
# plt.rcdefaults()
# present = new.set_index('novel_name')
# present[:20].plot(kind='barh')
# # plt.figure(figsize=(12,9))
# plt.title(u'热门小说本月点击排行榜', fontsize=16)
# plt.xlabel(u'热门小说本月点击量', fontsize=16)
# plt.ylabel(u'热门小说名称', fontsize=16)
# plt.show()

# 历史点击排行榜，
# lc2 = pd.DataFrame(df)
# lc2 = lc2.iloc[:,[0,3]]
# new2 = lc2.sort_values(by=['reviews'],ascending=True)
# new2 = new2.tail(20)
# present = new2.set_index('novel_name')
# present[:20].plot(kind='barh')
# plt.title(u'热门小说历史点击排行榜', fontsize=16)
# plt.xlabel(u'热门小说历史点击量', fontsize=16)
# plt.ylabel(u'热门小说名称', fontsize=16)
# plt.show()

# 历史收藏榜，
# lc3 = pd.DataFrame(df)
# lc3 = lc3.iloc[:,[0,2]]
# new3 = lc3.sort_values(by=['collects'],ascending=True)
# new3 = new3.tail(20)
# present = new3.set_index('novel_name')
# present[:20].plot(kind='barh')
# plt.title(u'热门小说历史收藏榜', fontsize=16)
# plt.xlabel(u'热门小说历史收藏量', fontsize=16)
# plt.ylabel(u'热门小说名称', fontsize=16)
# plt.show()

# 热门作者，
# lc4 = pd.DataFrame(df)
# lc4 = lc4.iloc[:,[1,3]]
# lc4 = lc4.groupby(by=['author'])['reviews'].sum()
# # 生成的数据类型是Series,如果进一步需要将其转换为dataframe,可以调用Series中的to_frame()方法.
# lc4 = lc4.to_frame()
# new4 = lc4.sort_values(by=['reviews'],ascending=False)
# new4 = new4.head(20)
# print new4
# present = new4.set_index('author')
# present[:20].plot(kind='barh')
# plt.title(u'热门小说作者排行榜', fontsize=16)
# plt.xlabel(u'热门小说作者点击量', fontsize=16)
# plt.ylabel(u'热门小说作者', fontsize=16)
# plt.show()

