# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: mm131
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# https://mmapi3.mcxxkjs.cn:2443
# https://mmres-cdn.jiefeixinxij.top/back/20220517/a34ee5ec7314f712bdb087aeec06f478.jpg
# curl -H "Host: mmapi3.mcxxkjs.cn:2443"
# -H "accept: */*"
# -H "channel: AS_1"
# -H "api_version: v20"
# -H "accept-language: zh-Hans-CN;q=1"
# -H "client_version: 1.0.1"
# -H "token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjE0MDgyMjE0NTYyLCJyYW5kb20iOjE1OTg5NzAyMDI3MTQsImxvZ2luX3R5cGUiOjJ9.u8z0ABQc_4vxON-9ddNj6kGCs2EVBK02Vfge2kbV1cc"
# -H "applicationid: 102"
# -H "did: 2FA99489-2B04-4EE8-BC2D-73D8FF3256CB"
# -H "appkey: BDC628A72BF854F2"
# -H "user-agent: mm131/1.0.1 (iPhone; iOS 15.0.2; Scale/3.00)"
# -H "sign: EB784E13C01A7334999E7046FD5FC8F4"
# --compressed "https://mmapi3.mcxxkjs.cn:2443/mm131/getCollectionList?collectionType=0&lastIndex=-1"
#***************************************************************

from PO.NetPO import *
Net_PO = NetPO()
import requests, json


# url = "https://mmapi3.mcxxkjs.cn:2443/mm131/getCollectionList?collectionType=3&lastIndex=5579"
# header = {
# "accept": "*/*" ,
# "channel": "AS_1",
# "api_version": "v20",
# "accept-language": "zh-Hans-CN;q=1",
# "client_version": "1.0.1",
# "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjE0MDgyMjE0NTYyLCJyYW5kb20iOjE1OTg5NzAyMDI3MTQsImxvZ2luX3R5cGUiOjJ9.u8z0ABQc_4vxON-9ddNj6kGCs2EVBK02Vfge2kbV1cc",
# "applicationid": "102",
# "did": "2FA99489-2B04-4EE8-BC2D-73D8FF3256CB",
# "appkey": "BDC628A72BF854F2",
# "user-agent": "mm131/1.0.1 (iPhone; iOS 15.0.2; Scale/3.00)",
# "sign": "1F454D5C98869EA8A67858965791384C"
# }
# r = requests.get(url=url, headers=header)
# rr = json.loads(r.text)
# # print(rr)
# # print(rr['dataObj']['picDetail'][0]['pic_url'])
# # print(rr['dataObj']['picDetail'][1]['pic_url'])
# for i in range(len(rr['dataObj']['picDetail'])):
#     print("https://mmres-cdn.jiefeixinxij.top" + rr['dataObj']['picDetail'][i]['pic_url'])
#     Net_PO.downImage("https://mmres-cdn.jiefeixinxij.top" + rr['dataObj']['picDetail'][i]['pic_url'], "/Users/linghuchong/Downloads/eMule/youtube/mm131/")   # 将 kaptcha.jpg 下载保存在 d:\11目录下，如目录不存在则自动创建
#



url = "https://mmapi3.mcxxkjs.cn:2443/mm131//mm131/getCollectionList?collectionType" \
      "=2&lastIndex=14"
header = {
"accept": "*/*" ,
"channel": "AS_1",
"api_version": "v20",
"accept-language": "zh-Hans-CN;q=1",
"client_version": "1.0.1",
"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjE0MDgyMjE0NTYyLCJyYW5kb20iOjE1OTg5NzAyMDI3MTQsImxvZ2luX3R5cGUiOjJ9.u8z0ABQc_4vxON-9ddNj6kGCs2EVBK02Vfge2kbV1cc",
"applicationid": "102",
"did": "2FA99489-2B04-4EE8-BC2D-73D8FF3256CB",
"appkey": "BDC628A72BF854F2",
"user-agent": "mm131/1.0.1 (iPhone; iOS 15.0.2; Scale/3.00)",
"sign": "18E22C709F6BD54DB4404A886084B335"
}
r = requests.get(url=url, headers=header)
rr = json.loads(r.text)
# print(rr)
# print(rr['dataObj']['picDetail'][0]['pic_url'])
# print(rr['dataObj']['picDetail'][1]['pic_url'])
for i in range(len(rr['dataObj']['articleVideoDetail'])):
    print(rr['dataObj']['articleVideoDetail'][i]['video_url'])
    Net_PO.downImage( rr['dataObj']['articleVideoDetail'][i]['video_url'], "/Users/linghuchong/Downloads/eMule/youtube/mm131_v/")   # 将 kaptcha.jpg 下载保存在 d:\11目录下，如目录不存在则自动创建
