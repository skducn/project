# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-5-12
# Description: SAAS库
# *****************************************************************

import sys, unittest

sys.path.append("../../../../")
import instance.zyjk.SAAS.PageObject.ReadConfigPO as readConfig
localReadConfig = readConfig.ReadConfigPO()
from PO.LogPO import *
from PO.NetPO import *
from PO.DevicePO import *
from PO.ColorPO import *
from PO.ExcelPO.ExcelPO import *
from PO.TimePO import *
from PO.SqlserverPO import *
from PO.FilePO import *
from PO.HtmlPO import *
from PO.ListPO import *
from PO.MysqlPO import *

from time import sleep
from BeautifulReport import BeautifulReport as bf
from BeautifulReport import BeautifulReport


class CustomizeError(BaseException):
    # 自定义报错
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class SaasPO(unittest.TestCase):

    # def save_img(self, img_name):
    #     self.Web_PO.captureBrowser('{}/{}.png'.format(os.path.abspath('d:\\'), img_name))

    # def __init__(self):
    #     self.Time_PO = TimePO()
    #     self.File_PO = FilePO()
    #     self.Excel_PO = ExcelPO()
    #     # self.Log_PO = LogPO(logFile, fmt='%(levelname)s - %(message)s - %(asctime)s')  # 输出日志
    #     self.Web_PO = WebPO("chrome")
    #     self.Web_PO.openURL(localReadConfig.get_http("varUrl"))
    #     self.Web_PO.driver.maximize_window()  # 全屏
    #     # self.Web_PO.driver.set_window_size(1366,768)  # 按分辨率1366*768打开
    #     self.List_PO = ListPO()
    #     self.Color_PO = ColorPO()
    #     self.Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "saasuserdev", 3306)  # 测试环境

    @classmethod
    def setUpClass(self):
        global ruleType, isRun, caseFrom, caseTo, curl, rulesApi, archiveNum, jar, excel, excelSheet1
        self.Time_PO = TimePO()
        self.File_PO = FilePO()
        self.Excel_PO = ExcelPO()
        self.Device_PO = DevicePO()
        self.List_PO = ListPO()
        self.Color_PO = ColorPO()
        self.excelFile = localReadConfig.get_excel("webFile")
        self.Mysql_PO = MysqlPO(localReadConfig.get_db("host"), localReadConfig.get_db("username"), localReadConfig.get_db("password"), localReadConfig.get_db("database"), localReadConfig.get_db("port"))
        # self.Log_PO = LogPO(logFile, fmt='%(levelname)s - %(message)s - %(asctime)s')  # 输出日志

        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(localReadConfig.get_http("webUrl"))
        self.Web_PO.driver.maximize_window()  # 全屏

        self.varExcel = os.path.abspath(File_PO.getLayerPath("../config") + "/" + self.excelFile)
        self.varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取当天日期时间,格式：20161020130318
        bk = xlrd.open_workbook(self.varExcel, formatting_info=True)
        self.newbk = copy(bk)
        self.sheetMain = bk.sheet_by_name("main")
        self.sheetTestCase = bk.sheet_by_name("testcase")
        self.styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
        self.styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
        self.styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')

    @classmethod
    def tearDownClass(self):
        pass

    def test1Main(self):

        ''' 测试模块 '''

        for i in range(1, self.sheetMain.nrows):
            if self.sheetMain.cell_value(i, 0) == "Y":
                self.mainModule = self.sheetMain.cell_value(i, 1)
                sleep(2)
                self.readTestcase()

    def readTestcase(self):
        # 遍历TestCase及调用函数模块,定位测试用例位置及数量
        # print("\n")
        caseEnd = 0
        caseFrom = 0
        for j in range(1, self.sheetTestCase.nrows):  # 遍历所有记录
            if self.sheetTestCase.cell_value(j, 2) == self.mainModule:  # 判断 module = 登录 的编号
                caseFrom = j
                break
        for j in range(caseFrom + 1, self.sheetTestCase.nrows):  # 遍历从编号为登录记录到结尾的记录
            if j > self.sheetTestCase.nrows:
                caseEnd = j
            elif self.sheetTestCase.cell_value(j, 2) != "":
                caseEnd = j
                break
        # print(str(self.mainModule) + "(" + str(caseFrom+1) + " - " + str(caseEnd) + ")")

        # 遍历 module的case
        newWs = self.newbk.get_sheet(1)
        for l in range(caseFrom, caseEnd):
            if self.sheetTestCase.cell_value(l, 1) == "N" or self.sheetTestCase.cell_value(l,
                                                                                           1) == "n" or self.sheetTestCase.cell_value(
                    l, 4) == "":
                pass
            else:
                newWs.write(l, 0, "", self.styleBlue)  # 清空执行日期
                newWs.write(l, 5, "", self.styleBlue)  # 清空备注
                varResult = eval(self.sheetTestCase.cell_value(l, 4))
                if varResult[1] == "ok":
                    newWs.write(l, 0, varResult[0], self.styleBlue)
                    self.newbk.save(self.varExcel)
                    print("[ok] caseNo." + str(l + 1) + " , " + str(
                        self.sheetTestCase.cell_value(caseFrom, 2)) + " , " + str(
                        self.sheetTestCase.cell_value(l, 3)) + " , " + str(self.sheetTestCase.cell_value(l, 4)))
                elif varResult[1] == "error":
                    newWs.write(l, 0, varResult[0], self.styleRed)
                    newWs.write(l, 5, varResult[2], self.styleRed)
                    self.newbk.save(self.varExcel)
                    print("[error: " + varResult[2] + "] caseNo." + str(l + 1) + " , " + str(
                        self.sheetTestCase.cell_value(caseFrom, 2)) + " , " + str(
                        self.sheetTestCase.cell_value(l, 3)) + " , " + str(self.sheetTestCase.cell_value(l, 4)))
                    exit()
                elif varResult[1] == "warning":
                    newWs.write(l, 0, varResult[0], self.styleRed)
                    newWs.write(l, 5, varResult[2], self.styleRed)
                    self.newbk.save(self.varExcel)
                    Color_PO.consoleColor("31", "33",
                                          "[warning: " + varResult[2] + "] caseNo." + str(l + 1) + " , " + str(
                                              self.sheetTestCase.cell_value(caseFrom, 2)) + " , " + str(
                                              self.sheetTestCase.cell_value(l, 3)) + " , " + str(
                                              self.sheetTestCase.cell_value(l, 4)), "")

    def login(self, varUser, varPass):

        ''' 登录 '''

        self.Web_PO.inputXpath("//input[@placeholder='用户名']", varUser)
        self.Web_PO.inputXpath("//input[@placeholder='密码']", varPass)
        self.Web_PO.clickXpath("//button[@type='button']", 2)  # 登录
        # 检查登录是否成功
        if self.Web_PO.isElementXpath(
                '//*[@id="app"]/section/div/section/section/header/div/div[1]/div[3]/div[2]/div/span[2]'):
            if self.Web_PO.getXpathText(
                    '//*[@id="app"]/section/div/section/section/header/div/div[1]/div[3]/div[2]/div/span[2]') == "个人中心":
                return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "ok", ""]
            else:
                return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "error", "登录后页面异常！"]
        else:
            return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "error", "无法登录或登录后页面异常！"]

    # 操作菜单
    def clickMenuAll(self, varMenu1, varMenu2):

        ''' 选择主菜单 '''

        try:
            varSign = 0
            list1 = self.Web_PO.getXpathsAttr("//li", "index")
            list1 = self.List_PO.listDel(list1, None)
            list2 = self.Web_PO.getXpathsText("//li")
            list2 = self.List_PO.listDel(list2, "")
            dict1 = self.List_PO.lists2dict(list2, list1)
            for k in dict1:
                if k == varMenu1:
                    varSign = 1
                    self.Web_PO.clickXpath("//li[@index='" + dict1[k] + "']", 2)
                    break
            sleep(1)
            # 如果菜单不存在则退出系统
            if varSign == 0:
                return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "error", '"' + varMenu1 + '" 不存在！']

            # 选择子菜单 '''

            varSign = 0
            list1 = self.Web_PO.getXpathsText("//a/li")
            list2 = self.Web_PO.getXpathsAttr("//a", "href")
            dict1 = self.List_PO.lists2dict(list1, list2)
            for k in dict1:
                if k == varMenu2:
                    varSign = 1
                    self.Web_PO.clickXpath("//a[@href='" + str(dict1[k]).split("http://192.168.0.213")[1] + "']", 2)
                    break
            if varSign == 0:
                return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "error", '"' + varMenu2 + '" 不存在！']

            return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "ok", ""]

        except CustomizeError as e:
            print(e)

    # 注册.医疗机构注册
    def reg_medicalReg_add_address(self, varProvince, varCity):

        '''注册管理 - 医疗机构注册 - 新增 - 联系地址,遍历所属地区'''

        list1 = self.Web_PO.getXpathsText("//li")
        list1 = self.List_PO.listIntercept(list1, '澳门特别行政区', 1)
        # print(list1)
        for i in range(len(list1)):
            if varProvince == list1[i]:
                self.Web_PO.clickXpath(
                    "//ul[@类与实例='el-scrollbar__view el-cascader-menu__list']/li[" + str(i + 2) + "]", 2)  # 所属地区2级
                list2 = self.Web_PO.getXpathsText("//li")
                list2 = self.List_PO.listIntercept(list2, '台湾', 1)
                # print(list2)
                for i in range(len(list2)):
                    if varCity == list2[i]:
                        self.Web_PO.clickXpath(
                            "//div[@类与实例='el-cascader-panel']/div[2]/div[1]/ul/li[" + str(i + 1) + "]", 2)
                        break
                break

    def reg_medicalReg_search(self, varHospital):

        '''注册管理 - 医疗机构注册 - 搜索 '''

        varSign = -1
        self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院名称']", varHospital)
        self.Web_PO.clickXpath("//button[@类与实例='el-button left-search el-button--primary']", 2)  # 搜索
        if self.Web_PO.isElementXpath("//tr[@类与实例='el-table__row']"):
            list1 = self.Web_PO.getXpathsText("//tr[@类与实例='el-table__row']/td[1]/div")
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if varHospital == list1[i]:
                    varSign = i
            if varSign > -1:
                return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "ok", "", True, varSign + 1]
            else:
                return [1, datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "error", "没找到！", False, varSign + 1]
        return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "error", "没找到！", False, varSign + 1]

    def reg_medicalReg_add(self, l_medicalReg):

        ''' 注册管理.医疗机构注册 - 新增医疗机构 '''
        # 逻辑：数据库里检查是否有重复的医院名称及代码，如果都不存在则新增医疗机构，否则提示已存在。

        try:
            # 数据库里检查是否有重复的医院名称及代码
            self.Mysql_PO.cur.execute('select count(*) from sys_org where orgName="%s"' % l_medicalReg[0])
            t_countOrgNameByDb = self.Mysql_PO.cur.fetchall()
            self.Mysql_PO.cur.execute('select count(*) from sys_org where orgNo="%s"' % l_medicalReg[1])
            t_countOrgNoByDb = self.Mysql_PO.cur.fetchall()

            if t_countOrgNameByDb[0][0] == 0 and t_countOrgNoByDb[0][0] == 0:
                self.Web_PO.clickXpath("//button[@类与实例='el-button right-add el-button--primary']", 2)  # 新增
                self.Web_PO.inputXpathClear("//form[@类与实例='el-form']/div[1]/div/div/input", l_medicalReg[0])  # 医院名称
                self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院代码']", l_medicalReg[1])  # 代码
                self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院负责人姓名']", l_medicalReg[2])  # 负责人
                self.Web_PO.clickXpath("//input[@placeholder='请输入所属地区']", 2)  # 所属地区
                self.reg_medicalReg_add_address(l_medicalReg[3], l_medicalReg[4])
                self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院详细地址']", l_medicalReg[5])
                self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院联系人姓名']", l_medicalReg[6])
                self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院联系人电话']", l_medicalReg[7])
                self.Web_PO.inputXpathClear("//textarea[@placeholder='请输入医院介绍']", l_medicalReg[8])
                self.Web_PO.clickXpath("//div[@类与实例='el-dialog__footer']/span/button[2]", 2)  # 保存
                return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "ok", ""]
            else:
                return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "warning", "医院名称或代码已存在！"]
        except:
            return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "error", "注册管理.医疗机构注册 - 新增医疗机构报错！"]

    def reg_medicalReg_edit(self, varHospitalName, l_medicalReg):

        '''注册管理 - 医疗机构注册 - 编辑 '''
        # varHospital, varCode, varLead, varProvince, varCity, varAddress, varName, varPhone, varIntro
        # 逻辑：数据库里检查是否有重复的医院名称及代码，如果都不存在则编辑医疗机构，否则提示已存在。

        try:
            # 数据库里检查是否有重复的医院名称及代码
            self.Mysql_PO.cur.execute('select count(*) from sys_org where orgName="%s"' % l_medicalReg[0])
            t_countOrgNameByDb = self.Mysql_PO.cur.fetchall()
            self.Mysql_PO.cur.execute('select count(*) from sys_org where orgNo="%s"' % l_medicalReg[1])
            t_countOrgNoByDb = self.Mysql_PO.cur.fetchall()

            list1 = self.reg_medicalReg_search(varHospitalName)
            if list1[3] == True:
                if t_countOrgNameByDb[0][0] == 0 and t_countOrgNoByDb[0][0] == 0:
                    self.Web_PO.clickXpath("//div[@类与实例='el-table__fixed-right']/div[2]/table/tbody/tr[" + str(
                        list1[4]) + "]/td[8]/div/span", 2)  # 编辑
                    self.Web_PO.inputXpathClear("//form[@类与实例='el-form']/div[1]/div/div/input",
                                                l_medicalReg[0])  # 医院名称
                    self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院代码']", l_medicalReg[1])  # 代码
                    self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院负责人姓名']", l_medicalReg[2])  # 负责人
                    self.Web_PO.clickXpath("//form[@类与实例='el-form']/div[4]/div/div/div/input", 2)  # 所属地区
                    self.reg_medicalReg_add_address(l_medicalReg[3], l_medicalReg[4])
                    self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院详细地址']", l_medicalReg[5])
                    self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院联系人姓名']", l_medicalReg[6])
                    self.Web_PO.inputXpathClear("//input[@placeholder='请输入医院联系人电话']", l_medicalReg[7])
                    self.Web_PO.inputXpathClear("//textarea[@placeholder='请输入医院介绍']", l_medicalReg[8])
                    self.Web_PO.clickXpath("//div[@类与实例='el-dialog__footer']/span/button[2]", 2)  # 保存
                    return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "ok", ""]
                else:
                    return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "warning", "医院名称或代码已存在！"]
            else:
                return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "warning", "医院名称不存在！"]
        except:
            return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "error", "注册管理.医疗机构注册 - 编辑医疗机构报错！"]

    def reg_medicalReg_opr(self, varSearchHospital, varOpr):

        '''对医院名称进行启用或停用操作'''

        try:
            list1 = self.reg_medicalReg_search(varSearchHospital)
            # print(list1)
            if list1[3] == True:
                if varOpr == "启用":
                    if not self.Web_PO.isElementXpath(
                            "//div[@类与实例='el-table__fixed-right']/div[2]/table/tbody/tr[" + str(
                                    list1[3]) + "]/td[8]/div/div/span[1]/span[@aria-hidden]"):
                        self.Web_PO.clickXpath("//div[@类与实例='el-table__fixed-right']/div[2]/table/tbody/tr[" + str(
                            list1[3]) + "]/td[8]/div/div/span[1]/span", 2)  # 点击停用
                if varOpr == "停用":
                    if not self.Web_PO.isElementXpath(
                            "//div[@类与实例='el-table__fixed-right']/div[2]/table/tbody/tr[" + str(
                                    list1[3]) + "]/td[8]/div/div/span[3]/span[@aria-hidden]"):
                        self.Web_PO.clickXpath("//div[@类与实例='el-table__fixed-right']/div[2]/table/tbody/tr[" + str(
                            list1[3]) + "]/td[8]/div/div/span[3]/span", 2)  # 点击启用
                return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "ok", ""]
            else:
                return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "warning", "医院名称没找到！"]
        except:
            return [datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "error", varSearchHospital + "," + varOpr + "失败！"]

    # 注册.科室管理
    def reg_officeReg_search(self, varHospital):

        '''注册管理 - 可是注册 - 搜索医疗机构或科室'''

        self.Web_PO.inputXpath("//input[@placeholder='请输入机构或科室名称']", varHospital)
        self.Web_PO.clickXpath("//button[@类与实例='el-button left-search el-button--primary']", 2)  # 搜索
        list1 = self.Web_PO.getXpathsText("//span")
        varNoData = list1.pop()
        if varNoData == "暂无数据":
            return False
        return True

    def reg_officeReg_add(self, varSearchResult, varOffice, varOfficeIntro):

        '''注册管理 - 科室注册 - 添加科室'''

        if varSearchResult:
            self.Web_PO.clickXpath(
                '//*[@id="app"]/section/div/section/section/main/div/div/div/div[1]/section/main/div/div[11]/div[1]/span[2]/span[2]/button/span',
                2)  # 添加
            self.Web_PO.inputXpath("//input[@placeholder='请输入科室名称']", varOffice)
            self.Web_PO.inputXpath("//textarea[@palceholder='请输入科室介绍']", varOfficeIntro)
            self.Web_PO.clickXpath("//button[@类与实例='el-button el-button--primary']", 2)  # 保存

    # 注册.医护人员注册
    def reg_nurseReg_search(self, varName):

        '''注册管理 - 医护人员注册 - 搜索姓名'''

        varSign = -1
        self.Web_PO.inputXpathClear("//input[@placeholder='请输入姓名']", varName)
        self.Web_PO.clickXpath("//button[@类与实例='el-button left-search el-button--primary']", 2)  # 搜索
        if self.Web_PO.isElementXpath("//tr[@类与实例='el-table__row']"):
            list1 = self.Web_PO.getXpathsText("//tr[@类与实例='el-table__row']/td[1]/div")
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if varName == list1[i]:
                    varSign = i
            if varSign > -1:
                return [1, datetime.datetime.now().strftime('%Y%m%d%H%M%S'), True, varSign + 1]
            else:
                return [1, datetime.datetime.now().strftime('%Y%m%d%H%M%S'), False, varSign + 1]
        return ["没找到...", datetime.datetime.now().strftime('%Y%m%d%H%M%S'), False, varSign + 1]

    def reg_nurseReg_add(self, varSearchName, varInfo):

        '''注册管理 - 医护人员注册 - 新增 '''
        # varName, varHead, varPhone, varCertificateType, varIdcard, varSex, varBirthday, varMemberType, varHospital, varOffice, varTitle, varRegDate, varIntro

        list1 = self.reg_nurseReg_search(varSearchName)
        if list1[2] == False:

            self.Web_PO.clickXpath("//button[@类与实例='el-button right-add el-button--primary']", 2)  # 新增

            self.Web_PO.inputXpathClear("//form[@类与实例='el-form']/div[1]/div/div/div/div/input", varInfo[0])  # 姓名
            self.Web_PO.sendKeysName("file", varInfo[1])  # 头像
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入手机号码']", varInfo[2])  # 手机号

            self.Web_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 证件类型
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varInfo[3]:
                    self.Web_PO.clickXpath('/html/body/div[3]/div[1]/div[1]/ul/li[' + str(i + 1) + ']', 2)  # 选择证件类型

            self.Web_PO.inputXpathClear("//input[@placeholder='身份证类型，校验身份证号码']", varInfo[4])

            self.Web_PO.clickXpath("//div[@类与实例='el-col el-col-13']/div[1]/div/div/div[1]/input", 2)  # 性别
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varInfo[5]:
                    self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(i + 1) + "]",
                                           2)  # 选择性别

            self.Web_PO.inputXpathEnter("//input[@placeholder='选择日期']", varInfo[6])

            self.Web_PO.clickXpath("//div[@类与实例='el-col el-col-13']/div[3]/div/div/div[1]/input", 2)  # 人员类别
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varInfo[7]:
                    self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(i + 1) + "]",
                                           2)  # 选择人员类别

            self.Web_PO.clickXpath(
                '//*[@id="app"]/section/div/section/section/main/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div[4]/div/div/div/input',
                2)  # 就职医院及科室
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varInfo[8]:
                    self.Web_PO.clickXpath('//div[@类与实例="el-cascader-panel"]/div[1]/div[1]/ul/li[' + str(i + 1) + ']',
                                           2)  # 选择医疗结构
                    list2 = self.Web_PO.getXpathsText("//span")
                    list2 = self.List_PO.listIntercept(list2, varInfo[8], 1)
                    list2 = self.List_PO.listDel(list2, "")
                    for j in range(len(list2)):
                        if list2[j] == varInfo[9]:
                            self.Web_PO.clickXpath(
                                '//div[@类与实例="el-cascader-panel"]/div[2]/div[1]/ul/li[' + str(j + 1) + ']', 2)  # 选择科室
                            break
                    break

            self.Web_PO.clickXpath("//div[@类与实例='el-col el-col-13']/div[5]/div/div/div[1]/input", 2)  # 职称
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varInfo[10]:
                    self.Web_PO.clickXpath(
                        "//div[@类与实例='el-select-dropdown el-popper' and @x-placement]/div[1]/div[1]/ul/li[" + str(
                            i + 1) + "]", 2)  # 选择职称
                    break

            self.Web_PO.inputXpathEnter(
                '//*[@id="app"]/section/div/section/section/main/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div[6]/div/div/input',
                varInfo[11])  # 注册日期
            self.Web_PO.inputXpathClear("//textarea[@placeholder='请输入个人介绍']", varInfo[12])
            self.Web_PO.clickXpath("//div[@类与实例='el-dialog__footer']/span/button[2]", 2)  # 保存

    def reg_nurseReg_edit(self, varSearchResult, varName, varHead, varPhone, varCertificateType, varIdcard, varSex,
                          varBirthday, varMemberType, varHospital, varOffice, varTitle, varRegDate, varIntro):

        '''注册管理 - 医护人员注册 - 编辑 '''

        if varSearchResult == True:
            self.Web_PO.clickXpath(
                '//*[@id="app"]/section/div/section/section/main/div/div/section/main/div/div[4]/div[2]/table/tbody/tr/td[8]/div/span[1]',
                2)  # 用户
            self.Web_PO.inputXpathClear("//form[@类与实例='el-form']/div[1]/div/div/div/div/input", varName)  # 姓名
            self.Web_PO.sendKeysName("file", varHead)  # 头像
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入手机号码']", varPhone)  # 手机号

            self.Web_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 证件类型
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varCertificateType:
                    self.Web_PO.clickXpath('/html/body/div[3]/div[1]/div[1]/ul/li[' + str(i + 1) + ']', 2)  # 选择证件类型

            self.Web_PO.inputXpathClear("//input[@placeholder='身份证类型，校验身份证号码']", varIdcard)

            self.Web_PO.clickXpath("//div[@类与实例='el-col el-col-13']/div[1]/div/div/div[1]/input", 2)  # 性别
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varSex:
                    self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(i + 1) + "]",
                                           2)  # 选择性别

            self.Web_PO.inputXpathClearEnter("//input[@placeholder='选择日期']", varBirthday)  # 出生日期

            self.Web_PO.clickXpath("//div[@类与实例='el-col el-col-13']/div[3]/div/div/div[1]/input", 2)  # 人员类别
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varMemberType:
                    self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(i + 1) + "]",
                                           2)  # 选择人员类别

            self.Web_PO.clickXpath(
                '//*[@id="app"]/section/div/section/section/main/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div[4]/div/div/div/input',
                2)  # 就职医院及科室
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varHospital:
                    self.Web_PO.clickXpath('//div[@类与实例="el-cascader-panel"]/div[1]/div[1]/ul/li[' + str(i + 1) + ']',
                                           2)  # 选择医疗结构
                    list2 = self.Web_PO.getXpathsText("//span")
                    list2 = self.List_PO.listIntercept(list2, varHospital, 1)
                    list2 = self.List_PO.listDel(list2, "")
                    for j in range(len(list2)):
                        if list2[j] == varOffice:
                            self.Web_PO.clickXpath(
                                '//div[@类与实例="el-cascader-panel"]/div[2]/div[1]/ul/li[' + str(j + 1) + ']', 2)  # 选择科室
                            break
                    break

            self.Web_PO.clickXpath("//div[@类与实例='el-col el-col-13']/div[5]/div/div/div[1]/input", 2)  # 职称
            list1 = self.Web_PO.getXpathsText("//span")
            list1 = self.List_PO.listIntercept(list1, "保存", 1)
            list1 = self.List_PO.listDel(list1, "")
            for i in range(len(list1)):
                if list1[i] == varTitle:
                    self.Web_PO.clickXpath("//div[@x-placement='top-start']/div/div/ul/li[" + str(i + 1) + "]",
                                           2)  # 选择职称

            self.Web_PO.inputXpathClearEnter(
                '//*[@id="app"]/section/div/section/section/main/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div[6]/div/div/input',
                varRegDate)  # 注册日期
            self.Web_PO.inputXpathClear("//textarea[@placeholder='请输入个人介绍']", varIntro)
            self.Web_PO.clickXpath("//div[@类与实例='el-dialog__footer']/span/button[2]", 2)  # 保存

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
                self.Web_PO.clickXpath(
                    "//div[@类与实例='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/div/span[1]/span", 2)  # 启用
                print("已启用")

            if varOpr == "停用" and varSign == 0:
                self.Web_PO.clickXpath(
                    "//div[@类与实例='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/div/span[3]/span", 2)  # 停用
                print("已停用")

    # 注册.配置维护
    def reg_Config_opr(self, varConfigName, varValue):

        '''注册管理 - 配置维护 - 修改配置的当前值'''

        self.Web_PO.inputXpathClearEnter("//input[@placeholder='支持配置名称关键字及拼音首字母关键字']", varConfigName)  # 搜索配置名称
        self.Web_PO.clickXpath(
            '//*[@id="app"]/section/div/section/section/main/div/section/main/form/div/div[4]/div[2]/table/tbody/tr/td[8]/div/span',
            2)  # 点击修改
        # 当前值，如果是输入框，否则是下拉框
        if self.Web_PO.isElementXpath("//input[@placeholder='请输入数字']"):
            self.Web_PO.inputXpathClearEnter("//input[@placeholder='请输入数字']", varValue)
        elif self.Web_PO.isElementXpath(
                '//*[@id="app"]/section/div/section/section/main/div/section/main/form/div/div[3]/table/tbody/tr/td[3]/div/div/div/div/div[1]/input'):
            self.Web_PO.clickXpath(
                '//*[@id="app"]/section/div/section/section/main/div/section/main/form/div/div[3]/table/tbody/tr/td[3]/div/div/div/div/div[1]/input',
                1)
            if varValue == "启用" or varValue == "是":
                self.Web_PO.clickXpath('/html/body/div[2]/div[1]/div[1]/ul/li[1]', 1)  # 启用/是
            else:
                self.Web_PO.clickXpath('/html/body/div[2]/div[1]/div[1]/ul/li[2]', 2)  # 停用/否
        self.Web_PO.clickXpath(
            '//*[@id="app"]/section/div/section/section/main/div/section/main/form/div/div[4]/div[2]/table/tbody/tr/td[8]/div/span[1]',
            2)  # 保存

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
                varSign = 1
                break
        if varSign == 0:
            self.Web_PO.clickXpath(
                '//*[@id="app"]/section/div/section/section/main/div/section/section[1]/header/div/div[2]/button/span',
                2)  # 新建角色
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入内容']", varRole)  # 角色
            self.Web_PO.clickXpath(
                '//*[@id="app"]/section/div/section/section/main/div/section/section[1]/main/ul/li[' + str(
                    len(list1) + 1) + ']/div/div[2]', 2)  # 保存

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
                varSign = i + 1
                break
        if varSign != 0:
            self.Web_PO.clickXpath(
                '//*[@id="app"]/section/div/section/section/main/div/section/section[1]/main/ul/li[' + str(
                    varSign) + ']/div/div[2]', 2)  # 编辑
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入内容']", varRoleNew)  # 新角色
            self.Web_PO.clickXpath(
                '//*[@id="app"]/section/div/section/section/main/div/section/section[1]/main/ul/li[' + str(
                    varSign) + ']/div/div[2]', 2)  # 保存

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
                varSign = i + 1
                break
        if varSign != 0:
            self.Web_PO.clickXpath(
                '//*[@id="app"]/section/div/section/section/main/div/section/section[1]/main/ul/li[' + str(
                    varSign) + ']/div/div[3]', 2)  # 删除
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
            self.Web_PO.clickXpath(
                '//*[@id="app"]/section/div/section/section/main/div/section/section[1]/main/ul/li[' + str(
                    varSign) + ']/div/div[1]', 2)  # 点击角色

            # 获取大菜单列表
            list0 = self.Web_PO.getXpathsText("//li")
            list0 = self.List_PO.listIntercept(list0, "角色管理", 0)
            list0 = self.List_PO.listDel(list0, "")

            # 清除所有大菜单的勾选（点击大菜单的checkbox，再取消已勾选的。）
            for i in range(len(list0)):
                self.Web_PO.clickXpaths("//div[@类与实例='el-tree']/div[" + str(i + 1) + "]/div[1]/label", 2)
            for i in range(len(list0)):
                if self.Web_PO.isElementXpathByAttr("//div[@类与实例='el-tree']/div[" + str(i + 1) + "]", "aria-checked",
                                                    "true"):
                    self.Web_PO.clickXpaths("//div[@类与实例='el-tree']/div[" + str(i + 1) + "]/div[1]/label", 2)

            # 子菜单列表
            list6 = (self.Web_PO.getXpathsText("//div[@类与实例='el-tree-node__children']/div/div[1]/span[2]"))

            # 子菜单对应的层级及序号
            x = (self.Web_PO.getXpathsQty("//div[@类与实例='el-tree']/div"))
            list2 = []
            for i in range(x - 1):
                a = (self.Web_PO.getXpathsQty("//div[@类与实例='el-tree']/div[" + str(i + 1) + "]/div[2]/div"))
                for j in range(a):
                    list2.append(str(i + 1) + "." + str(j + 1))

            # 将子菜单列表与子菜单对应的层级及序号组合成字典
            dict1 = self.List_PO.lists2dict(list6, list2)
            # {'医疗机构注册': '1.1', '科室注册': '1.2', '医护人员注册': '1.3', '配置维护': '1.4', '标准代码': '1.5', '角色管理': '2.1', '用户管理': '2.2', '项目管理': '3.1', '元素库': '4.1', '表单库': '4.2', '随访方案': '4.3', '元素DB分类': '4.4', '元素缺省值维护': '4.5', '宣教文章管理': '5.1'}

            for i in range(len(varMenu)):
                for k in dict1:
                    if k == varMenu[i]:
                        self.Web_PO.clickXpath(
                            "//div[@类与实例='el-tree']/div[" + str(dict1[k]).split(".")[0] + "]/div[2]/div[" +
                            str(dict1[k]).split(".")[1] + "]/div[1]/label", 2)

            self.Web_PO.clickXpath(
                '//*[@id="app"]/section/div/section/section/main/div/section/section[2]/footer/button', 2)  # 保存


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern='SaasPO.py', top_level_dir=None)
    runner = bf(suite)
    reportFile = '../report/saas测试报告_' + str(Time_PO.getDatetime()) + '.html'
    runner.report(filename=reportFile, description='SAAS自动化测试报告')
    os.system("start " + reportFile)

# if __name__ == '__main__':
#     currentPath = os.path.split(os.path.realpath(__file__))[0]
#     getConfig = os.path.join(currentPath, "config.ini")
#     print(currentPath)
#     # Saas_PO = SaasPO()
