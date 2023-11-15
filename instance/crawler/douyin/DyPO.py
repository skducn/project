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
# sys.path.append("../../../")
sys.path.append("/Users/linghuchong/Downloads/51/Python/project/")

from PO.DataPO import *
Data_PO = DataPO()

from PO.FilePO import *
File_PO = FilePO()

from PO.HttpPO import *
Http_PO = HttpPO()

from PO.StrPO import *
Str_PO = StrPO()

from PO.WebPO import *
Web_PO = WebPO("chrome")

class DyPO:

	def getVideo(self, surl, toPath):

		header = {
			"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"}

		# 解析获取id
		share = re.search(r'/v.douyin.com/(.*?)/', surl).group(1)
		share_url = "https://v.douyin.com/{}/".format(share)
		# print(share_url)  # https://v.douyin.com/SrL7RnM/
		s_html = requests.get(url=share_url, headers=header)
		surl = s_html.url
		# print(surl) # https://www.douyin.com/video/7206155470149635384
		if len(surl) > 60:
			id = re.search(r'video/(\d.*)/', surl).group(1)
		else:
			id = re.search(r'video/(\d.*)', surl).group(1)
		# print(id) # 7206155470149635384


		# 获取json数据
		u_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?item_ids={}&a_bogus=".format(id)
		v_rs = requests.get(url=u_id, headers=header).json()
		# print(v_rs)

		# 作者名
		nickname = v_rs['item_list'][0]['author']['nickname']
		# print(nickname)

		# 视频标题
		titles = re.search(r'^(.*?)[；;。.#]', v_rs['item_list'][0]['desc']).group(1)
		# print(titles)

		# 创建video文件夹
		if not os.path.exists(toPath + nickname):
			os.makedirs(toPath + nickname)

		# 获取uri参数
		req = v_rs['item_list'][0]['video']['play_addr']['uri']
		# print("vvvvvv", req)

		# 下载无水印视频
		v_url = "https://www.douyin.com/aweme/v1/play/?video_id={}".format(req)
		v_req = requests.get(url=v_url, headers=header).content
		print(f"[下载中] => {v_url}")

		# 写入文件
		with open(f'{toPath}{nickname}/{titles}.mp4', 'wb') as f:
			f.write(v_req)

		print(f'[已完成] => {toPath}{nickname}/{titles}.mp4')
		return toPath + nickname

	def downVideo(self, url, toSave):

		'''
		1，下载单个抖音视频
		:param url = 'https://www.douyin.com/video/7157633339661307168'
		:param url = "https://v.douyin.com/hbjqhuT"
		'''


		headers = {
			"cookie":
				"s_v_web_id=verify_kwlyvfty_u4F0a4eC_HR0R_45qA_BGNr_tcfqSLkaFeIa; _"
				"tea_utm_cache_1300=undefined; __ac_nonce=061a6114700def9eb597f; __"
				"ac_signature=_02B4Z6wo00f01e59nzAAAIDAZTYE0lZHzxHuWZuAABo7n7oK78zhgb8Ol30kLigl-Pu9Q6sKyLpV-BQ3rbF1vLak-TtxN0ysQpQIX.VKlIbTkVBVA4rBt1JdylfNbrGz2NI4r4d7uQWMRa.r56; tt_scid=tbEntOkthFZL51883ve.2ORcwMNYlHUb6tegsnIzC9HSbV5u3J8ASl23x6S7wONy6e5e; "
			,
			# "user-agent": Http_PO.getUserAgent()
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

		}

		if 'https://v.douyin.com/' in url:
			url = url.split('https://v.douyin.com/')[1].split('复制此链接')[0]
			url = 'https://v.douyin.com/' + url
			# print(url)
		if 'https://www.douyin.com/' in url:
			url = url.split('https://www.douyin.com/')[1].split('复制此链接')[0]
			url = 'https://www.douyin.com/' + url
			# print(url)

		# 解析 https://v.douyin.com/hbjqhuT 成 https://www.douyin.com/video/7157633339661307168
		if 'https://v.douyin.com/' in url or 'https://www.douyin.com/' in url:

			r = Http_PO.getHtml(url)

			aweme_id = re.findall(r'video/(\w+-\w+-\w+|\w+-\w+|\w+)', r.url)  # ['6976835684271279400']
			# # print(aweme_id)
			url2 = 'https://www.douyin.com/video/' + aweme_id[0]
			print(url2)

			# url2 = 'https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7278475988445580596&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Chrome&browser_version=115.0.0.0&browser_online=true&engine_name=Blink&engine_version=115.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7224823478217967108&msToken=jEwTaPiZTXTuQjQqhzZBGBVBAiOC-GeoPnGAVdTYnH8LLNttKWbI2YaW8DAT6F1tWva59V8dQa-8OudnuyfB0Q4KfG4xhzC7wYHHd896_qHuwBPKT-OCiYg=&X-Bogus=DFSzswVOoobANry/tPRwAN7Tlqtx'
			# url2 = 'https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id=' + aweme_id[0]
			r = requests.get(url=url2, headers=headers)
			# print(r.text)
			# sys.exit(0)

			info = bs4.BeautifulSoup(r.text, 'lxml')
			js = str(info.select_one("script#RENDER_DATA"))  # 定位到<script id="RENDER_DATA" type="application/json">
			s_json = parse.unquote(js)  # 将 RENDER_DATA 解码成 json 文本
			# print(s_json)



			# 转换成json格式
			s_json = s_json.replace('<script id="RENDER_DATA" type="application/json">', '').replace('</script>', '')
			# print(s_json)
			d_json = json.loads(s_json)
			# print("1111111111111")
			print(d_json)

			from jsonpath import jsonpath
			# 用户名
			nickname = jsonpath(d_json, '$[*].aweme.detail.authorInfo.nickname')
			nickname = nickname[0]
			# nickname = "123"
			# print(nickname)

			# 标题
			title = jsonpath(d_json, '$[*].aweme.detail.desc')
			title = title[0]
			title = Str_PO.delSpecialChar(str(title), "，", "。", "#", "@")  # 优化文件名中不需要的字符
			if len(title) > 254:
				title = title[:250]
			# print(title)

			# 生成目录（# 用户名作为目录）
			File_PO.newLayerFolder(toSave + "/" + nickname)
			# folder = f'{toSave}/{nickname}'
			folder = toSave + "/" + nickname
			# print(folder)

			# 下载链接
			downUrl = jsonpath(d_json, '$[*].aweme.detail.video.playApi')
			downUrl = downUrl[0]
			downUrl = downUrl.replace("//", "https://")
			# print(downUrl)

			# print("[下载中] => " + url + " => " + url2 + " => " + downUrl)
			print("[下载中] => \n" + downUrl)

			r = Http_PO.getHtml(downUrl)
			# open(f'{folder}/{title}.mp4', 'wb').write(r.content)
			open(folder + '/' + title + '.mp4', 'wb').write(r.content)
			print('[已完成] => \n' + str(folder) + "/" + str(title) + ".mp4")

			return folder


	# # 输出结果['目录'，'标题','下载地址']
			# l_result = []
			# l_result.append(f)
			# # l_result.append((str(title).encode("utf-8").decode("utf-8")))
			# l_result.append(title)
			# l_result.append(downUrl)
			# # print(l_result)
			# print('[已完成] => ' + str(l_result).encode('gbk', 'ignore').decode('gbk'))




	def downVidoeList(self, url, toSave, *param):

		'''
		2，下载多个抖音(列表页)视频
		:param url:  https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg
		:param toSave:
		:return:
		'''

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
				# print("https://www.douyin.com" + a['href'])
				self.downVideo("https://www.douyin.com" + a['href'], toSave)


if __name__ == '__main__':

	Dy_PO = DyPO()

