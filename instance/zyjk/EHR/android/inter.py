# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-3-11
# Description: 电子健康档案 接口
# https://www.cnblogs.com/malcolmfeng/p/6909293.html  python连接sql server数据库实现增删改查
# http://192.168.0.102:8080/healthRecord/swagger-ui.html#/  管理系统api文档
# https://www.cnblogs.com/TF12138/p/4064752.html  sql server 查询数据库所有的表名+字段
# *****************************************************************
import requests, jsonpath, json
host = 'http://192.168.0.36:8080'

# 登录
endpoint = r"/healthRecord/app/login"
url = ''.join([host, endpoint])
headers = {"Content-Type": "application/json;charset=UTF-8"}
body = {"userName": "jinhao", "password": "123456"}
r = requests.post(url, headers=headers, json=body)
print(r.url)
print(r.text)
token = jsonpath.jsonpath(json.loads(r.text), expr='$.refresh_token')
print(token[0])

from time import sleep
sleep(1212)
# '初次修改密码'
# endpoint = r"/healthRecord/app/setPassword"
# url = ''.join([host, endpoint])
# body = {"userName":"jinhao", "password":"Jh123456...", "newPassword":"Jh123456///"}
# r = requests.post(url, headers=headers, json=body)
# print(r.url)
# print(r.text)

# 获取密保
endpoint = r"/healthRecord/encrypted/getQuestionList?userName=jinhao"
url = ''.join([host, endpoint])
r = requests.get(url, headers=headers)
print(r.url)
print(r.text)
userId = jsonpath.jsonpath(json.loads(r.text), expr='$.data.userId')
# print(userId[0])

# 密保校验->
endpoint = r"/healthRecord/encrypted/check"
url = ''.join([host, endpoint])
# headers = {"Content-Type": "application/json;charset=UTF-8"}
body = {"answer1": "111","answer2": "222","answer3": "333","question1": "name","question2": "age","question3": "good","userId": userId[0]}
r = requests.post(url, headers=headers, json=body)
print(r.url)
print(r.text)

# 获取个人信息表
endpoint = r"/healthRecord/PersonBasicInfo/getArchiveNum?idCard=310101198004110014"
url = ''.join([host, endpoint])
r = requests.get(url, headers=headers)
print(r.url)
print(r.text)

# # 密保通过时重设密码->
# endpoint = r"/healthRecord/encrypted/setPassAfterCheck"
# url = ''.join([host, endpoint])
# headers = {"Content-Type": "application/json;charset=UTF-8", "token":token[0]}
# body = {"userName":"jinhao", "newPassword":"Jh123456///"}
# r = requests.post(url, headers=headers, json=body)
# print(r.url)
# print(r.text)

# # 保存档案封面( healthrecord.HrPersonBasicInfo)
# endpoint = r"/healthRecord/app/coverManager/save"
# url = ''.join([host, endpoint])
# headers = {"Content-Type": "application/json;charset=UTF-8", "token":token[0]}
# body = {"userName":"jinhao", "newPassword":"Jh123456,,,"}
# r = requests.post(url, headers=headers, json=body)
# print(r.url)
# print(r.text)
#
# "archiveNum": "310101198004110014",
#   "archiveUnitId": 0,
#   "archiveUnitName": "string",
#   "archiverId": 0,
#   "archiverName": "string",
#   "cityId": 0,
#   "cityName": "string",
#   "coverId": 0,
#   "createArchiveDate": "string",
#   "districtId": 0,
#   "districtName": "string",
#   "hasAudio": 0,
#   "idCard": "string",
#   "name": "string",
#   "neighborhoodId": 0,
#   "neighborhoodName": "string",
#   "new": true,
#   "permanentAddress": "string",
#   "phone": "string",
#   "presentAddress": "string",
#   "provinceId": 0,
#   "provinceName": "string",
#   "recordTimeList": [
#     {
#       "archiveNum": "string",
#       "attributeName": "string",
#       "endTime": 0,
#       "moduleName": "string",
#       "operationType": 0,
#       "recordTime": 0,
#       "startTime": 0
#     }
#   ],
#   "responsibleDoctorId": 0,
#   "responsibleDoctorName": "string",
#   "villageId": 0,
#   "villageName": "string"
# }