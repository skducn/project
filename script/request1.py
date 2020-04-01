# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018/7/20 11:00
# Description: request1.py
# https://www.cnblogs.com/ranxf/p/7808537.html python3_requests 模块详解
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import requests, json

test_url = "http://172.21.200.48/test"
files = {'file': ('test.txt', b'Hello Requests.')}  # 必需显式的设置文件名
# r = requests.get(test_url)
r = requests.post(test_url, files=files)
# print(r.text)

# r1 = requests.get(url='http://dict.baidu.com/s', params={'wd': 'python'})      # 带参数的get请求
# print(r1.url)  # https://dict.baidu.com/s?wd=python

# # 响应状态码
# print(r.status_code)
#
# # 查看r.ok的布尔值便可以知道是否登陆成功，返回True 或 False
# print(r.ok)
#
# # # 以字典对象存储服务器响应头，但是这个字典比较特殊，字典键不区分大小写，若键不存在则返回None
# print(r.headers)
# print(r.headers['Content-Type'])
# print(r.headers.get('content-type')) #访问响应头部分内容的两种方式
#
# # 以encoding解析返回内容。字符串方式的响应体，会自动根据响应头部的字符编码进行解码。
# print(r.text)
#
# # 以字节形式（二进制）返回。字节方式的响应体，会自动为你解码 gzip 和 deflate 压缩。
# print(r.content)
#
# # 获取当前的编码
# r = requests.get('https://www.baidu.com')
# print(r.text, '\n{}\n'.format('*'*79), r.encoding)
# r.encoding = 'utf-8'  # 设置网页编码
# print(r.text, '\n{}\n'.format('*'*79), r.encoding)
#
# # 失败请求(非200响应)抛出异常 , 正常的话返回None
# print(r.raise_for_status())
#
# # Requests中内置的JSON解码器，以json形式返回,前提返回的内容确保是json格式的，不然解析出错会抛异常
# # r.json()


# # json处理
# r = requests.get('https://github.com/timeline.json')
# print(r.json())

# post发送json请求：
# r = requests.post('https://api.github.com/some/endpoint', data=json.dumps({'some': 'data'}))
# print(r.json())  # {'message': 'Not Found', 'documentation_url': 'https://developer.github.com/v3'}


# 定制头和cookie信息
# header = {'user-agent': 'my-app/0.0.1'}
# cookie = {'key':'value'}
#  r = requests.get/post('your url',headers=header,cookies=cookie)

# data = {'some': 'data'}
# headers = {'content-type': 'application/json',
#            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
# r = requests.post('http://172.21.200.48', data=data, headers=headers)
# # print(r.text)
# print(r.request.headers)  # #返回发送到服务器的头信息


# # 会话对象，能够跨请求保持某些参数
# s = requests.Session()
# s.auth = ('auth','passwd')
# s.headers = {'key':'value'}
# r = s.get('url')
# r1 = s.get('url1')
#
# # 代理
# proxies = {'http':'ip1','https':'ip2' }
#如果代理需要用户名和密码，则需要这样：
# proxies = {
#     "http": "http://user:pass@10.10.1.10:3128/",
# requests.get('url',proxies=proxies)
# }

# # Cookies
# url = 'http://example.com/some/cookie/setting/url'
# r = requests.get(url)
# r.cookies['example_cookie_name']  # 读取cookies
#
# url = 'http://m.ctrip.com/cookies'
# cookies = dict(cookies_are='working')
# r = requests.get(url, cookies=cookies)  # 发送cookies
#
# # 设置超时时间
# r = requests.get('http://m.ctrip.com', timeout=0.001)