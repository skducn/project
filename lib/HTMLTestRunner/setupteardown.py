# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2019/1/15
# Description: web自动化打开页面  common/html1.py
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import unittest
from test.HTMLTestRunner.calculate1 import *

class SetupTeardwon(unittest.TestCase): #继承类，写测试用例
    def setUp(self):               # 测试前环境准备
        print("用例执行前环境准备")

    def tearDown(self):            #测试后环境还原
        print("用例执行后环境还原")
