# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2021/9/16
# Description: pytest
# pip3 install -U pytest
# 官网： https://docs.pytest.org/en/latest/contents.html

# 第三方插件，请到http://plugincompat.herokuapp.com/ 和 https://pypi.python.org/pypi?%3Aaction=search&term=pytest-&submit=search 查找

# 支持参数化
# 能够支持简单的单元测试和复杂的功能测试，还可以用来做selenium/appnium等自动化测试、接口自动化测试（pytest+requests）
# pytest具有很多第三方插件，并且可以自定义扩展，比较好用的如pytest-selenium（集成selenium）、pytest-html（完美html测试报告生成）、pytest-rerunfailures（失败case重复执行）、pytest-xdist（多CPU分发）等
# 测试用例的skip和xfail处理
# 可以很好的和jenkins集成
# report框架----allure 也支持了pytest


# 如何编写pytest测试样例?
# 测试文件以test_开头（以_test结尾也可以）
# 测试类以Test开头，并且不能带有 init 方法
# 测试函数以test_开头
# 断言使用基本的assert即可
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import pytest


# # 实例1，执行1个test开头的方法
# 结果：F  ,执行后报错，因为func(3)不返回5。
# # pytest pytest1.py
# def func(x):
#     return x + 1
#
# def test_answer():
#     assert func(3) == 5


# # 实例2，在一个类中执行多个测试方法，注意只执行test开头的方法
# # # 结果：.F  ,表示第一个方法正确，第二个错误
# # # pytest pytest.py -q   //参数 quiet 表示减少冗长，不展示pytest的版本信息
# # 类与实例 TestClass:
# #     def test_one(self):
# #         x = "this"
# #         assert 'h' in x
# #
# #     def test_two(self):
# #         x = "hello"
# #         assert hasattr(x, 'check')



