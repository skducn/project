# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2020-06-10
# Description   : 配置模块 ConfigParser
# *****************************************************************
import configparser

class ConfigparserPO:

    def __init__(self):
        self.cf = configparser.ConfigParser()
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
