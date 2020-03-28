# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018/4/20 15:04
# Description: HTMLTestRunner 对象层 之 运行脚本
# http://tungwaiyip.info/software/HTMLTestRunner.html
# test3,py 中类名可以是中文，测试函数必须test开头，函数内第一行注释可显示在Html中。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import unittest
from PO.TimePO import *
time_PO = TimePO()

class 测试(unittest.TestCase):

    def test_123(self):
        u"""函数第一行注释可作为标题"""
        print("66666")  # 第2个执行

    def test_baidu(self):
        u"""百度"""
        print("66666")  # 第3个执行

    def test_00(self):
        u"""test函数执行顺序按照 数字，字母"""
        print("66666")   # 第1个执行

class 功能(unittest.TestCase):
    def testtaobao(self):
        print("66666")

    def dingdong(self):
        print("1111")   # 不执行


if __name__ == '__main__':
    unittest.main()