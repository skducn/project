# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-4-27
# Description: 发起首营,上游发给下游的企业
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # import sys, os
# # sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../")))  # 将上级目录添加到环境变量中
# # from PageObject.color import *
# import sys
# sys.path.append("..")
# from dkzy.shouying.config.config import *
from PageObject.ShouyingPO import *

varERROR = u"错误，缺少参数，预期参数" + str(len(sys.argv)) + u"个。\n"

if len(sys.argv) != 3:
    print u"功能：发起企业首营\n" \
           u"语法：" + str(sys.argv[0]).split(".")[0] + u" 上游企业 下游企业 \n" \
           u"例子：" + str(sys.argv[0]).split(".")[0] + u" 14516109051  14516109052 \n"
else:

    from Public.webdriver import *
    Level_PO = LevelPO(Webdriver())
    Shouying_PO = ShouyingPO(Level_PO)

    Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[1]))
    sendEnterpriseId = Database_PO.cur.fetchone()
    Database_PO.cur.execute('select link_man from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (sendEnterpriseId[0]))
    sendName = Database_PO.cur.fetchone()  # 发起方企业管理员
    Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[2]))
    receiveEnterpriseId = Database_PO.cur.fetchone()
    Database_PO.cur.execute('select link_man from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (receiveEnterpriseId[0]))
    receiveName = Database_PO.cur.fetchone()  # 接受方企业管理员
    if not (sendName):
        Level_PO.printColor('\033[1;31;47m', 'printRed', u"很抱歉，该账号（" + sys.argv[1] + u"）不存在。")
        Level_PO.close_driver();os._exit(0)
    if not (receiveName):
        Level_PO.printColor('\033[1;31;47m', 'printRed', u"很抱歉，该账号（" + sys.argv[2] + u"）不存在。")
        Level_PO.close_driver();os._exit(0)
    Database_PO.cur.execute('select name,phone_number from tt_enterprise_user where enterprise_id="%s" order by enterprise_user_id desc limit 1' % (sendEnterpriseId[0]))
    sendManager = Database_PO.cur.fetchone()
    Database_PO.cur.execute('select name,phone_number from tt_enterprise_user where enterprise_id="%s" order by enterprise_user_id desc limit 1' % (receiveEnterpriseId[0]))
    receiveManager = Database_PO.cur.fetchone()

    # main =============================================================================================================

    printColor('\033[1;31;47m', 'printSkyBlue', u"发起企业首营（1我方发起、2对方拒绝、3我方再次发起、4对方接收、5我方普管拒绝、6我方重新签发、7我方普管通过、8对方普管通过、9我方企管通过、10对方企管通过、11我方及对方首营统计）")

    # 1、我方发起
    printColor('\033[1;31;47m', 'printGreen', u"\n[1/11]，我方(" + sendName[0] + u"，" + sys.argv[1] + u")发起企业首营交换。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[1], "q123456")
    Shouying_PO.shouyingFrom(sys.argv[1], sys.argv[2])


    # 2、对方拒绝
    printColor('\033[1;31;47m', 'printGreen', u"\n[2/11]，对方(" + receiveName[0] + u"，" + sys.argv[2] + u")拒绝企业首营交换。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[2], u"q123456")
    Shouying_PO.shouyingTo(sys.argv[2], u"refuse", u"拒绝理由是资料缺少！")


    # 3、我方再次发起
    printColor('\033[1;31;47m', 'printGreen', u"\n[3/11]，我方(" + sendName[0] + u"，" +  sys.argv[1] + u")再次发起首营交换申请。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[1], u"q123456")
    Shouying_PO.shouyingFromAgain(sys.argv[1])


    # 4、对方接收
    printColor('\033[1;31;47m', 'printGreen', u"\n[4/11]，对方(" + receiveName[0] + u"，" +  sys.argv[2] + u")接收企业首营交换。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[2], u"q123456")
    Shouying_PO.shouyingTo(sys.argv[2], u"pass", u"")


    # 5、我方普管拒绝
    printColor('\033[1;31;47m', 'printGreen', u"\n[5/11]，我方普管（" + sendManager[0] + u"，" + sendManager[1] + u"）审核拒绝。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sendManager[1], u"q123456")
    Shouying_PO.normalManagerAudit(sys.argv[1], u"refuse")


    # 6、我方重新签发
    printColor('\033[1;31;47m', 'printGreen', u"\n[6/11]，对方(" + receiveName[0] + u"，" + sys.argv[2] + u")重新签发。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[2], u"q123456")
    Shouying_PO.shouyingToRetry(sys.argv[2])


    # 7、我方普管通过
    printColor('\033[1;31;47m', 'printGreen', u"\n[7/11]，我方普管（" + sendManager[0] + u"，" + sendManager[1] + u"）审核通过。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sendManager[1], u"q123456")
    Shouying_PO.normalManagerAudit(sys.argv[1], "pass")


    # 8、对方普管通过
    printColor('\033[1;31;47m', 'printGreen', u"\n[8/11]，对方普管（" + receiveManager[0] + u"，" + receiveManager[1] + u"）审核通过。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(receiveManager[1], u"q123456")
    Shouying_PO.normalManagerAudit(sys.argv[2], "pass")


    # 9、我方企管通过
    printColor('\033[1;31;47m', 'printGreen', u"\n[9/11]，我方企管(" + sendName[0] + u"，" + sys.argv[1] + u")审核通过。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[1], u"q123456")
    Shouying_PO.enterpriseManagerAudit(sys.argv[1], u"pass")


    # 10、对方企管通过
    printColor('\033[1;31;47m', 'printGreen', u"\n[10/11]，对方企管(" + receiveName[0] + u"，" + sys.argv[2] + u")审核通过。")
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[2], u"q123456")
    Shouying_PO.enterpriseManagerAudit(sys.argv[2], u"pass")


    # 11、统计双方首营统计信息
    printColor('\033[1;31;47m', 'printGreen', u"\n[11/11]，显示双发首营统计信息")
    print u"我方（" + sys.argv[1] + u"）首页首营统计信息。"
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[1], u"q123456")
    Shouying_PO.statisticsShouying(1)
    print u"对方（" + sys.argv[2] + u"）首页首营统计信息。"
    Level_PO.openURL(varURLfront, 3)
    Shouying_PO.login(sys.argv[2], u"q123456")
    Shouying_PO.statisticsShouying(0)

    printColor('\033[1;31;47m', 'printSkyBlue', u"\n企业首营交换已完成")

    Level_PO.close_driver()



