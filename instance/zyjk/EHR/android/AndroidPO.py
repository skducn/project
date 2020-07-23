# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2018-7-18
# Description: android自动化测试框架
# config.py 配置文件，负责启动appium
# AndroidPO.py 函数封装包
#***************************************************************
from config import *
class AndroidPO(object):
    def __init__(self, Level_PO):
        self.Level_PO = Level_PO
    def login(self,userName,passWord):
        try:
            self.Level_PO.inputId("zy.android.healthstatisticssystem:id/et_user_name", 'zhaoyun')
            self.Level_PO.inputId("zy.android.healthstatisticssystem:id/et_user_pwd", 'Zhaoyun,./')
            self.Level_PO.clickId("zy.android.healthstatisticssystem:id/btn_login", 2)
            if self.Level_PO.getIdText("com.cetc.partybuilding:id/title_tv_name") == u"首页":
                print(u"login，登录成功")
            else:
                print (u"login，登录失败")
        except:
            print (u"错误，login，登录失败")