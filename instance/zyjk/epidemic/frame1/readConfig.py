# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-19
# Description   : 读取 config.ini , configparser
# ConfigParser 是用来读取config.ini配置文件的包
# *****************************************************************

import os, codecs, configparser, platform

# 获取当前路径
proDir = os.path.split(os.path.realpath(__file__))[0]

if platform.system() == 'Darwin':
    configPath = os.path.join(proDir + "/config//", "config.ini")
if platform.system() == 'Windows':
    configPath = os.path.join(proDir + "\config\\", "config.ini")

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
        self.cf.read(configPath, encoding="utf-8-sig")

    def get_system(self, name):
        value = self.cf.get("SYSTEM", name)
        return value

    def get_test(self, name):
        value = self.cf.get("TEST", name)
        return value

    def get_dev(self, name):
        value = self.cf.get("DEV", name)
        return value


    #
    # def get_headers(self, name):
    #     value = self.cf.get("HEADERS", name)
    #     return value

    # def set_headers(self, name, value):
    #     self.cf.set("HEADERS", name, value)
    #     with open(configPath, 'w+') as f:
    #         self.cf.write(f)

    # def get_url(self, name):
    #     value = self.cf.get("URL", name)
    #     return value
    #
    # def get_db(self, name):
    #     value = self.cf.get("DATABASE", name)
    #     return value


if __name__ == '__main__':
    print(proDir)  # D:\51\python\project\instance\zyjk\epidemic\frame1
    print(configPath)  # D:\51\python\project\instance\zyjk\epidemic\frame1\config\config.ini
    r = ReadConfig()
    print(r.get_test('ip'))  # 192.168.0.243
