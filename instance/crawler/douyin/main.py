# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: 抖音视频下载（手机端，Web端，支持单个视频、视频列表批量下载
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# https://www.douyin.com/
# 手机版单视频页、列表页 https://v.douyin.com/Jp4GEo6/
# 网页版单视频页 https://www.douyin.com/discover
# 网页版列表页 https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg  全说商业

# 过滤掉非法的多字节序列问题
# b = "型➕换季收纳法🔥叠衣"
# print(b.encode('gbk', 'ignore').decode('gbk') )   # 型换季收纳法叠衣
#***************************************************************

'''
1，单视频下载（手机版）
2，多视频下载（手机版）
3，单视频下载（网页版）
4，多视频下载（网页版）
'''


from DyPO import *
douyin = DyPO()


print("1，单视频下载（手机版）".center(100, "-"))
# douyin.getVidoeByPhone("https://v.douyin.com/6hHBR9K", "d:\\1")
# douyin.getVidoeByPhone("https://v.douyin.com/NHePEyX/", "/Users/linghuchong/Desktop/mac")
douyin.getVidoeByPhone("https://v.douyin.com/2c6fEbw/", "d:\\11")
# douyin.getVidoeByPhone("https://v.douyin.com/NdLh3fT/", "/Users/linghuchong/Desktop/mac")
# douyin.getVidoeByPhone(" https://v.douyin.com/FxTSCxU/", "/Users/linghuchong/Desktop/mac")



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
