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
# python /Users/linghuchong/Downloads/51/Python/project/instance/crawler/pornhub/cmd.py 'https://cn.pornhub.com/view_video.php?viewkey=ph63bddd2130'
# ph https://cn.pornhub.com/view_video.php?viewkey=ph63bddd2130
#***************************************************************

from PornhubPO import *
Pornhub_PO = PornhubPO()

import sys
query1 = sys.argv[1]
query2 = sys.argv[2]
Pornhub_PO.downloadOneOver(query1, query2)
