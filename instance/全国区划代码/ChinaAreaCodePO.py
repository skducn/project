# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : 获取全国22个省4个市5个自治区
# 国家统计局 http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html
# *********************************************************************

import requests,sys,os
from bs4 import BeautifulSoup
from PO.ListPO import *
List_PO = ListPO()
from PO.HtmlPO import *
Html_PO = HtmlPO()



class ChinaAreaCodePO():

    def __init__(self):

        self.listMain = []
        self.list1 = []
        self.l_county = []
        self.l_street = []
        self.s = 1

        self.d_city = {}
        self.d_county = {}
        self.d_town = {}
        self.d_village = {}

        self.l_county = []
        self.l_town = []
        self.l_village = []
        self.l_village1 = []

        self.temp = ""
        self.x = 0

        self.d_province = {}
        self.l_city = []
        self.jiedao = ""

        self.city = ""
        self.county = ""
        self.town = ""
        self.village = ""


    def get_html(self, url):

        # 根据地址获取页面内容，并返回BeautifulSoup

        response = requests.get(url, headers=Html_PO.getHeaders())
        response.encoding = "GBK"
        return BeautifulSoup(response.text, "lxml")
        # print(response.text)



    # 获取地址前缀（用于相对地址）
    def get_prefix(self, url):
        return url[0:url.rindex("/") + 1]


    def update(self, varProvince, file):

        # 抓取省份页面
        province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html"
        province_list = self.get_html(province_url).select('tr.provincetr a')
        # print(province_list)  # [<a href="11.html">北京市<br/></a>, <a href="12.html">天津市<br/></a>,

        for province in province_list:
            name = province.text
            if name == varProvince:
                href = province.get("href")
                code = href[0: 2] + "0000000000"
                self.d_province[code] = name
                d = self.spider_next(self.get_prefix(province_url) + href, 2)
                print(d)
                with open(file, mode='w', encoding='utf-8') as f:
                    f.write(json.dumps(d, ensure_ascii=False))

                break

    # 递归抓取下一页面
    def spider_next(self, url, lev):

        if lev == 2:
            spider_class = "city"
        elif lev == 3:
            spider_class = "county"
        elif lev == 4:
            spider_class = "town"
        else:
            spider_class = "village"
        for item in self.get_html(url).select("tr." + spider_class + "tr"):
            item_td = item.select("td")
            item_td_code = item_td[0].select_one("a")
            item_td_name = item_td[1].select_one("a")
            if item_td_code is None:
                item_href = None
                item_code = item_td[0].text
                item_name = item_td[1].text
                if lev == 5:
                    item_name = item_td[2].text
            else:
                item_href = item_td_code.get("href")  # 31/3101.html
                item_code = item_td_code.text  # 310100000000
                item_name = item_td_name.text  # 市辖区

            if lev == 2:
                # 市辖区
                self.d_province[item_code] = item_name

            elif lev == 3:
                # 区
                self.d_province[item_code] = item_name
                print(item_name)

            elif lev == 4:
                # 街道
                self.d_province[item_code] = item_name

            elif lev == 5:
                # 居委
                self.d_province[item_code] = item_name

            if item_href is not None:
                self.spider_next(self.get_prefix(url) + item_href, lev + 1)

        return self.d_province



    def getDict(self, file):

        # 获取文件内容为字典类型格式

        with open(file, "r", encoding="utf-8") as f:
            for userline in f:
                userline = eval(userline)
        return (userline)


    def find(self, d_bj, varCity):

        # 获取直辖市下的区
        dict1 = {}

        for k,v in d_bj.items():
            # 直辖市
            if v == varCity and k[4:] == "00000000":
                varLeft = k[:4]
                varRight = "000000"
                for k1,v1 in d_bj.items():
                    if k1[:4] == varLeft and k1[-6:] == varRight:
                        dict1[k1] = v1
                break
            # 区
            if v == varCity and k[6:] == "000000":
                varLeft = k[:6]
                varRight = "000"
                for k,v in d_bj.items():
                    if k[:6] == varLeft and k[-3:] == varRight:
                        dict1[k] = v
            # 街道
            if v == varCity and k[9:] == "000":
                varLeft = k[:9]
                for k,v in d_bj.items():
                    if k[:9] == varLeft and k[-3:] != "000":
                        dict1[k] = v

        return dict1


if __name__ == '__main__':


    ChinaAreaCode_PO = ChinaAreaCodePO()

    # 下载城市到文件(字典格式)
    # ChinaAreaCode_PO.update("北京市", "json_bj.txt")
    # ChinaAreaCode_PO.update("上海市", "json_sh.txt")
    ChinaAreaCode_PO.update("重庆市", "json_cq.txt")




    # # 获取区、街道、居委

    # print(ChinaAreaCode_PO.find(ChinaAreaCode_PO.getDict("json_bj.txt"), "市辖区"))
    # print(ChinaAreaCode_PO.find(ChinaAreaCode_PO.getDict("json_bj.txt"), "东城区"))
    # print(ChinaAreaCode_PO.find(ChinaAreaCode_PO.getDict("json_bj.txt"), "永定门外街道"))

    # print(ChinaAreaCode_PO.find(ChinaAreaCode_PO.getDict("json_sh.txt"), "市辖区"))
    # print(ChinaAreaCode_PO.find(ChinaAreaCode_PO.getDict("json_sh.txt"), "浦东新区"))
    # print(ChinaAreaCode_PO.find(ChinaAreaCode_PO.getDict("json_sh.txt"), "金杨新村街道"))
