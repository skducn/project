# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: 抖音视频下载（手机端，Web端，支持单个视频、视频列表批量下载）
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# 手机版单视频页、列表页 https://v.douyin.com/Jp4GEo6/
# 网页版单视频页 https://www.douyin.com/discover
# 网页版列表页 https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg  全说商业

# 过滤掉非法的多字节序列问题
# b = "型➕换季收纳法🔥叠衣"
# print(b.encode('gbk', 'ignore').decode('gbk') )   # 型换季收纳法叠衣
#***************************************************************

import requests, re, os, platform, bs4, json, sys
from urllib import parse
# sys.path.append("../../../")
sys.path.append("/Users/linghuchong/Downloads/51/Python/project/")

from PO.DataPO import *
Data_PO = DataPO()

from PO.FilePO import *
File_PO = FilePO()

from PO.HttpPO import *
Http_PO = HttpPO()

from PO.StrPO import *
Str_PO = StrPO()

from PO.WebPO import *
Web_PO = WebPO("chrome")

class DyPO:

	def getVideo(self, surl, toPath):

		header = {
			"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"}

		# 解析获取id
		share = re.search(r'/v.douyin.com/(.*?)/', surl).group(1)
		share_url = "https://v.douyin.com/{}/".format(share)
		# print(share_url)  # https://v.douyin.com/SrL7RnM/
		s_html = requests.get(url=share_url, headers=header)
		surl = s_html.url
		# print(surl) # https://www.douyin.com/video/7206155470149635384
		if len(surl) > 60:
			id = re.search(r'video/(\d.*)/', surl).group(1)
		else:
			id = re.search(r'video/(\d.*)', surl).group(1)
		# print(id) # 7206155470149635384


		# 获取json数据
		u_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?item_ids={}&a_bogus=".format(id)
		v_rs = requests.get(url=u_id, headers=header).json()
		# print(0,v_rs)

		# 作者名
		nickname = v_rs['item_list'][0]['author']['nickname']
		# print(1,nickname)

		# 视频标题
		titles = v_rs['item_list'][0]['desc']
		# print(3, v_rs['item_list'][0]['desc'])
		# titles = re.search(r'^(.*?)[；;。.#]', v_rs['item_list'][0]['desc'])
		# titles = re.search(r'^(.*?)[；;。.#]', v_rs['item_list'][0]['desc']).group(1)
		# if titles == None:
		# 	titles = nickname
		# else:
		# 	titles = v_rs['item_list'][0]['desc']
		# 	titles = re.search(r'^(.*?)[；;。.#]', v_rs['item_list'][0]['desc']).group(1)
		# print(titles)

		# 创建video文件夹
		if not os.path.exists(toPath + nickname):
			os.makedirs(toPath + nickname)

		# 获取uri参数
		req = v_rs['item_list'][0]['video']['play_addr']['uri']
		# print("vvvvvv", req)

		# 下载无水印视频
		v_url = "https://www.douyin.com/aweme/v1/play/?video_id={}".format(req)
		v_req = requests.get(url=v_url, headers=header).content
		print(f"[下载中] => {v_url}")

		# 写入文件
		with open(f'{toPath}{nickname}/{titles}.mp4', 'wb') as f:
			f.write(v_req)

		print(f'[已完成] => {toPath}{nickname}/{titles}.mp4')
		return toPath + nickname



if __name__ == '__main__':

	Dy_PO = DyPO()

	folder = Dy_PO.getVideo("https://v.douyin.com/iR49gsDg/", "/Users/linghuchong/Downloads/video/douyin/")
	os.system("open " + folder)

