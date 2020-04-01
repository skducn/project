# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-7-9
# Description: 特殊药品流向登记
# usage: python drugFlowRegistere.py 经营企业
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PageObject.ShouyingPO import *

if len(sys.argv) != 2:
    print u"功能：特色药品流向登记 \n" \
           u"语法：python " + str(sys.argv[0]).split(".")[0] + u".py 经营企业\n" \
           u"例子：python " + str(sys.argv[0]).split(".")[0] + u".py 14516109052  \n"
else:

    from Public.webdriver import *
    Level_PO = LevelPO(Webdriver())
    Shouying_PO = ShouyingPO(Level_PO)

    # main =============================================================================================================

    try:
        Level_PO.openURL(varURLfront, 1)
        Shouying_PO.login(sys.argv[1], "q123456")
    except:printColor('\033[1;31;47m', 'printRed', "errorrrrrrrrrr, " + str(sys._getframe().f_lineno) + " row from " + str(__file__));os._exit(0)

    Level_PO.clickLinktext(u"特殊药品出入库管理", 2)
    Level_PO.clickLinktext(u"特殊药品流向登记", 2)
    # Level_PO.clickXpath("//button[@id='close-message-box']", 2)  # 关闭站内信弹框窗口
    # 大宗交易情况月报表
    Level_PO.clickLinktext(u"上传数据", 2)
    Level_PO.inputNameClear("yearMonth", u"2018-04")  # 报表月份
    Level_PO.clickXpath("settingSfdaBtn", 2)  # 设置
    Level_PO.selectXpathText(u"//div[@id='next-level-bar']/select[3]", u'成华区')
    Level_PO.selectXpathText(u"//div[@id='next-level-bar']/select[4]", u'龙潭街道市场和质量监督管理所')
    Level_PO.clickId("saveSfdaBtn", 2)  # 保存
    Level_PO.sendKeysName_mac("descriptionFile", varJpg)
    Level_PO.clickXpath("//button[@onclick='doOpenAddRecordForm()']", 2)  # 记录录入
    # 记录录入
    Level_PO.inputName("authenticationCode", "12345678") # 批准文号
    Level_PO.inputName("spec", "1000ml")  # 规格
    Level_PO.inputName("factoryName", u"上海长江")  # 生产厂家
    Level_PO.inputName("saleTo", u"小王单位")  # 销往单位
    Level_PO.inputName("authenticationCode", "12345678")  # 批准文号
    Level_PO.inputXpath("//input[@name='saleDate']", u"2018-04-12")  # 销售日期
    Level_PO.inputName("saleAmount", "12")  # 销售数量
    Level_PO.inputName("saleBillNo", "12345678")  # 销售单据号
    Level_PO.inputName("name", u"阿司匹林胶囊")  # 品种名称
    Level_PO.inputName("subAmount", "2")  # 每件装量
    Level_PO.inputName("batchNumber", "12345678")  # 批号
    Level_PO.inputName("vendor", u"上海百慕大")  # 供货方名称
    Level_PO.inputXpath("//input[@name='purchaseDate']", u"2018-07-11")  # 购进日期
    Level_PO.inputName("amount", "6")  # 购进数量
    Level_PO.clickXpath("//button[@onclick='doSaveRecord()']", 2)  # 保存


    # Level_PO.close_driver()

