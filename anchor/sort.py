# -*- coding: utf-8 -*-
import csv
import pandas as pd
import numpy as np
import sys
reload(sys)
# sys.setdefaultencoding('utf-8')
sys.setdefaultencoding('utf_8_sig')

# df = pd.read_csv('douyu3.old.csv',header=0,usecols=[0,1,2,3,4])
df = pd.read_csv('douyu3.bak.csv',header=0,usecols=[0,1,2,3,4])
# df.iloc[:,[0,1]]
# print df.head()
#cols = df.columns
#print cols
# 热门主播排行榜，
lc=pd.DataFrame(df)
# lc=lc.drop_duplicates(['roomUrl'])
lc = lc[lc['category']!=u'热血传奇']
# df[(True-df['appID'].isin([278,382]))] 
lc=lc.drop_duplicates(['userName'])
# lc.drop(42927)
# lc = lc.iloc[:,[0,4]]
# new = lc.sort_values(by=['fans'],ascending=False)
# new = new.head(20)
new = lc.sort_values(by=['fans'],ascending=True)
new = new.tail(20)
# print new.shape
# print new.columns
print new

# 热门主播排行榜
import matplotlib.pyplot as plt
present = new.set_index('userName')
present[:20].plot(kind='barh')
plt.title(u'热门主播排行榜', fontsize=16)
plt.xlabel(u'粉丝数', fontsize=16)
plt.ylabel(u'主播', fontsize=16)
plt.show()

