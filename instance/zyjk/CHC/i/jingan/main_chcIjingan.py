# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-3-6
# Description   : CHC 社区健康接口测试（静安）
# 接口文档：http://192.168.0.202:22081/doc.html
# 测试环境: http://192.168.0.202:22080/ lbl,Ww123456

# # 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
public_key = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'

# todo nacos
# http://192.168.0.223:8848/nacos/	nacos,Zy123456
# chc-test
# chc-gateway-sqlserver.yml
# enabled: false    // 改为false无法登录，因为页面加密，用于接口测试
# 安全配置
# # security:
#   验证码
#   # captcha:
#   #   enabled: false    //去掉验证码

# 【腾讯文档】项目信息表
# https://docs.qq.com/sheet/DYmZMVmFTeXFWRFpQ?tab=BB08J2
# *****************************************************************

from ChcIjinganPO import *
ChcIjingan_PO = ChcIjinganPO('{"username":"lbl","password":"Ww123456","code":"1","uuid":""}')


# 1，获取菜单
d = ChcIjingan_PO.curl("GET", '/system/sysSystem/systemMenuInfoBySystemId?0=', '{"systemId":1}')
print(d)  # {'code': 200, 'msg': None, 'data': [{'id': 2, 'systemId': 1, 'name': '居民健康服务', 'paren...
print(d['data'][0]['name'], d['data'][0]['url'])  # 居民健康服务 /SignManage
print(d['data'][0]['children'][0]['name'], d['data'][0]['children'][0]['url'])  # 健康服务 /SignManage/service



# # 登录(lbl,Ww123456)
# # 注意需要关闭验证码
# ChcIjingan_PO = ChcIjinganPO('9580414215bd76bf8ddd310c894fdfb155f439b427a43fb3dbb13a142055e4b7236fd7498a6e8d2febc7a44688c45d68c11606a34632ce07aa94d037124c0c15c0a19ab3c9f35bab234dd5bc8a3b37d419786c17b2e26d46d0f378e3691f2823e48804aecfb23ebc8511fd66e9b927bb5344d97a9f6c9c001ba4e76865f4890a5c6f7c21810fdedf6bbe85625e6ca990e1fe1cef025760c3382326c993')
#


# # todo chc-system, REST-系统信息表
# # print(ChcIjingan_PO.querySystemRole(userId))  # 获取所有系统的角色
# print(ChcIjingan_PO.systemMenuInfoBySystemId())  # 根据用户ID获取能够使用的系统
# # print(ChcIjingan_PO.systemMenuInfo(systemId))  # 获取系统菜单
# # print(ChcIjingan_PO.systemMenuInfoBySystemId(systemId))  # 根据系统Id获取所有菜单
# # print(ChcIjingan_PO.sysSystem(Id))  # 单条查询
#
#
# # todo chc-system, REST-用户信息表
# # print(ChcIjingan_PO.getFamilyDoc())  # 获取家庭医生
# # print(ChcIjingan_PO.getAssistantList())  # 获取家医助手
# # print(ChcIjingan_PO.getHealthManagerList())  # 获取健康管理师
# # print(ChcIjingan_PO.getUser())  # 根据用户名获取用户信息
# # print(ChcIjingan_PO.getUserByOrg())  # 根据机构获取医生
# # print(ChcIjingan_PO.getUserConfigByThird(orgCode,thirdNO))  # 获取用户配置信息
# # print(ChcIjingan_PO.getUserInfoByThirdNo(thirdNO))  # 根据用户名获取用户信息
# # print(ChcIjingan_PO.getUserInfoByThirdNoAndOrgCode(orgCode,thirdNO))  # 根据用户名和机构号获取用户信息
# # print(ChcIjingan_PO.getUserInfoThirdInfo(orgCode,thirdNO))  # 根据用户名获取用户信息
# print(ChcIjingan_PO.selectUserInfo())  # 根据token获取用户信息
# # print(ChcIjingan_PO.sysUser(id))  # 单条查询
#
#
# # todo chc-auth, 登录模块
# print(ChcIjingan_PO.logout())  # 登出
