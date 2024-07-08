# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2020-06-10
# Description   : 配置模块 ConfigParser
# *****************************************************************
import configparser

class ConfigparserPO:

    def __init__(self, file):
        self.cf = configparser.ConfigParser()
        self.cf.read(file, encoding="utf-8-sig")
        self.file = file

    def HTTP(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def DB(self, name):
        value = self.cf.get("DB", name)
        return value

    def write(self, folder, key, value):
        self.cf[folder][key] = value  #  # Configparser_PO.cf['EXCEL']['sheetName'] = '55'  # 重新赋值
        self.cf.write(open(self.file, 'w'))



if __name__ == '__main__':

    Configparser_PO = ConfigparserPO('config.ini')

    # Configparser_PO.cf.read('config.ini')  # 读

    # Configparser_PO.write('EXCEL', 'sheetName', '355')
    # print(Configparser_PO.EXCEL('sheetName'))  # 355

    sectionName = Configparser_PO.cf.sections()  # 获取所有section名
    print(sectionName)

    # 判断配置文件中是否有已存在的section，如果不存在则创建section，并设置相应的key和value
    if 'section' not in sectionName:
        Configparser_PO.cf.add_section('section')  # 新增section, 如果已存在则报错
        Configparser_PO.cf.set('section', 'name1', 'jh2333')  # 新增 key和value （覆盖）
        Configparser_PO.cf.write(open('config.ini', 'w'))  # 写保存

    # Configparser_PO.cf.get("EXCEL",'rrr')

    print(Configparser_PO.cf.options('EXCEL'))  # ['filename', 'sheetname', 'title']


