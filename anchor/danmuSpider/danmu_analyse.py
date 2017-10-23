# -*- coding: utf-8 -*-  
# 抓取弹幕后保存为text文档，然后词云分析,此部分是词云部分

import jieba
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import os,sys
import PIL.Image as Image
import numpy as np


def getWorldCloud(filename):
    # with open('大司马即将上课前后.txt','r',encoding='utf-8') as f:
    with open(filename+'.txt','r') as f:
        text = f.read()
        f.close()
    cut_text = " ".join(jieba.cut(text))  #使用空格连接 进行中文分词
    d = os.path.dirname(__file__) # 获取当前文件路径
    color_mask = np.array(Image.open(os.path.join(d,'img.jpg')))   # 设置图片
    cloud = WordCloud(
        background_color='#F0F8FF',      # 参数为设置背景颜色,默认颜色则为黑色
        font_path="FZLTKHK--GBK1-0.ttf", # 使用指定字体可以显示中文，或者修改wordcloud.py文件字体设置并且放入相应字体文件
        max_words=1000,  # 词云显示的最大词数
        font_step=10,    # 步调太大，显示的词语就少了
        mask=color_mask,  #设置背景图片
        random_state= 15, # 设置有多少种随机生成状态，即有多少种配色方案
        min_font_size=15,  #字体最小值
        max_font_size=232, #字体最大值
        )
    cloud.generate(cut_text)  #对分词后的文本生成词云
    image_colors = ImageColorGenerator(color_mask)  # 从背景图片生成颜色值
    plt.show(cloud.recolor(color_func=image_colors))  # 绘制时用背景图片做为颜色的图片
    plt.imshow(cloud)            # 以图片的形式显示词云
    plt.axis('off')                     # 关闭坐标轴
    plt.show()                          # 展示图片
    cloud.to_file(os.path.join(d, filename+"-3"+'.jpg'))  # 图片大小将会按照 mask 保存
    print("generate filename.jpg:",filename);

if __name__ == "__main__":
    args=sys.argv
    print(args)
    # filename="douyuChat592227.txt"
    # filename="douyuChat4809"
    # filenames = ['douyuChat4809','douyuChat56040','douyuChat71017','douyuChat85981']
    # filenames = ['douyuDanmu4809','douyuDanmu10903','douyuDanmu1229','douyuDanmu138243','douyuDanmu138286','douyuDanmu56040','douyuDanmu67373','douyuDanmu688','douyuDanmu71017','douyuDanmu7911','douyuDanmu93912','douyuDanmu96291']
    # filenames = ['pandaDanmu1102322','pandaDanmu18000','pandaDanmu371037']
    filenames = ['douyuDanmu673327','pandaDanmu371037']
    # if(len(args)==2):
    #     filename=args[1]
    # print("生成 filename.jpg:",filename);
    for filename in filenames:
        getWorldCloud(filename);