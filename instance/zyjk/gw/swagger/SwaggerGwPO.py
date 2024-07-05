# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : swagger库
# http://192.168.0.203:38080/doc.html
# https://www.sojson.com/
# *********************************************************************

iUrl = 'http://192.168.0.203:38080'
iDoc = '/doc.html'

import json

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.WebPO import *

from urllib.parse import quote, unquote
# quote和unquote函数来进行URL编码和解码。

class SwaggerGwPO():

    def _getInterfaceUrl(self, varMenu):

        # 获取接口页面地址
        Web_PO = WebPO("noChrome")
        Web_PO.openURL(iUrl + iDoc)

        # 1.1 获取菜单名
        l_menu = Web_PO.getTextListByX("//option")
        # print(l_project)  # ['phs-auth', 'phs-job', 'phs-system', 'phs-server', 'phs-server-export', 'phs-third-api']
        # 1.2 获取菜单与url键值对
        d_url = Web_PO.getTextAttrValueDictByX("//option", "data-url")
        # print(d_url)  # {'auth': '/v2/api-docs', 'oss': '/oss//v2/api-docs', 'hypertension': '/hypertension//v2/api-docs', 'ecg': '/ecg//v2/api-docs', 'cms': '/cms//v2/api-docs', 'saascrf': '/saascrf//v2/api-docs', 'cuser': '/cuser//v2/api-docs', 'saasuser': '/saasuser//v2/api-docs'}
        # 1.3 合成列表
        l_url = [iUrl + v for k, v in d_url.items()]
        # print(l_url)  # ['http://192.168.0.203:38080/auth/v2/api-docs', 'http://192.168.0.203:38080/schedule/v2/api-docs', 'http://192.168.0.203:38080/system/v2/api-docs', 'http://192.168.0.203:38080/server/v2/api-docs', 'http://192.168.0.203:38080/serverExport/v2/api-docs', 'http://192.168.0.203:38080/thirdApi/v2/api-docs']
        # 1.4 合成字典
        d_interfaceUrl = dict(zip(l_menu, l_url))
        # print(d_all)  # {'phs-auth': 'http://192.168.0.203:38080/auth/v2/api-docs', 'phs-job': 'http://192.168.0.203:38080/schedule/v2/api-docs', 'phs-system': 'http://192.168.0.203:38080/system/v2/api-docs', 'phs-server': 'http://192.168.0.203:38080/server/v2/api-docs', 'phs-server-export': 'http://192.168.0.203:38080/serverExport/v2/api-docs', 'phs-third-api': 'http://192.168.0.203:38080/thirdApi/v2/api-docs'}
        Web_PO.cls()

        print(d_interfaceUrl[varMenu])  # http://192.168.0.203:38080/thirdApi/v2/api-docs
        html = requests.get(d_interfaceUrl[varMenu])
        html.encoding = 'utf-8'
        d = json.loads(html.text)
        return d
    def _traversalDict(self, d, d_parametersMemo):

        # 遍历迭代检查是否有下级originalRef，并获取参数

        d1 = {}
        for k, v in d_parametersMemo.items():
            for k1, v1 in v.items():
                if k1 == 'originalRef':
                    # print(k, d['definitions'][v1]['properties'])  # {'id': {'type': 'integer', 'format': 'int32', 'description': 'ID'}, 'recordId': {'type': 'string', 'description': '编号'}, 'sfjlid': {'type': 'string', 'description': '糖尿病随访卡ID'}, 'ywcd': {'type': 'string', 'description': '药物编码'}, 'ywjl': {'type': 'string', 'description': '单次使用药物剂量'}, 'ywmc': {'type': 'string', 'description': '药物名称'}, 'ywpl': {'type': 'string', 'description': '药物使用频率'}}
                    d1[k] = d['definitions'][v1]['properties']
                    # print(111,d1[k])

                    # 下下级
                    for k2, v2 in d1[k].items():
                        for k3, v3 in v2.items():
                            if k3 == 'originalRef':
                                # print(k, k1, d['definitions'][v3]['properties'])  # {'id': {'type': 'integer', 'format': 'int32', 'description': 'ID'}, 'recordId': {'type': 'string', 'description': '编号'}, 'sfjlid': {'type': 'string', 'description': '糖尿病随访卡ID'}, 'ywcd': {'type': 'string', 'description': '药物编码'}, 'ywjl': {'type': 'string', 'description': '单次使用药物剂量'}, 'ywmc': {'type': 'string', 'description': '药物名称'}, 'ywpl': {'type': 'string', 'description': '药物使用频率'}}
                                d1[k][k2] = d['definitions'][v3]['properties']
                            if k3 == 'items':
                                if 'originalRef' in v3:
                                    # print(6, k, k2, d['definitions'][v3['originalRef']]['properties'])  # {'id': {'type': 'integer', 'format': 'int32', 'description': 'ID'}, 'recordId': {'type': 'string', 'description': '编号'}, 'sfjlid': {'type': 'string', 'description': '糖尿病随访卡ID'}, 'ywcd': {'type': 'string', 'description': '药物编码'}, 'ywjl': {'type': 'string', 'description': '单次使用药物剂量'}, 'ywmc': {'type': 'string', 'description': '药物名称'}, 'ywpl': {'type': 'string', 'description': '药物使用频率'}}
                                    d1[k][k2] = d['definitions'][v3['originalRef']]['properties']
                if k1 == 'items':
                    if 'originalRef' in v1:
                        # print(v1['originalRef'])  # TnbSfyyInfoResponse
                        # print(3, k, d['definitions'][v1['originalRef']]['properties']) # {'id': {'type': 'integer', 'format': 'int32', 'description': 'ID'}, 'recordId': {'type': 'string', 'description': '编号'}, 'sfjlid': {'type': 'string', 'description': '糖尿病随访卡ID'}, 'ywcd': {'type': 'string', 'description': '药物编码'}, 'ywjl': {'type': 'string', 'description': '单次使用药物剂量'}, 'ywmc': {'type': 'string', 'description': '药物名称'}, 'ywpl': {'type': 'string', 'description': '药物使用频率'}}
                        d1[k] = d['definitions'][v1['originalRef']]['properties']

        # d1覆盖d_parametersMemo中已存在的key
        d_body = {**d_parametersMemo, **d1}
        return d_body

        # 将参数格式化
        # d3 = self.formatParameters(d_body)
        # sys.exit(0)

    def getOne(self, varMenu, varTags, varSummary):

        # 获取一个接口的信息

        l_1 = []
        varQuery = ''
        d_body = {}

        # 1 获取并解析接口页面地址
        d = self._getInterfaceUrl(varMenu)

        # 2 遍历接口
        for k, v in d['paths'].items():

            # 2.1 路径
            paths = k
            # print(paths)  # /afPreoperativeCounselingInfo/addMassMessage

            # 2.2 提交方式
            l_method = list(d['paths'][k])
            # print(l_method[0]) # POST

            # 2.3 接口标签
            tags = d['paths'][k][l_method[0]]['tags'][0]
            # print(tags)  # REST - 第三方模块糖尿病接口

            # 2.4 接口名
            summary = d['paths'][k][l_method[0]]['summary']
            # print(summary) # 保存第三方糖尿病随访
            # print(tags, summary)  # 保存第三方糖尿病随访
            # Color_PO.consoleColor2({"31": tags, "32": summary})

            # 2.5 operationId
            operationId = d['paths'][k][l_method[0]]['operationId']
            # print(operationId)

            # get 或 delete 没有consumes
            if varTags == tags and varSummary == summary:

                # 编码中文
                q_varTags = quote(varTags)  # http://192.168.0.203:38080/doc.html#/phs-server/%E6%AE%8B%E7%96%BE%E4%BA%BA%E7%AE%A1%E7%90%86-%E4%B8%93%E9%A1%B9%E7%99%BB%E8%AE%B0/findPageUsingPOST_5
                varUrl = iUrl + iDoc + "#/" + varMenu + "/" + q_varTags + "/" + operationId

                # 条件标题和链接地址
                print(Color_PO.getColor({"32": [varMenu, varTags, varSummary]}) + "=> " + varUrl)

                if l_method[0] == 'post' or l_method[0] == 'put':
                    # 2.6 content-type内容类型
                    consumes = d['paths'][k][l_method[0]]['consumes'][0]
                    # print(consumes)  # 'application/json'
                else:
                    consumes = ''

                # 2.7 获取body参数（通过originalRef定位）
                if 'parameters' in d['paths'][k][l_method[0]]:
                    l_parameters = d['paths'][k][l_method[0]]['parameters']
                    # print(l_parameters)  # [{'in': 'body', 'name': 'body', 'description': 'body', 'required': True, 'schema': {'$ref': '#/definitions/ThridTnbSfListInfoResponse', 'originalRef': 'ThridTnbSfListInfoResponse'}}]
                    if len(l_parameters) == 1:
                        # 1个参数
                        if l_parameters[0]['in'] == 'body':
                            # todo body
                            if 'originalRef' in l_parameters[0]['schema']:
                                # 'schema': {'$ref': '#/definitions/ThridTnbSfListInfoResponse', 'originalRef': 'ThridTnbSfListInfoResponse'}}]
                                originalRef = l_parameters[0]['schema']['originalRef']
                                d_parametersMemo = d['definitions'][originalRef]['properties']
                                print('1参body =>', d_parametersMemo)  # {'ccsffl': {'type': 'string', 'description': '随访评价结果代码'},...
                            elif 'items' in l_parameters[0]['schema']:
                                # 'schema': {'type': 'array', 'items': {'$ref': '#/definitions/PerformRequest', 'originalRef': 'PerformRequest'}
                                if 'originalRef' in l_parameters[0]['schema']['items']:
                                    originalRef = l_parameters[0]['schema']['items']['originalRef']
                                    d_parametersMemo = d['definitions'][originalRef]['properties']
                                    print('1参body(items) =>', d_parametersMemo)
                                else:
                                    # 'schema': {'type': 'array', 'items': {'type': 'integer', 'format': 'int32'}}}]
                                    if 'type' in l_parameters[0]['schema']:
                                        if l_parameters[0]['schema']['type'] == 'array':
                                            # 参数不是字典，是数组
                                            print('1参body数组 =>', l_parameters[0])
                                            d_parametersMemo = {}
                            # # 遍历检查是否有下级originalRef，并获取参数
                            d_body = self._traversalDict(d, d_parametersMemo)
                            print('1参body遍历 =>', d_body)
                        elif l_parameters[0]['in'] == 'query' or l_parameters[0]['in'] == 'path':
                            # todo query
                            varQuery = l_parameters[0]['name'] + "={" + l_parameters[0]['type'] + "}"
                            d_body = ''
                    else:
                        # 多个参数
                        s = ''
                        for i in range(len(l_parameters)):
                            # print(l_parameters)
                            if l_parameters[i]['in'] == 'body':
                                # todo body
                                originalRef = l_parameters[i]['schema']['originalRef']
                                d_parametersMemo = d['definitions'][originalRef]['properties']
                                print('多参body =>', d_parametersMemo)  # {'ccsffl': {'type': 'string', 'description': '随访评价结果代码'},...
                                # 遍历检查是否有下级originalRef，并获取参数
                                d_body = self._traversalDict(d, d_parametersMemo)
                            if l_parameters[i]['in'] == 'query' or l_parameters[i]['in'] == 'path':
                                # todo query
                                varQuery = l_parameters[i]['name'] + "={" + l_parameters[i]['type'] + "}"
                                s = s + varQuery + ','
                                if len(d_body) < 1:
                                    d_body = ''
                        varQuery = s[:-1]
                        print('多参query =>', varQuery)
                else:
                    # 没有参数，即get
                    d_body = ''

                # 2.8 生成列表
                l_1.append(tags)
                l_1.append(summary)
                l_1.append(paths)
                l_1.append(l_method[0])
                l_1.append(consumes)
                l_1.append(varQuery)  # query
                l_1.append(str(d_body))  # body
                l_1.append(varUrl)

                varQuery = ''
                s = ''
                d_body = {}

                # print(l_1)
                Color_PO.consoleColor2({"35": l_1})
                break

    def getAll(self, varMenu):

        l_all = []
        l_1 = []
        c = 0
        varQuery = ''
        d_body = {}

        # 1 获取并解析接口页面地址
        d = self._getInterfaceUrl(varMenu)


        # 2 遍历接口
        for k, v in d['paths'].items():

            # 2.1 路径
            paths = k
            # print(paths)  # /afPreoperativeCounselingInfo/addMassMessage

            # 2.2 提交方式
            l_method = list(d['paths'][k])
            # print(l_method[0]) # POST

            # 2.3 接口标签
            tags = d['paths'][k][l_method[0]]['tags'][0]
            # print(tags)  # REST - 第三方模块糖尿病接口

            # 2.4 接口名
            summary = d['paths'][k][l_method[0]]['summary']
            # print(summary) # 保存第三方糖尿病随访
            # print(tags, summary) # 保存第三方糖尿病随访
            # Color_PO.consoleColor2({"31": tags, "32": summary})

            # 2.5 operationId
            operationId = d['paths'][k][l_method[0]]['operationId']
            # print(operationId)

            # 编码中文
            q_varTags = quote(tags)  # http://192.168.0.203:38080/doc.html#/phs-server/%E6%AE%8B%E7%96%BE%E4%BA%BA%E7%AE%A1%E7%90%86-%E4%B8%93%E9%A1%B9%E7%99%BB%E8%AE%B0/findPageUsingPOST_5
            varUrl = iUrl + iDoc + "#/" + varMenu + "/" + q_varTags + "/" + operationId

            # 条件标题和链接地址
            print(Color_PO.getColor({"32": [varMenu, tags, summary]}) + "=> " + varUrl)

            # get 或 delete 没有consumes
            if l_method[0] == 'post' or l_method[0] == 'put':
                # 2.6 content-type内容类型
                consumes = d['paths'][k][l_method[0]]['consumes'][0]
                # print(consumes)  # 'application/json'
            else:
                consumes = ''

            # 2.7 获取body参数（通过originalRef定位）
            varQuery = ''
            if 'parameters' in d['paths'][k][l_method[0]]:
                l_parameters = d['paths'][k][l_method[0]]['parameters']
                # print(l_parameters)  # [{'in': 'body', 'name': 'body', 'description': 'body', 'required': True, 'schema': {'$ref': '#/definitions/ThridTnbSfListInfoResponse', 'originalRef': 'ThridTnbSfListInfoResponse'}}]
                if len(l_parameters) == 1:
                    # 1个参数
                    if l_parameters[0]['in'] == 'body':
                        # todo body
                        if 'originalRef' in l_parameters[0]['schema']:
                            # 'schema': {'$ref': '#/definitions/ThridTnbSfListInfoResponse', 'originalRef': 'ThridTnbSfListInfoResponse'}}]
                            originalRef = l_parameters[0]['schema']['originalRef']
                            d_parametersMemo = d['definitions'][originalRef]['properties']
                            print('1参body =>', d_parametersMemo)  # {'ccsffl': {'type': 'string', 'description': '随访评价结果代码'},...
                        elif 'items' in l_parameters[0]['schema']:
                            # 'schema': {'type': 'array', 'items': {'$ref': '#/definitions/PerformRequest', 'originalRef': 'PerformRequest'}
                            if 'originalRef' in l_parameters[0]['schema']['items']:
                                originalRef = l_parameters[0]['schema']['items']['originalRef']
                                d_parametersMemo = d['definitions'][originalRef]['properties']
                                print('1参body(items) =>', d_parametersMemo)
                            else:
                                # 'schema': {'type': 'array', 'items': {'type': 'integer', 'format': 'int32'}}}]
                                if 'type' in l_parameters[0]['schema']:
                                    if l_parameters[0]['schema']['type'] == 'array':
                                        # 参数不是字典，是数组
                                        print('1参body数组 =>', l_parameters[0])
                                        d_parametersMemo = {}
                        # # 遍历检查是否有下级originalRef，并获取参数
                        d_body = self._traversalDict(d, d_parametersMemo)
                        print('1参body遍历 =>', d_body)
                    elif l_parameters[0]['in'] == 'query' or l_parameters[0]['in'] == 'path':
                        # todo query
                        varQuery = l_parameters[0]['name'] + "={" + l_parameters[0]['type'] + "}"
                        d_body = ''
                else:
                    # 多个参数
                    s = ''
                    for i in range(len(l_parameters)):
                        # print(l_parameters)
                        if l_parameters[i]['in'] == 'body':
                            # todo body
                            originalRef = l_parameters[i]['schema']['originalRef']
                            d_parametersMemo = d['definitions'][originalRef]['properties']
                            print('多参body =>', d_parametersMemo)  # {'ccsffl': {'type': 'string', 'description': '随访评价结果代码'},...
                            # 遍历检查是否有下级originalRef，并获取参数
                            d_body = self._traversalDict(d,  d_parametersMemo)
                        if l_parameters[i]['in'] == 'query' or l_parameters[i]['in'] == 'path':
                            # todo query
                            varQuery = l_parameters[i]['name'] + "={" + l_parameters[i]['type'] + "}"
                            s = s + varQuery + ','
                            if len(d_body) < 1 :
                                d_body = ''
                    varQuery = s[:-1]
                    print('多参query =>', varQuery)
            else:
                # 没有参数，即get
                d_body = ''


            # 生成列表

            l_1.append(tags)
            l_1.append(summary)
            l_1.append(paths)
            l_1.append(l_method[0])
            l_1.append(consumes)
            l_1.append(varQuery)  # query
            l_1.append(str(d_body))  # body
            l_1.append(varUrl)

            c = c + 1
            print(c, l_1, "\n")
            varQuery = ''
            s = ''
            d_body = {}
            l_all.append(l_1)
            l_1 = []

        # Color_PO.consoleColor2({"35": l_all})
        return l_all



if __name__ == '__main__':


    SwaggerPO_PO = SwaggerGwPO()
    
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



