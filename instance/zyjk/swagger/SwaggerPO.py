# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : 获取swagger内容 另存为excel
# http://192.168.0.238:8801/doc.html
# http://192.168.0.238:8801/saasuser/v2/api-docs
# http://192.168.0.238:8090/doc.html
# *********************************************************************

import requests, json, sys

sys.path.append("../../../../")
# sys.path.append("C:\Python39\Lib\site-packages")


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
# from PO.DomPO import *
# Dom_PO = DomPO(driver)

iUrl = 'http://192.168.0.238:8801'
iDoc = '/doc.html'


class SwaggerPO():

    def __init__(self):

        global d_all


    def getOne(self, iUrl, iDoc, varProject, toSave):

        Web_PO = WebPO("chrome")
        Web_PO.openURL(iUrl + iDoc)

        # 获取模块名
        l_project = Web_PO.getTexts("//option")
        # print(l_project)  # ['auth', 'oss', 'hypertension', 'ecg', 'cms', 'saascrf', 'cuser', 'saasuser']

        d_url = Web_PO.getTextsAndAttrs("//option", "data-url")
        # print(d_url)  # {'auth': '/v2/api-docs', 'oss': '/oss//v2/api-docs', 'hypertension': '/hypertension//v2/api-docs', 'ecg': '/ecg//v2/api-docs', 'cms': '/cms//v2/api-docs', 'saascrf': '/saascrf//v2/api-docs', 'cuser': '/cuser//v2/api-docs', 'saasuser': '/saasuser//v2/api-docs'}

        l_url = [iUrl + v for k, v in d_url.items()]
        # print(l_url)  # ['http://192.168.0.238:8801/v2/api-docs', 'http://192.168.0.238:8801/oss//v2/api-docs',...

        d_all = dict(zip(l_project, l_url))
        # print(d_all)  # {'auth': 'http://192.168.0.238:8801/v2/api-docs', 'oss': 'http://192.168.0.238:8801/oss//v2/api-docs', 'hypertension': 'http://192.168.0.238:8801/hypertension//v2/api-docs', 'ecg': 'http://192.168.0.238:8801/ecg//v2/api-docs', 'cms': 'http://192.168.0.238:8801/cms//v2/api-docs', 'saascrf': 'http://192.168.0.238:8801/saascrf//v2/api-docs', 'cuser': 'http://192.168.0.238:8801/cuser//v2/api-docs', 'saasuser': 'http://192.168.0.238:8801/saasuser//v2/api-docs'}



        html = requests.get(d_all[varProject])
        html.encoding = 'utf-8'
        # http://192.168.0.238:8801//v2/api-docs
        d = json.loads(html.text)
        # print(d['info']['description'])
        # print(d['basePath'])
        # print(d['tags'])
        # toSave = "i.xlsx"

        if os.path.isfile(toSave):
            pass
        else:
            Newexcel_PO = NewexcelPO(toSave)

        Openpyxl_PO = OpenpyxlPO(toSave)
        Openpyxl_PO.addCoverSheet(varProject)

        # Openpyxl_PO.setRowValue({1: ["tags", "summary", "paths", "method", "consumes", "query", "body", "parameters [参数名称，参数说明，请求类型，是否必须，数据类型，schema]"]})
        Openpyxl_PO.insertRows({1: ["tags", "summary", "paths", "method", "consumes", "query", "body", "parameters [参数名称，参数说明，请求类型，是否必须，数据类型，schema]"]})
        Openpyxl_PO.setRowColColor(1, "all", "ff0000")
        Openpyxl_PO.setRowColDimensions(1, 30, ['a', 'f'], 20)  # 设置第五行行高30，f - h列宽33
        Openpyxl_PO.setCellDimensions(1, 30, 'g', 40)
        Openpyxl_PO.setCellDimensions(1, 30, 'h', 80)
        Openpyxl_PO.setRowColFont(1, ["a", "h"], size=11, bold=True, italic=True)

        for i in range(len(d['tags'])):
            Openpyxl_PO.insertRows({i+2: [d['tags'][i]['name']]})
        Openpyxl_PO.save()

        # sys.exit(0)


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
                    # print(11, v['parameters'])
                    list1 = v['parameters']
                    # list1 = Str_PO.str2list(str(v['parameters']))
                    s = ""
                    # print(22,list1)
                    if 'in' in list1[0]:
                        for i in range(len(list1)):
                            # print(list1)
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
                d_parameters_sub3 = {}
                if 'parameters' in v:
                    # l_parameters = Str_PO.str2list(str(v['parameters']))
                    # print(l_parameters)
                    list2 = v['parameters']

                    if "in" in list2[0] and list2[0]['in'] == 'body' :
                        # print(d['definitions'])
                        for k, v in d['definitions'].items():

                            if "$ref" in list2[0]['schema']:
                                # print(l_parameters[0]['schema']['$ref'].split("#/definitions/")[1])
                                if k == list2[0]['schema']['$ref'].split("#/definitions/")[1]:  # ChatVO
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
                                                    elif v2['type'] == "integer" or v2['type'] == "number":
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
                                                                                        elif "integer" in v9['type'] or "number" in v9['type'] :
                                                                                            d_parameters_sub1[k9] = 0
                                                                                        elif v9['type'] == "array":
                                                                                            d_parameters_sub1[k9] = []
                                                                                            # ?


                                                                                            if "items" in v9:
                                                                                                for k16, v16 in d['definitions'].items():
                                                                                                    # print(1, "~~~~~~~~~`")
                                                                                                    if "$ref" in v9["items"]:
                                                                                                        # print(v2["items"]["$ref"].split("#/definitions/")[1])
                                                                                                        # sys.exit(0)
                                                                                                        if k16 == v9["items"]["$ref"].split("#/definitions/")[1] :  # SysRoleVO对象
                                                                                                            # print(d['definitions'][k6])

                                                                                                            for k17, v18 in d['definitions'][k16].items():
                                                                                                                if k17 == "properties":
                                                                                                                    # print(v18)
                                                                                                                    for k19, v19 in v18.items():
                                                                                                                        # print(v19)
                                                                                                                        if "type" in v19:
                                                                                                                            if "string" in v19['type']:
                                                                                                                                d_parameters_sub3[k19] = ""
                                                                                                                            elif "integer" in v19['type'] or "number" in v19['type'] :
                                                                                                                                d_parameters_sub3[k19] = 0
                                                                                                                            elif v19['type'] == "array":
                                                                                                                                d_parameters_sub3[k19] = []
                                                                                                                            elif v19['type'] == "boolean":
                                                                                                                                d_parameters_sub3[k19] = True
                                                                                                                            else:
                                                                                                                                d_parameters_sub3[k19] = '?'

                                                                                                d_parameters_sub1[k9] = [d_parameters_sub3]

                                                                                        elif v9['type'] == "boolean":
                                                                                            d_parameters_sub1[k9] = True
                                                                                        else:
                                                                                            d_parameters_sub1[k9] = '?'
                                                                # print(4, d_parameters_sub1)
                                                                else:
                                                                    d_parameters_sub1 = None
                                                        if d_parameters_sub1 == None:
                                                            d_parameters[k2] = []
                                                        else:
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
                                                                    elif "integer" in v99['type'] or "number" in v99['type']:
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
                            elif "items" in list2[0]['schema']:
                                # print(list2[0]['schema'])
                                # print(l_parameters[0]['schema']['items']['$ref'].split("#/definitions/")[1])
                                # if list2[0]['schema']['items']['$ref'] in list2[0]['schema']:
                                if '$ref' in list2[0]['schema']['items']:
                                    if k == list2[0]['schema']['items']['$ref'].split("#/definitions/")[1]:  # ChatVO
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
            Openpyxl_PO.setRows({i+2: l_all[i]})
        Openpyxl_PO.setAllWordWrap()
        Openpyxl_PO.setRowColAlignment(1, ["a", "h"], 'center', 'center')
        Openpyxl_PO.setFreeze('A2')

        Openpyxl_PO.save()
        print("ok => " + toSave)

        Web_PO.cls()

    def getAll(self, iUrl, iDoc, toSave):

        Web_PO = WebPO("chrome")
        Web_PO.openURL(iUrl + iDoc)

        # 获取模块名
        l_project = Web_PO.getTexts("//option")
        # print(l_project)  # ['auth', 'oss', 'hypertension', 'ecg', 'cms', 'saascrf', 'cuser', 'saasuser']

        d_url = Web_PO.getTextsAndAttrs("//option", "data-url")
        # print(d_url)  # {'auth': '/v2/api-docs', 'oss': '/oss//v2/api-docs', 'hypertension': '/hypertension//v2/api-docs', 'ecg': '/ecg//v2/api-docs', 'cms': '/cms//v2/api-docs', 'saascrf': '/saascrf//v2/api-docs', 'cuser': '/cuser//v2/api-docs', 'saasuser': '/saasuser//v2/api-docs'}

        l_url = [iUrl + v for k, v in d_url.items()]
        # print(l_url)  # ['http://192.168.0.238:8801/v2/api-docs', 'http://192.168.0.238:8801/oss//v2/api-docs',...

        d_all = dict(zip(l_project, l_url))
        # print(d_all)  # {'auth': 'http://192.168.0.238:8801/v2/api-docs', 'oss': 'http://192.168.0.238:8801/oss//v2/api-docs', 'hypertension': 'http://192.168.0.238:8801/hypertension//v2/api-docs', 'ecg': 'http://192.168.0.238:8801/ecg//v2/api-docs', 'cms': 'http://192.168.0.238:8801/cms//v2/api-docs', 'saascrf': 'http://192.168.0.238:8801/saascrf//v2/api-docs', 'cuser': 'http://192.168.0.238:8801/cuser//v2/api-docs', 'saasuser': 'http://192.168.0.238:8801/saasuser//v2/api-docs'}

        # 便利所有项
        for p in range(len(l_project)):

            # http://192.168.0.238:8801//v2/api-docs

            html = requests.get(d_all[l_project[p]])
            html.encoding = 'utf-8'
            d = json.loads(html.text)
            # print(d['info']['description'])
            # print(d['basePath'])
            # print(d['tags'])

            if os.path.isfile(toSave):
                pass
            else:
                Newexcel_PO = NewexcelPO(toSave)

            Openpyxl_PO = OpenpyxlPO(toSave)
            Openpyxl_PO.addCoverSheet(l_project[p])

            # Openpyxl_PO.setRowValue({1: ["tags", "summary", "paths", "method", "consumes", "query", "body", "parameters [参数名称，参数说明，请求类型，是否必须，数据类型，schema]"]})
            Openpyxl_PO.insertRows({1: ["tags", "summary", "paths", "method", "consumes", "query", "body", "parameters [参数名称，参数说明，请求类型，是否必须，数据类型，schema]"]})
            Openpyxl_PO.setRowColColor(1, "all", "ff0000")
            Openpyxl_PO.setRowColDimensions(1, 30, ['a', 'f'], 20)  # 设置第五行行高30，f - h列宽33
            Openpyxl_PO.setCellDimensions(1, 30, 'g', 40)
            Openpyxl_PO.setCellDimensions(1, 30, 'h', 80)
            Openpyxl_PO.setRowColFont(1, ["a", "h"], size=14, bold=False, italic=False)

            for i in range(len(d['tags'])):
                Openpyxl_PO.insertRows({i+2: [d['tags'][i]['name']]})
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
                    # print(l_project[p])
                    if l_project[p] == "auth":
                        l_i.append(paths)
                    else:
                        l_i.append("/" + l_project[p] + paths)
                    l_i.append(method)
                    if 'consumes' in v:
                        l_i.append(v['consumes'][0])
                    else:
                        l_i.append(None)

                    # query
                    if 'parameters' in v:
                        # print(11, v['parameters'])
                        list1 = v['parameters']
                        # list1 = Str_PO.str2list(str(v['parameters']))
                        s = ""
                        # print(22,list1)
                        if 'in' in list1[0]:
                            for i in range(len(list1)):
                                # print(list1)
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
                    d_parameters_sub3 = {}
                    if 'parameters' in v:
                        # l_parameters = Str_PO.str2list(str(v['parameters']))
                        # print(l_parameters)
                        list2 = v['parameters']

                        if "in" in list2[0] and list2[0]['in'] == 'body' :
                            # print(d['definitions'])
                            for k, v in d['definitions'].items():

                                if "$ref" in list2[0]['schema']:
                                    # print(l_parameters[0]['schema']['$ref'].split("#/definitions/")[1])
                                    if k == list2[0]['schema']['$ref'].split("#/definitions/")[1]:  # ChatVO
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
                                                        elif v2['type'] == "integer" or v2['type'] == "number":
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
                                                                                            elif "integer" in v9['type'] or "number" in v9['type'] :
                                                                                                d_parameters_sub1[k9] = 0
                                                                                            elif v9['type'] == "array":
                                                                                                d_parameters_sub1[k9] = []
                                                                                                # ?


                                                                                                if "items" in v9:
                                                                                                    for k16, v16 in d['definitions'].items():
                                                                                                        # print(1, "~~~~~~~~~`")
                                                                                                        if "$ref" in v9["items"]:
                                                                                                            # print(v2["items"]["$ref"].split("#/definitions/")[1])
                                                                                                            # sys.exit(0)
                                                                                                            if k16 == v9["items"]["$ref"].split("#/definitions/")[1] :  # SysRoleVO对象
                                                                                                                # print(d['definitions'][k6])

                                                                                                                for k17, v18 in d['definitions'][k16].items():
                                                                                                                    if k17 == "properties":
                                                                                                                        # print(v18)
                                                                                                                        for k19, v19 in v18.items():
                                                                                                                            # print(v19)
                                                                                                                            if "type" in v19:
                                                                                                                                if "string" in v19['type']:
                                                                                                                                    d_parameters_sub3[k19] = ""
                                                                                                                                elif "integer" in v19['type'] or "number" in v19['type'] :
                                                                                                                                    d_parameters_sub3[k19] = 0
                                                                                                                                elif v19['type'] == "array":
                                                                                                                                    d_parameters_sub3[k19] = []
                                                                                                                                elif v19['type'] == "boolean":
                                                                                                                                    d_parameters_sub3[k19] = True
                                                                                                                                else:
                                                                                                                                    d_parameters_sub3[k19] = '?'

                                                                                                    d_parameters_sub1[k9] = [d_parameters_sub3]

                                                                                            elif v9['type'] == "boolean":
                                                                                                d_parameters_sub1[k9] = True
                                                                                            else:
                                                                                                d_parameters_sub1[k9] = '?'
                                                                    # print(4, d_parameters_sub1)
                                                                    else:
                                                                        d_parameters_sub1 = None
                                                            if d_parameters_sub1 == None:
                                                                d_parameters[k2] = []
                                                            else:
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
                                                                        elif "integer" in v99['type'] or "number" in v99['type']:
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
                                elif "items" in list2[0]['schema']:
                                    # print(list2[0]['schema'])
                                    # print(l_parameters[0]['schema']['items']['$ref'].split("#/definitions/")[1])
                                    # if list2[0]['schema']['items']['$ref'] in list2[0]['schema']:
                                    if '$ref' in list2[0]['schema']['items']:
                                        if k == list2[0]['schema']['items']['$ref'].split("#/definitions/")[1]:  # ChatVO
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
                Openpyxl_PO.setRows({i+2: l_all[i]})
            Openpyxl_PO.setAllWordWrap()
            Openpyxl_PO.setRowColAlignment(1, ["a", "h"], 'center', 'center')
            Openpyxl_PO.setFreeze('A2')

            Openpyxl_PO.save()


        Web_PO.cls()
        print("ok => " + toSave)


if __name__ == '__main__':


    SwaggerPO_PO = SwaggerPO()
    
    SwaggerPO_PO.getAll('http://192.168.0.238:8801', '/doc.html','saas.xlsx')


    # SwaggerPO_PO.getOne('http://192.168.0.238:8801', '/doc.html', "auth", "auth.xlsx")
    # SwaggerPO_PO.getOne('http://192.168.0.238:8801', '/doc.html', "saasuser", "saasuser.xlsx")
    # SwaggerPO_PO.getOne('http://192.168.0.238:8801', '/doc.html',"cms", "cms.xlsx")
    # SwaggerPO_PO.getOne('http://192.168.0.238:8801', '/doc.html',"oss", "oss.xlsx")
    # SwaggerPO_PO.getOne('http://192.168.0.238:8801', '/doc.html',"saascrf", "saascrf.xlsx")
    # SwaggerPO_PO.getOne('http://192.168.0.238:8801', '/doc.html',"ecg", "ecg.xlsx")
    # SwaggerPO_PO.getOne('http://192.168.0.238:8801', '/doc.html',"cuser", "cuser.xlsx")
    # SwaggerPO_PO.getOne('http://192.168.0.238:8801', '/doc.html', "hypertension", "hypertension.xlsx")




    # SwaggerPO_PO.getOne('http://192.168.0.238:8090', '/doc.html', "default", "erp.xlsx")



