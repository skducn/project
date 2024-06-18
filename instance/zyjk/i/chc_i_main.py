# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-3-6
# Description   : CHC 社区健康接口测试（静安）
# 接口文档：http://192.168.0.202:22081/doc.html
# web:http://192.168.0.202:22080/ lbl,Ww123456
# 【腾讯文档】项目信息表
# https://docs.qq.com/sheet/DYmZMVmFTeXFWRFpQ?tab=BB08J2
# *****************************************************************

from Chc_i_PO import *


# 登录(lbl,Ww123456)
chc_i_PO = Chc_i_PO('9580414215bd76bf8ddd310c894fdfb155f439b427a43fb3dbb13a142055e4b7236fd7498a6e8d2febc7a44688c45d68c11606a34632ce07aa94d037124c0c15c0a19ab3c9f35bab234dd5bc8a3b37d419786c17b2e26d46d0f378e3691f2823e48804aecfb23ebc8511fd66e9b927bb5344d97a9f6c9c001ba4e76865f4890a5c6f7c21810fdedf6bbe85625e6ca990e1fe1cef025760c3382326c993')

# todo chc-system, REST-系统信息表
# print(chc_i_PO.querySystemRole(userId))  # 获取所有系统的角色
print(chc_i_PO.systemMenuInfoBySystemId())  # 根据用户ID获取能够使用的系统
# print(chc_i_PO.systemMenuInfo(systemId))  # 获取系统菜单
# print(chc_i_PO.systemMenuInfoBySystemId(systemId))  # 根据系统Id获取所有菜单
# print(chc_i_PO.sysSystem(Id))  # 单条查询


# todo chc-system, REST-用户信息表
# print(chc_i_PO.getFamilyDoc())  # 获取家庭医生
# print(chc_i_PO.getAssistantList())  # 获取家医助手
# print(chc_i_PO.getHealthManagerList())  # 获取健康管理师
# print(chc_i_PO.getUser())  # 根据用户名获取用户信息
# print(chc_i_PO.getUserByOrg())  # 根据机构获取医生
# print(chc_i_PO.getUserConfigByThird(orgCode,thirdNO))  # 获取用户配置信息
# print(chc_i_PO.getUserInfoByThirdNo(thirdNO))  # 根据用户名获取用户信息
# print(chc_i_PO.getUserInfoByThirdNoAndOrgCode(orgCode,thirdNO))  # 根据用户名和机构号获取用户信息
# print(chc_i_PO.getUserInfoThirdInfo(orgCode,thirdNO))  # 根据用户名获取用户信息
print(chc_i_PO.selectUserInfo())  # 根据token获取用户信息
# print(chc_i_PO.sysUser(id))  # 单条查询


# todo chc-auth, 登录模块
print(chc_i_PO.logout())  # 登出
