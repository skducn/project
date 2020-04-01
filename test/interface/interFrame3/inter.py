# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-3-11
# Description: 电子健康档案 接口
# https://www.cnblogs.com/malcolmfeng/p/6909293.html
# pymssql托管在Github上：https://github.com/pymssql
# https://www.cnblogs.com/TF12138/p/4064752.html
# *****************************************************************
import requests
import json
host = 'http://192.168.0.102:8080'
endpoint = r"/healthRecord/app/login"
url = ''.join([host,endpoint])

headers = { "Content-Type": "application/json;charset=UTF-8"}
body = {"userName": "zhaoyun", "password": "123456"}
r = requests.post(url, headers=headers, data=json.dumps(body))
# r = requests.post(url,headers=headers,json=body)
print(r.text)
print(r.url)
