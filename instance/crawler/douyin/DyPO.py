# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: 抖音视频下载（手机端，Web端，支持单个视频、视频列表批量下载）
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# 手机版单视频页、列表页 https://v.douyin.com/Jp4GEo6/
# 网页版单视频页 https://www.douyin.com/discover
# 网页版列表页 https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg  全说商业

# 过滤掉非法的多字节序列问题
# b = "型➕换季收纳法🔥叠衣"
# print(b.encode('gbk', 'ignore').decode('gbk') )   # 型换季收纳法叠衣
#***************************************************************

import requests, re, os, platform, bs4, json, sys
from urllib import parse
sys.path.append("../../../")

from PO.DataPO import *
Data_PO = DataPO()

from PO.FilePO import *
File_PO = FilePO()

from PO.HtmlPO import *
Html_PO = HtmlPO()

from PO.StrPO import *
Str_PO = StrPO()

from PO.WebPO import *
Web_PO = WebPO("chrome")

class DyPO:


	def downVideo(self, url, toSave):

		'''
		1，下载单个抖音视频
		:param url = 'https://www.douyin.com/video/7157633339661307168'
		:param url = "https://v.douyin.com/hbjqhuT"
		'''

		# 解析 https://v.douyin.com/hbjqhuT 成 https://www.douyin.com/video/7157633339661307168
		if 'https://v.douyin.com/' in url:
			rsp = Html_PO.rspGet(url)
			aweme_id = re.findall(r'video/(\w+-\w+-\w+|\w+-\w+|\w+)', rsp.url)  # ['6976835684271279400']
			url2 = 'https://www.douyin.com/video/' + aweme_id[0]

		print("[待下载] => " + url + " => " + url2)

		headers = {
			"cookie":
					  "s_v_web_id=verify_kwlyvfty_u4F0a4eC_HR0R_45qA_BGNr_tcfqSLkaFeIa; _"
					  "tea_utm_cache_1300=undefined; __ac_nonce=061a6114700def9eb597f; __"
					  "ac_signature=_02B4Z6wo00f01e59nzAAAIDAZTYE0lZHzxHuWZuAABo7n7oK78zhgb8Ol30kLigl-Pu9Q6sKyLpV-BQ3rbF1vLak-TtxN0ysQpQIX.VKlIbTkVBVA4rBt1JdylfNbrGz2NI4r4d7uQWMRa.r56; tt_scid=tbEntOkthFZL51883ve.2ORcwMNYlHUb6tegsnIzC9HSbV5u3J8ASl23x6S7wONy6e5e; "
					 ,
			"user-agent": Data_PO.getUserAgent()
		}

		rsp = requests.get(url=url2, headers=headers)
		# print(rsp.text)

		info = bs4.BeautifulSoup(rsp.text, 'lxml')

		# 定位到<script id="RENDER_DATA" type="application/json">
		js = str(info.select_one("script#RENDER_DATA"))

		# 将 RENDER_DATA 解码成 json 文本
		s_json = parse.unquote(js)
		# print(s_json)

		# 转换成json格式
		s_json = s_json.replace('<script id="RENDER_DATA" type="application/json">', '').replace('</script>', '')
		d_json = json.loads(s_json)

		# 用户名
		nickname = d_json['41']['aweme']['detail']['authorInfo']['nickname']
		# print(nickname)

		# 标题
		title = d_json['41']['aweme']['detail']['desc']
		title = Str_PO.delSpecialChar(str(title), "，", "。", "#", "@")  # 优化文件名中不需要的字符
		# print(title)

		# 生成目录（# 用户名作为目录）
		File_PO.newLayerFolder(toSave + "/" + nickname)
		folder = f'{toSave}/{nickname}'

		# 下载链接
		downUrl = d_json['41']['aweme']['detail']['video']['playApi']
		downUrl = downUrl.replace("//", "https://")
		# print(downUrl)
		ir = Html_PO.rspGet(downUrl)
		open(f'{folder}/{title}.mp4', 'wb').write(ir.content)

		# # 输出结果['目录'，'标题','下载地址']
		# l_result = []
		# l_result.append(f)
		# # l_result.append((str(title).encode("utf-8").decode("utf-8")))
		# l_result.append(title)
		# l_result.append(downUrl)
		# # print(l_result)
		# print('[已完成] => ' + str(l_result).encode('gbk', 'ignore').decode('gbk'))

		print('[已完成] => ' + str(folder) + "/" + str(title) + ".mp4")


	def downVidoeList(self, url, toSave, *param):

		'''
		2，下载多个抖音(列表页)视频
		:param url:  https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg
		:param toSave:
		:return:
		'''


		headers = {
			"cookie":
				"s_v_web_id=verify_kwlyvfty_u4F0a4eC_HR0R_45qA_BGNr_tcfqSLkaFeIa; _"
				"tea_utm_cache_1300=undefined; __ac_nonce=061a6114700def9eb597f; __"
				"ac_signature=_02B4Z6wo00f01e59nzAAAIDAZTYE0lZHzxHuWZuAABo7n7oK78zhgb8Ol30kLigl-Pu9Q6sKyLpV-BQ3rbF1vLak-TtxN0ysQpQIX.VKlIbTkVBVA4rBt1JdylfNbrGz2NI4r4d7uQWMRa.r56; tt_scid=tbEntOkthFZL51883ve.2ORcwMNYlHUb6tegsnIzC9HSbV5u3J8ASl23x6S7wONy6e5e; "
			,
			"user-agent": Data_PO.getUserAgent()
		}

		print("[待下载列表页] => " + url)

		# 使用selenium解析动态html
		# 参考：https://blog.csdn.net/weixin_44259720/article/details/127075628
		Web_PO.openURL(url)
		qty = Web_PO.pageDown('Eie04v01')
		# print(qty)

		text = Web_PO.driver.page_source
		text = bs4.BeautifulSoup(text, 'lxml')
		link = text.find(class_='EZC0YBrG').find_all('a')
		sign = 0
		for a in link:
			if len(param) == 2:
				vid = "/video/" + str(param[1])
				# 下载vid之后（即最新）
				if param[0] == 'a':
					if vid != a['href']:
						# print("https://www.douyin.com" + a['href'])
						self.downVideo("https://www.douyin.com" + a['href'], toSave)
					else:
						break
				# 下载vid之前（即最旧）
				if param[0] == 'b':
					if vid == a['href']:
						sign = 1
					if sign == 1:
						# print("https://www.douyin.com" + a['href'])
						self.downVideo("https://www.douyin.com" + a['href'], toSave)

			else:
				# 下载所有
				print("https://www.douyin.com" + a['href'])
				# self.downVideo("https://www.douyin.com/video/7151241259796008222", toSave)



		sys.exit(0)



		# # 获取网页作品数
		#
		# html = requests.get(url)
		# html.encoding = 'utf-8'
		# text = html.text
		# bsop = BeautifulSoup(text, 'html.parser')
		# for i in bsop.select('span[class="_03811320ee25b81d1c705fae532572ec-scss"]'):
		# 	# print(i.get_text())
		# 	workQTY = i.get_text()
		# 	break
		#
		#
		# # 输出信息
		# sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=50&max_cursor=0&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(sec_id)
		# comment = Html_PO.getJson(sec_id_url)
		# for s in comment['aweme_list']:
		# 	# 用户名
		# 	nickname = s['author']['nickname']
		# 	# 生成目录
		# 	if platform.system() == 'Darwin':
		# 		File_PO.newLayerFolder(toSave + "/" + nickname)
		# 		varFolder = str(toSave) + "/" + nickname
		# 	if platform.system() == 'Windows':
		# 		File_PO.newLayerFolder(toSave + "\\" + nickname)
		# 		varFolder = str(toSave) + "\\" + nickname
		# 	print("用户名：{}({})".format(nickname, url))
		# 	print("视频数：{}".format(workQTY))
		# 	break
		#
		# max_cursor = 0
		#
		# # 分页功能
		# while True:
		# 	while True:
		# 		if (max_cursor == 0):
		# 			sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=50&max_cursor=0&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(sec_id)
		# 		else:
		# 			sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=50&max_cursor={1}&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(sec_id, max_cursor)
		# 		comment = Html_PO.getJson(sec_id_url)
		# 		if (len(comment['aweme_list']) == 0):
		# 			os._exit(0)
		# 		else:
		# 			# 下一页最大下标
		# 			max_cursor = comment['max_cursor']
		#
		# 			for s in comment['aweme_list']:
		#
		# 				# 视频标题
		# 				varTitle = s['desc']
		#
		# 				# 优化文件名不支持的9个字符
		# 				varTitle = Str_PO.delSpecialCharacters(str(varTitle))
		#
		# 				# 过滤掉#后的广告
		# 				# varTitle = re.sub("(\#\w+)|(\@\w+)", '', varTitle)
		#
		# 				# 视频地址(过滤v5-开头的视频)
		# 				videoURL = s['video']['play_addr_lowbr']['url_list'][0]
		# 				if "http://v5-" in videoURL:
		# 					videoURL = s['video']['play_addr_lowbr']['url_list'][1]
		#
		# 				# 下载
		# 				if isinstance(scope, int):
		# 					# 下载从序号《3》之前的音频
		# 					if scope >= int(workQTY):
		# 						# 优化文件名不支持的9个字符
		# 						varTitle = str(workQTY) + "_" + varTitle
		# 						ir = Html_PO.rspGet(videoURL)
		# 						open(f'{toSave}/{nickname}/{varTitle}.mp4', 'wb').write(ir.content)
		# 						# 输出结果
		# 						l_result = []
		# 						l_result.append(varFolder)
		# 						l_result.append(varTitle)
		# 						l_result.append(videoURL)
		# 						# print(l_result)
		# 						print(str(l_result).encode('gbk', 'ignore').decode('gbk'))
		#
		# 						l_result = []
		# 				if isinstance(scope, str):
		# 					# 下载所有视频
		# 					if scope == "all":
		# 						varTitle = str(workQTY) + "_" + varTitle
		# 						ir = Html_PO.rspGet(videoURL)
		# 						open(f'{toSave}/{nickname}/{varTitle}.mp4', 'wb').write(ir.content)
		# 						# 输出结果
		# 						l_result = []
		# 						l_result.append(varFolder)
		# 						l_result.append(varTitle)
		# 						l_result.append(videoURL)
		# 						# print(l_result)
		# 						print(str(l_result).encode('gbk', 'ignore').decode('gbk'))
		#
		# 						l_result = []
		# 					# 下载标题中带关键字的音频
		# 					elif scope in varTitle:
		# 						varTitle = str(workQTY) + "_" + varTitle
		# 						ir = Html_PO.rspGet(videoURL)
		# 						open(f'{toSave}/{nickname}/{varTitle}.mp4', 'wb').write(ir.content)
		# 						# 输出结果
		# 						l_result = []
		# 						l_result.append(varFolder)
		# 						l_result.append(varTitle)
		# 						l_result.append(videoURL)
		# 						# print(l_result)
		# 						print(str(l_result).encode('gbk', 'ignore').decode('gbk'))
		#
		# 						l_result = []
		# 				workQTY = int(workQTY) - 1
		# 			break



if __name__ == '__main__':

	Dy_PO = DyPO()

