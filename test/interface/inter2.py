# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-17
# Description   : 带Token登录接口 ，for python2
# *****************************************************************
import requests, json

# 1、获取Token
result = requests.post('http://112.74.191.10:8081/inter/HTTP/auth', data=None)
print(result.text)  # {"status":200,"msg":"success","token":"572a817885db4a83b42b04785ea7b1ba"}
jsonres = json.loads(result.text)
# print(jsonres['token'])  # 572a817885db4a83b42b04785ea7b1ba ， 获取token值
headers = {"token":  jsonres['token']}  # 将Token放在头里。

# 2、带Token登录
d = {'username':'will','password':'123456'}
result = requests.post('http://112.74.191.10:8081/inter/HTTP/login', data=d, headers=headers)
print(result.text)

# 3、带Token登出
result = requests.post('http://112.74.191.10:8081/inter/HTTP/logout',data=None,headers=headers)
print(result.text)

# {"status":200,"msg":"success","token":"572a817885db4a83b42b04785ea7b1ba"}
# {"status":200,"msg":"恭喜您，登录成功","userid":"1"}
# {"status":200,"msg":"用户已退出登录"}