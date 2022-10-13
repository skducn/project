# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: 抖音视频下载（单个，多个（获取抖音视频用户列表进行批量下载））
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# 参数哈 click（）， 参考：https://blog.csdn.net/weixin_33506900/article/details/112187887
#***************************************************************

import requests, re, os, platform
import click
import sys
sys.path.append("../../")
# from PO.DataPO import *
# Data_PO = DataPO()
from PO.FilePO import *
File_PO = FilePO()
from PO.HtmlPO import *
Html_PO = HtmlPO()
from PO.StrPO import *
Str_PO = StrPO()


headers = Html_PO.getHeaders()
proxies = Html_PO.getProxies()


@click.command()
@click.option("-u", "--url", help='url地址')
def getVidoeByPhone(url, toSave="d:\\2"):
	'''
	1，单视频下载（手机版）
	:param copyURL:
	:param toSave:
	:return:
		# 参数：用户页链接 - 分享 - 复制链接
	'''


	# 解析复制链接及API地址并获取视频ID
	res = Html_PO.sessionGet(url, headers, proxies)
	# print(res.url)
	aweme_id = re.findall(r'video/(\w+-\w+-\w+|\w+-\w+|\w+)', res.url)  # ['6976835684271279400']
	apiUrl = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + aweme_id[0]
	res = Html_PO.sessionGet(apiUrl, headers, proxies)
	res = (str(res.text).encode('gbk', 'ignore').decode('gbk'))
	tmp = json.loads(res)
	# print(tmp)

	if tmp['item_list'] == [] and tmp['filter_list'][0]['notice'] == "抱歉，作品不见了":
		# print(tmp['filter_list'][0]['detail_msg'])   # 因作品权限或已被删除，无法观看，去看看其他作品吧
		noVid = (tmp['filter_list'][0]['notice'])  # 抱歉，作品不见了
		print(url + " " + noVid)
	else:

		# 获取视频Id
		# vid = tmp['item_list'][0]['video']['vid']  # v0200fg10000ca0rof3c77u9aib3u93g

		# 视频Id
		# video_id = re.findall(r'/?video_id=(\w+)', res1.text)  #  # v0300f3d0000bvn9r1prh6u8gbdusbdg
		# 用户名
		nickname = re.findall('"nickname":"(.+?)"', res)
		# 视频标题
		varTitle = re.findall('"share_title":"(.+?)"', res)
		# 优化文件名不支持的9个字符
		varTitle = Str_PO.delSpecialChar(str(varTitle[0]))
		# 生成目录
		if platform.system() == 'Darwin':
			File_PO.newLayerFolder(toSave + "/" + nickname[0])
			varFolder = str(toSave) + "/" + nickname[0]
		if platform.system() == 'Windows':
			File_PO.newLayerFolder(toSave + "\\" + nickname[0])
			varFolder = str(toSave) + "\\" + nickname[0]
		# 下载（API地址）
		videoUrl = tmp['item_list'][0]['video']['play_addr']['url_list'][0]  # v0200fg10000ca0rof3c77u9aib3u93g
		# videoUrl = "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=" + str(vid)

		ir = Html_PO.sessionGet(videoUrl, headers, proxies)
		open(f'{toSave}/{nickname[0]}/{varTitle}.mp4', 'wb').write(ir.content)

		# 输出结果
		l_result = []
		l_result.append(varFolder)
		# l_result.append((str(varTitle).encode("utf-8").decode("utf-8")))
		l_result.append(varTitle)
		l_result.append(videoUrl)
		# print(l_result)
		print(str(l_result).encode('gbk', 'ignore').decode('gbk'))



print("1，单视频下载（手机版）".center(100, "-"))
getVidoeByPhone()  # 单个抖音链接

# cmd 命令：python dy2.py -u https://v.douyin.com/2c6fEbw/



