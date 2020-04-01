# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2017-12-13
# Description: 云慧诊 脑卒中 web2.1, 医生机构平台
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 业务场景，管理员创建医生和患者：

from YHZ.PageObject.yhzPO import *
Yhz_PO = YhzPO(Level_PO)


'''机构信息'''
varOrg = u"上海第五人民医院"


'''新建医生'''
'''医生信息'''
varDoctorName = Third_PO.randomUserName()  # *姓名
varDoctorIdCard = Third_PO.randomIdCard()  # *身份证号
varDoctorPhone = Third_PO.randomPhone()  # *手机号码
varDoctorGender = Third_PO.getGender(varDoctorIdCard)  # 性别
varDoctorAccount = Third_PO.getUserNameinitial(varDoctorName) + Third_PO.randomDigit(3)  # *登录帐号 （规则：D + 用户名首字母 + 3个数字）
varDoctorOrg = u"上海第五人民医院"   # *机构名称
varDoctorTitle = u"正高"  # *职称
varDoctorPosition = u"主治医师"  # *职位
varDoctorOffice = u"肿瘤科"  # *所属科室
varDoctorJobNumber = varDoctorAccount  # 工号（规则：是登录帐号）
varHZ = u"开启"  # *会诊（开启，关闭）
varJX = u"开启"  # *教学（开启，关闭）
varHY = u"开启"  # *会议（开启，关闭）
varKszr = u"关闭"  # *科室主任 （开启，关闭）
varAccountType = u"关闭"  # *机构管理员 （开启，关闭）

Level_PO.getError(Level_PO.clickLINKTEXT(u"医生管理", 2), u"医生管理链接未找到！", sys._getframe().f_lineno)
Level_PO.getError(Level_PO.clickLINKTEXT(u"新建医生档案", 2), u"新建医生档案链接未找到！", sys._getframe().f_lineno)
varDoctorId = Yhz_PO.createDoctor(u"verify", varDoctorName, varDoctorIdCard, varDoctorPhone, varDoctorGender, varDoctorAccount, varDoctorOrg, varDoctorTitle, varDoctorPosition, varDoctorOffice, varDoctorJobNumber, varHZ, varJX, varHY, varKszr, varAccountType)


'''新建患者'''
'''患者信息, 6个必填项'''
varPatientName = Third_PO.randomUserName()  # *患者姓名
varPatientIdCard = Third_PO.randomIdCard()  # *患者身份证
varPatientPhone = Third_PO.randomPhone()  # *患者电话
varPatientGender = Third_PO.getGender(varPatientIdCard)  # 性别
varPatientAge = Third_PO.getAge(varPatientIdCard)  # 年龄
varPatientAddress = u"上海市浦东新区南泉北路1200弄23号1203室"  # 家庭地址
varPatientDiagnosisNo = Third_PO.randomDigit(7)   # *就诊号
varPatientOrg = u"上海第五人民医院"   # *医疗机构
varOffice = u"肿瘤科"   #  *所属科室
varPatientYibaoNo = Third_PO.getUserNameinitial(varPatientName) + Third_PO.randomDigit(7)   # 医保号码
# varDoctorId ，如果varDoctorId不存在, 则依据 医疗机构和所属科室自动匹配，默认匹配到的最后一个医生。
varPatientDiseasyHistory = u"10年前得过血小板减少"  #  简要病史

Level_PO.getError(Level_PO.clickLINKTEXT(u"患者管理", 2), u"患者管理链接未找到！", sys._getframe().f_lineno)
Level_PO.getError(Level_PO.clickLINKTEXT(u"新建患者档案", 2), u"新建患者档案链接未找到！", sys._getframe().f_lineno)
varPatientId = Yhz_PO.createPatient(u"verify", varPatientName, varPatientIdCard, varPatientPhone, varPatientGender, varPatientAge, varPatientAddress, varPatientDiagnosisNo, varPatientOrg, varOffice, varPatientYibaoNo, varDoctorId, varPatientDiseasyHistory)



