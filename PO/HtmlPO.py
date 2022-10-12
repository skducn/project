# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2021-7-1
# Description: Html 对象层
# *******************************************************************************************************************************

'''
1 获取网站状态码 getCode()
2 获取网站的headers getHeaders()
3 获取网页内容 getText()

4.1 生成headers getHeaders()
4.2 生成proxies代理 getProxies()

5 获取json网页内容 getJson()

6 解析session.get
'''


from PO.DataPO import *
Data_PO = DataPO()
from PO.SysPO import *
Sys_PO = SysPO()

class HtmlPO:


    def getCode(self, varUrl):

        # 1 获取网站状态码

        response = requests.get(varUrl)
        return response.status_code


    def getHeaders(self, varUrl):

        # 2 获取网站的header

        # {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'Keep-Alive',
        #  'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Fri, 20 Sep 2019 07:12:16 GMT',
        #  'Last-Modified': 'Mon, 23 Jan 2017 13:23:55 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18',
        #  'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}'''
        response = requests.get(varUrl)
        return response.headers


    def getText(self, varUrl):

        # 3 获取网页内容

        res = requests.get(url=varUrl)
        # get请求时，response默认使用iso - 8859 - 1编码对消息体进行编码，如果返回内容出现乱码，可以使用 utf-8 , gb2312
        # 解决方法：查看网页源码找到charset关键字，如 charset=utf-8
        res.encoding = "utf-8"
        return res.text


    def getHeaders(self):

        # 4.1 生成headers

        self.headers = {'User-Agent': Data_PO.getUserAgent2()}
        return self.headers

    def getProxies(self):

        # 4.2 生成proxies代理

        varIp = Data_PO.getIpAgent()
        self.proxies = {str(varIp).split("://")[0]: varIp}
        return self.proxies


    def getJson(self, varUrl):

        # 5 获取json网页内容

        self.session = requests.session()
        response = requests.get(url=varUrl, headers=self.headers, proxies=self.proxies)
        return response.json()



    def sessionGet(self, varUrl, headers, proxies):

        # 6 解析session.get

        self.session = requests.session()
        ir = self.session.get(varUrl, headers=headers, proxies=proxies)
        return ir



if __name__ == '__main__':

    Html_PO = HtmlPO()


    # print("1，获取网站状态码".center(100, "-"))
    # print(Html_PO.getCode("http://www.baidu.com"))
    #
    # print("2，获取网站的headers".center(100, "-"))
    # print(Html_PO.getHeaders("http://www.baidu.com"))
    #
    # print("3，获取网页内容".center(100, "-"))
    # print(Html_PO.getText("http://www.baidu.com"))
    #
    # print("4.1 生成headers".center(100, "-"))
    # Html_PO.getHeaders()
    #
    # print("4.2 生成proxies代理".center(100, "-"))
    Html_PO.getProxies()
    #
    # print("5，获取json网页内容".center(100, "-"))
    # print(Html_PO.getJson("https://www.ximalaya.com/revision/album/getTracksList?albumId=13738175&pageNum=1"))
