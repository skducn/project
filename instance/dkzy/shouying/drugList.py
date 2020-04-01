# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-4-27
# Description: 首营 药检单， 新建药检单，发出药检单，接受药检单
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PageObject.ShouyingPO import *

if len(sys.argv) != 6:
    print u"功能：药检单（新建药检单、发送药检单、接收/拒绝药检单、继续发送给下游企业[经营、公立、私立、诊所、零售药房]），只适用于药品或药片中饮，且药检品种名必须已审核通过）\n" \
           u"语法：" + str(sys.argv[0]).split(".")[0] + u" 生产企业 经营企业 下游企业 药品名 接收或拒绝\n" \
           u"例子：" + str(sys.argv[0]).split(".")[0] + u" 14516109051 14516109052 14516109053 维生素 pass|refuse\n"
else:

    from Public.webdriver import *
    Level_PO = LevelPO(Webdriver())
    Shouying_PO = ShouyingPO(Level_PO)

    if platform.system() == 'Darwin':
        varProductName = unicode(sys.argv[4], "utf8")  # 产品名称
    if platform.system() == 'Windows':
        varProductName = unicode(sys.argv[4], "gbk")  # 产品名称

    varPihao = Third_PO.randomDigit(8)  # 随机生成8位数的批号


    # main =============================================================================================================

    # 获取sys.argv[1]的企业类型
    Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[1]))
    t0 = Database_PO.cur.fetchone()
    Database_PO.cur.execute('select type from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (t0[0]))
    t1 = Database_PO.cur.fetchone()
    tblType1 = t1[0]
    # 获取sys.argv[2]的企业类型
    Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[2]))
    t0 = Database_PO.cur.fetchone()
    Database_PO.cur.execute('select type from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (t0[0]))
    t1 = Database_PO.cur.fetchone()
    tblType2 = t1[0]
    # 获取sys.argv[3]的企业类型
    Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[3]))
    t0 = Database_PO.cur.fetchone()
    Database_PO.cur.execute('select type from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (t0[0]))
    t1 = Database_PO.cur.fetchone()
    tblType3 = t1[0]

    if not (tblType1):
        Level_PO.printColor('\033[1;31;47m', 'printRed', u"很抱歉，该账号（" + sys.argv[1] + u"）不存在。")
        Level_PO.close_driver();os._exit(0)
    if not (tblType2):
        Level_PO.printColor('\033[1;31;47m', 'printRed', u"很抱歉，该账号（" + sys.argv[2] + u"）不存在。")
        Level_PO.close_driver();os._exit(0)
    if not (tblType3):
        Level_PO.printColor('\033[1;31;47m', 'printRed', u"很抱歉，该账号（" + sys.argv[3] + u"）不存在。")
        Level_PO.close_driver();os._exit(0)

    if tblType1 != 1 :
        Level_PO.printColor('\033[1;31;47m', 'printRed', u"很抱歉，该账号（" + sys.argv[1] + u"）不是生产企业，请重新填写。")
        Level_PO.close_driver()
        os._exit(0)
    elif tblType2 != 2 :
        Level_PO.printColor('\033[1;31;47m', 'printRed', u"很抱歉，该账号（" + sys.argv[2] + u"）不是经营企业，请重新填写。")
        Level_PO.close_driver()
        os._exit(0)
    elif tblType3 == 1:
        Level_PO.printColor('\033[1;31;47m', 'printRed', u"很抱歉，该账号（" + sys.argv[3] + u"）不能是生产企业，请重新填写。")
        Level_PO.close_driver()
        os._exit(0)
    elif sys.argv[2] == sys.argv[3]:
        Level_PO.printColor('\033[1;31;47m', 'printRed', u"很抱歉，经营企业与下游企业不能是同一个账号，请重新填写。")
        Level_PO.close_driver()
        os._exit(0)
    else:
        printColor('\033[1;31;47m', 'printSkyBlue', u"药检单（生产企业新建药检单，给经营企业发送药检单，经营企业接收后在发给下游企业[经营、公立、私立、诊所、零售药房]）")

        print u"[1/4]，生产企业（" + sys.argv[1] + u"）新建药检单、并发送药检单给经营企业（" + sys.argv[2] + u"）"
        Level_PO.openURL(varURLfront, 1)
        Shouying_PO.login(sys.argv[1], "q123456")
        Shouying_PO.drugList_addDrug(varProductName, varPihao)
        Shouying_PO.drugList_sendDrug(sys.argv[2], varProductName, varPihao)

        if sys.argv[5] == "pass" :
            print u"[2/4]，经营企业（" + sys.argv[2] + u"）接收生产企业（" + sys.argv[1] + u"）发来的药检单。"
        else:
            print u"[2/4]，经营企业（" + sys.argv[2] + u"）拒绝生产企业（" + sys.argv[1] + u"）发来的药检单。"
        Level_PO.openURL(varURLfront, 1)
        Shouying_PO.login(sys.argv[2], "q123456")
        Shouying_PO.drugList_receiveDrug(varProductName, varPihao, sys.argv[5])  # 接收 或 拒绝

        if sys.argv[5] == "pass":
            print u"[3/4]，经营企业（" + sys.argv[2] + u"）继续发送药检单给下游企业（" + sys.argv[3] + u"）。"
            Shouying_PO.drugList_sendDrug(sys.argv[3], varProductName, varPihao)

            print u"[4/4]，下游企业（" + sys.argv[3] + u"）接收经营企业（" + sys.argv[2] + u"）发来的药检单。"
            Level_PO.openURL(varURLfront, 1)
            Shouying_PO.login(sys.argv[3], "q123456")
            Shouying_PO.drugList_receiveDrug(varProductName, varPihao, sys.argv[5])  # 接收

    printColor('\033[1;31;47m', 'printGreen', u"9、恭喜您，药检单发送成功。下一步发起品种首营：python faqiProduct.py " + sys.argv[1] + u" " + sys.argv[2] + u" 维生素")

    Level_PO.close_driver()