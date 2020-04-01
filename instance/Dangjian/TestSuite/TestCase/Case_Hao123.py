# coding: utf-8
#****************************************************************
# Author     : John
# Version    : 1.0.0
# Date       : 2017-1-20
# Description:
#****************************************************************

from Case_Loginlevel2 import *
from Server.PageObject.Hao123PO import Hao123PO

class Case_Hao123(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print u"C2，检查hao123页面搜索功能"

    def test1_searchKeyword(self):
        print u"C2，检查hao123页面搜索功能"
        # 百度首页点击hao123
        Home_PO = HomePO(driver, u"news.hao123.com", u"hao123")
        Home_PO.click_hao123()
        sleep(3)
        Home_PO.checkTitle()
        handle1 = driver.current_window_handle
        print u"\nS2-1，打开hao123页面。"


        # hao123页面，搜索关键字qtp123
        Hao123_PO = Hao123PO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))
        Hao123_PO.input_hao123Search(u"qtp123")
        Hao123_PO.click_hao123Baiduyixia()
        sleep(5)
        print u"S2-2，搜索关键字qtp123，并在新窗口中显示搜索结果如下："


        # # 切换到第2个浏览器
        handles = driver.window_handles
        for handleX in handles:
            if handleX != handle1:
                driver.switch_to_window(handleX)
                sleep(5)
                Home_PO.show_baiduSearchResult()
                break


        # 切换回第一个浏览器
        handles = driver.window_handles
        for handleX in handles:
            if handleX == handle1:
                driver.switch_to_window(handleX)
                sleep(2)
        print u"S2-3，切换回第一个浏览器。"


        # 切换到hao123页面，再搜索另一个关键字 selenium
        Hao123_PO.input_hao123Search(u"selenium")
        Hao123_PO.click_hao123Baiduyixia()
        print u"S2-4，搜索关键字selenium，并在新窗口中显示搜索结果（省略）。"


        # 关闭第三个浏览器，并切换回第二个浏览器
        handles = driver.window_handles
        for handleX in handles:
            if handleX != handle1:
                driver.switch_to_window(handles[1])   # 第三方个浏览器
                sleep(2)
                driver.close()
                driver.switch_to_window(handles[2])   # 第二个浏览器
                break
        print u"S2-5，关闭第三个浏览器，并切换回第二个浏览器。"

    # def test2_no(self):
    #
    #
    #     handles = driver.window_handles
    #     sleep(3)
    #
    #     xx = driver.find_element_by_xpath("//div[@id='u']/a[2]")
    #     # yy = driver.find_element_by_xpath("//div[@id='wrapper']/div[4]/a[1]")
    #
    #     ActionChains(driver).move_to_element(xx).perform()
    #
    #     sleep(5)
    #     # login_page.click_hao123SearchAdvance()
    #     sleep(3)
    #
    #     # login_page.click_hao123back()
    #     sleep(3)
    #     driver.close()
    #     driver.switch_to_window(handles[0])
    #     sleep(3)
    #
    #     # login_page.check_hao123SearchResult()
    #
    #     # sleep(4)
    #     print u"\n点击了hao123页面中登录的X"

    @classmethod
    def tearDownClass(self):
        pass
        driver.close()
        driver.quit()

