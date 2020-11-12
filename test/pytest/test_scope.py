# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest 之 fixture作用范围 scope ， 测试用例执行之前的准备工作
# scope 参数值分别是 session， module，class，function
# 1.session 会话级别（通常这个级别会结合conftest.py文件使用）
# 2.module 模块级别，模块里所有的用例执行前执行一次module级别的fixture
# 3.class 类级级别，每个类执行前都会执行一次class级别的fixture
# 4.function ：函数级别，这个是默认的模式，函数级别的，每个测试用例执行前都会执行一次function级别的fixture
# ********************************************************************************************************************
import pytest

# 整个模块只执行了一次module级别的fixture ，每个类分别执行了一次class级别的fixture， 而每一个函数之前都执行了一次function级别的fixture
# 注意：这些都只是做了测试用例执行之前的准备工作

@pytest.fixture(scope='module', autouse=True)
def module_fixture():
    print('\n我是module fixture ~~~~~~~~~')

@pytest.fixture(scope='class')
def class_fixture():
    print('\n我是class fixture +++++++++')

@pytest.fixture(scope='function', autouse=True)
def func_fixture():
    print('\n我是function fixture--------')

def test_1():
    print('我是test1')

@pytest.mark.usefixtures('class_fixture')
class TestFixture1(object):
    def test_2(self):
        print('我是class1里面的test2')
    def test_3(self):
        print('我是class1里面的test3')
@pytest.mark.usefixtures('class_fixture')
class TestFixture2(object):
    def test_4(self):
        print('我是class2里面的test4')
    def test_5(self):
        print('我是class2里面的test5')

if __name__=='__main__':
    pytest.main(['-s', 'test_scope.py'])
