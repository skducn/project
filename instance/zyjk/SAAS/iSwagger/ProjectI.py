# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : 获取swagger内容 另存为excel
# http://192.168.0.238:8801/doc.html
# http://192.168.0.238:8801/saasuser/v2/api-docs
# *********************************************************************


import requests, json, sys

sys.path.append("../../../../")
sys.path.append("C:\Python39\Lib\site-packages")


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


iUrl = 'http://192.168.0.238:8801'
iDoc = '/doc.html'


class ProjectI():

    def __init__(self):

        global d_all

        # Web_PO = WebPO("chrome")
        # Web_PO.openURL(iUrl+iDoc)
        # # Web_PO.driver.maximize_window()  # 全屏
        # l_project = Web_PO.getXpathsText("//option")
        # l_url = Web_PO.getXpathsAttr("//option", "data-url")
        # # print(l_url)
        # l_url = [iUrl + i for i in l_url]
        # # l_url = ['http://192.168.0.238:8801' + i for i in l_url]
        # d_all = List_PO.twoList2dict(l_project, l_url)
        # # print(d_all)
        # #
        # # sys.exit(0)
        # Web_PO.closeURL()



    def getI(self, iUrl, iDoc, varProject, toSave):

        Web_PO = WebPO("chrome")
        Web_PO.openURL(iUrl + iDoc)
        l_project = Web_PO.getXpathsText("//option")
        l_url = Web_PO.getXpathsAttr("//option", "data-url")
        l_url = [iUrl + i for i in l_url]
        d_all = List_PO.twoList2dict(l_project, l_url)
        Web_PO.close()

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
        Openpyxl_PO.setRowColFont(1, ["a", "h"], size=11, bold=True, italic=True)

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

                # if v['summary'] == "新增系统管理用户":
                # print(v)
                # sys.exit(0)
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
                d_parameters_sub1 = {}
                d_parameters_sub2 = {}
                if 'parameters' in v:
                    l_parameters = Str_PO.str2list(str(v['parameters']))
                    # print(l_parameters)


                    if "in" in l_parameters[0] and l_parameters[0]['in'] == 'body' :
                        # print(d['definitions'])
                        for k, v in d['definitions'].items():

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

                                                        # print(v2["items"]["$ref"].split("#/definitions/")[1])
                                                        # print(3, v2)
                                                        if "items" in v2:
                                                            for k6, v6 in d['definitions'].items():
                                                                # print(1, "~~~~~~~~~`")
                                                                if "$ref" in v2["items"]:
                                                                    # print(v2["items"]["$ref"].split("#/definitions/")[1])
                                                                    # sys.exit(0)
                                                                    if k6 == v2["items"]["$ref"].split("#/definitions/")[1] :  # SysRoleVO对象
                                                                        # print(d['definitions'][k6])

                                                                        for k7, v8 in d['definitions'][k6].items():
                                                                            if k7 == "properties":
                                                                                # print(v8)
                                                                                for k9, v9 in v8.items():
                                                                                    # print(v9)
                                                                                    if "type" in v9:
                                                                                        if "string" in v9['type']:
                                                                                            d_parameters_sub1[k9] = ""
                                                                                        elif "integer" in v9['type']:
                                                                                            d_parameters_sub1[k9] = 0
                                                                                        elif v9['type'] == "array":
                                                                                            d_parameters_sub1[k9] = []
                                                                                        elif v9['type'] == "boolean":
                                                                                            d_parameters_sub1[k9] = True
                                                                                        else:
                                                                                            d_parameters_sub1[k9] = '?'
                                                            # print(4, d_parameters_sub1)
                                                        d_parameters[k2] = [d_parameters_sub1]

                                                    else:
                                                        d_parameters[k2] = '?'

                                                if "$ref" in v2:   # {'description': '用户登录信息详情', '$ref': '#/definitions/SysUserVO对象'}
                                                    # print(v2["$ref"].split("#/definitions/")[1])
                                                    # print(v2["$ref"].split("#/definitions/")[1][:-2])
                                                    # d_parameters[v2["$ref"].split("#/definitions/")[1][:-2]] = {}  # 增加 SysUserVO 键

                                                    # print(9,d['definitions'][v2["$ref"].split("#/definitions/")[1]])
                                                    for k77, v88 in d['definitions'][v2["$ref"].split("#/definitions/")[1]].items():
                                                        if k77 == "properties":
                                                            # print(v8)
                                                            for k99, v99 in v88.items():
                                                                # print(v9)
                                                                if "type" in v99:
                                                                    if "string" in v99['type']:
                                                                        d_parameters_sub2[k99] = ""
                                                                    elif "integer" in v99['type']:
                                                                        d_parameters_sub2[k99] = 0
                                                                    elif v99['type'] == "array":
                                                                        d_parameters_sub2[k99] = []
                                                                    elif v99['type'] == "boolean":
                                                                        d_parameters_sub2[k99] = True
                                                                    else:
                                                                        d_parameters_sub2[k99] = '?'
                                                    d_parameters[v2["$ref"].split("#/definitions/")[1][:-2]] = d_parameters_sub2


                                    # print(5, d_parameters)
                                    # l_i.append(str(d_parameters))
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
            # print(l_all)
            l_i = []

        for i in range(len(l_all)):
            Openpyxl_PO.setRowValue({i+2: l_all[i]})
        Openpyxl_PO.setAllWordWrap()
        Openpyxl_PO.setRowColAlignment(1, ["a", "h"], 'center', 'center')
        Openpyxl_PO.setFreeze('A2')

        Openpyxl_PO.save()


if __name__ == '__main__':

    Sys_PO.killPid('EXCEL.EXE')

    project_I = ProjectI()

    # project_I.getI("auth", "i.xlsx")
    # project_I.getI("saasuser", "saasuser.xlsx")
    # project_I.getI("cms")
    # project_I.getI("oss")
    # project_I.getI("saascrf")
    # project_I.getI("ecg")
    # project_I.getI("cuser")
    # project_I.getI("hypertension")

    # project_I.getI('http://192.168.0.238:8801', '/doc.html', "saasuser", "saasuser.xlsx")
    project_I.getI('http://192.168.0.238:8801', '/doc.html', "saasuser", "i_sassuser_swagger_case.xlsx")


