# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2018-7-18
# Description: android自动化测试框架
# config.py 配置文件，负责启动appium
# AndroidPO.py 函数封装包
#***************************************************************
import sys
if len(sys.argv) != 3:
    print(u"app登录，参数1：手机，参数2：密码\n"\
    u"如：" + str(sys.argv[0]).split(".")[0] + u" 13636371320 123456\n")
else:
    from AndroidPO import *
    Level_PO = LevelPO(driver)
    Android_PO = AndroidPO(Level_PO)
    # app登录，参数1：手机号，参数2：密码
    Android_PO.login(sys.argv[1], sys.argv[2])