# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-12-27
# Description: 抖音视频下载 for cmd
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# json在线解析 https://www.sojson.com/
# js在线解密 https://www.sojson.com/jsjiemi.html
# Python爬虫：用requests、json、bs4等模块轻轻松松抓取抖音视频的下载链接 https://zhuanlan.zhihu.com/p/442884562
# Python解码JS的encodeURIComponent并转化JSON https://blog.csdn.net/jeff06143132/article/details/124919764
# 使用方法：
# cd /Users/linghuchong/miniconda3/envs/py310/bin
# python /Users/linghuchong/Downloads/51/Python/project/instance/crawler/douyin/mainCMD.py 'https://v.douyin.com/SsReryQ/'
#***************************************************************

from DyPO import *
Dy_PO = DyPO()

import sys
query = sys.argv[1]
# print(query)
# query = "https://v.douyin.com/SrL7RnM/"  或  https://www.douyin.com/video/7157633339661307168

# if platform.system() == "Windows":
#     folder = Dy_PO.downVideo(query, "d:/11/44")
#     os.system("start " + folder)


if platform.system() == "Darwin":
    folder = Dy_PO.getVideo(query, "/Users/linghuchong/Downloads/video/douyin/")
    f = folder.replace(" ", "\\ ")
    # print(f)
    os.system("open " + f)
