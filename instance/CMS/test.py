# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: CMS web自动化，登录
# https://blog.csdn.net/xc_zhou/article/details/82415870 chrome浏览器的options参数
# *****************************************************************

from CMS.PageObject.CmsPO import *
Cms_PO = CmsPO(Level_PO)

'''登录'''
Cms_PO.login(varURL, "test", "jinhao")

'''发帖'''
Cms_PO.