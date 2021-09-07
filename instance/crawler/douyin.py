# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: 抖音视频下载（手机端，Web端，支持单个视频、视频列表批量下载
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# https://www.douyin.com/
# 手机版单视频页、列表页 https://v.douyin.com/Jp4GEo6/
# 网页版单视频页 https://www.douyin.com/video/6979549164304731428
# 网页版列表页 https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg
#***************************************************************

import requests, re, os, platform
import sys
sys.path.append("../../")
from bs4 import BeautifulSoup

from PO.DataPO import *
Data_PO = DataPO()

from PO.FilePO import *
File_PO = FilePO()

from PO.HtmlPO import *
Html_PO = HtmlPO()

from PO.StrPO import *
Str_PO = StrPO()


class Douyin:

	def __init__(self):
		# 初始化代理
		Html_PO.getHeadersProxies()

	# 1，单视频下载（手机版）
	def downSingle(self, copyURL, toSave):
		# 参数：用户页链接 - 分享 - 复制链接

		# 解析复制链接及API地址并获取视频ID
		res = Html_PO.sessionGet(copyURL)
		# print(res.url)  # https://www.douyin.com/video/6976835684271279400?previous_page=app_code_link
		videoId = re.findall(r'video/(\w+-\w+-\w+|\w+-\w+|\w+)', res.url)  # ['6976835684271279400']
		url1 = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + videoId[0]
		res1 = Html_PO.sessionGet(url1)

		# 视频Id
		video_id = re.findall(r'/?video_id=(\w+)', res1.text)  #  # v0300f3d0000bvn9r1prh6u8gbdusbdg
		# 用户名
		nickname = re.findall('"nickname":"(.+?)"', res1.text)
		# 视频标题
		varTitle = re.findall('"share_title":"(.+?)"', res1.text)
		# 优化文件名不支持的9个字符
		varTitle = Str_PO.nonsupportChar(str(varTitle[0]))
		# 生成目录
		File_PO.newLayerFolder(toSave + "\\" + nickname[0])
		varFolder = str(toSave) + "\\" + nickname[0]
		# 下载（API地址）
		videoURL = "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=" + video_id[0] + "&ratio=720p&line=0"
		ir = Html_PO.sessionGet(videoURL)
		open(f'{toSave}/{nickname[0]}/{varTitle}.mp4', 'wb').write(ir.content)

		# 输出结果
		l_result = []
		l_result.append(varFolder)
		l_result.append(varTitle)
		l_result.append(videoURL)
		print(l_result)


	# 2，多视频下载（手机版）
	def downRange(self, copyURL, toSave, scope="all"):
		# 参数1：用户列表页链接：右上角... - 分享 - 复制链接
		# 参数3：scope 表示从第几视频开始下载  如：100表示从第100个开始下载，之前视频忽略。

		# 解析复制链接及API地址并获取视频ID 获取sec_uid
		res = Html_PO.sessionGet(copyURL)
		seu_udi = re.findall(r'sec_uid=(\w+-\w+-\w+|\w+-\w+|\w+)', res.url)   # ['MS4wLjABAAAA641dgYSbDRfR9YDDe3ve46BGVqE0doMTy0uDK10CYBw']
		sum_url = 'https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={0}'.format(seu_udi[0])  # https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=MS4wLjABAAAA641dgYSbDRfR9YDDe3ve46BGVqE0doMTy0uDK10CYBw
		se = Html_PO.sessionGet(sum_url)

		# 用户名
		nickname = re.findall('"nickname":"(.+?)"', se.text)
		print("用户名：%s" % nickname[0])
		# 视频数
		sm_count = re.findall('"aweme_count":(\w+)', se.text)
		print("视频数：%s" % sm_count[0])
		count = sm_count[0]
		# # 抖音号
		# unique_id = re.findall('"unique_id":"(.+?)"', se.text)
		# print("抖音号：%s" % unique_id[0])
		# # 粉丝量
		# fensi = re.findall('"follower_count":(\w+)', se.text)
		# print("粉丝数量：%s" % fensi[0])
		# # 关注量
		# guanzhu = re.findall('"following_count":(\w+)', se.text)
		# print("关注：%s" % guanzhu[0])

		# 生成目录
		File_PO.newLayerFolder(toSave + "\\" + nickname[0])
		varFolder = str(toSave) + "\\" + nickname[0]

		# 分页功能
		max_cursor = 0
		while True:
			while True:
				if (max_cursor == 0):
					sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=21&max_cursor=0&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(seu_udi[0])
				else:
					sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=21&max_cursor={1}&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(seu_udi[0], max_cursor)
				comment = Html_PO.getJson(sec_id_url)
				if (len(comment['aweme_list']) == 0):
					os._exit(0)
				else:
					# 下一页最大下标
					max_cursor = comment['max_cursor']
					for s in comment['aweme_list']:

						# 视频标题
						varTitle = s['desc']

						# 优化文件名不支持的9个字符
						varTitle = Str_PO.nonsupportChar(str(varTitle))

						# 过滤掉#后的广告
						varTitle = re.sub("(\#\w+)|(\@\w+)", '', varTitle)
						# print(varTitle)

						# 视频地址(过滤v5-开头的视频)
						videoURL = s['video']['play_addr_lowbr']['url_list'][0]
						if "http://v5-" in videoURL:
							videoURL = s['video']['play_addr_lowbr']['url_list'][1]

						# # 点赞数
						# dianzan = s['statistics']["digg_count"]
						# # 评论数
						# pinglun = s['statistics']["comment_count"]
						# # 分享数
						# fenxiang = s['statistics']["share_count"]

						# 下载
						if isinstance(scope, int):
							# 下载从序号《3》之前的音频
							if scope >= int(count):
								# 优化文件名不支持的9个字符
								varTitle = str(count) + "_" + varTitle
								ir = Html_PO.sessionGet(videoURL)
								open(f'{toSave}/{nickname[0]}/{varTitle}.mp4', 'wb').write(ir.content)
								# 输出结果
								l_result = []
								l_result.append(varFolder)
								l_result.append(varTitle)
								l_result.append(videoURL)
								print(l_result)
								l_result = []
						if isinstance(scope, str):
							# 下载所有视频
							if scope == "all":
								varTitle = str(count) + "_" + varTitle
								ir = Html_PO.sessionGet(videoURL)
								open(f'{toSave}/{nickname[0]}/{varTitle}.mp4', 'wb').write(ir.content)
								# 输出结果
								l_result = []
								l_result.append(varFolder)
								l_result.append(varTitle)
								l_result.append(videoURL)
								print(l_result)
								l_result = []
							# 下载标题中带关键字的音频
							elif scope in varTitle:
								varTitle = str(count) + "_" + varTitle
								ir = Html_PO.sessionGet(videoURL)
								open(f'{toSave}/{nickname[0]}/{varTitle}.mp4', 'wb').write(ir.content)
								# 输出结果
								l_result = []
								l_result.append(varFolder)
								l_result.append(varTitle)
								l_result.append(videoURL)
								print(l_result)
								l_result = []
						count = int(count) - 1
					break



	# 3，单视频下载（网页版）
	def downSingelWeb(self, videoId, toSave):
		# 参数1：https://www.douyin.com/video/6974964160962530591 地址最后 videoId

		# API解析地址
		url1 = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + videoId
		res1 = Html_PO.sessionGet(url1)

		# 视频Id
		video_id = re.findall(r'/?video_id=(\w+)', res1.text)  # v0300f3d0000bvn9r1prh6u8gbdusbdg
		# 用户名
		nickname = re.findall('"nickname":"(.+?)"', res1.text)
		# 视频标题
		varTitle = re.findall('"share_title":"(.+?)"', res1.text)  # 视频标题
		# 优化文件名不支持的9个字符
		varTitle = Str_PO.nonsupportChar(str(varTitle[0]))
		# 生成目录
		File_PO.newLayerFolder(toSave + "\\" + nickname[0])
		varFolder = str(toSave) + "\\" + nickname[0]
		# 下载（API地址）
		videoURL = "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=" + video_id[0] + "&ratio=720p&line=0"
		ir = Html_PO.sessionGet(videoURL)
		open(f'{toSave}/{nickname[0]}/{varTitle}.mp4', 'wb').write(ir.content)

		# 输出结果
		l_result = []
		l_result.append(varFolder)
		l_result.append(varTitle)
		l_result.append(videoURL)
		print(l_result)


	# 4，多视频下载（网页版）
	def downRangeWeb(self, sec_id, toSave,scope="all"):
		# 参数1：https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg 地址最后的 sec_id
		# 参数3：从指定位置往后开始下载
		# 参数4：按名字中关键字进行下载

		# 获取网页作品数
		url = 'https://www.douyin.com/user/' + sec_id
		html = requests.get(url)
		html.encoding = 'utf-8'
		text = html.text
		bsop = BeautifulSoup(text, 'html.parser')
		for i in bsop.select('span[class="_03811320ee25b81d1c705fae532572ec-scss"]'):
			# print(i.get_text())
			workQTY = i.get_text()
			break


		# 输出信息
		sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=50&max_cursor=0&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(sec_id)
		comment = Html_PO.getJson(sec_id_url)
		for s in comment['aweme_list']:
			# 用户名
			nickname = s['author']['nickname']
			# 生成目录
			File_PO.newLayerFolder(toSave + "\\" + nickname)
			varFolder = str(toSave) + "\\" + nickname
			print("用户名：{}({})".format(nickname, url))
			print("视频数：{}".format(workQTY))
			break

		max_cursor = 0

		# 分页功能
		while True:
			while True:
				if (max_cursor == 0):
					sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=50&max_cursor=0&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(sec_id)
				else:
					sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=50&max_cursor={1}&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(sec_id, max_cursor)
				comment = Html_PO.getJson(sec_id_url)
				if (len(comment['aweme_list']) == 0):
					os._exit(0)
				else:
					# 下一页最大下标
					max_cursor = comment['max_cursor']

					for s in comment['aweme_list']:

						# 视频标题
						varTitle = s['desc']

						# 优化文件名不支持的9个字符
						varTitle = Str_PO.nonsupportChar(str(varTitle))

						# 过滤掉#后的广告
						# varTitle = re.sub("(\#\w+)|(\@\w+)", '', varTitle)

						# 视频地址(过滤v5-开头的视频)
						videoURL = s['video']['play_addr_lowbr']['url_list'][0]
						if "http://v5-" in videoURL:
							videoURL = s['video']['play_addr_lowbr']['url_list'][1]

						# 下载
						if isinstance(scope, int):
							# 下载从序号《3》之前的音频
							if scope >= int(workQTY):
								# 优化文件名不支持的9个字符
								varTitle = str(workQTY) + "_" + varTitle
								ir = Html_PO.sessionGet(videoURL)
								open(f'{toSave}/{nickname}/{varTitle}.mp4', 'wb').write(ir.content)
								# 输出结果
								l_result = []
								l_result.append(varFolder)
								l_result.append(varTitle)
								l_result.append(videoURL)
								print(l_result)
								l_result = []
						if isinstance(scope, str):
							# 下载所有视频
							if scope == "all":
								varTitle = str(workQTY) + "_" + varTitle
								ir = Html_PO.sessionGet(videoURL)
								open(f'{toSave}/{nickname}/{varTitle}.mp4', 'wb').write(ir.content)
								# 输出结果
								l_result = []
								l_result.append(varFolder)
								l_result.append(varTitle)
								l_result.append(videoURL)
								print(l_result)
								l_result = []
							# 下载标题中带关键字的音频
							elif scope in varTitle:
								varTitle = str(workQTY) + "_" + varTitle
								ir = Html_PO.sessionGet(videoURL)
								open(f'{toSave}/{nickname}/{varTitle}.mp4', 'wb').write(ir.content)
								# 输出结果
								l_result = []
								l_result.append(varFolder)
								l_result.append(varTitle)
								l_result.append(videoURL)
								print(l_result)
								l_result = []
						workQTY = int(workQTY) - 1
					break

if __name__ == '__main__':

	douyin = Douyin()

	# 1，单视频下载（手机版）
	douyin.downSingle("https://v.douyin.com/d6x4QLT/", "d:\\600")


	# 2，多视频下载（手机版）
	# douyin.downRange("https://v.douyin.com/Jp4GEo6/", "d:\\4")  # 下载所有视频，走遍中国5A景区-大龙
	# douyin.downRange("https://v.douyin.com/Jp4GEo6/", "d:\\4", 3)  # 下载从序号《3》之前的音频
	# douyin.downRange("https://v.douyin.com/Jp4GEo6/", "d:\\4", scope="三星")  # 下载标题中带“XXX”关键字的音频


	# 3，单视频下载（网页版）
	# douyin.downSingelWeb("6974964160962530591", "d:\\4")



	# 4，多视频下载（网页版）
	# "https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg"
	# douyin.downRangeWeb("MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg", "d:\\3")  # 下载所有视频
	# douyin.downRangeWeb("MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg", "d:\\3", 5)  # 下载从序号《5》之前的音频
	# douyin.downRangeWeb("MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg", "d:\\3", scope="中国")  # 下载标题中带“XXX”关键字的音频
