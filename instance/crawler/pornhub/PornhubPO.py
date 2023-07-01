# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: pornhub 获取页面视频地址
# 1, 翻墙保存页面

#***************************************************************

import requests, re, os, platform, bs4, json, sys
from urllib import parse
# sys.path.append("../../../")
sys.path.append("/Users/linghuchong/Downloads/51/Python/project/")

from time import sleep

from PO.FilePO import *
File_PO = FilePO()

from PO.StrPO import *
Str_PO = StrPO()

from contextlib import closing
import requests, jsonpath, hashlib, json
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# requests.get('https://example.com', verify=False)

s_projectPath = "/Users/linghuchong/Downloads/eMule/pornhub/"

class PornhubPO:

	def setFileList(self):

		# 初始化000.txt文件

		# varPath = "/Users/linghuchong/Downloads/eMule/pornhub/"
		s_listFile=  "000.txt"
		l_folderFile= (File_PO.getListDir(s_projectPath))
		print(l_folderFile)
		# sys.exit(0)

		for s_folder in l_folderFile:
			varPathFolder = s_projectPath + s_folder + "/"  # /Users/linghuchong/Downloads/eMule/pornhub/delphine1

			if os.path.isdir(varPathFolder):
				l_varFile = []
				l_varSize = []

				# 更新000.txt文件
				if os.path.isfile(varPathFolder + s_listFile):
					...
					# 1，获取待下载文件名和字节数与list文件比对，没有的文件则下载，下载后写入list
					# 2，文件名一样，字节数不一样，提醒，且不下载

				else:
					# 新建文件（获取目录中文件名和字节数）
					File_PO.newFile(varPathFolder, s_listFile)
					# 获取制定目录里的文件名
					l_pathFile = (File_PO.getListFile(varPathFolder + "*.*"))
					for varPathFile in l_pathFile:
						varSize = (File_PO.getFileSize(varPathFile))  # 获取文件的大小
						varFile = (os.path.split(varPathFile)[1])  # 截取文件名
						l_varFile.append(varFile)
						l_varSize.append(varSize)
					d = dict(zip(l_varFile, l_varSize))  # 组成字典
					# 对字典key进行升序
					d2 = ({k: v for k, v in sorted(d.items(), key=lambda item: item[0])})
					with open(varPathFolder + s_listFile, "w") as f:
						for k, v in d2.items():
							f.write(str(k) + "/" + str(d[k]) + "\n")


	def html2url(self, varHtml, varPh, varUrl):

		# 将html解析成URL
		# varUrl 用于脚本
		# varPh  用于 alfrd

		# File_PO.delFile(os.getcwd() + "/" + varUrl)

		# 1，解析html获取页面url
		soup = BeautifulSoup(open(varHtml, encoding='utf-8'), features='lxml')
		s_title = (soup.title.string)
		# varFolder = title.split('的')[0]
		# print(s_title) # Delphine Films 黄片&高清现场预告| Pornhub
		# print(varFolder)
		s_pageUrl = soup.find("link", {'rel': 'canonical'}).attrs['href']
		# print(s_pageUrl)  # https://cn.pornhub.com/channels/delphine
	

		# 2，获取目录名
		if "/model" in s_pageUrl:
			s_folder = s_pageUrl.split("https://cn.pornhub.com/model/")[1].split("/")[0]
			s_plate = 'model'
		elif "channels" in s_pageUrl:
			s_folder = s_pageUrl.split("https://cn.pornhub.com/channels/")[1].split("/")[0]
			s_plate = 'channels'
		# print(s_folder) # delphine
		if 'page=' in s_pageUrl:
			s_pageNum = s_pageUrl.split("videos?page=")[1]
		else:
			s_pageNum = '1'
		s_folder = s_folder + s_pageNum
		# print(s_folder) # delphine1	

		if s_plate == 'model':
			s_videoUrlTotalNum = len(soup.find("ul", {'id': 'mostRecentVideosSection'}).find_all('a'))
		elif s_plate == 'channels':
			s_videoUrlTotalNum = len(soup.find("ul", {'id': 'moreData'}).find_all('a'))
			
		# 3，新建目录及000.txt文件
		if os.path.isdir(s_projectPath + s_folder) == False:
			File_PO.newFolder(s_projectPath + s_folder)
			File_PO.newFile(s_projectPath + s_folder, "000.txt")
			with open(s_projectPath + s_folder + "/000.txt", "w") as f:
				f.write(s_pageUrl + "(" + str(int(s_videoUrlTotalNum/2)) + ")\n")

		# 4，新建 varPh 及 varUrl 文件
		if os.path.isfile(varPh) == "False":
			File_PO.newFile(os.getcwd(), varPh)
		if os.path.isfile(varUrl) == "False":
			File_PO.newFile(os.getcwd(), varUrl)

		# 5，初始化 varPh 及 varUrl 文件

		with open(varPh, "w") as f:
			f.write(s_pageUrl + "(" + str(int(s_videoUrlTotalNum/2)) + ")\n") # https://cn.pornhub.com/channels/delphine(36)
		for i in range(1, s_videoUrlTotalNum, 2):
			if s_plate == 'model':
				s_videoUrl = (soup.find("ul", {'id': 'mostRecentVideosSection'}).find_all('a')[i].attrs['href'])
				# vName = (soup.find("ul", {'id': 'mostRecentVideosSection'}).find_all('a')[i].text).strip()
			elif s_plate == 'channels':
				s_videoUrl = (soup.find("ul", {'id': 'moreData'}).find_all('a')[i].attrs['href'])
			with open(varPh, "a") as f:
				f.write("ph " + s_folder + " " + s_videoUrl + "\n")
			with open(varUrl, "a") as f:
				f.write(s_folder + ", " + s_videoUrl + ",[]" + "\n")
		with open(varPh, "a") as f:
			f.write("-" * len("ph " + s_folder + " " + s_videoUrl) + "\n")






	def brazzers2url(self, varHtml, varPh, varUrl):

		# 将html解析成URL
		# varUrl 用于脚本
		# varPh  用于 alfrd

		# 删除 url.txt
		if os.path.isfile(os.getcwd() + "/" + varUrl):
			File_PO.delFile(os.getcwd() + "/" + varUrl)

		if os.path.isfile(varPh) == "False":
			File_PO.newFile(os.getcwd(), varPh)
		if os.path.isfile(varUrl) == "False":
			File_PO.newFile(os.getcwd(), varUrl)

		# 1，获取目录名
		soup = BeautifulSoup(open(varHtml, encoding='utf-8'), features='lxml')
		# title = (soup.title.string)
		# print(title)
		
		varPage = soup.find("link", {'rel': 'canonical'}).attrs['href']
		# print(varPage)
		varPage2 = varPage.split('videos?page=')[1]
		# print(varPage)
		# sys.exit(0)
		varFolder = 'Brazzers' + str(varPage2)
		# sys.exit(0)

		# 新建目录
		varPath = "/Users/linghuchong/Downloads/eMule/pornhub/"
		if os.path.isdir(varPath + varFolder) == False:
			File_PO.newFolder(varPath + varFolder)


		# 首页
		# total = len(soup.find("ul", {'id': 'moreData'}).find_all('a'))
		# 第二页开始
		total = len(soup.find("ul", {'id': 'showAllChanelVideos'}).find_all('a'))


		with open(varPh, "w") as f:
			f.write(varPage + "(" + str(int(total/2)) + ")\n")

		for i in range(1, total, 2):
			# vUrl = (soup.find("ul", {'id': 'moreData'}).find_all('a')[i].attrs['href'])
			vUrl = (soup.find("ul", {'id': 'showAllChanelVideos'}).find_all('a')[i].attrs['href'])
			# vName = (soup.find("ul", {'id': 'mostRecentVideosSection'}).find_all('a')[i].text).strip()
			with open(varPh, "a") as f:
				f.write("ph " + varFolder + " " + vUrl + "\n")
			with open(varUrl, "a") as f:
				f.write(varFolder + "," + vUrl + ",[]" + "\n")
		with open(varPh, "a") as f:
			f.write("-" * len("ph " + varFolder + " " + vUrl) + "\n")


	def downloadOne(self, varFolder, vUrl):

		# 单个视频下载（存在则忽略）
		# alfred用法，如：ph folder https://cn.pornhub.com/view_video.php?viewkey=63de9d08b9
		# python cmd.py folder https://cn.pornhub.com/view_video.php?viewkey=63de9d08b9
		# folder 如果为/表示 下载到 '/Users/linghuchong/Downloads/eMule/pornhub/'

		os.system("clear")
		varPath = '/Users/linghuchong/Downloads/eMule/pornhub/'
		# print((varFolder + "'s 视频").center(100, "-"))

		# 新建目录
		if os.path.isdir(varPath + varFolder) == False:
			File_PO.newFolder(varPath + varFolder)

		# 2,MD5加密
		m = hashlib.md5(vUrl.encode(encoding="utf-8"))  # 等同于 m = hashlib.md5(b'123456')
		job_id = m.hexdigest()
		# print(job_id)

		# 3，解析视频地址1
		param = {"type":"extractor",
			 "job_id": job_id,
			 "params":
				 {"priority": "10000",
				  "playlist": "false",
				  "page_url": vUrl,
				  "clientip": "103.125.165.103"}
			 }

		headers = {
		"authority": "api.xxxsave.net",
		"method": "POST",
		"path": "/api/job",
		"scheme": "https",
		'accept': '*/*',
		# "Accept-Encoding": "identity",
		# "Range": "bytes=0-1",
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'zh-CN,zh;q=0.9',
		# 'content-length': '213',
		'content-type': 'application/json',
		'dnt': '1',
		'origin': 'https://xxxsave.net',
		'referer': 'https://xxxsave.net/',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': "macOS",
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-site',
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
		}
		session = requests.session()
		try:
			r = session.post("https://api.xxxsave.net/api/job", json=param, verify=False, headers=headers)
		except:
			r = session.post("https://api.xxxsave.net/api/job", json=param, verify=False, headers=headers)
		# print(r.text)

		sleep(2)

		try:
			# 4，解析视频地址2
			for x in range(10):
				r = session.get("https://api.xxxsave.net/api/check?type=extractor&job_id=" + str(job_id), verify=False)
				sleep(2)
				# print(r.text)
				d_json = {}
				d_json = json.loads(r.text)
				if d_json['data']['state'] == "completed":
					break

		# 5，获取title
			fileName = d_json['data']['title'] + ".mp4"
			fileName = Str_PO.delSpecialChar(fileName)
		except:
			viewKey = vUrl.split("viewkey=")[1]
			print("***[errorrrrrrrrrr解析视频地址2] => [" + str(viewKey) + "]")
			return -1
			# sys.exit(0)

		# 6，获取各分辨率的视频地址
		format_id = jsonpath.jsonpath(d_json, '$.data.formats[*].format_id')
		# print(format_id)  # ['240p', 'hls-547-0', 'hls-547-1', '480p', 'hls-1049-0', 'hls-1049-1', '720p', 'hls-1964-0', 'hls-1964-1', '1080p', 'hls-3560']
		url = jsonpath.jsonpath(d_json, '$.data.formats[*].url')
		# print(url)
		d = dict(zip(format_id, url))
		# print(d)

		# 7, 下载视频，显示文件大小，下载进度条'''
		varPathFileName = varPath + varFolder + "/" + fileName
		# print(varPathFileName)
		# print("!!!!!!!!!!!!")
		

		# https://blog.csdn.net/weixin_38819889/article/details/124853178
		# try :
		with closing(requests.get(d['720p'], timeout=10, verify=False, stream=True)) as response:
			chunk_size = 1024  # 单次请求最大值
			content_size = int(response.headers['content-length'])  # 文件总大小
			M = int(content_size / 1024 / 1024)
			# content_size = int(response.request.headers['content-length'])
			# print(content_size)

			var = ""

			# 判断文件是否存在
			# M = content_size / 1024 / 1024
			viewKey = vUrl.split("viewkey=")[1]
			var000 = "[" + str(viewKey) + "], " + str(fileName) 
			# print(var000)
			# var000 = fileName + "/" + str(content_size)  # Dragon Ball - Bulma - Lite Version.mp4/24071579
			
			# # 获取实际目录里所有文件名和大小
			l_files = File_PO.getListFile(varPathFileName)

			s_actualFile = varPathFileName.split(varPath + varFolder + "/")[1]
			s_actualSize = File_PO.getFileSize(varPathFileName)

			# print(s_actualFile) # Delphine Films  Blake Blossom Is The Sexiest Boss Ever.mp4
			# print(s_actualSize) # 234687674
			s_actualFileSize = s_actualFile + "(" + str(s_actualSize) + ")"

			# list4 = []
			# for i in l_files:
			# 	size = File_PO.getFileSize(i)
			# 	s_file = i.split(varPath + varFolder + "/")[1]
			# 	list4.append(s_file + "(" + str(size) + ")")
			# print(list4) # ['Delphine Films  Blake Blossom Is The Sexiest Boss Ever.mp4(234687674)']

			# sys.exit(0)

			# 遍历000.txt文件名的大小与实际目录里文件名大小是否一直
			with open(varPath + varFolder + "/000.txt", "r") as f:
				list1 = f.readlines()
				for l in list1:
					if s_actualFileSize in l:
						# viewKey = vUrl.split("viewkey=")[1]

						print("*** [ignore] => [" + str(viewKey) + "], " + str(fileName) + "(" + str(content_size) + ")\n")
						var = "ignore"
						break
					if fileName in l:
						print("*** [warning] => [" + str(viewKey) + "], " + str(fileName) + " => 实际：" + str(s_actualSize) + " / 预期：" + str(content_size) + "\n")
	
						xunwen = input("是否要重新下载 y/n?")
						if xunwen == "n":
							var = "ignore"
						else:
							var = "download"

						break

			# sys.exit(0)

			if var != 'ignore':
				M = content_size / 1024 / 1024
				# print(str(content_size) + " = " + str(M) + "MB")                # 显示文件大小，如 1024 = 1MB
				varSize = str(content_size) + " = " + str(M) + "MB"
				data_count = 0  # 当前已传输的大小
				# print(varFolder + " => " + vUrl + " (" + str(int(M)) + " MB" + ")")
				viewKey = vUrl.split("viewkey=")[1]
				# print("  Downloading " + download_url + " (" + str(int(M)) + " MB" + ")")
				with open(varPathFileName, "wb") as file:
					for data in response.iter_content(chunk_size=chunk_size):
						file.write(data)
						done_block = int((data_count / content_size) * 50)  # 已经下载的文件大小
						data_count = data_count + len(data)  # 实时进度条进度
						now_jd = (data_count / content_size) * 100  # %% 表示%
						# print("\r[%s] (%s) [%s%s] %d%% %s/%s" % (viewKey, fileName, done_block * '█', ' ' * (50 - 1 - done_block), now_jd, data_count, content_size), end=" ")
						print("\r%d%%, %s, %s(%s MB)" % (now_jd, viewKey, fileName, int(M)), end=" ")

				with open(varPath + varFolder + "/000.txt", "a") as f:
					# f.write(str(fileName) + "/" + str(content_size) + "/" + vUrl + "\n")
					f.write("[" + str(viewKey) + "], " + str(fileName) + "(" + str(int(M)) + " MB)\n")
				print("\n")
		# except:
		# 	print("[errorrrrrrrrrr下载视频] => " + vUrl)
			return -1
		return 0

	def downloadOneOver(self, varFolder, vUrl):

		# 单个视频下载（强制下载）
		# alfred用法，如：phover folder https://cn.pornhub.com/view_video.php?viewkey=63de9d08b9
		# python cmdOver.py folder https://cn.pornhub.com/view_video.php?viewkey=63de9d08b9
		# folder 如果为/表示 下载到 '/Users/linghuchong/Downloads/eMule/pornhub/'

		varPath = '/Users/linghuchong/Downloads/eMule/pornhub/'
		print((varFolder + "'s 视频").center(100, "-"))

		# 新建目录
		if os.path.isdir(varPath + varFolder) == False:
			File_PO.newFolder(varPath + varFolder)

		# 2,MD5加密
		m = hashlib.md5(vUrl.encode(encoding="utf-8"))  # 等同于 m = hashlib.md5(b'123456')
		job_id = m.hexdigest()
		# print(job_id)

		# 3，解析视频地址1
		param = {"type":"extractor",
			 "job_id": job_id,
			 "params":
				 {"priority": "10000",
				  "playlist": "false",
				  "page_url": vUrl,
				  "clientip": "103.125.165.103"}
			 }

		headers = {
		"authority": "api.xxxsave.net",
		"method": "POST",
		"path": "/api/job",
		"scheme": "https",
		'accept': '*/*',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'zh-CN,zh;q=0.9',
		# 'content-length': '213',
		'content-type': 'application/json',
		'dnt': '1',
		'origin': 'https://xxxsave.net',
		'referer': 'https://xxxsave.net/',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': "macOS",
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-site',
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
		}
		session = requests.session()
		try:
			r = session.post("https://api.xxxsave.net/api/job", json=param, verify=False, headers=headers)
		except:
			r = session.post("https://api.xxxsave.net/api/job", json=param, verify=False, headers=headers)
		# print(r.text)

		sleep(2)

		# 4，解析视频地址2
		for x in range(10):
			r = session.get("https://api.xxxsave.net/api/check?type=extractor&job_id=" + str(job_id), verify=False)
			sleep(2)
			# print(r.text)
			d_json = {}
			d_json = json.loads(r.text)
			if d_json['data']['state'] == "completed":
				break

		# 5，获取title
		try:
			fileName = d_json['data']['title'] + ".mp4"
			fileName = Str_PO.delSpecialChar(fileName)
		except:
			print("errorrrrrrrrrr, 解析失败！")
			sys.exit(0)

		# 6，获取各分辨率的视频地址
		format_id = jsonpath.jsonpath(d_json, '$.data.formats[*].format_id')
		# print(format_id)  # ['240p', 'hls-547-0', 'hls-547-1', '480p', 'hls-1049-0', 'hls-1049-1', '720p', 'hls-1964-0', 'hls-1964-1', '1080p', 'hls-3560']
		url = jsonpath.jsonpath(d_json, '$.data.formats[*].url')
		# print(url)
		d = dict(zip(format_id, url))
		# print(d)

		# 7, 下载视频，显示文件大小，下载进度条'''
		varPathFileName = varPath + varFolder + "/" + fileName

		# https://blog.csdn.net/weixin_38819889/article/details/124853178
		with closing(requests.get(d['720p'], timeout=10, verify=False, stream=True)) as response:
			chunk_size = 1024  # 单次请求最大值
			content_size = int(response.headers['content-length'])  # 文件总大小
			M = content_size / 1024 / 1024
			# print(str(content_size) + " = " + str(M) + "MB")                # 显示文件大小，如 1024 = 1MB
			varSize = str(content_size) + " = " + str(M) + "MB"
			data_count = 0  # 当前已传输的大小
			print("Collecting '" + fileName + "' (" + str(int(M)) + " MB" + ")")
			# print("  Downloading " + download_url + " (" + str(int(M)) + " MB" + ")")
			with open(varPathFileName, "wb") as file:
				for data in response.iter_content(chunk_size=chunk_size):
					file.write(data)
					done_block = int((data_count / content_size) * 50)  # 已经下载的文件大小
					data_count = data_count + len(data)  # 实时进度条进度
					now_jd = (data_count / content_size) * 100  # %% 表示%
					print("\r Downloading [%s%s] %d%% %s/%s" % (done_block * '█', ' ' * (50 - 1 - done_block), now_jd, data_count, content_size), end=" ")
		with open(varPath + varFolder + "/000.txt", "a") as f:
			f.write("-" * len(str(fileName) + "/" + str(content_size)) + "\n")
			f.write(str(fileName) + "/" + str(content_size) + "\n")
		print("\n")

	def downloadMore(self, varUrlFile):

		with open(varUrlFile, 'r') as f:
			l_content = f.readlines()
		# f.close()

		for ele in l_content:
			varFolder = ele.split(",")[0]
			vUrl = ele.split(",")[1]
			vStatus = ele.split(",")[2].replace("\n", "")
			# print(vStatus)

			if vStatus == "[]":
				varResult = self.downloadOne(varFolder, vUrl)
				if varResult == 0:
					for l in range(len(l_content)):
						if varFolder + "," + vUrl + ",[]" in l_content[l]:
							l_content[l] = varFolder + "," + vUrl + ",[done]\n"
							break
							# print(l_content[l])
					# print(l_content)
					with open(varUrlFile, 'w') as f:
						for i in l_content:
							f.write(i)
					f.close()
			else:
				print(ele)





if __name__ == '__main__':
	Pornhub_PO = PornhubPO()

