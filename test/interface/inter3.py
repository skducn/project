# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-17
# Description   : 带Token登录接口 ，for python3
# *****************************************************************

import requests, json
session = requests.session()

# 1、获取Token
result = session.post('http://112.74.191.10:8081/inter/HTTP/auth', data=None)
print(result.text)
jsonres = json.loads(result.text)
session.headers['token'] = jsonres['token']
print(jsonres['token'])

# 2、带Token登录
d = {
    'username':'will',
    'password':'123456',
}
result = session.post('http://112.74.191.10:8081/inter/HTTP/login',data=d)
print(result.text)

# 3、带Token登出
result = session.post('http://112.74.191.10:8081/inter/HTTP/logout',data=None)
print(result.text)


# {"status":200,"msg":"success","token":"b1ea385a14154aa7a68c7b3ce268b928"}
# {"status":200,"msg":"恭喜您，登录成功","userid":"1"}
# {"status":200,"msg":"用户已退出登录"}