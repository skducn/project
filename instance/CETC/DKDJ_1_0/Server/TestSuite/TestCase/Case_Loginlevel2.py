# coding: utf-8
#****************************************************************
# Author     : John
# Version    : 1.0.0
# Date       : 2017-1-20
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
from Server.PageObject.LoginPO import LoginPO
from Server.PageObject.HomePO import HomePO
from Server.PageObject.createNewsPO import CreateNewsPO



driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/Users/linghuchong/Downloads/51/ForWin/selenium/selenium3/geckodriver', firefox_options=None, log_path='geckodriver5.log')
driver.implicitly_wait(10)

# varExcel = os.path.abspath(r"../TestData/DKDJ1_0.xls")  # run1跑

varExcel = os.path.abspath(r"../../TestData/web20.xls")  # 单独跑

bk = xlrd.open_workbook(varExcel, formatting_info=True)
sheetParam = bk.sheet_by_name("param")
varNewsTitle = u"金浩666"



class Case_Loginlevel2(unittest.TestCase):

    # @classmethod
    # def setUpClass(self):
    #     print u"C1，中电科党建管理后台登录 level2"
        # varNewsTitle = u"金浩666"

    def test1_login(self):

        # CreateNews_PO = CreateNewsPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(1, 2))
        # CreateNews_PO.switchwin()
        # sleep(1212)

        print u"C1，中电科党建管理后台登录。"
        Login_PO = LoginPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))

        # 打开后台登录
        xx = Login_PO.open()
        print xx
        print "4444444"
        print type(xx)
        print u"\nS1-1，打开中电科党建管理后台网页。"
        sleep(2)

        # level2登录
        Login_PO.input_username(sheetParam.cell_value(3, 2))
        Login_PO.input_password(sheetParam.cell_value(4, 2))
        Login_PO.click_submit()
        print u"S1-2，" + sheetParam.cell_value(3, 2) + "登录成功。"

        # # 检查文案
        Home_PO = HomePO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(1, 2))
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




    def test2_baiduSearch(self):

         print "12121212121212"
         # # 搜索关键字QTP
         # Home_PO = HomePO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))
         # Home_PO.input_baiduSearch("QTP")
         # Home_PO.click_baiduyixia()
         # sleep(5)
         # print u"\nS2-1，搜索关键字QTP，并在新窗口中显示结果如下："
         # Home_PO.show_baiduSearchResult()
         # driver.back()
         # sleep(5)



         # driver.close()
         # driver.quit()

# if __name__ == '__main__':
#
#     # unittest.main()  //不生产报告。
#
#     testunit = unittest.TestSuite()
#     testunit.addTest(Home111("test_baidu_Search"))
#     # testunit.addTest(Home111("test_baidu_set"))
#
#     now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
#     print now
#     filename = '//Users//linghuchong//Downloads//51//Project//XXX_AutoTest//baidu//TestReport//Baidu_' + now + '.html'
#     fp =open(filename, 'wb')
#     runner = HTMLTestRunner.HTMLTestRunner(
#         stream=fp,
#         title='Baidu首页',
#         description='This demonstrates the report测试报告')
#     runner.run(testunit)
#     fp.close()
#     print "home111111"
#     #driver.close()
#     # driver.quit()


