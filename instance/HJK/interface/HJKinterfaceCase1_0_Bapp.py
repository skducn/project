# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2017-10-17
# Description: 慧健康1.0 B端app 接口
# https://md5jiami.51240.com/  MD5在线加密
# *******************************************************************************************************************************

from CETCinterfaceDriver import *
from Public.PageObject.DatabasePO import *
Database_PO = DatabasePO('10.111.3.4', 3306, 'cetc', '20121221', 'hjk')


# 测试帐号（手机号）
varAdmin = sheet0.cell_value(12, 1)
varUser9051 = sheet0.cell_value(13, 1)
varUser9052 = sheet0.cell_value(14, 1)
varPass = u"a123456"
varPhone = u"13816109056"


'''个人中心'''


resp = Icase("用户登录","bapp1_N1_C1", varUser9051, varPass)
varUserId = resp.split('userId":')[1].split(",")[0]
print u"varUserId = " + varUserId


resp = Icase("用户退出","bapp1_N2_C1", varUserId, varSessionId)
resp = Icase("修改密码","bapp1_N3_C1", varUserId, varSessionId, varPass, u"a111111")
resp = Icase("用户相关机构列表","bapp1_N3_C1", varUserId, varSessionId)
resp = Icase("切换机构列表","bapp1_N4_C1", varUserId, varSessionId, varOrgId, varOfficeId)
resp = Icase("意见反馈","bapp1_N2_C1", varUserId, varSessionId, u"医生的意见反馈")

