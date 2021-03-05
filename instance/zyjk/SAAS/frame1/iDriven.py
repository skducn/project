# -*- coding: utf-8 -*-
import jsonpath, requests, urllib3, redis
from readConfig import *
localReadConfig = ReadConfig()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HTTP:
    def __init__(self):

        self.ip = localReadConfig.get_http("ip")
        self.port = localReadConfig.get_http("port")
        self.r_host = localReadConfig.get_redis("host")
        self.r_password = localReadConfig.get_redis("password")
        self.r_port = localReadConfig.get_redis("port")
        self.r_db = localReadConfig.get_redis("db")
        self.session = requests.session()
        self.jsonres = {}   # 存放json解析后的结果
        self.params = {}   # 用来保存所需要的数据，实现关联
        self.headers = {"Content-Type": "application/json;charset=UTF-8"}
        # self.session.headers['Content-type'] = 'application/x-www-form-urlencoded'
        # self.session.headers['User Agent'] = 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/64.0'   # 添加默认UA，模拟chrome浏览器

        # 从redis的db0中随机获取一个token
        # r1 = redis.Redis(host=self.r_host, password=self.r_password, port=self.r_port, db=self.r_db, decode_responses=False)
        # for i in r1.keys():
        #     if len(i) == 32:
        #         token = str(i, encoding="utf-8")
        #         break
        # self.session.headers['token'] = token


    def header(self, interName, param, d_var):

        ''' 全局参数设置 '''

        d_param = eval(param)
        for k in d_param:
            self.session.headers[k] = d_param[k]
        print("header = " + str(self.session.headers))
        return {}


    def post(self, interName, param, d_var):

        ''' post请求'''

        print("header = " + str(self.session.headers))
        print("参数变量：" + str(param))
        print("字典变量：" + str(d_var))
        testURL = self.ip + ":" + self.port + interName
        if param == '':
            result = self.session.post(testURL, data=None)
        else:
            if "{$." in param:
                for k in d_var:
                    if "{" + k + "}" in param:
                        param = str(param).replace("{" + k + "}", str(d_var[k]))
                result = self.session.post(testURL, headers=self.headers, json=param, verify=False)
                print("request = " + str(param))
            else:
                result = self.session.post(testURL, headers=self.headers, json=param, verify=False)
        print("response = " + str(result.text))
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}')+1]
        except Exception as e:
            print(e.__traceback__)
        return res


    def get(self, interName, param, d_var):

        ''' get 请求'''

        print("header = " + str(self.session.headers))
        if d_var != {}:
            print("字典变量：" + str(d_var))
        if param == None:
            if "{{" in interName:
                for k in d_var:
                    if "{{" + k + "}}" in interName:
                        interName = str(interName).replace("{{" + k + "}}", str(d_var[k]))
                testURL = self.ip + ":" + self.port + interName
            else:
                testURL = self.ip + ":" + self.port + interName
            print("request = " + str(testURL))
            # result = self.session.get(testURL, data=None)
            result = self.session.get(testURL, headers=self.headers, verify=False)

        else:
            testURL = self.ip + ":" + self.port + interName + "?" + param
            if "{{" in param:
                for k in d_var:
                    if "{{" + k + "}}" in param:
                        param = str(param).replace("{{" + k + "}}", str(d_var[k]))
                result = self.session.get(testURL, headers=self.headers, verify=False)
            else:
                result = self.session.get(testURL, headers=self.headers, verify=False)
            print("request = " + str(testURL))
        print("response = " + str(result.text))
        res = result.text
        try:
            res = res[res.find('{'):res.rfind('}') + 1]
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
