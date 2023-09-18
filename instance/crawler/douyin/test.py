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


import json
import re

# 获取视频信息
def get_video_info(video_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        # 使用requests获取视频的网页内容
    content = requests.get(video_url, headers=headers, timeout=10).text
        # 使用正则表达式获取视频信息
    video_info_pattern = re.compile(r'<script.*?>window\.__DATA__ = (.*?)</script>', re.S)
    video_info_match = video_info_pattern.search(content)
    if video_info_match:
        # 将视频信息转化为json格式
        video_info_str = video_info_match.group(1)
        video_info_data = json.loads(video_info_str)
        return video_info_data
    else:
        return None

# 获取视频地址
def get_video_url(video_info_data):
    if video_info_data and 'aweme_detail' in video_info_data.keys():
        aweme_detail = video_info_data['aweme_detail']
        video_play_info = aweme_detail['video_play_info']
        if video_play_info:
            url_list = []
            for item in video_play_info['url_list']:
                url_list.append(item.replace('playwm', 'play'))
            return url_list[0]  # 取不加水印的第一条视频地址即可
    return None

# 获取视频标题
def get_video_title(video_info_data):
    if video_info_data and 'aweme_detail' in video_info_data.keys():
        aweme_detail = video_info_data['aweme_detail']
        return aweme_detail['desc']
    else:
        return None


import requests

html2 = requests.get(ur,headers=headers) #请求json链接


# fo_list'][0]['video']['play_addr']['url_list'][0]
#
# se = requests.get(video_url)
#
# p4', 'wb') as f

# setent)