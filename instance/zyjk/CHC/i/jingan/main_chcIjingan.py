# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-3-6
# Description   : CHC 社区健康接口测试（静安）
# 接口文档：http://192.168.0.202:22081/doc.html
# 测试环境: http://192.168.0.202:22080/ lbl,Ww123456
# https://www.sojson.com/
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


# todo【1 首页】
# # 1, 获取登录人信息
# d_selectUserInfo = ChcIjingan_PO.curl("GET", '/system/sysUser/selectUserInfo?0=', '{}')
# print("用户信息 =>", d_selectUserInfo)
#
# # # 2，获取菜单
# d_systemMenuInfoBySystemId = ChcIjingan_PO.curl("GET", '/system/sysSystem/systemMenuInfoBySystemId?0=', '{"systemId":1}')
# print("菜单 =>", d_systemMenuInfoBySystemId)  # {'code': 200, 'msg': None, 'data': [{'id': 2, 'systemId': 1, 'name': '居民健康服务', 'paren...
# print(d_systemMenuInfoBySystemId['data'][0]['name'], d_systemMenuInfoBySystemId['data'][0]['url'])  # 居民健康服务 /SignManage
# print(d_systemMenuInfoBySystemId['data'][0]['children'][0]['name'], d_systemMenuInfoBySystemId['data'][0]['children'][0]['url'])  # 健康服务 /SignManage/service


# todo【2 签约居民管理】
# todo 2.1 健康服务
# d_getSignFamilyDoc = ChcIjingan_PO.curl("家庭医生", "GET", '/server/qyyh/getSignFamilyDoc')
# d_getDictionaryService = ChcIjingan_PO.curl("服务模式", "GET", '/system/sysDictionary/getDictionaryService')
# d_findServicePage = ChcIjingan_PO.curl("健康服务列表页", "POST", '/server/qyyh/findServicePage', '{"categoryCode":"","endLastServiceDate":"","idCard":"","name":"","startLastServiceDate":"","thirdNo":"","current":1,"size":10}')
# d_getHealthService = ChcIjingan_PO.curl("健康服务", "GET", '/server/qyyh/getHealthService')
# d_getDictionaryAssess = ChcIjingan_PO.curl("评估疾病", "GET", '/system/sysDictionary/getDictionaryAssess')

# todo 2.2 健康评估
# d_findPage = ChcIjingan_PO.curl("健康评估列表页", "POST", '/server/qyyh/findPage', '{"reportStatus":null,"categoryCode":"","endSignDate":"","idCard":"","name":"","startSignDate":"","thirdNo":"","current":1,"size":10}')
# d_getDocInfo = ChcIjingan_PO.curl("家庭医生", "GET", '/server/qyyh/getDocInfo')
# d_123123 = ChcIjingan_PO.curl("评估统计", "GET", '/server/qyyh/getAssessStatistics/123123')

# todo 2.3 居民反馈
# d_page = ChcIjingan_PO.curl("居民反馈列表页", "POST", '/server/tHealthFeedback/page', '{"current":1,"size":10}')


# todo【3 健康管理门诊】
# todo 3.1 居民登记
# todo 3.2 健康评估


# # todo【4 用户中心】
# # # todo 4.1 机构维护
# d_getOrgPage = ChcIjingan_PO.curl("机构维护列表页", "POST", '/system/sysHospital/getOrgPage', '{"current":1,"size":10}')
# d_getOrgCategory = ChcIjingan_PO.curl("机构类别", "GET", '/system/sysHospital/getOrgCategory')
# # 新增（未处理）
#
# # todo 3.2用户维护
# d_getOrgList = ChcIjingan_PO.curl("机构列表", "POST", '/system/sysHospital/getOrgList')
# d_getDictionaryUser = ChcIjingan_PO.curl("人员类别", "GET", '/system/sysDictionary/getDictionaryUser')
# d_findPageByIdAndName = ChcIjingan_PO.curl("机构维护列表页", "POST", '/system/sysUser/findPageByIdAndName?0=' + ChcIjingan_PO.encrypt('{"current":1,"size":10}'), '{}')
# # 新增（未处理）
#
# # todo 3.3 角色维护
# d_findList = ChcIjingan_PO.curl("所属系统", "POST", '/system/sysSystem/findList', '{}')
# d_findPage = ChcIjingan_PO.curl("角色维护列表页", "POST", '/system/sysRole/findPage?0=' + ChcIjingan_PO.encrypt('{"current":1,"size":10}'), '{"current":1,"size":10}')
# # 新增（未处理）
#
# # todo 3.4 接口管理
# d_findPage = ChcIjingan_PO.curl("角色管理列表页", "POST", '/system/sysThirdKey/findPage?0=' + ChcIjingan_PO.encrypt('{"current":1,"size":10}'), '{"current":1,"size":10}')
# # 新增（未处理）
#
# # todo 3.5 错误日志
# d_getAssessProcess = ChcIjingan_PO.curl("错误日志列表页", "POST", '/server/tHealthAssess/getAssessProcess', '{"current":1,"size":10}')


# todo【4 资源配置管理】
# # todo 4.1 实有人口管理
# d_getBasic = ChcIjingan_PO.curl("常住人口", "GET", '/server/tBasicInfo/getBasic')
# d_findPage = ChcIjingan_PO.curl("常住人口列表页", "POST", '/server/tBasicPerson/findPage', '{"current":1,"size":10,"idCard":"","name":""}')
# d_findTeamPage = ChcIjingan_PO.curl("常住人口团队列表页", "POST", '/server/tTeam/findTeamPage', '{"current":1,"size":10}')

# # todo 4.2 家医团队管理
# d_findTeamPage = ChcIjingan_PO.curl("家医团队管理列表页", "POST", '/server/tTeam/findTeamPage', '{"current":1,"size":10}')
#
# # todo 4.3 家医助手管理
# d_assistantPage = ChcIjingan_PO.curl("家医助手管理列表页", "POST", '/server/tAssistant/assistantPage', '{"current":1,"size":10}')
# # # 新增（未处理）
#
# # todo 4.4 儿童健康建议
# d_findServiceList = ChcIjingan_PO.curl("儿童健康建议列表页", "POST", '/server/tInterveneConfig/findServiceList', '{"current":1,"size":10}')

# todo 4.5 停止评估名单
# d_getStopAssessPage = ChcIjingan_PO.curl("停止评估名单列表页", "POST", '/server/qyyh/getStopAssessPage', '{"current":1,"size":10}')
# # # # 新增（未处理）
#
# # todo 4.6 社区用户维护
# d_getStopAssessPage = ChcIjingan_PO.curl("社区用户维护列表页", "POST", '/system/sysUser/findPageByIdAndName?0=' + ChcIjingan_PO.encrypt('{"current":1,"size":10}'), '{"orgCode":"0000001"}')
# d_getOrgPage = ChcIjingan_PO.curl("机构列表", "POST", '/system/sysHospital/getOrgList')
# d_getDictionaryUser = ChcIjingan_PO.curl("人员类型", "GET", '/system/sysDictionary/getDictionaryUser')

# todo【5 系统监控】
# todo 5.1 定时任务
# d_list = ChcIjingan_PO.curl("定时任务列表页", "GET", '/schedule/job/list?0=', '{"pageNum":1,"pageSize":10}')
# 新增（未处理）


# todo【6 社区驾驶舱】
# todo 6.1 社区中心


# todo【7 重点人群管理】
# todo 7.1 人群管理









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
