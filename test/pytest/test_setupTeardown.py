# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest 之 xunit fixture的4个级别（function,method,class,module）
# 1.每个级别的setup/teardown都可以多次复用
# 2.如果相应的初始化函数执行失败或者被跳过则不会执行teardown方法
# 3.在pytest4.2之前，xunit fixture 不遵循fixture的作用规则的，因此可以在一个session级别且参数auto=True的fixture前执行setup_method方法
# 但是到目前为止，所有的xunit fixture已经遵循了fixture执行的规则
官方文档：https://buildmedia.readthedocs.org/media/pdf/pytest/latest/pytest.pdf
# ********************************************************************************************************************
import pytest

# # function级别
# def setup_function(function):
#     print('\nfunction setup ---------')
# def teardown_function(function):
#     print('function teardown ---------')
# def test_function_1():
#     print('函数1')
# def test_function_2():
#     print('函数2')
#
#
# # method级别
# class TestMethod(object):
#     def setup_method(self, method):
#         print('\nmethod setup +++++++')
#     def teardown_method(self, method):
#         print('method teardown +++++++')
#     def test_method_1(self):
#         print('测试方法1')
#     def test_method_2(self):
#         print('测试方法2')


# # class级别
# class TestClass(object):
#     @classmethod
#     def setup_class(cls):
#         print('\nclass setup for {} ~~~~~~~~'.format(cls.__name__))
#     @classmethod
#     def teardown_class(cls):
#         print('\nclass teardown ~~~~~~~~')
#     def test_1(self):
#         print('test1')
#     def test_2(self):
#         print('test2')


# module级别
def setup_module(module):
    print('\nsetup_module() for {}'.format(module.__name__))
def teardown_module(module):
    print('\nteardown_module() for {}'.format(module.__name__))
def test_1():
    print('test_1()')
def test_2():
    print('test_2()')

class TestClass(object):
    def test_3(self):
        print('self.test_3()')
    def test_4(self):
        print('self.test_4()')



if __name__ == '__main__':
    pytest.main(['-sq', 'test_setupTeardown.py'])
