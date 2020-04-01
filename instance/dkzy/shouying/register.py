# coding: utf-8
# subject : 首营 - 注册企业账号，
# Author     : John
# Date       : 2018-6-5
# usage: python register.py 手机号 企业类型对应的编号
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from PageObject.ShouyingPO import *

if len(sys.argv) != 3:
    print u"功能：首营注册企业账号\n" \
           u"语法：" + str(sys.argv[0]).split(".")[0] + u" 手机号 企业类型对应的编号 \n" \
           u"参数：企业类型对应编号 1 = 生产企业，2 = 经营企业，3 = 公立医院，4 = 私立医院，5 = 诊所，6 = 零售药店\n" \
           u"例子：" + str(sys.argv[0]).split(".")[0] + u" 14516109051 1  \n" \
           u"注释：注册一家上海14516109051生产企业，手机号 14516109051，密码 q123456，邮箱 14516109051@cetc.cn\n"
elif len(sys.argv[1]) != 11: printColor('\033[1;31;47m', 'printRed', u"很抱歉，手机号必须是11位。")
elif int(sys.argv[2]) < 1 or int(sys.argv[2])> 6: printColor('\033[1;31;47m', 'printRed', u"很抱歉，企业类型编号范围1 - 6 \n")
else:

    from Public.webdriver import *
    Level_PO = LevelPO(Webdriver())
    Shouying_PO = ShouyingPO(Level_PO)

    # main =============================================================================================================

    try:Level_PO.openURL(varURLfront, 1)
    except:printColor('\033[1;31;47m', 'printRed', "errorrrrrrrrrr, " + str(sys._getframe().f_lineno) + " row from " + str(__file__));os._exit(0)

    Level_PO.clickLinktext(u"注册", 2)
    if sys.argv[2] == "1":
        Shouying_PO.register(sys.argv[1] + u"@cetc.cn", u"q123456", u"上海" + sys.argv[1] + u"生产企业", u"生产企业", sys.argv[1])
    elif sys.argv[2] == "2":
        Shouying_PO.register(sys.argv[1] + u"@cetc.cn", u"q123456", u"上海" + sys.argv[1] + u"经营企业", u"经营企业", sys.argv[1])
    elif sys.argv[2] == "3":
        Shouying_PO.register(sys.argv[1] + u"@cetc.cn", u"q123456", u"上海" + sys.argv[1] + u"公立医院", u"医疗机构 - 公立医院", sys.argv[1])
    elif sys.argv[2] == "4":
        Shouying_PO.register(sys.argv[1] + u"@cetc.cn", u"q123456", u"上海" + sys.argv[1] + u"私立医院", u"医疗机构 - 私立医院", sys.argv[1])
    elif sys.argv[2] == "5":
        Shouying_PO.register(sys.argv[1] + u"@cetc.cn", u"q123456", u"上海" + sys.argv[1] + u"诊所", u"医疗机构 - 诊所", sys.argv[1])
    elif sys.argv[2] == "6":
        Shouying_PO.register(sys.argv[1] + u"@cetc.cn", u"q123456", u"上海" + sys.argv[1] + u"零售药店", u"零售药店", sys.argv[1])

    Level_PO.close_driver()

