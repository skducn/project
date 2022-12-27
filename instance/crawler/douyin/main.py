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
douyin = DyPO()


douyin.downVideo("https://v.douyin.com/hbjqhuT", "d:\\11")
# douyin.downVideo("https://www.douyin.com/video/7151241259796008222", "d:\\11")





# print("2，多视频下载（手机版）".center(100, "-"))
# douyin.getVidoesByPhone("https://v.douyin.com/Jp4GEo6/", "d:\\4")  # 下载所有视频，走遍中国5A景区-大龙
# douyin.getVidoesByPhone("https://v.douyin.com/Jp4GEo6/", "d:\\4", 3)  # 下载从序号《3》之前的音频
# douyin.getVidoesByPhone("https://v.douyin.com/Jp4GEo6/", "d:\\4", scope="三星")  # 下载标题中带“XXX”关键字的音频



# print("3，单视频下载（网页版）".center(100, "-"))
# douyin.getVidoeByWeb("7050823376893381902", "/Users/linghuchong/Desktop/mac")



# print("4，多视频下载（网页版）".center(100, "-"))
# "https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg"
# douyin.getVidoesByWeb("MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg", "d:\\3")  # 下载所有视频
# douyin.getVidoesByWeb("MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg", "d:\\3", 5)  # 下载从序号《5》之前的音频
# douyin.getVidoesByWeb("MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg", "d:\\3", scope="中国")  # 下载标题中带“XXX”关键字的音频
