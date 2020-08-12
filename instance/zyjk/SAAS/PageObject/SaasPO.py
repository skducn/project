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


    def clickMenu(self, varMenu1):

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

    def clickMenu2(self, varName):

        ''' 点击菜单2 '''

        list1 = self.Web_PO.getXpathsText("//a/li")
        list2 = self.Web_PO.getXpathsAttr("//a", "href")
        dict1 = self.List_PO.lists2dict(list1, list2)
        for k in dict1:
            if k == varName:
                x = str(dict1[k]).split("http://192.168.0.213")[1]
                self.Web_PO.clickXpath("//a[@href='" + x + "']", 2)
                break

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



    def reg_nurseReg_search(self, varName):

        '''注册管理 - 医护人员注册 - 搜索姓名'''

        self.Web_PO.inputXpath("//input[@placeholder='请输入姓名']", varName)
        self.Web_PO.clickXpath("//button[@class='el-button left-search el-button--primary']", 2)  # 搜索
        list1 = self.Web_PO.getXpathsText("//span")
        for i in list1:
            if i == "暂无数据":
                return False
        return True

    def reg_nurseReg_add(self, varSearchResult, varName, varHead, varPhone, varIdcard, varBirthday, varRegDate, varIntro):

        '''注册管理 - 医护人员注册 - 新增 '''

        if varSearchResult == False:
            self.Web_PO.clickXpath("//button[@class='el-button right-add el-button--primary']", 2)  # 新增
            self.Web_PO.inputXpathClear("//form[@class='el-form']/div[1]/div/div/div/div/input", varName)  # 姓名
            self.Web_PO.inputXpathEnter("//input[@class='el-upload__input']", varHead)  # 头像
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入手机号码']", varPhone)  # 手机号
            self.Web_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 证件类型
            self.Web_PO.clickXpath('/html/body/div[3]/div[1]/div[1]/ul/li[2]', 2)  # 军官证
            self.Web_PO.inputXpathClear("//input[@placeholder='身份证类型，校验身份证号码']", varIdcard)

            self.Web_PO.clickXpath("//div[@class='el-col el-col-13']/div[1]/div/div/div[1]/input", 2)  # 性别
            self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[2]", 2)  # 女

            self.Web_PO.inputXpathEnter("//input[@placeholder='选择日期']", varBirthday)

            self.Web_PO.clickXpath("//div[@class='el-col el-col-13']/div[3]/div/div/div[1]/input", 2)  # 人员类型
            self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[2]", 2)  # 医生

            # self.Web_PO.clickXpath("//div[@class='el-col el-col-13']/div[4]/div/div/div[1]/input", 2)  # 就职医院及科室
            # self.Web_PO.clickXpath('//*[@id="cascader-menu-2150-0-10"]/span', 2)  #  医疗结构
            # self.Web_PO.clickXpath('//*[@id="cascader-menu-8114-1-2"]/span', 2)  # 科室

            self.Web_PO.clickXpath("//div[@class='el-col el-col-13']/div[5]/div/div/div[1]/input", 2)  # 职称
            self.Web_PO.clickXpath("//div[@x-placement='top-start']/div/div/ul/li[2]", 2)  # 护士

            self.Web_PO.inputXpathEnter('//*[@id="app"]/section/div/section/section/main/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div[6]/div/div/input',"2020-08-13")
            # self.Web_PO.inputXpathEnter('//*[@id="app"]/section/div/section/section/main/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div[6]/div/div/input', varRegDate) #  注册日期
            self.Web_PO.inputXpathClear("//textarea[@placeholder='请输入个人介绍']", varIntro)
            # self.Web_PO.clickXpath("//div[@class='el-dialog__footer']/span/button[2]", 2)  # 保存




if __name__ == '__main__':
    currentPath = os.path.split(os.path.realpath(__file__))[0]
    getConfig = os.path.join(currentPath, "config.ini")
    print(currentPath)
    # Saas_PO = SaasPO()


