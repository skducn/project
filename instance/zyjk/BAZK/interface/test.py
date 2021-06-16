# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2020-8-25
# Description   : SAAS 接口自动化
# 接口文档 http://192.168.0.213:8801/doc.html
# *****************************************************************
import json, jsonpath, requests, urllib3, sys

import instance.zyjk.SAAS.config.readConfig as readConfig
localReadConfig = readConfig.ReadConfig()

class HTTP:
    def __init__(self):

        self.varUrl = localReadConfig.get_interface("varUrl")
        self.session = requests.session()   # 实例化session，会话保持（跨请求保持某些参数）
        self.jsonres = {}   # 存放json解析后的结果
        self.params = {}   # 用来保存所需要的数据，实现关联
        self.url = ''  # 全局的url
        self.headers = {"Content-Type": "application/json;charset=UTF-8"}  # 设置请求头, heaaders 默认请求Content-type

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

        url = self.varUrl + interName
        result = self.session.post(url, headers=self.headers, json=param, verify=False)
        # print(result.status_code)
        # print(result.text)
        self.jsonres = json.loads(result.text)
        # print(str(self.jsonres))
        # print("前：" + str(self.session.headers))
        try:
            # print(self.jsonres['data']['token'])
            if "token" not in self.session.headers:
                self.session.headers['token'] = self.jsonres['data']['token']
            # print("后：" + str(self.session.headers))
            # res = result.text
            return self.jsonres
        except Exception as e:
            # import traceback
            # print(e.__traceback__)  # <traceback object at 0x0000017ADEFC8C80>  traceback 对象
            # traceback.print_tb(sys.exc_info()[2])  # 查看 traceback 对象包含的内容
            print(sys.exc_info())  # 捕获异常信息（type,value,traceback）
            # print(e.args)
            # print(e.__str__())  # 异常实例
            # print(e.with_traceback(sys.exc_info()[2]))
        # except TypeError as e:
        #     raise ValueError(e).with_traceback(sys.exc_info()[2])

    def post(self, interName, param=''):
        ''' post 请求
            :param interName 接口地址: /inter/HTTP/login
            :param param 参数: {'userName': 'jin', 'password': 'Jinhao1/'}
            :return: 有
        '''
        try:
            url = self.varUrl + interName
            if param == '':
                result = self.session.post(url, data=None)
            else:
                result = self.session.post(url, headers=self.headers, json=param, verify=False)
            self.jsonres = json.loads(result.text)
            if "token" not in self.session.headers:
                self.session.headers['token'] = self.jsonres['data']['token']
            return self.jsonres
        except Exception as e:
            print(e.__traceback__)

    def get(self, interName, param=''):
        ''' get 请求
            :param interName: /inter/HTTP/login
            :param param: userName=jinhao
            :return: 有
        '''
        try:
            if param == '':
                url = self.varUrl + interName
                result = self.session.get(url, headers=self.headers, verify=False)
            else:
                url = self.varUrl + interName + "?" + param
                result = requests.get(url, headers=self.headers)
            return json.loads(result.text)
        except Exception as e:
            print(e.__traceback__)



if __name__ == '__main__':

    http = HTTP()
    print(http.post("/auth/login", {'userNo': '016', 'password': '123456'}))
    dict1 = (http.get("/auth/getCodeByToken"))
    print(dict1)
    print(http.get("/auth/getTokenByCode", 'code=' + dict1['data']))
    print(http.get("/saasuser/sysOrg/getProvince"))
    print(http.get("/saasuser/sysOrg/getCity", 'code=820000'))
    print(http.post("/auth/logout"))
