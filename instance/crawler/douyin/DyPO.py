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

# from PO.DataPO import *
# Data_PO = DataPO()
#
# from PO.FilePO import *
# File_PO = FilePO()
#
# from PO.HttpPO import *
# Http_PO = HttpPO()
#
# from PO.StrPO import *
# Str_PO = StrPO()

# from PO.WebPO import *
# Web_PO = WebPO("chrome")

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
		# print(surl) # https://www.douyin.com/video/7316708968867401014
		if len(surl) > 60:
			id = re.search(r'video/(\d.*)/', surl).group(1)
		else:
			id = re.search(r'video/(\d.*)', surl).group(1)
		# print(id) # 7206155470149635384

		#

		# 获取json数据
		u_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?item_ids={}&a_bogus=".format(id)
		# u_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?reflow_source=reflow_page&item_ids={}&a_bogus=".format(id)

		print(u_id)
		v_rs = requests.get(url=u_id, headers=header)
		print(v_rs.json())
		sys.exit(0)
		# v_rs = requests.get(url=u_id, headers=header).json()
		# print(0,v_rs)

		# 作者名
		nickname = v_rs['item_list'][0]['author']['nickname']

		nickname = str(nickname).replace(" ", "_")
		print(1, nickname)

		# 视频标题
		titles = v_rs['item_list'][0]['desc']
		# print(3, v_rs['item_list'][0]['desc'])
		# titles = re.search(r'^(.*?)[；;。.#]', v_rs['item_list'][0]['desc'])
		# titles = re.search(r'^(.*?)[；;。.#]', v_rs['item_list'][0]['desc']).group(1)
		# if titles == None:
		# 	titles = nickname
		# else:
		# 	titles = v_rs['item_list'][0]['desc']
		# 	titles = re.search(r'^(.*?)[；;。.#]', v_rs['item_list'][0]['desc']).group(1)
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
		# print(v_url)
		print("下载中 ", v_url)
		# print(f"[下载中] => {v_url}")

		ff = toPath + nickname + "/" + titles + ".mp4"
		print(ff)

		# 写入文件
		with open(ff, 'wb') as f:
			f.write(v_req)

		print("[已完成] => ", ff)
		return toPath + nickname

	def getVideo2(self, surl, savePath):

		# 通过页面获取cookie（detail/？aweme_id=1644267442269561330）
		headers = {
			"cookie":
				"device_web_cpu_core=4; device_web_memory_size=8; __ac_nonce=065f3c1fa00bef1423f6; __ac_signature=_02B4Z6wo00f01yzcAJQAAIDCwvnEaoav5Nss.AQAAK7P9a; ttwid=1%7Cza3a0V9sZWVXQtFTYdg1tIYDQdKPXBCospMJtQBpJ28%7C1710473722%7C6aa9c4a695b158cfd9b251ef3152973d2c837476f809a67a376ebcccac4af056; csrf_session_id=6eaea5441cfead14775b47ceeacc531b; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; strategyABtestKey=%221710473724.647%22; passport_csrf_token=4de2dc6072fe1d0815862fb2675f0dc9; passport_csrf_token_default=4de2dc6072fe1d0815862fb2675f0dc9; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A1%7D; bd_ticket_guard_client_web_domain=2; ttcid=4518e71687614734b864141d15a00c0131; passport_assist_user=CjzIA27dVWnLf-9XbxwQESh4-y5q99AGtFnYJ2s24LrdfBIvOKTw6Y-VBQfVTqKrRscimoI0zTcA24xkYhoaSgo8srCHn7pW6sbKU1V6TQdQvMsQQp6FVbzfhX0aFPnn2Qy9ao8EfuoHmC3h85yZ1xZfxmkFAU9YPVEDUKFIEML8yw0Yia_WVCABIgEDbbeZjw%3D%3D; n_mh=WS535DN4ran5MY8jwy5rsPR32VTkVf71wiCo9CkZcUk; sso_uid_tt=883ae607e15aeed291f994a1aaffcfee; sso_uid_tt_ss=883ae607e15aeed291f994a1aaffcfee; toutiao_sso_user=1c4588c6e810a350e5646a7f4e98d4ab; toutiao_sso_user_ss=1c4588c6e810a350e5646a7f4e98d4ab; sid_ucp_sso_v1=1.0.0-KDBkZDU2OTkwNWNhMzhhODIwMzEzZjNjNWE2ZTExYTc5ODcyZTkxYTkKHQi-qf6o8AIQsYTPrwYY7zEgDDDyqITYBTgGQPQHGgJobCIgMWM0NTg4YzZlODEwYTM1MGU1NjQ2YTdmNGU5OGQ0YWI; ssid_ucp_sso_v1=1.0.0-KDBkZDU2OTkwNWNhMzhhODIwMzEzZjNjNWE2ZTExYTc5ODcyZTkxYTkKHQi-qf6o8AIQsYTPrwYY7zEgDDDyqITYBTgGQPQHGgJobCIgMWM0NTg4YzZlODEwYTM1MGU1NjQ2YTdmNGU5OGQ0YWI; passport_auth_status=a408ba0374e4cb9afaf790166e8accc2%2C; passport_auth_status_ss=a408ba0374e4cb9afaf790166e8accc2%2C; uid_tt=5f908ea1b85221f0c2344c01ecc7e059; uid_tt_ss=5f908ea1b85221f0c2344c01ecc7e059; sid_tt=f4e64b8da5fe064138ac91e75911983e; sessionid=f4e64b8da5fe064138ac91e75911983e; sessionid_ss=f4e64b8da5fe064138ac91e75911983e; publish_badge_show_info=%220%2C0%2C0%2C1710473783357%22; LOGIN_STATUS=1; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=52e0d429df3a993303254e0224e054d0; __security_server_data_status=1; store-region=cn-sh; store-region-src=uid; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQ2trRjBXRUZhbkc4Z0Uzb3RoWHg4U3BFRE1qZUE0SVhUT2taVWFzSXF5N01DeW9TZFZxaEphaDNkUmRhSGFMMG1UT3VtUG1uZ2dBYmJDQi92azdGY0k9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; s_v_web_id=verify_lts3xhn6_tFhdD6mT_lVW3_4CEF_8TlA_LMEx6N3nIgO8; odin_tt=6bf7c94a6ce315b8b205796959e309edb6bf14135c801c7cb899c2470d4e1e003b39150696b1c8a6e5214408c6f42468; tt_scid=jaej88AxToHVzUSQXWDmNZziaZjc-evJLkLV6-MmY32zyh1TdIOtzrkjhERK.aQnec5d; d_ticket=c20707798d78785d2d8289658bd4806d5170f; sid_guard=f4e64b8da5fe064138ac91e75911983e%7C1710473803%7C5183978%7CTue%2C+14-May-2024+03%3A36%3A21+GMT; sid_ucp_v1=1.0.0-KGZlZGIyZTRlNmZkNGFkZDVjNDI4NDUwMTBiYTZjZDQwNGUxMmNiODMKGQi-qf6o8AIQy4TPrwYY7zEgDDgGQPQHSAQaAmxxIiBmNGU2NGI4ZGE1ZmUwNjQxMzhhYzkxZTc1OTExOTgzZQ; ssid_ucp_v1=1.0.0-KGZlZGIyZTRlNmZkNGFkZDVjNDI4NDUwMTBiYTZjZDQwNGUxMmNiODMKGQi-qf6o8AIQy4TPrwYY7zEgDDgGQPQHSAQaAmxxIiBmNGU2NGI4ZGE1ZmUwNjQxMzhhYzkxZTc1OTExOTgzZQ; msToken=Ew0cZ5gFbhaYNOu--GqDqFAgXKLFR2XnZBrJcujKcL1GcIFCeiU06MmEue3oI30p4B0UvWyv38Hc2kKCwUW77RLJqjWw2vrXk8bYNy0Z0lE6ZFkFnA2IWkXr6b4=; download_guide=%221%2F20240315%2F0%22; pwa2=%220%7C0%7C1%7C0%22; GlobalGuideTimes=%221710474233%7C1%22; msToken=gIX3RDGb5D1WOsUR5bZYG3qnp56Spn8JmJBaNmjRDobe5ZJHvlK7cCI2JiFKfBf6KndEslouBIViqmzljDA18w5zDLoDTcPSD9F5snaSMt2XuGSkl3ZbfrQ=; passport_fe_beating_status=false; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A1%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; dy_swidth=1440; dy_sheight=900; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1440%2C%5C%22screen_height%5C%22%3A900%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAq9Lx60wscsSvp16gH6RYWZ3iyAngdi9YT0tgCXBbkQc%2F1710518400000%2F0%2F0%2F1710475404147%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAq9Lx60wscsSvp16gH6RYWZ3iyAngdi9YT0tgCXBbkQc%2F1710518400000%2F0%2F1710474804148%2F0%22",
				'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
		}

		# 获取id
		if "https://www.douyin.com/video/" not in surl:

			share = re.search(r'/v.douyin.com/(.*?)/', surl).group(1)
			share_url = "https://v.douyin.com/{}/".format(share)
			s_html = requests.get(url=share_url, headers=headers)
			surl = s_html.url
			# print(surl)  # https://www.douyin.com/video/7345754203735756069?previous_page=web_code_link
		id = surl.split("https://www.douyin.com/video/")[1].split("?")[0]
		# print(id)  # 7345754203735756069


		# 获取视频地址
		# 解析
		url = "https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={}".format(id)
		v_rs = requests.get(url=url, headers=headers).json()
		# print(v_rs)
		# 获取地址
		v_url = v_rs['aweme_detail']['video']['download_addr']['url_list'][0]
		# v_url = v_rs['aweme_detail']['video']['download_addr']['url_list'][3]
		# print(v_url)

		# 昵称（目录）
		v_nickname = v_rs['aweme_detail']['author']['nickname']
		# print(v_nickname)
		v_nickname = str(v_nickname).replace(" ", "_")

		# 视频标题
		v_desc = v_rs['aweme_detail']['desc']
		# print(v_desc)
		# title = re.search(r'^(.*?)[；;。.#]', v_desc).group(0)
		# print(title)
		# title = re.search(r'^(.*?)[；;。.#]', v_desc).group(1)
		# print(title)

		# 3 下载视频
		result = self.downVideo(v_url, v_nickname, v_desc, savePath)
		return result


	def downVideo(self, v_url, v_folder, v_title,  savePath):
		'''
		1，下载单个抖音视频
		:param url = 'https://www.douyin.com/video/7157633339661307168'
		:param url = "https://v.douyin.com/hbjqhuT"
		'''
		# 创建video文件夹
		if not os.path.exists(savePath + v_folder):
			os.makedirs(savePath + v_folder)

		print("下载 => ", v_url)

		# 存放路径
		ff = savePath + v_folder + "/" + v_title + ".mp4"
		# print(ff)

		# 写入文件
		res = requests.get(v_url)
		with open(ff, "wb") as f:
			f.write(res.content)

		print("[已完成] => ", ff)
		return savePath + v_folder




	# def downVideo(self, url, toSave):
	#
	# 	'''
	# 	1，下载单个抖音视频
	# 	:param url = 'https://www.douyin.com/video/7157633339661307168'
	# 	:param url = "https://v.douyin.com/hbjqhuT"
	# 	'''
	#
	#
	# 	headers = {
	# 		"cookie":
	# 			"s_v_web_id=verify_kwlyvfty_u4F0a4eC_HR0R_45qA_BGNr_tcfqSLkaFeIa; _"
	# 			"tea_utm_cache_1300=undefined; __ac_nonce=061a6114700def9eb597f; __"
	# 			"ac_signature=_02B4Z6wo00f01e59nzAAAIDAZTYE0lZHzxHuWZuAABo7n7oK78zhgb8Ol30kLigl-Pu9Q6sKyLpV-BQ3rbF1vLak-TtxN0ysQpQIX.VKlIbTkVBVA4rBt1JdylfNbrGz2NI4r4d7uQWMRa.r56; tt_scid=tbEntOkthFZL51883ve.2ORcwMNYlHUb6tegsnIzC9HSbV5u3J8ASl23x6S7wONy6e5e; "
	# 		,
	# 		# "user-agent": Http_PO.getUserAgent()
	# 		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
	#
	# 	}
	#
	# 	if 'https://v.douyin.com/' in url:
	# 		url = url.split('https://v.douyin.com/')[1].split('复制此链接')[0]
	# 		url = 'https://v.douyin.com/' + url
	# 		# print(url)
	# 	if 'https://www.douyin.com/' in url:
	# 		url = url.split('https://www.douyin.com/')[1].split('复制此链接')[0]
	# 		url = 'https://www.douyin.com/' + url
	# 		# print(url)
	#
	# 	# 解析 https://v.douyin.com/hbjqhuT 成 https://www.douyin.com/video/7157633339661307168
	# 	if 'https://v.douyin.com/' in url or 'https://www.douyin.com/' in url:
	#
	# 		r = Http_PO.getHtml(url)
	#
	# 		aweme_id = re.findall(r'video/(\w+-\w+-\w+|\w+-\w+|\w+)', r.url)  # ['6976835684271279400']
	# 		# # print(aweme_id)
	# 		url2 = 'https://www.douyin.com/video/' + aweme_id[0]
	# 		print(url2)
	#
	# 		# url2 = 'https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7278475988445580596&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Chrome&browser_version=115.0.0.0&browser_online=true&engine_name=Blink&engine_version=115.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7224823478217967108&msToken=jEwTaPiZTXTuQjQqhzZBGBVBAiOC-GeoPnGAVdTYnH8LLNttKWbI2YaW8DAT6F1tWva59V8dQa-8OudnuyfB0Q4KfG4xhzC7wYHHd896_qHuwBPKT-OCiYg=&X-Bogus=DFSzswVOoobANry/tPRwAN7Tlqtx'
	# 		# url2 = 'https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id=' + aweme_id[0]
	# 		r = requests.get(url=url2, headers=headers)
	# 		# print(r.text)
	# 		# sys.exit(0)
	#
	# 		info = bs4.BeautifulSoup(r.text, 'lxml')
	# 		js = str(info.select_one("script#RENDER_DATA"))  # 定位到<script id="RENDER_DATA" type="application/json">
	# 		s_json = parse.unquote(js)  # 将 RENDER_DATA 解码成 json 文本
	# 		# print(s_json)
	#
	#
	#
	# 		# 转换成json格式
	# 		s_json = s_json.replace('<script id="RENDER_DATA" type="application/json">', '').replace('</script>', '')
	# 		# print(s_json)
	# 		d_json = json.loads(s_json)
	# 		# print("1111111111111")
	# 		print(d_json)
	#
	# 		from jsonpath import jsonpath
	# 		# 用户名
	# 		nickname = jsonpath(d_json, '$[*].aweme.detail.authorInfo.nickname')
	# 		nickname = nickname[0]
	# 		# nickname = "123"
	# 		# print(nickname)
	#
	# 		# 标题
	# 		title = jsonpath(d_json, '$[*].aweme.detail.desc')
	# 		title = title[0]
	# 		title = Str_PO.delSpecialChar(str(title), "，", "。", "#", "@")  # 优化文件名中不需要的字符
	# 		if len(title) > 254:
	# 			title = title[:250]
	# 		# print(title)
	#
	# 		# 生成目录（# 用户名作为目录）
	# 		File_PO.newLayerFolder(toSave + "/" + nickname)
	# 		# folder = f'{toSave}/{nickname}'
	# 		folder = toSave + "/" + nickname
	# 		# print(folder)
	#
	# 		# 下载链接
	# 		downUrl = jsonpath(d_json, '$[*].aweme.detail.video.playApi')
	# 		downUrl = downUrl[0]
	# 		downUrl = downUrl.replace("//", "https://")
	# 		# print(downUrl)
	#
	# 		# print("[下载中] => " + url + " => " + url2 + " => " + downUrl)
	# 		print("[下载中] => \n" + downUrl)
	#
	# 		r = Http_PO.getHtml(downUrl)
	# 		# open(f'{folder}/{title}.mp4', 'wb').write(r.content)
	# 		open(folder + '/' + title + '.mp4', 'wb').write(r.content)
	# 		print('[已完成] => \n' + str(folder) + "/" + str(title) + ".mp4")
	#
	# 		return folder


	# # 输出结果['目录'，'标题','下载地址']
			# l_result = []
			# l_result.append(f)
			# # l_result.append((str(title).encode("utf-8").decode("utf-8")))
			# l_result.append(title)
			# l_result.append(downUrl)
			# # print(l_result)
			# print('[已完成] => ' + str(l_result).encode('gbk', 'ignore').decode('gbk'))




	# def downVidoeList(self, url, toSave, *param):
	#
	# 	'''
	# 	2，下载多个抖音(列表页)视频
	# 	:param url:  https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg
	# 	:param toSave:
	# 	:return:
	# 	'''
	#
	# 	print("[待下载列表页] => " + url)
	#
	# 	# 使用selenium解析动态html
	# 	# 参考：https://blog.csdn.net/weixin_44259720/article/details/127075628
	# 	Web_PO.openURL(url)
	# 	qty = Web_PO.pageDown('Eie04v01')
	# 	# print(qty)
	#
	# 	text = Web_PO.driver.page_source
	# 	text = bs4.BeautifulSoup(text, 'lxml')
	# 	link = text.find(class_='EZC0YBrG').find_all('a')
	# 	sign = 0
	# 	for a in link:
	# 		if len(param) == 2:
	# 			vid = "/video/" + str(param[1])
	# 			# 下载vid之后（即最新）
	# 			if param[0] == 'a':
	# 				if vid != a['href']:
	# 					# print("https://www.douyin.com" + a['href'])
	# 					self.downVideo("https://www.douyin.com" + a['href'], toSave)
	# 				else:
	# 					break
	# 			# 下载vid之前（即最旧）
	# 			if param[0] == 'b':
	# 				if vid == a['href']:
	# 					sign = 1
	# 				if sign == 1:
	# 					# print("https://www.douyin.com" + a['href'])
	# 					self.downVideo("https://www.douyin.com" + a['href'], toSave)
	#
	# 		else:
	# 			# 下载所有
	# 			# print("https://www.douyin.com" + a['href'])
	# 			self.downVideo("https://www.douyin.com" + a['href'], toSave)


if __name__ == '__main__':

	Dy_PO = DyPO()

