# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description:
# *****************************************************************

# from PO.WebPO import *
# Web_PO = WebPO("chrome")
#
# Web_PO.openURL("https://kyfw.12306.cn/otn/resources/login.html")
#

# def abc():
#     x =10
#     print(x)
# abc()

def enclosing_scope_example():
    x =11
    def inner():
        print(x)
    inner()

enclosing_scope_example()

x =12
def global_score_example():
    print(x)

global_score_example()











