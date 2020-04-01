# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2016-7-29
# Description: 百度首页登录对象层，定义元素与封装对象
#***************************************************************

from selenium.webdriver.common.by import By
from Public.PageObject.BasePage import BasePage
from time import sleep
import json

# 继承BasePage类,操作登录页面元素
class LoginPO(BasePage):

    # ByID
    def inputID(self, varId, varContent):
        self.find_element(*(By.ID, varId)).clear()
        self.find_element(*(By.ID, varId)).send_keys(varContent)

    # ByNAME
    def inputNAME(self, varName, varContent):
        self.find_element(*(By.NAME, varName)).clear()
        self.find_element(*(By.NAME, varName)).send_keys(varContent)

    # ByLinktext
    def clickLINKTEXT(self, varContent, t):
        self.find_element(*(By.LINK_TEXT, varContent)).click()
        sleep(t)

    # ByTAG_NAME
    def clickTAGNAME(self, varContent, t):
        self.find_element(*(By.TAG_NAME, varContent)).click()
        sleep(t)

    # ByXpath
    def clickXPATH(self, varPath,t):
        self.find_element(*(By.XPATH, varPath)).click()
        sleep(t)

    def printXPATH(self, varPath):
        print self.find_element(*(By.XPATH, varPath)).text



    # 遍历一级二级菜单
    def selectMenu(self, varPath, varMenu, varPath2, varMenu2):
        for a in self.find_elements(*(By.XPATH, varPath)):
            if varMenu == a.text:
                a.click()
                sleep(1)
                for a2 in self.find_elements(*(By.XPATH, varPath2)):
                    if varMenu2 == a2.text:
                        a2.click()
                        break
                break

    def get_selectRadio(self, varPath, varName):
        varcount =0
        list1 =[]
        list0 = []
        # 获取tr的数量
        for a in self.find_elements(*(By.XPATH, varPath)):
            varcount = varcount + 1
            # print a.get_attribute("onclick")
            xx = a.get_attribute("onclick")
            # print xx.split("'")[1]  # _306832140866158592
            list0.append(xx.split("'")[1])
        # print varcount

        # 获取 遍历td值，存入列表
        for a in self.find_elements(*(By.XPATH, varPath)):
            for b in self.find_elements(*(By.XPATH, varPath + "/td")):
                list1.append(b.text)
            break
        # listtmp = []
        # listtmp = json.dumps(list1, encoding="UTF-8", ensure_ascii=False)  # 字典 转 unicode
        # print listtmp

        # varName与选择框id关联，输入varName返回id号
        tmp = 0
        for i in range(len(list1)):
            if list1[i] == varName:
                # print i
                x = i % 5
                for j in range(varcount):
                    if x == j+1:
                        return list0[j]
                break

        print "Errorrrr, get_selectRadio." + varName + ",不存在！"
        return None


