# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: 抖音视频下载（单个，多个（获取抖音视频用户列表进行批量下载））
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# 参数哈 click（）， 参考：https://blog.csdn.net/weixin_33506900/article/details/112187887
#***************************************************************

import requests, re, os, platform
import click

# todo :download douyin
def getVideoList(url, varFromNumDown=0):

	# varFromNumDown 表示从第几视频开始下载  如：100表示从第100个开始下载，之前视频忽略。
	session = requests.session()
	headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
	sum_url = ""

	# 分享链接返回url 获取sec_uid
	res = session.get(url=url, headers=headers)
	seu_udi = re.findall(r'sec_uid=(\w+-\w+-\w+|\w+-\w+|\w+)', res.url)

	# 获取视频数量总数  用户名
	sum_url = 'https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={0}'.format(seu_udi[0])
	# print(sum_url)  # https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=MS4wLjABAAAA641dgYSbDRfR9YDDe3ve46BGVqE0doMTy0uDK10CYBw
	se = session.get(sum_url)

	# 用户名
	nickname = re.findall('"nickname":"(.+?)"', se.text)
	print("用户名：%s" % nickname[0])

	# 抖音号
	unique_id = re.findall('"unique_id":"(.+?)"', se.text)
	print("抖音号：%s" % unique_id[0])

	# 视频数
	sm_count = re.findall('"aweme_count":(\w+)', se.text)
	print("视频数：%s" % sm_count[0])

	# 下载目录
	print("下载目录：d:\\%s" % nickname[0])

	# # 粉丝数量
	# fensi = re.findall('"follower_count":(\w+)', se.text)
	# print("粉丝数量:%s" % fensi[0])
	#
	# # 关注数
	# guanzhu = re.findall('"following_count":(\w+)', se.text)
	# print("本人关注:%s" % guanzhu[0])

	max_cursor = 0
	id = 0
	list1 = []

	while True:
		while True:
			if (max_cursor == 0):
				sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=21&max_cursor=0&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(seu_udi[0])
			else:
				sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=21&max_cursor={1}&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(seu_udi[0], max_cursor)

			sec_respone = session.get(url=sec_id_url, headers=headers)
			comment = sec_respone.json()
			if (len(comment['aweme_list']) == 0):
				continue
			else:
				break

		# 下一页下标
		max_cursor = comment['max_cursor']
		list1.append(max_cursor)

		url = []
		for s in comment['aweme_list']:
			id += 1

			# 视频名称
			text = s['desc']
			# # 点赞数
			# dianzan = s['statistics']["digg_count"]
			# # 评论数
			# pinglun = s['statistics']["comment_count"]
			# # 分享数
			# fenxiang = s['statistics']["share_count"]
			# 无水印视频链接地址
			video_url = s['video']['play_addr_lowbr']['url_list'][0]
			text = re.sub("(\#\w+)|(\@\w+)", '', text)

			# 视频文件优化，自动去除特殊符合，如?
			if "?" in str(text):
				text = str(text).replace("?", "")

			if id >= int(varFromNumDown):
				# print(str(id) + "、视频名称为：{0},点赞数为:{1},评论数为:{2},分享数量为:{3},视频无水印地址为：{4}".format(text, str(dianzan), str(pinglun),str(fenxiang), video_url))
				print(str(id) + "，{0} {1}".format(text, video_url))
				ir = session.get(video_url, headers=headers)

				if platform.system() == 'Darwin':
					# 下载（for mac）
					# 新建用户目录及视频
					if not os.path.exists("/Users/linghuchong/Downloads/" + nickname[0]):
						os.mkdir("/Users/linghuchong/Downloads/" + nickname[0])
					open(f'/Users/linghuchong/Downloads/{nickname[0]}/{text}.mp4', 'wb').write(ir.content)
				if platform.system() == 'Windows':
					# 下载（for windows）
					# 新建用户目录及视频
					if not os.path.exists("d:/video/" + nickname[0]):
						os.mkdir("d:/video/" + nickname[0])
					open(f'd:/video/{nickname[0]}/{text}.mp4', 'wb').write(ir.content)
			else:
				print(str(id) + "，{0}".format(text))

		if(int(id) == int(sm_count[0])):
			break


@click.command()
@click.option('-u',"--url", help='url地址')
@click.option("-s", '--save', help='保存路径')
def getVideoOne(url, save):

	print(url)
	print(save)
	# session = requests.session()
	# headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
	#
	# # 解析url
	# res = session.get(url=url, headers=headers)
	# video = re.findall(r'video/(\w+-\w+-\w+|\w+-\w+|\w+)', res.url)   # 如：video_id=6912637146767674636
	#
	# # 解析url1
	# url1 = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + video[0]
	# res1 = requests.get(url=url1, headers=headers)
	# # print(res1.text)
	# video_id = re.findall(r'/?video_id=(\w+)', res1.text)   # 如：video_id=v0300f3d0000bvn9r1prh6u8gbdusbdg
	# nickname = re.findall('"share_title":"(.+?)"', res1.text)  # 视频标题
	#
	# # 视频文件优化，自动去除特殊符合，如?
	# if "?" in str(nickname[0]):
	# 	nickname = str(nickname[0]).replace("?", "")
	#
	# # 下载
	# ir = session.get("https://aweme.snssdk.com/aweme/v1/playwm/?video_id=" + video_id[0] +"&ratio=720p&line=0", headers=headers)
	# open(f'{save}/{nickname}.mp4', 'wb').write(ir.content)
	# print("已下载到本地：" + str(save) + "\%s.mp4" % nickname[0])


if __name__ == '__main__':

	# getVideoList("https://v.douyin.com/Jp4GEo6/")  # 走遍中国5A景区-大龙 抖音列表

	getVideoOne()  # 单个抖音链接
	# cmd 命令：python dy.py -u "https://v.douyin.com/eFW2VfN/" -s d:\1


