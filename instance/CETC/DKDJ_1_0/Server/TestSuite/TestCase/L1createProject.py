# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.0.0
# Date       : 2017-4-9
# Description: 一级账号创建项目
# Function   :
# geckodriver 0.14.0 for selenium3.0 （ https://github.com/mozilla/geckodriver/releases ）
# geckodriver是一原生态的第三方浏览器，对于selenium3.x版本都会使用geckodriver来驱动firefox
# 将文件geckodriver 放在 /Users/linghuchong/Downloads/51/ForWin/selenium/selenium3/ 下。
# 不支持firefox53以上版本，及geckodriver 0.15
# HTMLTestRunner （ http://tungwaiyip.info/software/HTMLTestRunner.html ）
# HTMLTestRunner.py /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import sys, unittest, os, xlwt, xlrd, datetime,MySQLdb
from xlutils.copy import copy
reload(sys)
sys.setdefaultencoding("utf-8")
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from time import sleep
from Project.CETC.DKDJ_1_0.Server.PageObject.LoginPO import LoginPO
from Server.PageObject.HomePO import HomePO
from Server.PageObject.OperationPO import OperationPO
# from DKDJ_Param import *

conn = MySQLdb.connect(host='10.111.3.5', user='cetc', passwd='20121221', db='dangjian', port=3306, use_unicode=True)
cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')

# driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/Users/linghuchong/Downloads/51/ForWin/Selenium/selenium3/geckodriver', firefox_options=None, log_path='geckodriver5.log')
driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/usr/local/bin/geckodriver', firefox_options=None, log_path='geckodriver5.log')
driver.implicitly_wait(10)
varExcel = os.path.abspath(r"../TestData/web20.xls")  # run1, 批量跑
# varExcel = os.path.abspath(r"../../TestData/DKDJ1_0.xls")  # 单独运行
bk = xlrd.open_workbook(varExcel, formatting_info=True)
newbk = copy(bk)
sheetParam = bk.sheet_by_name("param")
styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')


class L1createProject(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print u"C1，党建项目管理后台,一级账户创建项目、子项目、资源"

    def test_L1createProject(self):
        print u"C1，党建项目管理后台,一级账户创建项目、子项目、资源"
        Login_PO = LoginPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))
        Home_PO = HomePO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))
        Operation_PO = OperationPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))

        # 1，打开，党建项目管理后台, 一级账号登录
        Login_PO.open(3)
        Login_PO.input_username(sheetParam.cell_value(3, 1))
        Login_PO.input_password(sheetParam.cell_value(3, 1))
        Login_PO.click_submit(3)
        print u"#1，完成 - 账号'" + sheetParam.cell_value(3, 1) + u"'已登录。"


        # 2，进入发布项目，创建主项目
        # Home_PO.assertTrue(Home_PO.isElementXpath("//div[@class='index-1 disabled']"), u'显化被屏蔽')
        # Home_PO.assertTrue(Home_PO.isElementXpath("//div[@class='index-3 disabled']"), u'审核被屏蔽')

        Operation_PO.select_operations(u'发布的项目',2)
        # 发布项目 - 操作 - 新建
        Operation_PO.click_oper(2)
        Operation_PO.select_operations(u'新建', 3)
        # print u"Step4，新建项目。"

        # 发布项目 - 项目信息 - 项目标题
        varProjectTitle = Home_PO.input_rlsProjectTitle(u'城市' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        # 保存项目名到excel中，用于之后调用。
        newWs = newbk.get_sheet(1)
        newWs.write(9, 1, varProjectTitle, styleRed)
        newbk.save(varExcel)
        # 发布项目 - 项目信息 - 项目简介
        Home_PO.input_rlsProjectIntro(u'项目介绍' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        # 发布项目 - 项目信息 - 学习方式 （# 可选：随时学、直播、点播、群组讨论、测试、线上自学、线下集体学习、线下自学）
        Home_PO.select_byName('task_learn_style', u'群组讨论')
        # 发布项目 - 项目信息 - 类别 （# 可选：时政新闻、学习近平讲话、十八届六中全会精神、学党规党章、中国电科新闻报道）
        Home_PO.select_byName1('task_sub_type', u'学党规党章')
        # 发布项目 - 项目信息 - 责任人
        Home_PO.input_rlsPerson(sheetParam.cell_value(3, 3))
        # 发布项目 - 项目信息 - 项目结束时间
        varTimeYMD = datetime.datetime.now().strftime('%Y-%m-%d')  # 获取当天日期
        Home_PO.input_rlsEndTime(varTimeYMD, 1)
        # 发布项目 - 项目信息 - 项目开始时间
        Home_PO.input_rlsStartTime(u"2017-04-14", 1)
        # 发布项目 - 下发单位（全选／反选）
        Home_PO.check_rlsTargetCompanysIsAll(u'中国电子科技集团公司第十四研究所党委')  # 可选：全选、中电科软件信息服务有限公司党委，中国电子科技集团公司党群工作部，中国电子科技集团公司第十四研究所党委，奇聚联创

        # 发布项目 - 下一步
        Home_PO.click_rlsNextStep(2)
        # 发布项目 - 确认（弹框：你确定新建项目吗？）
        Home_PO.click_popupConfirm(2)
        print u"#2，完成 - 新建项目。"


        #【scene 1，直接操作子项目】
        # 3-1、操作 - 删除子项目（当无子项目时，弹框提示：你确定删除子项目吗？请选择请求操作的行。）
        Operation_PO.click_oper(2)
        Operation_PO.select_operations(u'删除子项目',2)
        Home_PO.click_popupConfirm(3)
        Home_PO.click_popupConfirm(3)
        print u"#3-1，检查无子项目时点击删除子项目的提示信息。"

        # 3-2、操作 - 添加子项目后删除
        Operation_PO.click_oper(2)
        Operation_PO.select_operations(u'添加子项目',2)
        # 进入第一层iframe >>>>>>>>>>>>>>>>>>>>>>>>>>>
        Home_PO.inIframeDiv("[@class='cetc-popup-content']/div", 2)
        # 添加子项目 - 子项目信息 - 子项目标题
        newWs = newbk.get_sheet(1)
        newWs.write(9, 2, Home_PO.input_rlsSubProjectTitle(u'规划' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')), styleRed)
        newbk.save(varExcel)
        # 添加子项目 - 子项目信息 - 子项目介绍
        Home_PO.input_rlsSubProjectIntro(u'子项目介绍' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        # 添加子项目 - 子项目信息 - 选择图片
        Home_PO.click_thumbnail(u"//Users//linghuchong//Downloads//51//Picture//4729.jpg", 3)
        # 添加子项目 - 子项目信息 - 提交
        Home_PO.click_rlsSubProjectSubmit(3)
        # 添加子项目 - 确认（弹框：你确定新建项目吗？）
        Home_PO.click_popupConfirm(3)
        Home_PO.outIframe(2)
        Home_PO.click_popupConfirm(3)
        #子项目列表勾选所有编号，进行删除子项目操作。
        Home_PO.check_byPathInputClass("cetc-page-lists-check-all", 2)
        Operation_PO.click_oper(2)
        Operation_PO.select_operations(u'删除子项目',2)
        Home_PO.click_popupConfirm(3)
        # 子项目添加完成"
        # Home_PO.get_msg() # 没有数据信息
        Home_PO.assertEqual(Home_PO.get_msg(), u"没有数据信息.",u'删除子项目',2)
        # print u"#3-2，完成 - 检查删除子项目。"

        # 操作 - 添加子项目
        Operation_PO.click_oper(2)
        Operation_PO.select_operations(u'添加子项目',2)
        # 进入第一层iframe >>>>>>>>>>>>>>>>>>>>>>>>>>>
        Home_PO.inIframeDiv("[@class='cetc-popup-content']/div", 2)
        # 添加子项目 - 子项目信息 - 子项目标题
        newWs = newbk.get_sheet(1)
        newWs.write(9, 2, Home_PO.input_rlsSubProjectTitle(u'规划' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')), styleRed)
        newbk.save(varExcel)
        # 添加子项目 - 子项目信息 - 子项目介绍
        Home_PO.input_rlsSubProjectIntro(u'子项目介绍' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        # 添加子项目 - 子项目信息 - 选择图片
        Home_PO.click_thumbnail(u"//Users//linghuchong//Downloads//51//Picture//4729.jpg", 3)
        # 添加子项目 - 子项目信息 - 提交
        Home_PO.click_rlsSubProjectSubmit(3)
        # 添加子项目 - 确认（弹框：你确定新建项目吗？）
        Home_PO.click_popupConfirm(3)
        print u"#3-2，完成 - 添加子项目。"

        # 4，添加资源列表 - 操作 - 添加
        Operation_PO.click_oper(1)
        Home_PO.move_screenLeft(u'1000', 2)  # 屏幕中，向左移动1000个像素
        Operation_PO.select_operations(u'添加', 2)
        # 发布项目 - 添加子项目 - 添加项目资源 - 勾选资源checkbox
        # 进入第二层iframe >>>>>>>>>>>>>>>>>>>>>>>>>>>
        Home_PO.inIframeDiv("[@class='cetc-popup-content']/div", 2)
        Home_PO.check_rlsAddProjectResource('2,4')  # 勾选1个
        # Home_PO.check_rlsAddProjectResource('3,5,6')  # 勾选3个
        Home_PO.outIframe(2)   # 退出所有的iframe <<<<<<<<<<<<<<<<<<<<<<<<<<<
        # 进入第一层iframe >>>>>>>>>>>>>>>>>>>>>>>>>>>
        Home_PO.inIframeDiv("[@class='cetc-popup-content']/div", 2)
        # 发布项目 - 添加子项目 - 添加项目资源 - 确认
        Home_PO.click_popupConfirm(4)
        # 发布项目 - 添加子项目 - 确认（你确定要添加新的资源吗？）
        Home_PO.click_popupConfirmResource(2)
        Home_PO.outIframe(2)  # 退出所有的iframe <<<<<<<<<<<<<<<<<<<<<<<<<<<
        print u"#4，完成 - 添加资源。"

        # 发布项目 - 添加子项目 - 确认
        Home_PO.click_popupConfirm(2)
        print u"#5，完成 - 项目、子项目、资源的新增。"


        # 打印，子项目内容
        varNums = Home_PO.get_subProjectlistsByXpath(u'[子项目]: ',1)
        newWs = newbk.get_sheet(1)
        newWs.write(9, 3, varNums, styleRed)
        cur.execute('select count(*) from tt_subject_detail where subject_id="%s"' %(varNums))
        newWs.write(9, 4, cur.fetchone()[0], styleRed)
        newbk.save(varExcel)

        # 发送给平台项目运营团队
        # 发布项目 - 子项目列表 - 发送给平台项目运营团队
        Home_PO.click_confirmBtn3(3)
        Home_PO.click_popupConfirm(3)
        print u"#6，已发送给平台项目运营团队。"


        # 打印，发布的项目清单
        print u">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        # 1, 项目信息
        varProjectStatus = Home_PO.get_listsByXpath(u'[项目]: ', varProjectTitle, 8, 4)
        Home_PO.assertEqual(varProjectStatus, u'待发布', varProjectStatus, 2)
        # 2，子项目列表
        Home_PO.inIframeDiv("[@id='task_view_target']", 2)
        varSubprojectStatus = Home_PO.get_listsByXpath(u'[子项目]: ',u"#" + varNums, 8, 7)
        Home_PO.assertEqual(varSubprojectStatus, u'待发布', varSubprojectStatus, 2)
        # 3，目标单位
        Home_PO.assertEqual(Home_PO.get_targetlistsByXpath(), u'["待发布"]', varProjectStatus, 5)


        # scene 2，直接保存
        # # 发布项目 - 子项目列表 - 保存
        # Home_PO.click_confirmBtn2(3)
        # # 发布项目 - 子项目列表 - 确定（你确定要保存项目信息吗？） ，保存后进入项目信息编辑页面，可再编辑主项目及添加或删除子项目，保存或发送给运营。
        # Home_PO.click_popupConfirm(3)
        # print u"\Step12，保存（进入项目信息编辑页面，可再编辑主项目及添加或删除子项目，保存或发送给运营。"
        # # 发布项目 - 项目信息 - 发送给平台项目运营团队（弹框：你确定发送给平台项目运营团队吗？发送后不可以在做编辑。）
        # Home_PO.click_popupConfirm(3)
        # print u"\Step13，已发送给平台项目运营团队。（页面返回到发布的项目详情页）"
        # 退出并切换运营账号
        # Login_PO.click_logout(3)
        # print u"Step14，" + sheetParam.cell_value(3, 1) + u"'已登出。"

        # scene 3，发送给平台项目运营团队??


        # # 登出
        # Login_PO.click_logout(3)
        # print u"Step14，'" + sheetParam.cell_value(3, 1) + u"'已登出。"

        Home_PO.close_driver()
        # 下个脚本 OperAuditProject.py


