# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-19
# Description   : EHR 接口自动化框架之 驱动
# *****************************************************************

import json, jsonpath, os, xlrd, xlwt, requests, inspect, smtplib, email, mimetypes, base64,urllib3
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

from requests_toolbelt.multipart.encoder import MultipartEncoder
import instance.zyjk.epidemic.frame1.readConfig as readConfig
localReadConfig = readConfig.ReadConfig()

# 解决Python3 控制台输出InsecureRequestWarning的问题,https://www.cnblogs.com/ernana/p/8601789.html
# 代码页加入以下这个
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 禁用安全请求警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from xlutils.copy import copy
from xlrd import open_workbook

class HTTP:
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
        # self.headers = {"Content-Type": "application/json;charset=UTF-8"}  # heaaders 默认请求Content-type   ,
        self.headers = {"Content-Type": "application/json"}  # heaaders 默认请求Content-type   ,
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


    def get(self, interName, param, d_var):
        ''' get 请求'''

        if param == None:
            path = scheme + "://" + baseurl + ":" + port + commonpath + interName
            print("请求地址：" + str(path) + "<BR>")
            result = self.session.get(path, data=None)
        else:
            path = scheme + "://" + baseurl + ":" + port + interName + "?" + param
            print("请求地址：" + str(path) + "<BR>")
            if "{{" in param:
                for k in d_var:
                    if "{{" + k + "}}" in param:
                        param = str(param).replace("{{" + k + "}}", str(d_var[k]))
                result = self.session.get(path, headers=self.headers, verify=False)
                print("请求参数：" + str(param) + "<BR>")

            else:
                result = self.session.get(path, headers=self.headers, verify=False)
        print("字典变量：" + str(d_var) + "<BR>")
        print("返回：" + str(result.text) + "<BR>")
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res

    def post(self, interName, param, d_var):
        ''' post 请求'''

        print(self.session.headers)
        path = scheme + "://" + baseurl + ":" + port + commonpath + interName
        print("请求地址：" + str(path) + "<BR>")
        if param == '':
            result = self.session.post(path, data=None)
        else:
            if "{$." in param:
                for k in d_var:
                    if "{" + k + "}" in param:
                        param = str(param).replace("{" + k + "}", str(d_var[k]))
                result = self.session.post(path, headers=self.headers, json=param, verify=False)
            else:
                result = self.session.post(path, headers=self.headers, json=param, verify=False)
            print("请求参数：" + str(param) + "<BR>")
            print("字典变量：" + str(d_var) + "<BR>")
        print("返回：" + str(result.text) + "<BR>")
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}')+1]
        except Exception as e:
            print(e.__traceback__)
        return res

    def delete(self, interName, param, d_var):
        ''' delete 请求'''

        path = scheme + "://" + baseurl + ":" + port + commonpath + interName
        print("请求地址：" + str(path) + "<BR>")
        if param == '':
            result = self.session.delete(path, data=None)
        else:
            if "{$." in param:
                for k in d_var:
                    if "{" + k + "}" in param:
                        param = str(param).replace("{" + k + "}", str(d_var[k]))
                result = self.session.delete(path, headers=self.headers, json=param, verify=False)
            else:
                result = self.session.delete(path, headers=self.headers, json=param, verify=False)
            print("请求参数：" + str(param) + "<BR>")
            print("字典变量：" + str(d_var) + "<BR>")
        print("返回：" + str(result.text) + "<BR>")
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}')+1]
        except Exception as e:
            print(e.__traceback__)
        return res

    def token(self, interURL, param):
        ''' 登录接口 post请求 '''

        path = scheme + "://" + baseurl + ":" + port + interURL
        print("请求地址：" + str(path) + "<BR>")
        print("请求参数：" + str(param) + "<BR>")
        result = self.session.post(path, headers=self.headers, json=dict(eval(param)), verify=False)
        print(self.session.headers)
        self.jsonres = json.loads(result.text)
        self.session.headers['token'] = self.jsonres['data']['token']
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res

    def token2(self, interURL, param):
        ''' 登录接口 post请求 '''

        self.headers = {"Content-Type": "application/json"}
        path = scheme + "://" + baseurl + ":" + port + interURL
        print("请求地址：" + str(path) + "<BR>")
        print("请求参数：" + str(param) + "<BR>")
        result = self.session.post(path, headers=self.headers, json=dict(eval(param)), verify=False)
        self.jsonres = json.loads(result.text)
        self.session.headers['token'] = self.jsonres['data']['token']
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res

    def file(self, interURL, filePath):
        ''' post请求 上传文件 '''
       # 参考 http://www.manongjc.com/detail/23-edxwzduohhtlzhf.html

        x = os.path.split(filePath)
        m = MultipartEncoder(
            fields={
                'file': (x[1], open(filePath, 'rb'), 'text/plain')
            }
        )
        self.headers = {'Content-Type': m.content_type,}
        path = scheme + "://" + baseurl + ":" + port + interURL
        print("请求地址：" + str(path) + "<BR>")
        print("上传文件：" + str(filePath) + "<BR>")
        result = requests.post(path, data=m, headers=self.headers)
        self.jsonres = json.loads(result.text)
        print("返回：" + str(result.text) + "<BR>")
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
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

    # 3个关于Email函数
    def getAttachment(self, attachmentFilePath):
        contentType, encoding = mimetypes.guess_type(attachmentFilePath)
        if contentType is None or encoding is not None:
            contentType = 'application/octet-stream'
        mainType, subType = contentType.split('/', 1)
        file = open(attachmentFilePath, 'rb')
        if mainType == 'text':
            attachment = MIMEText(file.read())
        elif mainType == 'message':
            attachment = email.message_from_file(file)
        elif mainType == 'image':
            attachment = MIMEImage(file.read(), subType=subType)
        elif mainType == 'audio':
            attachment = MIMEAudio(file.read(), subType=subType)
        else:
            attachment = MIMEBase(mainType, subType)
        attachment.set_payload(file.read())
        # encode_base64(attachment)
        base64.b64encode(attachment.encode('utf-8'))

        file.close()
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachmentFilePath))
        return attachment
    def sendemail(self, subject, text, *attachmentFilePaths):
        gmailUser = 'skducn@163.com'
        gmailPassword = 'jinhao123'
        recipient = 'skducn@163.com'
        # recipient = "'jinhao@mo-win.com.cn', 'guoweiliang@mo-win.com.cn'"
        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(text, 'plain', 'utf-8'))
        # 附件是可选项
        for attachmentFilePath in attachmentFilePaths:
            if attachmentFilePath != '':
                msg.attach(self.getAttachment(attachmentFilePath))
        mailServer = smtplib.SMTP('smtp.exmail.qq.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, msg.as_string())
        mailServer.close()
        print('Sent email to %s' % recipient)
    def send1(self):

        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header

        mail_host = "smtp.163.com"
        mail_user = "skducn@163.com"
        mail_pass = "123456"
        sender = 'skducn@163.com'
        # receivers = ['skducn@163.com', '******@163.com']
        receivers = ['skducn@163.com']
        body_content = """ 测试文本  """

        message = MIMEText(body_content, 'plain', 'utf-8')
        message['From'] = "skducn@163.com"
        message['To'] = "skducn@163.com"
        subject = """
        项目异常测试邮件
        """
        message['Subject'] = Header(subject, 'utf-8')
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.set_debuglevel(1)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")

