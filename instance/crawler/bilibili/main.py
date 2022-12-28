# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-12-28
# Description: bilibili视频下载

# 过滤掉非法的多字节序列问题
# b = "型➕换季收纳法🔥叠衣"
# print(b.encode('gbk', 'ignore').decode('gbk') )   # 型换季收纳法叠衣

# json在线解析 https://www.sojson.com/
# js在线解密 https://www.sojson.com/jsjiemi.html
# 5分钟学会用python爬取b站视频 https://www.bilibili.com/read/cv16789932/
#***************************************************************

from BilibiliPO import *
Bilibili_PO = BilibiliPO()


Bilibili_PO.downVideo("https://www.bilibili.com/video/BV1VP4y197si/?spm_id_from=333.788.recommend_more_video.0", "d:/11/22")
# Bilibili_PO.downVideo("https://www.bilibili.com/video/BV1u84y1r7cg/", "d:/11/33")

