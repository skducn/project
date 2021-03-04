# -*- coding: utf-8 -*-
# *****************************************************************
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

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_system(self, name):
        value = self.cf.get("SYSTEM", name)
        return value

    def get_redis(self, name):
        value = self.cf.get("REDIS", name)
        return value


if __name__ == '__main__':
    print(proDir)
    print(configPath)
    r = ReadConfig()
    print(r.get_db('host'))
