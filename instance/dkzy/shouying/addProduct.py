# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-6-6
# Description: 首营产品管理，新增产品 （只限于生产企业、经营企业）
'产品目的是用于品种交换，因此在品种首营交换前必须先新建产品'
'场景1，生产企业新建产品资料 ，认证状态 = "厂家认证"'
'场景2，经营企业代为上传产品资料，如新建产品资料时生产厂家一栏填写生产企业名，如：上海14616109051生产企业 ; 认证状态 = "经营公司认证",'
'同时此生产企业的待认证产品列表中也会显示该产品的 处理状态 ="待认证"'
'生产企业在待认证产品列表页中编辑经营企业上传的产品，提交后此产品资料转移到产品列表中，认证状态 = "厂家认证"'
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PageObject.ShouyingPO import *

if len(sys.argv) != 5:
    print u"功能：首营新增产品\n" \
           u"语法：" + str(sys.argv[0]).split(".")[0] + u" 生产企业账号 经营企业账号 产品类别对应编号 产品名称\n" \
           u"参数：产品类别对应编号： 1 = 药品 ，2 = 中药饮片 ， 3 = 化妆品 ， 4 = 食品 ， 5 = 日用品 ， 6 = 消毒产品 ， 7 = 保健食品 ， 8 = 医疗器械 \n" \
           u"例子1：" + str(sys.argv[0]).split(".")[0] + u" 14616109051 ? 1 阿司匹林肠溶片 //生产企业新增品种，无经营企业则用？代替。\n" \
                                                         u"例子2：" + str(sys.argv[0]).split(".")[0] + u" 14616109051 14616109052 4 膨化食品 //经营企业代生产企业新增品种。 \n"
else:

    from Public.webdriver import *
    Level_PO = LevelPO(Webdriver())
    Shouying_PO = ShouyingPO(Level_PO)

    try:
        Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[1]))
        t0 = Database_PO.cur.fetchone()
        Database_PO.cur.execute('select name,business_scope from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (t0[0]))
        t1 = Database_PO.cur.fetchone()
        varEnterpriseCompany = t1[0]  # 生产企业
    except:
        printColor('\033[1;31;47m', 'printRed', u"很抱歉，企业账号" + sys.argv[1] + u"不存在。")
        os._exit(0)  # 会直接将python程序终止，之后的所有代码都不会继续执行。

    try:
        # 经营企业
        if sys.argv[2] != "?":
            Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[2]))
            t0 = Database_PO.cur.fetchone()
            Database_PO.cur.execute('select name,business_scope from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (t0[0]))
            t1 = Database_PO.cur.fetchone()
            varOperateCompany = t1[0]  # 经营企业
        varNo = sys.argv[3]
        if varNo not in t1[1]:
            printColor('\033[1;31;47m', 'printRed', u"很遗憾，输入的产品类别对应编号不在此范围内（1 = 药品 ，2 = 中药饮片 ， 3 = 化妆品 ， 4 = 食品 ， 5 = 日用品 ， 6 = 消毒产品 ， 7 = 保健食品 ， 8 = 医疗器械） ，程序异常退出！")
            os._exit(0)
        if platform.system() == 'Windows':
            varProductName = unicode(sys.argv[4], "gbk")
        elif platform.system() == 'Darwin':  # for mac
            varProductName = unicode(sys.argv[4], "utf8")
    except:
        print "\n"
        printColor('\033[1;31;47m', 'printRed', u"很遗憾，企业账号不存在或程序异常中断！")
        os._exit(0)

    # main =============================================================================================================

    Level_PO.openURL(varURLfront, 1)

    if sys.argv[2] == u"?":
        # '场景1，生产企业新建产品资料 ，认证状态 = "厂家认证"'
        Shouying_PO.login(sys.argv[1], "q123456")
    else:
        # '场景2，经营企业代为上传产品资料，如新建产品资料时生产厂家一栏填写生产企业名，如：上海14616109051生产企业 ; 认证状态 = "经营公司认证",'
        # '同时此生产企业的待认证产品列表中也会显示产品的 处理状态 ="待认证"'
        Shouying_PO.login(sys.argv[2], "q123456")

    Level_PO.clickLinktext(u"产品管理", 2)
    Level_PO.clickLinktext(u"新建产品资料", 2)
    # 产品管理（产品类别，产品名称，规格，批准文号，批准文号JPG，证件有效期，生产企业，企业内部编码，剂型，药品质量标准JPG，药品注册证JPG，证件有效期，药品检验报告书JPG，药品包装盒JPG，药品说明书JPG，产品说明书JPG）
    if varNo == "1":  # '药品'
        Shouying_PO.createProductInfo(u"药品", varProductName, u"10支/盒", u"国药准字H19997001", varJpg, varValidDate, varEnterpriseCompany, "11111111", u"溶剂型",varJpg,varJpg, varValidDate, varJpg,varJpg,varJpg,varDoc)
    elif varNo == "2":  # '中药饮片'
        Shouying_PO.createProductInfo(u"中药饮片", varProductName, u"20支/盒", u"国药准字H19997002", varJpg, varValidDate, varEnterpriseCompany, "22222222", u"溶剂型", varJpg,varJpg, varValidDate, varJpg,varJpg,varJpg,varDoc)
    elif varNo == "3":  # '化妆品'
        Shouying_PO.createProductInfo(u"化妆品", varProductName, u"30支/盒", u"国药准字H19997003", varJpg, varValidDate, varEnterpriseCompany, "33333333", u"溶剂型", varJpg,varJpg, varValidDate, varJpg,varJpg,varJpg,varDoc)
    elif varNo == "4":  # '食品'
        Shouying_PO.createProductInfo(u"食品", varProductName, u"40支/盒", u"国药准字H19997004", varJpg, varValidDate, varEnterpriseCompany, "44444444", u"溶剂型", varJpg,varJpg,varValidDate, varJpg,varJpg,varJpg,varDoc)
    elif varNo == "5":  # '日用品'
        Shouying_PO.createProductInfo(u"日用品", varProductName, u"50支/盒", u"国药准字H19997005", varJpg, varValidDate, varEnterpriseCompany, "55555555", u"溶剂型", varJpg,varJpg, varValidDate, varJpg,varJpg,varJpg,varDoc)
    elif varNo == "6":  # '消毒产品'
        Shouying_PO.createProductInfo(u"消毒产品", varProductName, u"60支/盒", u"国药准字H19997006",varJpg, varValidDate, varEnterpriseCompany, "66666666", u"溶剂型", varJpg,varJpg, varValidDate, varJpg,varJpg,varJpg,varDoc)
    elif varNo == "7":  # '保健食品'
        Shouying_PO.createProductInfo(u"保健食品", varProductName, u"70支/盒", u"国药准字H34997007", varJpg, varValidDate, varEnterpriseCompany, "77777777", u"溶剂型", varJpg,varJpg, varValidDate, varJpg,varJpg,varJpg,varDoc)
    elif varNo == "8":  # '医疗器械'
        Shouying_PO.createProductInfo(u"医疗器械", varProductName, u"80支/盒", u"国药准字H22997008", varJpg, varValidDate, varEnterpriseCompany, "88888888", u"溶剂型", varJpg,varJpg, varValidDate, varJpg,varJpg,varJpg,varDoc)
    else:
        os._exit(0)

    sleep(2)
    # 新增后，产品管理列表页，检查记录状态
    Level_PO.inputName("name", varProductName)  # 产品名称
    Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
    x = 0
    list1 = Level_PO.getXpathsText("//td")
    if sys.argv[2] == u"?":
        for i in range(len(list1)):
            if list1[i] == varProductName or list1[i] == u"厂家认证":
                x = x + 1
        if x == 2:
            printColor('\033[1;31;47m', 'printGreen', u"7、恭喜您，生产企业已成功新增产品 \"" + varProductName + u"\" （厂家认证）。下一步审核产品 python productApprove.py "+ varProductName + u"pass|refuse")
    else:
        for i in range(len(list1)):
            if list1[i] == varProductName or list1[i] == u"经营公司认证":
                x = x + 1
        if x == 2 :
            printColor('\033[1;31;47m', 'printYellow', u"7、恭喜您，经营企业代生产企业（" + sys.argv[1] + u"）已成功新增产品 \"" + varProductName + u"\" （经营公司认证）。")


     # 经营企业，生产企业在待认证产品列表页中编辑经营企业上传的产品，提交后此产品资料转移到产品列表中，认证状态 = "厂家认证"'
    if sys.argv[2] != u"?":
        Level_PO.openURL(varURLfront, 3)
        Level_PO.setMaximize()
        Shouying_PO.login(sys.argv[1], "q123456")
        Level_PO.clickLinktext(u"产品管理", 2)
        Level_PO.clickLinktext(u"待认证产品", 2)
        Level_PO.inputName("name", varProductName)  # 搜索产品名称
        Level_PO.clickId("btnQuery", 2)  # 搜索
        Level_PO.clickLinktext(u"编辑", 2)  # 编辑
        Level_PO.inputName("internalCode", "58887414") # 企业内部编码
        Level_PO.clickXpath("//input[@onclick='doSubmit();']", 2)  # 提交（没有编辑内容直接提交）
        Level_PO.clickLinktext(u"产品列表", 2)
        Level_PO.inputName("name", varProductName)  # 搜索产品名称
        Level_PO.clickId("btnQuery", 2)  # 搜索
        x = 0
        list1 = []
        list1 = Level_PO.getXpathsText("//td")
        if sys.argv[2] != u"?":
            for i in range(len(list1)):
                if list1[i] == varProductName or list1[i] == u"厂家认证":
                    x = x + 1
            if x == 2:
                printColor('\033[1;31;47m', 'printYellow', u"7、恭喜您，生产企业已将产品 \"" + varProductName + u"\" 状态更新为厂家认证。下一步审核产品 python productApprove.py "+ varProductName + u"pass|refuse")

    Level_PO.close_driver()



