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

        # response = requests.get(url, headers=Html_PO.getHeaders())
        # response.encoding = "GBK"
        # return BeautifulSoup(response.text, "lxml")
        # print(response.text)
        while True:
            try:
                # 超时时间为1秒
                # print(Html_PO.getHeaders())
                # print(Html_PO.getProxies())
                # response = Html_PO.sessionGet(url, Html_PO.getHeaders(), Html_PO.getProxies())
                # response = Html_PO.sessionGet(url, Html_PO.getHeaders(), proxies={'HTTP': 'http://122.9.101.6:8888'})
                # print(response)
                # response = requests.get(url)
                response = requests.get(url, headers=Html_PO.getHeaders())
                # response = Html_PO.sessionGet(url, headers=Html_PO.getHeaders(), proxies=Html_PO.getProxies())
                # print(response.text)
                # response.encoding = "GBK"
                response.encoding = "utf-8"
                if response.status_code == 200:
                    return BeautifulSoup(response.text, "lxml")
                else:
                    continue
            except Exception:
                continue


    # 获取地址前缀（用于相对地址）
    def get_prefix(self, url):
        return url[0:url.rindex("/") + 1]


    def update(self, varProvince):

        d_file = {}

        # 抓取省份页面
        province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/index.html"
        province_list = self.get_html(province_url).select('tr.provincetr a')
        # print(province_list)  # [<a href="11.html">北京市<br/></a>, <a href="12.html">天津市<br/></a>,

        for province in province_list:
            name = province.text
            d_file[name] = Char_PO.chinese2pinyin(name) + ".txt"
        print(d_file)


        for province in province_list:
            name = province.text
            # 下载单个省市
            for k, v in d_file.items():
                if name == varProvince and name == k:
                    if os.path.isfile(v) == False:
                        href = province.get("href")
                        code = href[0: 2] + "0000000000"
                        self.d_province[code] = name
                        d = self.spider_next(self.get_prefix(province_url) + href, 2)
                        print(d)
                        with open(v, mode='w', encoding='utf-8') as f:
                            f.write(json.dumps(d, ensure_ascii=False))


                # 下载所有省市
                if varProvince == "":
                    if os.path.isfile(v) == False:
                        if k == name and name != "河北省":
                            href = province.get("href")
                            code = href[0: 2] + "0000000000"
                            self.d_province[code] = name
                            # print(self.d_province)
                            print(name.center(100, "-"))
                            d = self.spider_next(self.get_prefix(province_url) + href, 2)
                            # print(d)
                            with open(v, mode='w', encoding='utf-8') as f:
                                f.write(json.dumps(d, ensure_ascii=False))



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
            # print(item_td)
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
                print(2, item_name)


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


    def find(self, d_bj, l_area):

        # 获取直辖市下的区
        dict1 = {}

        for k, v in d_bj.items():

            # 市(直辖)
            if l_area[1] == "" and v == l_area[0] and k[4:] == "00000000":
                varLeft = k[:4]
                for k, v in d_bj.items():
                    if k[:4] == varLeft and k[-6:] == "000000" and v != l_area[0]:
                        dict1[k] = v


            # 区(直辖)
            if v == l_area[0] and k[4:] == "00000000":
                varLeft = k[:4]
                for k, v in d_bj.items():
                    if v == l_area[1] and k[:4] == varLeft and k[-6:] == "000000" and v != l_area[0]:
                        varLeft = k[:6]
                        for k,v in d_bj.items():
                            if k[:6] == varLeft and k[-3:] == "000" and v != l_area[1]:
                                dict1[k] = v

            # 街道
            if v == l_area[0] and k[6:] == "000000":
                varLeft = k[:6]
                for k, v in d_bj.items():
                    if v == l_area[1] and k[9:] == "000" and k[:6] == varLeft:
                        varLeft = k[:9]
                        for k, v in d_bj.items():
                            if k[:9] == varLeft and k[-3:] != "000":
                                dict1[k] = v

        return dict1


if __name__ == '__main__':


    ChinaAreaCode_PO = ChinaAreaCodePO()

    # 下载所有省市
    ChinaAreaCode_PO.update("")

    # 下载省市
    # ChinaAreaCode_PO.update("北京市")
    # ChinaAreaCode_PO.update("上海市")
    # ChinaAreaCode_PO.update("天津市")
    # ChinaAreaCode_PO.update("辽宁省")
    # ChinaAreaCode_PO.update("山西省")
    # ChinaAreaCode_PO.update("内蒙古自治区")
    # ChinaAreaCode_PO.update("吉林省")
    # ChinaAreaCode_PO.update("黑龙江省")
    # ChinaAreaCode_PO.update("江苏省")
    # ChinaAreaCode_PO.update("浙江省")

    # ChinaAreaCode_PO.update("河北省")











    # # 获取区、街道、居委

    # 市下属所有区
    # print(ChinaAreaCode_PO.find(ChinaAreaCode_PO.getDict("json_nmg.txt"), ["呼伦贝尔市", ""]))
    #
    # # 区下属所有街道
    # print(ChinaAreaCode_PO.find(ChinaAreaCode_PO.getDict("json_nmg.txt"), ["呼伦贝尔市", "海拉尔区"]))
    #
    # # 街道下属所有居委会
    # print(ChinaAreaCode_PO.find(ChinaAreaCode_PO.getDict("json_nmg.txt"), ["海拉尔区", "胜利街道"]))


    # print(ChinaAreaCode_PO.find(ChinaAreaCode_PO.getDict("json_sh.txt"), ["市辖区", ""]))
    # print(ChinaAreaCode_PO.find(ChinaAreaCode_PO.getDict("json_sh.txt"), ["市辖区", "浦东新区"]))
    # print(ChinaAreaCode_PO.find(ChinaAreaCode_PO.getDict("json_sh.txt"), ["浦东新区", "金杨新村街道"]))
