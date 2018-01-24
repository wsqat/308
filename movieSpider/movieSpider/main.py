# -*- coding: utf-8 -*-

from scrapy import cmdline

cmdline.execute("scrapy crawl nuomimovie".split())
# 获取榜单电影的票房以及用户画像
# cmdline.execute("scrapy crawl dict".split())
# cmdline.execute("scrapy crawl piaofang".split())
# getMovieDict
# cmdline.execute("scrapy crawl dict".split())
# getMoviePiaoFang and getMovieDataJson
# cmdline.execute("scrapy crawl baidu".split())
# cmdline.execute("scrapy crawl baidu -o items.json -t json".split())