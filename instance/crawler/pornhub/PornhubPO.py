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


from contextlib import closing
import requests, jsonpath, hashlib, json
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# requests.get('https://example.com', verify=False)

class PornhubPO:

	def run(self, varHtml):

		varPath =  '/Users/linghuchong/Downloads/eMule/pornhub/'
		print((varHtml + "'s 视频").center(100, "-"))

		# 新建目录
		if os.path.isdir(varPath + varHtml) == False:
			File_PO.newFolder(varPath + varHtml)

		# 1, 获取页面中视频地址
		l_vedioUrl = []
		soup = BeautifulSoup(open(varHtml, encoding='utf-8'), features='lxml')
		for i in range(1, len(soup.find("ul", {'id': 'mostRecentVideosSection'}).find_all('a')), 2):
		# for i in range(1, 10, 2):
			vUrl = (soup.find("ul", {'id': 'mostRecentVideosSection'}).find_all('a')[i].attrs['href'])
			l_vedioUrl.append(vUrl)
			# print(vUrl)

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
			try:
				r = session.get("https://api.xxxsave.net/api/check?type=extractor&job_id=" + str(job_id), verify=False)
			except:
				r = session.get("https://api.xxxsave.net/api/check?type=extractor&job_id=" + str(job_id), verify=False)
			# print(r.text)
			d_json = {}
			d_json = json.loads(r.text)

			# 5，获取title
			fileName = d_json['data']['title'] + ".mp4"

			# 6，获取各分辨率的视频地址
			format_id = jsonpath.jsonpath(d_json, '$.data.formats[*].format_id')
			# print(format_id)  # ['240p', 'hls-547-0', 'hls-547-1', '480p', 'hls-1049-0', 'hls-1049-1', '720p', 'hls-1964-0', 'hls-1964-1', '1080p', 'hls-3560']
			url = jsonpath.jsonpath(d_json, '$.data.formats[*].url')
			# print(url)
			d = dict(zip(format_id, url))
			# print(d)

			# 7, 下载视频，显示文件大小，下载进度条'''
			varPathFileName = varPath + varHtml + "/" + fileName
			# varPathHtml = varPath + varHtml

			# 判断文件是否存在
			if os.path.isfile(varPathFileName):
				print("[ignore] => " + fileName)
			else:
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
				print("\n")

	def runS(self, varFolder, vUrl):

		varPath = '/Users/linghuchong/Downloads/eMule/pornhub/'
		print((varFolder + "'s 视频").center(100, "-"))

		# 1,新建目录
		if os.path.isdir(varPath + varFolder) == False:
			File_PO.newFolder(varPath + varFolder)

		# 2,MD5加密
		m = hashlib.md5(vUrl.encode(encoding="utf-8"))  # 等同于 m = hashlib.md5(b'123456')
		job_id = m.hexdigest()
		print(job_id)

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
		print(r.text)

		sleep(2)

		# 4，解析视频地址2
		try:
			r = session.get("https://api.xxxsave.net/api/check?type=extractor&job_id=" + str(job_id), verify=False)
		except:
			r = session.get("https://api.xxxsave.net/api/check?type=extractor&job_id=" + str(job_id), verify=False)
		print(r.text)
		d_json = {}
		d_json = json.loads(r.text)

		# 5，获取title
		fileName = d_json['data']['title'] + ".mp4"

		# 6，获取各分辨率的视频地址
		format_id = jsonpath.jsonpath(d_json, '$.data.formats[*].format_id')
		# print(format_id)  # ['240p', 'hls-547-0', 'hls-547-1', '480p', 'hls-1049-0', 'hls-1049-1', '720p', 'hls-1964-0', 'hls-1964-1', '1080p', 'hls-3560']
		url = jsonpath.jsonpath(d_json, '$.data.formats[*].url')
		# print(url)
		d = dict(zip(format_id, url))
		# print(d)

		# 7, 下载视频，显示文件大小，下载进度条'''
		varPathFileName = varPath + varFolder + "/" + fileName
		# varPathHtml = varPath + varHtml

		# 判断文件是否存在
		if os.path.isfile(varPathFileName):
			print("[ignore] => " + fileName)
		else:
			# https://blog.csdn.net/weixin_38819889/article/details/124853178
			with closing(requests.get(vUrl, timeout=10, verify=False, stream=True)) as response:
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
			print("\n")


if __name__ == '__main__':

	Pornhub_PO = PornhubPO()

