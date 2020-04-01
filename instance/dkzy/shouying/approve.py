# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-6-5
# Description: 首营 后台审核企业认证
# usage: python approve.py 手机号
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from PageObject.ShouyingPO import *
varERROR = u"错误，缺少参数，预期参数" + str(len(sys.argv)) + u"个。\n"

if len(sys.argv) != 3:
    print u"功能：首营后台审核企业认证\n" \
           u"语法：" + str(sys.argv[0]).split(".")[0] + u" 手机号 审核状态对应的编号\n" \
           u"参数：审核状态对应的编号 pass = 通过，refuse = 拒绝\n" \
           u"例子：" + str(sys.argv[0]).split(".")[0] + u" 14516109051 pass|refuse \n"
elif sys.argv[2] != "pass" and sys.argv[2] != "refuse":printColor('\033[1;31;47m', 'printRed', u"很遗憾，审核状态对应的编号不存在！\n")
else:

    from Public.webdriver import *
    Level_PO = LevelPO(Webdriver())
    Shouying_PO = ShouyingPO(Level_PO)

    # main =============================================================================================================

    # 通过手机号获得企业类型和企业名称
    varCompanyName, varCompanyType = Shouying_PO.getEnterpriseTypeAndName(sys.argv[1])

    try:
        Level_PO.openURL(varURLbehind, 1)
        Shouying_PO.houtaiLogin("13816109050", "q123456")  # 默认管理员
    except:printColor('\033[1;31;47m', 'printRed', "errorrrrrrrrrr, " + str(sys._getframe().f_lineno) + " row from " + str(__file__));os._exit(0)

    Level_PO.clickLinktext(u"审核管理", 2)
    Level_PO.clickLinktext(u"企业资质审核", 2)     # 企业审核 - 默认待审核标签
    Level_PO.inputId("enterprise_name", varCompanyName)  # 搜索 企业名称
    Level_PO.clickXpath("//button[@type='submit']", 2)  # 提交
    Level_PO.clickLinktext(u"去审核", 2)
    if sys.argv[2] == u"pass": # 通过
        '审核通过'
        Level_PO.clickLinktext(u"审核通过", 4)
        Level_PO.clickXpath("//div[@class='cetc-popup-footer']/button", 2)
        if varCompanyType == u"医疗机构 - 私立医院" or varCompanyType == u"医疗机构 - 诊所":
            Level_PO.clickLinktext(u"审核通过", 2)
            Level_PO.clickXpath("//div[@class='cetc-popup-footer']/button", 2)  # 二次确认
        printColor('\033[1;31;47m', 'printGreen', u"3、恭喜您，企业账号（" + sys.argv[1] + u"）认证资料审核通过。下一步设置普管：python setManager.py " + sys.argv[1] + u" new ?")

    elif sys.argv[2] == u"refuse": #拒绝
        '审核拒绝'
        Level_PO.clickLinktext(u"审核拒绝", 2)
        varRefuseId = Level_PO.getXpathAttr("//input[@name='refuse-cause']", u"id")
        Level_PO.inputName("refuse-cause", u"测试，内容不完成所以拒绝!!!")  # 输入拒绝理由
        Level_PO.clickXpath("//button[@onclick='approveNotThrough(" + str(varRefuseId).split("-")[2] + ",this)']", 2)  # 确认
        Level_PO.clickXpath("//div[@class='cetc-popup-footer']/button", 4)  # 二次确认
        '检查认证状态及拒绝原因'
        Database_PO.cur.execute('select approve_status,refuse_cause from tt_enterprise where name="%s" order by enterprise_id desc limit 1' % (varCompanyName))
        t1 = Database_PO.cur.fetchone()
        Database_PO.conn.commit()
        if t1[0] == 1 and t1[1] == u"测试，内容不完成所以拒绝!!!":
            printColor('\033[1;31;47m', 'printGreen', u"3、恭喜您，企业账号（" + sys.argv[1] + u"）认证资料审核被拒且拒绝理由正确。")
        else:
            printColor('\033[1;31;47m', 'printRed', u"3、很遗憾，企业账号（" + sys.argv[1] + u"）认证资料审核拒绝或拒绝理由未填写！")

    Level_PO.close_driver()
