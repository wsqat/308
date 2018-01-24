# fetch_baidu_index

目的：本项目主要是用来抓取百度指数的值。因为百度指数为了防止抓取，将数字转成了图片。

# 运行步骤:
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
