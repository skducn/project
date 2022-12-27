# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-12-27
# Description: bilibili下载
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# json在线解析 https://www.sojson.com/
# js在线解密 https://www.sojson.com/jsjiemi.html
# https://www.bilibili.com/read/cv16789932/
#***************************************************************


import requests

import json

import subprocess

import os

from bs4 import BeautifulSoup



def getUrl(url):

    print('地址解析中')

    bvideoHTML = requests.get(url)

    values = bvideoHTML.text

    text = BeautifulSoup(values, features='lxml')

    title = text.find('title').contents[0].replace(' ',',').replace('/',',')

    items = text.find_all('script')[2]

    items = items.contents[0].replace('window.__playinfo__=', '')

    obj = json.loads(items)

    videoUrl = obj["data"]["dash"]["video"][0]["baseUrl"]

    audioUrl = obj["data"]["dash"]["audio"][0]["baseUrl"]

    print('地址解析完成')

    return (videoUrl, audioUrl, title)





def getvideoAndAudio(url):

    print('开始发送请求')

    #https://www.bilibili.com/video/BV1cU4y1m7c9?spm_id_from=333.1007.extension.content.click

    Url = getUrl(url)

    videoUrl = Url[0]

    audioUrl = Url[1]

    title = Url[2]

    os.mkdir(f'./{title}')

    headers = {


    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',

    # 'Range': 'bytes=0-29609553',

    'Referer': url

    }

    print('请求成功返回')

    print('开始下载视频，音频文件')

    print(f'./{title}/video.mp4')

    with open(f'./{title}/video.mp4', 'wb') as video:

        video.write(requests.get(videoUrl, headers=headers).content)

    with open(f'./{title}/audio.mp3', 'wb') as audio:

        audio.write(requests.get(audioUrl, headers=headers).content)



    print('下载完毕')

    return (f'./{title}/video.mp4',f'./{title}/audio.mp3',title)



def video_add_mp4(url):

    print('开始合出音频视频')

    file = getvideoAndAudio(url)

    mp4_file = file[0]

    file_name = file[1]

    title = file[2]

    print(title)

    cmd = f'ffmpeg -i {mp4_file} -i {file_name} -acodec copy -vcodec copy ./{title}/{title}.mp4'

    subprocess.call(cmd,shell=True)

    print('合成完毕')

    os.remove(mp4_file)

    os.remove(file_name)

    print('正在删除临时文件')







video_add_mp4("https://www.bilibili.com/video/BV1VP4y197si/?spm_id_from=333.788.recommend_more_video.0")

