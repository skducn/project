# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : 2020 年全国统计用区划代码
# 五级行政区域划分API接口 https://www.wenjiangs.com/api/v2/xzqh
# 可选参数 code    https://www.wenjiangs.com/api/v2/xzqh?code=110100000000
# 三级行政区域划分API接口 https://www.wenjiangs.com/api/v2/xzqhSimple

# 参考：https://www.wenjiangs.com/division?code=350725203000
# *********************************************************************

import requests,json,sys
from bs4 import BeautifulSoup
from PO.OpenpyxlPO import *
from PO.NewexcelPO import *

from PO.StrPO import *
Str_PO = StrPO()

from PO.ListPO import *
List_PO = ListPO()

from PO.SysPO import *
Sys_PO = SysPO()

from PO.WebPO import *


# iUrl = 'https://www.wenjiangs.com/api/v2/xzqh'
# iUrl = 'https://www.wenjiangs.com/api/v2/xzqh?code=110100000000'
# iUrl = 'https://www.wenjiangs.com/api/v2/xzqhSimple'

class XzqhPO():

    def __init__(self):

        global d_all


    def getI(self, iUrl, iDoc, varProject, toSave):

        Web_PO = WebPO("chrome")
        Web_PO.openURL(iUrl + iDoc)
        l_project = Web_PO.getXpathsText("//option")
        l_url = Web_PO.getXpathsAttr("//option", "data-url")
        l_url = [iUrl + i for i in l_url]
        d_all = List_PO.twoList2dict(l_project, l_url)
        Web_PO.closeURL()

        html = requests.get(d_all[varProject])
        html.encoding = 'utf-8'
        d = json.loads(html.text)
        # print(d['basePath'])
        # print(d['tags'])
        # toSave = "i.xlsx"

        if os.path.isfile(toSave):
            pass
        else:
            Newexcel_PO = NewexcelPO(toSave)

        Openpyxl_PO = OpenpyxlPO(toSave)
        Openpyxl_PO.addSheetCover(varProject)

        Openpyxl_PO.setRowValue({1: ["tags", "summary", "paths", "method", "consumes", "query", "body", "parameters [参数名称，参数说明，请求类型，是否必须，数据类型，schema]"]})
        Openpyxl_PO.setRowColColor(1, "all", "ff0000")
        Openpyxl_PO.setRowColDimensions(1, 30, ['a', 'f'], 20)  # 设置第五行行高30，f - h列宽33
        Openpyxl_PO.setCellDimensions(1, 30, 'g', 40)
        Openpyxl_PO.setCellDimensions(1, 30, 'h', 80)
        Openpyxl_PO.setRowColFont(1, ["a", "h"],  size=11)

        for i in range(len(d['tags'])):
            Openpyxl_PO.setRowValue({i+2: [d['tags'][i]['name']]})
        Openpyxl_PO.save()

        l_i = []
        l_all = []


        # 接口地址
        for paths, v in d['paths'].items():
            # print(paths)  # /afPreoperativeCounselingInfo/addMassMessage
            # print(d['paths'][paths])
            for method, v in d['paths'][paths].items():
                # print(method)  # post
                # print(v['tags'])  # ['医患交流信息表接口']
                # print(v['summary'])  # 群发消息-PC
                # print(v['consumes'])  # ['application/json']
                # print(v['parameters'])
                # print(d['paths'][paths])
                # print(v)
                # sys.exit(0)

                l_i.append(v['tags'][0])
                l_i.append(v['summary'])
                if varProject == "auth":
                    l_i.append(paths)
                else:
                    l_i.append("/" + varProject + paths)
                l_i.append(method)
                if 'consumes' in v:
                    l_i.append(v['consumes'][0])
                else:
                    l_i.append(None)

                # query
                if 'parameters' in v:
                    # print(v['parameters'])
                    list1 = Str_PO.str2list(str(v['parameters']))
                    s = ""
                    # print(list1)
                    if 'in' in list1[0]:
                        for i in range(len(list1)):
                            # print(list1[i])
                            if list1[i]['in'] == 'query' and list1[i]['required'] == True:
                                s = s + list1[i]['name'] + "=" + "{*" + list1[i]['type'] + "}&"
                            if list1[i]['in'] == 'query' and list1[i]['required'] == False:
                                s = s + list1[i]['name'] + "=" + "{" + list1[i]['type'] + "}&"
                        # print(s[:-1])  # currentPage={integer}&docId={integer}&itemId={integer}&pageSize={integer}
                        l_i.append(str(s[:-1]))
                        # print(str(s[:-1]))
                    else:
                        l_i.append(None)



                # body
                l_parameters = []
                d_parameters = {}

                d_parameters_1 = {}
                l_parameters_1 = []

                d_parameters_2 = {}
                l_parameters_2 = []

                if 'parameters' in v:
                    l_parameters = Str_PO.str2list(str(v['parameters']))
                    # print(l_parameters)
                    # print(l_parameters[0]['in'])

                    if "in" in l_parameters[0] and l_parameters[0]['in'] == 'body' :

                        for k, v in d['definitions'].items():
                            # print(l_parameters[0])
                            # print(k)
                            if "$ref" in l_parameters[0]['schema']:
                                # print(l_parameters[0]['schema']['$ref'].split("#/definitions/")[1])
                                if k == l_parameters[0]['schema']['$ref'].split("#/definitions/")[1]:  # ChatVO
                                    for k1, v1 in d['definitions'][k].items():
                                        # if k1 == "required":
                                        #     print(v1)
                                        if k1 == "properties":
                                            # print(v1)
                                            for k2, v2 in v1.items():
                                                # print(v2)

                                                if "type" in v2:
                                                    if v2['type'] == "string":
                                                        d_parameters[k2] = ""
                                                    elif v2['type'] == "integer":
                                                        d_parameters[k2] = 0
                                                    elif v2['type'] == "array":
                                                        # d_parameters[k2] = []

                                                        # 第二层array
                                                        if "items" in v2:
                                                            if "$ref" in v2['items']:
                                                                # print(v2['items']['$ref'].split("#/definitions/")[1])
                                                                # print(k)
                                                                for k9, v in d['definitions'].items():
                                                                    if k9 == v2['items']['$ref'].split("#/definitions/")[1]:  # 会议反馈人员记录DTO
                                                                        for k10, v10 in d['definitions'][k9].items():
                                                                            if k10 == "properties":
                                                                                # print(v1)
                                                                                for k20, v20 in v10.items():
                                                                                    # print(v20)
                                                                                    if "type" in v20:
                                                                                        if v20['type'] == "string":
                                                                                            d_parameters_1[k20] = ""
                                                                                        elif v20['type'] == "integer":
                                                                                            d_parameters_1[k20] = 0
                                                                                        elif v20['type'] == "array":
                                                                                            d_parameters_1[k20] = []

                                                                                            # 第三层array
                                                                                            for k119, v in d['definitions'].items():
                                                                                                # print(v20['items'])
                                                                                                if "$ref" in v20['items']:
                                                                                                    if k119 == v20['items']['$ref'].split("#/definitions/")[1]:  # 产品观念DTO
                                                                                                        # print(k119)
                                                                                                        for k100, v100 in d['definitions'][k119].items():
                                                                                                            if k100 == "properties":
                                                                                                                for k200, v200 in v100.items():
                                                                                                                    # print(v200)
                                                                                                                    if "type" in v200:
                                                                                                                        if v200['type'] == "string":
                                                                                                                            d_parameters_2[k200] = ""
                                                                                                                        elif v200['type'] == "integer":
                                                                                                                            d_parameters_2[k200] = 0
                                                                                                                        elif v200['type'] == "array":
                                                                                                                            d_parameters_2[k200] = []
                                                                                                                l_parameters_2.append(d_parameters_2)
                                                                                                                # print(l_parameters_2)
                                                                                                                d_parameters_1[k20] = l_parameters_2


                                                                                l_parameters_1.append(d_parameters_1)
                                                                                d_parameters[k2] = l_parameters_1

                                                    elif v2['type'] == "number":
                                                        d_parameters[k2] = 0.00
                                                    else:
                                                        d_parameters[k2] = '?'



                                    # print(d_parameters)
                                    # print(json.dumps(d_parameters))
                                    l_i.append(json.dumps(d_parameters))
                                    break
                            elif "items" in l_parameters[0]['schema']:
                                # print(l_parameters[0]['schema']['items']['$ref'].split("#/definitions/")[1])
                                if k == l_parameters[0]['schema']['items']['$ref'].split("#/definitions/")[1]:  # ChatVO
                                    for k1, v1 in d['definitions'][k].items():
                                        # if k1 == "required":
                                        #     print(v1)
                                        if k1 == "properties":
                                            # print(v1)
                                            for k2, v2 in v1.items():
                                                if v2['type'] == "string":
                                                    d_parameters[k2] = ""
                                                elif v2['type'] == "integer":
                                                    d_parameters[k2] = 0
                                    # print(d_parameters)
                                    # l_i.append(str(d_parameters))
                                    l_i.append(json.dumps(d_parameters))
                                    break
                    else:
                        l_i.append(None)


                # parameters
                if 'parameters' in v:
                    l_i.append(str(v['parameters']))
                else:
                    l_i.append(None)

            l_all.append(l_i)
            l_i = []

        for i in range(len(l_all)):
            Openpyxl_PO.setRowValue({i+2: l_all[i]})
        Openpyxl_PO.setAllWordWrap()
        Openpyxl_PO.setRowColAlignment(1, ["a", "h"], 'center', 'center')
        Openpyxl_PO.setFreeze('A2')
        Openpyxl_PO.save()

        print("[Done] => " + toSave)

    def getFive(self, varProvince):
        html = requests.get("https://www.wenjiangs.com/api/v2/xzqh")
        html.encoding = 'utf-8'
        l_province = json.loads(html.text)
        # print(l_province)
        # print(len(l_province))
        for i in range(len(l_province)):
            # print(l_province[i])
            for j in range(len(l_province[i])):
                if l_province[i]['name'] == varProvince:
                    print(l_province[i]['code'])
                    break

    def getArea(self, varCode):
        html = requests.get("https://www.wenjiangs.com/api/v2/xzqh?code=" + str(varCode))
        html.encoding = 'utf-8'
        l_area = json.loads(html.text)
        print(l_area)
        print(len(l_area))
        for i in range(len(l_area)):
            print(l_area[i])
            # for j in range(len(l_province[i])):
            #     if l_province[i]['name'] == varProvince:
            #         print(l_province[i]['code'])
            #         break

if __name__ == '__main__':

    Sys_PO.killPid('EXCEL.EXE')

    Xzqh_PO = XzqhPO()

    code = Xzqh_PO.getFive("上海市")

    Xzqh_PO.getArea(code)
    #
    # Xzqh_PO.getThree('上海市', '市辖区', "auth", "auth.xlsx")
    # Xzqh_PO.getThree('江苏省', '南京市', "市辖区", "auth.xlsx")




