# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2019-5-7
# Description: OA之web平台 - 加班申请单
# ff 66.0.4 (64 位) , selenium =3.141.0，gecko = 0.24.0
# geckodriver下载：https://github.com/mozilla/geckodriver/releases
# selenium更新： pip3 install -U selenium
#***************************************************************
# from OA.web.PageObject.ShouyingPO import *
from zyjk.OA.web.PageObject.OvertimePO import *

# if len(sys.argv) != 3:
#     print(u"功能：首营注册企业账号\n" \
#            u"语法：" + str(sys.argv[0]).split(".")[0] + u" 手机号 企业类型对应的编号 \n" \
#            u"参数：企业类型对应编号 1 = 生产企业，2 = 经营企业，3 = 公立医院，4 = 私立医院，5 = 诊所，6 = 零售药店\n" \
#            u"例子：" + str(sys.argv[0]).split(".")[0] + u" 14516109051 1  \n" \
#            u"注释：注册一家上海14516109051生产企业，手机号 14516109051，密码 q123456，邮箱 14516109051@cetc.cn\n")
# elif len(sys.argv[1]) != 11:
#     printColor('\033[1;31;47m', 'printRed', u"很抱歉，手机号必须是11位。")
# elif int(sys.argv[2]) < 1 or int(sys.argv[2])> 6:
#     printColor('\033[1;31;47m', 'printRed', u"很抱歉，企业类型编号范围1 - 6 \n")
# else:


from Public.webdriver import *
Level_PO = LevelPO(Webdriver())
Overtime_PO = OvertimePO(Level_PO)

# 盛蕴 - 东区经理 - 加班申请单
# 部门经理/地区经理（刘挺）——>总监（廖荣平）—>人事经理（王磊）—>副总经理（陈剑波）—>通知人事（王蕾）


# Level_PO.openURL(varURLfront, 1)
# Overtime_PO.login("liuting")
# Level_PO.openURL("http://192.168.0.65/general/workflow/new/new_old/index.php", 2)  # 打开加班申请单
# (varSerial, varNextPerson) = Overtime_PO.createRequisition(u'上海盛蕴医药科技股份有限公司', '申请', '工作日', '2019-05-07 18:30:09', '2019-05-07 20:30:09', u'我要加班楼！')  # 填写申请单

# Level_PO.openURL(varURLfront, 1)
# Overtime_PO.login("liaorongping")
# Level_PO.openURL("http://192.168.0.65/general/workflow/list/", 2)  # 打开待办工作列表
# varNextPerson = Overtime_PO.backlog(varSerial, 'on', '总监审批', '总监审批建议', '总监同意哦。')  # 打开待办事项，审核申请单
#
# Level_PO.openURL(varURLfront, 1)
# Overtime_PO.login("wanglei01")
# Level_PO.openURL("http://192.168.0.65/general/workflow/list/", 2)  # 打开待办工作列表
# varNextPerson = Overtime_PO.backlog(varSerial, 'on', '人力资源部审批结果', '人力资源部审批建议', '人事经理同意哦。')  # 打开待办事项，审核申请单
#
# Level_PO.openURL(varURLfront, 1)
# Overtime_PO.login("chenjianbo")
# Level_PO.openURL("http://192.168.0.65/general/workflow/list/", 2)  # 打开待办工作列表
# varNextPerson = Overtime_PO.backlog(varSerial, 'on', '副总经理审批', '副总经理建议', '副总经理同意哦。')  # 打开待办事项，审核申请单
#
# Level_PO.openURL(varURLfront, 1)
# Overtime_PO.login("wanglei")
# Level_PO.openURL("http://192.168.0.65/general/workflow/list/", 2)  # 打开待办工作列表
# varNextPerson = Overtime_PO.notice(varSerial)  # 打开待办事项，通知
#
# Level_PO.openURL(varURLfront, 1)
# Overtime_PO.login("liuting")
# Level_PO.openURL("http://192.168.0.65/general/workflow/list/", 2)  # 打开待办工作列表
# Overtime_PO.backlog(varSerial, 'off', '', '', '')  # 打开待办事项，审核申请单


# Level_PO.close_driver()






# Level_PO.clickLinktext(u"注册", 2)
# if sys.argv[2] == "1":
#     Shouying_PO.register(sys.argv[1] + u"@cetc.cn", u"q123456", u"上海" + sys.argv[1] + u"生产企业", u"生产企业", sys.argv[1])
# elif sys.argv[2] == "2":
#     Shouying_PO.register(sys.argv[1] + u"@cetc.cn", u"q123456", u"上海" + sys.argv[1] + u"经营企业", u"经营企业", sys.argv[1])
# elif sys.argv[2] == "3":
#     Shouying_PO.register(sys.argv[1] + u"@cetc.cn", u"q123456", u"上海" + sys.argv[1] + u"公立医院", u"医疗机构 - 公立医院", sys.argv[1])
# elif sys.argv[2] == "4":
#     Shouying_PO.register(sys.argv[1] + u"@cetc.cn", u"q123456", u"上海" + sys.argv[1] + u"私立医院", u"医疗机构 - 私立医院", sys.argv[1])
# elif sys.argv[2] == "5":
#     Shouying_PO.register(sys.argv[1] + u"@cetc.cn", u"q123456", u"上海" + sys.argv[1] + u"诊所", u"医疗机构 - 诊所", sys.argv[1])
# elif sys.argv[2] == "6":
#     Shouying_PO.register(sys.argv[1] + u"@cetc.cn", u"q123456", u"上海" + sys.argv[1] + u"零售药店", u"零售药店", sys.argv[1])
#
# Level_PO.close_driver()

