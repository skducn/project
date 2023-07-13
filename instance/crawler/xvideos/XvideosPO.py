# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-10
# Description: xvideos 下载学习 (https://www.hotbox.fun/)

# https://www.fujieace.com/jingyan/xvideos-download.html
# https://www.rstk.cn/news/866463.html?action=onClick
# cat *.ts > xxx.ts
# brew install ffmpeg
# ffmpeg -y -i xxx.ts -c:v libx264 -c:a copy -bsf:a aac_adtstoasc xxx.mp4

# 1, 获取源码，搜多 setVideoHLS 和 setUploaderName
# html5player.setVideoHLS('https://cdn77-vid.xvideos-cdn.com/qHdCP9l007yzoXJWRb-bnA==,1689166227/videos/hls/cb/fa/f0/cbfaf0bbd22695ac8c50b1f90eecd0b6/hls.m3u8');
# html5player.setUploaderName('chicken1806');
# html5player.setVideoURL('/video76932809/_');
#
# 2，下载 hls.m3u8 、 hls-720p-879f1.m3u8、 *.ts
# 下载 hls.m3u8后打开定位 hls-720p-XXXX.m3u8并下载后打开，获取所有ts文件并下载。

#***************************************************************

import io, requests, re, os, platform, bs4, json, sys, m3u8
from urllib import parse
# sys.path.append("../../../")
sys.path.append("/Users/linghuchong/Downloads/51/Python/project/")
import sys, smtplib, os, base64, requests, urllib, json, jsonpath, logging, time
from urllib.request import urlretrieve
from time import sleep

from PO.FilePO import *
File_PO = FilePO()

from PO.StrPO import *
Str_PO = StrPO()

from PO.NetPO import *
Net_PO = NetPO()

from contextlib import closing
import requests, jsonpath, hashlib, json
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# requests.get('https://example.com', verify=False)

path = "/Users/linghuchong/Downloads/eMule/Xvideos/"

class XvideosPO:


	def getInfo(self, varUrl):

		# soup = BeautifulSoup(open('./data/video76932809__.mhtml'), 'lxml')
		# r = requests.get(varUrl)
		# r.encoding = "gbk2312"
		# print(r.content)


		soup = BeautifulSoup("https://www.baidu.com", 'lxml')
		print(soup.text)

		sys.exit(0)
		setVideoHLS = soup.text.split("html5player.setVideoHLS(")[1].split(')')[0]
		setVideoHLS = setVideoHLS.replace("'htt=\nps:", "https:").replace("\n", "").replace("hls.m3u8'", "")
		print(setVideoHLS)

		setUploaderName = soup.text.split("html5player.setUploaderName('")[1].split("')")[0]
		print(setUploaderName)

		setVideoURL = soup.text.split("html5player.setVideoURL('")[1].split("')")[0]
		print(setVideoURL)


	def getVideoUrl(self, varUrl, varUser, varFileName):

		# 创建用户目录
		if not os.path.exists(path + varUser):
			os.makedirs(path + varUser)  # chicken1806

		# 创建文件目录
		if not os.path.exists(path + varUser + "/" + varFileName):
			os.makedirs(path + varUser + "/" + varFileName)  # XXX系列

			# 下载1，hls.m3u8
			Net_PO.downFile(varUrl + "hls.m3u8", path + varUser + "/" + varFileName + "/hls.m3u8")
			d_hls = m3u8.load(path + varUser + "/" + varFileName + "/hls.m3u8").data
			l_hls = []
			for i in d_hls["playlists"]:
				l_hls.append(i['uri'])
			print(l_hls)  # ['hls-480p-f9657.m3u8', 'hls-720p-518b4.m3u8', 'hls-1080p-e61c4.m3u8', 'hls-360p-161de.m3u8', 'hls-250p-73a03.m3u8']

			# 下载2，hls-720p-518b4.m3u8
			for i in l_hls:
				if "hls-720" in i:
					Net_PO.downFile(varUrl + i, path + varUser + "/" + varFileName + "/" + i)
					d_720 = m3u8.load(path + varUser + "/" + varFileName + "/" + i).data
					l_ts = []
					for i in d_720["segments"]:
						l_ts.append(i['uri'])
					print(l_ts)  # ['hls-720p-518b40.ts', 'hls-720p-518b41.ts', 'hls-720p-518b42.ts']
					break

			# 下载3，ts
			for i in l_ts:
				Net_PO.downFile(varUrl + i, path + varUser + "/" + varFileName + "/" + i)


		# f = open(path + varFolder + "/hls.m3u8")
		# for f720 in f.readlines():
		# 	if 'hls-720p' in f720:
		# 		# 下载2，hls-720pXXX.m3u8
		# 		Net_PO.downFile(varUrl + f720, path + varFolder + "/" + f720)
		# 		data = m3u8.load(path + varFolder + "/" + f720).data
				# print(path + varFolder + "/" + f720)
				# print(data)
				# l_ts = []
				# for i in data["segments"]:
				# 	l_ts.append(i['uri'])
				# # print(l_ts)  # ['hls-720p-518b40.ts', 'hls-720p-518b41.ts', 'hls-720p-518b42.ts']
				# # file = open(path + varFolder + "/temp.m3u8", 'w')
				# # for n in list1:
				# # 	file.write("file '" + path + varFolder + "/" + n + "'")
				# # 	file.write("\n")
				# for i in l_ts:
				# 	Net_PO.downFile(varUrl + i, path + varFolder + "/" + i)

				# # sys.exit(0)
				# f2 = open(path + varFolder + "/" + f720)
				# for fts in f2.readlines():
				# 	if '.ts' in fts:
				# 		fts = fts.replace('\n', '')
				# 		print(varUrl + fts)
				# 		Net_PO.downFile(varUrl + fts, path + varFolder + "/" + fts)


		# os.system('cat ' + path + varFolder + "/" + '*.ts > ' + path + varFolder + "/" + varFolder + '.mp4')
		# os.system('del ' + path + varFolder + "/" + '*.ts')


if __name__ == '__main__':

	Xvideos_PO = XvideosPO()

	# Xvideos_PO.getVideoUrl("https://cdn77-vid.xvideos-cdn.com/RQ8awptsSFkElOGWOsXYsw==,1689224214/videos/hls/7b/d4/d4/7bd4d4b0c1d23afeed2f450edebfcc7f/",
	# 					   'chicken1806',
	# 					   '腿玩年系列！抱起黑丝长腿长驱直入，白嫩小穴清晰可见「看片头视频可以约她！」')

	Xvideos_PO.getInfo("https://www.xvideos.com/video76932809/_")
	# Xvideos_PO.getInfo("https://www.baidu.com")