# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2019-9-19
# Description: fake
# 关于大数据测试，你一定要试试python的fake库！ http://www.51testing.com/html/53/15150753-7793925.html
# 官网 https://faker.readthedocs.io/en/master/
# pip3.9 install faker

# 银行卡号查询 https://www.haoshudi.com/yinhangka/
# 身份证查询 https://www.haoshudi.com/shenfenzheng/
# 手机号码查询 https://www.shoujichahao.com/，https://www.haoshudi.com/
# ***************************************************************

import sys,os
from faker import Faker
from faker.providers import internet


list1 = []
list3 = ['今天', '你好', '谢谢', '意愿']


class FakePO():

    def __init__(self):

        self.faker = Faker(locale='zh_CN')


    def genName(self, country, n=1):

        '''1 生成N个姓名 '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.name()
        elif n > 0:
            for i in range(n):
                list1.append(faker.name())
        else:
            return None
        return list1


    def genPhone_number(self, country, n=1):

        '''2 生成N个手机号 '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.phone_number()
        elif n > 0:
            for i in range(n):
                list1.append(faker.phone_number())
        else:
            return None
        return list1



    def genSsn(self, country, n=1):

        '''3 生成N个身份证 '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.ssn()
        elif n > 0:
            for i in range(n):
                list1.append(faker.ssn())
        else:
            return None
        return list1



    def genAddress(self, country, n=1):

        '''4 生成N个地址 '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.address()
        elif n > 0:
            for i in range(n):
                list1.append(faker.address())
        else:
            return None
        return list1


    def genEmail(self, n=1):

        '''5 生成N个Email '''

        list1 = []
        if n == 1:
            return self.faker.email()
        elif n > 0:
            for i in range(n):
                list1.append(self.faker.email())
        else:
            return None
        return list1


    def genCompany(self, country, n=1):

        '''6 生成N个公司 '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.company()
        elif n > 0:
            for i in range(n):
                list1.append(faker.company())
        else:
            return None
        return list1


    def genUrl(self, n=1):

        '''7 生成N个url '''

        list1 = []
        if n == 1:
            return self.faker.url()
        elif n > 0:
            for i in range(n):
                list1.append(self.faker.url())
        else:
            return None
        return list1


    def genLatitudeLongitude(self, n=1):

        '''8 生成N个经度纬度 '''

        dict1 = {}
        for i in range(n):
            longitude = str(self.faker.longitude())
            latitude = str(self.faker.latitude())
            dict1[longitude] = latitude
        return dict1



    def genIpv4(self, n=1):

        '''9 生成N个ip '''

        list1 = []
        if n == 1:
            return self.faker.ipv4(network=False)
        elif n > 0 :
            for i in range(n):
                list1.append(self.faker.ipv4(network=False))
        else:
            return None
        return list1


    def genPostcode(self, country, n=1):

        '''10 生成N个邮编 '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.postcode()
        elif n > 0 :
            for i in range(n):
                list1.append(faker.postcode())
        else:
            return None
        return list1


    def genText(self, country, n=1):

        '''10 生成N个text '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.text()
        elif n > 0 :
            for i in range(n):
                list1.append(faker.text())
        else:
            return None
        return list1


    def genTest(self, varList, n=1):

        ''' 生成N个测试数据 '''

        list1 = []
        list2 = []
        for k in range(n):
            for i in range(len(varList)):
                if varList[i] == "genName":
                    list1.append(self.faker.name())
                if varList[i] == "genAddress":
                    list1.append(self.faker.address())
                if varList[i] == "genPostcode":
                    list1.append(self.faker.postcode())
                if varList[i] == "genPhone_number":
                    list1.append(self.faker.phone_number())
                if varList[i] == "genSsn":
                    list1.append(self.faker.ssn())
                if varList[i] == "genEmail":
                    list1.append(self.faker.email())
                if varList[i] == "genCompany":
                    list1.append(self.faker.company())
                if varList[i] == "genIpv4":
                    list1.append(self.faker.ipv4(network=False))
                if varList[i] == "genUrl":
                    list1.append(self.faker.url())
                if varList[i] == "genLatitudeLongitude":
                    dict1 = {}
                    longitude = str(self.faker.longitude())
                    latitude = str(self.faker.latitude())
                    dict1[longitude] = latitude
                    list1.append(dict1)

            list2.append(list1)
            list1 = []
        return list2




if __name__ == '__main__':

    Fake_PO = FakePO()

    #
    # for i in range(30):


    #     test = faker.sentence(ext_word_list=list3)
    #     zh_text = faker_zh.text()
    #
    #     # data = [zh_text,zh_add,test,zh_name,zh_company,zh_phone,zh_email,zh_birthday,zh_city,zh_ssn,url,src,name,jp_name]
    #     data = [zh_add,zh_name,zh_company,zh_phone,zh_email,zh_birthday,zh_city,zh_ssn,url,src,name,jp_name]
    #     print(data)
    #     # list1.append(data)
    #     #
    #     # print(list1)



    print("1，生成N个姓名".center(100, "-"))
    print(Fake_PO.genName("zh_CN", 5))  # ['曾勇', '程旭', '金云', '张桂芝', '潘凤兰']
    print(Fake_PO.genName('ja_JP', 5))  # ['橋本 翔太', '山田 七夏', '山口 香織', '山口 陽一', '加藤 花子']
    print(Fake_PO.genName('zh_TW', 5))  # ['陳瑋婷', '彭志偉', '李家豪', '楊淑華', '孫佩君']
    print(Fake_PO.genName('ko_KR', 5))  # ['김병철', '김혜진', '엄영길', '이영자', '곽경숙']
    print(Fake_PO.genName('it_IT', 5))    # ['Rembrandt Gargallo', 'Rosalia Foscari-Salvo', 'Cecilia Golino', 'Pierpaolo Zampa', 'Lando Scialpi']


    print("2，生成N个手机号".center(100, "-"))
    print(Fake_PO.genPhone_number('Zh_CN', 5))
    print(Fake_PO.genPhone_number('ja_JP', 5))
    print(Fake_PO.genPhone_number('zh_TW', 5))
    print(Fake_PO.genPhone_number('ko_KR', 5))
    print(Fake_PO.genPhone_number('it_IT', 5))


    print("3，生成N个身份证".center(100, "-"))
    print(Fake_PO.genSsn('Zh_CN', 5))
    print(Fake_PO.genSsn('ja_JP', 5))
    print(Fake_PO.genSsn('zh_TW', 5))
    print(Fake_PO.genSsn('ko_KR', 5))
    print(Fake_PO.genSsn('it_IT', 5))


    print("4，生成N个地址".center(100, "-"))
    print(Fake_PO.genAddress('zh_CN', 5))
    print(Fake_PO.genAddress('ja_JP', 5))
    print(Fake_PO.genAddress('zh_TW', 5))
    print(Fake_PO.genAddress('ko_KR', 5))
    print(Fake_PO.genAddress('it_IT', 5))


    print("5，生成N个Email".center(100, "-"))
    print(Fake_PO.genEmail(5))

    print("6，生成N个公司".center(100, "-"))
    print(Fake_PO.genCompany('zh_CN', 5))
    print(Fake_PO.genCompany('ja_JP', 5))
    print(Fake_PO.genCompany('zh_TW', 5))
    print(Fake_PO.genCompany('ko_KR', 5))
    print(Fake_PO.genCompany('it_IT', 5))


    print("7，生成N个url".center(100, "-"))
    print(Fake_PO.genUrl(5))


    print("8，生成N个经纬度".center(100, "-"))
    print(Fake_PO.genLatitudeLongitude(5))


    print("9，生成N个ip地址".center(100, "-"))
    print(Fake_PO.genIpv4(5))


    print("10，生成N个邮编".center(100, "-"))
    print(Fake_PO.genPostcode('zh_CN', 5))
    print(Fake_PO.genPostcode('ja_JP', 5))
    print(Fake_PO.genPostcode('zh_TW', 5))
    print(Fake_PO.genPostcode('ko_KR', 5))
    print(Fake_PO.genPostcode('it_IT', 5))


    print("11，生成N个文本".center(100, "-"))
    print(Fake_PO.genText('zh_CN', 5))
    print(Fake_PO.genText('ja_JP', 5))
    print(Fake_PO.genText('zh_TW', 5))
    print(Fake_PO.genText('ko_KR', 5))
    print(Fake_PO.genText('it_IT', 5))


    print("12，生成10条测试数据，写入表格".center(100, "-"))
    print(Fake_PO.genTest(['genName', 'genPhone_number', 'genPostcode','genSsn', 'genAddress','genEmail','genCompany','genIpv4','genUrl','genLatitudeLongitude'], 5))


