# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2017-4-9
# Description: 项目对象层，定义元素与封装对象
#***************************************************************

from selenium.webdriver.common.by import By
from Public.PageObject.BasePage import BasePage
from selenium.webdriver.support.ui import Select

from time import sleep
import datetime,json


# 继承BasePage类,操作登录页面元素
class HomePO(BasePage):

    # 对象定位器，通过元素属性定位元素对象

    # 通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    def open(self):
        self._open(self.base_url, self.pagetitle)
    def check_title(self):
        self._check_title(self.base_url, self.pagetitle)



    # 发布的项目 - 子项目列表中全选框
    def check_byPathInputClass(self, name, t):
        self.find_element(*(By.XPATH, "//input[@class='" + name + "']")).click()
        sleep(t)


    # 发布的项目 - 子项目列表中文案"没有数据信息"

    def get_msg(self):
        return self.find_element(*(By.XPATH, "//tbody[@class='cetc-page-lists-body-container']/tr/td")).text
        # sleep(t)






    # 项目发布 - 下发单位遍历
    def check_rlsTargetCompanysIsAll(self, choose):
        l_name = []
        l_value = []
        xxx = 0
        varNames = self.find_elements(*(By.XPATH, "//label[@class='checkbox']"))
        # varNames = self.driver.find_elements_by_xpath("//label[@class='checkbox']")
        for a in varNames:
            l_name.append(a.text)
            # print a.text
        l_name.pop(0)
        varValues = self.find_elements(*(By.XPATH, "//input[@name='task_company_info[][company_id]']"))

        # varValues = self.driver.find_elements_by_xpath("//input[@name='task_company_info[][company_id]']")
        for a1 in varValues:
            l_value.append(a1.get_attribute('value'))
            # print a1.get_attribute('value')
        # print json.dumps(l_value, encoding="UTF-8", ensure_ascii=False)
        # print json.dumps(l_name, encoding="UTF-8", ensure_ascii=False)
        d_total = dict(zip(l_name, l_value))
        # d_total = json.dumps(d_total, encoding="UTF-8", ensure_ascii=False)  # 字典 转 unicode
        # print d_total
        # print type(d_total)
        for i in range(len(d_total)):
            if sorted(d_total.items())[i][0] == choose:  # u'中电科软件信息服务有限公司党委':
                 xxx = sorted(d_total.items())[i][1]
        # 选择所有
        if choose == u'全选':
             self.find_element(*(By.XPATH, "//input[@onclick='doSelectCompanyAll(this)']")).click()
             # self.driver.find_element_by_xpath("//input[@onclick='doSelectCompanyAll(this)']").click()
        else:
            checkboxs = self.find_elements(*(By.XPATH, "//input[@type='checkbox']"))
            # checkboxs = self.driver.find_elements_by_xpath("//input[@type='checkbox']")
            for a3 in checkboxs:
                if a3.get_attribute('value') == xxx:
                    a3.click()
                    break


    # 项目发布 - 勾选子项目资源(单个或多个)
    def check_rlsAddProjectResource(self, strNums):
        # 例子：check_rlsAddProjectResource123('3,5,6') ,勾选第3、5、6个
        # 例子：check_rlsAddProjectResource123('2') ,勾选第2
        r = 1
        strNums.split(',')
        list1 = []
        for i in range(len(strNums.split(','))):
            list1.append(strNums.split(',')[i])
            # print int(list1[i])
            varValues = self.find_elements(*(By.XPATH, "//input[@name='learn_source_id[]']"))
            for a1 in varValues:
                if r == int(list1[i]):
                    a1.click()
                    r = 1
                    break
                else:
                    r = r + 1




    # 打印，项目发布 - 主项目列表，并返回状态
    def get_listsByXpath(self, value1 , varProjectTitle, printNums, returnNum):
        # get_listsByXpath(varProjectTitle, 8, 4)  # 8=打印列表内容数量，4=返回第四个值（这里是状态）
        list1 = []
        list2 = []
        status1 = 0
        varStatus = 0
        varProjectLists = self.find_elements(*(By.XPATH, "//tbody[@class='cetc-page-lists-body-container']/tr/td"))
        for a in varProjectLists:
            list1.append(a.text)
        for a1 in range(len(list1)):
            if list1[a1] == varProjectTitle:
                for a2 in range(printNums):
                    list2.append(list1[a2])
                print value1 + json.dumps(list2, encoding="UTF-8", ensure_ascii=False)
                varStatus = list1[a1 + returnNum - 1]
                status1 = status1 + 1
            else:
                status1 = 0
        if status1 != 1:
            status1 = 0
            return varStatus
        else:
            return "errorrrrrrrrr,没有找到对应的表单状态"


    # # 运营(qiju) - 返回项目列表中项目表单状态（遍历）
    # def get_OperProjectListStatus(self, varProjectTitle):
    #     list1 = []
    #     status1 = 0
    #     varStatus = 0
    #     varrlsSubProjectList = self.find_elements(*(By.XPATH, "//tbody[@class='cetc-page-lists-body-container']/tr/td"))
    #
    #     # varrlsSubProjectList = self.driver.find_elements_by_xpath("//tbody[@class='cetc-page-lists-body-container']/tr/td")
    #     for a1 in varrlsSubProjectList:
    #         list1.append(a1.text)
    #     for a1 in range(len(list1)):
    #         if list1[a1] == varProjectTitle:
    #             varListall = list1[a1] + ", " + list1[a1+1] + ", " + list1[a1+2] + ", " + list1[a1+3] + ", " + list1[a1+4] + ", " + list1[a1+5] + ", " + list1[a1+6] + ", " + list1[a1+7]
    #             print json.dumps(varListall, encoding="UTF-8", ensure_ascii=False)
    #             varStatus = list1[a1+3]
    #             status1 = status1 + 1
    #         else:
    #             status1 = 0
    #     if status1 != 1:
    #         return varStatus
    #     else:
    #         return self.varStatusFault + "没有找到对应的表单状态"

    # # 打印，发布的项目 - 子项目列表(二级账号)，并返回状态
    # def get_rlsSubProjectRtnStatus(self, subtitle):
    #     list1 = []
    #     status1 = 0
    #     varStatus = 0
    #     vars = self.find_elements(*(By.XPATH, "//tbody[@class='cetc-page-lists-body-container']/tr/td"))
    #
    #     # vars = self.driver.find_elements_by_xpath("//tbody[@class='cetc-page-lists-body-container']/tr/td")
    #     for a in vars:
    #         list1.append(a.text)
    #     for a1 in range(len(list1)):
    #         if list1[a1] == subtitle:
    #             varListall = u"子项目 = " + list1[a1-1] + ", " + list1[a1] + ", " + list1[a1+1] + ", " + list1[a1+2] + ", " + list1[a1+3] + ", " + list1[a1+4] + ", " + list1[a1+5] + ", " + list1[a1+6]
    #             print json.dumps(varListall, encoding="UTF-8", ensure_ascii=False)
    #             varStatus = list1[a1+3]
    #             status1 = status1 + 1
    #         else:
    #             status1 = 0
    #     if status1 != 1:
    #         return varStatus
    #     else:
    #         return self.varStatusFault + "没有找到对应的表单状态"


    # 打印，项目的发布 - 子项目列表，返回编号(去掉#)
    def get_subProjectlistsByXpath(self, value1, returnNum):
        list_varrlsSubProjectList=[]
        varrlsSubProjectList = self.find_elements(*(By.XPATH, "//tbody[@class='cetc-page-lists-body-container']/tr/td"))
        for a1 in varrlsSubProjectList:
            list_varrlsSubProjectList.append(a1.text)
        # list_varrlsSubProjectList.pop(0)
        x = list_varrlsSubProjectList[returnNum]
        x = x.split("#")[1]
        print value1 + json.dumps(list_varrlsSubProjectList, encoding="UTF-8", ensure_ascii=False)
        return x








    # 打印，发布的项目 - 目标单位（二级账号）, 并返回所有状态
    def get_targetlistsByXpath(self):
        list2 = []
        list3 = []
        list4 = []
        x = 0
        vars = self.find_elements(*(By.XPATH, "//table[@class='table table-bordered table-hover']/tbody/tr/td"))
        for a1 in vars:list2.append(a1.text)
        for a1 in vars:
            x = x + 1
            if u"- " in a1.text:
                break
        for a2 in range(x-1, len(list2)):
            list3.append(list2[a2])
        for a3 in range(1, len(list3), 2):
            list4.append(list3[a3])
        print u'[目标单位]: ' + json.dumps(list3, encoding="UTF-8", ensure_ascii=False)
        print json.dumps(list4, encoding="UTF-8", ensure_ascii=False)
        return json.dumps(list4, encoding="UTF-8", ensure_ascii=False)





    # 二级用户(14suo) - 项目标题内容
    def click_L2editProjectTitle(self, editProjectTitleValue, t):
        self.find_element(*(By.XPATH, "//a[@href='/dangjian/event/web/app_test.php/task/forward?task_id=" + editProjectTitleValue + "']")).click()
        # self.driver.find_element_by_xpath("//a[@href='/dangjian/event/web/app_test.php/task/forward?task_id=" + editProjectTitleValue + "']").click()
        sleep(t)


    # 运营(qiju) - 获取项目标题内容的编辑值
    def get_editProjectTitleValue(self, projectname):
            varOnlick = self.driver.find_element_by_link_text(projectname).get_attribute("onclick")
            return varOnlick.split('\'')[1]

    # 运营(qiju) - 项目标题内容
    def click_editProjectTitle(self,editProjectTitleValue, t):
        self.find_element(*(By.XPATH, "//a[@href='/dangjian/event/web/app_test.php/task/form?task_id=" + editProjectTitleValue + "']")).click()
        sleep(t)





    def click_OperProjectAudit(self,ab,t):
        self.find_element(*(By.XPATH, "//input[@value='" + ab + "']")).click()

        # self.driver.find_element_by_xpath("//input[@value='" + ab + "']").click()
        sleep(t)




    #
    #
    # # 申请发布（齐聚）
    # applyRelease_loc = (By.LINK_TEXT, "申请发布")
    # def click_applyRelease(self,sleeptime):
    #     self.find_element(*self.applyRelease_loc).click()
    #     sleep(sleeptime)


    # 下一步
    def click_L2Next(self, t):
        self.find_element(*(By.XPATH, "//div[@class='col-md-offset-5 col-md-5']/button")).click()
        sleep(t)




    # 发布的项目 - 项目标题
    def input_rlsProjectTitle(self, varProjectTitle):
        self.find_element(*(By.XPATH, "//input[@id='task_title']")).clear()
        self.find_element(*(By.XPATH, "//input[@id='task_title']")).send_keys(varProjectTitle)
        return varProjectTitle

   # 发布的项目 - 项目简介
    def input_rlsProjectIntro(self, varProjectINtro):
        self.find_element(*(By.XPATH, "//textarea[@id='task_resume']")).clear()
        self.find_element(*(By.XPATH, "//textarea[@id='task_resume']")).send_keys(varProjectINtro)


    # 发布的项目  - 责任人
    rlsPerson_loc = (By.NAME, "task_duty_man")
    def input_rlsPerson(self, oprname):
        self.find_element(*self.rlsPerson_loc).clear()
        self.find_element(*self.rlsPerson_loc).send_keys(oprname)


    # 发布的项目  - 项目开始时间
    rlsStartTime_loc = (By.ID, "task_begin_date")
    def input_rlsStartTime(self, starttime,sleeptime):
        self.find_element(*self.rlsStartTime_loc).clear()
        self.find_element(*self.rlsStartTime_loc).send_keys(starttime)
        sleep(sleeptime)

    # 发布的项目  - 项目结束时间
    rlsEndTime_loc = (By.ID, "task_end_date")
    def input_rlsEndTime(self, endtime,sleeptime):
        self.find_element(*self.rlsEndTime_loc).clear()
        self.find_element(*self.rlsEndTime_loc).send_keys(endtime)
        sleep(sleeptime)


   # 发布的项目 - 子项目标题
    def input_rlsSubProjectTitle(self, varSubProjectTitle):
        self.find_element(*(By.XPATH, "//input[@id='subject_title']")).clear()
        self.find_element(*(By.XPATH, "//input[@id='subject_title']")).send_keys(varSubProjectTitle)
        return varSubProjectTitle

    # 发布的项目 - 子项目介绍
    def input_rlsSubProjectIntro(self, varSubProjectIntro):
        self.find_element(*(By.XPATH, "//textarea[@id='subject_resume']")).clear()
        self.find_element(*(By.XPATH, "//textarea[@id='subject_resume']")).send_keys(varSubProjectIntro)

    # 发布的项目 - 添加子项目 - 选择图片
    def click_thumbnail(self, picpath, t):
        self.find_element(*(By.XPATH, "//div[@id='web-uploader-image-subject_image_url-picker']/div[2]/input")).send_keys(picpath)
        sleep(t)




    # # 二级单位 发布的项目 - 下一步
    # rlsNextStep_loc = (By.XPATH, "//div[@class='col-md-offset-5 col-md-5']/button")
    # def click_rlsNextStep(self,sleeptime):
    #     self.find_element(*self.rlsNextStep_loc).click()
    #     sleep(sleeptime)



    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # <<按钮>>


    # 弹框确定 （如：添加资源 - 确定 ，发布的项目 - 确定）
    def click_popupConfirm(self, t):
        self.find_element(*(By.XPATH, "//div[@class='cetc-popup-footer']/button")).click()
        sleep(t)

    # 页面底部button1，(如：返回）
    def click_confirmBtn1(self, t):
        self.find_element(*(By.XPATH, "//div[@id='btn-update']/button[1]")).click()
        sleep(t)

    # 页面底部button2 (如：保存、确定)
    def click_confirmBtn2(self, t):
        self.find_element(*(By.XPATH, "//div[@id='btn-update']/button[2]")).click()
        sleep(t)

    # 页面底部button3 （如：发送给平台项目运营团队）
    def click_confirmBtn3(self, t):
        self.find_element(*(By.XPATH, "//div[@id='btn-update']/button[3]")).click()
        sleep(t)

    # 添加资源 - 确定（弹框）
    def click_popupConfirmResource(self, t):
        self.find_element(*(By.XPATH, "//body/div[6]/div[3]/button")).click()
        sleep(t)

    # 添加子项目 - 提交、下一步
    def click_rlsSubProjectSubmit(self, t):
        self.find_element(*(By.XPATH, "//button[@id='btn-create']")).click()
        sleep(t)

    # 发布的项目 - 下一步
    def click_rlsNextStep(self, t):
        self.find_element(*(By.XPATH, "//button[@id='btn-create']")).click()
        sleep(t)














    # Select globalSelect = new Select(driver.findElement(By.id("selectid")));
    # globalSelect.selectByIndex(1);--[注]index是从0开始的

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









