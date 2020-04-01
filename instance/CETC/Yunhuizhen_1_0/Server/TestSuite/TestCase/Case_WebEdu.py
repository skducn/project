# coding: utf-8
#****************************************************************
# Author     : John
# Version    : 1.0.0
# Date       : 2017-4-9
# Description:
# Function   :
# geckodriver 0.14.0 for selenium3.0 （ https://github.com/mozilla/geckodriver/releases ）
# geckodriver是一原生态的第三方浏览器，对于selenium3.x版本都会使用geckodriver来驱动firefox
# 将文件geckodriver 放在 /Users/linghuchong/Downloads/51/ForWin/selenium/selenium3/ 下。

# HTMLTestRunner （ http://tungwaiyip.info/software/HTMLTestRunner.html ）
# HTMLTestRunner.py /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7
#****************************************************************

import sys, unittest,xlrd,os
from time import sleep
reload(sys)
sys.setdefaultencoding("utf-8")
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from Server.PageObject.LoginPO import LoginPO
from Server.PageObject.HomePO import HomePO
from Server.PageObject.OperationPO import OperationPO



driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/Users/linghuchong/Downloads/51/ForWin/selenium/selenium3/geckodriver', firefox_options=None, log_path='geckodriver5.log')
driver.implicitly_wait(10)

# varExcel = os.path.abspath(r"../TestData/DKDJ1_0.xls")  # run1跑
varExcel = os.path.abspath(r"../../TestData/web20.xls")  # 单独跑

bk = xlrd.open_workbook(varExcel, formatting_info=True)
sheetParam = bk.sheet_by_name("param")
varNewsTitle = u"金浩666"

class Case_Project(unittest.TestCase):

    # @classmethod
    # def setUpClass(self):
    #     print u"C1，中电科党建管理后台登录 level2"
        # varNewsTitle = u"金浩666"

    def test1_Level1CreateProject(self):

        print u"C1，党建项目管理后台,一级账户创建项目、子项目、资源"

        # 打开党建项目管理后台
        Login_PO = LoginPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))
        Login_PO.open(3)
        print u"\nS1-1，打开党建项目管理后台。"

        # 一级账号登录
        Login_PO.input_username(sheetParam.cell_value(3, 1))
        Login_PO.input_password(sheetParam.cell_value(3, 1))
        Login_PO.click_submit(3)
        print u"\nS1-2，'" + sheetParam.cell_value(3, 1) + u"'已登录。"

        # 发布项目
        Home_PO = HomePO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(1, 2))
        Home_PO.click_releaseProject(3)
        print u"\nS1-3，进入发布的项目。"

        # 发布项目 - 操作 - 新建
        Operation_PO = OperationPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(1, 2))
        Operation_PO.click_oper(2)
        Operation_PO.select_create(2)
        print u"\nS1-4，开始新建项目。"

        # 发布项目 - 项目信息 - 项目标题
        Home_PO.input_rlsProjectTitle()
        # 发布项目 - 项目信息 - 项目简介
        Home_PO.input_rlsProjectIntro()
        # 发布项目 - 项目信息 - 学习方式
        Home_PO.select_rlsLearnWay(u'直播')
        # 发布项目 - 项目信息 - 类别
        Home_PO.select_rlsType('1')
        # 发布项目 - 项目信息 - 责任人
        Home_PO.input_rlsPerson('john')
        # 发布项目 - 下发单位（全选／反选）  （参数可选：中电科软件信息服务有限公司党委，中国电子科技集团公司党群工作部，中国电子科技集团公司第十四研究所党委，奇聚联创，全选）
        Home_PO.check_rlsTargetCompanysIsAll(u'中国电子科技集团公司第十四研究所党委')
        # 发布项目 - 下一步
        Home_PO.click_rlsNextStep(2)
        # 发布项目 - 确认（弹框：你确定新建项目吗？）
        Home_PO.click_rlsConfirm(2)
        print u"\nS1-5，新建项目完成。"

        # choose 1，立即添加子项目
        # 发布项目 - 操作 - 添加子项目
        Operation_PO.click_oper(2)
        Operation_PO.select_addSubProject(2)
        print u"\nS1-6，开始添加子项目。"

        Home_PO.inIframe(4)         # 进入第一层iframe >>>>>>>>>>>>>>>>>>>>>>>>>>>
        # 添加子项目 - 子项目信息 - 子项目标题
        Home_PO.input_rlsSubProjectTitle()
        # 添加子项目 - 子项目信息 - 子项目介绍
        Home_PO.input_rlsSubProjectIntro()
        # 添加子项目 - 子项目信息 - 选择图片
        Home_PO.click_thumbnail(2)
        # 添加子项目 - 子项目信息 - 提交
        Home_PO.click_rlsSubProjectSubmit(2)
        # 添加子项目 - 确认（弹框：你确定新建项目吗？）
        Home_PO.click_rlsConfirm(3)
        print u"\nS1-7，子项目添加完成。"


        # 发布项目 - 添加子项目 - 资源列表 - 操作 - 添加
        Operation_PO.click_oper(2)
        Home_PO.move_screenLeft('1000', 2)  # 在 iframe 中左移动屏幕1000
        Operation_PO.select_operAddResource(2)
        print u"\nS1-8，开始添加项目资源。"

        # 发布项目 - 添加子项目 - 添加项目资源 - 勾选资源checkbox
        Home_PO.inIframe(2)        # 进入第二层iframe >>>>>>>>>>>>>>>>>>>>>>>>>>>
        Home_PO.check_rlsAddProjectResource(2)  # 表示勾选第二个
        Home_PO.outIframe(2)
        Home_PO.inIframe(2)    # 进入第一层iframe >>>>>>>>>>>>>>>>>>>>>>>>>>>
        # 发布项目 - 添加子项目 - 添加项目资源 - 确认
        Home_PO.click_rlsConfirm(4)
        # 发布项目 - 添加子项目 - 确认（你确定要添加新的资源吗？）
        Home_PO.click_rlsPopConfirm(2)
        Home_PO.outIframe(2)  # 退出所有的iframe <<<<<<<<<<<<<<<<<<<<<<
        print u"\nS1-9，项目资源添加完成。"


        # 发布项目 - 添加子项目 - 确认
        Home_PO.click_rlsConfirm(2)
        print u"\nS1-10，完成项目、子项目、资源的新增。"


        # 打印子项目内容，断言？？
        Home_PO.print_rlsSubProjectList(3)
        print u"\nS1-11，打印子项目列表页。"

        # # choose 2，保存
        # # 发布项目 - 子项目列表 - 保存
        # Home_PO.click_rlsSave(3)
        # # 发布项目 - 子项目列表 - 确定（你确定要保存项目信息吗？） ，保存后进入项目信息编辑页面，可再编辑主项目及添加或删除子项目，保存或发送给运营。
        # Home_PO.click_rlsConfirm(3)
        # print u"\nS1-12，保存（进入项目信息编辑页面，可再编辑主项目及添加或删除子项目，保存或发送给运营。"
        # # 发布项目 - 项目信息 - 发送给平台项目运营团队（弹框：你确定发送给平台项目运营团队吗？发送后不可以在做编辑。）
        # Home_PO.click_rlsConfirm(3)
        # print u"\nS1-13，已发送给平台项目运营团队。（页面返回到发布的项目详情页）"


        # choose 3，发送给平台项目运营团队
        # 发布项目 - 子项目列表 - 发送给平台项目运营团队
        Home_PO.click_rlsSendOperation(3)
        Home_PO.click_rlsConfirm(3)
        print u"\nS1-12，已发送给平台项目运营团队。（页面返回到发布的项目详情页）"

        # 退出并切换运营账号
        Login_PO.click_logout(3)
        print u"\nS1-13，" + sheetParam.cell_value(3, 1) + u"'已登出。"













        # Home_PO.check_newsmanagement_loc()  # 新闻管理
        # Home_PO.check_msgmanagement_loc()  # 资料管理
        # Home_PO.check_tvmanagement_loc()  # 直播管理
        # Home_PO.check_projectmanagement_loc()  # 项目管理
        #
        # 点击新闻列表
        Home_PO.click_newslist()
        print u"S1-3，点击新闻列表"
        sleep(2)
        Home_PO.click_oper()
        sleep(2)
        Home_PO.click_oper_create()
        sleep(2)
        #
        # # 新建新闻
        CreateNews_PO = CreateNewsPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(1, 2))
        CreateNews_PO.input_newsTitle(varNewsTitle)
        CreateNews_PO.click_thumbnail()
        # CreateNews_PO.click_thumbnail2()



# ——————————————————————————————————————————————————
        # client操作 test???
        # 客户端上验证是否显示
        CreateNews_PO.client_news()


        CreateNews_PO.current_windows(xx)
        sleep(3)
        CreateNews_PO.click_thumbnail2()

        # # 关闭后台
        # driver.close()
        # Login_PO = LoginPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))
        # # 打开后台登录
        # Login_PO.open()
        # Login_PO.input_username(sheetParam.cell_value(3, 2))
        # Login_PO.input_password(sheetParam.cell_value(4, 2))
        # Login_PO.click_submit()
        # sleep(2)

        # 继续操作client
        CreateNews_PO.client_news2()
        sleep(2)
        print "end"
        sleep(1212)




        CreateNews_PO.click_top()
        sleep(3)
        CreateNews_PO.click_submit()
        sleep(3)
        CreateNews_PO.click_submit2()

        # 退出系统，切换角色
        CreateNews_PO.click_logout()


        # level1登录，进行审核
        Login_PO.input_username(sheetParam.cell_value(3, 1))
        Login_PO.input_password(sheetParam.cell_value(4, 1))
        Login_PO.click_submit()
        print u"S1-2，" + sheetParam.cell_value(3, 1) + "登录成功。"

        CreateNews_PO.click_newsAudit()
        sleep(2)

        # 选择新闻
        CreateNews_PO.select_News(self.varNewsTitle)
        # # CreateNews_PO.select_News(u"新闻标题")  #  可选择多个，且重复的新闻

        # 操作 - 审核通过
        CreateNews_PO.click_oper()
        sleep(2)
        CreateNews_PO.click_oper_auditPass()
        #
        # # # 退出系统，切换角色
        # CreateNews_PO.click_logout()

        # # level2登录，进行验证
        # Login_PO.input_username(sheetParam.cell_value(3, 2))
        # Login_PO.input_password(sheetParam.cell_value(4, 2))
        # Login_PO.click_submit()
        # print u"S1-2，" + sheetParam.cell_value(3, 2) + "登录成功。"
        # Home_PO.click_newslist()
        # CreateNews_PO.input_search(u"asdfasdf")
        # sleep(2)
        # CreateNews_PO.click_find()
        #
        # sleep(2)
        # # 检查审核人是level1
        # if CreateNews_PO.check_auditUser(u'level1') == 1:
        #     print u"客户端上验证新闻应该可见"
        #
        # # 勾选新闻
        # CreateNews_PO.select_News(u"asdfasdf")
        # # 操作 - 停用
        # CreateNews_PO.click_oper()
        # sleep(2)
        # CreateNews_PO.click_oper_stop()
        # # 检查审核人是 已停用
        # if CreateNews_PO.check_auditUser(u'已停用') == 1:
        #     print u"验证客户端上新闻应不可见。"


        # # 操作 - 启用
        # CreateNews_PO.click_oper()
        # sleep(2)
        # CreateNews_PO.click_oper_start()
        # # 检查审核人是 启用 ， 目前启动后显示待审核。
        # if CreateNews_PO.check_auditUser(u'level1') == 1:
        #     print u"客户端任然不可见，处于待审核"
        #
        # sleep(10)

        driver.close()
        driver.quit()


        # client操作
        # 客户端上验证是否显示
        CreateNews_PO.client_news()
        Login_PO = LoginPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))

        # 打开后台登录
        Login_PO.open()
        print u"\nS1-1，打开中电科党建管理后台网页。"
        sleep(2)

        # level2登录
        Login_PO.input_username(sheetParam.cell_value(3, 2))
        Login_PO.input_password(sheetParam.cell_value(4, 2))
        Login_PO.click_submit()
        print u"S1-2，" + sheetParam.cell_value(3, 2) + "登录成功。"




        # 点击音频资料
        Home_PO.click_musiclist()
        print u"S1-4，点击音频资料"
        sleep(2)
        # 点击文稿资料
        Home_PO.click_filelist()
        print u"S1-5，点击文稿资料"
        sleep(2)
        # 点击视频资料
        Home_PO.click_vediolist()
        print u"S1-6，点击视频资料"
        sleep(2)






        # # # 设置
        # ActionChains(driver).move_to_element(Home_PO.suspend_setup()).perform()
        # sleep(3)
        # Home_PO.click_advancedSearch()
        # sleep(3)
        # # Home_PO.click_advancedSearch()
        # sleep(3)

    def test2_LevelOperationAudit(self):

        print u"C2，党建项目管理后台,运营账户审核"

        # 二级账号登录
        Login_PO = LoginPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))
        Login_PO.input_username(sheetParam.cell_value(4, 1))
        Login_PO.input_password(sheetParam.cell_value(4, 1))
        Login_PO.click_submit(3)
        print u"S1-1，'" + sheetParam.cell_value(4, 1) + u"'已登录。"




         # driver.close()
         # driver.quit()



