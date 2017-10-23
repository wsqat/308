# -*- coding: utf-8 -*-

from danmu_panda import PandaTvDanmakuClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

panda = PandaTvDanmakuClient()
queue = panda.subscribe(10300)
panda.run()
try:
    while 1:
        data = queue.get()
        print(data)
except KeyboardInterrupt:
    pass
finally:
        panda.close()