# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-6-22
# Description: 特殊药品出入库管理 （新建出库单、出库管理），依赖于产品
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from PageObject.ShouyingPO import *


if len(sys.argv) != 5:
    print u"功能：特殊药品出入库管理（新建出库单），依赖于产品\n" \
    u"语法：" + str(sys.argv[0]).split(".")[0] + u" 生产企业 经营企业 下游企业 产品名\n" \
    u"例子1：" + str(sys.argv[0]).split(".")[0] + u" 15016109051 15016109052 15016109053 消毒产品 "
else:

    from Public.webdriver import *
    Level_PO = LevelPO(Webdriver())
    Shouying_PO = ShouyingPO(Level_PO)

    if platform.system() == 'Darwin':
        varProductName = unicode(sys.argv[4], "utf8")  # 产品名称
    if platform.system() == 'Windows':
        varProductName = unicode(sys.argv[4], "gbk")  # 产品名称
    varProductNameJinying = varProductName + u"(经营)"

    varStockOutDate = datetime.date.today() + datetime.timedelta(days=1)  # 出库日期为明天
    varStockInDate = datetime.date.today() + datetime.timedelta(days=2)  # 入库日期为后天
    varPihao = Third_PO.randomDigit(9)
    varQuantity = Third_PO.randomDigit(3)

    # 生产企业
    Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[1]))
    t0 = Database_PO.cur.fetchone()
    Database_PO.cur.execute('select name from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (t0[0]))
    t1 = Database_PO.cur.fetchone()
    varEnterpriseCompany = t1[0]  # 生产企业名

    # 经营企业
    Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[2]))
    t0 = Database_PO.cur.fetchone()
    Database_PO.cur.execute('select name from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (t0[0]))
    t1 = Database_PO.cur.fetchone()
    varOperateCompany = t1[0]  # 经营企业名

    # 公立医院
    Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[3]))
    t0 = Database_PO.cur.fetchone()
    Database_PO.cur.execute('select name from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (t0[0]))
    t1 = Database_PO.cur.fetchone()
    varPublicHospital = t1[0]  # 公立医院名

    # main =============================================================================================================

    printColor('\033[1;31;47m', 'printSkyBlue', u"特殊药品出入库管理（1生产企业新建产品并审核、2生产企业新建出库单、3经营企业全部接收入库、4经营企业新建产品并审核、5经营企业新建入库单...）")

    # 1、生产企业新建产品并审核
    printColor('\033[1;31;47m', 'printGreen', u"\n[1/11]，生产企业（" + sys.argv[1] + u"）新建产品（"+ varProductName + u"）并审核。")
    # 新建产品
    Level_PO.openURL(varURLfront, 2)
    Shouying_PO.login(sys.argv[1], "q123456")
    Level_PO.clickLinktext(u"产品管理", 2)
    Level_PO.clickLinktext(u"新建产品资料", 2)
    Shouying_PO.createProductInfo(u"药品", varProductName, u"10支/盒", u"国药准字H19997001", varJpg, varValidDate, varEnterpriseCompany, Third_PO.randomDigit(9), u"溶剂型", varJpg, varJpg, varValidDate, varJpg, varJpg, varJpg, varDoc)
    # 审核产品
    Level_PO.openURL(varURLbehind, 2)
    Shouying_PO.houtaiLogin("13816109050", "q123456")
    Shouying_PO.productApprove(varProductName, "pass")

    2、生产企业新建出库单
    printColor('\033[1;31;47m', 'printGreen', u"\n[2/11]，生产企业（" + sys.argv[1] + u"）新建出库单。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[1], "q123456")
    Level_PO.clickLinktext(u"特殊药品出入库管理", 2)
    Level_PO.clickLinktext(u"新建出库单", 2)  # Level_PO.clickXpath("//ul[@class='sidebar-menu tree']/li[5]//ul/li[2]/a", 2)  # 新建出库单
    Shouying_PO.newStockOut(varProductName, varPihao, varQuantity, str(varStockOutDate), varJpg, varOperateCompany)


    # 3、经营企业全部接收入库
    printColor('\033[1;31;47m', 'printGreen', u"\n[3/11]，3经营企业(" + sys.argv[2] + u")全部接收入库。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[2], "q123456")
    Level_PO.clickLinktext(u"特殊药品出入库管理", 2)
    Level_PO.clickLinktext(u"入库管理", 2)
    Level_PO.clickLinktext(u"我收到的出库申请", 2)
    Shouying_PO.StockIn(varProductName, str(varStockOutDate), varPihao, str(varStockInDate), varJpg)

    # 4、经营企业新建产品并审核
    printColor('\033[1;31;47m', 'printGreen', u"\n[4/11]，经营企业（" + sys.argv[2] + u"）新建产品（"+ varProductNameJinying + u"）并审核。")
    # 新建产品
    Level_PO.openURL(varURLfront, 2)
    Shouying_PO.login(sys.argv[2], "q123456")
    Level_PO.clickLinktext(u"产品管理", 2)
    Level_PO.clickLinktext(u"新建产品资料", 2)
    Shouying_PO.createProductInfo(u"药品", varProductNameJinying, u"10支/盒", u"国药准字H19997001", varJpg, varValidDate, varEnterpriseCompany, Third_PO.randomDigit(9), u"溶剂型", varJpg, varJpg, varValidDate, varJpg, varJpg, varJpg, varDoc)
    # 审核产品
    Level_PO.openURL(varURLbehind, 2)
    Shouying_PO.houtaiLogin("13816109050", "q123456")
    Shouying_PO.productApprove(varProductNameJinying, "pass")

    # 5、经营企业新建出库单
    printColor('\033[1;31;47m', 'printGreen', u"\n[5/11]，经营企业（" + sys.argv[2] + u"）新建出库单。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[2], "q123456")
    Level_PO.clickLinktext(u"特殊药品出入库管理", 2)
    Level_PO.clickLinktext(u"新建出库单", 2)
    Shouying_PO.newStockOut(varProductNameJinying, varPihao, varQuantity, str(varStockOutDate), varJpg, varPublicHospital)

    # 6、公立医院全部接收入库
    printColor('\033[1;31;47m', 'printGreen', u"\n[6/11]，公立医院(" + sys.argv[3] + u")全部接收入库。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[3], "q123456")
    Level_PO.clickLinktext(u"特殊药品出入库管理", 2)
    Level_PO.clickLinktext(u"入库管理", 2)
    Level_PO.clickLinktext(u"我收到的出库申请", 2)
    Shouying_PO.StockIn(varProductNameJinying, str(varStockOutDate), varPihao, str(varStockInDate), varJpg)

    # Level_PO.close_driver()



