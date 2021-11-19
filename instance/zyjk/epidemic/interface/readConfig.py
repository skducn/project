# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-19
# Description   : 读取 config.ini , configparser
# ConfigParser 是用来读取config.ini配置文件的包
# *****************************************************************

import configparser, codecs

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
        self.cf.read('config.ini')
        # self.cf.read('config.ini', encoding="utf-8-sig")

    def get_env(self, name):
        value = self.cf.get("ENV", name)
        return value

    def get_system(self, name):
        value = self.cf.get("SYSTEM", name)
        return value

    def get_test(self, name):
        value = self.cf.get("TEST", name)
        return value

    def get_dev(self, name):
        value = self.cf.get("DEV", name)
        return value

