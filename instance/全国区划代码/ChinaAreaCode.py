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

    def __init__(self, toSave):

        self.listMain = []
        self.list1 = []
        self.l_district = []
        self.l_street = []
        self.s = 1
        self.toSave = toSave
        if os.path.isfile(toSave):
            self.Openpyxl_PO = OpenpyxlPO(toSave)

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

    def xx(self, varArea):
        # 抓取省份页面
        province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html"
        province_list = self.get_html(province_url).select('tr.provincetr a')
        print(province_list)  # [<a href="11.html">北京市<br/></a>, <a href="12.html">天津市<br/></a>,

        for province in province_list:
            province_name = province.text

            if province_name == varArea:

                href = province.get("href")
                province_code = href[0: 2] + "0000000000"

                print(href)
                print(province_code)
                print(province_name)

                # sys.exit(0)
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
                self.spider_next(self.s, self.get_prefix(province_url) + href, 2)

    def update(self, varList):
        sign = 0
        if os.path.isfile(self.toSave):
            if len(varList) == 1 and varList[0] == 'all':
                File_PO.delFile(self.toSave)  # 删除
                self.Newexcel_PO = NewexcelPO(self.toSave)
                self.Openpyxl_PO = OpenpyxlPO(self.toSave)
            else:

                for j in range(len(self.Openpyxl_PO.getSheets())):
                    if varList[0] == self.Openpyxl_PO.getSheets()[j]:
                        self.Openpyxl_PO.delSheet(varList[0])
                        self.Openpyxl_PO.addSheetCover(varList[0], j)
                        sign = 1
                        print("添加内容")
                        self.xx(varList[0])
                if sign == 0 :
                    self.Openpyxl_PO.addSheetCover(varList[0], 0)


            # 抓取省份页面
            province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html"
            province_list = self.get_html(province_url).select('tr.provincetr a')
            # print(province_list)


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
                # 区
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(item_code[:6])
                self.list1.append(item_name)
                # print([x for x in self.list1 if x is not None])
                self.l_district.append([x for x in self.list1 if x is not None])
            elif lev == 4:
                # 街道
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                for i in range(len(self.l_district)):
                    if self.l_district[i][0] in item_code:
                        self.list1.append(self.l_district[i][0])
                        self.list1.append(self.l_district[i][1])
                self.list1.append(item_code[:9])
                self.list1.append(item_name)
                self.l_street.append([x for x in self.list1 if x is not None])
                # print(self.l_street)
            elif lev == 5:
                # 居委
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                for i in range(len(self.l_district)):
                    if self.l_district[i][0] in item_code:
                        self.list1.append(self.l_district[i][0])
                        self.list1.append(self.l_district[i][1])
                for i in range(len(self.l_street)):
                    if self.l_street[i][2] in item_code:
                        self.list1.append(self.l_street[i][2])
                        self.list1.append(self.l_street[i][3])
                self.list1.append(item_code)
                self.list1.append(item_name)

            self.s = self.s+1
            print(self.s, self.list1)
            self.Openpyxl_PO.setRowValue({self.s: self.list1})
            self.list1 = []

            if item_href is not None:
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

    ChinaAreaCode_PO = ChinaAreaCodePO("123.xlsx")
    ChinaAreaCode_PO.update(["上海市"])

    # 思路 获取表格里徐家汇行区间，删除，将徐家汇数据插入
    # ChinaAreaCode_PO.update(["上海市","徐汇区"])
    # ChinaAreaCode_PO.update(["上海市","徐汇区","徐家汇街道"])
