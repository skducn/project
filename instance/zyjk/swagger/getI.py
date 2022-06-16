# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : 获取swagger内容 另存为excel
# http://192.168.0.238:8801/doc.html
# *********************************************************************

import requests,json
from bs4 import BeautifulSoup
from PO.OpenpyxlPO import *
from PO.NewexcelPO import *
from PO.StrPO import *
Str_PO = StrPO()


# x = "[{'name': 'currentPage', 'in': 'query', 'description': '当前页码(必填)', 'required': True, 'type': 'integer', 'format': 'int32'}, {'name': 'docId', 'in': 'query', 'description': '医生id(当前登录用户id(必填))', 'required': True, 'type': 'integer', 'format': 'int32'}, {'name': 'itemId', 'in': 'query', 'description': '项目id(当前登录用户项目id(必填))', 'required': True, 'type': 'integer', 'format': 'int32'}, {'name': 'pageSize', 'in': 'query', 'description': '每页条数(必填)', 'required': True, 'type': 'integer', 'format': 'int32'}]"
# list1 = Str_PO.str2list(x)
# s = ""
# for i in range(len(list1)):
#     print(list1[i])
#     if list1[i]['in'] == 'query' and list1[i]['required'] == True:
#         s = s + list1[i]['name'] + "=" + "{" + list1[i]['type'] + "}&"
# print(s[:-1])  # currentPage={integer}&docId={integer}&itemId={integer}&pageSize={integer}
#
# x = "[{'in': 'body', 'name': 'chatVos', 'description': '数据对象', 'required': False, 'schema': {'type': 'array', 'items': {'$ref': '#/definitions/ChatVO'}}}]"
#
# # list1 = Str_PO.str2list(x)
# # print(list1[0]['schema']['items']['$ref'].split("#/definitions/")[1])
#
#
# x = "[{'in': 'body', 'name': 'chatVo', 'description': '数据对象', 'required': False, 'schema': {'$ref': '#/definitions/ChatVO'}}]"
#
# list1 = Str_PO.str2list(x)
#
# if "$ref" in list1[0]['schema']:
#     print(list1[0]['schema']['$ref'].split("#/definitions/")[1])
# elif "items" in list1[0]['schema']:
#     print(list1[0]['schema']['items']['$ref'].split("#/definitions/")[1])
#
# sys.exit(0)

url = 'http://192.168.0.238:8801/saasuser/v2/api-docs'
html = requests.get(url)
html.encoding = 'utf-8'
d = json.loads(html.text)
# print(d['basePath'])
# print(d['tags'])
toSave = "d://i.xlsx"

if os.path.isfile(toSave):
    Openpyxl_PO = OpenpyxlPO(toSave)
else:
    Newexcel_PO = NewexcelPO(toSave)
    Openpyxl_PO = OpenpyxlPO(toSave)
    Openpyxl_PO.addSheetCover("saasuser", 0)
    Openpyxl_PO.setRowValue({1: ["tags", "summary", "paths", "method", "consumes", "query", "body", "parameters [参数名称，参数说明，请求类型，是否必须，数据类型，schema]"]})
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
        l_i.append("/saasuser" + paths)
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
                        s = s + list1[i]['name'] + "=" + "{" + list1[i]['type'] + "}&"
                # print(s[:-1])  # currentPage={integer}&docId={integer}&itemId={integer}&pageSize={integer}
                l_i.append(str(s[:-1]))
                # print(str(s[:-1]))
            else:
                l_i.append(None)



        # body
        l_parameters = []
        d_parameters = {}
        if 'parameters' in v:
            l_parameters = Str_PO.str2list(str(v['parameters']))
            # print(l_parameters)
            # print(l_parameters[0]['in'])

            if "in" in l_parameters[0] and l_parameters[0]['in'] == 'body' :

                for k, v in d['definitions'].items():
                    print(l_parameters[0])
                    if "$ref" in l_parameters[0]['schema']:
                        print(l_parameters[0]['schema']['$ref'].split("#/definitions/")[1])
                        if k == l_parameters[0]['schema']['$ref'].split("#/definitions/")[1]:  # ChatVO
                            for k1, v1 in d['definitions'][k].items():
                                # if k1 == "required":
                                #     print(v1)
                                if k1 == "properties":
                                    # print(v1)
                                    for k2, v2 in v1.items():
                                        print(v2)

                                        if "type" in v2:
                                            if v2['type'] == "string":
                                                d_parameters[k2] = ""
                                            elif v2['type'] == "integer":
                                                d_parameters[k2] = 0
                                            elif v2['type'] == "array":
                                                d_parameters[k2] = []
                                            else:
                                                d_parameters[k2] = '?'

                            # print(d_parameters)
                            l_i.append(str(d_parameters))
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
                            l_i.append(str(d_parameters))
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
Openpyxl_PO.save()




