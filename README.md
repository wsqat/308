# Python-crawler
> Some Interesting Crawlers

# 一、IP小说

## xiaoshuo 抓取各大小说网站的数据并生成小说榜单

### 项目介绍
> 抓取如下小说网站，总计约百万条小说数据。采用多进程多线程并发下载技术，运用Scrapy框架，结合代理UserAgent、代理IP等多种反爬虫技术。
1、阅读为主：QQ阅读 103729部作品
2、男频为主：
- 17k小说网   1033171部作品
- 创世中文小说网 192694部作品
- 纵横中文网 33771部作品
- 起点中文网 806700部作品

3、女频为主：
- 潇湘书院 209768部作品
- 起点女生网 19033部作品

> 抓取了相应字段信息如下

| 小说名称 | 作者 |  链接  | 状态 | 字数 | 类别 | 总收藏 | 总点击 | 月点击 |
|:-----|:-----|:----|:-----|:----|:-----|:----|:-----|:----|
|圣墟|辰东| https://book.qidian.com/info/1004608738 | 连载中|324.94万字|玄幻|18662700|17826400|348540|


### 参数修改
1、page_num，修改参数，xiao/xiao/spiders/xxx.py中
```
# print page_num
print u"当前开始爬取起点小说网……"
# for i in range(1, int(page_num)+1): # 取消此注释则默认抓取所以页面
for i in range(1, 3):  # 当前按照总人气抓取前三页
```

2、如果选择抓取所有页面，请务必修改，xiao/xiao/main.py
```
sleep(128) #sleep(40000) 抓取所有页面

```

### 运行命令
> python main.py

### 数据结果，生成相应的榜单数据
- rank
--- 历史收藏排行榜.csv
--- 历史点击排行榜.csv
--- 本月点击排行榜.csv
--- 热门小说作者排行榜.csv

> 历史收藏排行榜.csv
```
开启青少年智慧的150个创意故事,宿春礼 杜延起,http://dushu.qq.com/intro.html?bid=131732,69242340,69242340,1432
择天记,猫腻,http://chuangshi.qq.com/bk/xh/357735.html,21444969,26228376,10136
圣墟,辰东,https://book.qidian.com/info/1004608738,18662700,17826400,348540
斗战狂潮,骷髅精灵,https://book.qidian.com/info/1003694333,17566900,11814500,538888
一念永恒,耳根,https://book.qidian.com/info/1003354631,16463400,16473599,218884
青帝,荆柯守,http://chuangshi.qq.com/bk/xx/227536.html,13845117,8748503,6952
欢乐颂（第二季）,阿耐,http://dushu.qq.com/intro.html?bid=194777,10053762,10053762,11608
欢乐颂第一季,阿耐,http://dushu.qq.com/intro.html?bid=181770,9491891,9491891,2658
联盟之谁与争锋,乱,http://chuangshi.qq.com/bk/yx/216351.html,9049553,15664982,844
大官人,三戒大师,http://chuangshi.qq.com/bk/ls/216350.html,8933812,6126354,2492
不朽凡人,鹅是老五,https://book.qidian.com/info/1003307568,8822600,7284600,11508
余罪,常书欣,http://chuangshi.qq.com/bk/qc/215913.html,8777084,5947523,1996
大明武夫,特别白,http://chuangshi.qq.com/bk/ls/238171.html,8073648,5504148,2692
斗罗大陆III龙王传说,唐家三少,https://book.qidian.com/info/3681560,7872500,8158900,90252
鬼藏人（天黑莫上山，夜半鬼藏人）,李达,http://dushu.qq.com/intro.html?bid=320607,7735018,7735018,42933
冠军之光,林海听涛,http://chuangshi.qq.com/bk/ty/316686.html,7625918,2717430,900
飞剑问道,我吃西红柿,https://book.qidian.com/info/1010468795,7063600,12254200,729616
萌萌山海经,肥面包,http://chuangshi.qq.com/bk/xh/238196.html,6899928,3465290,4064
修真聊天群,圣骑士的传说,https://book.qidian.com/info/3602691,6628700,10674000,157840
俗人回档,庚不让,http://chuangshi.qq.com/bk/ds/321098.html,6282953,2174312,22280
```


# 二、电影

## 1、百度指数 fetch_baidu_index
> 目的：本项目主要是用来抓取百度指数的值。因为百度指数为了防止抓取，将数字转成了图片。

### 运行步骤:
1.修改baidu_index/config.ini要启用的浏览器driver. 具体参考selenium的浏览器环境配置。
  如果没有百度登陆的验证码，理想的情况是使用PhantomJS，毕竟没有浏览器界面。
  考虑到目前每次登陆都要输入验证码的情况，推荐使用chrome浏览器。
  虽然chrome浏览器需要配置驱动，但是感觉比Firefox更稳定靠谱，已经有网友反馈说是Firefox下执行js获取不到PPval值的问题了.

  讨论区里面，jxlwqq这位朋友说用selenium的2.53.6版本，安装firefox 45 版本，并禁止浏览器自动升级。

2.修改baidu_index/config.ini里面的百度账号跟密码

3.修改baidu_index/config.ini中的start_date和end_date，如果不配置可以查询到这个关键词数据的最大区间

4.可自主修改baidu_index/config.ini中的其他配置,
   如: num_of_threads,file_name_encoding,index_type_list,area_list

5.修改task.txt，这是关键词的任务列表，一行一个。

6.执行 python main.py


## 2、豆瓣电影短评 dbmoive 

### 参数设置
> 修改 dbmovie/dbmovie/spiders/comments.py
```
def start_requests(self):
	# “这个杀手不太冷”对应的movieId是1295644，请务必一一对应
    movieIds = [1295644,3287562]  # 设置电影的Id
    movieNames = ["这个杀手不太冷","神偷奶爸"]  # 设置电影名称
    ...
    page = 40 # 设置页码数，自测每部电影大概能抓取3k-4k，故设置页码数 page约为37-40
```
### 运行命令
> python main.py

### 数据结果
- comments
--- 这个杀手不太冷.txt # 抓取的短评
--- 这个杀手不太冷_wc.txt # 短评分词

### 其他的豆瓣相关接口见：
- 数据的接口调用的是豆瓣电影api(官方)，文档地址：https://developers.douban.com/wiki/?title=movie_v2
- 豆瓣电影评论信息接口调用的api(非官方)，github地址：https://github.com/jokermonn/-Api/blob/master/DoubanMovie.md

## 3、糯米电影的用户画像 movieSpider
> 糯米票房网站：piaofang.baidu.com

每次运行代码之前
- 先修改 movieSpider/movieSpider/data/movieTop.txt
- 再运行命令: python main.py
- 结果查看见 movieSpider/movieSpider/data/items_2018-01-21.json 

### 参数设置

> 参数文件，修改 movieSpider/movieSpider/data/movieTop.txt，修改Top电影榜单
```
寻梦环游记
解忧杂货店
无问西东
芳华
星球大战：最后的绝地武士
勇敢者游戏：决战丛林
英雄本色2018
东方快车谋杀案
兄弟，别闹！
前任3：再见前任
```
### 运行命令
> python main.py
> 爬虫文件见 movieSpider/movieSpider/spiders/movieDict.py

### 数据结果
- data
--- dict.json # 所以糯米网站的{"movieName":movieId}的字典文件
--- dict_2018-01-20.json # 运行生成的{"movieName":movieId}的字典文件
--- items_2018-01-20.json
--- items_2018-01-21.json # 运行生成的json格式的的电影榜单的信息 
--- movieTop.txt 修改Top电影榜单

### 参数介绍
- movieName：电影名称
- movieId：电影Id
- boxList：为上映票房数据
- dateList：为上映的时间，与boxList一一对应
- portrait：用户画像，详见“寻梦环游记“的用户画像：https://piaofang.baidu.com/detail/movie?movieId=95322
```
{"boxList": ["619", "8866", "393563", "111735", "613090", "640029", "554965", "594706", "3801748", "3711779", "555659", "1217156", "1242889", "1261770", "1253585", "7525757", "7508419", "1709090", "1464234", "1560296", "1928148", "21060341", "21318211", "13854959", "3051684", "3326477", "3144835", "3164474", "5472918", "20886251", "20117928", "4308284", "6456689", "7084851", "7715820", "8640194", "43765629", "52259676", "17603721", "12902021", "15437551", "16507308", "18519402", "82463241", "104740754", "43352868", "24782232", "28122260", "29928602", "31749132", "113491347", "127635757", "51357841", "25054086", "24018355", "21630649", "20086879", "58348530", "47436740", "12790496", "39286", "12160"], "dateList": ["2018-01-23", "2018-01-22", "2018-01-21", "2018-01-20", "2018-01-19", "2018-01-18", "2018-01-17", "2018-01-16", "2018-01-15", "2018-01-14", "2018-01-13", "2018-01-12", "2018-01-11", "2018-01-10", "2018-01-09", "2018-01-08", "2018-01-07", "2018-01-06", "2018-01-05", "2018-01-04", "2018-01-03", "2018-01-02", "2018-01-01", "2017-12-31", "2017-12-30", "2017-12-29", "2017-12-28", "2017-12-27", "2017-12-26", "2017-12-25", "2017-12-24", "2017-12-23", "2017-12-22", "2017-12-21", "2017-12-20", "2017-12-19", "2017-12-18", "2017-12-17", "2017-12-16", "2017-12-15", "2017-12-14", "2017-12-13", "2017-12-12", "2017-12-11", "2017-12-10", "2017-12-09", "2017-12-08", "2017-12-07", "2017-12-06", "2017-12-05", "2017-12-04", "2017-12-03", "2017-12-02", "2017-12-01", "2017-11-30", "2017-11-29", "2017-11-28", "2017-11-27", "2017-11-26", "2017-11-25", "2017-11-24", "2017-11-23", "2017-11-21"], "movieName": "寻梦环游记", "portrait": {"constellation": [{"proportion": 16, "name": "金牛座", "idx": 3}, {"proportion": 16, "name": "天蝎座", "idx": 9}, {"proportion": 11, "name": "双子座", "idx": 4}, {"proportion": 11, "name": "双鱼座", "idx": 1}, {"proportion": 9, "name": "天秤座", "idx": 8}, {"proportion": 7, "name": "处女座", "idx": 7}, {"proportion": 7, "name": "水瓶座", "idx": 0}, {"proportion": 5, "name": "射手座", "idx": 10}, {"proportion": 5, "name": "白羊座", "idx": 2}, {"proportion": 5, "name": "巨蟹座", "idx": 5}, {"proportion": 5, "name": "狮子座", "idx": 6}, {"proportion": 4, "name": "摩羯座", "idx": 11}], "ageInfo": [{"age": "80后", "proportion": 33, "idx": 1}, {"age": "95后", "proportion": 26, "idx": 4}, {"age": "90后", "proportion": 20, "idx": 3}, {"age": "85后", "proportion": 15, "idx": 2}, {"age": "70后", "proportion": 6, "idx": 0}, {"age": "00后", "proportion": 1, "idx": 5}], "movieId": 95322, "region": [{"province": "江苏", "proportion": 13.6}, {"province": "安徽", "proportion": 9.9}, {"province": "四川", "proportion": 8.6}, {"province": "河北", "proportion": 8.6}, {"province": "福建", "proportion": 7.4}, {"province": "北京", "proportion": 7.4}, {"province": "辽宁", "proportion": 4.9}, {"province": "河南", "proportion": 4.9}, {"province": "天津", "proportion": 3.7}, {"province": "吉林", "proportion": 3.7}, {"province": "山东", "proportion": 3.7}, {"province": "广东", "proportion": 3.7}, {"province": "黑龙江", "proportion": 2.5}, {"province": "湖北", "proportion": 2.5}, {"province": "广西", "proportion": 2.5}, {"province": "甘肃", "proportion": 2.5}, {"province": "山西", "proportion": 2.5}, {"province": "浙江", "proportion": 2.5}, {"province": "内蒙古", "proportion": 1.2}, {"province": "湖南", "proportion": 1.2}, {"province": "云南", "proportion": 1.2}, {"province": "江西", "proportion": 1.2}], "sexInfo": {"male": 40, "female": 60}}}

```

# 三、直播

## proxy 获取IP代理池
scrapy crwal kdlspider #获取免费IP池   
python test_proxy.py   #过滤有效IP池

## zhubo 获取douyu弹幕
python douyu_test.py

## DouyuTV
相关斗鱼的直播房间以及弹幕接口的API

## anchor 主播，虎牙、斗鱼、熊猫
获取各大直播网站的主播信息生成Top主播榜单，以及弹幕数据生成词云
