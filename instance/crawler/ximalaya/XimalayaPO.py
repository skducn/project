# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-6-30
# Description: 听喜马拉雅抖音频下载
# https://www.ximalaya.com/
# 获取index，专辑音频总数，页数 https://www.ximalaya.com/revision/album/getTracksList?albumId=13738175&pageNum=1
# 获取src，https://www.ximalaya.com/revision/play/album?albumId=13738175&pageNum=1
# 参考：https://blog.csdn.net/weixin_40873462/article/details/89706555
#******************************************************************************************************************

import sys
sys.path.append("../../../")

from PO.DataPO import *
Data_PO = DataPO()

from PO.FilePO import *
File_PO = FilePO()

from PO.HtmlPO import *
Html_PO = HtmlPO()

from PO.StrPO import *
Str_PO = StrPO()


class XimalayaPO:

	def __init__(self):
		self.headers = Html_PO.getUserAgent()
		self.proxies = Html_PO.getProxies()

	# 1，获取音频列表
	def getAlbumList(self, albumId):

		# 获取专辑音频总数
		cjson = Html_PO.rspGetJson("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum=1".format(albumId))
		# print(cjson)



		if cjson["ret"] != 200 :
			print("[errorrrrrrrrr] albumId不存在！")
			os._exit(0)
		else:
			trackTotalCount = int(cjson["data"]["trackTotalCount"])
			albumTitle = cjson['data']['tracks'][0]['albumTitle']
			# print("专辑名：{}({})".format(albumTitle, "https://www.ximalaya.com/gerenchengzhang/" + str(albumId)))
			# print("音频数：" + str(trackTotalCount))
			if trackTotalCount < 30 or trackTotalCount == 30:
				pageNum = 1
			else:
				if trackTotalCount % 30 == 0 :
					pageNum = trackTotalCount // 30
				else:
					pageNum = trackTotalCount // 30 + 1
			# print("总页数：" + str(pageNum))
			print("听喜马拉雅 => {}({})".format(albumTitle, "https://www.ximalaya.com/gerenchengzhang/" + str(albumId)) + " => " + str(pageNum) + "页 " + str(trackTotalCount) + "个音频\n")

			# 获取 [index, 标题] ，生成列表1
			l_indexTitle = []
			l_tmp = []
			for num in range(1, pageNum + 1):
				cjson = Html_PO.rspGetJson("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum={}".format(albumId, num))
				countByPage = len(cjson['data']['tracks'])
				if countByPage == 30:
					for i in range(30):
						index = cjson['data']['tracks'][i]['index']
						title = cjson['data']['tracks'][i]['title']
						trackId = cjson['data']['tracks'][i]['trackId']

						res = Html_PO.rspGet("https://mobile.ximalaya.com/shortcontent-web/track/subtitle?trackId=" + str(trackId))
						# print(res.text)
						d = json.loads(res.text)
						testASR = d["data"]["subtitlesContent"]

						l_tmp.append(index)
						l_tmp.append(title)
						l_tmp.append(trackId)
						l_tmp.append(testASR)
						l_indexTitle.append(l_tmp)
						l_tmp = []
				else:
					for i in range(countByPage):
						index = cjson['data']['tracks'][i]['index']
						title = cjson['data']['tracks'][i]['title']
						trackId = cjson['data']['tracks'][i]['trackId']
						res = Html_PO.rspGet(
							"https://mobile.ximalaya.com/shortcontent-web/track/subtitle?trackId=" + str(trackId))
						# d = dict(eval(res.text))
						d = json.loads(res.text)
						testASR = d["data"]["subtitlesContent"]
						l_tmp.append(index)
						l_tmp.append(title)
						l_tmp.append(trackId)
						l_tmp.append(testASR)
						l_indexTitle.append(l_tmp)
						l_tmp = []
			# print(l_indexTitle)

			# 获取[标题，地址]，生成列表2
			l_titleSrc = []
			l_tmp = []
			for num in range(1, pageNum + 1):
				cjson = Html_PO.rspGetJson("https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}".format(albumId, num))
				for i in range(cjson['data']['pageSize']):
					try:
						if cjson['data']['tracksAudioPlay'][i]['canPlay'] == True:
							src = cjson['data']['tracksAudioPlay'][i]['src']  # 下载链接
						else:
							src = ""
						trackName = cjson['data']['tracksAudioPlay'][i]['trackName']  # 音频标题
						l_tmp.append(trackName)
						l_tmp.append(src)
						l_titleSrc.append(l_tmp)
						l_tmp = []
					except IndexError:
						break
			# print(l_titleSrc)

			# 两列表合并，输出结果
			for i in range(len(l_indexTitle)):
				if l_indexTitle[i][1] == l_titleSrc[i][0] :
					l_indexTitle[i].append(l_titleSrc[i][1])
			for i in range(len(l_indexTitle)):
				print(l_indexTitle[i])


	# 2，单音频下载
	def getOneAudio(self, albumId, varKeyword, toSave):

		# 获取专辑音频总数
		cjson = Html_PO.rspGetJson("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum=1".format(albumId))
		if cjson["ret"] != 200 :
			print("[errorrrrrrrrr] albumId不存在！")
			os._exit(0)
		else:
			albumTitle = cjson['data']['tracks'][0]['albumTitle']
			# print("专辑名：{}({})".format(albumTitle, "https://www.ximalaya.com/gerenchengzhang/" + str(albumId)))
			trackTotalCount = int(cjson["data"]["trackTotalCount"])
			# print("音频数：" + str(trackTotalCount))
			# print("保存至：{}\{}".format(toSave, albumTitle))


			if trackTotalCount < 30 or trackTotalCount == 30:
				pageNum = 1
			else:
				if trackTotalCount % 30 == 0 :
					pageNum = trackTotalCount // 30
				else:
					pageNum = trackTotalCount // 30 + 1

			# 生成列表1，[index,标题]
			l_indexTitle = []
			l_tmp = []
			for num in range(1, pageNum + 1):
				cjson = Html_PO.rspGetJson("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum={}".format(albumId, num))
				countByPage = len(cjson['data']['tracks'])
				if countByPage == 30:
					for i in range(30):
						index = cjson['data']['tracks'][i]['index']
						title = cjson['data']['tracks'][i]['title']
						l_tmp.append(index)
						l_tmp.append(title)
						l_indexTitle.append(l_tmp)
						l_tmp = []
				else:
					for i in range(countByPage):
						index = cjson['data']['tracks'][i]['index']
						title = cjson['data']['tracks'][i]['title']
						l_tmp.append(index)
						l_tmp.append(title)
						l_indexTitle.append(l_tmp)
						l_tmp = []


			# 生成列表2，[标题，地址]
			l_titleSrc = []
			l_tmp = []
			for num in range(1, pageNum + 1):
				cjson = Html_PO.rspGetJson("https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}".format(albumId, num))
				for i in range(30):
					try:
						if cjson['data']['tracksAudioPlay'][i]['canPlay'] == True:
							src = cjson['data']['tracksAudioPlay'][i]['src']  # 下载链接
						else:
							src = ""
						trackName = cjson['data']['tracksAudioPlay'][i]['trackName']  # 音频标题
						l_tmp.append(trackName)
						l_tmp.append(src)
						l_titleSrc.append(l_tmp)
						l_tmp = []
					except IndexError:
						break

			# 两列表合并，输出结果
			for i in range(len(l_indexTitle)):
				if l_indexTitle[i][1] == l_titleSrc[i][0] :
					l_indexTitle[i].append(l_titleSrc[i][1])


			# 生成目录
			File_PO.newLayerFolder(toSave + "\\" + albumTitle)

			# 下载
			for i in range(len(l_indexTitle)):
				if isinstance(varKeyword, int):
					if l_indexTitle[i][0] == varKeyword :
						if l_indexTitle[i][2] != None:
							ir = Html_PO.rspGet(l_indexTitle[i][2])
							# 优化文件名不支持的9个字符
							varTitle = Str_PO.delSpecialChar(str(l_indexTitle[i][1]))
							varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
							open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)

							l_indexTitle[i].append("{}\{}".format(toSave, albumTitle))
							print(l_indexTitle[i])
						else:
							print("[warning] => 空地址可能是付费音频，无法下载")
						break


	# 3，多视频下载
	def getMoreAudio(self, albumId, toSave, scope="all", keyword="all"):

		# 获取专辑音频总数
		cjson = Html_PO.rspGetJson("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum=1".format(albumId))
		if cjson["ret"] != 200 :
			print("[errorrrrrrrrr] albumId不存在！")
			os._exit(0)
		else:
			albumTitle = cjson['data']['tracks'][0]['albumTitle']
			# print("专辑名：{}({})".format(albumTitle, "https://www.ximalaya.com/gerenchengzhang/" + str(albumId)))
			trackTotalCount = int(cjson["data"]["trackTotalCount"])
			# print("音频数：" + str(trackTotalCount))
			if trackTotalCount < 30 or trackTotalCount == 30:
				pageNum = 1
			else:
				if trackTotalCount % 30 == 0 :
					pageNum = trackTotalCount // 30
				else:
					pageNum = trackTotalCount // 30 + 1
			# print("总页数：" + str(pageNum))
			# print("保存至：{}\{}".format(toSave, albumTitle))

			# 生成列表1，[index,标题]
			l_indexTitle = []
			l_tmp = []
			for num in range(1, pageNum + 1):
				cjson = Html_PO.rspGetJson("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum={}".format(albumId, num))
				countByPage = len(cjson['data']['tracks'])
				if countByPage == 30:
					for i in range(30):
						index = cjson['data']['tracks'][i]['index']
						title = cjson['data']['tracks'][i]['title']
						l_tmp.append(index)
						l_tmp.append(title)
						l_indexTitle.append(l_tmp)
						l_tmp = []
				else:
					for i in range(countByPage):
						index = cjson['data']['tracks'][i]['index']
						title = cjson['data']['tracks'][i]['title']
						l_tmp.append(index)
						l_tmp.append(title)
						l_indexTitle.append(l_tmp)
						l_tmp = []


			# 生成列表2，[标题，地址]
			l_titleSrc = []
			l_tmp = []
			for num in range(1, pageNum + 1):
				cjson = Html_PO.rspGetJson("https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}".format(albumId, num))
				for i in range(30):
					try:
						if cjson['data']['tracksAudioPlay'][i]['canPlay'] == True:
							src = cjson['data']['tracksAudioPlay'][i]['src']  # 下载链接
						else:
							src = ""
							# if str(src) in ("null", "None"):
								# print("此为付费音频，无法下载")
						trackName = cjson['data']['tracksAudioPlay'][i]['trackName']  # 音频标题
						l_tmp.append(trackName)
						l_tmp.append(src)
						l_titleSrc.append(l_tmp)
						l_tmp = []
					except IndexError:
						break

			# 两列表合并，输出结果
			for i in range(len(l_indexTitle)):
				if l_indexTitle[i][1] == l_titleSrc[i][0] :
					l_indexTitle[i].append(l_titleSrc[i][1])
			# print(l_indexTitle)

			# 生成目录
			File_PO.newLayerFolder(toSave + "\\" + albumTitle)

			# 下载
			for i in range(len(l_indexTitle)):
				# keyword如果是整数，判断下载前后音频
				if isinstance(keyword, int):
					# 下载指定序号之前的音频
					if scope == "before":
						if keyword >= l_indexTitle[i][0]:
							ir = Html_PO.rspGet(l_indexTitle[i][2])
							# 优化文件名不支持的9个字符
							varTitle = Str_PO.delSpecialChar(str(l_indexTitle[i][1]))
							varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
							open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)
							l_indexTitle[i].append("{}\{}".format(toSave, albumTitle))
							print(l_indexTitle[i])
					# 下载指定序号之后的音频
					elif scope == "after":
						if keyword <= l_indexTitle[i][0]:
							ir = Html_PO.rspGet(l_indexTitle[i][2])
							# 优化文件名不支持的9个字符
							varTitle = Str_PO.delSpecialChar(str(l_indexTitle[i][1]))
							varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
							open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)
							l_indexTitle[i].append("{}\{}".format(toSave, albumTitle))
							print(l_indexTitle[i])
				# keyword如果是字符串，下载标题中带关键字的音频
				if isinstance(keyword, str):
					# print("1212121")
					# print(l_indexTitle[i][1])
					if keyword in l_indexTitle[i][1]:
						if l_indexTitle[i][2] != None:
							ir = Html_PO.rspGet(l_indexTitle[i][2])
							# 优化文件名不支持的9个字符
							varTitle = Str_PO.delSpecialChar(str(l_indexTitle[i][1]))
							varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
							open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)
							l_indexTitle[i].append("{}\{}".format(toSave, albumTitle))
							print(l_indexTitle[i])
						else:
							print("[warning] => 空地址可能是付费音频，无法下载")
				# 下载所有视频
				if scope == "all":
					ir = Html_PO.rspGet(l_indexTitle[i][2])
					# 优化文件名不支持的9个字符
					varTitle = Str_PO.delSpecialChar(str(l_indexTitle[i][1]))
					varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
					open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)
					l_indexTitle[i].append("{}\{}".format(toSave, albumTitle))
					print(l_indexTitle[i])

	def getTapescriptASR(self, trackId):
		resTrack = Html_PO.rspGet("https://mobile.ximalaya.com/shortcontent-web/track/subtitle?trackId=" + trackId)
		d_resTrack = json.loads(resTrack.text)
		print(d_resTrack["data"]["subtitlesContent"])  # https://fdfs.xmcdn.com/storages/7a1e-audiofreehighqps/2B/78/GKwRIUEHGXcjAAAcXgGu5H4M.txt

		# 解析链接，转换编码
		resTxt = Html_PO.rspGet(d_resTrack["data"]["subtitlesContent"])
		resTxt = resTxt.text.encode('raw_unicode_escape').decode("utf-8")
		# print(list(eval(resTxt)))

		# # 清洗文本
		l = list(eval(resTxt))
		for i in range(len(l)):
			print(l[i]['text'])


if __name__ == '__main__':

	ximalaya_PO = XimalayaPO()


	# 1，获取音频列表
	# ximalaya_PO.getAlbumList("43576130")  # 超级演说家刘媛媛说高效学习法
	ximalaya_PO.getAlbumList("13738175")  # 刘媛媛的晚安电台


	# 2，单音频下载
	# ximalaya_PO.getOneAudio("13738175", 603, "d:\\500")   # 下载序号为604的音频


	# 3，多音频下载
	# ximalaya_PO.getMoreAudio("13738175", "d:\\500")   # 下载所有音频
	# ximalaya_PO.getMoreAudio("13738175", "d:\\500", "before", 3)  # 下载从序号《3》之前的音频
	# ximalaya_PO.getMoreAudio("13738175", "d:\\500", "after", 544)  # 下载从序号《3》之前的音频
	# ximalaya_PO.getMoreAudio("13738175", "d:\\500", keyword="为什么")   # 下载标题中带“为什么”关键字的音频


