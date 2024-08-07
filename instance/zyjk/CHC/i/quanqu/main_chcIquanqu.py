# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-8-6
# Description: 社区健康管理中心 接口
# 接口文档：http://192.168.0.202:22081/doc.html
# 测试环境 http://192.168.0.243:8010/#/login # 'cs', '12345678'
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
#***************************************************************

from ChcIquanquPO import *
ChcIquanqu_PO = ChcIquanquPO('{"username":"cs","password":"12345678","code":"","uuid":""}')

# todo【首页】
d_selectUserInfo = ChcIquanqu_PO.curl("用户信息", "GET", '/system/sysUser/selectUserInfo?0=', '{}')

d_systemMenuInfoBySystemId = ChcIquanqu_PO.curl("菜单", "GET", '/system/sysSystem/systemMenuInfoBySystemId?0=', '{"systemId":1}')
# print(d_systemMenuInfoBySystemId['data'][0]['name'], d_systemMenuInfoBySystemId['data'][0]['url'])  # 居民健康服务 /SignManage
# print(d_systemMenuInfoBySystemId['data'][0]['children'][0]['name'], d_systemMenuInfoBySystemId['data'][0]['children'][0]['url'])  # 健康服务 /SignManage/service

# # 3, 首页ehr信息
# d_getEhrHomeEhr = ChcIquanqu_PO.curl("POST", '/server/ehr/getEhrHomeEhr', '{"orgCode":"csdm","thirdNos":["cs"]}')
# print("首页ehr信息 =>", d_getEhrHomeEhr)

# # 4, 首页chc信息
# d_getChcHomeAssess = ChcIquanqu_PO.curl("POST", '/server/qyyh/getChcHomeAssess', '{"orgCode":"csdm","thirdNos":["cs"]}')
# print("首页chc信息 =>", d_getChcHomeAssess)
#

# 5，冠状病毒病是True
d_getCovidIsTrue = ChcIquanqu_PO.curl("冠状病毒病是True", "POST", '/server/covid/getCovidIsTrue')

# 6，冠状病毒病信息
d_getCovidInfo = ChcIquanqu_PO.curl("冠状病毒病信息", "POST", '/server/covid/getCovidInfo', '{"thirdNos":["cs"],"thirdOrgCode":"csdm"}')

#
# todo【1 居民健康服务】
# todo 1.1 健康服务
# {"categoryCode":"","endLastServiceDate":"","idCard":"","name":"","startLastServiceDate":"","thirdNo":"","current":1,"size":20}')
# name 姓名
# idCard 身份证
# categoryCode 人群分类
# thirdNo 家庭医生
# startLastServiceDate 上次服务日期
# endLastServiceDate 上次服务日期
# 健康服务列表页
# d_findServicePage = ChcIquanqu_PO.curl("POST", '/server/qyyh/findServicePage', '{"categoryCode":"","endLastServiceDate":"","idCard":"","name":"","startLastServiceDate":"","thirdNo":"","current":1,"size":20}')
# print("健康服务列表页 =>", d_findServicePage)
#
# # # 评估疾病
# d_getDictionaryAssess = ChcIquanqu_PO.curl("GET", '/system/sysDictionary/getDictionaryAssess')
# print("评估疾病 =>", d_getDictionaryAssess)
# #
# # # 家庭医生
# d_getSignFamilyDoc = ChcIquanqu_PO.curl("GET", '/server/qyyh/getSignFamilyDoc')
# print("家庭医生 =>", d_getSignFamilyDoc)
# #
# # # 服务模式
# d_getDictionaryService = ChcIquanqu_PO.curl("GET", '/system/sysDictionary/getDictionaryService')
# print("服务模式 =>", d_getDictionaryService)

# todo 1.2 健康评估及干预
# {"reportStatus":"","categoryCode":"","endSignDate":"","idCard":"","manageCode":[],"name":"","startSignDate":"","thirdNo":"","current":1,"size":10,"startLatestAssessDate":"","endLatestAssessDate":"","startLatestConfirmDate":"","endLatestConfirmDate":""}
# name 姓名
# idCard 身份证
# categoryCode 人群分类
# thirdNo 家庭医生
# startSignDate ，endSignDate 签约日期范围
# reportStatus 年度评估状态
# manageCode 管理人群
# "startLatestAssessDate":"","endLatestAssessDate":""," 最近一次评估日期
# startLatestConfirmDate":"","endLatestConfirmDate" 最近一次确认日期
# d_findPage = ChcIquanqu_PO.curl("POST", '/server/qyyh/findPage', '{"reportStatus":"","categoryCode":"","endSignDate":"","idCard":"","manageCode":[],"name":"","startSignDate":"","thirdNo":"","current":1,"size":10,"startLatestAssessDate":"","endLatestAssessDate":"","startLatestConfirmDate":"","endLatestConfirmDate":""}')
# print("健康评估及干预列表页 =>", d_findPage)
#
# # 管理人群
# d_getManageDic = ChcIquanqu_PO.curl("GET", '/system/sysDictionary/getManageDic')
# print("管理人群 =>", d_getManageDic)

# todo 1.3 慢病管理
# # {"thirdNos":["cs"],"thirdNo":"cs","orgCode":"csdm","current":1,"size":10,"thirdName":"测试人员超六个字"}
# d_getChronicList = ChcIquanqu_PO.curl("POST", '/server/ehr/getChronicList', '{"thirdNos":["cs"],"thirdNo":"cs","orgCode":"csdm","current":1,"size":10,"thirdName":"测试人员超六个字"}')
# print("慢病管理列表页 =>", d_getChronicList)
#
# todo 1.4 老年人体检
# # {"current":1,"size":10,"thirdNos":["cs"],"orgCode":"csdm"}
# d_getSnrList = ChcIquanqu_PO.curl("POST", '/server/ehr/getSnrList', '{"current":1,"size":10,"thirdNos":["cs"],"orgCode":"csdm"}')
# print("老年人体检列表页 =>", d_getSnrList)

# todo 1.5 重点人群
# d_getSnrList = ChcIquanqu_PO.curl("POST", '/server/covid/pageCovidInfo', '{"current":1,"size":10,"thirdNos":["cs"],"thirdOrgCode":"csdm"}')
# print("重点人群列表页 =>", d_getSnrList)
#
# todo【2 健康管理门诊】
# todo 2.1 居民登记
# todo 2.2 健康评估


# # todo【3 用户中心】
# # todo 3.1 机构维护
# d_getOrgPage = ChcIquanqu_PO.curl("POST", '/system/sysHospital/getOrgPage', '{"current":1,"size":1,"orgName":""}')
# print("机构维护列表页 =>", d_getOrgPage)

# # 机构类别（社区医院、区卫健委）
# d_getOrgCategory = ChcIquanqu_PO.curl("GET", '/system/sysHospital/getOrgCategory')
# print("机构类别 =>", d_getOrgCategory)

# 新增（未处理）

# todo 3.2用户维护

# 人员类别
# d_getDictionaryUser = ChcIquanqu_PO.curl("GET", '/system/sysDictionary/getDictionaryUser')
# print("人员类别 =>", d_getDictionaryUser)

# # 机构列表
# d_getOrgList = ChcIquanqu_PO.curl("POST", '/system/sysHospital/getOrgList')
# print("机构列表 =>", d_getOrgList)

# # 机构维护列表页
# a = ChcIquanqu_PO.encrypt('{"current":1,"size":10}')
# d_findPageByIdAndName = ChcIquanqu_PO.curl("POST", '/system/sysUser/findPageByIdAndName?0=' + a, '{}')
# print("机构维护列表页 =>", d_findPageByIdAndName)

# 新增（未处理）

# todo 3.3 角色维护

# # 所属系统（社区健康管理中心）
# d_findList = ChcIquanqu_PO.curl("POST", '/system/sysSystem/findList', '{}')
# print("所属系统 =>", d_findList)
#
# # 角色维护列表页
# a = ChcIquanqu_PO.encrypt('{"current":1,"size":10}')
# d_findPage = ChcIquanqu_PO.curl("POST", '/system/sysRole/findPage?0=' + a, '{"current":1,"size":10}')
# print("角色维护列表页 =>", d_findPage)

# 新增（未处理）


# todo 3.4 接口管理
# 角色管理列表页
# a = ChcIquanqu_PO.encrypt('{"current":1,"size":10}')
# d_findPage = ChcIquanqu_PO.curl("POST", '/system/sysThirdKey/findPage?0=' + a, '{"current":1,"size":10}')
# print("角色管理列表页 =>", d_findPage)

# 新增（未处理）

# todo 3.5 批量评估

# # 机构列表
# d_getOrgList = ChcIquanqu_PO.curl("POST", '/system/sysHospital/getOrgList', 'csdm')
# print("机构列表 =>", d_getOrgList)

# # # 批量评估列表页
# a = ChcIquanqu_PO.encrypt('{"current":1,"size":10}')
# d_page = ChcIquanqu_PO.curl("POST", '/server/tAssessBatch/page?0=' + a, '{"current":1,"size":10}')
# print("批量评估列表页 =>", d_page)

# todo 3.6 错误日志

# 错误日志列表页
# d_getAssessProcess = ChcIquanqu_PO.curl("POST", '/server/tAssessInfo/getAssessProcess', '{"current":1,"size":10}')
# print("错误日志列表页 =>", d_getAssessProcess)


# todo【4 社区配置】

# todo 4.1 常住人口
# 常住人口
# d_getBasic = ChcIquanqu_PO.curl("GET", '/server/tBasicInfo/getBasic')
# print("常住人口 =>", d_getBasic)
#
# # 常住人口列表页
# d_findPage = ChcIquanqu_PO.curl("POST", '/server/tBasicPerson/findPage', '{"current":1,"size":10,"idCard":"","name":""}')
# print("常住人口列表页 =>", d_findPage)


# todo 4.2 家医团队维护
# 家医团队维护列表页
# d_findTeamPage = ChcIquanqu_PO.curl("POST", '/server/tTeam/findTeamPage', '{"current":1,"size":10}')
# print("家医团队维护列表页 =>", d_findTeamPage)

# 新增（未处理）

# todo 4.3 家医助手
# # 家医助手列表页
# d_assistantPage = ChcIquanqu_PO.curl("POST", '/server/tAssistant/assistantPage', '{"current":1,"size":10}')
# print("家医助手列表页 =>", d_assistantPage)


# todo 4.4 干预规则配置
# # 干预规则配置列表页
# d_findServiceList = ChcIquanqu_PO.curl("POST", '/server/tInterveneConfig/findServiceList', '{"current":1,"size":10}')
# print("干预规则配置列表页 =>", d_findServiceList)


# todo 4.5 停止评估名单
# 停止评估名单列表页
# d_getStopAssessPage = ChcIquanqu_PO.curl("POST", '/server/qyyh/getStopAssessPage', '{"current":1,"size":10}')
# print("停止评估名单列表页 =>", d_getStopAssessPage)

# 新增（未处理）

# todo 4.6 社区用户维护
# # 社区用户维护列表页
# a = ChcIquanqu_PO.encrypt('{"current":1,"size":10}')
# d_getStopAssessPage = ChcIquanqu_PO.curl("POST", '/system/sysUser/findPageByIdAndName?0=' + a, '{"orgCode":"csdm"}')
# print("社区用户维护列表页 =>", d_getStopAssessPage)
#
# # 人员类型
# d_getDictionaryUser = ChcIquanqu_PO.curl("GET", '/system/sysDictionary/getDictionaryUser')
# print("人员类型 =>", d_getDictionaryUser)
#
# # 机构页
# d_getOrgPage = ChcIquanqu_PO.curl("POST", '/system/sysHospital/getOrgPage', '{"current":1,"size":99999}')
# print("机构页 =>", d_getOrgPage)


# todo 4.7 评估建议
# # 评估建议列表页
# d_getInterveneTemplate = ChcIquanqu_PO.curl("POST", '/server/tInterveneConfig/getInterveneTemplate', '{"current":1,"size":10}')
# print("评估建议列表页 =>", d_getInterveneTemplate)
#
# # 评估疾病
# d_getDictionaryAssess = ChcIquanqu_PO.curl("GET", '/system/sysDictionary/getDictionaryAssess')
# print("评估疾病 =>", d_getDictionaryAssess)


# todo【5 系统监控】

# todo 5.1 定时任务
# 定时任务列表页
# d_list = ChcIquanqu_PO.curl("GET", '/schedule/job/list?0=', '{"pageNum":1,"pageSize":10}')
# print("定时任务列表页 =>", d_list)

# 新增（未处理）

# todo【6 重点人群管理】

# todo 6.1 人群管理
# d_getThirdToken = ChcIquanqu_PO.curl("POST", '/system/sysUser/getThirdToken?0=' + ChcIquanqu_PO.encrypt('{"appId":1}'))
# print("定时任务列表页 =>", d_getThirdToken)






