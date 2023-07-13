# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-12-27
# Description: xvideos ，解析html.txt中的视频链接
# 安装 lxml 需要查看python版本， https://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
# html5player.setVideoHLS('https://cdn77-vid.xvideos-cdn.com/RQ8awptsSFkElOGWOsXYsw==,1689224214/videos/hls/7b/d4/d4/7bd4d4b0c1d23afeed2f450edebfcc7f/hls.m3u8');
# setUploaderName('chicken1806')
# html5player.setVideoTitle('腿玩年系列！抱起黑丝长腿长驱直入，白嫩小穴清晰可见「看片头视频可以约她！」')
#***************************************************************

from XvideosPO import *
Xvideos_PO = XvideosPO()
import sys, smtplib, os, base64, requests, urllib, json, jsonpath, logging, time

# Xvideos_PO.html2url("html.txt", 'xvideo.txt')

Xvideos_PO.getVideoUrl("https://cdn77-vid.xvideos-cdn.com/RQ8awptsSFkElOGWOsXYsw==,1689224214/videos/hls/7b/d4/d4/7bd4d4b0c1d23afeed2f450edebfcc7f/",
                       'chicken1806',
                       '腿玩年系列！抱起黑丝长腿长驱直入，白嫩小穴清晰可见「看片头视频可以约她！」'
                       )



# import subprocess
#
# infile = 'ttt1.ts'
# outfile = 'video.mp4'
#
# subprocess.run(['ffmpeg', '-i', infile, outfile])

# os.system('cat *.ts? > ttt1.ts')

# os.system("open xvideo.txt")