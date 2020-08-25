# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2020-06-10
# Description   : 配置文件 config.ini
# ConfigParser 读取配置文件
# *****************************************************************

import os, codecs, configparser, platform

# 获取当前路径
currentPath = os.path.split(os.path.realpath(__file__))[0]
getConfig = os.path.join(currentPath, "config.ini")


class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(getConfig, encoding="utf-8-sig")

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_excel(self, name):
        value = self.cf.get("EXCEL", name)
        return value

    def get_user(self, name):
        value = self.cf.get("USER", name)
        return value

    def get_database(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_interface(self, name):
        value = self.cf.get("INTERFACE", name)
        return value


if __name__ == '__main__':
    print(currentPath)
    print(getConfig)
    r = ReadConfig()
    print(r.get_database('host'))
