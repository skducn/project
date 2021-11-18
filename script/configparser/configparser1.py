# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-18
# Description   : configparser 模块用于配置文件的格式的配置
# 使用 ConfigParser 模块来读取config.ini配置文件内容，文件可包含一个或多个节（section），每个节可以有多个参数（键=值）。
# *****************************************************************
# 应用1，生成配置项
# 应用2，判断sections是否存在，不存在则新增
# 应用3，判断key是否存在，不存在则新增

'''
1.1，新增sections、key、value写入文件（key存在则替换）
1.2，新增sections（存在则报错）

2.1，获取sections列表
2.2，获取key的值
2.3，获取key（不区分大小写）的值
2.4，获取sections下所有的key，返回列表
2.5，获取sections下所有的key和value，返回列表
2.6，遍历获取sections下所有的key

3，删除sections、key

4，getfloat将值改为float

5，判断sections（区分大小写）是否存在
'''

import configparser

class ReadConfig:

    def __init__(self):
        self.cf = configparser.ConfigParser()
        # self.cf.read('config.ini', encoding="utf-8-sig")
        self.cf.read('config.ini', encoding="gbk")

    def get_system(self, name):
        value = self.cf.get("SYSTEM", name)
        return value

    def get_test(self, name):
        value = self.cf.get("TEST", name)
        return value

    def get_dev(self, name):
        value = self.cf.get("DEV", name)
        return value


if __name__ == '__main__':

    r = ReadConfig()

    print(r.get_test('ip'))  # 192.168.0.243

    print("1.1，新增sections、key、value写入文件（key存在则替换）".center(100, "-"))
    r.cf['topsecret.server.com'] = {'Host Port': '50022', 'ForwardX11': 'no1'}
    with open('config.ini', 'w') as configfile:
        r.cf.write(configfile)

    # print("1.2，新增sections（存在则报错）".center(100, "-"))
    # r.cf.add_section("john")  # 如果存在则保存
    # r.cf.set('john', 'k2', '11111')
    # with open('config.ini', 'w') as f:
    #     r.cf.write(f)


    print("2.1，获取sections列表".center(100, "-"))
    print(r.cf.sections())  # ['SYSTEM', 'TEST', 'DEV', 'topsecret.server.com']

    print("2.2，获取key的值".center(100, "-"))
    print(r.cf.get("SYSTEM", 'reportname'))  # report.html

    print("2.3，获取key（不区分大小写）的值".center(100, "-"))
    print(r.cf['TEST']['ip'])  # 192.168.0.243
    print(r.cf['TEST']['IP'])  # 192.168.0.243
    print(r.cf['TEST']['Ip'])  # 192.168.0.243

    print("2.4，获取sections下所有的key，返回列表".center(100, "-"))
    print(r.cf.options('topsecret.server.com'))  # ['host port', 'forwardx11']
    print(r.cf.options('topsecret.server.com')[1])  # forwardx11

    print("2.5，获取sections下所有的key和value，返回列表".center(100, "-"))
    print(r.cf.items('topsecret.server.com'))  # [('host port', '50022'), ('forwardx11', 'no1')]
    print(r.cf.items('topsecret.server.com')[0])  # ('host port', '50022')
    print(r.cf.items('topsecret.server.com')[0][1])  # 50022

    print("2.6，遍历获取sections下所有的key".center(100, "-"))
    for key in r.cf['SYSTEM']:
        print(key)
        # projectname
        # excelname
        # reportname
        # switchenv


    print("3，删除sections、key".center(100, "-"))
    r.cf.remove_section('john')  # 删除 section（sections即使不存在，删除也不报错）
    # r.cf.remove_option('john', 'k2')  # 删除一个key (key不存在，则报错)
    with open('config.ini', 'w') as f:
        r.cf.write(f)


    print("4，getfloat将值改为float".center(100, "-"))
    print(r.cf.get("TEST", "port"))  # 8001
    print(r.cf.getfloat("TEST", "port"))  # 8001.0


    print("5，判断sections（区分大小写）是否存在".center(100, "-"))
    print('bitbucket.org' in r.cf)  # False
    print('system' in r.cf)  # False
    print('TEST' in r.cf)  # True
    print(r.cf.has_section("SYSTEM"))  # True
    print(r.cf.has_option("TEST", "iP"))  # True