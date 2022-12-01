# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018/7/20 11:00
# Description: request1.py
# python3_requests 模块详解 https://www.cnblogs.com/ranxf/p/7808537.html
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# def get(url: str | bytes,
#         params: Any = ...,
#         data: Any | None = ...,
#         headers: Any | None = ...,
#         cookies: Any | None = ...,
#         files: Any | None = ...,
#         auth: Any | None = ...,
#         timeout: Any | None = ...,
#         allow_redirects: bool = ...,
#         proxies: Any | None = ...,
#         hooks: Any | None = ...,
#         stream: Any | None = ...,
#         verify: Any | None = ...,
#         cert: Any | None = ...,
#         json: Any | None = ...)

import requests, json


# todo 重定向
'''重定向的状态码'''
# 301 redirect: 301 代表永久性转移(Permanently Moved)
# 302 redirect: 302 代表暂时性转移(Temporarily Moved )

'''禁用重定向 allow_redirects = False'''
# 如：response = requests.get(url=url, allow_redirects=False)
# 如url地址是重定向，设置 allow_redirects = False 则返回状态码302
# allow_redirects 默认是True，即启动重定向，则请求url后重定向到其他地址，返回状态码200

'''获取重定向的跳转url'''
# 请求地址后，响应结果header中有一个属性 Location ，他代表重定向；
# 方法1：reponse.headers.get("Location") 从响应头中获取重定向 url
# 方法2：response.url 获取跳转后真实的url

'''查看重定向历史,并且记录最终重定向到的 url'''
# l_redit = response.history
# redit_link = l_redit[len(l_redit)-1].headers["location"]


# todo 获取cookies
# headers = {"content-type": "application/x-www-form-urlencoded"}
# s = requests.session()
# s.post("http://192.168.0.65/logincheck.php", headers=headers)
# getCookies = s.cookies.get_dict()  # 获取cookies
# print(getCookies)  # {'PHPSESSID': 'vdhk8gspvt3d3hjn7rv6fjqbe5'}


# todo 获取cookie过期时间
# @classmethod
# def get_cookie_expires(cls, jar_cookies):
#     """
#     获取 jar_cookies 里面 sessionid 或 sessionid_ss 或 sid_tt 的有效期
#     """
#     result = None
#     for item in jar_cookies:
#         if item.name == "sessionid" or item.name == "sessionid_ss" or item.name == "sid_tt":
#             timestamp = item.expires
#             if timestamp:
#                 result = cls.timestamp_to_datetime(timestamp)
#     return result
#
# @staticmethod
# def timestamp_to_datetime(timestamp):
#     """
#     时间戳转datetime
#     :param timestamp:
#     :return: datetime
#     """
#     result = datetime.fromtimestamp(timestamp)


# todo session() 会话对象可以跨请求保持某些参数
# 如：登录页面在爬取数时会自动为每个爬虫请求添加cookie，保持爬虫的会话状态,避免手动的为每个爬虫请求手动添加cookie.
# s = requests.session()
# # 添加cookies
# requests.utils.add_dict_to_cookiejar(s.cookies, {"PHPSESSID":"07et4ol1g7ttb0bnjmbiqjhp43"})
# print(s.cookies.get_dict())  # {'PHPSESSID': '07et4ol1g7ttb0bnjmbiqjhp43'}
# res1 = s.get("http://www.baidu.com")
# print(s.cookies) # <RequestsCookieJar[<Cookie PHPSESSID=07et4ol1g7ttb0bnjmbiqjhp43 for />, <Cookie BDORZ=27315 for .baidu.com/>]>
# res2 = s.get("https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_9000013757081156770%22%7D&n_type=0&p_from=1")
# print(s.cookies) # <RequestsCookieJar[<Cookie PHPSESSID=07et4ol1g7ttb0bnjmbiqjhp43 for />, <Cookie BAIDUID=27CF0C58C79798D87E2BC1226FEC3EC4:FG=1 for .baidu.com/>, <Cookie BDORZ=27315 for .baidu.com/>, <Cookie x-logic-no=2 for .mbd.baidu.com/>]>


# todo session() 会话请求方法的缺省数据
# # 如：
# s = requests.Session()
# # 设置session对象的auth属性，用来作为请求的默认参数
# s.auth = ('user', 'pass')  # {'Authorization': 'Basic dXNlcjpwYXNz'}
# # 设置session的headers属性，通过update方法合并headers属性。
# s.headers.update({'x-test12': 'true'})
# r = s.get('http://httpbin.org/headers', headers={'x-test456': 'true'})
# # 查看发送请求的请求头
# print(r.request.headers)
# # {'User-Agent': 'python-requests/2.23.0', 'Accept-Encoding': 'gzip, deflate',
# # 'Accept': '*/*', 'Connection': 'keep-alive',
# # 'x-test12': 'true', 'x-test456': 'true', 'Authorization': 'Basic dXNlcjpwYXNz'}
#
# # 方法层的参数auth=('user','hah')覆盖了session的属性 s.auth = ('user', 'pass')
# r = s.get('http://httpbin.org/headers', auth=('user','hah'),headers={'x-test456': 'true'})
# print(r.request.headers)
# # {'User-Agent': 'python-requests/2.23.0', 'Accept-Encoding': 'gzip, deflate',
# # 'Accept': '*/*', 'Connection': 'keep-alive', 'x-test12': 'true',
# # 'x-test456': 'true', 'Authorization': 'Basic dXNlcjpoYWg='}


# todo 1将cookies信息放入字典，2发送请求，3将请求得到cookies添加到session对象的cookie中
# 1， cookie_dict = requests.utils.dict_from_cookiejar(s.cookies)
# 2， session.post(url) 或者 session.get(url) 等等
# 给 requests.session() 对象设置cookie信息
# 3，s.cookies = requests.utils.cookiejar_from_dict(cookies_dict)


# import time
# mycookie = { "PHPSESSID":"56v9clgo1kdfo3q5q8ck0aaaaa" }
# s = requests.session()
# requests.utils.add_dict_to_cookiejar(s.cookies,{"PHPSESSID":"07et4ol1g7ttb0bnjmbiqjhp43"})
# r = s.get("http://127.0.0.1:80",cookies = mycookie)
# print(s.cookies.get_dict())  # {'PHPSESSID': '07et4ol1g7ttb0bnjmbiqjhp43'}
# time.sleep(5)
# #请求以后抓包可以检验一下是不是添加成功
# s.get("http://127.0.0.1:80")
# print(s.cookies)

# todo 处理cookie内容为字典
# cookie = "SINAGLOBAL=821034395211.0111.1522571861723; wb_cmtLike_1850586643=1; un=tyz950829@sina.com; wb_timefeed_1850586643=1; UOR=,,login.sina.com.cn; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWsNeq71O_sXkkXNnXFHgOW5JpX5KMhUgL.Fo2RSK5f1hqcShe2dJLoI0qLxK-L12qLB-zLxKqL1hnL1K2LxK-LBo5L12qLxKqL1hML1KzLxKnL1K.LB-zLxK-L1K-LBKqt; YF-V5-G0=c99031715427fe982b79bf287ae448f6; ALF=1556795806; SSOLoginState=1525259808; SCF=AqTMLFzIuDI5ZEtJyAEXb31pv1hhUdGUCp2GoKYvOW0LQTInAItM-ENbxHRAnnRUIq_MR9afV8hMc7c-yVn2jI0.; SUB=_2A2537e5wDeRhGedG7lIU-CjKzz-IHXVUm1i4rDV8PUNbmtBeLVrskW9NUT1fPIUQGDKLrepaNzTEZxZHOstjoLOu; SUHB=0IIUWsCH8go6vb; _s_tentry=-; Apache=921830614666.5322.1525261512883; ULV=1525261512916:139:10:27:921830614666.5322.1525261512883:1525239937212; YF-Page-G0=b5853766541bcc934acef7f6116c26d1"
# cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}


# todo file参数写法，单个或多个文件
# # {"name": fileObj}
# files = {
#     'file1': open('/Downloads/hello.txt', 'rb'),
#     'file2': open('/Downloads/hello2.txt', 'rb')
# }
#
# # [("name", fileObj)]
# files = [
#   ('file1', open('/Downloads/hello.txt', 'rb')),
#   ('file2', open('/Downloads/hello2.txt', 'rb'))
# ]
#
# query = {}
# data = {"key": "val"}
# response = requests.post('http://httpbin.org/post', data=data,
#               params=query,
#               files=files,
#               timeout=10)
# fileObj 都可以替换为 tuple 形式, (file_name, fileObj)
# (file_name, fileObj, content-type)
# ('hello', open('/Downloads/hello.txt', 'rb'), 'plain/text'))

# todo files上传文件时，中文路径报错解决方法 。
# files = {'media': open(r'C:\新建文件夹\中文名字.jpg','rb')}
# requests.post(url=url, files=files)
# 解决：site-packages\urllib3\fields.py 文件，大约46行的位置，result.encode('ascii') 修改为 result.encode('utf-8')
# result.encode('utf-8').decode('utf-8') # 如果上面的还有问题就用这个。


# todo get请求，params参数中有%的解决方案：
# # 如：http://127.0.0.1/?test=%25test
# url = 'http://127.0.0.1'
# params = {'test':'%25test'}
# r = requests.get(url, params = params)
# # 响应结果中显示：GET /?test=%2525test HTTP/1.1 ，多了25，原因是URL中的百分号是个特殊字符，用来对需要进行百分号编码的字符的ASCII码进行转义
# # requests库会将params中的百分号进行转义（ASCII编码表中25表示%）
# # 解决方法：禁止对%进行编码
# url = 'http://127.0.0.1'
# params = {'test':'%25test'}
# params['test'] = unquote(params['test'])
# r = requests.get(url, params = params)



# todo 响应值
r = requests.get('https://www.baidu.com')
print(r.status_code)  # 200  //响应状态码
print(r.ok)  # True  //返回True 或 False
print(r.headers)  # {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Wed, 15 Jun 2022 07:49:40 GMT', 'Last-Modified': 'Mon, 23 Jan 2017 13:23:55 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18', 'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}
print(r.headers['Content-Type'])  # text/html
print(r.headers.get('content-type'))  # text/html
# print(r.text)  # 返回以encoding解析的内容。字符串方式的响应体，会自动根据响应头部的字符编码进行解码。
r.encoding = 'utf-8'  # 设置编码
# print(r.text, '\n{}\n'.format('*'*79), r.encoding)
print(r.content)  # 返回二进制字节形式的响应体，并自动解码 gzip 和 deflate。
print(r.raise_for_status())  # None  //失败请求(非200响应)抛出异常, 正确请求返回None
# print(r.json())  # Requests中内置的JSON解码器，以json形式返回,如果返回内容非json格式的，则会抛异常.
r = requests.get('https://api.github.com/some/endpoint')
# r.text 是字符串（双引号）
print(r.text)  # {"message":"Not Found","documentation_url":"https://docs.github.com/rest"}
# r.json() 是json格式的字典（单引号）
print(r.json())  # {'message':'Not Found','documentation_url':'https://docs.github.com/rest'}
print(r.json()['documentation_url'])  # https://docs.github.com/rest

# todo 参数 data和json：
# 请求体是字典， data = {'name':'lxx'},
# 请求体是序列化成的字符串 json= {"name":"jerry","pwd":"123"}
# 将字典序列化成字符串
str = json.dumps({'user_id': '66'})
print(str)  # {"user_id": "66"}
# 将字符串反序列化成字典
print(json.loads(str))  # {'user_id': '66'}
# 注意：如果提示AttributeError: module 'json' has no attribute 'dump' 问题：
# 解决：文件名不能是json.py 或 当前路径存不能有json目录


# todo proxies代理
# 普通代理
# proxies = {'http':'ip1','https':'ip2' }
# 有用户名和密码的代理
# proxies = {"http": "http://user:pass@10.10.1.10:3128/"）
# requests.get('url',proxies=proxies)

