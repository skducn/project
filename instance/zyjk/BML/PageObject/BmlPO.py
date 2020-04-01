# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: 白茅岭对象库
# *****************************************************************

from instance.zyjk.BML.config import *

class BmlPO(object):

    def __init__(self, Level_PO):
        self.Level_PO = Level_PO

    def login(self, dimUrl, dimUsername, dimPassword):

        ''' 登录 '''

        self.Level_PO.openURL(dimUrl, 1)
        self.Level_PO.inputXpath("//input[@placeholder='请输入用户名']", dimUsername)
        self.Level_PO.inputXpath("//input[@placeholder='请输入密码']", dimPassword)
        self.Level_PO.clickXpath("//button[@class='el-button login-button el-button--default']", 2)