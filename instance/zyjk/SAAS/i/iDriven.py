# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 接口驱动程序
# pip3 install requests_toolbelt  for cmd

# Python3 控制台输出 InsecureRequestWarning 的问题？
# 参考：https://www.cnblogs.com/ernana/p/8601789.html
# 解决方法，加入以下代码：
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 禁用安全请求警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# *****************************************************************

import json, jsonpath, os, requests, inspect, smtplib, email, mimetypes, base64, urllib3
import sys
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from requests_toolbelt.multipart.encoder import MultipartEncoder
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()


class HTTP:
    def __init__(self):
        # 构造函数，实例化实例变量
        global protocol, ip, port, password, userNo

        if localReadConfig.get_env("env") == "test":
            protocol = localReadConfig.get_test("protocol")
            ip = localReadConfig.get_test("ip")
            port = localReadConfig.get_test("port")
        else:
            protocol = localReadConfig.get_dev("protocol")
            ip = localReadConfig.get_dev("ip")
            port = localReadConfig.get_dev("port")

        self.session = requests.session()
        self.headers = {"Content-Type": "application/json"}
        self.headersWWW = {"Content-Type": "application/x-www-form-urlencoded"}

        # self.session.headers['Content-type'] = 'application/x-www-form-urlencoded'
        # self.session.headers['User Agent'] = 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/64.0'   # 添加默认UA，模拟chrome浏览器

        # self.headers = {"Content-Type": "application/json; charset=UTF-8"}
        self.jsonres = {}  # 存放json解析后的结果
        self.params = {}  # 用来保存所需要的数据，实现关联
        self.url = ''  # 全局的url



    def seturl(self, url):
        # 设置请求地址
        if url.startswith('http'):
            self.url = url
            return True
        else:
            print('error:url请求地址不合法')
            return False



    def header(self, iPath, iQueryParam, iParam, d_var):

        '''  请求方式 header，用于设置header值 '''

        for k, v in d_var.items():
            self.session.headers[k] = str(v)
        # self.session.headers.update({'x-test': 'true'})  # 更新表头
        print("headers => " + str(self.session.headers))


    def token(self, iPath, iQueryParam, iParam, d_var):

        '''  请求方式 post，用于登录后将token加入header '''

        d_iParam = json.loads(iParam)
        path = protocol + "://" + ip + ":" + port + iPath
        result = self.session.post(path, headers=self.headers, json=d_iParam, verify=False)
        d_response = json.loads(result.text)
        if d_response['code'] != 200:
            print("response => " + str(d_response))
            sys.exit(0)
        else:
            self.session.headers['token'] = d_response['data']['token']
            for k, v in d_var.items():
                if "$." in str(v):
                    res_value = jsonpath.jsonpath(d_response, expr=v)
                    d_var[k] = res_value[0]
            # print("request => " + str(path))
            # print("param => " + str(d_iParam))
            # print("method => post")
            # print("<font color='blue'>response => " + str(result.text) + "</font>")
            print("headers => " + str(self.session.headers))
            res = result.text
            print("response => " + str(res))
            try:
                res = res[res.find('{'):res.rfind('}') + 1]
            except Exception as e:
                print(e.__traceback__)
            return res, d_var


    def get(self, iPath, iQueryParam, iParam, d_var):

        ''' 请求方式 get '''

        # query参数
        if iQueryParam != None and iParam == None:
            path = protocol + "://" + ip + ":" + port + iPath + "?" + iQueryParam
            print("request => " + str(path))
            result = self.session.get(path, headers=self.headers, verify=False)
        # elif iQueryParam == None and iParam != None:
        #     iPath = protocol + "://" + ip + ":" + port + iPath + "?" + iParam
        #     result = self.session.get(iPath, headers=self.headers, verify=False)
        #     print("request => " + str(iPath))
        #     # print("param => " + str(iParam))
        else:
            path = protocol + "://" + ip + ":" + port + iPath
            result = self.session.get(path, data=None)

        d_response = json.loads(result.text)

        for k, v in d_var.items():
            if "$." in str(v):
                res_value = jsonpath.jsonpath(d_response, expr=v)
                # print(res_value)
                d_var[k] = res_value[0]
        # print("method => get")
        # print("<font color='blue'>response => " + str(result.text) + "</font>")
        res = result.text
        print("response => " + str(d_response))
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var


    def post(self, iPath, iQueryParam, iParam, d_var):

        ''' 请求方式 post '''

        path = protocol + "://" + ip + ":" + port + iPath
        if iParam == None:
            result = self.session.post(path, data=None)
        else:
            result = self.session.post(path, headers=self.headers, json=json.loads(iParam), verify=False)
        d_response = json.loads(result.text)
        # print(d_response)
        for k, v in d_var.items():
            if "$." in str(v):
                res_value = jsonpath.jsonpath(d_response, expr=v)
                if res_value == False:
                    print("Error, 返回值是False，无效的jsonpath")
                    sys.exit(0)
                # print(d_var[k],res_value)
                d_var[k] = res_value[0]
        # print("param => " + str(iParam))
        # print("method => post")
        # print("<font color='blue'>response => " + str(result.text) + "</font>")
        # print("headers => " + str(self.session.headers) + "\n")
        res = result.text
        print("response => " + str(d_response))
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var


    def put(self, iPath, iQueryParam, iParam, d_var):

        ''' 请求方式 put '''

        # query参数
        if iQueryParam != None and iParam == None:
            path = protocol + "://" + ip + ":" + port + iPath + "?" + iQueryParam
            print("request => " + str(path))
            result = self.session.put(path, headers=self.headers, verify=False)
        elif iQueryParam == None and iParam != None:
            path = protocol + "://" + ip + ":" + port + iPath
            result = self.session.put(path, headers=self.headers, json=json.loads(iParam), verify=False)
        else:
            path = protocol + "://" + ip + ":" + port + iPath
            result = self.session.put(path, data=None)

        d_response = json.loads(result.text)

        # iPath = protocol + "://" + ip + ":" + port + iPath
        # if iParam == None:
        #     result = self.session.put(iPath, headers=self.headers, verify=False)
        # else:
        #     result = self.session.put(iPath, headers=self.headers, json=json.loads(iParam), verify=False)
        # d_response = json.loads(result.text)
        for k, v in d_var.items():
            if "$." in str(v):
                res_value = jsonpath.jsonpath(d_response, expr=v)
                d_var[k] = res_value[0]
        res = result.text
        print("response => " + str(d_response))
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var
    def putWWW(self, iPath, iQueryParam, iParam, d_var):

        ''' 请求方式 put '''

        # self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.session.headers['Content-type'] = 'application/x-www-form-urlencoded'

        # query参数
        if iQueryParam != None and iParam == None:
            path = protocol + "://" + ip + ":" + port + iPath + "?" + iQueryParam
            print("request => " + str(path))
            result = self.session.put(path, headers=self.headersWWW, verify=False)
        elif iQueryParam == None and iParam != None:
            path = protocol + "://" + ip + ":" + port + iPath
            result = self.session.put(path, headers=self.headersWWW, json=json.loads(iParam), verify=False)
        else:
            path = protocol + "://" + ip + ":" + port + iPath
            result = self.session.put(path, data=None)
        print("headers => " + str(self.session.headers))
        d_response = json.loads(result.text)

        # iPath = protocol + "://" + ip + ":" + port + iPath
        # if iParam == None:
        #     result = self.session.put(iPath, headers=self.headers, verify=False)
        # else:
        #     result = self.session.put(iPath, headers=self.headers, json=json.loads(iParam), verify=False)
        # d_response = json.loads(result.text)
        for k, v in d_var.items():
            if "$." in str(v):
                res_value = jsonpath.jsonpath(d_response, expr=v)
                d_var[k] = res_value[0]
        res = result.text
        print("response => " + str(d_response))
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var


    def delete(self, iPath, iQueryParam, iParam, d_var):

        ''' 请求方式 delete '''

        iPath = protocol + "://" + ip + ":" + port + iPath
        if iParam == None:
            result = self.session.delete(iPath, data=None)
            # print("\n<font color='blue'>response => " + str(result.text) + "</font")
        else:
            result = self.session.delete(iPath, headers=self.headers, json=json.loads(iParam), verify=False)
            # print("\nparam => " + str(iParam))
            # print("\nmethod => delete")
            # print("\n<font color='blue'>response => " + str(result.text) + "</font")
            # print("\ncurrVar => " + str(d_var))
        # d_var = json.loads(g_var)
        res = result.text
        print("response => " + str(res))
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var


    def downFileGet(self, iPath, iQueryParam, iParam, d_var):

        ''' 请求方式 get 之下载文件 '''

        # 文件名放在 d_var中，格式：{'file': '/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/SAAS/i/sfb.xlsx'
        iPath = protocol + "://" + ip + ":" + port + iPath
        # print("request => " + str(iPath))
        # result = self.session.get(path, stream=True)
        r = requests.get(iPath, stream=True)
        f = open(d_var['file'], "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        # d_var = json.loads(g_var)
        return None, d_var


    def downFilePost(self, iPath, iQueryParam, iParam, d_var):

        ''' 请求方式 post 之下载文件 '''

        iPath = protocol + "://" + ip + ":" + port + iPath
        self.headers = {"Content-Type": "application/json", "token": self.session.headers['token']}
        r = self.session.post(iPath, headers=self.headers, json=json.loads(iParam), verify=False)
        f = open(d_var['file'], "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        return None, d_var


    def upFile(self, iPath, iQueryParam, filePath, d_var):

        ''' 请求方式 post 之上传文件 '''

        # 参考 http://www.manongjc.com/detail/23-edxwzduohhtlzhf.html
        x = os.path.split(filePath)
        m = MultipartEncoder(fields={'file': (x[1], open(filePath, 'rb'), 'text/plain')})
        self.headers = {'Content-Type': m.content_type}
        iPath = protocol + "://" + ip + ":" + port + iPath
        result = self.session.post(iPath, data=m, headers=self.headers)
        self.jsonres = json.loads(result.text)
        # print("request => " + str(iPath))
        # print("upFile => " + str(filePath))
        # print("<font color='blue'>response => " + str(result.text) + "</font>\n")
        self.headers = {"Content-Type": "application/json"}
        # print("\nheaders => " + str(self.session.headers) + "\n")
        # d_var = json.loads(g_var)
        res = result.text
        print("response => " + str(res))
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var


 #    # 定义断言相等的关键字，用来判断json的key对应的值和期望相等。
 #    def assertequals(self, jsonpaths, value):
 #        res = 'None'
 #        try:
 #            res = str(jsonpath.jsonpath(self.jsonres, jsonpaths)[0])
 #        except Exception as e:
 #            print(e.__traceback__)
 #
 #        value = self.__getparams(value)
 #
 #        if res == str(value):
 #            return True
 #        else:
 #            return False
 #
 #    # 给头添加一个键值对的关键字
 #    def addheader(self, key, value):
 #        value = self.__getparams(value)
 #        self.session.headers[key] = value
 #        return True
 #
 #    # 定义保存一个json值为参数的关键字
 #    def savejson(self, key, p):
 #        res = ''
 #        try:
 #            res = self.jsonres[key]
 #        except Exception as e:
 #            print(e.__traceback__)
 #        self.params[p] = res
 #        return True
 #
 #    # 获取参数里面的值
 #    def __getparams(self, s):
 #        for key in self.params:
 #            s = s.replace('{' + key + '}', self.params[key])
 #        return s
 #
 #    def __strTodict(self, s):
 #        '''
 #        字符型键值队格式 转 字典类型
 #        :param s: username=will&password=123456
 #        :return: {'username':'will','password':'123456’}
 #        '''
 #
 #        httpparam = {}
 #        param = s.split('&')
 #        for ss in param:
 #            p = ss.split('=')
 #            if len(p) > 1:
 #                httpparam[p[0]] = p[1]
 #            else:
 #                httpparam[p[0]] = ''
 #        return httpparam
 #
 #    def getJointParam(self, keys, values):
 #        """
 #            将两个字符串组合成一组接口参数
 #            如：xls.getJointParam('username,password', 'will,123456')
 #            返回：'username=will&password=123456'
 #        """
 #        interKey = len(str(keys).split(','))
 #        exlValue = len(str(values).split(','))
 #        varJoint = ''
 #
 #        try:
 #            if interKey == exlValue:
 #                for i in range(interKey):
 #                    varJoint = varJoint + str(keys).split(',')[i] + '=' + str(values).split(',')[i] + '&'
 #            else:
 #                assert (interKey == exlValue)
 #        except Exception as e:
 #            # print(e.__traceback__)
 #            print("error, 接口的参数与值数量不一致！")
 #
 #        return varJoint[:-1]
 #
 #