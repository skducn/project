# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: 白茅岭对象库
# *****************************************************************

from PO.webdriverPO import *
from instance.zyjk.PIM.config.config import *
from selenium.webdriver.common.action_chains import ActionChains

webdriver_PO = WebdriverPO("chrome")
webdriver_PO.open(varURL)
webdriver_PO.driver.maximize_window()  # 全屏
Level_PO = LevelPO(webdriver_PO.driver)

import string,numpy
from string import digits

class PimPO(object):

    def __init__(self):
        self.Level_PO = Level_PO

    # 登录
    def login(self, varUser):

        ''' 登录 '''

        self.Level_PO.inputXpath("//input[@placeholder='请输入用户名']", varUser)
        sleep(3)
        self.Level_PO.inputXpath("//input[@placeholder='请输入密码']", "123456")
        sleep(3)
        self.Level_PO.clickXpath("//button[@type='button']", 7)

    # 主菜单
    def leftMenu(self, varFirstMenuName):

        ''' 切换主菜单'''

        l_menu = Level_PO.getXpathsText("//div[@class='el-scrollbar__view']/ul/li/div/span")
        # print(l_menu)
        for i in range(len(l_menu)):
            if l_menu[i] == varFirstMenuName:
                Level_PO.clickXpath("//div[@class='el-scrollbar__view']/ul/li[" + str(i+1) +"]/div/span", 2)

    # 模块菜单
    def modelMenu(self, varMeneName):

        ''' 模块菜单'''

        l_modelMenu = Level_PO.getXpathsText("//div[@class='clearfix btn_header']/ul/li")
        # print(l_modelMenu)
        for i in range(len(l_modelMenu)):
            if varMeneName in l_modelMenu[i]:
                Level_PO.clickXpath("//div[@class='clearfix btn_header']/ul/li[" + str(i + 1) + "]", 2)

    # 患者挂号
    def registration(self, varAdmin, varPatient):
        # 收费管理员给患者进行挂号操作。
        self.login(varAdmin)  # s001 收费管理员1
        self.leftMenu("挂号收费")
        Level_PO.clickLinkstext("门诊挂号管理", 2)
        Level_PO.clickXpath("//div[@aria-label='请核对']/div[3]/span/button", 2)  # 请核对 - 确定
        Level_PO.inputXpathEnter("//input[@placeholder='姓名/手机/电话/身份证']", varPatient)  # 患者信息
        Level_PO.clickXpath("//div[@aria-label='患者信息列表']/div[3]/span/button[2]", 2)  # 患者信息列表 - 确定
        Level_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 挂号代码
        varInputCode = Level_PO.getXpathText("//li[@class='el-select-dropdown__item']/div/p[1]")  # 获取输入码
        # print(varInputCode)  # nkmzpz
        Level_PO.clickXpath("//li[@class='el-select-dropdown__item']/div/p[1]", 2)  # 自动选择未使用的挂号代码
        l_modelMenu = Level_PO.getXpathsText("//ul[@class='clearfix topContentUl']/li")
        for i in range(len(l_modelMenu)):
            if "结算" in l_modelMenu[i]:
                Level_PO.clickXpath("//ul[@class='clearfix topContentUl']/li[" + str(i+1) + "]", 4)   # 点击菜单结算
                break
        Level_PO.clickXpath("//div[@aria-label='挂号唱票']/div[3]/span/button", 6)  # 结算
        Level_PO.clickXpathEnter("//div[@aria-label='发票二次确认']/div[3]/span/button[1]", 2)  # 发票二次确认 - 确认
        Level_PO.clickXpath("//i[@class='el-icon-caret-bottom']", 2)  # 点击右上角账号
        Level_PO.clickXpath("//ul[@class='el-dropdown-menu el-popper avatar-container-dropdown']/li[6]/span", 2)  # 退出登录
        print("[done] " + varAdmin + "对患者‘" + varPatient + "’进行挂号操作")
        return varInputCode

    # 医生给患者开处方药
    def prescribe(self,varDoctor, varPatient, varInputCode):
        # 医生就诊开处方
        self.login(varDoctor)  # d001 测试医生1
        self.leftMenu("诊间就诊")
        Level_PO.clickLinkstext("门诊患者列表", 2)
        if "nkmz" not in varInputCode:
            Level_PO.clickXpath("//div[@class='searchWarp']/ul/li[2]", 2)  # 点击门诊科室
            if "wkmz" in varInputCode:
                Level_PO.clickXpath(
                    "//div[@class='el-select-dropdown el-popper select_component PT_component']/div[1]/div[1]/ul/li[2]/div/p[1]",
                    2)
            elif "kqmz" in varInputCode:
                Level_PO.clickXpath(
                    "//div[@class='el-select-dropdown el-popper select_component PT_component']/div[1]/div[1]/ul/li[3]/div/p[1]",
                    2)
            elif "zymz" in varInputCode:
                Level_PO.clickXpath(
                    "//div[@class='el-select-dropdown el-popper select_component PT_component']/div[1]/div[1]/ul/li[4]/div/p[1]",
                    2)
        l_patientName = Level_PO.getXpathsText("//td[@class='el-table_1_column_6 is-center  ']/div")  # 患者姓名
        l_patientRegType = Level_PO.getXpathsText("//td[@class='el-table_1_column_8 is-center  ']/div")  # 患者挂号类型
        l_zhuhe = [i + j for i, j in zip(l_patientName, l_patientRegType)]  # ['张洪瑞平诊', '张华卿急诊', '张洪瑞急诊', '张凯旋急诊']
        # print(l_zhuhe)
        if "jz" in varInputCode:
            varType = "急诊"
        else:
            varType = "平诊"
        l_zhuhe2 = varPatient + varType
        aa = l_zhuhe.index(l_zhuhe2)
        # print(aa)
        Level_PO.clickXpathsNum("//tr[@class='el-table__row']/td[2]/div", aa+1, 2)  # 选择指定的患者（依据 患者姓名+挂号类别）
        # Level_PO.clickXpathsNum("//td[@class='el-table_1_column_10 is-center  cellColorVisit']/div", aa+1,2)  # 选择指定的患者（依据 患者姓名+挂号类别）

        l_modelMenu = Level_PO.getXpathsText("//ul[@class='clearfix OutpationListUl']/li")
        for i in range(len(l_modelMenu)):
            if "开始就诊" in l_modelMenu[i]:
                Level_PO.clickXpath("//ul[@class='clearfix OutpationListUl']/li[" + str(i + 1) + "]", 2)
                break
        Level_PO.inIframe("ueditor_0", 2)
        Level_PO.clickXpath("//body/p[6]/span/span/span", 2)  # 点击 门诊诊断
        Level_PO.outIframe(2)
        Level_PO.clickXpath("//div[@class='el-table__fixed-header-wrapper']/table/thead/tr/th[5]/div/button",
                            2)  # 诊断录入 - 添加
        Level_PO.clickXpath("//input[@placeholder='请输入关键词']", 2)  # 点击 诊断名称
        Level_PO.inputXpath("//input[@placeholder='请输入关键词']", "1")  # 输入 1
        Level_PO.clickXpath("//body/div[13]/div[1]/div[1]/ul/li[1]/div/p[1]", 2)  # 默认选择第一个诊断名称，如 结核性脑膜炎。
        Level_PO.clickXpath("//div[@class='el-table__fixed-body-wrapper']/table/tbody/tr/td[5]/div/div/span[1]",
                            2)  # 保存
        Level_PO.clickXpath("//button[@class='el-button initBtn el-button--primary el-button--small']", 2)  # 保存
        l_modelMenu = Level_PO.getXpathsText("//ul[@class='clearfix']/li")
        # print(l_modelMenu)
        for i in range(len(l_modelMenu)):
            if "处方" in l_modelMenu[i]:
                Level_PO.clickXpath("//ul[@class='clearfix']/li[" + str(i + 1) + "]", 2)
                break
        l_modelMenu = Level_PO.getXpathsText("//div[@class='OP_cinfo clearfix']/div/div/ul/li")
        for i in range(len(l_modelMenu)):
            if "添加处方" in l_modelMenu[i]:
                Level_PO.clickXpath("//div[@class='OP_cinfo clearfix']/div/div/ul/li[" + str(i + 1) + "]", 2)
                break
        Level_PO.clickXpath("//div[@class='el-dialog__body']/form/div[2]/div/div/div[2]/input", 2)  # 处方诊断
        Level_PO.clickXpath("//div[@class='el-select-dropdown el-popper is-multiple']/div[1]/div[1]/ul/li",
                            2)  # 选择 结核性脑膜炎
        Level_PO.clickXpathEnter("//div[@aria-label='处方属性']/div[3]/span/button", 2)  # 处方属性 - 保存
        Level_PO.clickXpath("//input[@placeholder='名称/代码/输入码']", 2)  # 点击名称
        Level_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[4]/div/p[1]", 2)  # 选择 急支糖浆
        # Level_PO.clickXpath("//li[@class='el-select-dropdown__item']/div/p[1]", 2)  # 自动获取未使用的种类
        Level_PO.inputXpath("//tr[@class='el-table__row']/td[7]/div/div/div/div[1]/input", "2")  # 用量
        Level_PO.inputXpath("//tr[@class='el-table__row']/td[8]/div/div/div/div[1]/input", "3")  # 数量
        Level_PO.clickXpath("//tr[@class='el-table__row']/td[9]/div/div/div/div[1]/div[1]/input", 2)  # 途径
        Level_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[3]", 2)  # 选择 嚼服
        Level_PO.clickXpath("//tr[@class='el-table__row']/td[10]/div/div/div/div[1]/div[1]/input", 2)  # 频次
        Level_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[3]", 2)  # 选择 bid
        Level_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[18]/div/span[3]", 2)  # 保存
        for i in range(len(l_modelMenu)):
            if "保存全部" in l_modelMenu[i]:
                Level_PO.clickXpath("//div[@class='OP_cinfo clearfix']/div/div/ul/li[" + str(i + 1) + "]", 2)
                break
        Level_PO.clickXpath("//i[@class='el-icon-caret-bottom']", 2)  # 点击右上角账号
        Level_PO.clickXpath("//ul[@class='el-dropdown-menu el-popper avatar-container-dropdown']/li[6]/span", 2)  # 退出登录
        print("[done] " + varDoctor + "对患者‘" + varPatient + "’进行就诊开处方操作")

    # 患者结账
    def charge(self, varAdmin, varPatient):
        # 收费管理员给患者收费结算
        self.login(varAdmin)  # s001收费管理员 登录
        self.leftMenu("挂号收费")
        Level_PO.clickLinkstext("门诊收费管理", 2)
        Level_PO.clickXpath("//div[@aria-label='请核对']/div[3]/span/button", 2)  # 请核对 - 确定
        Level_PO.inputXpathEnter("//input[@placeholder='姓名/手机/电话/身份证']", varPatient)  # 患者信息
        Level_PO.clickXpath("//div[@aria-label='患者信息列表']/div[3]/span/button", 2)  # 患者信息列表 - 确定
        l_modelMenu = Level_PO.getXpathsText("//div[@class='clearfix topContent']/ul/li")
        for i in range(len(l_modelMenu)):
            if "结算" in l_modelMenu[i]:
                Level_PO.clickXpath("//div[@class='clearfix topContent']/ul/li[" + str(i + 1) + "]", 4)  # 点击菜单结算
                break
        Level_PO.clickXpath("//div[@aria-label='收费唱票']/div[3]/span/button", 6)  # 结算
        Level_PO.clickXpathEnter("//div[@aria-label='发票确认']/div[3]/span/button[1]", 2)  # 发票确认 - 确认
        Level_PO.clickXpath("//i[@class='el-icon-caret-bottom']", 2)  # 点击右上角账号
        Level_PO.clickXpath("//ul[@class='el-dropdown-menu el-popper avatar-container-dropdown']/li[6]/span", 2)  # 退出登录
        print("[done] " + varAdmin + "对患者‘" + varPatient + "’进行费用结账")

    # 门诊配发药
    def peifayao(self, varDrugstore):
        # 测试药房给患者进行门诊配发药
        self.login(varDrugstore)  # y001测试药房1
        self.leftMenu("门诊配发药")
        Level_PO.clickLinkstext("门诊配发药管理", 2)
        # print("门诊配发药 - 门诊配发药管理")
        varWinSum = Level_PO.getXpathsNums("//div[@class='el-table__fixed-body-wrapper']/table/tbody/tr")
        # print("门诊配发药窗口数：" + str(varWinSum))
        l_sum = Level_PO.getXpathsText("//div[@class='printWrap clearfix']/span/span")
        # print("待发数：" + str(l_sum[0]) + " , 已发数：" + str(l_sum[1]))
        # c1，检查已发数，默认翌日依法数量已发数为0
        if int(l_sum[1]) != 0:
            print("[warning] c1,已发数不为0！")
            print("c1,已发数：" + str(l_sum[1]))
        else:
            print("[ok] c1,已发数为0")
        # c2，检查门诊配发药窗口数与待发数量是否一致
        # 备注：门诊配发药窗口数来自 门诊收费 （小寒测试提供门诊收费数量）
        if int(varWinSum) != int(l_sum[0]):
            print("[errorrrrrrrrrrr] c2,门诊配发药窗口数与待发数量不一致，门诊配发药窗口数：" + str(varWinSum) + " , 待发数：" + str(l_sum[0]))
        else:
            print("[ok] c2,门诊配发药窗口数与待发数量一致")

        # c3，检查门诊配发药窗口中每个处方号是否有可用配发药数量
        # 规则：number - previewnumber + 规则*后数量
        # 药品_门诊发药明细表 t_ph_outpatient_dispensing_detail

        # c4，检查患者药品名称的处方药品数量、单价、金额、总计。
        varEmpty = varCount = varSum = varMoney = varTotal = 0
        l_recipeId = Level_PO.getXpathsText("//div[@class='el-table__body-wrapper is-scrolling-left']/table/tbody/tr/td[4]/div")
        # print(l_recipeId) # ['4323', '4322', '4321', '4218', '4314', '4307', '4308', '4310', '4292', '4294', '4295', '4291', '4290', '4289', '4288', '4287', '4286']
        for i in range(len(l_recipeId)):
            l_drugIdSpec = sqlserver_PO.ExecQuery('select drugId,drugName,spec,number,packUnit,price,amount from t_ph_outpatient_dispensing_detail where recipeId=%s ' % (l_recipeId[i]))
            # l_drugIdSpec = sqlserver_PO.ExecQuery('select drugId,spec,recipeId,price,number from t_ph_outpatient_dispensing_detail where recipeId=%s ' % (l_recipeId[i]))
            # print(l_drugIdSpec)   # 记录数列表, 如 [(225, '急支糖浆', '200ml/瓶*1/瓶', 3, '瓶', Decimal('18.0000'), Decimal('54.0000'))]
            for j in range(len(l_drugIdSpec)):
                # print(l_drugIdSpec[j][0])  # drugId ， 如 225
                # print(l_drugIdSpec[j][1])  # drugName , 如 急支糖浆
                # print(l_drugIdSpec[j][2])  # spec ， 如 50mg/片*24/瓶
                # print(l_drugIdSpec[j][3])  # number ,如 3
                # print(l_drugIdSpec[j][4])  # packUnit ， 瓶
                # print(l_drugIdSpec[j][5])  # price , 18
                # print(l_drugIdSpec[j][6])  # amount ， 54
                l_drugCount = sqlserver_PO.ExecQuery('select number,previewNumber from t_ph_outpatient_drug_info where drugId=%s ' % (l_drugIdSpec[j][0]))
                if "*" in str(l_drugIdSpec[j][2]):
                    x = str(l_drugIdSpec[j][2]).split("*")
                    x = x[1].split("/")
                    varEmpty = int(x[0])
                    varCount = int(l_drugCount[0][0]) - int(l_drugCount[0][1]) + varEmpty  # number - previewNumber + 24
                    # print(str(l_drugCount[0][0]) + " - " + str(l_drugCount[0][1]) + " + " + str(varEmpty))
                else:
                    varCount = int(l_drugCount[0][0]) - int(l_drugCount[0][1]) + 1
                    # print(str(l_drugCount[0][0]) + " - " + str(l_drugCount[0][1]) + " + 1")
                # print(varCount)
                varSum = varCount + varSum  # 某一个处方号下可配发药数量合计
                # varMoney = l_drugIdSpec[j][3] * int(l_drugIdSpec[j][5])  #  处方药品数量 * 单价
                varTotal = varTotal + l_drugIdSpec[j][6]
            # print("处方号(" + str(l_drugIdSpec[0][2]) + ")的可配发药数：" + str(varSum) + "， 金额：" + str(l_drugIdSpec[j][6]) + " , 总计：" + str(varTotal))
            print("处方号 " + str(l_recipeId[i]) + " 的可配发药数：" + str(varSum) + " => " + str(
                l_drugIdSpec[j][1]) + " , " + str(l_drugIdSpec[j][2]) + " , " + str(l_drugIdSpec[j][3]) + " , " + str(
                l_drugIdSpec[j][4]) + " , " + str(round(l_drugIdSpec[j][5], 2)) + " , " + str(
                round(l_drugIdSpec[j][6], 2)) + ", 总计：" + str(round(varTotal, 2)))
            # print("********************************************")
            varSum = 0
            varTotal = 0
        print("[done] " + varDrugstore + "门诊配发药管理核对窗口数、待发数、已发数、所有处方可配发药数、金额、总计")

    # 医嘱录入
    def doctorAdvice(self,varTest123, varBedNo):
        self.login(varTest123)  # test123
        self.leftMenu("住院医生工作站")
        Level_PO.clickLinkstext("病区一览", 2)
        Level_PO.inputXpathEnter("//input[@placeholder='床位号/姓名/就诊卡号']", varBedNo)  # 搜索1-07
        sleep(6)
        Level_PO.clickXpath("//button[@class='el-button el-button--primary el-button--medium']", 4)  # 查询
        Level_PO.floatXpath("//div[@class='wl_card_content_top']", "//div[@class='wl_card_content']/div[2]/button[1]", 4)  # 医嘱录入
        Level_PO.clickXpath("//div[@class='switch_three clearfix overHi']/ul/button[1]", 2)  # 添加
        Level_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[1]", 2)  # 长期
        Level_PO.inputXpathEnter("//span[@class='idPopoverTrue']/div/input", "维生素b1片")  # 名称
        Level_PO.inputXpath("//tr[@class='el-table__row current-row']/td[7]/div/div/div/div[1]/input", "5")  # 用量
        # Level_PO.inputXpath("//input[@name='dosageInput']", "3")  # 用量
        Level_PO.clickXpath("//tr[@class='el-table__row']/td[10]/div/div/div/div[1]/div/input", 2)  # 途径
        Level_PO.clickXpath("//div[@x-placement='top-start']/div[1]/div[1]/ul/li[2]", 2)  # 嚼服
        Level_PO.clickXpath("//div[@x-placement='top-start']/div[1]/div[1]/ul/li[2]", 2)  # bid

