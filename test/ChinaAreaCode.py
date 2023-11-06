# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : 获取全国22个省4个市5个自治区
# 国家统计局 http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/index.html
# *********************************************************************

import requests,sys,os
from bs4 import BeautifulSoup
from PO.OpenpyxlPO import *

from PO.NewexcelPO import *

class ChinaAreaCodePO():

    def __init__(self, toSave, varList):

        self.listMain = []
        self.list1 = []
        self.s = 1
        if os.path.isfile(toSave):
            if len(varList) == 1 and varList[0] == 'all':
                File_PO.delFile(toSave)  # 删除
                Openpyxl_PO.newExcel(toSave)
            else:
                for i in range(len(varList)):
                    for j in range(len(Excel_PO.l_getSheet())):
                        if varList[i] == Excel_PO.l_getSheet()[j]:
                            Openpyxl_PO.delSheet(varList[i])
                            Openpyxl_PO.addSheetCover(varList[i], j)
                            print("添加内容")
        else:

            self.Newexcel_PO = NewexcelPO(toSave)
            self.Openpyxl_PO = OpenpyxlPO(toSave)

    # 根据地址获取页面内容，并返回BeautifulSoup
    def get_html(self, url):
        # 若页面打开失败，则无限重试，没有后退可言
        while True:
            try:
                # 超时时间为1秒
                response = requests.get(url, timeout=1)
                response.encoding = "GBK"
                if response.status_code == 200:
                    return BeautifulSoup(response.text, "lxml")
                else:
                    continue
            except Exception:
                continue


    def update(self, toSave, varList):

        # if os.path.isfile(toSave):
        #     if len(varList) == 1 and varList[0] == 'all':
        #         File_PO.delFile(toSave)  # 删除
        #         Openpyxl_PO.newExcel(toSave)
        #     else:
        #         for i in range(len(varList)):
        #             for j in range(len(Excel_PO.l_getSheet())):
        #                 if varList[i] == Excel_PO.l_getSheet()[j]:
        #                     Openpyxl_PO.delSheet(varList[i])
        #                     Openpyxl_PO.addSheetCover(varList[i], j)
        #                     print("添加内容")
        # else:
        #
        #     Newexcel_PO = NewexcelPO(toSave)
        #     Openpyxl_PO = OpenpyxlPO(toSave)

            # print("创建sheet，添加内容")

            # 抓取省份页面
            province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html"
            province_list = self.get_html(province_url).select('tr.provincetr a')
            # print(province_list)


            for province in province_list:
                href = province.get("href")
                province_code = href[0: 2] + "0000000000"
                province_name = province.text

                # print(href)
                self.Openpyxl_PO.addSheet(province_name)
                self.Openpyxl_PO.initData([['区划代码', '地区', '区划代码', '名称', '区划代码', '名称', '区划代码', '名称']])


                # print(province_code)
                # print(province_name)
                # 输出：级别、区划代码、名称
                content = "1\t" + province_code + "\t" + province_name
                # print(content)
                self.list1.append(province_code)
                self.list1.append(province_name)
                # self.listMain.append(self.list1)

                # print(self.list1)
                self.Openpyxl_PO.setRowValue({2: self.list1})
                # Openpyxl_PO.setRowValue({2: [1,2,3]})
                self.list1 = []

                # print(self.get_prefix(province_url)) # http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/
                # s = 1
                self.spider_next(self.s , self.get_prefix(province_url) + href, 2)


    # 获取地址前缀（用于相对地址）
    def get_prefix(self, url):
        return url[0:url.rindex("/") + 1]


    # 递归抓取下一页面
    def spider_next(self, s, url, lev):

        if lev == 2:
            spider_class = "city"
        elif lev == 3:
            spider_class = "county"
        elif lev == 4:
            spider_class = "town"
        else:
            spider_class = "village"

        for item in self.get_html(url).select("tr." + spider_class + "tr"):
            # print(item)
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
                item_href = item_td_code.get("href")
                item_code = item_td_code.text
                item_name = item_td_name.text
            # 输出：级别、区划代码、名称
            content2 = str(lev) + "\t" + item_code + "\t" + item_name
            # print(content2)
            # print(self.listMain)
            if lev == 2:
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(item_code)
                self.list1.append(item_name)
            elif lev == 3:
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(item_code)
                self.list1.append(item_name)
            elif lev == 4:
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(item_code)
                self.list1.append(item_name)
            elif lev == 5:
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(item_code)
                self.list1.append(item_name)
            # self.listMain.append(self.list1)
            # print(self.list1)

            self.s= self.s+1
            print(self.s, self.list1)
            self.Openpyxl_PO.setRowValue({self.s: self.list1})
            self.list1 = []


            if item_href is not None:
                print(item_href)
                self.spider_next(self.s, self.get_prefix(url) + item_href, lev + 1)


# 入口
if __name__ == '__main__':

    # # 抓取省份页面
    # province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html"
    # province_list = get_html(province_url).select('tr.provincetr a')
    # print(province_list)
    #
    # # 数据写入到当前文件夹下 area-number-2020.txt 中
    # f = open("area-number-2021.txt", "w", encoding="utf-8")
    # try:
    #     for province in province_list:
    #         href = province.get("href")
    #         province_code = href[0: 2] + "0000000000"
    #         province_name = province.text
    #
    #         print(href)
    #         print(province_code)
    #         print(province_name)
    #         # 输出：级别、区划代码、名称
    #         content = "1\t" + province_code + "\t" + province_name
    #         print(content)
    #         f.write(content + "\n")
    #         print(province_url)
    #         spider_next(get_prefix(province_url) + href, 2)
    # finally:
    #     f.close()

    ChinaAreaCode_PO = ChinaAreaCodePO("123.xlsx", ["北京"])
    # ChinaAreaCode_PO.update("ExcelPO/123.xlsx", ["all"])
    ChinaAreaCode_PO.update("123.xlsx", ["北京"])
    # ChinaAreaCode_PO.update("d:\\test1.xlsx", ["北京"，"上海"])
