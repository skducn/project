# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: 抖音视频下载（手机端，Web端，支持单个视频、视频列表批量下载
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# https://www.douyin.com/
#***************************************************************

import requests, re, os, platform
from PO.DataPO import *
Data_PO = DataPO()


# 1，手机版抖音视频下载（单个）
def getOne(copyURL, toSave):

	session = requests.session()
	proxies = {"url": Data_PO.getIpAgent()}
	headers = {'User-Agent': Data_PO.getUserAgent()}

	# 解析复制链接及API地址并获取视频ID
	res = session.get(url=copyURL, headers=headers, proxies=proxies)
	# print(res.url)  # https://www.douyin.com/video/6976835684271279400?previous_page=app_code_link
	videoId = re.findall(r'video/(\w+-\w+-\w+|\w+-\w+|\w+)', res.url)
	# print(videoId)  # ['6976835684271279400']
	url1 = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + videoId[0]
	res1 = requests.get(url=url1, headers=headers)
	video_id = re.findall(r'/?video_id=(\w+)', res1.text)
	# print(video_id)  # v0300f3d0000bvn9r1prh6u8gbdusbdg

	# 视频标题
	varTitle = re.findall('"share_title":"(.+?)"', res1.text)  # 视频标题
	# 视频文件优化，自动去除特殊符合，如?
	if "?" in str(varTitle[0]):
		varTitle = str(varTitle[0]).replace("?", "")

	# 视频下载（API地址）
	videoURL = "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=" + video_id[0] + "&ratio=720p&line=0"
	# 如果toSave指定的目录不存在，则自动创建目录
	if not os.path.exists(toSave):
		os.mkdir(toSave)
	ir = session.get(videoURL, headers=headers)
	open(f'{toSave}/{varTitle}.mp4', 'wb').write(ir.content)
	print(str(toSave) + "\%s.mp4 (%s)" % (varTitle[0], videoURL))

# 2，手机端抖音列表视频下载（批量）
def getList(copyURL, toSave, varFromNumDown=0, keyword=""):

	# varFromNumDown 表示从第几视频开始下载  如：100表示从第100个开始下载，之前视频忽略。
	session = requests.session()
	proxies = {"url": Data_PO.getIpAgent()}
	headers = {'User-Agent': Data_PO.getUserAgent()}
	sum_url = ""
	max_cursor = 0
	id = 0

	# 解析复制链接及API地址并获取视频ID 获取sec_uid
	res = session.get(url=copyURL, headers=headers, proxies=proxies)
	seu_udi = re.findall(r'sec_uid=(\w+-\w+-\w+|\w+-\w+|\w+)', res.url)
	# print(seu_udi)  # ['MS4wLjABAAAA641dgYSbDRfR9YDDe3ve46BGVqE0doMTy0uDK10CYBw']
	sum_url = 'https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={0}'.format(seu_udi[0])
	# print(sum_url)  # https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=MS4wLjABAAAA641dgYSbDRfR9YDDe3ve46BGVqE0doMTy0uDK10CYBw
	se = session.get(sum_url)

	# 获取用户名、抖音号、视频数、粉丝、关注
	# 用户名
	nickname = re.findall('"nickname":"(.+?)"', se.text)
	print("用户名：%s" % nickname[0])

	# 抖音号
	unique_id = re.findall('"unique_id":"(.+?)"', se.text)
	print("抖音号：%s" % unique_id[0])

	# 视频数
	sm_count = re.findall('"aweme_count":(\w+)', se.text)
	print("视频数：%s" % sm_count[0])

	# 粉丝量
	fensi = re.findall('"follower_count":(\w+)', se.text)
	print("粉丝数量：%s" % fensi[0])

	# 关注量
	guanzhu = re.findall('"following_count":(\w+)', se.text)
	print("关注：%s" % guanzhu[0])


	# 分页功能
	while True:
		while True:
			if (max_cursor == 0):
				sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=21&max_cursor=0&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(seu_udi[0])
			else:
				sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=21&max_cursor={1}&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(seu_udi[0], max_cursor)
			sec_respone = session.get(url=sec_id_url, headers=headers)
			comment = sec_respone.json()

			if (len(comment['aweme_list']) == 0):
				os._exit(0)
			else:
				# 下一页最大下标
				max_cursor = comment['max_cursor']
				for s in comment['aweme_list']:
					id += 1

					# 视频标题
					varTitle = s['desc']
					# 视频标题中非法字符处理，如 ?
					if "?" in str(varTitle):
						varTitle = str(varTitle).replace("?", "")
					# 过滤掉#后的广告
					varTitle = re.sub("(\#\w+)|(\@\w+)", '', varTitle)
					# print(varTitle)

					# 视频地址
					videoURL = s['video']['play_addr_lowbr']['url_list'][0]
					if "http://v5-" in videoURL:
						videoURL = s['video']['play_addr_lowbr']['url_list'][1]

					# # 点赞数
					# dianzan = s['statistics']["digg_count"]
					# # 评论数
					# pinglun = s['statistics']["comment_count"]
					# # 分享数
					# fenxiang = s['statistics']["share_count"]

					# 视频下载
					if id >= int(varFromNumDown):
						# 如果toSave指定的目录不存在，则自动创建目录
						if not os.path.exists(toSave + "//" + nickname[0]):
							os.mkdir(toSave + "//" + nickname[0])

						# 搜索标题中的关键字
						if keyword != "":
							if keyword in varTitle:
								ir = session.get(videoURL, headers=headers)
								open(f'{toSave}/{nickname[0]}/{varTitle}.mp4', 'wb').write(ir.content)
								print(str(id) + ", " + str(toSave) + "\\" + str(nickname[0]) + "\%s.mp4 (%s)" % (varTitle, str(videoURL)))
						else:
							ir = session.get(videoURL, headers=headers)
							open(f'{toSave}/{nickname[0]}/{varTitle}.mp4', 'wb').write(ir.content)
							print(str(id) + ", " + str(toSave) + "\\" + str(nickname[0]) + "\%s.mp4 (%s)" % (varTitle, str(videoURL)))
							# print(str(id) + "、视频名称为：{0},点赞数为:{1},评论数为:{2},分享数量为:{3},视频无水印地址为：{4}".format(text, str(dianzan), str(pinglun),str(fenxiang), video_url))

					else:
						print(str(id) + "，{0}".format(varTitle))
				break


# 3，网页版抖音视频下载（单个）
def getOneFromWeb(videoId, toSave):

	session = requests.session()
	proxies = {"url": Data_PO.getIpAgent()}
	headers = {'User-Agent': Data_PO.getUserAgent()}

	# API解析地址
	url1 = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + videoId
	res1 = requests.get(url=url1, headers=headers, proxies=proxies)
	video_id = re.findall(r'/?video_id=(\w+)', res1.text)
	# print(video_id)  # v0300f3d0000bvn9r1prh6u8gbdusbdg

	# 视频标题
	varTitle = re.findall('"share_title":"(.+?)"', res1.text)  # 视频标题
	# 视频文件优化，自动去除特殊符合，如?
	if "?" in str(varTitle[0]):
		varTitle = str(varTitle[0]).replace("?", "")

	# 视频下载（API地址）
	videoURL = "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=" + video_id[0] + "&ratio=720p&line=0"
	ir = session.get(videoURL, headers=headers)
	open(f'{toSave}/{varTitle}.mp4', 'wb').write(ir.content)
	print(str(toSave) + "\%s.mp4 (%s)" % (varTitle[0], videoURL))

# 4，网页版抖音列表视频下载（批量）
def getListFromWeb(sec_id, toSave,varFromNumDown=0, keyword=""):
	# 参数3：从指定位置往后开始下载
	# 参数4：按名字中关键字进行下载
	session = requests.session()
	proxies = {"url": Data_PO.getIpAgent()}
	headers = {'User-Agent': Data_PO.getUserAgent()}
	max_cursor = 0
	id = 0

	# 分页功能
	while True:
		while True:
			if (max_cursor == 0):
				sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=50&max_cursor=0&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(sec_id)
			else:
				sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=50&max_cursor={1}&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(sec_id, max_cursor)
			sec_respone = session.get(url=sec_id_url, headers=headers, proxies=proxies)
			comment = sec_respone.json()
			if (len(comment['aweme_list']) == 0):
				os._exit(0)
			else:
				# 下一页最大下标
				max_cursor = comment['max_cursor']
				for s in comment['aweme_list']:
					id += 1

					# 用户名
					nickname = s['author']['nickname']

					# 视频标题
					varTitle = s['desc']
					# 视频标题中非法字符处理，如 ?
					if "?" in str(varTitle):
						varTitle = str(varTitle).replace("?", "")
					# 过滤掉#后的广告
					varTitle = re.sub("(\#\w+)|(\@\w+)", '', varTitle)

					# 视频地址
					videoURL = s['video']['play_addr_lowbr']['url_list'][0]
					if "http://v5-" in videoURL:
						videoURL = s['video']['play_addr_lowbr']['url_list'][1]

					# 视频下载
					if id >= int(varFromNumDown):
						# 如果toSave指定的目录不存在，则自动创建目录
						if not os.path.exists(toSave + "//" + nickname):
							os.mkdir(toSave + "//" + nickname)

						# 搜索标题中的关键字
						if keyword != "":
							if keyword in varTitle:
								ir = session.get(videoURL, headers=headers)
								open(f'{toSave}/{nickname}/{varTitle}.mp4', 'wb').write(ir.content)
								print(str(id) + ", " + str(toSave) + "\\" + str(nickname) + "\%s.mp4 (%s)" % (varTitle, str(videoURL)))
						else:
							ir = session.get(videoURL, headers=headers)
							open(f'{toSave}/{nickname}/{varTitle}.mp4', 'wb').write(ir.content)
							print(str(id) + ", " + str(toSave) + "\\" + str(nickname) + "\%s.mp4 (%s)" % (varTitle, str(videoURL)))
					else:
						print(str(id) + "，{0}".format(varTitle))
				break



if __name__ == '__main__':

	# 1，手机版抖音视频下载（单个）
	# 参数1：用户页链接 - 分享 - 复制链接
	# getOne(" https://v.douyin.com/eXmTAdU/", "d:\\11")
	# getOne(" https://v.douyin.com/eXmTAdU/", "/Users/linghuchong/Downloads/")


	# 2，手机端抖音列表视频下载（批量）
	# 参数1：用户列表页链接：右上角... - 分享 - 复制链接
	# getList("https://v.douyin.com/Jp4GEo6/", "d:\\4")  # 走遍中国5A景区-大龙
	# getList("https://v.douyin.com/Jp4GEo6/", "d:\\4", 10)
	# getList("https://v.douyin.com/Jp4GEo6/", "d:\\4", keyword="节日快乐")
	# getList("https://v.douyin.com/Jp4GEo6/", "/Users/linghuchong/Downloads/")  # 走遍中国5A景区-大龙 抖音列表


	# 3，网页版抖音视频下载（单个）
	# 参数1：https://www.douyin.com/video/6974964160962530591 地址最后 videoId
	# getOneFromWeb("6974964160962530591", "d:\\3")\
	# getOneFromWeb("6974964160962530591", "/Users/linghuchong/Downloads/")


	# 4，网页版抖音列表视频下载（批量）
	# 参数1：https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg 地址最后的 sec_id
	getListFromWeb("MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg", "d:\\3")
	# getListFromWeb("MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg", "d:\\3", 10)
	# getListFromWeb("MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg", "d:\\3", keyword="看美国")
	# getListFromWeb("MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg", "/Users/linghuchong/Downloads/")