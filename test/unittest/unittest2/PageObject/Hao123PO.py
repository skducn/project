# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2016-7-29
# Description: Hao123页对象层，定义元素与封装对象
#***************************************************************

from selenium.webdriver.common.by import By
from Public.PageObject.BasePage import BasePage

# 继承BasePage类,操作登录页面元素
class Hao123PO(BasePage):

    # 定位器，通过元素属性定位元素对象

    # hao123 => 百度首页
    hao123BaiduHome_loc = (By.XPATH, "//div[@id='u']/a[1]")
    def click_hao123BaiduHome(self):
        self.find_element(*self.hao123BaiduHome_loc).click()

    # hao123 => search => keyword
    hao123Search_loc = (By.ID,'search-input')
    def input_hao123Search(self, keyword):
        self.find_element(*self.hao123Search_loc).clear()
        self.find_element(*self.hao123Search_loc).send_keys(keyword)

    # hao123 => search => 百度一下
    hao123Baiduyixia_loc = (By.XPATH, "//form[@id='search-form']/div[2]")
    def click_hao123Baiduyixia(self): self.find_element(*self.hao123Baiduyixia_loc).click()


    # 设置
    hao123SearchSetup_loc = (By.XPATH, "//div[@id='u']/a[2]")
    def click_hao123SearchSetup(self):
        return self.find_element(*self.hao123SearchSetup_loc)





