# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest 框架之命令行参数详解

# ********************************************************************************************************************
import pytest
from selenium import webdriver

def testOpenUrl():
    try:
        driver = webdriver.Firefox() # 打开浏览器
        driver.get('http://www.baidu.com') # 访问百度
        title = driver.title # 获取百度首页的title
        assert title == '百度一下，你就知道' # 断言
        print(driver.title)
    except AssertionError:
        raise AssertionError('断言失败!')
    driver.quit()

def testBaidu():
    driver = webdriver.Firefox() # 打开浏览器
    driver.get('http://www.baidu.com') # 访问百度
    title = driver.title # 获取百度首页的title
    assert title == '百度一下，你就知道' # 断言

if __name__ == '__main__':
    pytest.main(["-sv","test_command.py"])