# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-7-1
# Description: 爬取 youtube(未测试通过)
#***************************************************************

from __future__ import unicode_literals
import youtube_dl
import time
import os


from pytube import YouTube
url = 'https://www.youtube.com/watch?v=MzG8GrpsrUg'
result = YouTube(url)
print(url + '  ' + result.title)
result.streams.get_by_itag(137).download('/Users/linghuchong/Downloads/test/video')
print('done video')
result.streams.get_by_itag(251).download('/Users/linghuchong/Downloads/test/audio')
print('done audio')

