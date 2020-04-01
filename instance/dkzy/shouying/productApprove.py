# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-6-5
# Description: 首营 后台品种资料审核
# usage: python productApprove.py 手机号
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PageObject.ShouyingPO import *

'''首营前台'''

if len(sys.argv) != 3:
    print u"功能：首营后台品种资料审核\n" \
          u"语法：" + str(sys.argv[0]).split(".")[0] + u" 品种名称 审核状态对应的编号\n" \
          u"参数：审核状态对应的编号 pass = 通过，refuse = 拒绝\n" \
          u"例子：" + str(sys.argv[0]).split(".")[0] + u" 登山用品 pass \n"
elif sys.argv[2] != "pass" and sys.argv[2] != "refuse":
    printColor('\033[1;31;47m', 'printRed', u"8、很遗憾，审核状态对应的编号不存在！\n")
else:

    from Public.webdriver import *
    Level_PO = LevelPO(Webdriver())
    Shouying_PO = ShouyingPO(Level_PO)

    if platform.system() == 'Windows':
        varProductName = unicode(sys.argv[1], "gbk")
    elif platform.system() == 'Darwin':  # for mac
        varProductName = unicode(sys.argv[1], "utf8")
    # 后台企业审核

    Level_PO.openURL(varURLbehind, 1)
    Shouying_PO.houtaiLogin("13816109050", "q123456")  # 已存在的管理员
    Shouying_PO.productApprove(varProductName, "pass")

