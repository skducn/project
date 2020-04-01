# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2016-7-29
# Description: 页面基本操作方法：如open，input_username，input_password，click_submit
#***************************************************************

'''
页面对象层只关心元素定位问题
'''

from selenium.webdriver.common.by import By
from Public.PageObject.BasePage import BasePage

# 继承BasePage类,操作登录页面元素

class LoginPage(BasePage):

    # 定位器，通过元素属性定位元素对象
    username_loc = (By.NAME, 'email')
    password_loc = (By.NAME, 'password')
    submit_loc = (By.ID, 'dologin')
    span_loc = (By.CSS_SELECTOR, "div.error-tt>p")
    dynpw_loc = (By.ID, "lbDynPw")
    userid_loc = (By.ID, "spnUid")

    # 通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    # 打开网页
    def open(self):
        # 调用page中的_open打开连接
        self._open(self.base_url, self.pagetitle)

    # 输入用户名：调用send_keys对象，输入用户名
    def input_username(self, username):
        self.find_element(*self.username_loc).clear()
        self.find_element(*self.username_loc).send_keys(username)

    # 输入密码：调用send_keys对象，输入密码
    def input_password(self, password):
        self.find_element(*self.password_loc).clear()
        self.find_element(*self.password_loc).send_keys(password)

    # 点击登录：
    def click_submit(self):
        self.find_element(*self.submit_loc).click()

    # 用户名或密码不合理是Tip框内容展示
    def show_span(self):
        return self.find_element(*self.span_loc).text

    # 切换登录模式为动态密码登录（IE下有效）
    def swich_DynPw(self):
        self.find_element(*self.dynpw_loc).click()

    # 登录成功页面中的用户ID查找
    def show_userid(self):
        return self.find_element(*self.userid_loc).text