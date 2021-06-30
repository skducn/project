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


from PO.DataPO import *
from PO.FilePO import *
Data_PO = DataPO()
File_PO = FilePO()


class Ximalaya:

	def __init__(self):
		# 初始化
		self.session = requests.session()
		self.headers = {'User-Agent': Data_PO.getUserAgent()}
		varIp = Data_PO.getIpAgent()
		self.proxies = {str(varIp).split("://")[0]: str(varIp).split("://")[1]}

	def getHtml(self, varUrl):
		chtml = requests.get(url=varUrl, headers=self.headers, proxies=self.proxies)
		cjson = chtml.json()
		return cjson


	# 1，获取音频列表
	def getAudioList(self, albumId):

		# 获取专辑音频总数
		cjson = self.getHtml("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum=1".format(albumId))
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
			cjson = self.getHtml("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum={}".format(albumId, num))
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
			cjson = self.getHtml("https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}".format(albumId, num))
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



	# 2，下载专辑所有音频
	def downAll(self, albumId, toSave, varRange="all"):

		# 获取专辑音频总数
		cjson = self.getHtml("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum=1".format(albumId))
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
			cjson = self.getHtml("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum={}".format(albumId, num))
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
			cjson = self.getHtml("https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}".format(albumId, num))
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

		# 下载
		File_PO.newLayerFolder(toSave + "\\" + albumTitle)  # 自动创建目录
		for i in range(len(l_indexTitle)):
			if isinstance(varRange, int) and varRange >= l_indexTitle[i][0]:
				ir = self.session.get(l_indexTitle[i][2], headers=self.headers)
				varTitle = str(l_indexTitle[i][1]).replace("?", "").replace("/", "").replace("|", "").replace(":", "")
				varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
				open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)
				print(l_indexTitle[i])
			if varRange == "all":
				ir = self.session.get(l_indexTitle[i][2], headers=self.headers)
				varTitle = str(l_indexTitle[i][1]).replace("?", "").replace("/", "").replace("|", "").replace(":", "")
				varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
				open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)
				print(l_indexTitle[i])



	# 3，下载专辑单个音频
	def downOne(self, albumId, varKeyword, toSave):

		# 获取专辑音频总数
		cjson = self.getHtml("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum=1".format(albumId))
		trackTotalCount = int(cjson["data"]["trackTotalCount"])
		albumTitle = cjson['data']['tracks'][0]['albumTitle']
		print("专辑名：{}".format(albumTitle))
		print("保存：{}\{}".format(toSave, albumTitle))
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
			cjson = self.getHtml("https://www.ximalaya.com/revision/album/getTracksList?albumId={}&pageNum={}".format(albumId, num))
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
			cjson = self.getHtml("https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}".format(albumId, num))
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

		# 下载
		File_PO.newLayerFolder(toSave + "\\" + albumTitle)  # 自动创建目录
		for i in range(len(l_indexTitle)):
			if isinstance(varKeyword, int):
				if l_indexTitle[i][0] == varKeyword :
					if l_indexTitle[i][2] != None:
						ir = self.session.get(l_indexTitle[i][2], headers=self.headers)
						varTitle = str(l_indexTitle[i][1]).replace("?", "").replace("/", "").replace("|", "").replace(":", "")
						varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
						open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)
						print(l_indexTitle[i])
					else:
						print("[warning] => 空地址可能是付费音频，无法下载")
					break
			if isinstance(varKeyword, str):
				if varKeyword in l_indexTitle[i][1]:
					if l_indexTitle[i][2] != None:
						ir = self.session.get(l_indexTitle[i][2], headers=self.headers)
						varTitle = str(l_indexTitle[i][1]).replace("?", "").replace("/", "").replace("|", "").replace(":", "")
						varTitle = str(l_indexTitle[i][0]) + "_" + varTitle
						open(f'{toSave}/{albumTitle}/{varTitle}.mp4', 'wb').write(ir.content)
						print(l_indexTitle[i])
					else:
						print("[warning] => 空地址可能是付费音频，无法下载")



if __name__ == '__main__':

	ximalaya = Ximalaya()

	# 1，获取音频列表
	# ximalaya.getAudioList("13738175")


	# 2，下载专辑所有音频
	# ximalaya.downAll("46246212", "d:\\500", "all")
	# ximalaya.downAll("13738175", "d:\\500", varRange=169)  # 从169开始往前下载


	# 3，下载专辑单个音频
	# ximalaya.downOne("13738175", 173, "d:\\500")   # 下载音频编号170的视频
	# ximalaya.downOne("13738175", "为什么", "d:\\5")   # 下载音频标题中带“为什么”关键字的视频



