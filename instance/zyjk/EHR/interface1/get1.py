# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-2-1
# Description   : EHR 健康档案服务内容通知，推荐值管理
# yapi管理平台地址：http://192.168.0.235:3000/
# 用户名  zhiying@123.com   密码  123456
# *****************************************************************
import json, jsonpath, os, requests



def get():


    session = requests.session()
    headers = {"Content-Type": "application/json;charset=UTF-8"}  # heaaders 默认请求Content-type   ,

    # 登录
    path = "http://192.168.0.236:8088/healthRecord/login"
    param= {'name': 'admin', 'pass': 'f19b8dc2029cf707939e886e4b164681'}
    result = session.post(path, headers=headers, json=param, verify=False)
    print(result.text)
    jsonres = json.loads(result.text)
    session.headers['token'] = jsonres['token']

    # 获取签约居民人群分类
    path = "http://192.168.0.236:8088/healthRecord/contentInform/getCrowdClassify"
    result = session.get(path, data=None)
    print(result.text)

    # 获取签约居民电子健康档案指标
    path = "http://192.168.0.236:8088/healthRecord/contentInform/getRecordIndex"
    result = session.get(path, data=None)
    print(result.text)

    # 获取签约居民电子健康档案问题汇总列表
    path = "http://192.168.0.236:8088/healthRecord/contentInform/getRecordIssueList"
    result = session.get(path, data=None)
    print(result.text)

    # 获取质控结果任务提醒人员列表
    path = "http://192.168.0.236:8088/healthRecord/contentInform/getRemindUserList"
    result = session.get(path, data=None)
    print(result.text)

    # 根据身份证号，查找治理信息
    path = "http://192.168.0.236:8088/healthRecord/recommend/getRecommendValueInfo?idCardNo=310110194808114641&idOfTargetTable=310110194310171227&targetTable=HrCover"
    result = session.get(path, data=None)
    print(session.headers)
    print(result.text)


get()
