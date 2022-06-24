# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 接口驱动程序
# requests_toolbelt 支持 multipart/form-data类型的请求，一般用于上次文件
# pip3 install requests_toolbelt
# 如：headers['Content-Type'] = multipart_encoder.content_type
# response = requests.post(url, data=multipart_encoder, headers=headers)
# 参考：https://blog.csdn.net/summerpowerz/article/details/80293235
# 参考 Python 通过Request上传(form-data Multipart)\下载文件, http://www.manongjc.com/detail/23-edxwzduohhtlzhf.html

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
        global varUrl

        if localReadConfig.get_default("env") == "test":
            protocol = localReadConfig.get_test("protocol")
            ip = localReadConfig.get_test("ip")
            port = localReadConfig.get_test("port")
        else:
            protocol = localReadConfig.get_dev("protocol")
            ip = localReadConfig.get_dev("ip")
            port = localReadConfig.get_dev("port")

        varUrl = protocol + "://" + ip + ":" + port

        self.session = requests.session()


    def header(self, iPath, iConsumes, iQueryParam, iParam, d_var):

        '''  设置header '''

        for k, v in iParam.items():
            self.session.headers[k] = str(v)
        print("headers => " + str(self.session.headers))
        return None, {}

    def post(self, iPath, iConsumes, iQueryParam, iParam, d_var):

        result = self.session.post(varUrl + iPath, headers={"Content-Type": iConsumes}, json=json.loads(iParam), verify=False)
        d_response = json.loads(result.text)

        # '判断有无token，添加到headers'
        # print(d_response)
        if 'data' in d_response:
            if d_response['data'] != None and d_response['data'] != True and d_response['data'] != False and 'token' in d_response['data']:
                self.session.headers['token'] = d_response['data']['token']
                print("headers => " + str(self.session.headers))

        for k, v in d_var.items():
            if "$." in str(v):
                res_value = jsonpath.jsonpath(d_response, expr=v)
                if res_value == False:
                    print("Error, 返回值是False，无效的jsonpath")
                    sys.exit(0)
                else:
                    d_var[k] = res_value[0]

        # print("request => " + str(path))
        # print("param => " + str(d_iParam))
        # print("method => post")
        # print("<font color='blue'>res => " + str(result.text) + "</font>")
        # print("headers => " + str(self.session.headers))
        res = result.text
        print("res => " + str(res))
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var


    def get(self, iPath, iConsumes, iQueryParam, iParam, d_var):

        # query参数
        if iQueryParam != None and iParam == None:
            result = self.session.get(varUrl + iPath + "?" + iQueryParam, headers={"Content-Type": iConsumes}, verify=False)
        else:
            result = self.session.get(varUrl + iPath, data=None, headers={"Content-Type": iConsumes}, verify=False)
        d_response = json.loads(result.text)
        for k, v in d_var.items():
            if "$." in str(v):
                res_value = jsonpath.jsonpath(d_response, expr=v)
                if res_value == False:
                    print("Error, 返回值是False，无效的jsonpath")
                    sys.exit(0)
                else:
                    d_var[k] = res_value[0]
        # print("method => get")
        # print("<font color='blue'>res => " + str(result.text) + "</font>")
        res = result.text
        print("res => " + str(d_response))
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var


    def put(self, iPath, iConsumes, iQueryParam, iParam, d_var):

        # query参数
        if iQueryParam != None and iParam == None:
            result = self.session.put(varUrl + iPath + "?" + iQueryParam, headers={"Content-Type": iConsumes}, verify=False)
        elif iQueryParam == None and iParam != None:
            result = self.session.put(varUrl + iPath, headers={"Content-Type": iConsumes}, json=json.loads(iParam), verify=False)
        else:
            result = self.session.put(varUrl + iPath, data=None, headers={"Content-Type": iConsumes}, verify=False)
        d_response = json.loads(result.text)
        for k, v in d_var.items():
            if "$." in str(v):
                res_value = jsonpath.jsonpath(d_response, expr=v)
                if res_value == False:
                    print("Error, 返回值是False，无效的jsonpath")
                    sys.exit(0)
                else:
                    d_var[k] = res_value[0]
        res = result.text
        print("res => " + str(d_response))
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var


    def delete(self, iPath, iConsumes, iQueryParam, iParam, d_var):

        if iParam == None:
            result = self.session.delete(varUrl + iPath, data=None, headers={"Content-Type": iConsumes})
        else:
            result = self.session.delete(varUrl + iPath, headers={"Content-Type": iConsumes}, json=json.loads(iParam), verify=False)
        res = result.text
        print("res => " + str(res))
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var


    def getDownfile(self, iPath, iConsumes, iQueryParam, iParam, d_var):

        ''' 请求方式 get 之下载文件 '''

        # 文件名放在 d_var中，格式：{'file': '/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/SAAS/i/sfb.xlsx'
        # print("request => " + str(iPath))
        # result = self.session.get(path, stream=True)
        r = requests.get(varUrl + iPath, headers={"Content-Type": iConsumes}, stream=True)
        f = open(d_var['file'], "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        # d_var = json.loads(g_var)
        return None, d_var


    def postDownfile(self, iPath, iConsumes, iQueryParam, iParam, d_var):

        ''' 请求方式 post 之下载文件 '''

        # self.headers = {"Content-Type": "application/json", "token": self.session.headers['token']}
        r = self.session.post(varUrl + iPath, headers={"Content-Type": iConsumes}, json=json.loads(iParam), verify=False)
        f = open(d_var['file'], "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        return None, d_var


    def postUpfile(self, iPath, iConsumes, iQueryParam, filePath, d_var):

        ''' 请求方式 post 之上传文件 '''

        x = os.path.split(filePath)
        m = MultipartEncoder(fields={'file': (x[1], open(filePath, 'rb'), 'text/plain')})
        # self.headers = {'Content-Type': m.content_type}
        result = self.session.post(varUrl + iPath, data=m, headers={'Content-Type': m.content_type})
        self.jsonres = json.loads(result.text)
        # print("request => " + str(iPath))
        # print("upFile => " + str(filePath))
        # print("<font color='blue'>res => " + str(result.text) + "</font>\n")
        # self.headers = {"Content-Type": "application/json"}
        # print("\nheaders => " + str(self.session.headers) + "\n")
        # d_var = json.loads(g_var)
        res = result.text
        print("res => " + str(res))
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var
