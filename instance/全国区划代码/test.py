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
from PO.ListPO import *
List_PO = ListPO()
from PO.HtmlPO import *
Html_PO = HtmlPO()


class ChinaAreaCodePO():

    def __init__(self, toSave):

        self.listMain = []
        self.list1 = []
        self.l_county = []
        self.l_street = []
        self.s = 1

        self.d_city = {}
        self.d_county = {}
        self.d_town = {}
        self.d_village = {}


        self.toSave = toSave
        if os.path.isfile(toSave):
            self.Openpyxl_PO = OpenpyxlPO(toSave)
        else:
            self.Newexcel_PO = NewexcelPO(toSave)
            self.Openpyxl_PO = OpenpyxlPO(toSave)

    # 根据地址获取页面内容，并返回BeautifulSoup
    def get_html(self, url):

        # print(Html_PO.getHeaders())
        # response = Html_PO.sessionGet(url, Html_PO.getHeaders())
        # print(Html_PO.getHeaders())
        response = requests.get(url, headers=Html_PO.getHeaders())
        response.encoding = "GBK"
        return BeautifulSoup(response.text, "lxml")
        # print(response.text)

        # 若页面打开失败，则无限重试，没有后退可言
        # while True:
        #     try:
        #         # 超时时间为1秒
        #         # print(Html_PO.getHeaders())
        #         # print(Html_PO.getProxies())
        #         # response = Html_PO.sessionGet(url, Html_PO.getHeaders(), Html_PO.getProxies())
        #         # response = Html_PO.sessionGet(url, Html_PO.getHeaders(), proxies={'HTTP': 'http://122.9.101.6:8888'})
        #         # print(response)
        #         response = requests.get(url)
        #         print(response.text)
        #         response.encoding = "GBK"
        #         if response.status_code == 200:
        #             return BeautifulSoup(response.text, "lxml")
        #         else:
        #             continue
        #     except Exception:
        #         continue

    def getList(self, l_name):
        # 抓取省份页面
        province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html"
        province_list = self.get_html(province_url).select('tr.provincetr a')
        # print(province_list)  # [<a href="11.html">北京市<br/></a>, <a href="12.html">天津市<br/></a>,
        l_province = []
        l_city = []
        l_city_url = []
        l_city_url1 = []
        l_county = []
        l_county_url = []
        l_county_url1 = []
        l_town = []
        l_town_url = []
        l_town_url1 = []
        l_village = []
        d_province = {}
        d_city = {}
        d_county = {}
        d_town = {}
        d_village = {}

        d_city_county = {}
        d_city_town = {}
        d_city_town_village = {}
        l_village_m = []

        # {全国省市：url}
        for province in province_list:
            l_province.append(province.text)
            d_province[province.text] = self.get_prefix(province_url) + province.get("href")
            if province.text == l_name[0]:
                provincePrefixCode = province.get("href").replace(".html","")
                # print(provincePrefixCode)
        # print(l_province)
        # print(d_province)

        # {市：url}
        for k, v in d_province.items():
            if k == l_name[0]:
                # print(v)
                city_list = self.get_html(v).select('tr.citytr a')
                # print(city_list)
                for city in city_list:
                    l_city.append(city.text)
                    l_city_url.append(self.get_prefix(province_url) + city.get("href"))
                # print(l_city_url)
                l_city = [x for x in l_city if l_city.index(x) % 2 != 0]
                [l_city_url1.append(x) for x in l_city_url if x not in l_city_url1]
                break
        d_city = List_PO.twoList2dict(l_city, l_city_url1)
        # print(l_city)
        # print(l_city_url1)
        print(2, d_city)

        # {区：url}
        for k, v in d_city.items():
            if l_name[1] == "":
                district_list = self.get_html(v).select('tr.countytr a')
                # print(district_list)
                if l_name[2] == "":
                    for district in district_list:
                        l_county.append(district.text)
                        l_county_url.append(
                            self.get_prefix(province_url) + provincePrefixCode + "/" + district.get("href"))
                        districtPrefixCode = district.get("href")
                        # print(districtPrefixCode)
                    # print(l_county)
                    l_county = [x for x in l_county if l_county.index(x) % 2 != 0]
                    [l_county_url1.append(x) for x in l_county_url if x not in l_county_url1]
                    # print(l_county_url1)
                    d_county = List_PO.twoList2dict(l_county, l_county_url1)
                    d_city_county[k] = d_county
                    l_county = []
                    l_county_url = []
                    l_county_url1 = []
                    d_county = {}
                else:
                    sys.exit(0)
            elif k == l_name[1]:
                # print(v)
                district_list = self.get_html(v).select('tr.countytr a')
                # print(district_list)
                if l_name[2] == "":
                    for district in district_list:
                        l_county.append(district.text)
                        l_county_url.append(self.get_prefix(province_url) + provincePrefixCode + "/" + district.get("href"))
                        districtPrefixCode = district.get("href")
                        # print(districtPrefixCode)
                    # print(l_county)
                    l_county = [x for x in l_county if l_county.index(x) % 2 != 0]
                    [l_county_url1.append(x) for x in l_county_url if x not in l_county_url1]
                    print(l_county_url1)
                    d_county = List_PO.twoList2dict(l_county, l_county_url1)
                    d_city_county[k] = d_county
                    l_county = []
                    l_county_url = []
                    l_county_url1 = []
                    d_county = {}
                else:
                    for district in district_list:
                        if district.text == l_name[2]:
                            l_county.append(district.text)
                            l_county_url.append(self.get_prefix(province_url) + provincePrefixCode + "/" + district.get("href"))
                            districtPrefixCode = district.get("href")
                            # print(districtPrefixCode)
                            districtPrefixCode = districtPrefixCode.split("/")[0]
                            # print(l_county)
                            # print(l_county_url)
                            d_county = List_PO.twoList2dict(l_county, l_county_url)
                            d_city_county[k] = d_county
                            l_county = []
                            l_county_url = []
                            d_county = {}
        print(3, d_city_county)


        # {街道：url}
        # print(d_county2)
        for k, v in d_city_county.items():
            # print(k)
            # if k == l_name[3]:
            #     print(v)
            # print(k)
            # print(l_name[2])
            # if l_name[2] == "":
            #     pass
            # elif k == l_name[2]:
            #     print("4444")
                # town_list = self.get_html(v).select('tr.towntr a')
                # # print(town_list)
                # countyCode = v1.split(provincePrefixCode + "/")[1].split("/")[0]
                # # print(countyCode)
                if l_name[3] == "":
                    for k1, v1 in v.items():



                            town_list = self.get_html(v1).select('tr.towntr a')
                            # print(town_list)
                            countyCode = v1.split(provincePrefixCode+"/")[1].split("/")[0]
                            # print(countyCode)
                            for town in town_list:
                                l_town.append(town.text)
                                l_town_url.append(self.get_prefix(province_url) + provincePrefixCode + "/" + countyCode + "/" + town.get("href"))
                                # print(l_town_url)
                                # townPrefixCode = town.get("href")
                                # print(townPrefixCode)
                            # print(l_town_url)
                            l_town = [x for x in l_town if l_town.index(x) % 2 != 0]
                            [l_town_url1.append(x) for x in l_town_url if x not in l_town_url1]
                            # break
                            d_town = List_PO.twoList2dict(l_town, l_town_url1)
                            d_town2 = d_town
                            d_city_town[k1] = d_town
                            l_town = []
                            l_town_url = []
                            l_town_url1 = []
                            d_town = {}
                else:

                    for k1, v1 in v.items():
                        if l_name[2] == k1 :
                            town_list = self.get_html(v1).select('tr.towntr a')
                            # print(town_list)
                            countyCode = v1.split(provincePrefixCode+"/")[1].split("/")[0]
                            # print(countyCode)
                            for town in town_list:
                                l_town.append(town.text)
                                l_town_url.append(self.get_prefix(province_url) + provincePrefixCode + "/" + countyCode + "/" + town.get("href"))
                                # print(l_town_url)
                                # townPrefixCode = town.get("href")
                                # print(townPrefixCode)
                            # print(l_town_url)

                            l_town = [x for x in l_town if l_town.index(x) % 2 != 0]
                            [l_town_url1.append(x) for x in l_town_url if x not in l_town_url1]

                            # break
                            d_town = List_PO.twoList2dict(l_town, l_town_url1)
                            d_town = ({k:v for k,v in d_town.items() if k == l_name[3]})

                            d_city_town[k1] = d_town
                            l_town = []
                            l_town_url = []
                            l_town_url1 = []
                            d_town = {}
                    # print(4, d_city_town)

            # break
        # print(l_town)
        print(4, d_city_town)


        # [区划代码，城乡分类代码，名称]
        for k, v in d_city_town.items():
            # if k == l_name[2]:
            # print(v)
            for k1, v1 in v.items():
                village_list = self.get_html(v1).select('tr.villagetr td')
                for village in village_list:
                    l_village.append(village.text)
                List_PO.resolveList(l_village, 3)
                d_city_town_village[k1] = List_PO.resolveList(l_village, 3)
                l_village = []
            # break
        print(5, d_city_town_village)

    def jixu(self, varProvince):

        sign = 0
        l_last = []
        # 判断是否有参数的sheet
        for j in range(len(self.Openpyxl_PO.getSheets())):
            if varProvince == self.Openpyxl_PO.getSheets()[j]:
                # 获取最后一条的行数
                # print(self.Openpyxl_PO.l_getTotalRowCol(varProvince)[0])
                varLastRow = self.Openpyxl_PO.getRowCol(varProvince)[0]

                # 获取最后一条记录内容
                l_record = self.Openpyxl_PO.getOneRowValue(self.Openpyxl_PO.getRowCol(varProvince)[0]-1, varProvince)
                # print(l_record)  # [None, None, None, None, '320104', '秦淮区', '320104007', '洪武路街道', '320104007010', '王府园社区居委会']

                # 获取市
                province = self.Openpyxl_PO.getColValueByCol([4], [1], varProvince)
                # print([x for x in province[0] if x != None][-1])
                strProvince = ([x for x in province[0] if x != None][-1])

                # 获取区
                # print(l_record[5])

                # 获取街道
                # print(l_record[7])

                # 获取居委会
                # print(l_record[9])

                l_last.append(varLastRow)
                l_last.append(strProvince)
                l_last.append(l_record[5])
                l_last.append(l_record[7])
                l_last.append( l_record[9])
                break
        print(l_last)
                # self.getList([varProvince, [x for x in province[0] if x != None][-1], l_record[5], l_record[7]])

                # 获取这个街道第一次出现的行号，删除所有此街道所有记录，插入此街道所有居委会
                # r = self.Openpyxl_PO.l_getRowValueByPartCol([8], varProvince)
                # print(r)


                # # 定位到第一次出现街道名的行号
                # print([r.index(x)+1 for x in r if x == [l_record[7]]][0])

                # # 删除此行号
                # op = [r.index(x)+1 for x in r if x == [l_record[7]]][0]
                # # self.Openpyxl_PO.delRow(op, 333)
                # # self.Openpyxl_PO.save()

                # 插入后续记录


        sys.exit(0)

                # 抓取省份页面
        province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html"
        province_list = self.get_html(province_url).select('tr.provincetr a')
        # print(province_list)  # [<a href="11.html">北京市<br/></a>, <a href="12.html">天津市<br/></a>,
        l_province = []
        l_city = []
        l_city_url = []
        l_city_url1 = []
        l_county = []
        l_county_url = []
        l_county_url1 = []
        l_town = []
        l_town_url = []
        l_town_url1 = []
        l_village = []
        d_province = {}
        d_city = {}
        d_county = {}
        d_town = {}
        d_village = {}

        d_city_county = {}
        d_city_town = {}
        d_city_town_village = {}
        l_village_m = []

        # {全国省市：url}
        for province in province_list:
            l_province.append(province.text)
            d_province[province.text] = self.get_prefix(province_url) + province.get("href")
            if province.text == l_name[0]:
                provincePrefixCode = province.get("href").replace(".html","")
                # print(provincePrefixCode)
        # print(l_province)
        # print(d_province)

        # {市：url}
        for k, v in d_province.items():
            if k == l_name[0]:
                # print(v)
                city_list = self.get_html(v).select('tr.citytr a')
                # print(city_list)
                for city in city_list:
                    l_city.append(city.text)
                    l_city_url.append(self.get_prefix(province_url) + city.get("href"))
                # print(l_city_url)
                l_city = [x for x in l_city if l_city.index(x) % 2 != 0]
                [l_city_url1.append(x) for x in l_city_url if x not in l_city_url1]
                break
        d_city = List_PO.twoList2dict(l_city, l_city_url1)
        # print(l_city)
        # print(l_city_url1)
        print(2, d_city)

        # {区：url}
        for k, v in d_city.items():
            if l_name[1] == "":
                district_list = self.get_html(v).select('tr.countytr a')
                # print(district_list)
                if l_name[2] == "":
                    for district in district_list:
                        l_county.append(district.text)
                        l_county_url.append(
                            self.get_prefix(province_url) + provincePrefixCode + "/" + district.get("href"))
                        districtPrefixCode = district.get("href")
                        # print(districtPrefixCode)
                    # print(l_county)
                    l_county = [x for x in l_county if l_county.index(x) % 2 != 0]
                    [l_county_url1.append(x) for x in l_county_url if x not in l_county_url1]
                    # print(l_county_url1)
                    d_county = List_PO.twoList2dict(l_county, l_county_url1)
                    d_city_county[k] = d_county
                    l_county = []
                    l_county_url = []
                    l_county_url1 = []
                    d_county = {}
                else:
                    sys.exit(0)
            elif k == l_name[1]:
                # print(v)
                district_list = self.get_html(v).select('tr.countytr a')
                # print(district_list)
                if l_name[2] == "":
                    for district in district_list:
                        l_county.append(district.text)
                        l_county_url.append(self.get_prefix(province_url) + provincePrefixCode + "/" + district.get("href"))
                        districtPrefixCode = district.get("href")
                        # print(districtPrefixCode)
                    # print(l_county)
                    l_county = [x for x in l_county if l_county.index(x) % 2 != 0]
                    [l_county_url1.append(x) for x in l_county_url if x not in l_county_url1]
                    print(l_county_url1)
                    d_county = List_PO.twoList2dict(l_county, l_county_url1)
                    d_city_county[k] = d_county
                    l_county = []
                    l_county_url = []
                    l_county_url1 = []
                    d_county = {}
                else:
                    for district in district_list:
                        if district.text == l_name[2]:
                            l_county.append(district.text)
                            l_county_url.append(self.get_prefix(province_url) + provincePrefixCode + "/" + district.get("href"))
                            districtPrefixCode = district.get("href")
                            # print(districtPrefixCode)
                            districtPrefixCode = districtPrefixCode.split("/")[0]
                            # print(l_county)
                            # print(l_county_url)
                            d_county = List_PO.twoList2dict(l_county, l_county_url)
                            d_city_county[k] = d_county
                            l_county = []
                            l_county_url = []
                            d_county = {}
        print(3, d_city_county)


        # {街道：url}
        # print(d_county2)
        for k, v in d_city_county.items():
            # if k == l_name[2]:
            # print(v)
            for k1, v1 in v.items():
                town_list = self.get_html(v1).select('tr.towntr a')
                # print(town_list)
                countyCode = v1.split(provincePrefixCode+"/")[1].split("/")[0]
                # print(countyCode)
                for town in town_list:
                    # print(town){'南京市': {'玄武区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/01/320102.html', '秦淮区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/01/320104.html', '建邺区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/01/320105.html', '鼓楼区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/01/320106.html', '浦口区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/01/320111.html', '栖霞区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/01/320113.html', '雨花台区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/01/320114.html', '江宁区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/01/320115.html', '六合区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/01/320116.html', '溧水区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/01/320117.html', '高淳区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/01/320118.html'}, '无锡市': {'锡山区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/02/320205.html', '惠山区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/02/320206.html', '滨湖区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/02/320211.html', '梁溪区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/02/320213.html', '新吴区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/02/320214.html', '江阴市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/02/320281.html', '宜兴市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/02/320282.html'}, '徐州市': {'鼓楼区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/03/320302.html', '云龙区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/03/320303.html', '贾汪区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/03/320305.html', '泉山区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/03/320311.html', '铜山区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/03/320312.html', '丰县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/03/320321.html', '沛县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/03/320322.html', '睢宁县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/03/320324.html', '徐州经济技术开发区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/03/320371.html', '新沂市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/03/320381.html', '邳州市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/03/320382.html'}, '常州市': {'天宁区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/04/320402.html', '钟楼区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/04/320404.html', '新北区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/04/320411.html', '武进区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/04/320412.html', '金坛区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/04/320413.html', '溧阳市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/04/320481.html'}, '苏州市': {'虎丘区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/05/320505.html', '吴中区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/05/320506.html', '相城区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/05/320507.html', '姑苏区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/05/320508.html', '吴江区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/05/320509.html', '苏州工业园区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/05/320571.html', '常熟市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/05/320581.html', '张家港市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/05/320582.html', '昆山市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/05/320583.html', '太仓市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/05/320585.html'}, '南通市': {'崇川区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/06/320602.html', '港闸区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/06/320611.html', '通州区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/06/320612.html', '如东县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/06/320623.html', '南通经济技术开发区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/06/320671.html', '启东市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/06/320681.html', '如皋市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/06/320682.html', '海门市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/06/320684.html', '海安市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/06/320685.html'}, '连云港市': {'连云区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/07/320703.html', '海州区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/07/320706.html', '赣榆区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/07/320707.html', '东海县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/07/320722.html', '灌云县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/07/320723.html', '灌南县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/07/320724.html', '连云港经济技术开发区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/07/320771.html', '连云港高新技术产业开发区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/07/320772.html'}, '淮安市': {'淮安区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/08/320803.html', '淮阴区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/08/320804.html', '清江浦区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/08/320812.html', '洪泽区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/08/320813.html', '涟水县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/08/320826.html', '盱眙县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/08/320830.html', '金湖县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/08/320831.html', '淮安经济技术开发区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/08/320871.html'}, '盐城市': {'亭湖区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/09/320902.html', '盐都区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/09/320903.html', '大丰区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/09/320904.html', '响水县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/09/320921.html', '滨海县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/09/320922.html', '阜宁县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/09/320923.html', '射阳县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/09/320924.html', '建湖县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/09/320925.html', '盐城经济技术开发区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/09/320971.html', '东台市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/09/320981.html'}, '扬州市': {'广陵区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/10/321002.html', '邗江区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/10/321003.html', '江都区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/10/321012.html', '宝应县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/10/321023.html', '扬州经济技术开发区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/10/321071.html', '仪征市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/10/321081.html', '高邮市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/10/321084.html'}, '镇江市': {'京口区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/11/321102.html', '润州区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/11/321111.html', '丹徒区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/11/321112.html', '镇江新区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/11/321171.html', '丹阳市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/11/321181.html', '扬中市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/11/321182.html', '句容市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/11/321183.html'}, '泰州市': {'海陵区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/12/321202.html', '高港区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/12/321203.html', '姜堰区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/12/321204.html', '泰州医药高新技术产业开发区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/12/321271.html', '兴化市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/12/321281.html', '靖江市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/12/321282.html', '泰兴市': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/12/321283.html'}, '宿迁市': {'宿城区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/13/321302.html', '宿豫区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/13/321311.html', '沭阳县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/13/321322.html', '泗阳县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/13/321323.html', '泗洪县': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/13/321324.html', '宿迁经济技术开发区': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/13/321371.html'}}

                    l_town.append(town.text)
                    l_town_url.append(self.get_prefix(province_url) + provincePrefixCode + "/" + countyCode + "/" + town.get("href"))
                    # print(l_town_url)
                    # townPrefixCode = town.get("href")
                    # print(townPrefixCode)
                # print(l_town_url)
                l_town = [x for x in l_town if l_town.index(x) % 2 != 0]
                [l_town_url1.append(x) for x in l_town_url if x not in l_town_url1]
                # break
                d_town = List_PO.twoList2dict(l_town, l_town_url1)
                d_town2 = d_town
                d_city_town[k1] = d_town
                l_town = []
                l_town_url = []
                l_town_url1 = []
                d_town = {}
            break
        # print(l_town)
        print(4, d_city_town)


        # [区划代码，城乡分类代码，名称]
        for k, v in d_city_town.items():
            # if k == l_name[2]:
            # print(v)
            for k1, v1 in v.items():
                village_list = self.get_html(v1).select('tr.villagetr td')
                for village in village_list:
                    l_village.append(village.text)
                List_PO.resolveList(l_village, 3)
                d_city_town_village[k1] = List_PO.resolveList(l_village, 3)
                l_village = []
            # break
        print(5, d_city_town_village)





    def update(self, varProvince):
        sign = 0
        # 判断是否有参数的sheet
        for j in range(len(self.Openpyxl_PO.getSheets())):
            if varProvince == self.Openpyxl_PO.getSheets()[j]:
                # 删除参数sheet
                self.Openpyxl_PO.delSheet(varProvince)
                # 原位置插入参数sheet
                self.Openpyxl_PO.addSheetCover(varProvince, j)
                sign = 1
                self.xx(varProvince)
        if sign == 0 :
            # 新增参数sheet
            self.Openpyxl_PO.addSheetCover(varProvince, 0)
            self.xx(varProvince)

    def update2(self, varProvince):
        sign = 0
        # 判断是否有参数的sheet
        for j in range(len(self.Openpyxl_PO.getSheets())):
            if varProvince == self.Openpyxl_PO.getSheets()[j]:
                sign = 1
                self.xx2(varProvince)
        if sign == 0 :
            # 新增参数sheet
            self.Openpyxl_PO.addSheetCover(varProvince, 0)
            self.xx2(varProvince)


    def xx(self, varArea):
        # 抓取省份页面
        province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html"
        province_list = self.get_html(province_url).select('tr.provincetr a')
        # print(province_list)  # [<a href="11.html">北京市<br/></a>, <a href="12.html">天津市<br/></a>,

        for province in province_list:
            province_name = province.text

            if province_name == varArea:
                href = province.get("href")
                province_code = href[0: 2] + "0000000000"

                # print(href)  # 31.html
                # print(province_code)  # 310000000000
                # print(province_name)  # 上海市

                # 添加上海市sheet
                self.Openpyxl_PO.addSheet(province_name)
                self.Openpyxl_PO.addOnRowValue([['区划代码', '地区', '区划代码', '名称', '区划代码', '名称', '区划代码', '名称', '区划代码', '名称']])

                # print(province_code)
                # print(province_name)
                # 输出：级别、区划代码、名称
                # content = "1\t" + province_code + "\t" + province_name
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
    def xx2(self, varArea):
        # 抓取省份页面
        province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html"
        province_list = self.get_html(province_url).select('tr.provincetr a')
        # print(province_list)  # [<a href="11.html">北京市<br/></a>, <a href="12.html">天津市<br/></a>,
        for province in province_list:
            if province.text == varArea:
                # print(self.get_prefix(province_url) + province.get("href"))
                # print(self.s)

                self.spider_next2(self.s, self.get_prefix(province_url) + province.get("href"), 2)

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

        # print(url)
        # print(spider_class)
        # print(self.get_html(url).select("tr." + spider_class + "tr"))
        for item in self.get_html(url).select("tr." + spider_class + "tr"):
            # print(item)
            item_td = item.select("td")
            # print(item_td)
            item_td_code = item_td[0].select_one("a")
            # print(item_td_code)
            item_td_name = item_td[1].select_one("a")
            # print(item_td_name)
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
            # 输出：级别、区划代码、名称
            # content2 = str(lev) + "\t" + item_code + "\t" + item_name
            # print(content2)
            # print(self.listMain)
            if lev == 2:

                self.d_city[item_code] = item_name

                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(item_code)
                self.list1.append(item_name)
            elif lev == 3:
                # 区

                self.d_county[item_code] = item_name

                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(item_code[:6])
                self.list1.append(item_name)
                # print([x for x in self.list1 if x is not None])
                self.l_county.append([x for x in self.list1 if x is not None])
            elif lev == 4:
                # 街道

                self.d_town[item_code] = item_name

                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                for i in range(len(self.l_county)):
                    if self.l_county[i][0] in item_code:
                        self.list1.append(self.l_county[i][0])
                        self.list1.append(self.l_county[i][1])
                self.list1.append(item_code[:9])
                self.list1.append(item_name)
                self.l_street.append([x for x in self.list1 if x is not None])
                # print(self.l_street)
            elif lev == 5:
                # 居委

                self.d_village[item_code] = item_name


                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                for i in range(len(self.l_county)):
                    if self.l_county[i][0] in item_code:
                        self.list1.append(self.l_county[i][0])
                        self.list1.append(self.l_county[i][1])
                for i in range(len(self.l_street)):
                    if self.l_street[i][2] in item_code:
                        self.list1.append(self.l_street[i][2])
                        self.list1.append(self.l_street[i][3])
                self.list1.append(item_code)
                self.list1.append(item_name)

            self.s = self.s+1
            # print(self.s, self.list1)
            print(self.d_city)
            print(self.d_county)
            print(self.d_town)
            print(self.d_village)
            self.Openpyxl_PO.setRowValue({self.s: self.list1})
            self.list1 = []

            if item_href is not None:
                self.Openpyxl_PO.save()
                # print(self.get_prefix(url)) # http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/31/01/
                # print(item_href) # 01/310101015.html
                self.spider_next(self.s, self.get_prefix(url) + item_href, lev + 1)
    def spider_next2(self, s, url, lev):

        print(s,url,lev)

        if lev == 2:
            spider_class = "city"
        elif lev == 3:
            spider_class = "county"
        elif lev == 4:
            spider_class = "town"
        else:
            spider_class = "village"

        # print(url)
        # print(spider_class)
        # print(self.get_html(url).select("tr." + spider_class + "tr"))
        for item in self.get_html(url).select("tr." + spider_class + "tr"):
            # print(item)
            # <tr class="citytr"><td><a href="32/3201.html">320100000000</a></td><td><a href="32/3201.html">南京市</a></td></tr>
            item_td = item.select("td")
            # print(item_td)
            # [<td><a href="32/3201.html">320100000000</a></td>, <td><a href="32/3201.html">南京市</a></td>]
            item_td_code = item_td[0].select_one("a")
            # print(item_td_code)
            # <a href="32/3201.html">320100000000</a>
            item_td_name = item_td[1].select_one("a")
            # print(item_td_name)
            # <a href="32/3201.html">南京市</a>

            # [94, '南京市', '秦淮区', '红花街道', None]


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

            # if item_name == "南京市" or item_name == '秦淮区' or item_name == '红花街道':
            #     pass
            # sys.exit(0)
            # 输出：级别、区划代码、名称
            # content2 = str(lev) + "\t" + item_code + "\t" + item_name
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
                self.l_county.append([x for x in self.list1 if x is not None])
            elif lev == 4:
                # 街道
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                self.list1.append(None)
                for i in range(len(self.l_county)):
                    if self.l_county[i][0] in item_code:
                        self.list1.append(self.l_county[i][0])
                        self.list1.append(self.l_county[i][1])
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
                for i in range(len(self.l_county)):
                    if self.l_county[i][0] in item_code:
                        self.list1.append(self.l_county[i][0])
                        self.list1.append(self.l_county[i][1])
                for i in range(len(self.l_street)):
                    if self.l_street[i][2] in item_code:
                        self.list1.append(self.l_street[i][2])
                        self.list1.append(self.l_street[i][3])
                self.list1.append(item_code)
                self.list1.append(item_name)

            self.s = self.s+1
            print(self.s, self.list1)
            # self.Openpyxl_PO.setRowValue({self.s: self.list1})
            self.list1 = []

            # sys.exit()

            if item_href is not None:
                self.Openpyxl_PO.save()
                # print(self.get_prefix(url)) # http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/31/01/
                # print(item_href) # 01/310101015.html
                self.spider_next2(self.s, self.get_prefix(url) + item_href, lev + 1)


# 入口
if __name__ == '__main__':

    # # l_city_url = ['http://', 'htt3201.html', 'http://www.statsstats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/32021.html', 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/32/3202.html']
    # l_city_url = [1,1,2,2]
    # print(set(l_city_url))
    # l_city_url = list(set(l_city_url))
    # # list1 = []
    #
    # print(l_city_url)

    ChinaAreaCode_PO = ChinaAreaCodePO("123.xlsx")

    # 下载（覆盖）
    ChinaAreaCode_PO.update("江苏省")


    # 断点续传，获取区列表，街道列表，居委会列表，从表格最后一条记录开始，与列表比对，并继续递归
    # ChinaAreaCode_PO.jixu("上海市")
    # ChinaAreaCode_PO.jixu("江苏省")

    # ChinaAreaCode_PO.update2("江苏省")


    # 获取列表
    # ChinaAreaCode_PO.getList(["江苏省", '', ''])
    # ChinaAreaCode_PO.getList(["上海市", '市辖区', '浦东新区', ""])
    # ChinaAreaCode_PO.getList(["江苏省", '常州市', '',''])


# https://www.json.cn/

# {"310000000000":"上海市"}
# {"310100000000":"市辖区"}
# {"310101":"黄浦区"}
# {"310101002":"南京东路街道"}
# {"310101002001":"云南中路居委会"}

# [{"code":"110000","name":"北京市","city":[{"code":"110100","name":"市辖区","county":[{"code":"110101","name":"东城区","town":[{"code":"222222","name":"南京东路街道","village":[{"code":"33333","name":"云南中路居委会"}]}]},{"code":"110102","name":"西城区"},{"code":"110105","name":"朝阳区"},{"code":"110106","name":"丰台区"},{"code":"110107","name":"石景山区"},{"code":"110108","name":"海淀区"},{"code":"110109","name":"门头沟区"},{"code":"110111","name":"房山区"},{"code":"110112","name":"通州区"},{"code":"110113","name":"顺义区"},{"code":"110114","name":"昌平区"},{"code":"110115","name":"大兴区"},{"code":"110116","name":"怀柔区"},{"code":"110117","name":"平谷区"},{"code":"110118","name":"密云区"},{"code":"110119","name":"延庆区"}]}]}]