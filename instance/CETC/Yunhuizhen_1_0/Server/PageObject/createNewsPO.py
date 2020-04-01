# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2016-7-29
# Description: 百度首页对象层，定义元素与封装对象
#***************************************************************


from selenium.webdriver.common.by import By
from Public.PageObject.BasePage import BasePage
from selenium.webdriver.common.action_chains import *
import xlrd,time
from time import sleep

varExcel = "/Users/linghuchong/Downloads/51/Project/XXX_AutoTest/baidu/TestData/Baidu1_0.xls"
bk = xlrd.open_workbook(varExcel, formatting_info=True)
sheetParam = bk.sheet_by_name("param")

# 继承BasePage类,操作登录页面元素
class CreateNewsPO(BasePage):

    # 【新建新闻】

    # 通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    def open(self):
        self._open(self.base_url, self.pagetitle)



    # def current_windows(self):
    #     self._current_windows(self.now_handle)
        # all_handles = self.now_handle  #获取所有窗口句柄
        # print "1121212121212121"
        # for handle in all_handles:
        #     self.driver.switch_to_window(handle)
    #
    # def change1(self):
    #
    #     for handle in self.now_handle:
    #
    #         # if handle != self.now_handle:
    #         #     print handle    #输出待选择的窗口句柄
    #             self.driver.switch_to_window(handle)

    def checkTitle(self):   self._title(self.base_url, self.pagetitle)



    # 面包屑
    # 当前位置新闻管理新建新闻

    # 1,新闻标题*
    newsTitle_loc = (By.ID, 'news_list_title')
    def input_newsTitle(self, newsTitle):
        self.find_element(*self.newsTitle_loc).clear()
        self.find_element(*self.newsTitle_loc).send_keys(newsTitle)

    # 2,缩略图片
    file1_loc = (By.XPATH, "//form[@id='edit-form']/div[6]/div[1]/div[1]/div[2]/div/input")
    def click_thumbnail(self):
        self.find_element(*self.file1_loc).send_keys("//Users//linghuchong//testdata//err.png")

    # 3,详情图片
    file2_loc = (By.XPATH, "//form[@id='edit-form']/div[7]/div[1]/div[1]/div[2]/div/input")
    def click_thumbnail2(self):
        self.find_element(*self.file2_loc).send_keys("//Users//linghuchong//testdata//err2.png")


    # 3，置顶
    top_loc = (By.NAME, "news_list_tag")
    def click_top(self):
        self.find_element(*self.top_loc).click()



    # 4,提交
    submit_loc = (By.XPATH, "//form[@id='edit-form']/div[11]/div/button[3]")
    def click_submit(self):
        self.find_element(*self.submit_loc).click()

    # 5,提交确认
    submit2_loc = (By.XPATH, "/html/body/div[7]/div[3]/button")
    def click_submit2(self):
        self.find_element(*self.submit2_loc).click()

    # 退出系统
    logout_loc = (By.XPATH, "/html/body/div[1]/nav/div[3]/ul/li[2]/a")
    def click_logout(self):
        self.find_element(*self.logout_loc).click()


    # 新闻审核
    newsAudit_loc = (By.LINK_TEXT, "新闻审核")
    def click_newsAudit(self):
        self.find_element(*self.newsAudit_loc).click()

    # 勾选新闻内容
    def select_News(self, content):
        links = self.driver.find_elements_by_link_text(content)
        for link in links:
            tmphref = link.get_attribute("href")
            tmphrefvalue = tmphref.split("=")
            self.selectNews_loc = (By.XPATH, "//input[@value='" + tmphrefvalue[1] + "']")
            self.find_element(*self.selectNews_loc).click()


    # 审核管理 => 新闻审核 => 操作
    oper_loc = (By.XPATH, "//button[@id='action']")
    def click_oper(self):
        self.find_element(*self.oper_loc).click()


    # 审核管理 => 新闻审核 => 操作 => 审核通过
    oper_auditPass_loc= (By.LINK_TEXT, "审核通过")
    def click_oper_auditPass(self):
        self.find_element(*self.oper_auditPass_loc).click()

    # 新闻列表 => 标题检索
    search_loc = (By.ID, 'news_list_title')
    def input_search(self, keyword):
        self.find_element(*self.search_loc).clear()
        self.find_element(*self.search_loc).send_keys(keyword)


    # 新闻列表 => 查找
    find_loc = (By.XPATH, "//form[@id='search-form']/div[1]/div[3]/button")
    def click_find(self):
        self.find_element(*self.find_loc).click()

    # 新闻列表 => 审核人
    auditUser_loc = (By.XPATH, "//form[@id='list-form']/div[1]/table[1]/tbody/tr")
    def check_auditUser(self,username):
        ss=self.find_element(*self.auditUser_loc).text
        p=ss.split(" ")
        if p[5] == username:
            print u'[OK],新闻标题"' + p[0] + u'"的审核人是' + p[5]
            return 0
        else:
            print u'[Fault],新闻标题"' + p[0] + u'"的审核人是' + p[5]
            return 1

    # 新闻列表 => 停用
    oper_stop_loc= (By.LINK_TEXT, "停用")
    def click_oper_stop(self):
        self.find_element(*self.oper_stop_loc).click()

    # 新闻列表 => 启用
    oper_start_loc= (By.LINK_TEXT, "启用")
    def click_oper_start(self):
        self.find_element(*self.oper_start_loc).click()


    def changeWin(self):
        self.current_windows


    def client_news(self):
        from appium import webdriver
        import commands
        androidVersion = commands.getoutput('adb shell getprop ro.build.version.release')
        androidSerialno = commands.getoutput('adb shell getprop ro.serialno')
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = str(float(androidVersion[0:3]))
        desired_caps['deviceName'] = androidSerialno
        desired_caps['appPackage'] = 'com.cetc.partybuilding'
        desired_caps['appActivity'] = 'com.cetc.partybuilding.activity.InitActivity'
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.screenX = self.driver.get_window_size()['width']
        self.screenY = self.driver.get_window_size()['height']
        # reload(sys)
        # sys.setdefaultencoding('utf8')
        print "[客户端]"
        print "首页 - CETC头条 - 更多"
        sleep(7)
        # self.driver.find_element_by_id("android:id/button1").click()
        # sleep(3)
        self.driver.find_element_by_id("com.cetc.partybuilding:id/news_more_btn").click()
        sleep(5)
        # self.driver.find_element_by_id("android:id/tabs").find_element_by_xpath("//android.widget.FrameLayout[contains(@index,1)]").find_element_by_id("com.cetc.partybuilding:id/btn_text").click()
        # sleep(5)
        # print "点击事实要闻"
        # self.driver.swipe(self.screenX/2, self.screenY/2, self.screenX/2, self.screenY/2+200, 1000)
        # sleep(3)
        # print self.driver.find_element_by_id("com.cetc.partybuilding:id/listview").find_element_by_xpath("//android.widget.LinearLayout[contains(@index,1)]").find_element_by_id("com.cetc.partybuilding:id/title_tv").text

    def client_news2(self):
        # from appium import webdriver
        # import commands
        # androidVersion = commands.getoutput('adb shell getprop ro.build.version.release')
        # androidSerialno = commands.getoutput('adb shell getprop ro.serialno')
        # desired_caps = {}
        # desired_caps['platformName'] = 'Android'
        # desired_caps['platformVersion'] = str(float(androidVersion[0:3]))
        # desired_caps['deviceName'] = androidSerialno
        # desired_caps['appPackage'] = 'com.cetc.partybuilding'
        # desired_caps['appActivity'] = 'com.cetc.partybuilding.activity.InitActivity'
        # desired_caps['unicodeKeyboard'] = 'True'
        # desired_caps['resetKeyboard'] = 'True'
        # self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        # self.screenX = self.driver.get_window_size()['width']
        # self.screenY = self.driver.get_window_size()['height']
        # reload(sys)
        # sys.setdefaultencoding('utf8')
        print "[客户端2]"
        print "返回首页"
        sleep(7)
        # self.driver.find_element_by_id("android:id/button1").click()
        # sleep(3)
        self.driver.find_element_by_id("com.cetc.partybuilding:id/title_ll_back").click()
        sleep(5)

#
# driver.find_element_by_xpath('//input[@value="cv1"]').click()  # click
# driver.find_element_by_xpath('//input[@value="cv2"]').send_keys(Keys.SPACE)  # send space


    # file_loc= (By.NAME, 'file')
    # def click_thumbnail2(self):
    #     self.find_element(*self.file_loc).send_keys("//Users//linghuchong//testdata//err2.png")

    # username_loc = (By.ID, '_username')
    # def input_username(self, username):
    #     self.find_element(*self.username_loc).clear()
    #     self.find_element(*self.username_loc).send_keys(username)
    #
    #   #
      # 首先找到元素：WebElement  file = driver.findElement(By.name("filename"));
      # 给此元素设置值：file.sendKeys("/Users/linghuchong/testdata/err.png")


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
    newslist_loc= (By.XPATH, "//ul[@id='collapse-menu-2']/li/a[1]")
    def click_newslist(self):
        try:assert self.find_element(*self.newslist_loc).text == u'新闻列表', u"F,expected=新闻列表, actual=%s " %(self.find_element(*self.newslist_loc).text)
        finally:self.find_element(*self.newslist_loc).click()


    # 新闻管理 => 新闻列表 => 操作
    oper_loc= (By.XPATH, "//button[@id='action']")
    def click_oper(self):
        self.find_element(*self.oper_loc).click()


    # 新闻管理 => 新闻列表 => 操作 => 新建
    oper_create_loc= (By.XPATH, "//ul[@class='dropdown-menu']/li[1]")
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


    def switchwin(self,xx):
        # driver = self.driver
        print xx
        print "66666"
        print type(xx)
        # driver.get("https://www.hao123.com/")
        # now_handle = driver.current_window_handle #获取当前窗口句柄
        # driver.find_element_by_id("search-input").send_keys("selenium")
        # driver.find_element_by_xpath("//*[@id='search-form']/div[2]/input").click()
        # sleep(5)
        self.current_windows(xx)
        # self.switch_to_window(xx)
        # self.switch_to.window(self,xx)








