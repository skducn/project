# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.0.0
# Date       : 2017-4-9
# Description: 二级单位转发
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from L1createProject import *

class L2transmit(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print u"C5，党建项目管理后台,二级单位转发"

    def test_L2transmit(self):
        print u"C5，党建项目管理后台,二级单位转发"
        # # varExcel = os.path.abspath(r"../TestData/DKDJ1_0.xls")  # run1跑
        # bk = xlrd.open_workbook(varExcel, formatting_info=True)
        # sheetParam = bk.sheet_by_name("param")
        # exlProjectTitle = sheetParam.cell_value(20, 0)
        # exlSubProjectTitle = sheetParam.cell_value(20, 1)
        Home_PO = HomePO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))
        Operation_PO = OperationPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(1, 2))
        Login_PO = LoginPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))

        # 打开，党建项目管理后台 ，登录，二级账号
        Login_PO.open(3)
        Login_PO.input_username(sheetParam.cell_value(5, 1))
        Login_PO.input_password(sheetParam.cell_value(5, 1))
        Login_PO.click_submit(3)
        print u"#1，完成 - 账号'" + sheetParam.cell_value(5, 1) + u"'已登录。"

        # 点击，收到的项目
        Operation_PO.select_operations(u'收到的项目',6)

        # 点击指定项目内容编辑icon，收到的项目
        Home_PO.click_L2editProjectTitle(Home_PO.get_editProjectTitleValue(sheetParam.cell_value(9, 1)), 2)
        # print u"Step4，点击，指定项目内容编辑icon。"

        # 发布的项目 - 项目信息 - 责任人
        Home_PO.input_rlsPerson(u'yoyo')
        # 发布项目 - 下发单位（全选／反选）
        Home_PO.check_rlsTargetCompanysIsAll(u'中电科哈轨直属党支部')
        # print u"Step5，输入责任人、下发单位。"

        Home_PO.move_screenTop(u'1000', 2)  # 屏幕上，向上移动1000个像素

        # 点击，下一步
        Home_PO.click_L2Next(3)
        # 点击，确定（你确定转发项目吗？）
        Home_PO.click_popupConfirm(4)
        # print u"Step6，点击下一步。"


        # 发布的项目 - 子项目列表 ， 打印，指定项目所有内容
        # print u"Step7，打印当前项目内容，如下："
        varNums = Home_PO.get_subProjectlistsByXpath(u'[子项目]: ', 1)

        # 点击，发布
        Home_PO.click_confirmBtn3(2)
        Home_PO.click_popupConfirm(5)  # 确定，提示：你确定发布项目吗？项目发布后不允许再做修改。
        print u"#2，完成 - 发布"




        # # test，
        # Operation_PO.select_operations('发布的项目', 2)

        # 发布的项目的详情页
        # 打印，项目列表
        # print u"Step9，打印发布的项目下项目内容："
        # Home_PO.get_projectListRtnStatus(sheetParam.cell_value(9, 1))

        # 进入第一层iframe >>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Home_PO.inIframeDiv("[@id='task_view_target']", 2)

        # # 打印，子项目列表
        # print u"Step10，打印发布的项目下的子项目内容："
        # # Home_PO.print_rlsSubProjectList(3)
        # # Home_PO.get_listsByXpath(varNums, 8, 7)
        #
        # # 打印，目标单位   断言？
        # print u"Step11，打印发布的项目下的目标单位内容："
        # Home_PO.assertEqual(Home_PO.get_targetlistsByXpath(), u'["已发布", "已发布", "已接收"]', u"项目情况状态全部正确", 5)


        # 打印，发布的项目清单
        print u">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        # 1, 项目信息
        varProjectStatus = Home_PO.get_listsByXpath(u'[项目]: ', sheetParam.cell_value(9, 1), 8, 4)
        # Home_PO.assertEqual(varProjectStatus, u'已发布', varProjectStatus + u' -> ' + varProjectStatus, 2)
        # 2，子项目列表
        Home_PO.inIframeDiv("[@id='task_view_target']", 2)
        varSubprojectStatus = Home_PO.get_listsByXpath(u'[子项目]: ', sheetParam.cell_value(9, 2), 8, 6)
        Home_PO.assertEqual(varSubprojectStatus, u'已发布', varSubprojectStatus, 2)
        # 3，目标单位
        Home_PO.assertEqual(Home_PO.get_targetlistsByXpath(), u'["已发布", "已发布", "已接收"]', u'["已发布", "已发布", "已接收"]', 5)
        Home_PO.close_driver()
        # 下一脚本：L3transmit





