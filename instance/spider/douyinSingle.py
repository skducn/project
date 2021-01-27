# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: 下载单个抖音视频
# # user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
#***************************************************************


import requests, re, os
from time import sleep



def downloadSingleVideo(url):
	session = requests.session()
	headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

	# 解析url
	res = session.get(url=url, headers=headers)
	video = re.findall(r'video/(\w+-\w+-\w+|\w+-\w+|\w+)', res.url)   # 如：video_id=6912637146767674636

	# 解析url1
	url1 = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + video[0]
	res1 = requests.get(url=url1, headers=headers)
	# print(res1.text)
	video_id = re.findall(r'/?video_id=(\w+)', res1.text)   # 如：video_id=v0300f3d0000bvn9r1prh6u8gbdusbdg
	nickname = re.findall('"share_title":"(.+?)"', res1.text)  # 视频标题

	# 视频文件优化，自动去除特殊符合，如?
	if "?" in str(nickname[0]):
		nickname = str(nickname[0]).replace("?", "")

	# 下载目录
	print("下载保存路径：d:\\%s.mp4" % nickname[0])

	# 下载
	ir = session.get("https://aweme.snssdk.com/aweme/v1/playwm/?video_id=" + video_id[0] +"&ratio=720p&line=0", headers=headers)
	open(f'd:/{nickname}.mp4', 'wb').write(ir.content)
	# open(f'/Users/linghuchong/Downloads/{nickname}.mp4', 'wb').write(ir.content)
	# test


if __name__ == '__main__':

	downloadSingleVideo("https://v.douyin.com/JcF6mYb/")
