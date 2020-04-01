# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-7-9
# Description: 电科智药，发起品种首营
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PageObject.ShouyingPO import *

if len(sys.argv) != 4:
    print u"功能：发起品种首营\n" \
           u"语法：" + str(sys.argv[0]).split(".")[0] + u" 发起方 接收方 品种名称 \n" \
           u"例子：" + str(sys.argv[0]).split(".")[0] + u" 14516109051 14516109052 登山用品\n"
else:
    from Public.webdriver import *
    Level_PO = LevelPO(Webdriver())
    Shouying_PO = ShouyingPO(Level_PO)

    # 发起方
    Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[1]))
    t = Database_PO.cur.fetchone()
    sendEnterpriseId = t[0]  # ID
    Database_PO.cur.execute('select link_man from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (sendEnterpriseId))
    sendName = Database_PO.cur.fetchone()  # 中文用户名

    # 接受方
    Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[2]))
    y = Database_PO.cur.fetchone()
    receiveEnterpriseId = y[0]
    Database_PO.cur.execute('select link_man from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (receiveEnterpriseId))
    receiveName = Database_PO.cur.fetchone()  # 中文用户名

    # 发起方普通管理员用户名
    Database_PO.cur.execute('select name,phone_number from tt_enterprise_user where enterprise_id="%s" order by enterprise_user_id desc limit 1' % (sendEnterpriseId))
    sendManager = Database_PO.cur.fetchone()

    # 接收方普通管理员用户名
    Database_PO.cur.execute('select name,phone_number from tt_enterprise_user where enterprise_id="%s" order by enterprise_user_id desc limit 1' % (receiveEnterpriseId))
    receiveManager = Database_PO.cur.fetchone()

    # main =============================================================================================================
    printColor('\033[1;31;47m', 'printSkyBlue', u"发起品种首营（1我方发起、2对方普管拒绝、3我方再次发起、4对方普管接收、5对方企管接收、6首营统计）")

    # 1、我方发起
    printColor('\033[1;31;47m', 'printYellow', u"\n[1/6]，我方（" + sendName[0] + u"，" + sys.argv[1] + u"）发起品种交换。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[1], "q123456")
    Shouying_PO.productFrom(sys.argv[1], sys.argv[2], sys.argv[3])

    # 2、对方普管拒绝
    printColor('\033[1;31;47m', 'printYellow', u"\n[2/6]，对方普管（" + receiveManager[0] + u"，" + receiveManager[1] + u"）拒绝品种交换。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(receiveManager[1], "q123456")
    Shouying_PO.productToAudit(sys.argv[2], sys.argv[3], u"refuse")

    # 3、我方再次发起
    printColor('\033[1;31;47m', 'printYellow', u"\n[3/6]，我方（" + sendName[0] + u"，" + sys.argv[1] + u"）再次申请品种交换。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[1], "q123456")
    Shouying_PO.productFromAgain()

    # 4、对方普管接收
    printColor('\033[1;31;47m', 'printYellow', u"\n[4/6]，对方普管（" + receiveManager[0] + u"，" + receiveManager[1] + u"）同意品种交换。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(receiveManager[1], "q123456")
    Shouying_PO.productToAudit(sys.argv[2], sys.argv[3], u"pass")

    # 5、对方企管接收
    printColor('\033[1;31;47m', 'printYellow', u"\n[5/6]，对方（" + receiveName[0] + u"，" + sys.argv[2] + u"）同意品种交换。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[2], "q123456")
    Shouying_PO.productToAudit(sys.argv[2], sys.argv[3], u"pass")

    # 6、统计双方首营统计信息
    printColor('\033[1;31;47m', 'printYellow', u"\n[6/6]，显示双发首营统计信息")
    print u"我方（" + sys.argv[1] + u"）首页首营统计信息。"
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[1], "q123456")
    Shouying_PO.statisticsShouying(1)
    print u"对方（" + sys.argv[2] + u"）首页首营统计信息。"
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[2], "q123456")
    Shouying_PO.statisticsShouying(0)

    printColor('\033[1;31;47m', 'printSkyBlue', u"\n品种首营交换已完成")

    Level_PO.close_driver()

