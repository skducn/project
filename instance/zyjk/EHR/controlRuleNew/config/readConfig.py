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
        # fd = open(configPath, "r")
        # data = fd.read()
        #
        # #  remove BOM
        # if data[:3] == codecs.BOM_UTF8:
        #     data = data[3:]
        #     file = codecs.open(configPath, "w")
        #     file.write(data)
        #     file.close()
        # fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(getConfig, encoding="utf-8-sig")

    def get_filter(self, name):
        value = self.cf.get("FILTER", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_jar(self, name):
        value = self.cf.get("JAR", name)
        return value

    def get_excel(self, name):
        value = self.cf.get("EXCEL", name)
        return value

    # def get_log(self, name):
    #     value = self.cf.get("LOG", name)
    #     return value

    def get_database(self, name):
        value = self.cf.get("DATABASE", name)
        return value

if __name__ == '__main__':
    print(currentPath)
    print(getConfig)
    r = ReadConfig()
    print(r.get_jar('jar'))
