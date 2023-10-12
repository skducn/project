# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2020-06-10
# Description   : 配置模块 ConfigParser
# 读取 config.ini 配置文件
# *****************************************************************

import os, codecs, configparser, platform

# currentPath = os.path.split(os.path.realpath(__file__))[0]  # 获取当前路径
# print(currentPath)  # /Users/linghuchong/Downloads/51/Python/project/instance/config
# getConfig = os.path.join(currentPath, "Configparser.ini")

class ConfigparserPO:

    def __init__(self):
        self.cf = configparser.ConfigParser()
        # self.cf.read(getConfig, encoding="utf-8-sig")
        self.cf.read("Configparser.ini", encoding="utf-8-sig")

    def HTTP(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def USER(self, name):
        value = self.cf.get("USER", name)
        return value

    def DB(self, name):
        value = self.cf.get("DB", name)
        return value

    def EXCEL(self, name):
        value = self.cf.get("EXCEL", name)
        return value

if __name__ == '__main__':

    Configparser_PO = ConfigparserPO()
    print(Configparser_PO.DB('host'))  # 192.168.0.195
