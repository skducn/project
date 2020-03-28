# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018/4/20 15:04
# Description: HTMLTestRunner 对象层 之 运行脚本
# http://tungwaiyip.info/software/HTMLTestRunner.html
# test1,py 中类名可以是中文，测试函数必须test开头，函数内第一行注释可显示在Html中。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import unittest, time
from PO.TimePO import *
time_PO = TimePO()

class Test1(unittest.TestCase):

    def setUp(self):
        # 类的构造函数
        print("111111")

    def test123(self):
        print("66666")
        self.assertEqual("12323", u"123")

    def testbaidu(self):
        u"""百度搜索"""
        print("66666")

class Web(unittest.TestCase):
    def testtaobao(self):
        print("66666")

    def dingdong(self):
        print("1111")


if __name__ == '__main__':
    unittest.main()