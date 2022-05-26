# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-1-4
# Description: 下载腾讯视频(非vip)
#***************************************************************

import re
import os,shutil
import requests,threading
from urllib.request import urlretrieve
from pyquery import PyQuery as pq
from multiprocessing import Pool
import random
import time
import requests, re, os
import jsonpath
from time import sleep

#
class video_down():

    def __init__(self, url):
        session = requests.session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
        sec_respone = session.get(url="http://vv.video.qq.com/getinfo?vids=" + url + "&platform=101001&charge=0&otype=json", headers=self.headers)
        print(sec_respone.text)

        fn = re.findall('"fn":"(.+?)"', sec_respone.text)
        # print("fn：%s" % fn[0])

        fvkey = re.findall('"fvkey":"(.+?)"', sec_respone.text)
        # print("fvkey：%s" % fvkey[0])

        url3 = re.findall('"url":"(.+?)"', sec_respone.text)
        # print("url3：%s" % url3[-1])

        downURL = url3[-1] + fn[0] + "?fvkey=" + fvkey[0]
        print(downURL)


if __name__ == '__main__':

    v = video_down("q0035hvwowd")

    #电影目标url：狄仁杰之四大天王
    # url='https://v.qq.com/x/cover/r6ri9qkcu66dna8.html'
#     # ["x0027oqrq20", "o0030i760lp", "t0030kxu4lv", "k0030ek22hk", "o0030cmw34o", "m0780ds6f42", "i07367x9do4",
#     #  "f07252jefce", "g07426brd7g", "a0739m9r4rn", "w074487otra", "m0737sygu6f", "y07359kt80w", "h07406k0nwm",
#     #  "n0734rbwciv", "y073321aeqe", "b0735xxvtqf", "s0728s5zzd1", "f0711g224s1", "w0734id0oyc", "w0724itdqej",
#     #  "h07230iz1ug", "z0726lkdiqg", "b0720m6iwai", "f0718aiuft6", "e0712a5hpi0", "w06979zdu7s", "a0705zanx7r",
#     #  "h0637zx1wc8", "x0692tlysax", "r0663ocag8m", "b0552p30m20"]
#     # #电影碟中谍5：神秘国度
#     # url1='https://v.qq.com/x/cover/5c58griiqftvq00.html'
#     # #电视剧斗破苍穹
#     # url2='https://v.qq.com/x/cover/lcpwn26degwm7t3/z0027injhcq.html'
#     # url3='https://v.qq.com/x/cover/33bfp8mmgakf0gi.html'


# def qq_vedio(vid):
#     headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
#     appver = '3.2.19.333'
#     # try:
#     #     vid = url.split("/")[-1].split(".")[0]
#     # except:
#     #     vid = url
#     #     print(vid)
#     url = "http://vv.video.qq.com/getinfo?otype=json@platform=11&defnpayver=1&appver=" + appver + "&defn=fhd&vid=" + vid
#     html = requests.get(url,headers=headers)
#     html_text = html.text
#     print(html.text)
#
# qq_vedio("y0029h6miip")