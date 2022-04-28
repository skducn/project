# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest 之 fixture用yield实现teardown功能，测试用例执行之后的清理工作。
# yield, 当被掉函数遇到yield会停止执行，接着执行调用处的函数，调用出的函数执行完后会继续执行yield关键后面的代码
# 注意：实际中尽量少用auto=True 这个参数，可能会引发意想不到的结果！ 最常用的还是通过传递参数最好。
# ********************************************************************************************************************
import pytest
from selenium import webdriver
import time

@pytest.fixture()
def fixtureFunc():
    '''实现浏览器的打开和关闭'''
    driver = webdriver.Firefox()
    yield driver
    driver.quit()

def test_search(fixtureFunc):
    '''访问百度首页，搜索pytest字符串是否在页面源码中'''
    driver = fixtureFunc
    driver.get('http://www.baidu.com')
    driver.find_element_by_id('kw').send_keys('pytest')
    driver.find_element_by_id('su').click()
    time.sleep(3)
    source = driver.page_source
    assert 'pytest' in source

if __name__=='__main__':
    pytest.main(['-s', 'test_yield.py'])
