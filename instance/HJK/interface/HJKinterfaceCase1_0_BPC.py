# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2017-10-17
# Description: 慧健康1.0 B端PC接口 医生端
# https://md5jiami.51240.com/  MD5在线加密
# 接口URL：http://101.230.200.46:8094/smartHealth
# GPS经纬度：http://www.gpsspg.com/maps.htm   //百度地图：31.2349342624,121.5242938920  北纬31， 东经121
# python颜色输出规则，www.cnblogs.com/yinjia/p/5559702.html
# *******************************************************************************************************************************

import sys
sys.path.append('D:\\51\\Python\\09project')  # 如果要在cmd中执行python，需要加上路径，否则 public.PageObject.DatabasePO无法找到这个模块。
from CETCinterfaceDriver import *
from Public.PageObject.DatabasePO import *
from Public.PageObject.ThirdPO import *

Database_PO = DatabasePO('10.111.3.4', 3306, 'cetc', '20121221', 'hjk')
Third_PO = ThirdPO()

import redis, hashlib
connRedis = redis.StrictRedis(host='10.111.3.4', port=6379, db=0, password="b840fc02d524045429941cc15f59e41cb7be6c52")

# 测试帐号（手机号）
# varAdmin = sheet0.cell_value(12, 1)
# varUser9051 = sheet0.cell_value(13, 1)
# varUser9052 = sheet0.cell_value(14, 1)

varPhone = u"15123123123"
varPass = u"111111"
m = hashlib.md5()
m.update(varPass)



'''1.5 用户信息'''
resp = Icase("RtnOK", "获取验证码", "bpc1_N1_C1", varPhone)
resp = Icase("RtnOK", "检验验证码", "bpc1_N2_C1", varPhone, connRedis.get('msg_' + varPhone))
resp = Icase("RtnParamErr", "检验验证码", "bpc1_N2_C1", varPhone, "0")

# ？？注册功能，非本次需求
# resp = Icase("诊所管理员注册","bpc1_N3_C1", u"13816109050", u"111111")

resp = Icase("RtnOK", "用户登录", "bpc1_N4_C1", varPhone, m.hexdigest())
doctorId = resp.split('doctorId":')[1].split(",")[0]
officeId = resp.split('officeId":')[1].split(",")[0].replace('"', "")
print u"doctorId = " + doctorId
print u"officeId = " + officeId + "\n"

resp = Icase("RtnOK", "用户登出", "bpc1_N5_C1", doctorId)
resp = Icase("RtnParamErr", "用户登出", "bpc1_N5_C2", "0")

resp = Icase("RtnOK", "重置密码", "bpc1_N6_C1", varPhone, m.hexdigest())

#？ 与产品，开发沟通，只有基础班
resp = Icase("RtnOK", "商品信息列表", "bpc1_N7_C1", u"1", u"1", u"1")  # 基础版，条数，页码



'''1.6 用户信息'''

resp = Icase("RtnOK", "科室列表", "bpc1_N8_C1", u"1")   # names":["内科","外科","中医","口腔","妇科"]
names = resp.split('names":')[1].split("}")[0]
print u"names = " + str(names).decode("utf-8") + "\n"

resp = Icase("RtnOK", "科室中是否有人员存在","bpc1_N9_C1", officeId)
if resp.split('validateResult":"')[1].split('"}')[0] != "1" : print "[Errorrrrrrrrrr]"

resp = Icase("RtnOK", "科室中是否有人员存在","bpc1_N9_C2", "111111111")
if resp.split('validateResult":"')[1].split('"}')[0] != "0" : print "[Errorrrrrrrrrr]"


# import base64
# f = open(r'/Users/linghuchong/Downloads/51/Picture/100.jpg', 'rb') #二进制方式打开图文件
# imageBase = base64.b64encode(f.read()) #读取文件内容，转换为base64编码
# f.close()
# resp = Icase("RtnOK", "上传图片", "bpc1_N10_C1", "71", imageBase, "1")

resp = Icase("RtnOK", "获取科室信息", "bpc1_N11_C1", officeId)
orgId = resp.split('orgId":')[1].split(",")[0].replace('"', "")
print u"orgId = " + orgId + "\n"


resp = Icase("RtnOK", "获取科室的医生信息", "bpc1_N12_C1", officeId)

resp = Icase("RtnOK", "获取多机构、科室信息", "bpc1_N13_C1", doctorId)

resp = Icase("RtnOK", "获取机构、科室信息", "bpc1_N14_C1", orgId)


'''1.7 订单管理 '''

resp = Icase("RtnOK", "机构历史订单列表", "bpc1_N18_C1", orgId)

resp = Icase("RtnOK", "机构订单信息", "bpc1_N19_C1", orgId)


'''1.8 机构管理 '''

resp = Icase("RtnOK", "机构信息列表", "bpc1_N21_C1", doctorId, u"",  u"1", u"1")
resp = Icase("RtnOK", "药房信息列表", "bpc1_N22_C1", doctorId, u"",  u"1", u"1")

resp = Icase("RtnOK", "保存排序号", "bpc1_N23_C1", "120", u"1")


# # 机构管理 - 新增，查看，修改，级科室列表 一套
# resp = Icase("机构管理-新增","bpc1_N24_C1", u"121.5242938920",  u"31.2349342624", doctorId, u"上海南极人", u"1", u"https://www.baidu.com/img/bd_logo1.png", u"http://www.xitongcheng.com/images/logo.JPG", u"http://www.xitongcheng.com/images/logo.JPG", u"http://www.xitongcheng.com/images/logo.JPG")
# newOrgId = resp.split('orgId":')[1].split(",")[0].replace('"',"")
# print u"newOrgId = " + newOrgId
# resp = Icase("机构管理-查看","bpc1_N25_C1", newOrgId)
# resp = Icase("机构管理-修改","bpc1_N26_C1", newOrgId, u"121.5242938920", u"31.2349342620", u"上海南极人有限公司", u"上南", u"上海市南极人股份有限公司", u"021-56554433", u"2", u"1", u"1", u"https://www.baidu.com/img/bd_logo1.png", u'{\\"type\\":\\"全部\\",\\"end\\":\\"14\\",\\"begin\\":\\"9\\"}', u"http://www.xitongcheng.com/images/logo.JPG", u"http://www.xitongcheng.com/images/logo.JPG", u"13816108080", u"zhifubao", u"http://www.xitongcheng.com/images/logo.JPG", u"http://www.xitongcheng.com/images/logo.JPG", u"http://www.xitongcheng.com/images/logo.JPG", u"单位描述信息",u"")
# resp = Icase("科室-列表","bpc1_N27_C1", newOrgId)
# resp = Icase("科室查看","bpc1_N29_C1", officeId)
# resp = Icase("科室名称下拉列表","bpc1_N30_C1", newOrgId)

# # 随机生成中文作为科室名
# varOfficeName1 =  Third_PO.randomOffice()
# resp = Icase("科室新增","bpc1_N31_C1", orgId, varOfficeName1, u"科室简称1", u"科室全称1", u"13816102030", u"22", u"1", u"科室描述1")
# newOfficeId = Database_PO.tblWhere1Get1("tt_office", "name", varOfficeName1, "office_id")
# print u"newOfficeId = " + newOfficeId
# resp = Icase("科室修改","bpc1_N32_C1", newOfficeId, u"科室名1revise", u"科室简称1revise", u"科室全称1revise", u"13816102099", u"3", u"0", u"科室描述1revise")

# '''1.8.2 科室订单 '''
#
# resp = Icase("科室订单","bpc1_N33_C1", newOrgId, u"1")
# resp = Icase("科室订单","bpc1_N33_C2", newOrgId, u"2")

'''1.9 组织管理 '''

resp = Icase("RtnOK", "人员管理列表","bpc1_N34_C1", orgId, doctorId, u"",u"",u"",u"0",u"1",u"1")
resp = Icase("RtnOK", "人员管理列表","bpc1_N34_C2", orgId, doctorId, u"",u"",u"",u"1",u"1",u"1")
resp = Icase("RtnOK", "人员管理列表","bpc1_N34_C3", orgId, doctorId, u"",u"",u"",u"2",u"1",u"1")
resp = Icase("RtnOK", "人员管理列表","bpc1_N34_C4", orgId, doctorId, u"",u"",u"",u"4",u"1",u"1")
resp = Icase("RtnOK", "人员管理列表","bpc1_N34_C5", orgId, doctorId, u"",u"",u"",u"1,4",u"1",u"1")
resp = Icase("RtnOK", "人员管理列表","bpc1_N34_C6", orgId, doctorId, u"",u"",u"",u"1,2,4",u"1",u"1")


resp = Icase("RtnOK", "人员管理查看","bpc1_N35_C1", doctorId)


'''1.10 患者管理'''

resp = Icase("RtnOK", "患者信息列表","bpc1_N38_C1", u"",u"",u"",u"1",u"1")
patientId = resp.split('patientId":')[1].split(",")[0]
print u"patientId = " + patientId

resp = Icase("RtnOK", "患者信息详情","bpc1_N39_C1", patientId)

'''1.11 通知'''

resp = Icase("RtnOK", "B端消息新增","bpc1_N40_C1", doctorId, u"1", u"调班申请",u"0")
resp = Icase("RtnOK", "B端消息新增","bpc1_N40_C2", doctorId, u"2", u"调班申请通过", u"0")
resp = Icase("RtnOK", "B端消息新增","bpc1_N40_C3", doctorId, u"3", u"调班申请被拒", u"1")
resp = Icase("RtnOK", "B端消息新增","bpc1_N40_C4", doctorId, u"11", u"排班通知", u"1")
resp = Icase("RtnOK", "B端消息新增","bpc1_N40_C5", doctorId, u"21", u"处方审批通过", u"1")
resp = Icase("RtnOK", "B端消息新增","bpc1_N40_C6", doctorId, u"22", u"处方审批被拒", u"1")


# resp = Icase("C端消息新增","bpc1_N41_C6", patientId, orgId,u"22", u"处方审批被拒", u"1")
# {"content":"xx，请于20170101 12：00，去xx诊所进行随访","就诊人":"赵梦琪","诊所":"xxx","支付方式":"xxx","科室":"心理咨询科室","医生":"李大力","预约时间":"2017-10-26","金额":"16.13元","类型":"药品购买","退款时间":"2017-04-17 13:29"}


'''1.12 B端APP'''

resp = Icase("RtnOK", "预约列表","bpc1_N42_C1", doctorId, orgId, u"1", u"1", u"1", u"1")
resp = Icase("RtnOK", "预约列表","bpc1_N42_C2", doctorId, orgId, u"6", u"1", u"1", u"1")
resp = Icase("RtnOK", "预约列表","bpc1_N42_C3", doctorId, orgId, u"3", u"1", u"1", u"1")


# resp = Icase("RtnOK", "视频问诊信息记录","bpc1_N43_C1", ?, doctorId, patientId, u"1", u"1", u"1", u"1")
