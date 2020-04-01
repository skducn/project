# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 2.0
# Date       : 2017-11-6
# Description: 电科党员学习教育WEB平台, 获取架构及用户管理
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from Dangjian.Config.config import *
from Dangjian.PageObject.Dangjian20PO import *
Dangjian20_PO = Dangjian20PO()
# from android1_5 import AppDangjian
from random import choice
from selenium.webdriver.common.keys import Keys
varTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 当天日期时间时分秒，格式：20170914143616982，类型是 str，
varYMD = datetime.datetime.now().strftime('%Y-%m-%d')  # 当天日期年月日，格式：2016-06-28 ， 类型是 str


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 生产环境
varUrlPrefix = u"http://meeting.iotcetc.com"  # 访问URL
varFstAccount = u"wuxiaohao"   # 登录帐号 13816109060
varPass = u"a12345"   # 密码
varArchitecture = u"软信测试第一支部"  # 帐号角色   , 软信测试第一支部


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


print u">>>>>>>>>>>>>>>>>>>>>>>>>>> 架构及用户管理 >>>>>>>>>>>>>>>>>>>>>>>>>>>"

'''登录'''

Level_PO.openURL(1200, 900, varUrlPrefix + u"/dangjian1.5/web/app.php/DJsecurity/security/login", 3)
Level_PO.inputID(u"_username", varFstAccount)
Level_PO.inputID(u"_password", varPass)
Level_PO.inputID(u"_captcha", Level_PO.getCode(u"test.jpg", 2060, 850, 2187, 900))  # 获取并输入验证码
Level_PO.clickTAGNAME(u'button', 2)
# 多次遍历获取并输入验证码
for i in range(100):
    if Level_PO.isElementId(u"_captcha"):
        Level_PO.inputID(u"_username", varFstAccount)
        Level_PO.inputID(u"_password", varPass)
        Level_PO.inputID(u"_captcha", Level_PO.getCode(u"test1.jpg", 2060, 792, 2187, 849))
        Level_PO.clickTAGNAME(u'button', 2)
    else:
        break
Level_PO.setMaximize()
print u"S1, 已登录 -> " + varFstAccount + u""


varOrgUsers = Dangjian20_PO.orgUsers(u"软信测试第一支部")



'''用户及权限管理'''

Level_PO.clickLINKTEXT(u'用户及权限管理', 2)
Level_PO.clickLINKTEXT(u'架构及用户管理', 10)

listA = []
listA = Level_PO.getList_XpathsText(u"//ul[@id='treeDemo']/li/ul/li")
print listA
print len(listA)


print "end"

