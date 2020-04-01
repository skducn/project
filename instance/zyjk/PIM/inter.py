# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-4-11
# Description: PIM 接口
# https://www.cnblogs.com/malcolmfeng/p/6909293.html  python连接sql server数据库实现增删改查
# http://192.168.0.102:8080/healthRecord/swagger-ui.html#/  管理系统api文档
# https://www.cnblogs.com/TF12138/p/4064752.html  sql server 查询数据库所有的表名+字段
# *****************************************************************
import requests, jsonpath, json
host = 'http://192.168.0.16:8081'

# 登录
endpoint = r"/pim/login"
url = ''.join([host, endpoint])
headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
body = {"username": "001", "password": "123456"}
r = requests.post(url, headers=headers, data=body)
print(r.url)
print(r.text)
token = jsonpath.jsonpath(json.loads(r.text), expr='$.extra.token')
print(token[0])

# # '初次修改密码'
# # endpoint = r"/healthRecord/app/setPassword"
# # url = ''.join([host, endpoint])
# # body = {"userName":"jinhao", "password":"Jh123456...", "newPassword":"Jh123456///"}
# # r = requests.post(url, headers=headers, json=body)
# # print(r.url)
# # print(r.text)
#
# # 获取密保
# endpoint = r"/healthRecord/encrypted/getQuestionList?userName=jinhao"
# url = ''.join([host, endpoint])
# r = requests.get(url, headers=headers)
# print(r.url)
# print(r.text)
# userId = jsonpath.jsonpath(json.loads(r.text), expr='$.data.userId')
# # print(userId[0])
#
# # 密保校验->
# endpoint = r"/healthRecord/encrypted/check"
# url = ''.join([host, endpoint])
# # headers = {"Content-Type": "application/json;charset=UTF-8"}
# body = {"answer1": "111","answer2": "222","answer3": "333","question1": "name","question2": "age","question3": "good","userId": userId[0]}
# r = requests.post(url, headers=headers, json=body)
# print(r.url)
# print(r.text)
#
# # 获取个人信息表
# endpoint = r"/healthRecord/PersonBasicInfo/getArchiveNum?idCard=310101198004110014"
# url = ''.join([host, endpoint])
# r = requests.get(url, headers=headers)
# print(r.url)
# print(r.text)
#
# # # 密保通过时重设密码->
# # endpoint = r"/healthRecord/encrypted/setPassAfterCheck"
# # url = ''.join([host, endpoint])
# # headers = {"Content-Type": "application/json;charset=UTF-8", "token":token[0]}
# # body = {"userName":"jinhao", "newPassword":"Jh123456///"}
# # r = requests.post(url, headers=headers, json=body)
# # print(r.url)
# # print(r.text)
