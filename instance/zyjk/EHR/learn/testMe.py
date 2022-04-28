# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-19
# Description   : EHR 接口自动化框架之 驱动
# http://192.168.0.36:19090/test_ehr_sys/healthRecord/swagger-ui.html
# *****************************************************************
import json, jsonpath, os, xlrd, xlwt, requests, inspect, smtplib, email, mimetypes, base64,urllib3,sys
from time import sleep
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 禁用安全请求警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from xlutils.copy import copy
from xlrd import open_workbook

class HTTP:
    def __init__(self):
        # 实例化session，会话保持（跨请求保持某些参数）
        self.session = requests.session()
        self.jsonres = {}   # 存放json解析后的结果
        self.params = {}   # 用来保存所需要的数据，实现关联
        self.url = ''  # 全局的url
        # 设置请求头, heaaders 默认请求Content-type
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
            self.session.headers['token'] = self.jsonres['token']
            print("后：" + str(self.session.headers))
            res = result.text
            return res
        except Exception as e:
            import traceback
            # print(e.__traceback__)  # <traceback object at 0x0000017ADEFC8C80>  traceback 对象
            # traceback.print_tb(sys.exc_info()[2])  # 查看 traceback 对象包含的内容
            print(sys.exc_info())  # 捕获异常信息（type,value,traceback）
            print(e.args)
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
        # path = scheme + "://" + baseurl + ":" + port + "/" + commonpath + interName + "?" + param
        url = "http://192.168.0.36:8080/healthRecord" + interName + "?" + param
        if param == '':
            result = self.session.post(url, data=None)
        else:
            # result = requests.get(path, headers=self.headers)
            result = self.session.get(url, headers=self.headers, verify=False)
        print(self.session.headers)
        print(result.text)
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


if __name__ == '__main__':
    # cookie = "'beijing'=1,'上海'=2,'hangzhou'=3"
    cookie = "a =100,b=200"


    # print([i.split("=")[0] for i in cookie.split(",")])

    d = {}
    for i in cookie.split(","):
        d[i.split("=")[0]] =i.split("=")[1]
    print(d)
    # print(sys.exc_info())
    #
    # http = HTTP()
    # http.postLogin("/app/login", {'userName': 'shuyang', 'password': '07497ba923378ceada4a7f6428be9956'})
    # http.get("/encrypted/getQuestionList", 'userName=shuyang')
    # # http.get("/PersonBasicInfo/getArchiveNum", 'idCard=110101199003071970')
    # # http.get("/app/recordManager/validateIdCard", 'idCard=110101199003071970')
    # # http.get("/app/recordManager/getArchivePropertyByIdcard", 'idCard=110101199003071970')
    #
    # # http.post("/app/recordManager/save",{'fieldSourcesInfo': {'fields': ['Name', 'PermanentAddress', 'IdCard', 'DateOfBirth', 'Sex', 'NationCode'], 'sourceType': ''}, 'hasAudio': 1, 'personBasicInfo': {'archiveNum': '', 'bloodType': '0', 'contactsName': '金浩', 'contactsPhone': '13816109050', 'dateOfBirth': '1980-04-11', 'degree': '0', 'environmentCorral': '3', 'environmentFuelType': '2', 'environmentKitchenAeration': '1', 'environmentToilet': '2', 'environmentWater': '1', 'idCard': '310101198004110014', 'itemList': [{'code': '0', 'type': 'pay_method'}, {'code': '1000', 'type': 'history_of_drug_allergy'}, {'code': '0000', 'type': 'history_of_exposure'}, {'code': '1000', 'type': 'history_of_disease'}, {'code': '0000', 'type': 'family_history_of_father'}, {'code': '0000', 'type': 'family_history_of_mother'}, {'code': '0000', 'type': 'family_history_of_siblings'}, {'code': '0000', 'type': 'family_history_of_children'}, {'code': '1', 'type': 'disablity_type'}], 'maritalStatus': '0', 'name': '许恋柏', 'nationCode': '01',"noNumberProvided": 1, 'occupation': '1', 'occupationalDiseasesFlag': '0000', 'residenceType': '1', 'rhBloodType': '0', 'sex': '1', 'workUnit': '上海智赢健康科技有限公司'}, 'recordCoverDto': {'archiveNum': '', 'archiveUnit': '大场镇大场社区卫生服务中心', 'archiveUnitCode': 184, 'archiver': '金浩', 'archiverId': 31, 'city': '重庆市', 'cityCode': 500100, 'dateOfCreateArchive': '2019-05-28', 'district': '万州区', 'districtCode': 500101, 'name': '郑龙', 'neighborhood': '大场镇', 'neighborhoodCode': 310113102, 'permanentAddress': '分水镇新石村2组112号', 'phone': '13822050583', 'presentAddress': '大场镇沪太路2660弄', 'presentCityName': '上海市', 'presentDistrictCode': 310113, 'presentDistrictName': '宝山区', 'presentProvinceName': '上海市', 'province': '重庆市', 'provinceCode': 500000, 'responsibleDoctor': '吴怡', 'responsibleDoctorId': 11, 'villageCode': 310113102001, 'villageName': '大华一村一居委会'}, 'recordTimeList': [{'endTime': 1553650391128, 'moduleName': 'BASIC', 'operationType': 0, 'recordTime': 65646, 'startTime': 1553650292628}, {'endTime': 1553650358144, 'moduleName': 'COVER', 'operationType': 0, 'recordTime': 22429, 'startTime': 1553650272310}]})


