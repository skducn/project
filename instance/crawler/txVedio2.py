# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-7-1
# Description: 下载腾讯视频(非vip)
# 参考：https://www.cnblogs.com/blogsxyz/p/12811236.html
# pip install moviepy　
# 获取视频地址方法，打开视频连接，F12切换到Application ,storage - local storage - https://v.qq.com - txp-playtime
# 视频的真实地址 保存session中, 通过 https://www.sojson.com/simple_json.html 在线解析json ,定位到 vurl 这就是真实地址。
#***************************************************************

import os
import sys
import requests
import datetime
from moviepy.editor import *


def LoadVideo(url, toSave):
    """
    腾讯视频下载
    :param url: 视频m3u8地址
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    download_path = toSave + "\download"
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    # 新建日期文件夹
    download_path = os.path.join(download_path, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    os.mkdir(download_path)
    # 获取第一层M3U8文件内容
    all_content = requests.get(url).text
    if "#EXTM3U" not in all_content:
        raise BaseException("非M3U8的链接")
    if "EXT-X-STREAM-INF" in all_content:  # 第一层
        file_line = all_content.split("\n")
        for line in file_line:
            if '.m3u8' in line:
                # 拼出第二层m3u8的URL
                url = url.rsplit("/", 1)[0] + "/" + line
                all_content = requests.get(url, headers=headers).text
    file_line = all_content.split("\n")
    file_index = 0
    for index, line in enumerate(file_line):  # 第二层
        if "#EXT-X-KEY" in line:  # 找解密Key
            method_pos = line.find("METHOD")
            comma_pos = line.find(",")
            method = line[method_pos:comma_pos].split('=')[1]
            uri_pos = line.find("URI")
            quotation_mark_pos = line.rfind('"')
            key_path = line[uri_pos:quotation_mark_pos].split('"')[1]
            key_url = url.rsplit("/", 1)[0] + "/" + key_path  # 拼出key解密密钥URL
            res = requests.get(key_url)
            key = res.content
        # 找ts地址并下载
        if "EXTINF" in line:
            unknow = False
            # 拼出ts片段的URL
            pd_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1]
            file_index = file_index + 1;
            res = requests.get(pd_url)
            c_fule_name = str(file_index)
            with open(os.path.join(download_path, c_fule_name + ".mp4"), 'ab') as file:
                file.write(res.content)
                file.flush()
    merge_file(download_path, toSave)


def merge_file(path, toSave):
    """拼接视频
    :param path: 相对路劲
    """
    # 定义一个数组
    video_list = []
    # 访问 video 文件夹 (假设视频都放在这里面)
    for root, dirs, files in os.walk(path):
        # 按文件名排序
        files.sort()
        # 遍历所有文件
        index = 0
        for key in range(1, len(files) + 1):
            for file in files:
                if os.path.splitext(file)[0] == str(key):
                    # 拼接成完整路径
                    file_path = os.path.join(root, file)
                    # 载入视频
                    video = VideoFileClip(file_path)
                    # 添加到数组
                    video_list.append(video)
                else:
                    continue

    # 拼接视频
    final_clip = concatenate_videoclips(video_list)
    # 生成目标视频文件
    video_path = toSave
    if not os.path.exists(video_path):
        os.mkdir(video_path)
    video_path += datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.mp4'
    final_clip.to_videofile(video_path, fps=24, remove_temp=False)


if __name__ == '__main__':
    url = 'https://apd-aa8b6f923fc059e32e3558830ae24174.v.smtcdns.com/omts.tc.qq.com/AAL4r6Nhf93UXs88sVR5SrmlAQq2LKMvPxxVLL4a8MVI/uwMROfz2r57CIaQXGdGnC2dXOm6xTkXGF_gkBTC2AZ_Tpjhx/svp_50069/6fbWHgKblkRyfP-AbH9ns8Zq4DmuOZW5ibkj2cYrfQK0xaB2I-1T4SFWZKv1P8h89A--9Z6B0qOOVxBtG27eZzpMjyrXQfDh26EImxwrD0NWwLzWb2VOpsp4OF-o3sQszLeNmSDwVcpnkxct-y73pEQuwXEw0oZ3q0r2WFLw8Y5PgpusTWyx-g/gzc_1000035_0bc3eibhqaac4yafpdmqmvqjoiwdparae6ca.f304110.ts.m3u8?ver=4'
    LoadVideo(url, "d:\\3\\")

    # video=VideoFileClip("./download/20200416_140017/1.mp4")
    # videoClip = video.subclip(7,)
    # videoClip.to_videofile("./download/20200416_140017/01.mp4", fps=20)#输出文件