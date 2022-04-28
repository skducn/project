# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2020-8-27
# Description   : 接口请求方式
# *****************************************************************

import json, jsonpath, requests, urllib3
import instance.zyjk.SAAS.PageObject.ReadConfigPO as readConfig
localReadConfig = readConfig.ReadConfigPO()

# 解决Python3 控制台输出InsecureRequestWarning的问题,https://www.cnblogs.com/ernana/p/8601789.html
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 禁用安全请求警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from PO.DataPO import *
Data_PO = DataPO()


class HttpPO():

    def __init__(self):
        # 构造函数，实例化实例变量
        global interfaceUrl
        self.interfaceUrl = localReadConfig.get_http("interfaceUrl")
        self.session = requests.session()
        self.jsonres = {}   # 存放json解析后的结果
        self.params = {}   # 用来保存所需要的数据，实现关联
        self.url = ""
        self.headers = {"Content-Type": "application/json;charset=UTF-8"}
        # self.session.headers['Content-type'] = 'application/x-www-form-urlencoded'
        # self.session.headers['User Agent'] = 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/64.0'   # 添加默认UA，模拟chrome浏览器

    def seturl(self, url):
        # 设置地址
        if url.startswith('http'):
            self.url = url
            return True
        else:
            print('error:url地址不合法')
            return False

    def post(self, excelNo, caseName, interName, param=''):

        ''' post 请求
            :param interName 接口地址:
            :param param 参数:
            :return: 有
        '''

        try:
            url = self.interfaceUrl + interName
            if param == '':
                result = self.session.post(url, data=None)
                print("[" + str(excelNo + 1) + "] > " + caseName + " > post > " + url)
            elif "=" in param:
                if "$$[" in param:
                    for i in range(1, len(param.split("$$["))):
                        var = param.split("$$[")[1].split("]")[0]
                        param = param.replace("$$[" + var + "]", eval(var))

                print("[" + str(excelNo + 1) + "] => " + caseName + " > post > " + url + " > " + str(param))
                url = self.interfaceUrl + interName + "?" + param
                result = self.session.post(url, data=None)
            else:
                if "$$[" in param:
                    for i in range(1, len(param.split("$$["))):
                        var = param.split("$$[")[1].split("]")[0]
                        param = param.replace("$$[" + var + "]", eval(var))

                print("[" + str(excelNo + 1) + "] > " + caseName + " > post > " + url + " > " + str(param))
                result = self.session.post(url, headers=self.session.headers, json=dict(eval(param)), verify=False)

            self.jsonres = json.loads(result.text)
            if "token" not in self.session.headers:
                if None == self.jsonres["data"]:
                    pass
                elif 'token' in self.jsonres["data"]:
                    self.session.headers['token'] = self.jsonres['data']['token']
            return self.jsonres, param
        except Exception as e:
            print(e.__traceback__)

    def get(self, excelNo, caseName, interName, param=''):

        ''' get 请求
            :param interName:
            :param param:
            :return: 有
        '''
        try:
            if param == '':
                url = self.interfaceUrl + interName
                result = self.session.get(url, headers=self.session.headers, verify=False)
                print("[" + str(excelNo + 1) + "] > " + caseName + " > get > " + url)
            else:
                url = self.interfaceUrl + interName + "?" + param
                result = requests.get(url, headers=self.session.headers, verify=False)
                print("[" + str(excelNo + 1) + "] > " + caseName + " > get > " + url)

            return json.loads(result.text),param
        except Exception as e:
            print(e.__traceback__)

    def put(self, excelNo, caseName, interName, param=''):

        ''' put 请求
            :param interName:
            :param param:
            :return: 有
        '''
        try:
            url = self.interfaceUrl + interName
            if param == '':
                result = self.session.put(url, headers=self.session.headers, verify=False)
                print("[" + str(excelNo + 1) + "] > " + caseName + " > put > " + url)
            elif "{" in param and "}" in param:
                print("[" + str(excelNo + 1) + "] > " + caseName + " > put > " + url + " > " + str(param))
                result = self.session.put(url, headers=self.session.headers, json=dict(eval(param)), verify=False)
            else:
                if "$$[" in param:
                    for i in range(1, len(param.split("$$["))):
                        var = param.split("$$[")[1].split("]")[0]
                        param = param.replace("$$[" + var + "]", eval(var))
                print("[" + str(excelNo + 1) + "] => " + caseName + " > put > " + url + " > " + str(param))
                url = self.interfaceUrl + interName + "?" + param
                result = self.session.put(url, data=None)


            return json.loads(result.text), param

        except Exception as e:
            print(e.__traceback__)

    # 定义断言相等的关键字，用来判断json的key对应的值和期望相等。
    def assertequals(self,jsonpaths,value):
        res = 'None'
        try:
            res = str(jsonpath.jsonpath(self.jsonres, jsonpaths)[0])
        except Exception as e:
            print(e.__traceback__)

        value = self.__getparams(value)

        if res == str(value):
            return True
        else:
            return False

    # 给头添加一个键值对的关键字
    def addheader(self,key,value):
        value = self.__getparams(value)
        self.session.headers[key] = value
        return True
    # 88-93
    #
    #     return True

    # 定义保存一个json值为参数的关键字
    def savejson(self,key,p):
        res = ''
        try:
            res = self.jsonres[key]
        except Exception as e:
            print(e.__traceback__)
        self.params[p] = res
        return True

    # 获取参数里面的值
    def __getparams(self,s):
        for key in self.params:
            s = s.replace('{' + key +'}',self.params[key])
        return s

    def __strTodict(self,s):
        '''
        字符型键值队格式 转 字典类型
        :param s: username=will&password=123456
        :return: {'username':'will','password':'123456’}
        '''

        httpparam = {}
        param = s.split('&')
        for ss in param:
            p = ss.split('=')
            if len(p)>1:
                httpparam[p[0]] = p[1]
            else:
                httpparam[p[0]] = ''
        return httpparam

    def getJointParam(self, keys, values):
        """
            将两个字符串组合成一组接口参数
            如：xls.getJointParam('username,password', 'will,123456')
            返回：'username=will&password=123456'
        """
        interKey = len(str(keys).split(','))
        exlValue = len(str(values).split(','))
        varJoint = ''

        try:
            if interKey == exlValue:
                for i in range(interKey):
                    varJoint = varJoint + str(keys).split(',')[i] + '=' + str(values).split(',')[i] + '&'
            else:
                assert (interKey == exlValue)
        except Exception as e:
            # print(e.__traceback__)
            print("error, 接口的参数与值数量不一致！")

        return varJoint[:-1]

