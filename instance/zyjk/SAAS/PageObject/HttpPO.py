# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2020-8-27
# Description   : 接口请求方式
# *****************************************************************

import json, jsonpath, requests, urllib3
from time import sleep

import instance.zyjk.SAAS.PageObject.ReadConfigPO as readConfig
localReadConfig = readConfig.ReadConfigPO()

# 解决Python3 控制台输出InsecureRequestWarning的问题,https://www.cnblogs.com/ernana/p/8601789.html
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 禁用安全请求警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class HttpPO():
    def __init__(self):
        # 构造函数，实例化实例变量
        global scheme, baseurl, port, commonpath
        scheme = localReadConfig.get_http("scheme")
        baseurl = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        commonpath = localReadConfig.get_http("commonpath")

        self.session = requests.session()
        self.jsonres = {}   # 存放json解析后的结果
        self.params = {}   # 用来保存所需要的数据，实现关联
        self.url = ''  # 全局的url
        self.headers = {"Content-Type": "application/json;charset=UTF-8"}  # heaaders 默认请求Content-type   ,
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

    def postLogin(self, interName, param):
        ''' 登录接口的 post请求 '''
        path = scheme + "://" + baseurl + ":" + port + "/" + commonpath + interName
        result = self.session.post(path, headers=self.headers, json=param, verify=False)
        # print(result.text)
        self.jsonres = json.loads(result.text)
        self.session.headers['token'] = self.jsonres['token']
        # print(self.session.headers)
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res

    def post(self, interName, param):
        ''' post 请求
            :param interName 接口地址: /inter/HTTP/login
            :param param 参数: {'userName': 'jin', 'password': 'Jinhao1/'}
            :return: 有
        '''
        path = scheme + "://" + baseurl + ":" + port + "/" + commonpath + interName
        if param == '':
            result = self.session.post(path, data=None)
        else:
            result = self.session.post(path, headers=self.headers, json=param, verify=False)
            # print(result.text)
        # print(self.session.headers)
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}')+1]
            # print(res)
        except Exception as e:
            print(e.__traceback__)
        return res

    def postget(self, interName, param):
        ''' get 请求
            :param interName: /inter/HTTP/login
            :param param: userName=jinhao
            :return: 有
        '''
        path = scheme + "://" + baseurl + ":" + port + "/" + commonpath + interName + "?" + param
        if param == '':
            result = self.session.post(path, data=None)
        else:
            # result = requests.get(path, headers=self.headers)
            result = self.session.post(path, headers=self.headers, verify=False)
            if "token" in result.text:
                self.jsonres = json.loads(result.text)
                self.session.headers['token'] = self.jsonres['token']
        print(self.session.headers)
        # print(result.text)
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}')+1]
        except Exception as e:
            print(e.__traceback__)

        return res

    def get(self, interName, param):
        ''' get 请求
            :param interName: /inter/HTTP/login
            :param param: userName=jinhao
            :return: 有
        '''
        path = scheme + "://" + baseurl + ":" + port + "/" + commonpath + interName + "?" + param
        if param == '':
            result = self.session.post(path, data=None)
        else:
            # result = requests.get(path, headers=self.headers)
            result = self.session.get(path, headers=self.headers, verify=False)
        print(self.session.headers)
        # print(result.text)
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}')+1]
        except Exception as e:
            print(e.__traceback__)
        return res


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

