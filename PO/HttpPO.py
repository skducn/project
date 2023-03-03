# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2021-7-1
# Description: Http 请求封装 （requests模块）

# 属性或方法	说明
# apparent_encoding	返回当前文档的编码方式，如第一行# -*- coding: utf-8 -*- 则返回 utf-8
# close()	关闭与服务器的连接
# content	返回响应的内容，以字节为单位
# cookies	返回一个 CookieJar 对象，包含了从服务器发回的 cookie
# elapsed	返回一个 timedelta 对象，包含了从发送请求到响应到达之间经过的时间量，可以用于测试响应速度。比如 r.elapsed.microseconds 表示响应到达需要多少微秒。
# encoding	解码 r.text 的编码方式，如 utf-8
# headers	返回响应头，字典格式
# history	返回包含请求历史的响应对象列表（url）
# is_permanent_redirect	如果响应是永久重定向的 url，则返回 True，否则返回 False
# is_redirect	如果响应被重定向，则返回 True，否则返回 False
# iter_content()	迭代响应
# iter_lines()	迭代响应的行
# json()	返回结果的 JSON 对象 (结果需要以 JSON 格式编写的，否则会引发错误)
# links	返回响应的解析头链接
# next	返回重定向链中下一个请求的 PreparedRequest 对象
# ok	检查 "status_code" 的值，如果小于400，则返回 True，如果不小于 400，则返回 False
# raise_for_status()	如果发生错误，方法返回一个 HTTPError 对象
# reason	响应状态的描述，比如 "Not Found" 或 "OK"
# request	返回请求此响应的请求对象
# status_code	返回 http 的状态码，比如 404 和 200
# text	返回响应的内容，unicode 类型数据
# url	返回响应的 URL

# post()方法格式：
# url 请求 url。
# data 参数为要发送到指定 url 的字典、元组列表、字节或文件对象。
# json 参数为要发送到指定 url 的 JSON 对象。
# args 为其他参数，比如 cookies、headers、verify等。

# requests 方法：
# delete(url, args)	发送 DELETE 请求到指定 url
# get(url, params, args)	发送 GET 请求到指定 url
# head(url, args)	发送 HEAD 请求到指定 url
# patch(url, data, args)	发送 PATCH 请求到指定 url
# post(url, data, json, args)	发送 POST 请求到指定 url
# put(url, data, args)	发送 PUT 请求到指定 url
# request(method, url, args)	向指定的 url 发送指定的请求方法
# *******************************************************************************************************************************

'''
1.1，获取User-Agent getUserAgent()
1.2，获取代理IP  getProxies()

2.1 获取内容 getHtml()
2,2 获取内容带参数 getHtmlByParam()

3.1 获取状态码 getCode()
3.2 获取返回响应值 getHeaders()

'''

import os, random, requests
from time import sleep

# from PO.BeautifulsoupPO import *
from fake_useragent import UserAgent

class HttpPO:

    def __init__(self):
        ...
        # getUserAgent = self.getUserAgent()
        # getProxies = self.getProxies()
        # self.headers = {}
        # self.headers['User-Agent'] = getUserAgent

    def getUserAgent(self):

        ''' 1.1，获取User-Agent
        return: {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}'''

        # 如报错 fake_useragent.errors.FakeUserAgentError: Maximum amount of retries reached，则更新 pip3.9 install -U fake-useragent
        # ua = UserAgent(use_cache_server=False)  # 禁用服务器缓存
        # ua = UserAgent(cache=False)  # 不缓存数据
        # ua = UserAgent(verify_ssl=False)  # 忽略ssl验证
        # print(ua.chrome)
        # print(ua.browsers)
        # print(ua.data_browsers['browsers']['chrome'][0])
        # print(ua.data_browsers['browsers'])
        # return (str(UserAgent(path='D:/51/python/project/PO/fake_useragent_0.1.11.json')))

        try:
            userAgent = str(UserAgent().random)
        except:
            os.system("pip3.9 install -U fake-useragent")
            userAgent = str(UserAgent().random)
        # return {"User-Agent": userAgent}
        return str(userAgent)

    def getProxies(self):

        ''' 1.2，获取代理IP
        return: {'HTTP': 'HTTP://222.74.73.202:42055'}
        '''

        from bs4 import BeautifulSoup

        baseURL = "https://www.kuaidaili.com/free"
        # baseURL = "https://www.kuaidaili.com/free/inha/1/"

        headers = {"User-Agent": str(UserAgent().random)}
        html = requests.get(baseURL, headers=headers)
        # html.encoding = 'gb2312'
        # html.encoding = 'utf-8'
        # html.encoding = 'gbk'
        # bsop = BeautifulSoup(html.text.encode('gbk', 'ignore').decode('gbk'), 'html.parser')
        bsop = BeautifulSoup(html.text, "html.parser")

        # 获取 IP 列表
        l_ips = bsop.findAll("td", {"data-title": "IP"})
        l_ip = []
        for l in l_ips:
            l_ip.append(str(l).replace('<td data-title="IP">', "").replace("</td>", ""))

        # 获取 PORT 列表
        l_ports = bsop.findAll("td", {"data-title": "PORT"})
        l_port = []
        for l in l_ports:
            l_port.append(str(l).replace('<td data-title="PORT">', "").replace("</td>", ""))

        # 获取 类型 列表
        l_types = bsop.findAll("td", {"data-title": "类型"})
        l_type = []
        for l in l_types:
            l_type.append(str(l).replace('<td data-title="类型">', "").replace("</td>", ""))

        l_ipPort = []
        for i in range(len(l_ip)):
            l_ipPort.append(l_type[i] + "://" + l_ip[i] + ":" + l_port[i])
        sleep(1)
        varIp = l_ipPort[random.randint(0, len(l_ipPort) - 1)]
        proxies = {str(varIp).split("://")[0]: varIp}
        return proxies


    def getHtml(self, varUrl, headers={}):

        '''2.1 获取内容'''

        # 自定义头部

        # headers['Referer'] = varUrl
        # headers['cookie'] = ''
        # print(headers)
        # print(self.getUserAgent())
        headers['User-Agent'] = self.getUserAgent()
        r = requests.get(varUrl, headers=headers, proxies=self.getProxies())
        # r = requests.get(varUrl, headers=headers, proxies=self.getProxies(), timeout=30)

        # 如果返回的状态码不是200，则报错返回一个 HTTPError 对象，如403
        r.raise_for_status()

        # 设置内容编码，将文件第一行 # -*- coding: utf-8 -*- 即 返回内容转换成utf-8编码
        # r.encoding = r.apparent_encoding

        headers['User-Agent'] = ''

        # r.text 返回响应的内容(unicode 类型数据)
        # r.content 返回响应的内容(字节为单位)  # r.content.decode("utf8", "ignore")
        # r.json 返回响应的内容(字典格式)
        return r

    def getHtmlByParam(self, varUrl, headers={}, params=None):

        '''2.2 获取内容带参数'''

        headers['User-Agent'] = self.getUserAgent()

        r = requests.get(url=varUrl, headers=headers, params=params, proxies=self.getProxies())
        # r = requests.get(url=arUrl, headers=headers, params=params, proxies=self.getProxies(), timeout=30)

        # 如果返回的状态码不是200，则报错返回一个 HTTPError 对象，如403
        r.raise_for_status()

        # 设置内容编码，将文件第一行 # -*- coding: utf-8 -*- 即 返回内容转换成utf-8编码
        r.encoding = r.apparent_encoding

        headers['User-Agent'] = ''

        # r.text 返回响应的内容(unicode 类型数据)
        # r.content 返回响应的内容(字节为单位)  # r.content.decode("utf8", "ignore")
        # r.json 返回响应的内容(字典格式)
        return r


    def getCode(self, varUrl):

        '''3.1 获取状态码'''

        r = requests.get(varUrl)
        return r.status_code

    def getHeaders(self, varUrl):

        '''3.2 获取返回响应头'''
        # {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'Keep-Alive',
        #  'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Fri, 20 Sep 2019 07:12:16 GMT',
        #  'Last-Modified': 'Mon, 23 Jan 2017 13:23:55 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18',
        #  'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}'''

        # headers = {'User-Agent': 'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.1.6) Gecko/20070819 Firefox/2.0.0.6',
        #  'Referer': 'https://wall.alphacoders.com'}

        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        #            'Referer': 'https://wall.alphacoders.com/',
        #            'cookie' : 'id=2227a400f4da0069||t=1675903700|et=730|cs=002213fd48032ecf4127381082',
        #            'origin': 'https://wall.alphacoders.com',
        #            'content-type': 'text/plain'}
        #
        # print(headers)

        r = requests.get(varUrl)
        return r.headers



if __name__ == "__main__":

    Http_PO = HttpPO()

    # # print("1.1 获取UserAgent".center(100, "-"))
    # print(Http_PO.getUserAgent())  # Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; es-es) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27
    #
    # # print("1.2 获取proxies代理".center(100, "-"))
    # print(Http_PO.getProxies())  # {'HTTP': 'HTTP://121.13.252.62:41564'}
    #
    #
    # # print("2.1，获取内容，并通过bs4获取元素".center(100, "-"))
    # r = Http_PO.getHtml("https://www.baidu.com")
    # # print(r.txt)
    # Beautifulsoup_PO = BeautifulsoupPO("https://www.baidu.com")
    # x = Beautifulsoup_PO.soup.find("map", {'name': 'mp'}).find_all('area')[0].attrs['href']
    # print(x)  # //www.baidu.com/s?wd=%E7%99%BE%E5%BA%A6%E7%83%AD%E6%90%9C&sa=ire_dl_gh_logo_texing&rsv_dl=igh_logo_pcs
    #
    # r = Http_PO.getHtml("https://www.ximalaya.com/revision/album/getTracksList?albumId=13738175&pageNum=1")
    # print(r.json)
    # print(r.json['data']['albumId'])  # 13738175
    #
    # # print("2.2，获取内容带参数".center(100, "-"))
    # # r = Http_PO.getHtmlByParam("https://www.baidu.com")
    #
    #
    # # print("3.1 获取状态码".center(100, "-"))
    # # print(Http_PO.getCode("https://www.baidu.com"))  # 200

    # print("3.2 获取网站的headers".center(100, "-"))
    # print(Http_PO.getHeaders("https://www.baidu.com/"))



