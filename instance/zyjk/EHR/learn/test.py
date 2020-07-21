# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-19
# Description   : EHR 接口自动化
# 接口文档 http://192.168.0.36:19090/test_ehr_sys/healthRecord/swagger-ui.html
# *****************************************************************
import json, jsonpath, requests, urllib3, sys

class HTTP:
    def __init__(self):
        # 实例化session，会话保持（跨请求保持某些参数）
        self.session = requests.session()
        self.jsonres = {}   # 存放json解析后的结果
        self.params = {}   # 用来保存所需要的数据，实现关联
        self.url = ''  # 全局的url
        # 设置请求头, heaaders 默认请求Content-type
        self.headers = {"Content-Type": "application/json;charset=UTF-8"}

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

        url = "http://192.168.0.36:8080/healthRecord" + interName
        result = self.session.post(url, headers=self.headers, json=param, verify=False)
        print(result.status_code)
        print(result.text)
        self.jsonres = json.loads(result.text)
        print(str(self.jsonres))
        print("前：" + str(self.session.headers))
        try:

            self.session.headers['token'] = self.jsonres['token1']
            print("后：" + str(self.session.headers))
            res = result.text
            return res
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

    def post(self, interName, param):
        ''' post 请求
            :param interName 接口地址: /inter/HTTP/login
            :param param 参数: {'userName': 'jin', 'password': 'Jinhao1/'}
            :return: 有
        '''
        url = "http://192.168.0.36:8080/healthRecord" + interName
        if param == '':
            result = self.session.post(url, data=None)
        else:
            result = self.session.post(url, headers=self.headers, json=param, verify=False)
            print(result.text)
        # print(self.session.headers)
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}')+1]
            # print(res)
        except Exception as e:
            print(e.__traceback__)
        return res

    def get(self, interName, param):
        ''' get 请求
            :param interName: /inter/HTTP/login
            :param param: userName=jinhao
            :return: 有
        '''
        # path = scheme + "://" + baseurl + ":" + port + "/" + commonpath + interName + "?" + param
        url = "http://192.168.0.36:8080/healthRecord" + interName + "?" + param
        if param == '':
            result = self.session.post(url, data=None)
        else:
            # result = requests.get(path, headers=self.headers)
            result = self.session.get(url, headers=self.headers, verify=False)

        print(self.session.headers)


        # print(self.session.headers['data'])
        print(result.text)
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}')+1]
        except Exception as e:
            print(e.__traceback__)
        return res


if __name__ == '__main__':
    http = HTTP()
    http.postLogin("/app/login", {'userName': 'shuyang', 'password': '07497ba923378ceada4a7f6428be9956'})
    # http.get("/encrypted/getQuestionList", 'userName=shuyang')
    # x = http.get("/PersonBasicInfo/getArchiveNum", 'idCard=110101199003071970')
    # x = json.loads(x)
    # print(x['data'])