# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2016-7-29
# Description: 百度首页对象层，定义元素与封装对象
#***************************************************************


from selenium.webdriver.common.by import By
from Public.PageObject.BasePage import BasePage
from selenium.webdriver.common.action_chains import *
import xlrd
varExcel = "/Users/linghuchong/Downloads/51/Project/XXX_AutoTest/baidu/TestData/Baidu1_0.xls"
bk = xlrd.open_workbook(varExcel, formatting_info=True)
sheetParam = bk.sheet_by_name("param")

# 继承BasePage类,操作登录页面元素
class HomePO(BasePage):

    # 对象定位器，通过元素属性定位元素对象

    # 通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    def open(self):   self._open(self.base_url, self.pagetitle)
    def checkTitle(self):   self._title(self.base_url, self.pagetitle)

    # 新闻管理文案
    newsmanagement_loc= (By.XPATH, "//div[@id='navbar-left-collapse-cetc']/ul/li[1]/a[1]")
    def check_newsmanagement_loc(self):
        assert self.find_element(*self.newsmanagement_loc).text == u'新闻管理', u"F,expected=新闻管理, actual=%s " %(self.find_element(*self.newsmanagement_loc).text)

    # 资料管理文案
    msgmanagement_loc= (By.XPATH, "//div[@id='navbar-left-collapse-cetc']/ul/li[2]/a[1]")
    def check_msgmanagement_loc(self):
        assert self.find_element(*self.msgmanagement_loc).text == u'资料管理', u"F,expected=资料管理, actual=%s " %(self.find_element(*self.msgmanagement_loc).text)

    # 直播管理文案
    tvmanagement_loc= (By.XPATH, "//div[@id='navbar-left-collapse-cetc']/ul/li[3]/a[1]")
    def check_tvmanagement_loc(self):
        assert self.find_element(*self.tvmanagement_loc).text == u'直播管理', u"F,expected=直播管理, actual=%s " %(self.find_element(*self.tvmanagement_loc).text)

    # 项目管理文案
    projectmanagement_loc= (By.XPATH, "//div[@id='navbar-left-collapse-cetc']/ul/li[4]/a[1]")
    def check_projectmanagement_loc(self):
        assert self.find_element(*self.projectmanagement_loc).text == u'项目管理', u"F,expected=项目管理, actual=%s " %(self.find_element(*self.projectmanagement_loc).text)

    # 任务管理文案
    taskmanagement_loc= (By.XPATH, "//div[@id='navbar-left-collapse-cetc']/ul/li[5]/a[1]")
    def check_taskmanagement_loc(self):
        assert self.find_element(*self.taskmanagement_loc).text == u'任务管理', u"F,expected=任务管理, actual=%s " %(self.find_element(*self.taskmanagement_loc).text)

    # 学习设计师管理文案
    learnmanagement_loc= (By.XPATH, "//div[@id='navbar-left-collapse-cetc']/ul/li[6]/a[1]")
    def check_learnmanagement_loc(self):
        assert self.find_element(*self.learnmanagement_loc).text == u'项目管理', u"F,expected=项目管理, actual=%s " %(self.find_element(*self.learnmanagement_loc).text)

    # 论坛管理文案
    forummanagement_loc= (By.XPATH, "//div[@id='navbar-left-collapse-cetc']/ul/li[1]/a[7]")
    def check_forummanagement_loc(self):
        assert self.find_element(*self.forummanagement_loc).text == u'任务管理', u"F,expected=任务管理, actual=%s " %(self.find_element(*self.forummanagement_loc).text)




    # 新闻管理 => 新闻列表
    newslist_loc= (By.XPATH, "//ul[@id='collapse-menu-user']/li/a[1]")
    def click_newslist(self):
        try:assert self.find_element(*self.newslist_loc).text == u'新闻列表', u"F,expected=新闻列表, actual=%s " %(self.find_element(*self.newslist_loc).text)
        finally:self.find_element(*self.newslist_loc).click()


    # 新闻管理 => 新闻列表 => 操作
    oper_loc= (By.XPATH, "//button[@id='action']")
    def click_oper(self):
        self.find_element(*self.oper_loc).click()


    # 新闻管理 => 新闻列表 => 操作 => 新建
    oper_create_loc= (By.XPATH, "//ul[@类与实例='dropdown-menu']/li[1]")
    def click_oper_create(self):
        self.find_element(*self.oper_create_loc).click()



    # 资料管理 => 音频资料
    musiclist_loc= (By.XPATH, "//ul[@id='collapse-menu-3']/li[1]/a[1]")
    def click_musiclist(self):
        try:assert self.find_element(*self.musiclist_loc).text == u'音频资料', u"F,expected=音频资料, actual=%s " %(self.find_element(*self.musiclist_loc).text)
        finally:self.find_element(*self.musiclist_loc).click()

    # 资料管理 => 文稿资料
    filelist_loc= (By.XPATH, "//ul[@id='collapse-menu-3']/li[2]/a[1]")
    def click_filelist(self):
        try:assert self.find_element(*self.filelist_loc).text == u'文稿资料', u"F,expected=文稿资料, actual=%s " %(self.find_element(*self.filelist_loc).text)
        finally:self.find_element(*self.filelist_loc).click()

    # 资料管理 => 视频资料
    vediolist_loc= (By.XPATH, "//ul[@id='collapse-menu-3']/li[3]/a[1]")
    def click_vediolist(self):
        try:assert self.find_element(*self.vediolist_loc).text == u'视频资料', u"F,expected=视频资料, actual=%s " %(self.find_element(*self.vediolist_loc).text)
        finally:self.find_element(*self.vediolist_loc).click()









    # menu => 新闻
    news_loc= (By.XPATH, "//div[@id='u1']/a[2]")
    def click_news(self):
        try:   assert self.find_element(*self.news_loc).text == sheetParam.cell_value(3, 2), u"F,expected=%s, actual=%s " %(sheetParam.cell_value(3, 2), self.find_element(*self.nuomi_loc).text)
        finally:   self.find_element(*self.news_loc).click()

    # menu => hao123
    hao123_loc= (By.XPATH, "//div[@id='u1']/a[3]")
    def click_hao123(self):
        try:   assert self.find_element(*self.hao123_loc).text == sheetParam.cell_value(3, 3), u"F,expected=%s, actual=%s " %(sheetParam.cell_value(3, 3), self.find_element(*self.nuomi_loc).text)
        finally:   self.find_element(*self.hao123_loc).click()

    # menu => 登录
    login_loc= (By.XPATH, "//div[@id='u1']/a[7]")
    def click_login(self):
        try:   assert self.find_element(*self.login_loc).text == sheetParam.cell_value(3, 7), u"F,expected=%s, actual=%s " %(sheetParam.cell_value(3, 7), self.find_element(*self.nuomi_loc).text)
        finally:   self.find_element(*self.login_loc).click()

    # menu => 设置（悬浮）
    setup_loc= (By.XPATH, "//div[@id='u1']/a[8]")
    def suspend_setup(self):
        try:   assert self.find_element(*self.setup_loc).text == sheetParam.cell_value(3, 8), u"F,expected=%s, actual=%s " %(sheetParam.cell_value(3, 8), self.find_element(*self.nuomi_loc).text)
        finally:
            return self.find_element(*self.setup_loc)

    # advancedSearch_locc = (By.XPATH, "//a[contains(@href,'advanced.html')]")
    advancedSearch_loc = (By.XPATH, "//div[@id='wrapper']/div[6]/a[2]")
    def click_advancedSearch(self): self.find_element(*self.advancedSearch_loc).click()


    # search => keyword
    baiduSearch_loc = (By.ID, 'kw')
    def input_baiduSearch(self,keyword):
        self.find_element(*self.baiduSearch_loc).clear()
        self.find_element(*self.baiduSearch_loc).send_keys(keyword)

    # search => 百度一下
    baiduyixia_loc = (By.ID, 'su')
    def click_baiduyixia(self):
        self.find_element(*self.baiduyixia_loc).click()

    # search => searchResult（百度为您找到相关结果。。。。）
    baiduSearchResult_loc = (By.XPATH, "//div[@id='container']/div[2]/div/div[2]")
    def show_baiduSearchResult(self):
        print self.find_element(*self.baiduSearchResult_loc).text









