# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest 之 @pytest.fixture() 与 @pytest.mark.usefixtures()
# fixtur作用范围: 所有的实例默认都是函数级别的，所以测试函数只要调用了fixture
# ********************************************************************************************************************
import pytest


# fixture实现setup

# 实例1：被测函数将fixture作为参数调用，如返回值。
# 分析：fixtureFunc 这个函数就是一个fixture，fixture函数内部可以实现一些初始化操作，支持return返回值。
# 注意：可定义多个相同的fixture，但只处理最后一个fixture
@pytest.fixture()
def fixtureFunc1():
    print("1,我优先执行")
    return '---------share'

def test_fixture1(fixtureFunc1):
    print('2, {}'.format(fixtureFunc1))   # a100 ---------share

class TestFixture1(object):
    def test_fixture_class(self, fixtureFunc1):
        print('3 "{}"'.format(fixtureFunc1))  # b200 "---------share"
#
#
# # # ******************************************
# # 实例2：被测函数或者类前使用@pytest.mark.usefixtures('fixture')装饰器装饰
# # fixture函数内部可以实现一些初始化操作，但不支持return返回值。
# @pytest.fixture()
# def fixtureFunc2():
#     print('---------share2')
#     return '---------share33333'
#
# @pytest.mark.usefixtures('fixtureFunc2')
# def test_fixture2():
#     print('a1')
#
#
# @pytest.mark.usefixtures('fixtureFunc2')
# class TestFixture2(object):
#     def test_fixture_class(self):
#         print('a2')


# fixture实现teardown
# 关键字 yeild ,作用其实和return差不多，也能够返回数据给调用者，
# 唯一的不同是被掉函数执行遇到yield会停止执行，接着执行调用处的函数，调用出的函数执行完后会继续执行yield关键后面的代码.
# import pytest
# from selenium import webdriver
# import time
# @pytest.fixture()
# def fixtureFunc():
#     '''实现浏览器的打开和关闭'''
#     driver = webdriver.Firefox()
#     yield driver
#     driver.quit()
# def test_search(fixtureFunc):
#     '''访问百度首页，搜索pytest字符串是否在页面源码中'''
#     driver = fixtureFunc
#     driver.get('http://www.baidu.com')
#     driver.find_element_by_id('kw').send_keys('pytest')
#     driver.find_element_by_id('su').click()
#     time.sleep(3)
#     source = driver.page_source
#     assert 'pytest' in source
# if __name__=='__main__':
#     pytest.main(['--setup-show', 'test_fixture.py'])


if __name__ =='__main__':
    pytest.main(['-s', 'test_fixture.py'])