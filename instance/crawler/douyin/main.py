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

# 0.25 02/24 O@k.pD odn:/ # 股票 # 短线交易 # 成交量 # 股民交流 # 上证指数 跳空高开，分时图，预判主力的预判  https://v.douyin.com/iFyomEfY/ 复制此链接，打开Dou音搜索，直接观看视频！

# print("1，下载单个抖音视频".center(100, "-"))
# folder = Dy_PO.getVideo("https://v.douyin.com/SrL7RnM/", "/Users/linghuchong/Downloads/video/douyin/")
folder = Dy_PO.getVideo2("https://www.douyin.com/video/7316708968867401014", "/Users/linghuchong/Downloads/video/douyin/")
os.system("open " + folder)

# 4.66 ZzG:/ 12/30 W@m.QX （上）人类和机器共生时代的到来：特斯拉机器人的领先地位 特斯拉机器人展示了自然的动作，通过先进的技术和触觉感知实现了人类般的操作。优化的设计使其更灵活、精准，具备更大的自由度。# 看视频学英语 # 英语听力 # 英语听力训练  https://v.douyin.com/iFfLR75B/ 复制此链接，打开Dou音搜索，直接观看视频！
# folder = Dy_PO.downVideo("https://v.douyin.com/SrL7RnM/", "d:/11/44")
# os.system("start " + folder)

# 7.61 i@P.kp jca:/ 10/11 学习英语短语“伟大的户外活动”和“竭尽全力”（双语版） # 英语 # 英语口语 # 英语启蒙 # 英语学习 # 英语听力  https://v.douyin.com/iLPh1Lt4/ 复制此链接，打开Dou音搜索，直接观看视频！


# print("2，下载多个抖音(列表页)视频".center(100, "-"))
# if platform.system() == "Windows":
#     Dy_PO.downVidoeList("https://www.douyin.com/user/MS4wLjABAAAAOkdsWDIgI7EB8qug52evYguETk729ADZ10MgAQMfysY?vid=7181707656808221964", "d:/11/6")  # 下载所有视频
    # Dy_PO.downVidoeList("https://www.douyin.com/user/MS4wLjABAAAAOkdsWDIgI7EB8qug52evYguETk729ADZ10MgAQMfysY?vid=7181707656808221964", "d:/11/6", "a", "7181702424485186849")  # 下载 7181702424485186849 之后视频（即最新）
    # Dy_PO.downVidoeList("https://www.douyin.com/user/MS4wLjABAAAAOkdsWDIgI7EB8qug52evYguETk729ADZ10MgAQMfysY?vid=7181707656808221964", "d:/11/6", "b", "7041494252559420685")  # 下载 7041494252559420685 之前视频（即最旧）
# elif platform.system() == "Darwin":
    # Dy_PO.downVidoeList("https://www.douyin.com/user/MS4wLjABAAAAOkdsWDIgI7EB8qug52evYguETk729ADZ10MgAQMfysY?vid=7181707656808221964", "/Users/linghuchong/Downloads/video/douyin")  # 下载所有视频
    # Dy_PO.downVidoeList("https://www.douyin.com/user/MS4wLjABAAAAOkdsWDIgI7EB8qug52evYguETk729ADZ10MgAQMfysY?vid=7181707656808221964", "/Users/linghuchong/Downloads/video/douyin", "a", "7181702424485186849")  # 下载 7181702424485186849 之后视频（即最新）
    # Dy_PO.downVidoeList("https://www.douyin.com/user/MS4wLjABAAAAOkdsWDIgI7EB8qug52evYguETk729ADZ10MgAQMfysY?vid=7181707656808221964", "/Users/linghuchong/Downloads/video/douyin", "b", "7041494252559420685")  # 下载 7041494252559420685 之前视频（即最旧）


