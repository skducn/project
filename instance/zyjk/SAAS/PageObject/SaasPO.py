# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-5-12
# Description: SAAS库
# *****************************************************************

import instance.zyjk.SAAS.config.readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
from PO.LogPO import *
from PO.NetPO import *
from PO.DataPO import *
from PO.ColorPO import *
from PO.ExcelPO.ExcelPO import *
from PO.TimePO import *
from PO.SqlserverPO import *
from PO.FilePO import *
from PO.WebPO import *
from PO.ListPO import *
from PO.ColorPO import *
from time import sleep
from multiprocessing import Process

class SaasPO(object):

    def __init__(self):
        global ruleType,isRun,caseFrom,caseTo,curl,rulesApi,archiveNum,jar,excel,excelSheet1

        self.excelFile = localReadConfig.get_excel("excelFile")
        self.excelFileSheetName = localReadConfig.get_excel("excelFileSheetName")
        host = localReadConfig.get_database("host")
        username = localReadConfig.get_database("username")
        password = localReadConfig.get_database("password")
        database = localReadConfig.get_database("database")

        self.Sqlserver_PO = SqlServerPO(host, username, password, database)
        # logFile = localReadConfig.get_log("logFile")
        self.Time_PO = TimePO()
        self.File_PO = FilePO()
        self.Excel_PO = ExcelPO()
        # self.Log_PO = LogPO(logFile, fmt='%(levelname)s - %(message)s - %(asctime)s')  # 输出日志

        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(localReadConfig.get_http("varUrl"))
        self.Web_PO.driver.maximize_window()  # 全屏
        # self.Web_PO.driver.set_window_size(1366,768)  # 按分辨率1366*768打开
        self.List_PO = ListPO()
        self.Color_PO = ColorPO()


    def login(self, varUser, varPass):

        ''' 登录 '''

        global varUser_session
        varUser_session = varUser

        self.Web_PO.inputXpath("//input[@placeholder='用户名']", varUser)
        self.Web_PO.inputXpath("//input[@placeholder='密码']", varPass)
        self.Web_PO.clickXpath("//button[@type='button']", 2)

    # 操作菜单
    def clickMenuAll(self, varMenu1, varMenu2):

        ''' 点击菜单1 '''

        list1 = self.Web_PO.getXpathsAttr("//li", "index")
        list1 = self.List_PO.listDel(list1, None)
        list2 = self.Web_PO.getXpathsText("//li")
        list2 = self.List_PO.listDel(list2, "")
        dict1 = self.List_PO.lists2dict(list2, list1)
        for k in dict1:
            if k == varMenu1:
                self.Web_PO.clickXpath("//li[@index='" + dict1[k] + "']", 2)
                break
        sleep(1)

        ''' 点击菜单2 '''

        list1 = self.Web_PO.getXpathsText("//a/li")
        list2 = self.Web_PO.getXpathsAttr("//a", "href")
        dict1 = self.List_PO.lists2dict(list1, list2)
        for k in dict1:
            if k == varMenu2:
                x = str(dict1[k]).split("http://192.168.0.213")[1]
                self.Web_PO.clickXpath("//a[@href='" + x + "']", 2)
                break


    # 注册.医疗机构注册
    def reg_medicalReg_add_address(self, varProvince, varCity):

        '''注册管理 - 医疗机构注册 - 新增 - 联系地址,遍历所属地区'''

        list1 = self.Web_PO.getXpathsText("//li")
        list1 = self.List_PO.listIntercept(list1, '澳门特别行政区', 1)
        # print(list1)
        for i in range(len(list1)):
            if varProvince == list1[i]:
                self.Web_PO.clickXpath("//ul[@class='el-scrollbar__view el-cascader-menu__list']/li[" + str(i + 2) + "]", 2)  # 所属地区2级
                list2 = self.Web_PO.getXpathsText("//li")
                list2 = self.List_PO.listIntercept(list2, '台湾', 1)
                # print(list2)
                for i in range(len(list2)):
                    if varCity == list2[i]:
                        self.Web_PO.clickXpath("//div[@class='el-cascader-panel']/div[2]/div[1]/ul/li[" + str(i + 1) + "]", 2)
                        break
                break

    def reg_medicalReg_search(self, varHospital):

        '''注册管理 - 医疗机构注册 - 搜索 '''

        self.Web_PO.inputXpath("//input[@placeholder='请输入医院名称']", varHospital)
        self.Web_PO.clickXpath("//button[@class='el-button left-search el-button--primary']", 2)  # 搜索
        if self.Web_PO.isElementXpath("//tr[@class='el-table__row']"):
            return True
        return False

    def reg_medicalReg_add(self, varSearchResult, varHospital, varCode, varLead, varProvince, varCity, varAddress, varName, varPhone,varIntro):

        '''注册管理 - 医疗机构注册 - 新增 '''

        if varSearchResult == False:
            self.Web_PO.clickXpath("//button[@class='el-button right-add el-button--primary']", 2)  # 新增
            self.Web_PO.inputXpathClear("//form[@class='el-form']/div[1]/div/div/input", varHospital)  # 医院名称
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院代码']", varCode)  # 代码
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院负责人姓名']", varLead)  # 负责人
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入所属地区']", 2)  # 所属地区
            self.reg_medicalReg_add_address(varProvince, varCity)
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院详细地址']", varAddress)
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院联系人姓名']", varName)
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院联系人电话']", varPhone)
            self.Web_PO.inputXpathClear("//textarea[@placeholder='请输入医院介绍']", varIntro)
            self.Web_PO.clickXpath("//div[@class='el-dialog__footer']/span/button[2]", 2)  # 保存

    def reg_medicalReg_edit(self, varSearchResult, varHospital, varCode, varLead, varProvince, varCity, varAddress, varName, varPhone, varIntro):

        '''注册管理 - 医疗机构注册 - 编辑 '''

        if varSearchResult == True:
            self.Web_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/span", 2)  # 编辑
            self.Web_PO.inputXpathClear("//form[@class='el-form']/div[1]/div/div/input", varHospital)  # 医院名称
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院代码']", varCode)  # 代码
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院负责人姓名']", varLead)  # 负责人
            self.Web_PO.clickXpath("//form[@class='el-form']/div[4]/div/div/div/input", 2)  # 所属地区
            self.reg_medicalReg_add_address(varProvince, varCity)
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院详细地址']", varAddress)
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院联系人姓名']", varName)
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院联系人电话']", varPhone)
            self.Web_PO.inputXpathClear("//textarea[@placeholder='请输入医院介绍']", varIntro)
            self.Web_PO.clickXpath("//div[@class='el-dialog__footer']/span/button[2]", 2)  # 保存

    def reg_medicalReg_opr(self, varSearchResult, varOpr):

        '''对医院名称进行启用或停用操作'''

        if varSearchResult == True:
            # 操作（启用或停用）
            list1 = self.Web_PO.getXpathsText("//span")
            varSign = 0
            for i in list1:
                if varOpr == i:
                    varSign = 1
                    break
            if varOpr == "启用" and varSign == 0:
                self.Web_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/div/span[1]/span", 2)  # 启用
                print("已启用")

            if varOpr == "停用" and varSign == 0:
                self.Web_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/div/span[3]/span", 2)  # 停用
                print("已停用")


    # 注册.科室管理
    def reg_officeReg_search(self, varHospital):

        '''注册管理 - 可是注册 - 搜索医疗机构或科室'''

        self.Web_PO.inputXpath("//input[@placeholder='请输入机构或科室名称']", varHospital)
        self.Web_PO.clickXpath("//button[@class='el-button left-search el-button--primary']", 2)  # 搜索
        list1 = self.Web_PO.getXpathsText("//span")
        varNoData = list1.pop()
        if varNoData == "暂无数据":
            return False
        return True

    def reg_officeReg_add(self, varSearchResult, varOffice, varOfficeIntro):

        '''注册管理 - 科室注册 - 添加科室'''

        if varSearchResult:
            self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/div/div/div[1]/section/main/div/div[11]/div[1]/span[2]/span[2]/button/span', 2)  # 添加
            self.Web_PO.inputXpath("//input[@placeholder='请输入科室名称']", varOffice)
            self.Web_PO.inputXpath("//textarea[@palceholder='请输入科室介绍']", varOfficeIntro)
            self.Web_PO.clickXpath("//button[@class='el-button el-button--primary']", 2)  # 保存


    # 注册.医护人员注册
    def reg_nurseReg_search(self, varName):

        '''注册管理 - 医护人员注册 - 搜索姓名'''

        self.Web_PO.inputXpath("//input[@placeholder='请输入姓名']", varName)
        self.Web_PO.clickXpath("//button[@class='el-button left-search el-button--primary']", 2)  # 搜索
        list1 = self.Web_PO.getXpathsText("//span")
        for i in list1:
            if i == "暂无数据":
                return False
        return True

    def reg_nurseReg_add(self, varSearchResult, varName, varHead, varPhone, varCertificateType, varIdcard, varSex, varBirthday, varMemberType, varHospital, varOffice, varTitle, varRegDate, varIntro):

        '''注册管理 - 医护人员注册 - 新增 '''

        if varSearchResult == False:
            self.Web_PO.clickXpath("//button[@class='el-button right-add el-button--primary']", 2)  # 新增
            self.Web_PO.inputXpathClear("//form[@class='el-form']/div[1]/div/div/div/div/input", varName)  # 姓名
            self.Web_PO.sendKeysName("file", varHead)  # 头像
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入手机号码']", varPhone)  # 手机号

            self.Web_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 证件类型
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varCertificateType:
                    self.Web_PO.clickXpath('/html/body/div[3]/div[1]/div[1]/ul/li[' + str(i+1) + ']', 2)  # 选择证件类型

            self.Web_PO.inputXpathClear("//input[@placeholder='身份证类型，校验身份证号码']", varIdcard)

            self.Web_PO.clickXpath("//div[@class='el-col el-col-13']/div[1]/div/div/div[1]/input", 2)  # 性别
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varSex:
                    self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(i + 1) + "]", 2)  # 选择性别

            self.Web_PO.inputXpathEnter("//input[@placeholder='选择日期']", varBirthday)

            self.Web_PO.clickXpath("//div[@class='el-col el-col-13']/div[3]/div/div/div[1]/input", 2)  # 人员类别
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varMemberType:
                    self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(i + 1) + "]", 2)  # 选择人员类别

            self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div[4]/div/div/div/input', 2)  # 就职医院及科室
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varHospital:
                    self.Web_PO.clickXpath('//div[@class="el-cascader-panel"]/div[1]/div[1]/ul/li[' + str(i+1) + ']', 2)  #  选择医疗结构
                    list2 = self.Web_PO.getXpathsText("//span")
                    list2 = self.List_PO.listIntercept(list2, varHospital, 1)
                    list2 = self.List_PO.listDel(list2, "")
                    for j in range(len(list2)):
                        if list2[j] == varOffice:
                            self.Web_PO.clickXpath('//div[@class="el-cascader-panel"]/div[2]/div[1]/ul/li[' + str(j+1) + ']', 2)  #  选择科室
                            break
                    break

            self.Web_PO.clickXpath("//div[@class='el-col el-col-13']/div[5]/div/div/div[1]/input", 2)  # 职称
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varTitle:
                    self.Web_PO.clickXpath("//div[@x-placement='top-start']/div/div/ul/li[" + str(i + 1) + "]", 2)  # 选择职称

            self.Web_PO.inputXpathEnter('//*[@id="app"]/section/div/section/section/main/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div[6]/div/div/input', varRegDate) #  注册日期
            self.Web_PO.inputXpathClear("//textarea[@placeholder='请输入个人介绍']", varIntro)
            self.Web_PO.clickXpath("//div[@class='el-dialog__footer']/span/button[2]", 2)  # 保存

    def reg_nurseReg_edit(self, varSearchResult, varName, varHead, varPhone, varCertificateType, varIdcard, varSex, varBirthday, varMemberType, varHospital, varOffice, varTitle, varRegDate, varIntro):

        '''注册管理 - 医护人员注册 - 编辑 '''

        if varSearchResult == True:
            self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/div/section/main/div/div[4]/div[2]/table/tbody/tr/td[8]/div/span[1]', 2)  # 用户
            self.Web_PO.inputXpathClear("//form[@class='el-form']/div[1]/div/div/div/div/input", varName)  # 姓名
            self.Web_PO.sendKeysName("file", varHead)  # 头像
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入手机号码']", varPhone)  # 手机号

            self.Web_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 证件类型
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varCertificateType:
                    self.Web_PO.clickXpath('/html/body/div[3]/div[1]/div[1]/ul/li[' + str(i+1) + ']', 2)  # 选择证件类型

            self.Web_PO.inputXpathClear("//input[@placeholder='身份证类型，校验身份证号码']", varIdcard)

            self.Web_PO.clickXpath("//div[@class='el-col el-col-13']/div[1]/div/div/div[1]/input", 2)  # 性别
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varSex:
                    self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(i + 1) + "]", 2)  # 选择性别

            self.Web_PO.inputXpathClearEnter("//input[@placeholder='选择日期']", varBirthday)  # 出生日期

            self.Web_PO.clickXpath("//div[@class='el-col el-col-13']/div[3]/div/div/div[1]/input", 2)  # 人员类别
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varMemberType:
                    self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(i + 1) + "]", 2)  # 选择人员类别

            self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div[4]/div/div/div/input', 2)  # 就职医院及科室
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varHospital:
                    self.Web_PO.clickXpath('//div[@class="el-cascader-panel"]/div[1]/div[1]/ul/li[' + str(i + 1) + ']', 2)  # 选择医疗结构
                    list2 = self.Web_PO.getXpathsText("//span")
                    list2 = self.List_PO.listIntercept(list2, varHospital, 1)
                    list2 = self.List_PO.listDel(list2, "")
                    for j in range(len(list2)):
                        if list2[j] == varOffice:
                            self.Web_PO.clickXpath('//div[@class="el-cascader-panel"]/div[2]/div[1]/ul/li[' + str(j + 1) + ']', 2)  # 选择科室
                            break
                    break

            self.Web_PO.clickXpath("//div[@class='el-col el-col-13']/div[5]/div/div/div[1]/input", 2)  # 职称
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varTitle:
                    self.Web_PO.clickXpath("//div[@x-placement='top-start']/div/div/ul/li[" + str(i + 1) + "]", 2)  # 选择职称

            self.Web_PO.inputXpathClearEnter('//*[@id="app"]/section/div/section/section/main/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div[6]/div/div/input', varRegDate)  # 注册日期
            self.Web_PO.inputXpathClear("//textarea[@placeholder='请输入个人介绍']", varIntro)
            self.Web_PO.clickXpath("//div[@class='el-dialog__footer']/span/button[2]", 2)  # 保存

    def reg_nurseReg_opr(self, varSearchResult, varOpr):

        '''对医护人员进行启用或停用操作'''

        if varSearchResult == True:
            # 操作（启用或停用）
            list1 = self.Web_PO.getXpathsText("//span")
            varSign = 0
            for i in list1:
                if varOpr == i:
                    varSign = 1
                    break
            if varOpr == "启用" and varSign == 0:
                self.Web_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/div/span[1]/span", 2)  # 启用
                print("已启用")

            if varOpr == "停用" and varSign == 0:
                self.Web_PO.clickXpath(
                    "//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/div/span[3]/span", 2)  # 停用
                print("已停用")


    # 注册.配置维护
    def reg_Config_opr(self, varConfigName, varValue):

        '''注册管理 - 配置维护 - 修改配置的当前值'''

        self.Web_PO.inputXpathClearEnter("//input[@placeholder='支持配置名称关键字及拼音首字母关键字']", varConfigName)  # 搜索配置名称
        self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/section/main/form/div/div[4]/div[2]/table/tbody/tr/td[8]/div/span', 2)  # 点击修改
        # 当前值，如果是输入框，否则是下拉框
        if self.Web_PO.isElementXpath("//input[@placeholder='请输入数字']"):
            self.Web_PO.inputXpathClearEnter("//input[@placeholder='请输入数字']", varValue)
        elif self.Web_PO.isElementXpath('//*[@id="app"]/section/div/section/section/main/div/section/main/form/div/div[3]/table/tbody/tr/td[3]/div/div/div/div/div[1]/input'):
            self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/section/main/form/div/div[3]/table/tbody/tr/td[3]/div/div/div/div/div[1]/input', 1)
            if varValue == "启用" or varValue == "是":
                self.Web_PO.clickXpath('/html/body/div[2]/div[1]/div[1]/ul/li[1]', 1)  # 启用/是
            else:
                self.Web_PO.clickXpath('/html/body/div[2]/div[1]/div[1]/ul/li[2]', 2)  # 停用/否
        self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/section/main/form/div/div[4]/div[2]/table/tbody/tr/td[8]/div/span[1]', 2)  # 保存



    # 权限.新增角色
    def power_role_add(self, varRole):

        '''权限管理 - 角色管理 - 新增角色'''

        # 获取已存在的角色列表
        list1 = self.Web_PO.getXpathsText("//div/div[1]")
        list1 = self.List_PO.listIntercept(list1, "角色", 1)
        list1 = self.List_PO.listDel(list1, "")
        # print(list1)
        varSign = 0
        for i in list1:
            if i == varRole:
                varSign =1
                break
        if varSign == 0:
            self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/section/section[1]/header/div/div[2]/button/span', 2)  # 新建角色
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入内容']", varRole)  # 角色
            self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/section/section[1]/main/ul/li[' + str(len(list1)+1) + ']/div/div[2]', 2)  # 保存

    # 权限.编辑角色名称
    def power_role_editName(self, varRoleOld, varRoleNew):

        ''' 权限管理 - 角色管理 - 编辑角色名称 '''

        # 获取已存在的角色列表
        list1 = self.Web_PO.getXpathsText("//div/div[1]")
        list1 = self.List_PO.listIntercept(list1, "角色", 1)
        list1 = self.List_PO.listDel(list1, "")
        varSign = 0
        for i in range(len(list1)):
            if list1[i] == varRoleOld:
                varSign = i+1
                break
        if varSign != 0:
            self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/section/section[1]/main/ul/li[' + str(varSign) + ']/div/div[2]', 2)  # 编辑
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入内容']", varRoleNew)  # 新角色
            self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/section/section[1]/main/ul/li[' + str(varSign) + ']/div/div[2]', 2)  # 保存

    # 权限.删除角色
    def power_role_del(self, varRole):

        ''' 权限管理 - 角色管理 - 删除角色 '''

        # 获取已存在的角色列表
        list1 = self.Web_PO.getXpathsText("//div/div[1]")
        list1 = self.List_PO.listIntercept(list1, "角色", 1)
        list1 = self.List_PO.listDel(list1, "")
        varSign = 0
        for i in range(len(list1)):
            if list1[i] == varRole:
                varSign = i+1
                break
        if varSign != 0:
            self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/section/section[1]/main/ul/li[' + str(varSign) + ']/div/div[3]', 2)  # 删除
            self.Web_PO.clickXpath('/html/body/div[2]/div/div[3]/button[2]/span', 2)  # 确定

     # 权限.编辑角色的菜单
    def power_role_editMenu(self, varRole, varMenu):

        ''' 权限管理 - 角色管理 - 编辑角色的菜单 '''

        # 获取已存在的角色列表
        list1 = self.Web_PO.getXpathsText("//div/div[1]")
        list1 = self.List_PO.listIntercept(list1, "角色", 1)
        list1 = self.List_PO.listDel(list1, "")
        varSign = 0
        for i in range(len(list1)):
            if list1[i] == varRole:
                varSign = i + 1
                break
        if varSign != 0:
            self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/section/section[1]/main/ul/li[' + str(varSign) + ']/div/div[1]', 2)  # 点击角色

            # 获取大菜单列表
            list0 = self.Web_PO.getXpathsText("//li")
            list0 = self.List_PO.listIntercept(list0, "角色管理", 0)
            list0 = self.List_PO.listDel(list0, "")

            # 清除所有大菜单的勾选（点击大菜单的checkbox，再取消已勾选的。）
            for i in range(len(list0)):
                self.Web_PO.clickXpaths("//div[@class='el-tree']/div[" + str(i+1) + "]/div[1]/label", 2)
            for i in range(len(list0)):
                if self.Web_PO.isElementXpathByAttr("//div[@class='el-tree']/div[" + str(i+1) + "]", "aria-checked", "true"):
                    self.Web_PO.clickXpaths("//div[@class='el-tree']/div[" + str(i + 1) + "]/div[1]/label", 2)

            # 子菜单列表
            list6 = (self.Web_PO.getXpathsText("//div[@class='el-tree-node__children']/div/div[1]/span[2]"))

            # 子菜单对应的层级及序号
            x = (self.Web_PO.getXpathsQty("//div[@class='el-tree']/div"))
            list2 = []
            for i in range(x-1):
                a = (self.Web_PO.getXpathsQty("//div[@class='el-tree']/div[" + str(i+1) + "]/div[2]/div"))
                for j in range(a):
                    list2.append(str(i+1) + "." + str(j+1))

            # 将子菜单列表与子菜单对应的层级及序号组合成字典
            dict1 = self.List_PO.lists2dict(list6, list2)
            # {'医疗机构注册': '1.1', '科室注册': '1.2', '医护人员注册': '1.3', '配置维护': '1.4', '标准代码': '1.5', '角色管理': '2.1', '用户管理': '2.2', '项目管理': '3.1', '元素库': '4.1', '表单库': '4.2', '随访方案': '4.3', '元素DB分类': '4.4', '元素缺省值维护': '4.5', '宣教文章管理': '5.1'}

            for i in range(len(varMenu)):
                for k in dict1:
                    if k == varMenu[i]:
                        self.Web_PO.clickXpath("//div[@class='el-tree']/div[" + str(dict1[k]).split(".")[0] + "]/div[2]/div[" + str(dict1[k]).split(".")[1] + "]/div[1]/label", 2)

            self.Web_PO.clickXpath('//*[@id="app"]/section/div/section/section/main/div/section/section[2]/footer/button', 2)  # 保存


if __name__ == '__main__':
    currentPath = os.path.split(os.path.realpath(__file__))[0]
    getConfig = os.path.join(currentPath, "config.ini")
    print(currentPath)
    # Saas_PO = SaasPO()


