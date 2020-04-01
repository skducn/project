# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.0.0
# Date       : 2017-4-9
# Description: 运营团队发布
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from L1createProject import *


class OperRelease(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print u"C4，党建项目管理后台,运营发布"

    def test_OperRelease(self):
        print u"C4，党建项目管理后台,运营发布"
        # varExcel = os.path.abspath(r"../TestData/DKDJ1_0.xls")  # run1跑
        # bk = xlrd.open_workbook(varExcel, formatting_info=True)
        # sheetParam = bk.sheet_by_name("param")
        # exlProjectTitle = sheetParam.cell_value(20, 0)
        # exlSubProjectTitle = sheetParam.cell_value(20, 1)
        Home_PO = HomePO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))
        Login_PO = LoginPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))

        # 打开，党建项目管理后台,登录，运营账号
        Login_PO.open(3)
        Login_PO.input_username(sheetParam.cell_value(4, 1))
        Login_PO.input_password(sheetParam.cell_value(4, 1))
        Login_PO.click_submit(3)
        print u"#1，完成 - 账号'" + sheetParam.cell_value(4, 1) + u"'已登录。"

        # 打印，指定项目所有内容
        varOperRlsBefore = Home_PO.get_listsByXpath(u'[项目]: ', sheetParam.cell_value(9, 1), 8, 4)


        # 选择指定项目标题，并进行发布
        Home_PO.click_editProjectTitle(Home_PO.get_editProjectTitleValue(sheetParam.cell_value(9, 1)),2)        # get_editProjectTitleValue(varProjectTitle)  获取编辑项目的值，如313
        sleep(4)
        # 发布
        Home_PO.click_confirmBtn2(2)
        # 确定（弹框：你确定发布项目吗？项目发布后不允许再做修改。）
        Home_PO.click_popupConfirm(5)
        print u"#2，完成 - 发布"


        # 打印，检查指定项目内容中的项目表单状态
        # 打印，发布的项目清单
        # print u"Step4，打印申请发布后项目内容（状态变更），如下："
        # varOperRlsAfter = Home_PO.get_OperProjectListStatus(sheetParam.cell_value(9, 1))
        # Home_PO.assertEqual(varOperRlsAfter, '已发布', varOperRlsBefore + u' -> ' + varOperRlsAfter, 2)

        # # 打印，子项目列表# 打印，子项目列表
        # Home_PO.inIframeDiv("[@id='task_view_target']", 2)
        # varOperRlsAfter = Home_PO.get_listsByXpath(sheetParam.cell_value(9, 3), 8, 7)
        # Home_PO.assertEqual(varOperRlsAfter, u'已发布', varOperRlsAfter, 2)
        # # 打印，目标单位
        # Home_PO.assertEqual(Home_PO.get_targetlistsByXpath(), u'["已发布"]', varOperRlsAfter, 5)


        # 打印，发布的项目清单
        print u">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        # 1, 项目信息
        varProjectStatus = Home_PO.get_listsByXpath(u'[项目]: ', sheetParam.cell_value(9, 1), 8, 4)
        Home_PO.assertEqual(varProjectStatus, u'已发布', varOperRlsBefore + u' -> ' + varProjectStatus, 2)
        # 2，子项目列表
        Home_PO.inIframeDiv("[@id='task_view_target']", 2)
        varSubprojectStatus = Home_PO.get_listsByXpath(u'[子项目]: ', sheetParam.cell_value(9, 2), 8, 6)
        Home_PO.assertEqual(varSubprojectStatus, u'已发布', varSubprojectStatus, 2)
        # 3，目标单位
        Home_PO.assertEqual(Home_PO.get_targetlistsByXpath(), u'["已发布", "已接收"]', u'["已发布", "已接收"]', 5)
        Home_PO.close_driver()
        # 下一脚本：L2transmit.py




