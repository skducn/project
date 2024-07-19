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

headers = {
			"cookie":
				"s_v_web_id=verify_kwlyvfty_u4F0a4eC_HR0R_45qA_BGNr_tcfqSLkaFeIa; _"
				"tea_utm_cache_1300=undefined; __ac_nonce=061a6114700def9eb597f; __"
				"ac_signature=_02B4Z6wo00f01e59nzAAAIDAZTYE0lZHzxHuWZuAABo7n7oK78zhgb8Ol30kLigl-Pu9Q6sKyLpV-BQ3rbF1vLak-TtxN0ysQpQIX.VKlIbTkVBVA4rBt1JdylfNbrGz2NI4r4d7uQWMRa.r56; tt_scid=tbEntOkthFZL51883ve.2ORcwMNYlHUb6tegsnIzC9HSbV5u3J8ASl23x6S7wONy6e5e; "
			,
			# "user-agent": Http_PO.getUserAgent()
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
		,'referer':'https://www.douyin.com/video/7282222164672122146'
		}

url2 = "https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7090476853860781349&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Chrome&browser_version=115.0.0.0&browser_online=true&engine_name=Blink&engine_version=115.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7224823478217967108&msToken=O6EKBamnejH7dsEdHK5dEHRjrdE6-6zbsUqhOPODC-hwYcsTAHpPPGlnfl0C06a6kaNU30KjRibDp0pOGKmOK6AmO9QHB21huZ_S_2fQSYFGa8Ru34lCBWc=&X-Bogus=DFSzswVORixANry/tO5VHp7Tlqeb"

url2 = "https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7282222164672122146&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Chrome&browser_version=115.0.0.0&browser_online=true&engine_name=Blink&engine_version=115.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7224823478217967108&msToken=Dua5xKoVNQJPp6vtqWI7nMCd_r8SdV4XbJ-fOXKi7QU_UdvZBNGjvgXrZMBAgVOgGQcphCSdUOeCmxOW39wpAdKr9XtUmmifo-i-71sKmYee34LBZFwSBlw=&X-Bogus=DFSzswVOWaGANry/tO2Zg37Tlqtb"
r = requests.get(url=url2, headers=headers)
print(r.text)



