# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.0.0
# Date       : 2017-4-9
# Description: 二级单位发布
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from L1createProject import *

class L2release(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print u"C7，党建项目管理后台,二级单位发布"

    def test_L2release(self):
        print u"C7，党建项目管理后台,二级单位发布"
        # varExcel = os.path.abspath(r"../TestData/DKDJ1_0.xls")  # run1跑
        # bk = xlrd.open_workbook(varExcel, formatting_info=True)
        # sheetParam = bk.sheet_by_name("param")
        # exlProjectTitle = sheetParam.cell_value(20, 0)
        # exlSubProjectTitle = sheetParam.cell_value(20, 1)
        Home_PO = HomePO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))
        Operation_PO = OperationPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(1, 2))
        Login_PO = LoginPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))

        # 打开，党建项目管理后台,# 登录，二级账号14suo
        Login_PO.open(3)
        Login_PO.input_username(sheetParam.cell_value(5, 1))
        Login_PO.input_password(sheetParam.cell_value(5, 1))
        Login_PO.click_submit(3)
        print u"#1，完成 - 账号'" + sheetParam.cell_value(4, 1) + u"'已登录。"

        Operation_PO.select_operations(u'项目审核', 2)
        Operation_PO.select_operations(u'发布申请', 2)

        # 打印，指定项目所有内容
        print u"Step3，勾选指定项目"
        Home_PO.click_OperProjectAudit(Home_PO.get_editProjectTitleValue(sheetParam.cell_value(9, 1)), 2)

        # 项目审核 - 操作 - 同意发布
        Operation_PO.click_oper(2)
        Operation_PO.select_operations(u'同意发布',2)
        print u"Step4，审核通过"
        # 确定 （弹框：你确定审核通过吗？）
        Home_PO.click_popupConfirm(2)
        # 断言 没有信息

        Operation_PO.select_operations(u'发布的项目',2)



        #
        # # 打印，检查指定项目内容中的项目表单状态
        # print u"Step5，打印发布申请后项目内容（状态变更为已发布），如下："
        # varOperRlsAfter = Home_PO.get_OperProjectListStatus(sheetParam.cell_value(9, 1))
        # Home_PO.assertEqual(varOperRlsAfter, u'已发布', u'待发布 -> ' + varOperRlsAfter, 2)
        #
        # # 发布的项目的详情页
        # # 打印，项目列表
        # print u"Step6，打印发布的项目下项目内容："
        # Home_PO.get_projectListRtnStatus(sheetParam.cell_value(9, 1))
        #
        # # 进入第一层iframe >>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Home_PO.inIframeDiv("[@id='task_view_target']", 2)
        # # Home_PO.inIframeDiv(4)
        #
        # # 打印，子项目列表
        # print u"Step7，打印发布的项目下的子项目内容："
        # # Home_PO.print_rlsSubProjectList(3)
        # Home_PO.get_rlsSubProjectRtnStatus(sheetParam.cell_value(9, 2))
        #
        # # 打印，目标单位   断言？
        # print u"Step8，打印发布的项目下的目标单位内容："
        # Home_PO.assertEqual(Home_PO.get_targetlistsByXpath(), u'["已发布", "已发布", "已发布"]', u"项目情况状态", 2)


        # 打印，发布的项目清单
        print u">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        # 1, 项目信息
        varProjectStatus = Home_PO.get_listsByXpath(u'[项目]: ', sheetParam.cell_value(9, 1), 8, 4)
        Home_PO.assertEqual(varProjectStatus, u'已发布', varProjectStatus + u' -> ' + varProjectStatus, 2)
        # 2，子项目列表
        Home_PO.inIframeDiv("[@id='task_view_target']", 2)
        varSubprojectStatus = Home_PO.get_listsByXpath(u'[子项目]: ', sheetParam.cell_value(9, 2), 8, 6)
        Home_PO.assertEqual(varSubprojectStatus, u'已发布', varSubprojectStatus, 2)
        # 3，目标单位
        Home_PO.assertEqual(Home_PO.get_targetlistsByXpath(), u'["已发布", "已发布", "已发布"]', u'["已发布", "已发布", "已发布"]', 5)
        Home_PO.close_driver()
        # 完成







