# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2016-7-29
# Description: 百度首页登录对象层，定义元素与封装对象
#***************************************************************

from selenium.webdriver.common.by import By
from Public.PageObject.BasePage import BasePage
from time import sleep

# 继承BasePage类,操作登录页面元素
class LoginPO(BasePage):

    # 定位器，通过元素属性定位元素对象
    # 用户名
    def input_username(self, username):
        self.find_element(*(By.ID, '_username')).clear()
        self.find_element(*(By.ID, '_username')).send_keys(username)

    # 密码
    def input_password(self, password):
        self.find_element(*(By.ID, '_password')).clear()
        self.find_element(*(By.ID, '_password')).send_keys(password)

    # 登录
    def click_submit(self, t):
        self.find_element(*(By.TAG_NAME, "button")).click()
        sleep(t)

    # 退出
    def click_logout(self, t):
        self.find_element(*(By.XPATH, "//a[@class='logout']")).click()
        sleep(t)