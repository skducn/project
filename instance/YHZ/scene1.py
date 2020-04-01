# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2017-12-13
# Description: 云慧诊 脑卒中 web2.1, 医生机构平台

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from YHZ.PageObject.yhzPO import *
Yhz_PO = YhzPO(Level_PO)

Yhz_PO.login("http://192.168.0.81:8324/login", "1", "1", "11")
#
# print Level_PO.getTblRecordWhere1(curNCZ, "tm_doctor", "org_id=92")
# print Level_PO.getTblRecordWhere2(curNCZ, "tm_doctor", "org_id=92", "office_id=262")
# print Level_PO.getTblValueWhere1(connNCZ, curNCZ, "tm_doctor", "doctor_id", "job_number=lll23520")
# print Level_PO.getTblValueWhere2(connNCZ, curNCZ, "tm_doctor", "doctor_id", "org_id=92" , "job_number=lll520")
#
# sleep(1212)
#
#
# # 前置条件：
# # 1、机构必须要有1名审核者，否则无法发起会诊预约。
# # 2、机构管理中，有审核者（如果审核者不存在，则指派一名医生（可以是系统中已有的肿瘤科医生或自动创建一名肿瘤科医生））
#
# # 审核业务场景1 :
# # 上海第五人民医院的肿瘤科医生（某某）发起会诊预约。
# # 审核者: is_ywk=1， account_type=1
# # 科室主任: is_kszr=1
# # 机构管理员: account_type=1
#
# '''机构信息'''
# varOrgAccount = u"gdwrm"  # 机构管理员
# varOrgPass = u"123456"   # 管理员密码
# varOrg = u"上海第五人民医院" # 机构
# varOffice = u"肿瘤科"
#
# # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
# print '''1，机构登录'''
# Yhz_PO.login(varOrgUrl, varOrgAccount, varOrgPass, varOrg)
#
#
# print '''2，设置机构审核者'''
# varAuditorLoginName = Yhz_PO.getAuditor(varOrg, varOffice)
#
#
# print '''3，新建医生'''
# # '''医生信息'''
# varDoctorName = Third_PO.randomUserName()  # *姓名
# varDoctorIdCard = Third_PO.randomIdCard()  # *身份证号
# varDoctorPhone = Third_PO.randomPhone()  # *手机号码
# varDoctorGender = Third_PO.getGender(varDoctorIdCard)  # 性别
# varDoctorAccount = Third_PO.getUserNameinitial(varDoctorName) + Third_PO.randomDigit(3)  # *登录帐号 （规则：D + 用户名首字母 + 3个数字）
# varDoctorOrg = u"上海第五人民医院"   # *机构名称
# varDoctorTitle = u"正高"  # *职称
# varDoctorPosition = u"主治医师"  # *职位
# varDoctorOffice = u"肿瘤科"  # *所属科室
# varDoctorJobNumber = varDoctorAccount  # 工号（规则：是登录帐号）
# varHZ = u"开启"  # *会诊（开启，关闭）
# varJX = u"开启"  # *教学（开启，关闭）
# varHY = u"开启"  # *会议（开启，关闭）
# varKszr = u"关闭"  # *科室主任 （开启，关闭）
# varAccountType = u"关闭"  # *机构管理员 （开启，关闭）
#
# Level_PO.getError(Level_PO.clickLinktext(u"医生管理", 2), u"医生管理链接未找到！", sys._getframe().f_lineno)
# Level_PO.getError(Level_PO.clickLinktext(u"新建医生档案", 2), u"新建医生档案链接未找到！", sys._getframe().f_lineno)
# varDoctorId = Yhz_PO.createDoctor(u"verify", varDoctorName, varDoctorIdCard, varDoctorPhone, varDoctorGender, varDoctorAccount, varDoctorOrg, varDoctorTitle, varDoctorPosition, varDoctorOffice, varDoctorJobNumber, varHZ, varJX, varHY, varKszr, varAccountType)
#
#
# print '''4，新建患者'''
# # '''患者信息, 6个必填项'''
# varPatientName = Third_PO.randomUserName()  # *患者姓名
# varPatientIdCard = Third_PO.randomIdCard()  # *患者身份证
# varPatientPhone = Third_PO.randomPhone()  # *患者电话
# varPatientGender = Third_PO.getGender(varPatientIdCard)  # 性别
# varPatientAge = Third_PO.getAge(varPatientIdCard)  # 年龄
# varPatientAddress = u"上海市浦东新区南泉北路1200弄23号1203室"  # 家庭地址
# varPatientDiagnosisNo = Third_PO.randomDigit(7)   # *就诊号
# varPatientOrg = u"上海第五人民医院"   # *医疗机构
# varOffice = u"肿瘤科"   #  *所属科室
# varPatientYibaoNo = Third_PO.getUserNameinitial(varPatientName) + Third_PO.randomDigit(7)   # 医保号码
# # varDoctorId ，如果varDoctorId不存在, 则依据 医疗机构和所属科室自动匹配，默认匹配到的最后一个医生。
# varPatientDiseasyHistory = u"10年前得过血小板减少"  #  简要病史
#
# Level_PO.getError(Level_PO.clickLinktext(u"患者管理", 2), u"患者管理链接未找到！", sys._getframe().f_lineno)
# Level_PO.getError(Level_PO.clickLinktext(u"新建患者档案", 2), u"新建患者档案链接未找到！", sys._getframe().f_lineno)
# varPatientId = Yhz_PO.createPatient(u"verify", varPatientName, varPatientIdCard, varPatientPhone, varPatientGender, varPatientAge, varPatientAddress, varPatientDiagnosisNo, varPatientOrg, varOffice, varPatientYibaoNo, varDoctorId, varPatientDiseasyHistory)
#
#
# print '''5, 医生登录'''
# curNCZ.execute('select user_name from tm_doctor where doctor_id="%s"' % (varDoctorId))
# dd = curNCZ.fetchone()
# varDoctorAccount = dd[0]
# varOrgPass = u"123456"
# Yhz_PO.loginDoctor(varDoctorUrl, varDoctorAccount, varOrgPass, varOrg)
#
#
# print '''6, 会诊预约'''
# varSubject = u"血小板复查诊断" + Third_PO.randomDigit(5)
# Level_PO.getError(Level_PO.clickLinktext(u"会诊预约", 2), u"会诊预约链接未找到！", sys._getframe().f_lineno)
# Level_PO.inputId(u"title", varSubject)  # 会诊主题
# Level_PO.clickXPATH(u"//button[@data-target='#member-list']", 2)  # 添加  会诊邀请
# Level_PO.inIframeXPATH(u"//iframe[@name='member_iframe']", 2)  # 选择医生
# Level_PO.selectIdText(u"org", varOrg)  # 医疗机构
# Level_PO.selectIdText(u"office", u"全部")   # 所属科室
# Level_PO.selectNameText(u"title", u"全部")  # 职称
# Level_PO.selectNameText(u"position", u"全部")  # 职位
# Level_PO.clickXPATH(u"//button[@class='btn btn-primary' and @type='submit']", 2)  # 搜索
# Level_PO.clickXPATH(u"//input[@name='id[]']", 2)  # 默认选择第一条记录
# varInviteDoctorId = Level_PO.getXpathAttr(u"//input[@name='id[]']",u"value")
# Level_PO.outIframe(2)
# Level_PO.clickID(u"select-member", 2)
# Level_PO.clickXPATH(u"//input[@name='isAdmin[" + str(varInviteDoctorId) + u"]']", 2)   # 是否会诊室管理者
# Level_PO.clickID(u"patient_name", 2)  # 患者姓名
# Level_PO.inIframeXPATH(u"//iframe[@name='patient_iframe']", 2)  # 选择患者
# Level_PO.clickXPATH(u"//input[@name='id']", 2)  # 默认选择第一个
# Level_PO.outIframe(2)
# Level_PO.clickID(u"select-patient", 2)
# Level_PO.selectNameText(u"isPatientParticipate", u"否")  # 患者参与
# Level_PO.clickID(u"shadow-select", 2)  # 影像
# Level_PO.inIframe(u"shadow-iframe", 2)  # 选择患者
# Level_PO.clickXPATH(u"//input[@value='0' and @name='pacsId']", 1)
# Level_PO.clickXPATH(u"//input[@value='2' and @name='pacsId']", 1)
# Level_PO.outIframe(2)
# Level_PO.clickID(u"select-shadow", 2)
# # Level_PO.inputId(u"attach", u"//Users//linghuchong//Desktop//testpic//1.txt")  # 附件 ??写法有问题
# Level_PO.inputId(u"currentDiagnosis", u"患者之前没有会诊记录，当前诊断未知")  # 当前诊断
# Level_PO.inputId(u"illnessDesc", u"患者由于长时间未治疗，病情已开始恶化，需要化疗")  # 病情描述
# Level_PO.inputId(u"destination", u"通过化疗观察病情")  # 会诊目的
# Level_PO.inputName(u"remark", u"备注信息123")  # 备注
# Level_PO.selectNameText(u"mode", u"2方会诊室")  # 会诊室规模
# Level_PO.clickXPATH(u"//input[@onclick='submitForm();']", 2)  # 确定
#
#
# print ''' 获取会诊单据号 '''
# connNCZ.commit()
# tblSubject = curNCZ.execute('select meeting_id from tt_consultation where title="%s" order by meeting_id DESC ' % (varSubject))
# if tblSubject > 0:
#     tmp = curNCZ.fetchone()
#     tblMeetingId = tmp[0]
# else:
#     Level_PO.getError(u"error", u"scene1.py, tt_consultation表, 会诊单据号(" + varSubject + u")不存在！", sys._getframe().f_lineno)
#
#
# '''logout'''
# Level_PO.clickXPATH(u"//a[@data-toggle='dropdown']", 2)
# Level_PO.getError(Level_PO.clickLinktext(u"退出登录", 2), u"退出登录链接未找到！", sys._getframe().f_lineno)
#
# '''审核人登录'''
# Yhz_PO.loginDoctor(varDoctorUrl, varAuditorLoginName, varOrgPass, varOrg)
#
# '''会诊审核'''
# Level_PO.getError(Level_PO.clickLinktext(u"会诊审核", 2), u"会诊审核链接未找到！", sys._getframe().f_lineno)
# Level_PO.selectIdText(u"form_status", u"待审核")  # 查询待审核的会诊
# Level_PO.clickXPATH(u"//button[@class='btn btn-primary']", 2)
# Level_PO.clickXPATH(u"//a[@href='/yhzv2-doctor/web/app.php/huizhen/shenhe/detail/" + str(tblMeetingId) + u"']", 2)  # 查看详情
# Level_PO.clickXPATH(u"//button[@onclick='accept()']", 2)  # 接受该会诊
#
# # 打印进度跟踪
# Level_PO.printIDXpathsText(u'timeline', u"dl")
#
# '''logout'''
# Level_PO.clickXPATH(u"//a[@data-toggle='dropdown']", 2)
# Level_PO.getError(Level_PO.clickLinktext(u"退出登录", 2), u"退出登录链接未找到！", sys._getframe().f_lineno)
#
# 结束