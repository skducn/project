# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2019/1/15
# Description: web自动化打开页面  common/html1.py
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PO.webdriver import *
import unittest, time


class Baidu(unittest.TestCase):
    def setUp(self):
        self.webdriver_PO = WebdriverPO("chrome")
        self.driver = self.webdriver_PO.open('https://www.baidu.com/')


    def test_baidu_search(self):
        """百度搜索"""
        self.driver.find_element_by_id("kw").clear()
        self.driver.find_element_by_id("kw").send_keys("unittest")
        self.driver.find_element_by_id("su").click()
        time.sleep(3)
        title = self.driver.title
        self.assertEqual(title, u"unittest_百度搜索")

    def test_baidu_set(self):
        """百度设置"""
        self.driver = self.webdriver_PO.open('https://www.baidu.com/gaoji/preferences.html')
        m = self.driver.find_element_by_name("NR")
        time.sleep(1)
        m.find_element_by_xpath("//option[@value='50']").click()
        time.sleep(1)

    def tearDown(self):
        self.webdriver_PO.close()

if __name__ == "__main__":
    unittest.main()