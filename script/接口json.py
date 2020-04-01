# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.0.0
# Date       : 2017-5-16
# Description: 接口参数json，http post json
# requests.session()会话保持 ，requests库的session会话对象可以跨请求保持某些参数。它也会在同一个 Session 实例发出的所有请求之间保持 cookie。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PO.DataPO import *
Data_PO = DataPO()
import json, requests
from requests.auth import HTTPBasicAuth
import time


varURL = 'http://192.168.0.36:8080/healthRecord/app/login'
d_parm = {'userName': 'shuyang', 'password': '07497ba923378ceada4a7f6428be9956'}
headers = {"Content-Type": "application/json;charset=UTF-8"}  # 请求头

s = requests.session()
s.headers.update({'x-test': 'true'})  # 更新请求头

r = s.post(varURL, headers=headers, json=d_parm, verify=False)
if r.status_code == 200:
    print(r.text)  # 返回解析内容（字符串）
# {"msg":"成功","existenceTime":6,"userInfo":{"userName":"shuyang","uid":2,"role":"aiAdmin,recordLookAdmin,orgAdmin","name":"舒阳"},"code":200,"isQcloud":true,"permission":[{"name":"待办任务"},{"name":"档案查阅"},{"name":"档案更新"},{"name":"档案录入"},{"name":"个人中心"},{"name":"健康账户"},{"name":"离线管理"},{"name":"录音文件管理"},{"name":"统计分析"},{"name":"预检待办任务"},{"name":"诊前待办任务"},{"name":"智能核对"}],"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCLoiJLpmLNcIixcInJvbGVcIjpcImFpQWRtaW4scmVjb3JkTG9va0FkbWluLG9yZ0FkbWluXCIsXCJ1aWRcIjoyLFwidXNlck5hbWVcIjpcInNodXlhbmdcIn0iLCJpYXQiOjE1ODQ5NDk0MzksImV4cCI6MTU4NDk1NjYzOX0.TH1CN3JAQ7AMYQFfYDcdsISfvTZNgj7LJNHsGziCHysG6cpumAEbPAkv56nnrOSoT7WfMEdJ3Skg7ll0TOe63Q"}


jsonres = json.loads(r.text)

s.headers['token'] = jsonres['token']  # 将 token 放入 header
print(s.headers)
# {'User-Agent': 'python-requests/2.22.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'token1': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCLoiJLpmLNcIixcInJvbGVcIjpcImFpQWRtaW4scmVjb3JkTG9va0FkbWluLG9yZ0FkbWluXCIsXCJ1aWRcIjoyLFwidXNlck5hbWVcIjpcInNodXlhbmdcIn0iLCJpYXQiOjE1ODQ5NDk0MzksImV4cCI6MTU4NDk1NjYzOX0.TH1CN3JAQ7AMYQFfYDcdsISfvTZNgj7LJNHsGziCHysG6cpumAEbPAkv56nnrOSoT7WfMEdJ3Skg7ll0TOe63Q'}

print(jsonres['msg'])