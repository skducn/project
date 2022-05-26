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

class Ximalaya:

	def __init__(self):
		# 初始化代理
		Html_PO.getHeadersProxies()


	# 1，获取音频列表
	def getAlbumList(self, albumId):

		# 获取专辑音频总数
		cjson = Html_PO.getJson("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum=1".format(albumId))
		if cjson["ret"] != 200 :
			print("[errorrrrrrrrr] albumId不存在！")
			os._exit(0)
		else:
			trackTotalCount = int(cjson["data"]["trackTotalCount"])
			albumTitle = cjson['data']['tracks'][0]['albumTitle']
			print("专辑名：{}".format(albumTitle))
			print("音频数：" + str(trackTotalCount))
			if trackTotalCount < 30 or trackTotalCount == 30:
				pageNum = 1
			else:
				if trackTotalCount % 30 == 0 :
					pageNum = trackTotalCount // 30
				else:
					pageNum = trackTotalCount // 30 + 1
			print("总页数：" + str(pageNum))

			# 生成列表1，[index,标题]
			l_indexTitle = []
			l_tmp = []
			for num in range(1, pageNum + 1):
				cjson = Html_PO.getJson("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum={}".format(albumId, num))
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
				cjson = Html_PO.getJson("https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}".format(albumId, num))
				for i in range(30):
					try:
						trackName = cjson['data']['tracksAudioPlay'][i]['trackName']  # 音频标题
						src = cjson['data']['tracksAudioPlay'][i]['src']  # 下载链接
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
			for i in range(len(l_indexTitle)):
				print(l_indexTitle[i])



	# 2，多音频下载
	def downRange(self, albumId, toSave, scope="all"):

		# 获取专辑音频总数
		cjson = Html_PO.getJson("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum=1".format(albumId))
		if cjson["ret"] != 200 :
			print("[errorrrrrrrrr] albumId不存在！")
			os._exit(0)
		else:
			albumTitle = cjson['data']['tracks'][0]['albumTitle']
			print("专辑名：{}".format(albumTitle))
			trackTotalCount = int(cjson["data"]["trackTotalCount"])
			print("音频数：" + str(trackTotalCount))
			if trackTotalCount < 30 or trackTotalCount == 30:
				pageNum = 1
			else:
				if trackTotalCount % 30 == 0 :
					pageNum = trackTotalCount // 30
				else:
					pageNum = trackTotalCount // 30 + 1
			# print("总页数：" + str(pageNum))
			print("保存至：{}\{}".format(toSave, albumTitle))

			# 生成列表1，[index,标题]
			l_indexTitle = []
			l_tmp = []
			for num in range(1, pageNum + 1):
				cjson = Html_PO.getJson("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum={}".format(albumId, num))
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
				cjson = Html_PO.getJson("https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}".format(albumId, num))
				for i in range(30):
					try:
						trackName = cjson['data']['tracksAudioPlay'][i]['trackName']  # 音频标题
						src = cjson['data']['tracksAudioPlay'][i]['src']  # 下载链接
						l_tmp.append(trackName)
						l_tmp.append(src)
						l_titleSrc.append(l_tmp)
						l_tmp = []
						# if str(src) in ("null", "None"):
						# 	print("此为付费音频，无法下载")
						# 	break
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
				# 下载从指定序号开始往前音频
				if isinstance(scope, int):
					if scope >= l_indexTitle[i][0]:
						ir = Html_PO.sessionGet(l_indexTitle[i][2])
						# 优化文件名不支持的9个字符
						varTitle = Str_PO.nonsupportChar(str(l_indexTitle[i][1]))
						varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
						open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)
						print(l_indexTitle[i])
				# 下载标题中带关键字的音频
				if isinstance(scope, str):
					if scope in l_indexTitle[i][1]:
						if l_indexTitle[i][2] != None:
							ir = Html_PO.sessionGet(l_indexTitle[i][2])
							# 优化文件名不支持的9个字符
							varTitle = Str_PO.nonsupportChar(str(l_indexTitle[i][1]))
							varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
							open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)
							print(l_indexTitle[i])
						else:
							print("[warning] => 空地址可能是付费音频，无法下载")
				# 下载所有视频
				if scope == "all":
					ir = Html_PO.sessionGet(l_indexTitle[i][2])
					# 优化文件名不支持的9个字符
					varTitle = Str_PO.nonsupportChar(str(l_indexTitle[i][1]))
					varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
					open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)
					print(l_indexTitle[i])



	# 3，单音频下载
	def downSingle(self, albumId, varKeyword, toSave):

		# 获取专辑音频总数
		cjson = Html_PO.getJson("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum=1".format(albumId))
		if cjson["ret"] != 200 :
			print("[errorrrrrrrrr] albumId不存在！")
			os._exit(0)
		else:
			albumTitle = cjson['data']['tracks'][0]['albumTitle']
			print("专辑名：{}".format(albumTitle))
			trackTotalCount = int(cjson["data"]["trackTotalCount"])
			print("音频数：" + str(trackTotalCount))
			print("保存至：{}\{}".format(toSave, albumTitle))
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
				cjson = Html_PO.getJson("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum={}".format(albumId, num))
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
				cjson = Html_PO.getJson("https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}".format(albumId, num))
				for i in range(30):
					try:
						trackName = cjson['data']['tracksAudioPlay'][i]['trackName']  # 音频标题
						src = cjson['data']['tracksAudioPlay'][i]['src']  # 下载链接
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
				if isinstance(varKeyword, int):
					if l_indexTitle[i][0] == varKeyword :
						if l_indexTitle[i][2] != None:
							ir = Html_PO.sessionGet(l_indexTitle[i][2])
							# 优化文件名不支持的9个字符
							varTitle = Str_PO.nonsupportChar(str(l_indexTitle[i][1]))
							varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
							open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)
							print(l_indexTitle[i])
						else:
							print("[warning] => 空地址可能是付费音频，无法下载")
						break



if __name__ == '__main__':

	ximalaya = Ximalaya()


	albumId = input("请输入albumId（数字）：")

	if Str_PO.isNumberByStr(albumId):
		choose = input("请选择（1）获取音频列表；（2）多音频下载；（3）单音频下载：")
		if choose == "1":
			print("获取音频列表".center(100, "-"))
			ximalaya.getAlbumList(albumId)  # 13738175
		elif choose == "2":
			c2 = input("请选择（1）所有音频；（2）某序号之前音频；（3）标题中带关键字音频：")
			if c2 == "1":
				print("下载所有音频".center(100, "-"))
				ximalaya.downRange(albumId, "d:\\500")
			elif c2 == "2":
				sn = input("请输入序号：")
				print(("下载从序号《" + str(sn) + "》之前的音频").center(100, "-"))
				ximalaya.downRange(albumId, "d:\\500", scope=int(sn))  # 下载从序号《169》之前的音频
			elif c2 == "3":
				kw = input("请输入音频标题中的关键字：")
				print(("下载标题中带“" + str(kw) + "”的音频").center(100, "-"))
				ximalaya.downRange(albumId, "d:\\500", str(kw))  # 下载标题中带“XXX”关键字的音频
			else:
				os._exit(0)
		elif choose == "3":
			c33 = input("请输入音频序号：")
			print(("下载序号《" + str(c33) + "》的音频").center(100, "-"))
			ximalaya.downSingle(albumId, int(c33), "d:\\500")   # 下载序号《X》的音频

		else:
			os._exit(0)
	else:
		os._exit(0)

