# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2021/9/16
# Description: pytest 运行指定的case
# pip3 install -U pytest
# pip install -U pytest-html    //测试报告包
# pytest test_pytest1.py --html=report.html  //运行后生成测试报告（htmlReport）

# 如何运行指定的case？
# 注意：需要被测试的class类名，必须以T开头，不然pytest是不会去运行该class的。

# 模式1， 执行此文件所有的case
# 执行，pytest test_specifyCase.py
# 结果：test_specifyCase.py .F.F

# 模式2，执行此文件中的TestClassOne类下的两个cases:
# 执行，pytest test_specifyCase.py::TestClassOne
# 结果：test_specifyCase.py .F

# 模式3，执行此文件中TestClassTwo类下的test_one:
# 执行，pytest test_specifyCase.py::TestClassTwo::test_one
# 结果：test_specifyCase.py .
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import pytest


class TestClassOne(object):
    def test_one(self):
        x = "this"
        assert 't'in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')


class TestClassTwo(object):
    def test_one(self):
        x = "iphone"
        assert 'p'in x

    def test_two(self):
        x = "apple"
        assert hasattr(x, 'check')




