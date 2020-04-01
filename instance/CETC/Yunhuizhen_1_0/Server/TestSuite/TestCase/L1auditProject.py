# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.0.0
# Date       : 2017-4-9
# Description: 一级账号审核项目
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from Login import *

class L1auditProject(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print u"C3，党建项目管理后台,一级账户审核项目"

    def test_L1auditProject(self):
        print u"C3，党建项目管理后台,一级账户审核项目"
        # varExcel = os.path.abspath(r"../TestData/DKDJ1_0.xls")  # run1跑
        # bk = xlrd.open_workbook(varExcel, formatting_info=True)
        # sheetParam = bk.sheet_by_name("param")
        # exlProjectTitle = sheetParam.cell_value(20, 0)
        # exlSubProjectTitle = sheetParam.cell_value(20, 1)
        Operation_PO = OperationPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(1, 2))
        Home_PO = HomePO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(1, 2))
        Login_PO = LoginPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))

        # 打开，党建项目管理后台,登录，一级账号
        Login_PO.open(3)
        Login_PO.input_username(sheetParam.cell_value(3, 1))
        Login_PO.input_password(sheetParam.cell_value(3, 1))
        Login_PO.click_submit(3)
        print u"#1，完成 - 账号'" + sheetParam.cell_value(3, 1) + u"'已登录。"

        # 点击，项目审核
        # print Home_PO.isElementXpath("//div[@class='index-1 disabled']", "显化被屏蔽")
        # Home_PO.assertTrue(Home_PO.isElementXpath("//div[@class='index-1 disabled']"), u'显化被屏蔽',2)
        Operation_PO.select_operations('项目审核',2)
        # 点击，发布申请
        Operation_PO.select_operations('发布申请',3)
        # print u"#2，项目审核 - 点击发布申请。"

        # 打印，指定项目所有内容
        print u"#2，完成 - 勾选指定项目"
        Home_PO.click_OperProjectAudit(Home_PO.get_editProjectTitleValue(sheetParam.cell_value(9, 1)), 2)

        # 项目审核 - 操作 - 同意发布
        Operation_PO.click_oper(2)
        Operation_PO.select_operations('同意发布',2)
        # 确定 （弹框：你确定审核通过吗？）
        Home_PO.click_popupConfirm(2)
        print u"#3，完成 - 审核通过"

        # 返回发布的项目
        Operation_PO.select_operations('发布的项目',2)
        # 打印，发布的项目清单
        print u">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        # 1, 项目信息
        varProjectStatus = Home_PO.get_listsByXpath(u'[项目]: ', sheetParam.cell_value(9, 1), 8, 4)
        Home_PO.assertEqual(varProjectStatus, u'同意发布', u'申请发布 -> ' + varProjectStatus, 2)
        # 2，子项目列表
        Home_PO.inIframeDiv("[@id='task_view_target']", 2)
        varSubprojectStatus = Home_PO.get_listsByXpath(u'[子项目]: ', sheetParam.cell_value(9, 2), 8, 6)
        Home_PO.assertEqual(varSubprojectStatus, u'待发布', varSubprojectStatus, 2)
        # 3，目标单位
        Home_PO.assertEqual(Home_PO.get_targetlistsByXpath(), u'["同意发布"]', varProjectStatus, 5)
        Home_PO.close_driver()
        # 下一脚本：OperRelease.py
