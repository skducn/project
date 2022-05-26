# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 接口驱动程序
# pip3 install requests_toolbelt  for cmd
# *****************************************************************

import json, jsonpath, os, requests, inspect, smtplib, email, mimetypes, base64, urllib3
import sys

from requests_toolbelt.multipart.encoder import MultipartEncoder
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()

# 解决Python3 控制台输出InsecureRequestWarning的问题,
# 参考：https://www.cnblogs.com/ernana/p/8601789.html
# 代码页加入以下这个
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 禁用安全请求警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# from xlutils.copy import copy
# from xlrd import open_workbook

class HTTP:
    def __init__(self):
        # 构造函数，实例化实例变量
        global protocol, ip, port, password, userNo
        if localReadConfig.get_env("switchENV") == "test":
            protocol = localReadConfig.get_test("protocol")
            ip = localReadConfig.get_test("ip")
            port = localReadConfig.get_test("port")
            # userNo = localReadConfig.get_test("userNo")
            # password = localReadConfig.get_test("password")
        else:
            protocol = localReadConfig.get_dev("protocol")
            ip = localReadConfig.get_dev("ip")
            port = localReadConfig.get_dev("port")
            # userNo = localReadConfig.get_dev("userNo")
            # password = localReadConfig.get_dev("password")
        self.session = requests.session()
        self.jsonres = {}   # 存放json解析后的结果
        self.params = {}   # 用来保存所需要的数据，实现关联
        self.url = ''  # 全局的url
        # self.headers = {"Content-Type": "application/json;charset=UTF-8"}  # heaaders 默认请求Content-type   ,
        self.headers = {"Content-Type": "application/json"}  # heaaders 默认请求Content-type   ,
        # self.session.headers['Content-type'] = 'application/x-www-form-urlencoded'
        # self.session.headers['User Agent'] = 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/64.0'   # 添加默认UA，模拟chrome浏览器

    def seturl(self, url):
        # 设置请求地址
        if url.startswith('http'):
            self.url = url
            return True
        else:
            print('error:url请求地址不合法')
            return False


    # 请求方法
    def token(self, iPath, iParam, d_var):
        '''  post请求之登录获取token '''

        d_iParam = json.loads(iParam)
        path = protocol + "://" + ip + ":" + port + iPath
        result = self.session.post(path, headers=self.headers, json=d_iParam, verify=False)
        d_response = json.loads(result.text)
        if d_response['code'] != 200:
            print(d_response)
            sys.exit(0)
        else:
            self.session.headers['token'] = d_response['data']['token']
            for k, v in d_var.items():
                if "$." in str(v):
                    res_value = jsonpath.jsonpath(d_response, expr=v)
                    d_var[k] = res_value[0]
            # print("\nrequest => " + str(path))
            # print("\nparam => " + str(d_iParam))
            # print("\nmethod => post")
            # print("\n<font color='blue'>response => " + str(result.text) + "</font>")
            # print("\nheaders => " + str(self.session.headers) + "\n")
            res = result.text
            print("response => " + str(res))
            try:
                res = res[res.find('{'):res.rfind('}') + 1]
            except Exception as e:
                print(e.__traceback__)
            return res, d_var


    def get(self, iPath, iParam, d_var):
        ''' get 请求'''

        if iParam == None:
            path = protocol + "://" + ip + ":" + port + iPath
            # print("\nrequest => " + str(path))
            result = self.session.get(path, data=None)
        else:
            iPath = protocol + "://" + ip + ":" + port + iPath + "?" + iParam
            result = self.session.get(iPath, headers=self.headers, verify=False)
            # print("\nrequest => " + str(iPath))
            # print("\nparam => " + str(iParam))
        d_response = json.loads(result.text)
        for k, v in d_var.items():
            if "$." in str(v):
                res_value = jsonpath.jsonpath(d_response, expr=v)
                d_var[k] = res_value[0]
        # print("\nmethod => get")
        # print("\n<font color='blue'>response => " + str(result.text) + "</font>")
        res = result.text
        print("response => " + str(res))
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var


    def post(self, iPath, iParam, d_var):
        '''
        post 请求
        :param iPath:
        :param iParam:
        :param d_var:
        :return:
        '''

        iPath = protocol + "://" + ip + ":" + port + iPath
        # print("\nrequest => " + str(iPath))
        if iParam == None:
            result = self.session.post(iPath, data=None)
        else:
            result = self.session.post(iPath, headers=self.headers, json=json.loads(iParam), verify=False)
        d_response = json.loads(result.text)
        for k, v in d_var.items():
            if "$." in str(v):
                res_value = jsonpath.jsonpath(d_response, expr=v)
                d_var[k] = res_value[0]
        # print("\nparam => " + str(iParam))
        # print("\nmethod => post")
        # print("\n<font color='blue'>response => " + str(result.text) + "</font>")
        # print("\nheaders => " + str(self.session.headers) + "\n")
        res = result.text
        print("response => " + str(res))

        try:
            res = res[res.find('{'):res.rfind('}')+1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var


    def delete(self, iPath, iParam, d_var):
        ''' delete 请求'''

        iPath = protocol + "://" + ip + ":" + port + iPath
        print("request => " + str(iPath))
        if iParam == None:
            result = self.session.delete(iPath, data=None)
            print("\n<font color='blue'>response => " + str(result.text) + "</font")
        else:
            result = self.session.delete(iPath, headers=self.headers, json=json.loads(iParam), verify=False)
            print("\nparam => " + str(iParam))
            print("\nmethod => delete")
            print("\n<font color='blue'>response => " + str(result.text) + "</font")
            print("\ncurrVar => " + str(d_var))
        # d_var = json.loads(g_var)
        res = result.text
        print("response => " + str(res))
        try:
            res = res[res.find('{'):res.rfind('}')+1]
        except Exception as e:
            print(e.__traceback__)
        return res, d_var

    def downFileGet(self, iPath, iParam, d_var):

        '''下载文件之get请求'''
        # 文件名放在 d_var中，格式：{'file': '/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/SAAS/i/sfb.xlsx'

        iPath = protocol + "://" + ip + ":" + port + iPath
        print("request => " + str(iPath))
        # result = self.session.get(path, stream=True)
        r = requests.get(iPath, stream=True)
        f = open(d_var['file'], "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        # d_var = json.loads(g_var)

        return None, d_var

    def downFilePost(self, iPath, iParam, d_var):

        '''下载文件之post请求'''

        iPath = protocol + "://" + ip + ":" + port + iPath
        print("request => " + str(iPath))
        self.headers = {"Content-Type": "application/json", "token": self.session.headers['token']}
        r = self.session.post(iPath, headers=self.headers, json=json.loads(iParam), verify=False)
        f = open(d_var['file'], "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        return None, d_var

    def upFile(self, iPath, filePath ,d_var):
        ''' 上传文件之post请求  '''
       # 参考 http://www.manongjc.com/detail/23-edxwzduohhtlzhf.html

        x = os.path.split(filePath)
        m = MultipartEncoder(fields={'file': (x[1], open(filePath, 'rb'), 'text/plain')})
        self.headers = {'Content-Type': m.content_type, }
        iPath = protocol + "://" + ip + ":" + port + iPath
        result = self.session.post(iPath, data=m, headers=self.headers)
        self.jsonres = json.loads(result.text)
        print("request => " + str(iPath))
        print("upFile => " + str(filePath))
        print("<font color='blue'>response => " + str(result.text) + "</font>\n")
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

