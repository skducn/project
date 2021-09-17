# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2021/9/16
# Description: pytest  自定义的 markers
# 自定义一个mark，使用 @pytest.mark.webtest
# 对函数标记 webtest
# 1，通过 py.test -v -m webtest 只运行标记了webtest的函数
# 2，通过 py.test -v -m "not webtest"  运行未标记webtest的函数
# 3，通过 -v 执行指定的函数ID， py.test -v test_markers.py::TestClass::test_method 来运行指定的函数
# 4，通过 -k 执行模糊匹配名字子串， py.test -v -k http 表示执行函数名中带有http的函数； py.test -k "not send_http" -v 同样表示执行函数名中不带send_http的函数

# 在pytest.ini中注册markers
# # content of pytest.ini
# [pytest]
# markers =
#     webtest: mark a test as a webtest.
#     addopts = --pyargs
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import pytest

@pytest.mark.webtest
def test_send_http():
    pass # perform some webtest test for your app

def test_something_quick():
    pass

def test_another():
    pass

class TestClass:
    def test_method(self):
        pass


# py.test test_markers.py -v -m webtest 只运行标记了test_send_http()函数
# 结果： test_markers.py::test_send_http PASSED


# py.test test_markers.py -v -m "not webtest" 运行未标记webtest的其他3个函数
# 结果：
# test_markers.py::test_something_quick PASSED                                                                                                                                                                                                  [ 33%]
# test_markers.py::test_another PASSED                                                                                                                                                                                                          [ 66%]
# test_markers.py::TestClass::test_method PASSED


# pytest test_markers.py::TestClass::test_method -v
# 结果：test_markers.py::TestClass::test_method PASSED

# pytest -v test_markers.py -k http
# 结果：test_markers.py::test_send_http PASSED


# pytest -v test_markers.py -k "not send_ht"
# 结果：
# test_markers.py::test_something_quick PASSED                                                                                                                                                                                                  [ 33%]
# test_markers.py::test_another PASSED                                                                                                                                                                                                          [ 66%]
# test_markers.py::TestClass::test_method PASSED