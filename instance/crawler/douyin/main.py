# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-12-27
# Description: 抖音视频下载
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# json在线解析 https://www.sojson.com/
# js在线解密 https://www.sojson.com/jsjiemi.html
# Python爬虫：用requests、json、bs4等模块轻轻松松抓取抖音视频的下载链接 https://zhuanlan.zhihu.com/p/442884562
# Python解码JS的encodeURIComponent并转化JSON https://blog.csdn.net/jeff06143132/article/details/124919764
#***************************************************************

from DyPO import *
Dy_PO = DyPO()


# print("1，下载单个抖音视频".center(100, "-"))
if platform.system() == "Windows":
    Dy_PO.downVideo("https://v.douyin.com/SrL7RnM/", "d:/11/44")
elif platform.system() == "Darwin":
    Dy_PO.downVideo("https://www.douyin.com/video/7157633339661307168", "/Users/linghuchong/Downloads/video/douyin")



# print("2，下载多个抖音(列表页)视频".center(100, "-"))
# if platform.system() == "Windows":
#     Dy_PO.downVidoeList("https://www.douyin.com/user/MS4wLjABAAAAOkdsWDIgI7EB8qug52evYguETk729ADZ10MgAQMfysY?vid=7181707656808221964", "d:/11/6")  # 下载所有视频
    # Dy_PO.downVidoeList("https://www.douyin.com/user/MS4wLjABAAAAOkdsWDIgI7EB8qug52evYguETk729ADZ10MgAQMfysY?vid=7181707656808221964", "d:/11/6", "a", "7181702424485186849")  # 下载 7181702424485186849 之后视频（即最新）
    # Dy_PO.downVidoeList("https://www.douyin.com/user/MS4wLjABAAAAOkdsWDIgI7EB8qug52evYguETk729ADZ10MgAQMfysY?vid=7181707656808221964", "d:/11/6", "b", "7041494252559420685")  # 下载 7041494252559420685 之前视频（即最旧）
# elif platform.system() == "Darwin":
    # Dy_PO.downVidoeList("https://www.douyin.com/user/MS4wLjABAAAAOkdsWDIgI7EB8qug52evYguETk729ADZ10MgAQMfysY?vid=7181707656808221964", "/Users/linghuchong/Downloads/video/douyin")  # 下载所有视频
    # Dy_PO.downVidoeList("https://www.douyin.com/user/MS4wLjABAAAAOkdsWDIgI7EB8qug52evYguETk729ADZ10MgAQMfysY?vid=7181707656808221964", "/Users/linghuchong/Downloads/video/douyin", "a", "7181702424485186849")  # 下载 7181702424485186849 之后视频（即最新）
    # Dy_PO.downVidoeList("https://www.douyin.com/user/MS4wLjABAAAAOkdsWDIgI7EB8qug52evYguETk729ADZ10MgAQMfysY?vid=7181707656808221964", "/Users/linghuchong/Downloads/video/douyin", "b", "7041494252559420685")  # 下载 7041494252559420685 之前视频（即最旧）


