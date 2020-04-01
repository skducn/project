# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: CMS对象库
# *****************************************************************

from CMS.config.config import *

class CmsPO(object):

    def __init__(self, Level_PO):
        self.Level_PO = Level_PO

    def login(self, dimUrl, dimUsername, dimPassword):

        ''' 登录 '''
        self.Level_PO.openURL(dimUrl, 1)
        if self.Level_PO.isElementName("userName"):
            ''' 第一次登录 '''
            self.Level_PO.inputName("userName", dimUsername)
            self.Level_PO.inputName("userPass", dimPassword)
            self.Level_PO.clickId("button", 2)
        else:
            '''非第一次登录'''
            self.Level_PO.inputName("userPass", dimPassword)
            self.Level_PO.clickId("button2", 2)

