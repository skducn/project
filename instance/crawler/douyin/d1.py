# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-12-27
# Description: 抖音视频下载
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# json在线解析 https://www.sojson.com/
# js在线解密 https://www.sojson.com/jsjiemi.html
# Python爬虫：用requests、json、bs4等模块轻轻松松抓取抖音视频的下载链接 https://zhuanlan.zhihu.com/p/442884562
# Python解码JS的encodeURIComponent并转化JSON https://blog.csdn.net/jeff06143132/article/details/124919764

# https://blog.csdn.net/m0_50860574/article/details/134040048
#***************************************************************

import re
import requests
import os

# 请求头
header = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"}


# 视频无水印
def videos(surl, toPath):
    share = re.search(r'/v.douyin.com/(.*?)/', surl).group(1)
    # print(share)
    # 请求链接
    share_url = "https://v.douyin.com/{}/".format(share)

    # print(share_url)
    s_html = requests.get(url=share_url, headers=header)
    # 获取重定向后的视频id
    surl = s_html.url
    # print(surl)

    # 获取video_id （重定向后的链接会变化具体我也没弄清楚就做了两种判断）
    if len(surl) > 60:
        id = re.search(r'video/(\d.*)/', surl).group(1)
        # print(id)
    else:
        id = re.search(r'video/(\d.*)', surl).group(1)
    # print(id)
    # 获取json数据
    u_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?item_ids={}&a_bogus=".format(id)
    v_rs = requests.get(url=u_id, headers=header).json()
    # print(v_rs)
    nickname = v_rs['item_list'][0]['author']['nickname']
    # print(nickname)
    # 截取文案
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
    # 写入文件
    with open(f'{toPath}{nickname}/{titles}.mp4', 'wb') as f:
        f.write(v_req)


# 图片无水印
def pics(surl):
    print('正在解析图片链接')
    # 获取id
    if len(surl) > 60:
        pid = re.search(r'note/(\d.*)/', surl).group(1)
    else:
        pid = re.search(r'note/(\d.*)', surl).group(1)
    # 获取json数据
    p_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?reflow_source=reflow_page&item_ids={}&a_bogus=".format(pid)
    # print(p_id)
    p_rs = requests.get(url=p_id, headers=header).json()
    # print(p_rs)
    # 拿到images下的原图片
    images = p_rs['item_list'][0]['images']
    # 获取文案
    ptitle = re.search(r'^(.*?)[；;。.#]', p_rs['item_list'][0]['desc']).group(1)
    # 创建pic文件夹
    if not os.path.exists('pic'):
        os.makedirs('pic')
    if not os.path.exists(f'pic/{ptitle}'):
        os.makedirs(f'pic/{ptitle}')
    print('正在下载无水印图片')
    # 下载无水印照片(遍历images下的数据)
    for i, im in enumerate(images):
        # 每一条数据下面都有四个原图链接这边用的是第一个
        p_req = requests.get(url=im['url_list'][0]).content
        # print(p_req)
        # 保存图片
        with open(f'pic/{ptitle}/{str(i + 1)}.jpg', 'wb') as f:
            f.write(p_req)


if __name__ == '__main__':
    # 抖音
    # shares = input("请输入分享链接并按下回车键：")
    # # 提取分享链接后面的链接
    # share = re.search(r'/v.douyin.com/(.*?)/', shares).group(1)
    # print(share)
    # # 请求链接
    # share_url = "https://v.douyin.com/{}/".format(share)
    #
    # print(share_url)
    # s_html = requests.get(url=share_url, headers=header)
    # # 获取重定向后的视频id
    # surl = s_html.url
    # print(surl)
    # 判断链接类型为视频分享类型
    videos("https://v.douyin.com/iRyQegTL/","/Users/linghuchong/Downloads/Video/douyin/")

    # if re.search(r'/video', surl) != None:
    #     videos("https://v.douyin.com/iRyQegTL/ ")
    #     quit = input('下载完成，按回车键退出程序。')
    # # 判断链接类型为图集分享类型
    # elif re.search(r'/note', surl) != None:
    #     pics(surl)
    #     quit = input('下载完成，按回车键退出程序。')
    # else:
    #     quit = input('解析失败，按回车键退出程序。')
