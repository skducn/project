# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-19
# Description: fire模块 用来自动生成命令行接口（CLI）
# ********************************************************************************************************************

import fire

class Demo3():

    def __init__(self):

        self.x = 4
        self.y = 5

    def m(self,x,y):
        return x * y
    # (py308) localhost-2:命令行 linghuchong$ python -m fire Demo3.py Demo3 m 6 7
    # 42


    def p(self):
        return self.x * self.y
    # (py308) localhost-2:命令行 linghuchong$ python -m fire Demo3.py Demo3 p
    # 20
