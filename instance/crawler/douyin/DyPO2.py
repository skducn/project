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


	def downVideo(self, url, toSave):

		'''
		1，下载单个抖音视频
		:param url = 'https://www.douyin.com/video/7157633339661307168'
		:param url = "https://v.douyin.com/hbjqhuT"
		'''



		headers = {

			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
			, 'content-type': 'text/html'
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

			cookies = {
					"s_v_web_id":"verify_lkjg6awo_grfeTvCk_en3Z_47uP_9yVA_s9QBoi2jm8a0",
					"__ac_signature":"_02B4Z6wo00f01cMcEIQAAIDCV8pLisf6.xHDPBQAABXGsTLr4DVt7vcW3yFw-TMiPB17ze53sv7KU7t5lvt1WiB3LQNkdq09NX6z18eevQRXyKf9pBNPBinFiN.d8fukY0Jzq77jODesgCdb6d",
					"tt_scid":"Y1zjC72QisNkt6-xVbVfYBDfiZwCjr53jPoapz0u7uZTvI5YyeC2Us2EqDKKP5ZQ60f1"			}


			url2 = 'https://www.douyin.com/video/7278586466165411084'
			print(url2)

			session = requests.Session()
			requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
			cookies = session.cookies.get_dict()
			# sys.exit(0)

			res = session.get(url=url2, headers=headers, cookies=cookies)
			headers3 = res.headers
			# headers3['user-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
			# headers3['referer'] = 'https://www.douyin.com/video/7278586466165411084'
			# headers3['Connection'] = 'close'
			# print(headers3)
			# print(res.cookies)
			# print(res.text)
			for header in headers:
				print(header, headers[header])
			cookies1 = res.cookies.get_dict()
			print(cookies1)
			print(cookies)
			cookies['__ac_nonce'] = cookies1['__ac_nonce']
			print(cookies)
			# cookie = session.cookies.get_dict()
			# print(cookies)
			# # print(res.text)
			# r = requests.get(url=url2, headers=headers2)
			# print(r.text)

			# url2 = 'https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7278475988445580596&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Chrome&browser_version=115.0.0.0&browser_online=true&engine_name=Blink&engine_version=115.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7224823478217967108&msToken=jEwTaPiZTXTuQjQqhzZBGBVBAiOC-GeoPnGAVdTYnH8LLNttKWbI2YaW8DAT6F1tWva59V8dQa-8OudnuyfB0Q4KfG4xhzC7wYHHd896_qHuwBPKT-OCiYg=&X-Bogus=DFSzswVOoobANry/tPRwAN7Tlqtx'
			# url3 = 'https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7278586466165411084&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Chrome&browser_version=115.0.0.0&browser_online=true&engine_name=Blink&engine_version=115.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7224823478217967108&msToken=uAg9cjgukVs9CfQZ_VQhUgvS6iqF69Ps1-HX3rfDdsNI0P-Pqee8HLoi_iYAHLR4NXGJrkadMjLi78ckAcLJCxW-CfxR7ASNGtgWJOJUPr4lQEN7svRsC6k=&X-Bogus=DFSzswVYLnUANHqMtPUEJN7Tlqtc'
			url3 = 'https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id=7278586466165411084'
			# url3 = 'https://www.iesdouyin.com/aweme/v1/web/aweme/detail/?aweme_id=7278586466165411084'
			# r = session.get(url=url3, headers=headers3, cookies=cookies)

			headers1 = {
				"cookie":
					'__ac_signatur=_02B4Z6wo00f01cMcEIQAAIDCV8pLisf6.xHDPBQAABXGsTLr4DVt7vcW3yFw-TMiPB17ze53sv7KU7t5lvt1WiB3LQNkdq09NX6z18eevQRXyKf9pBNPBinFiN.d8fukY0Jzq77jODesgCdb6d;s_v_web_id=verify_lkjg6awo_grfeTvCk_en3Z_47uP_9yVA_s9QBoi2jm8a0;tt_scid=Y1zjC72QisNkt6-xVbVfYBDfiZwCjr53jPoapz0u7uZTvI5YyeC2Us2EqDKKP5ZQ60f1',
				'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
			,'referer':'https://www.douyin.com/video/7278586466165411084'
				,'content-type':'application/json'
			}

			headers4 = {

				'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
				, 'referer': 'https://www.douyin.com/video/7278586466165411084'
				, 'content-type': 'application/json'
			}

			r = session.get(url=url3, headers=headers4,cookies=cookies)
			print(r.content)

			sys.exit(0)
			info = bs4.BeautifulSoup(r.text, 'lxml')
			js = str(info.select_one("script#RENDER_DATA"))  # 定位到<script id="RENDER_DATA" type="application/json">
			s_json = parse.unquote(js)  # 将 RENDER_DATA 解码成 json 文本
			print(s_json)



			# 转换成json格式
			s_json = s_json.replace('<script id="RENDER_DATA" type="application/json">', '').replace('</script>', '')
			# print(s_json)
			d_json = json.loads(s_json)
			# print("1111111111111")
			# print(d_json)

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

