# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-3-6
# Description   : CHC 加密接口测试（静安），无场景
# 接口文档：http://192.168.0.202:22081/doc.html
# *****************************************************************

from Chc_i_PO import *


# 登录
chc_i_PO = Chc_i_PO()

# 根据用户ID获取能够使用的系统（系统信息表）
print(chc_i_PO.systemMenuInfoBySystemId())

# 根据token获取用户信息（用户信息表）
print(chc_i_PO.selectUserInfo())

# 登出
print(chc_i_PO.logout())
