# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.0.0
# Date       : 2017-4-9
# Description: 运营团队审核项目
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from L1createProject import *

class OperAuditProject(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print u"C2，党建项目管理后台,运营申请发布"

    def test_OperAuditProject(self):
        print u"C2，党建项目管理后台,运营申请发布"
        Login_PO = LoginPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))
        Home_PO = HomePO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))

        # 打开，党建项目管理后台，登录，运营账号
        Login_PO.open(3)
        Login_PO.input_username(sheetParam.cell_value(4, 1))
        Login_PO.input_password(sheetParam.cell_value(4, 1))
        Login_PO.click_submit(3)
        print u"#1，完成 - 账号'" + sheetParam.cell_value(4, 1) + u"'已登录。"

        # 打印，主项目内容并返回状态
        varStatus = Home_PO.get_listsByXpath(u'[项目]:',sheetParam.cell_value(9, 1), 8, 4)

        # 进入项目的编辑页面，并进行申请发布
        Home_PO.click_editProjectTitle(Home_PO.get_editProjectTitleValue(sheetParam.cell_value(9, 1)), 6)        # get_editProjectTitleValue(varProjectTitle)  获取编辑项目的值，如313
        # 申请发布
        Home_PO.click_confirmBtn2(2)
        # 确定（弹框：你确定申请发布项目吗？）
        Home_PO.click_popupConfirm(5)
        print u"#2，完成 - 申请发布。"


        # 打印，发布的项目清单
        print u">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        # 1, 项目信息
        varStatus1 = Home_PO.get_listsByXpath(u'[项目]: ', sheetParam.cell_value(9, 1), 8, 4)
        Home_PO.assertEqual(varStatus1, u'申请发布', varStatus + u' -> ' + varStatus1, 2)
        # 2，子项目列表
        Home_PO.inIframeDiv("[@id='task_view_target']", 2)
        varOperRlsAfter = Home_PO.get_listsByXpath(u'[子项目]: ', sheetParam.cell_value(9, 2), 8, 6)
        Home_PO.assertEqual(varOperRlsAfter, u'待发布', varOperRlsAfter, 2)
        # 3，目标单位
        Home_PO.assertEqual(Home_PO.get_targetlistsByXpath(), u'["申请发布"]', varStatus1, 5)
        Home_PO.close_driver()
        # 下个脚本：L1auditProject.py




