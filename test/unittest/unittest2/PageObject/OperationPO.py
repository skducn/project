# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2017-4-9
# Description: 党建项目管理后台，操作项
#***************************************************************


from selenium.webdriver.common.by import By
from Public.PageObject.BasePage import BasePage
from selenium.webdriver.common.action_chains import *
import xlrd,time
from time import sleep

class OperationPO(BasePage):

    # 【新建新闻】

    # 通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    def open(self):
        self._open(self.base_url, self.pagetitle)

    def checkTitle(self):
        self._title(self.base_url, self.pagetitle)


    # 操作
    def click_oper(self, t):
        self.find_element(*(By.XPATH, "//button[@id='action']")).click()
        sleep(t)

    # 操作 - (新建，添加子项目，删除子项目，添加（资源），删除（资源），审核通过，审核拒绝，同意发布，拒绝发布、收到的项目、项目审核)
    def select_operations(self, object, t):
        self.find_element(*(By.LINK_TEXT, object)).click()
        sleep(t)



    # 收到的项目
    receiveProject_loc = (By.LINK_TEXT, "收到的项目")
    def click_receiveProject(self,sleeptime):
        self.find_element(*self.receiveProject_loc).click()
        sleep(sleeptime)
    # 项目审核
    auditProject_loc = (By.LINK_TEXT, "项目审核")
    def click_auditProject(self,sleeptime):
        self.find_element(*self.auditProject_loc).click()
        sleep(sleeptime)