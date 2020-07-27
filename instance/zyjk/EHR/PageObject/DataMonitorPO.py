# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description:  电子健康档案数据监控中心（PC端）EHR对象库
# *****************************************************************

from PO.WebPO import *
from PO.ListPO import *
from PO.ColorPO import *
from instance.zyjk.EHR.config.config import *
import string,numpy
from string import digits

class DataMonitorPO():

    def __init__(self):
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varURL)
        self.Web_PO.driver.maximize_window()  # 全屏
        # self.Web_PO.driver.set_window_size(1366,768)  # 按分辨率1366*768打开
        self.List_PO = ListPO()
        self.Color_PO = ColorPO()

    def login(self, varUser, varPass):

        ''' 登录 '''

        self.Web_PO.inputXpath("//input[@type='text']", varUser)
        self.Web_PO.inputXpath("//input[@type='password']", varPass)
        self.Web_PO.clickXpath("//button[@type='button']", 2)

    def clickMenu(self, varName, varSubName=""):

        ''' 点击左侧菜单 '''

        # 获取菜单名称及对应href
        list1 = self.Web_PO.getXpathsText("//li[@tabindex='-1']")

        # 只有一层菜单
        if varName in str(list1):
            dict1 = self.List_PO.lists2dict(self.List_PO.listDel(list1, ""), self.Web_PO.getXpathsAttr("//div/ul/li/a", "href"))
            # print(dict1)
            for k in dict1:
                if k == varName:
                    self.Web_PO.clickXpathsContain("//a", "href", str(dict1[k]).replace("http://192.168.0.36:19090/test_ehr_admin/", ""), 1)
            self.Color_PO.consoleColor("31", "36", "[" + varName + "]", "")
        else:
            # 有第二层菜单
            list3 = self.Web_PO.getXpathsText("//li")
            list3 = self.List_PO.listDel(list3, "")
            for l in range(len(list3)):
                if varName == list3[l]:
                    self.Web_PO.clickXpath("//div[@class='el-scrollbar__view']/ul/li[" + str(l+1) + "]", 2)

                    list4 = self.Web_PO.getXpathsText("//li")
                    list5 = self.Web_PO.getXpathsAttr("//li[@aria-expanded='true']/ul/li//a", "href")
                    for p in list4:
                        if varName in p and varSubName in p :
                            list4 = (p.split("\n"))
                            list4.pop(0)
                            # break
                    # print(list4)
                    # print(list5)
                    dict6 = self.List_PO.lists2dict(list4, list5)
                    # print(dict6)
                    for k2 in dict6:
                        if k2 == varSubName:
                            self.Web_PO.clickXpathsContain("//a", "href", str(dict6[k2]).replace("http://192.168.0.36:19090/test_ehr_admin/", ""), 1)
            self.Color_PO.consoleColor("31", "36", "[" + varName + "] - [" + varSubName + "]", "")

    def updateDate(self):

        '''获取数据更新截止至时间'''

        l_text = self.Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")
        varDate = l_text[0].split("数据更新截止至时间：")[1].split("\nCopyright")[0]
        print ("数据更新截止至时间：" + varDate)

    def qcAnalysis_dropDownList1(self, varSelectName):

        ''' 档案质控分析 - 档案质控总体情况 - 下拉框选值'''

        self.Color_PO.consoleColor("31", "31", "\n[档案质控总体情况 - 查询 - " + varSelectName + "]", "")
        self.Web_PO.clickXpath("//input[@placeholder='请选择质控时间']", 2)
        l_text2 = self.Web_PO.getXpathsTextPart("//body/div[2]/div/div/ul/li/span", "Copyright © 2019上海智赢健康科技有限公司出品")
        l_text2 = self.List_PO.listSerialNumber(l_text2, 1)
        d_text2 = self.List_PO.list2dictByTuple(l_text2)
        d_text2 = {v: k for k, v in d_text2.items()}
        for k in d_text2:
            if k == varSelectName:
                self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(d_text2[k]) + "]", 2)

        # 显示搜索结果
        l_text = self.Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")
        l_qcOverall = l_text[0].split("重置\n")[1].split("\n本页")[0]
        l_qcOverall = l_qcOverall.split('\n')
        str1 = l_qcOverall.pop(0)
        print(str1)  # '质控时间 质控档案总数量 问题档案数量 规范建档率 操作'
        global list3
        list3 = []
        x = (self.List_PO.listSplitSubList(l_qcOverall, 6))
        for i in x:
            print(i)
            list3.append(i[0])

    def qcAnalysis_dropDownList1_opr(self, varKey, varOpr, varRule="", varPageNum=1):

        ''' 档案质控分析 - 档案质控总体情况 - 操作（详情，规范建档率提升分析）'''

        a = [list3.index(x) for x in list3 if x == varKey][0]
        if varOpr == "规范建档率提升分析":
            self.Color_PO.consoleColor("31", "31", "\n[规范建档率提升分析]", "")
            self.Web_PO.clickXpath("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr[" + str(a + 1) + "]/td[5]/div/div/div[2]/button", 2)  # 点击 记录规范建档率提升分析
            l_text = self.Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
            l_standardAnalysis = l_text[0].split("规范建档率提升分析\n序")[1].split("\n问题档案列表")[0]
            l_standardAnalysis = l_standardAnalysis.split('\n')
            tmp1 = l_standardAnalysis.pop(0)
            print("序" + tmp1)  # '序号 规则类型 问题档案数量(份) 规范建档率提升至'
            x = (self.List_PO.listSplitSubList(l_standardAnalysis, 4))
            x.pop(-1)
            for i in x:
                print(i)
        elif varOpr == "详情":
            # 点击 档案质控总体情况列表中的详情
            self.Web_PO.clickXpath("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr[" + str(a + 1) + "]/td[5]/div/div/div[1]/button", 2)
            if varRule == "":   # 默认不勾选规则类型
                self.Color_PO.consoleColor("31", "31", "\n[问题档案列表]", "")
            else:
                self.Color_PO.consoleColor("31", "31", "\n[问题档案列表 - " + varRule + "]", "")

                self.Web_PO.scrollIntoView("//div[@class='el-checkbox-group']/label[1]", 2)
                l_rule = self.Web_PO.getXpathsText("//div[@class='el-checkbox-group']/label")  # ['规范性 (10.99%)', '完整性 (59.47%)', '有效性 (29.54%)']
                l_rule = self.List_PO.listSerialNumber(l_rule, 1)
                d_rule = self.List_PO.list2dictByTuple(l_rule)
                d_rule = {value: key for key, value in d_rule.items()}

                # 选择规则类型
                varQty = varRule.split(",")
                if len(varQty) == 1:
                    for k in d_rule:
                        if varRule in k:
                            self.Web_PO.clickXpath("//div[@class='el-checkbox-group']/label[" + str(d_rule[k]) + "]", 2)
                else:
                    for i in range(len(varQty)):
                        for k in d_rule:
                            if varQty[i] in k:
                                self.Web_PO.clickXpath("//div[@class='el-checkbox-group']/label[" + str(d_rule[k]) + "]", 2)

            # 前往第几页（默认第一页）
            self.Web_PO.scrollIntoView("//input[@placeholder='请选择']", 2)
            self.Web_PO.inputXpathClearEnter("//div[@class='block']/div[2]/span/div/input", varPageNum)

            l_text = self.Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
            l_problemList = l_text[0].split("问题档案列表\n")[1].split("\n操作")[0]
            l_problemList = l_problemList.split('\n')
            # x = (self.List_PO.listSplitSubList(l_problemList, 5))
            for i in l_problemList:
                print(i)  # ['规则类型:', '规范性 (10.99%)', '完整性 (59.47%)', '有效性 (29.54%)']
            l_problemList = l_text[0].split("错误描述\n")[1].split("\n选择当前页数显示")[0]
            l_problemList = l_problemList.split('\n')
            l_problemList1 = (self.List_PO.listSplitSubList(l_problemList, 8))
            for i in l_problemList1:
                print(i)
            return l_problemList1

    def qcAnalysis_problem_opr(self,varList1, varIdCard):

        ''' 档案质控分析 - 问题档案列表 - 操作（患者身份证）
        获取患者质控项目汇总列表（健康档案封面 和 个人基本信息表）'''

        try:
            for i in range(len(varList1)):
                if varIdCard == varList1[i][1]:
                    varPatient = self.Web_PO.getXpathText("//div[@class='tableEHRss']/div/div/div[" + str(i + 1) + "]/div[3]")
                    self.Web_PO.clickXpath("//div[@class='tableEHRss']/div/div/div[" + str(i + 1) + "]/div[1]/div/span", 2)
                    break
            self.Color_PO.consoleColor("31", "31", "\n[质控项目汇总 - " + str(varIdCard) + "(" + varPatient + ")]", "")
            self.Color_PO.consoleColor("31", "33", "\n[健康档案封面]", "")
            l_text = self.Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
            l_cover = l_text[0].split("健康档案封面\n")[1].split("\n个人基本信息表")[0]
            l_cover = l_cover.split('\n')
            # print(l_cover)
            # 格式化 健康档案封面
            l_cover_format = []
            for i in range(len(l_cover)):
                if i < len(l_cover):
                    if ":" in l_cover[i] and "(" not in l_cover[i + 1]:
                        l_cover_format.append(l_cover[i] + l_cover[i + 1])
                        l_cover.pop(i + 1)
                    else:
                        l_cover_format.append(l_cover[i])
            print(l_cover_format.pop(0))  # 问题数：1
            d_cover_format = self.List_PO.list2dictBySerial(l_cover_format)
            for k in d_cover_format:
                print(k, d_cover_format[k])

            self.Color_PO.consoleColor("31", "33", "\n[个人基本信息表]", "")
            l_basic = l_text[0].split("个人基本信息表\n")[1].split("\n健康档案封面")[0]
            l_basic = l_basic.split('\n')
            # print(l_basic)
            # 格式化 个人基本信息表
            l_basic_format = []
            for i in range(len(l_basic)):
                if i < len(l_basic):
                    if ":" in l_basic[i] and "(" not in l_basic[i + 1]:
                        l_basic_format.append(l_basic[i] + l_basic[i + 1])
                        l_basic.pop(i + 1)
                    else:
                        l_basic_format.append(l_basic[i])
            print(l_basic_format.pop(0))  # 问题数：19
            d_basic_format = self.List_PO.list2dictBySerial(l_basic_format)
            for k in d_basic_format:
                print(k, d_basic_format[k])
        except:
            self.Color_PO.consoleColor("31", "31", "[ERROR]", "身份证号(" + str(varIdCard) + ")有误，请检查！")


    def qcAnalysis_problem_page(self, varPageNum):

        ''' 档案质控分析 - 问题档案列表 - 翻页 '''

        self.Web_PO.scrollIntoView("//input[@placeholder='请选择']", 2)
        self.Web_PO.inputXpathClearEnter("//div[@class='block']/div[2]/span/div/input", varPageNum)




    # def searchField(self, varName):
    #
    #     ''' 查找字段名称,返回找到的数量及字段列表 '''
    #
    #     self.self.Web_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 定位第一下拉框
    #     self.self.Web_PO.clickXpath("//div[@class='el-select-dropdown__wrap el-scrollbar__wrap']/ul/li[1]", 2)  # 选择字段名称
    #     self.self.Web_PO.inputXpath("//input[@placeholder='请输入字段名']", varName)  # 第二输入框输入身高
    #     self.self.Web_PO.clickXpath("//button[@type='button']", 2)  # 点击查找
    #     # 将查找结果保存到列表[字段名称，更新渠道，设置]
    #     l_result = []
    #     varList = self.Web_PO.getXpathsText("//table[@class='el-table__body']")
    #     if varList != "error":
    #         x = str(varList[0])
    #         y = x.replace("编辑 ", "").split("\n")
    #         for i in range(len(y)):
    #             l_result.append(y[i].strip(string.digits))
    #         for i in l_result:
    #             if i == '':
    #                 l_result.remove(i)
    #         # print(l_result)  # ['身高', '预检', '停用']
    #         l_result2 = numpy.array_split(l_result, int(len(l_result) / 3))
    #         return l_result2, int(len(l_result)/3)
    #     else:
    #         exit()
    #
    #     # [4, ['体温', '预检', '停用', '体重', '预检', '停用', '体质指数', '预检', '停用', '体育锻炼', '预检', '停用']]
    #
    # def getAllFieldByChannel(self, varChannel):
    #
    #     ''' 获取某更新渠道下所有字段名称的列表 '''
    #
    #     self.Web_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 定位第一下拉框
    #     self.Web_PO.clickXpath("//div[@class='el-select-dropdown__wrap el-scrollbar__wrap']/ul/li[2]", 2)  # 选择更新渠道
    #     self.Web_PO.clickXpath("//input[@placeholder='请选择更新渠道']", 2)  # 定位第二下拉框
    #     if varChannel == "预检":
    #         self.Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[1]", 2)  # 预检
    #     elif varChannel == "挂号":
    #         self.Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[2]", 2)  # 挂号
    #     elif varChannel == "诊前":
    #         self.Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[3]", 2)  # 诊前
    #     elif varChannel == "门诊":
    #         self.Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[4]", 2)  # 门诊
    #     else:
    #         return []
    #     self.Web_PO.clickXpath("//button[@type='button']", 2)  # 点击查找
    #     # 将所有字段名称保存到列表
    #     l_AllField = []
    #     varList = self.Web_PO.getXpathsText("//table[@class='el-table__body']")
    #     x = str(varList[0])
    #     y = x.replace("\n", "").replace("编辑 启用", "").replace("编辑 停用", "").split(varChannel)
    #     for i in range(len(y) - 1):
    #         l_AllField.append(y[i].strip(string.digits))
    #     # print(l_fieldName)  # ['姓名', '现住址', '户籍地址', '联系电话', '联系人姓名', '联系人电话']
    #
    #     return l_AllField,len(y)-1
    #
    # def getFieldSetupByChannel(self, varChannel):
    #
    #     ''' 获取某更新渠道下所有字段名称、渠道的列表 '''
    #
    #     self.Web_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 定位第一下拉框
    #     self.Web_PO.clickXpath("//div[@class='el-select-dropdown__wrap el-scrollbar__wrap']/ul/li[2]", 2)  # 选择更新渠道
    #     self.Web_PO.clickXpath("//input[@placeholder='请选择更新渠道']", 2)  # 定位第二下拉框
    #     if varChannel == "预检":
    #         self.Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[1]", 2)  # 预检
    #     elif varChannel == "挂号":
    #         self.Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[2]", 2)  # 挂号
    #     elif varChannel == "诊前":
    #         self.Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[3]", 2)  # 诊前
    #     elif varChannel == "门诊":
    #         self.Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[4]", 2)  # 门诊
    #     else:
    #         return []
    #     self.Web_PO.clickXpath("//button[@type='button']", 2)  # 点击查找
    #     list2 = []
    #     varList = self.Web_PO.getXpathsText("//table[@class='el-table__body']")
    #     x = str(varList[0])
    #     z = x.replace("启用\n", "启用??").replace("停用\n", "停用??").replace("\n" + varChannel + "\n编辑", "").split("??")
    #     for i in range(0, len(z)):
    #         remove_digits = str.maketrans('', '', digits)  # 去掉数字编号
    #         d = z[i].translate(remove_digits).replace("\n", "").split(" ")  # 去掉数字编号
    #         list2.append(d[0])
    #         list2.append(d[1])
    #     d_fieldstatus = {}
    #     if len(list2) % 2 == 0:
    #         for i in range(0, len(list2), 2):
    #             d_fieldstatus.update({list2[i]: list2[i + 1]})
    #         # print(d_fieldstatus)  # {'姓名': '启用', '现住址': '启用', '户籍地址': '启用', '联系电话': '启用', '联系人姓名': '启用', '联系人电话': '启用'}
    #     return len(z),d_fieldstatus
    #
    # def updateChannel(self, varChannel, varFieldName, varToChannel, l_FieldName):
    #
    #     ''' # 遍历编辑更新渠道 ，如 将联系电话 的 挂号 改为 诊前 '''
    #
    #     # 先判断 l_FieldName 中是否有 varFieldName
    #     if (varFieldName not in l_FieldName):
    #         print("error，" + str(l_FieldName) + "中没有找到‘" +  str(varFieldName) + "’字段，程序中断！")
    #         exit()
    #
    #     if varChannel == "预检":
    #         if varToChannel == '诊前':
    #             varU = '2'
    #         else:
    #             return []
    #     elif varChannel == "挂号":
    #         if varToChannel == '预检':
    #             varU = '1'
    #         elif varToChannel == '诊前':
    #             varU = '3'
    #         else:
    #             return []
    #     elif varChannel == "诊前":
    #         if varToChannel == '预检':
    #             varU = '1'
    #         else:
    #             return []
    #     elif varChannel == "门诊":
    #         if varToChannel == '预检':
    #             varU = '1'
    #         elif varToChannel == '诊前':
    #             varU = '2'
    #         else:
    #             return []
    #     else:
    #         return []
    #
    #     self.Web_PO.clickXpathsNum("//tr[@class='el-table__row']/td[4]/div/button[1]", l_FieldName.index(varFieldName) + 1, 2)  # 编辑
    #     self.Web_PO.clickXpathsNum("//input[@placeholder='请选择']", 2, 2)  # 定位 更新渠道
    #     self.Web_PO.clickXpath("//body//div[4]/div/div[1]/ul/li[" + varU + "]", 2)  # 选择 诊前
    #     self.Web_PO.clickXpathsNum("//tr[@class='el-table__row']/td[4]/div/button[2]", l_FieldName.index(varFieldName) + 1, 2)  # 保存
    #
    #     # 检查更新渠道转移后是否更新成功，如将 联系电话 转移到 诊前
    #     self.Web_PO.clickXpath("//input[@placeholder='请选择更新渠道']", 2)  # 定位第二下拉框
    #     if varToChannel == "预检":
    #         varU1 = '1'
    #     elif varToChannel == "挂号":
    #         varU1 = '2'
    #     elif varToChannel == "诊前":
    #         varU1 = '3'
    #     elif varToChannel == "门诊":
    #         varU1 = '4'
    #     self.Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[" + varU1 + "]", 2)  # 选择 更新渠道
    #     self.Web_PO.clickXpath("//button[@type='button']", 2)  # 点击查找
    #
    #     # # 遍历所有诊前字段名称保存到列表
    #     l_fieldname = []
    #     varList = self.Web_PO.getXpathsText("//table[@class='el-table__body']")
    #     x = str(varList[0])
    #     y = x.replace("\n", "").replace("编辑 启用", "").replace("编辑 停用", "").split(varToChannel)
    #     for i in range(len(y) - 1):
    #         l_fieldname.append(y[i].strip(string.digits))
    #     # print(l_fieldname)  # ['姓名', '现住址', '户籍地址', '联系电话', '联系人姓名', '联系人电话']
    #     return l_fieldname
    #
    # def getAllFieldStatus(self, varChannel):
    #
    #     ''' 将某个更新渠道中所有字段及状态（启用或停用）保存到字典 ，如 {'姓名': '启用', '现住址': '启用'}'''
    #
    #     list2 = []
    #     varList = self.Web_PO.getXpathsText("//table[@class='el-table__body']")
    #     x = str(varList[0])
    #     z = x.replace("启用\n", "启用??").replace("停用\n", "停用??").replace("\n" + varChannel + "\n编辑", "").split("??")
    #     for i in range(0, len(z)):
    #         remove_digits = str.maketrans('', '', digits)     # 去掉数字编号
    #         d = z[i].translate(remove_digits).replace("\n", "").split(" ")   # 去掉数字编号
    #         list2.append(d[0])
    #         list2.append(d[1])
    #     d_AllFieldStatus = {}
    #     if len(list2) % 2 == 0:
    #         for i in range(0, len(list2), 2):
    #             d_AllFieldStatus.update({list2[i]:list2[i+1]})
    #         return (d_AllFieldStatus)   # {'姓名': '启用', '现住址': '启用', '户籍地址': '启用', '联系电话': '启用', '联系人姓名': '启用', '联系人电话': '启用'}
    #     else:
    #         exit()
    #
    # def setSingleFieldStatus(self, d_AllFieldStatus,varFieldName,varStatus,l_fieldName):
    #
    #     ''' 遍历所有字段，对指定字段设置启用或停用'''
    #     # DataMonitor_PO.setSingleFieldStatus(d_AllFieldStatus, "户籍地址", "停用", l_AllField)
    #     for key in d_AllFieldStatus:
    #         if key == varFieldName and d_AllFieldStatus[key] != varStatus:
    #             self.Web_PO.clickXpathsNum("//tr[@class='el-table__row']/td[4]/div/button[2]", l_fieldName.index(varFieldName) + 1, 2)
    #
    #     print("[OK] 已" + varStatus + varFieldName)
    #
    # def setAllFieldStatus(self, varStatus):
    #
    #     ''' 遍历所有字段，设置所有字段全部 启用或停用'''
    #     # DataMonitor_PO.setAllFieldStatus("启用")
    #     x = self.Web_PO.getXpathsText("//tr[@class='el-table__row']/td[4]/div/button[2]/span")
    #     for i in range(len(x)):
    #         if x[i] != varStatus:
    #             self.Web_PO.clickXpathsNum("//tr[@class='el-table__row']/td[4]/div/button[2]", i+1, 2)
    #     print("[OK] 已" + varStatus + "所有字段")
    #
    # def ruleManage_getRuleList(self):
    #
    #     ''' 规则管理 - 获取规则列表（包括编号、规则名称、状态）'''
    #     l_rule = []
    #     l_tmp = self.Web_PO.getXpathsText("//tr")
    #     l_tmp = [''.join([i.strip() for i in price.strip().replace("\n", ", ")]) for price in l_tmp]
    #     for i in range(len(l_tmp)):
    #         if l_tmp[i] != '操作' and l_tmp[i] != '编辑停用' and l_tmp[i] != '编辑使用' and l_tmp[i] != '编号规则名称':
    #             l_rule.append(l_tmp[i])
    #     # print(l_rule)
    #     l_status = self.Web_PO.getXpathsText("//div[@class='el-table__fixed-body-wrapper']/table/tbody/tr")
    #     l_status = [''.join([i.strip() for i in price.strip().replace("编辑", "")]) for price in l_status]
    #     # print(l_status)
    #     l_merge = []
    #     for i in range(len(l_rule)):
    #         x = str(l_status[i]) + " => " + str(l_rule[i])
    #         l_merge.append(x)
    #         x = ""
    #     return(l_merge)
    #
    # def user_printList(self,varPage):
    #
    #     ''' 用户管理 - 输出某一页的用户列表（包括编号、用户名、昵称、手机、用户类型、是否医院人员、所属社区）'''
    #     self.Web_PO.script('document.querySelector("input[type=number]").value="";', 2)  # js方式清空输入框
    #     self.Web_PO.inputXpathClearEnter("//input[@type='number']", varPage)
    #     l_user = []
    #     l_tmp = []
    #     l_tmp = self.Web_PO.getXpathsText("//tr")
    #     l_tmp = [''.join([i.strip() for i in price.strip().replace("\n", ", ")]) for price in l_tmp]
    #     varPage = str(varPage) + " - "
    #     for i in range(len(l_tmp)):
    #         if l_tmp[i] != '编号用户名昵称手机用户类型是否医院人员所属社区' and l_tmp[i] != '操作' and l_tmp[i] != '角色编辑删除':
    #             c = varPage + l_tmp[i]
    #             l_user.append(c)
    #
    #     for i in range(len(l_user)):
    #         print(l_user[i])
    # def user_addUser(self,varUserName,varNickName,varPhone,varType,varIsThird,varCommunity):
    #
    #     '''用户管理 - 新增用户'''
    #
    #     self.Web_PO.clickXpath("//button[@class='el-button el-button--success el-button--mini']", 2)  # 点击 新增
    #     self.Web_PO.inputXpath("//input[@placeholder='用户名']", varUserName)  # 用户名不能重复，且不能是中文
    #     self.Web_PO.inputXpath("//input[@placeholder='昵称']", varNickName)
    #     self.Web_PO.inputXpath("//input[@placeholder='手机']", varPhone)
    #     self.Web_PO.clickXpath("//td[@class='el-table_1_column_5  ']/div/div/div/div/input", 2)  # 选择 建档专员或医生
    #     if varType == "建档专员":
    #         self.Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[1]", 2)  # 选择建档专员
    #     else:
    #         self.Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[2]", 2)  # 选择医生
    #     self.Web_PO.clickXpath("//td[@class='el-table_1_column_6  ']/div/div/div/div/input", 2)  # 选择 是否医院人员
    #     if varIsThird == "否":
    #         self.Web_PO.clickXpath("//body/div[3]/div[1]/div[1]/ul/li[1]", 2)  # 选择 否
    #     else:
    #         self.Web_PO.clickXpath("//body/div[3]/div[1]/div[1]/ul/li[2]", 2)  # 选择 是
    #     self.Web_PO.clickXpath("//td[@class='el-table_1_column_7  ']/div/div/div/div/input", 2)  # 选择 所属社区
    #
    #     x = self.Web_PO.getXpathsText("//body/div[4]/div[1]/div[1]/ul/li")  # 遍历社区
    #     for i in range(len(x)):
    #         if x[i] == varCommunity:
    #             self.Web_PO.clickXpath("//body/div[4]/div[1]/div[1]/ul/li[" + str(i+1) + "]", 2)  # 选择所属社区
    #
    #     self.Web_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/button[2]", 2)  # 保存

    def user_searchUser(self, varType, varValue):

        ''' 用户管理 - 搜索用户名、昵称、手机号
         返回：搜索列表'''

        if varType == '*':
            pass
        else:
            self.Web_PO.clickXpath("//form[@class='el-form login-form el-form--inline']/div[1]/div/div/div/div/div/input", 2)   # 请选择
            if varType == '用户名':
                self.Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[1]", 2)  # 用户名
            elif varType == '昵称':
                self.Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[2]", 2)  # 昵称
            elif varType == '手机':
                self.Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[3]", 2)  # 手机
            else:
                exit()
            self.Web_PO.inputXpathClear("//input[@placeholder='请输入搜索内容']", varValue)

        self.Web_PO.clickXpath("//form[@class='el-form login-form el-form--inline']/div[2]/div/button[1]", 2)  # 点击查找
        tmpList = self.Web_PO.getXpathsText("//tr")
        tmpList.pop(0)
        tmpList1 = self.List_PO.listReplace(tmpList, "操作", "")
        tmpList2 = self.List_PO.listReplace(tmpList1, "角色 编辑 删除", "")
        tmpList3 = self.List_PO.listReplace(tmpList2, "\n", ",")

        return tmpList3

    # def user_operateRole(self, varType, varUserName, *t_role):
    #
    #     '''用户管理 - 操作角色'''
    #
    #     self.user_searchUser(varType, varUserName)
    #     self.Web_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/button[1]", 2)  # 点击 角色
    #     self.Web_PO.clickXpath("//div[@class='el-select__tags']/input", 2)  # 选择角色
    #     x = self.Web_PO.getXpathsText("//div[@class='el-select-dropdown el-popper is-multiple']/div/div/ul/li")
    #     print(x)
    #     self.Web_PO.clickXpaths("//i[@class='el-tag__close el-icon-close']", 2)
    #     if len(t_role) == 1:
    #         for i in range(len(x)):
    #             if x[i] == t_role[0]:
    #                 self.Web_PO.clickXpath("//div[@class='el-select-dropdown el-popper is-multiple']/div/div/ul/li[" + str(i+1) + "]", 2)  # 选择 角色
    #     else:
    #         for j in range(len(t_role)):
    #             for i in range(len(x)):
    #                 if x[i] == t_role[j]:
    #                     self.Web_PO.clickXpath("//div[@class='el-select-dropdown el-popper is-multiple']/div/div/ul/li[" + str(i + 1) + "]", 2)  # 选择 角色
    #
    #     self.Web_PO.clickXpath("//div[@class='el-dialog__footer']/span/button[3]", 2)  # 确认
    # def user_operateEdit(self, varType, varUserName, varNewUserName, varNickName, varPhone, varType2, varIsThird, varCommunity):
    #
    #     '''用户管理 - 搜索用户名，操作编辑第一条记录'''
    #
    #     self.user_searchUser(varType, varUserName)
    #     self.Web_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/button[2]", 2)  # 点击 编辑
    #     self.Web_PO.inputXpathClear("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr/td[2]/div/div/div/input", varNewUserName)
    #     self.Web_PO.inputXpathClear("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr/td[3]/div/div/div/input", varNickName)
    #     self.Web_PO.inputXpathClear("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr/td[4]/div/div/div/input", varPhone)
    #     self.Web_PO.clickXpath("//td[@class='el-table_1_column_5  ']/div/div/div/div/input", 2)  # 选择 建档专员或医生
    #     if varType2 == "建档专员":
    #         self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[1]", 2)  # 选择建档专员
    #     else:
    #         self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[2]", 2)  # 选择医生
    #     self.Web_PO.clickXpath("//td[@class='el-table_1_column_6  ']/div/div/div/div/input", 2)  # 选择 是否医院人员
    #     if varIsThird == "否":
    #         self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[1]", 2)  # 选择 否
    #     else:
    #         self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[2]", 2)  # 选择 是
    #     self.Web_PO.clickXpath("//td[@class='el-table_1_column_7  ']/div/div/div/div/input", 2)  # 选择 所属社区
    #
    #     # x = self.Web_PO.getXpathsText("//body/div[5]/div[1]/div[1]/ul/li")
    #     x = self.Web_PO.getXpathsText("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li")
    #     # 遍历社区
    #     for i in range(len(x)):
    #         if x[i] == varCommunity:
    #             self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[" + str(i + 1) + "]", 2)  # 选择所属社区
    #
    #     self.Web_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/button[2]", 2)  # 保存
    # def user_operateDel(self, varType, varUserName):
    #
    #     '''用户管理 - 操作删除'''
    #     self.user_searchUser(varType, varUserName)
    #     try:
    #         self.Web_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/button[3]", 2)  # 点击 删除
    #         self.Web_PO.clickXpath("//div[@class='el-message-box']/div[3]/button[2]", 2)  # 二次确定。
    #     except:
    #         exit()
    #
    # def permission_printList(self, varPage):
    #
    #     ''' 权限管理 - 输出某一页的权限列表（包括编号、菜单名称、权限值、路径、是否显示、模块、状态、图标、所属系统、所属上级）'''
    #     self.Web_PO.script('document.querySelector("input[type=number]").value="";', 2)  # js方式清空输入框
    #     self.Web_PO.inputXpathClearEnter("//input[@type='number']", varPage)
    #     l_permission = []
    #     l_tmp = []
    #     l_tmp = self.Web_PO.getXpathsText("//tr")
    #     l_tmp = [''.join([i.strip() for i in price.strip().replace("\n", ", ")]) for price in l_tmp]
    #     varPage = str(varPage) + " - "
    #     for i in range(len(l_tmp)):
    #         if l_tmp[i] != '编号菜单名称权限值路径是否显示模块状态图标所属系统所属上级' and l_tmp[i] != '编辑删除' and l_tmp[i] != '操作':
    #             c = varPage + l_tmp[i]
    #             l_permission.append(c)
    #     for i in range(len(l_permission)):
    #         print(l_permission[i])
    #     print("\n")
    #
    # def permission_addMenu(self, varMenu, varPower, varPath, varIsShow, varModel, varStatus, varIcon, varSystem, varLead):
    #
    #     '''权限管理 - 新增菜单'''
    #
    #     self.Web_PO.clickXpath("//button[@class='el-button el-button--success el-button--mini']", 2)  # 点击 新增
    #     self.Web_PO.inputXpath("//input[@placeholder='菜单名称']", varMenu)  # 用户名不能重复，且不能是中文
    #     self.Web_PO.inputXpath("//input[@placeholder='权限值']", varPower)
    #     self.Web_PO.inputXpath("//input[@placeholder='路径']", varPath)
    #
    #     self.Web_PO.clickXpath("//td[@class='el-table_1_column_5  ']/div/div/div/div/input", 2)  # 选择 是否显示
    #     if varIsShow == "展示":
    #         self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[1]", 2)  # 选择 展示
    #     else:
    #         self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[2]", 2)  # 选择 隐藏
    #
    #     self.Web_PO.inputXpath("//input[@placeholder='模块']", varModel)
    #
    #     self.Web_PO.clickXpath("//td[@class='el-table_1_column_7  ']/div/div/div/div/input", 2)  # 选择 状态
    #     if varStatus == "禁止":
    #         self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[1]", 2)  # 选择 禁止
    #     else:
    #         self.Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[2]", 2)  # 选择 正常
    #
    #     self.Web_PO.inputXpath("//input[@placeholder='图标']", varIcon)
    #     self.Web_PO.inputXpath("//input[@placeholder='所属系统']", varSystem)
    #     self.Web_PO.inputXpathClear("//input[@placeholder='所属上级']", varLead)
    #     self.Web_PO.clickXpath("//td[@class='el-table_1_column_11 is-center ']/div/button[2]", 2)  # 保存