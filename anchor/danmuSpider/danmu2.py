# -*- coding: utf-8 -*-  
'''
利用第三方模块：danmu
抓取斗鱼弹幕
'''

import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from danmu import DanMuClient

def pp(msg):
    print(msg.encode(sys.stdin.encoding, 'ignore').
        decode(sys.stdin.encoding))

dmc = DanMuClient('https://www.douyu.com/lslalala')
if not dmc.isValid(): print('Url not valid')
else: print ('success')

@dmc.danmu
def danmu_fn(msg):
    pp('[%s] %s' % (msg['NickName'], msg['Content']))
    with open ('data/danmu.txt','a') as f:
      #  f.write('%s [%s] %s \n' % (time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()) ,msg['NickName'], msg['Content'])
		f.write('%s \n' %(msg['Content']))
		
@dmc.gift
def gift_fn(msg):
    pp('[%s] sent a gift!' % content['NickName'])

@dmc.other
def other_fn(msg):
    pp('Other message received')

dmc.start(blockThread = True)