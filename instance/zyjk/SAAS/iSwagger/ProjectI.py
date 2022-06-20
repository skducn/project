# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : 获取swagger内容 另存为excel
# http://192.168.0.238:8801/doc.html
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


iUrl = 'http://192.168.0.238:8801'
iDoc = '/doc.html'


class ProjectI():

    def __init__(self):

        global d_all

        Web_PO = WebPO("chrome")
        Web_PO.openURL(iUrl+iDoc)
        # Web_PO.driver.maximize_window()  # 全屏
        l_project = Web_PO.getXpathsText("//option")
        l_url = Web_PO.getXpathsAttr("//option", "data-url")
        # print(l_url)
        l_url = [iUrl + i for i in l_url]
        # l_url = ['http://192.168.0.238:8801' + i for i in l_url]
        d_all = List_PO.twoList2dict(l_project, l_url)
        # print(d_all)
        #
        # sys.exit(0)
        Web_PO.closeURL()



    def getI(self, varProject, toSave):

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
                if 'parameters' in v:
                    l_parameters = Str_PO.str2list(str(v['parameters']))
                    # print(l_parameters)
                    # print(l_parameters[0]['in'])

                    if "in" in l_parameters[0] and l_parameters[0]['in'] == 'body' :

                        for k, v in d['definitions'].items():
                            # print(l_parameters[0])
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


if __name__ == '__main__':

    Sys_PO.killPid('EXCEL.EXE')

    project_I = ProjectI()

    # project_I.getI("auth", "i.xlsx")
    project_I.getI("saasuser", "saasuser.xlsx")
    # project_I.getI("cms")
    # project_I.getI("oss")
    # project_I.getI("saascrf")
    # project_I.getI("ecg")
    # project_I.getI("cuser")
    # project_I.getI("hypertension")

