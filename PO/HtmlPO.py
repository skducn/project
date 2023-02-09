# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2021-7-1
# Description: Html 对象层
# *******************************************************************************************************************************

"""
1.1 获取网站状态码 getCode()
1.2 获取网站请求头 getHeaders()
1.3 获取网页内容 getHtml()
1.4 获取网页json内容 getJsonText()

2.1 生成请求头 getUserAgent()
2.2 生成代理 getProxies()

3.1 解析get
3.2 解析get带参数
"""


from PO.DataPO import *
Data_PO = DataPO()

from PO.SysPO import *
Sys_PO = SysPO()

from PO.BeautifulsoupPO import *

class HtmlPO:

    # def __init__(self):
    # self.userAgent = self.getUserAgent()
    # self.proxies = self.getProxies()

    def getCode(self, varUrl):

        '''1.1 获取网站状态码'''

        rsp = requests.get(varUrl)
        return rsp.status_code


    def getHeaders(self, varUrl):

        '''1.2 获取网站请求头'''
        # {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'Keep-Alive',
        #  'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Fri, 20 Sep 2019 07:12:16 GMT',
        #  'Last-Modified': 'Mon, 23 Jan 2017 13:23:55 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18',
        #  'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}'''

        rsp = requests.get(varUrl)
        return rsp.headers


    def getHtml(self, varUrl, headers={}):

        '''1.3 获取网页内容'''

        # get请求时，response默认使用iso - 8859 - 1编码对消息体进行编码，如果返回内容出现乱码，请使用 utf-8 或 gb2312
        # 解决方法：查看网页源码找到charset关键字，如 charset=utf-8

        headers = {'User-Agent': 'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.1.6) Gecko/20070819 Firefox/2.0.0.6',
         'Referer': 'https://wall.alphacoders.com'}

        # 自定义头部
        session = requests.session()

        session.headers['User-Agent'] = Data_PO.getUserAgent()
        session.headers['Referer'] = varUrl
        session.headers['cookie'] = '__cf_bm=UHumr6GHtinud9kOWMzYrpRTHxM_64VOgBpJjB9IsVM-1675922221-0-AURS173UEo6LOqLfSK/5mzkCFAZv4Dx4LVLVOcos5x1m0xhLpILlw4VR4lKXRWorOTILv4jsnjrlGuRYc7akl0uQQyel5n2qf7opCrAqf/M7IdBowOYLRNW6EkWKj9Wiy/7XnW61hq90uiQHsx54eCgq2RfMSHZImPQAHVTAqCnm/aHWL60+/Ce4KkstTZfK9w=='
        print(session.headers)
        # r = requests.get(varUrl, headers=headers)
        r = session.get(varUrl, headers=session.headers)

        # 返回状态码，200正常可运行
        r.raise_for_status()

        # 设置全文的编码等于文件头部编码，文件第一行是 # -*- coding: utf-8 -*-
        r.encoding = r.apparent_encoding

        # 返回html格式的字符串
        return r.text



    def getJsonText(self, varUrl):

        '''1.4 获取网页json内容'''

        rsp = requests.get(url=varUrl, headers=self.getUserAgent(), proxies=self.getProxies())
        return rsp.json()



    def getUserAgent(self):

        '''2.1 生成 User-Agent'''
        # 如报错fake_useragent.errors.FakeUserAgentError: Maximum amount of retries reached，则执行 pip3.9 install -U fake-useragent 更新
        # 结果：{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}

        self.userAgent = {"User-Agent": Data_PO.getUserAgent()}
        return self.userAgent


    def getProxies(self):

        '''2.2 生成proxies代理'''

        varIp = Data_PO.getProxies()
        self.proxies = {str(varIp).split("://")[0]: varIp}
        return self.proxies



    def rspGet(self, varUrl, headers={}):

        '''3.1 解析get'''

        headers['User-Agent'] = Data_PO.getUserAgent()
        # headers['Referer'] = 'https://wall.alphacoders.com/'
        # headers['sec-ch-ua'] ='" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"'
        # headers['sec-ch-ua-mobile'] = '?0'
        # headers['sec-ch-ua-platform'] ='"Windows"'
        # headers['Referer'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36}"

#
        print(headers)

        # return requests.get(url=varUrl, headers=headers, proxies=self.getProxies())


        res = requests.get(url=varUrl, headers=headers)
        return res.text

        # content= requests.get(url=varUrl, headers=headers).content
        # html = content.decode("utf8", "ignore")
        # return html


    def rspGetByParam(self, varUrl, headers=Data_PO.getUserAgent(), params=None):

        '''3.2 解析get带参数'''

        return requests.get(
            url=varUrl,
            params=params,
            headers=headers,
            proxies=self.getProxies()
        )




if __name__ == "__main__":

    Html_PO = HtmlPO()

    # print("1.1 获取网站状态码".center(100, "-"))
    # print(Html_PO.getCode("https://www.baidu.com"))  # 200
    # print(Html_PO.getCode("https://wall.alphacoders.com/by_resolution.php?w=3840&h=2160&lang=Chinese&page=3"))  # 403
    # print(Html_PO.getCode("https://wall.alphacoders.com/"))  # 400
    # print(Html_PO.getCode("https://wall.alphacoders.com/popular_searches.php"))  # 400
    #
    # print("1.2 获取网站的headers".center(100, "-"))
    # print(Html_PO.getHeaders("https://www.kuaidaili.com/"))  #  {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Fri, 04 Nov 2022 03:24:59 GMT', 'Last-Modified': 'Mon, 23 Jan 2017 13:27:36 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18', 'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}


    # print("1.3 获取网页内容".center(100, "-"))
    # print(Html_PO.getHtml("https://www.baidu.com"))
    print(Html_PO.getHtml("https://wall.alphacoders.com"))

    # Beautifulsoup_PO = BeautifulsoupPO("https://www.baidu.com")
    # x = Beautifulsoup_PO.soup.find("map", {'name': 'mp'}).find_all('area')[0].attrs['href']
    # print(x)


    #
    # print("1.4 获取网页json内容".center(100, "-"))
    # print(Html_PO.getJsonText("https://www.ximalaya.com/revision/album/getTracksList?albumId=13738175&pageNum=1"))


    # print("2.1 生成UserAgent".center(100, "-"))
    # print(Html_PO.getUserAgent())  # {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
    # print(Html_PO.getUserAgent())

    # print("2.2 生成proxies代理".center(100, "-"))
    # print(Html_PO.getProxies())
    # print(Html_PO.getProxies())


    # print("3.1 解析get".center(100, "-"))
    # r = Html_PO.rspGet("https://wall.alphacoders.com/by_resolution.php?w=3840&h=2160&lang=Chinese&page=3")
    # print(r)
    # print(r.text)
    # html = Html_PO.rspGet("https://www.baidu.com", Html_PO.getHeaders("https://www.baidu.com"))
    # html = Html_PO.rspGet("https://www.baidu.com")
    # print(html)
    # print(html.url)
