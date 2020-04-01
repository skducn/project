# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2016-7-29
# Description: 作业管理-作业框架管理
#***************************************************************

from selenium.webdriver.common.by import By
from Public.PageObject.BasePage import BasePage
import json

# 继承BasePage类,操作登录页面元素
class TaskManagePO(BasePage):


    # # 通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    # def open(self):   self._open(self.base_url, self.pagetitle)
    # def checkTitle(self):   self._title(self.base_url, self.pagetitle)


    def clickONline(self, selectNum):
        # 作业管理，遍历任务信息表格，勾选radio，点击上线
        varcount =0
        list1 =[]
        list0 = []
        # 获取tr的数量
        for a in self.find_elements(*(By.XPATH, "//table[@class='table table-striped table-bordered table-hover dataTables-example']/tbody/tr")):
            varcount = varcount + 1
            # print a.get_attribute("onclick")
            xx = a.get_attribute("onclick")
            # print xx.split("'")[1]  # _306832140866158592
            list0.append(xx.split("'")[1])
        # print varcount
        print list0

        print self.find_element(*(By.ID,list0[selectNum-1])).get_attribute('value')
        print self.find_element(*(By.ID,list0[selectNum-1])).get_attribute('value3')
        var1 = "jobOnline('" + self.find_element(*(By.ID,list0[selectNum-1])).get_attribute('value') +"','"+ self.find_element(*(By.ID,list0[selectNum])).get_attribute('value3') +"');"
        print var1

        # 获取 遍历td值，存入列表
        for a in self.find_elements(*(By.XPATH, "//table[@class='table table-striped table-bordered table-hover dataTables-example']/tbody/tr")):
            for b in self.find_elements(*(By.XPATH, "//table[@class='table table-striped table-bordered table-hover dataTables-example']/tbody/tr" + "/td")):
                list1.append(b.text)
            break
        listtmp = []
        listtmp = json.dumps(list1, encoding="UTF-8", ensure_ascii=False)  # 字典 转 unicode
        print listtmp


        # 点击 上线
        for c in self.find_elements(*(By.XPATH, "//button[@class='btn label-primary']")):
            if c.get_attribute("onclick") == var1:
                c.click()


        # # varName与选择框id关联，输入varName返回id号
        # tmp = 0
        # for i in range(len(list1)):
        #     if list1[i] == varName:
        #         # print i
        #         x = i % 5
        #         for j in range(varcount):
        #             if x == j+1:
        #                 return list0[j]
        #         break
        #
        # print "Errorrrr, get_selectRadio." + varName + ",不存在！"
        # return None






