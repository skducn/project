# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2019/1/15
# Description:
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import unittest
from test.HTMLTestRunner.calculate1 import *
from test.HTMLTestRunner.setupteardown import SetupTeardwon

class TestMath(SetupTeardwon): #继承类，写测试用例

    def test_add1(self):            # 测试方法，必须以test开头
        u"""测试加法用例，数字为3,2"""
        math1=Math(3,2)
        self.assertEqual(math1.add(),5)

    def test_add2(self):            # 测试方法，必须以test开头
        u"""测试加法用例，数字为1,1"""
        math1=Math(1,1)
        self.assertEqual(math1.add(),2)

class TestEnglish(SetupTeardwon): #继承类，写测试用例

    def test_English1(self):            # 测试方法，必须以test开头
        u"""测试加法用例，数字为3,2"""
        math1=Math(3,2)
        self.assertEqual(math1.add(),5)

    def test_english2(self):            # 测试方法，必须以test开头
        u"""测试加法用例，数字为1,1"""
        math1=Math(1,1)
        self.assertEqual(math1.add(),2)