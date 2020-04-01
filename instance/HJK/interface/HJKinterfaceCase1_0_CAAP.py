# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2017-10-17
# Description: 慧健康1.0 C端app接口 患者端
# https://md5jiami.51240.com/  MD5在线加密
# http://shenfenzheng.293.net/?_t_t_t=0.0596391458529979  身份证测试数据

# *******************************************************************************************************************************

from CETCinterfaceDriver import *
from Public.PageObject.DatabasePO import *
Database_PO = DatabasePO('10.111.3.4', 'cetc', '20121221', 'hjk')


# 测试帐号（手机号）
varDoctor1 = sheet0.cell_value(17, 1)
varPass = u"a123456"


'''用户信息'''

# resp = Icase("用户注册","capp1_N1_C1", varDoctor1, u"a123456")
resp = Icase("用户登录","capp1_N2_C1", varDoctor1, u"a123456")
varUserId = resp.split('userId":')[1].split(",")[0].replace('"', '')
varUserSessionId = resp.split('userSessionId":')[1].split(",")[0].replace('"', '')
print u"varUserId = " + varUserId
print u"varUserSessionId = " + varUserSessionId

# resp = Icase("用户登出","capp1_N3_C1", varUserId, varUserSessionId)
# resp = Icase("忘记密码","capp1_N4_C1", varDoctor1, u"a123456")

resp = Icase("视频设置","capp1_N5_C1", varUserId, varUserSessionId,u"1",u"1")
resp = Icase("视频设置","capp1_N5_C2", varUserId, varUserSessionId,u"1",u"2")
resp = Icase("视频设置","capp1_N5_C3", varUserId, varUserSessionId,u"1",u"3")
resp = Icase("视频设置","capp1_N5_C4", varUserId, varUserSessionId,u"0",u"1")
resp = Icase("视频设置","capp1_N5_C5", varUserId, varUserSessionId,u"0",u"2")
resp = Icase("视频设置","capp1_N5_C6", varUserId, varUserSessionId,u"0",u"3")

resp = Icase("是否推送消息设置","capp1_N6_C1", varUserId, varUserSessionId,u"0")
resp = Icase("是否推送消息设置","capp1_N6_C2", varUserId, varUserSessionId,u"1")


'''机构信息'''


resp = Icase("诊所列表获取","capp1_N8_C1", varUserId, varUserSessionId,u"1", u"10")
varOrgId = resp.split('orgId":')[1].split(",")[0].replace('"', '')  # 当有多个返回值，直接修改[1]，如[2]获取第二个符合条件的值。
print u"varOrgId = " + varOrgId
varName = resp.split('name":')[1].split(",")[0].replace('"', '')  # 当有多个返回值，直接修改[1]，如[2]获取第二个符合条件的值。
print u"varName = " + varName

resp = Icase("根据诊所名称或科室名称检索诊室列表","capp1_N7_C1", varUserId, varName, u"",u"1", u"10")

resp = Icase("诊所详情","capp1_N9_C1", varUserId, varUserSessionId,varOrgId)

'''科室信息'''

resp = Icase("科室列表","capp1_N10_C1", varUserId, varUserSessionId,u"1", u"10")
varOfficeId = resp.split('officeId":')[1].split(",")[0].replace('"', '')  # 当有多个返回值，直接修改[1]，如[2]获取第二个符合条件的值。
print u"varOfficeId = " + varOfficeId

resp = Icase("科室详情","capp1_N11_C1", varUserId, varUserSessionId,varOfficeId)

'''医生信息'''

resp = Icase("医生列表","capp1_N12_C1", varUserId, varUserSessionId,varOrgId,u"1", u"10")
varDoctorId = resp.split('doctorId":')[1].split(",")[0].replace('"', '')  # 当有多个返回值，直接修改[1]，如[2]获取第二个符合条件的值。
print u"varDoctorId = " + varDoctorId

resp = Icase("医生详情","capp1_N13_C1", varUserId, varUserSessionId,varDoctorId)

'''患者信息'''

resp = Icase("就诊人列表获取","capp1_N14_C1", varUserId, varUserSessionId,u"1", u"10")

resp = Icase("我的基本信息","capp1_N15_C1", varUserId, varUserSessionId)
varPatientId = resp.split('patientId":')[1].split(",")[0].replace('"', '')  # 当有多个返回值，直接修改[1]，如[2]获取第二个符合条件的值。
print u"varPatientId = " + varPatientId

resp = Icase("修改患者基本信息","capp1_N16_C1", varUserId, varUserSessionId,varPatientId, u"1", u"张三")

# http://shenfenzheng.293.net/?_t_t_t=0.0596391458529979  身份证测试数据
resp = Icase("添加就诊人信息","capp1_N17_C1", varUserId, varUserSessionId,u"鲍子裕",u"522629198409301016",u"1",u"13016109050",u"1")


'''关注'''

resp = Icase("我关注的医生列表","capp1_N18_C1", varUserId, varUserSessionId,u"1", u"10")

resp = Icase("关注医生","capp1_N19_C1", varUserId, varUserSessionId,varDoctorId)

resp = Icase("取消关注医生","capp1_N20_C1", varUserId, varUserSessionId,varDoctorId)

resp = Icase("我关注的诊所列表","capp1_N21_C1", varUserId, varUserSessionId,u"1", u"10")

resp = Icase("关注诊所","capp1_N22_C1", varUserId, varUserSessionId,varOrgId)

resp = Icase("取消关注诊所","capp1_N23_C1", varUserId, varUserSessionId,varOrgId)



