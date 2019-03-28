# -*- coding: utf-8 -*-
import jieba
from wordcloud import WordCloud,ImageColorGenerator
from random import randint


def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    h = randint(0, 140)
    s = int(140.0 * 255.0 / 255.0)
    l = int(100.0 * float(randint(190, 240)) / 255.0)
    return "hsl({}, {}%, {}%)".format(h, s, l)


def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'rb').readlines()]
    return stopwords


def CloudCreat(text,path,PicWidth,PicHeight):
    if(PicWidth<10):
        PicWidth=235
    if(PicHeight<10):
        PicHeight=237
    #读取标点符号库
    stopwords=stopwordslist(path+"\\Words\\stopwords.txt")
    #加载用户自定义词典
    jieba.load_userdict(path+"\\Words\\mywords.txt")
    segs=jieba.cut(text)
    mytext_list=[]	
	
    #文本清洗
    for seg in segs:
        if seg.encode() not in stopwords and seg!=" " and len(seg)!=1:
            mytext_list.append(seg.replace(" ",""))
    cloud_text=",".join(mytext_list)
    if(cloud_text.isdigit()):
        cloud_text="None"
    elif(cloud_text.isspace()):
        cloud_text = "None"
    elif(cloud_text==''):
        cloud_text = "None"

    wc = WordCloud(
        background_color=None,  # 背景颜色
        max_words=60,  # 显示最大词数
        font_path="C:\\Windows\\Fonts\\simkai.ttf",  # 使用字体
        mode='RGBA',
        min_font_size=18,
        max_font_size=42,
        width=PicWidth , # 图幅宽度
        height=PicHeight
    )
    wc.generate(cloud_text)
    wc.recolor(color_func=random_color_func)
    wc.to_file(path+"/Words/pic.png")

