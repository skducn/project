# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-12-28
# Description: bilibili视频下载

# 过滤掉非法的多字节序列问题
# b = "型➕换季收纳法🔥叠衣"
# print(b.encode('gbk', 'ignore').decode('gbk') )   # 型换季收纳法叠衣

# json在线解析 https://www.sojson.com/
# js在线解密 https://www.sojson.com/jsjiemi.html
# 5分钟学会用python爬取b站视频 https://www.bilibili.com/read/cv16789932/
#***************************************************************

import sys, subprocess, json
sys.path.append("../../../")

from PO.FilePO import *
File_PO = FilePO()

from PO.HttpPO import *
Html_PO = HttpPO()

from bs4 import BeautifulSoup


class BilibiliPO:

	def downVideo(self, url):

		bvideoHTML = requests.get(url)
		values = bvideoHTML.text
		text = BeautifulSoup(values, features='lxml')
		sleep(1)
		# print(text)

		# 用户名
		# username = text.find_all('h1', 'title')
		# print(username)
		# username = str(username).replace(" ", "").replace("\n", "")

		# 视频名
		title = text.find('title').contents[0].replace(' ', '').replace('_哔哩哔哩_bilibili', '')
		# print(title)
		print(f"[待下载] => {url} => {title}")

		items = text.find_all('script')[3]
		# print(items)
		items = items.contents[0].replace('window.__playinfo__=', '')
		# print(items)
		obj = json.loads(items)
		videoUrl = obj["data"]["dash"]["video"][0]["baseUrl"]
		audioUrl = obj["data"]["dash"]["audio"][0]["baseUrl"]

		# # 生成目录（# 用户名作为目录）
		# File_PO.newLayerFolder(toSave + "/" + username)
		# folder = f'{toSave}/{username}'

		# 生成临时音频和视频文件
		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
			'Referer': url
		}
		with open(f'{title}.mp4', 'wb') as video:
			video.write(requests.get(videoUrl, headers=headers).content)
		with open(f'{title}.mp3', 'wb') as audio:
			audio.write(requests.get(audioUrl, headers=headers).content)
		mp4_file = f'{title}.mp4'
		file_name = f'{title}.mp3'

		# 合成MP4并删除临时文件，参数-loglevel quiet 不输出ffmpeg合成信息。
		cmd = f'ffmpeg -loglevel quiet -y -i {mp4_file} -i {file_name} -acodec copy -vcodec copy {title}_1.mp4'
		subprocess.call(cmd, shell=True)
		os.remove(mp4_file)
		os.remove(file_name)

		print(f'[已完成] => {title}_1.mp4')


if __name__ == '__main__':

	Bilibili_PO = BilibiliPO()

