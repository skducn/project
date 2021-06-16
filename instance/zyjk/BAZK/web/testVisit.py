# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2020-8-14
# Description: SAAS 之 随访管理
# *****************************************************************

from instance.zyjk.SAAS.PageObject.SaasPO import *
Saas_PO = SaasPO()
from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()

# 登录
Saas_PO.login("016", "123456")

# # 1，元素库
Saas_PO.clickMenuAll("随访", "元素库")

def validateRule(varRule):
    Saas_PO.Web_PO.clickId("tab-validationRules0", 2)  # 1验证规则
    list1 = Saas_PO.Web_PO.getXpathsText("//span")
    list1 = List_PO.listIntercept(list1, "保存并新增", 1)
    list1 = List_PO.listDel(list1, "")
    # print(list1)
    for i in range(len(varRule)):
        for j in range(len(list1)):
            if list1[j] == varRule[i]:
                Saas_PO.Web_PO.clickXpath('//div[@id="pane-validationRules0"]/div/div[1]/div[1]/div[1]/div[' + str(j+1) + ']/div[1]/div/label', 2)
                Saas_PO.Web_PO.clickXpath('//div[@id="pane-validationRules0"]/div/div[1]/div[1]/div[1]/div[' + str(j+1) + ']/div[1]/div', 2)
                break

validateRule(["数字范围","正则校验"])


# Saas_PO.Web_PO.clickId("tab-attribute", 2)  # 组件属性
# Saas_PO.Web_PO.inputXpathClear("//input[@placeholder='最大宽度24格']", 12)
# Saas_PO.Web_PO.clickXpath('//*[@id="pane-attribute"]/form/div[1]/div/div[6]/div[2]/div/div/span')


