# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: PIM白茅岭对象库 - 门诊配发药
# *****************************************************************


from instance.zyjk.PIM.PageObject.PimPO import *


class ClinicAllotPO(object):

    def __init__(self):
        self.Level_PO = Level_PO

    def modelMenu(self, varMeneName):

        ''' 模块菜单'''

        l_modelMenu = Level_PO.getXpathsText("//div[@类与实例='clearfix btn_header']/ul/li")
        print(l_modelMenu)
        for i in range(len(l_modelMenu)):
            if varMeneName in l_modelMenu[i]:
                Level_PO.clickXpath("//div[@类与实例='clearfix btn_header']/ul/li[" + str(i + 1) + "]", 2)

