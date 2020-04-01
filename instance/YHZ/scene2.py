# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2017-12-17
# Description: 云慧诊 脑卒中 web2.1, 医生机构平台
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from YHZ.PageObject.yhzPO import *
Yhz_PO = YhzPO(Level_PO)

# 业务场景2：

# 机构管理者
# 1、编辑机构管理员信息及重置密码，
# 2、一级科室的新增、编辑、删除，二级子科室的新增
# 3、新增医生并删除
# 4、新增患者并删除患者




# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# '''机构登录'''
# Yhz_PO.login(varOrgUrl, varOrgAccount, varOrgPass, varOrgName)
#
# # '''科室管理'''
# # Level_PO.getError(Level_PO.clickLinktext(u"科室管理", 2), u"科室管理链接未找到！", sys._getframe().f_lineno)
# # # 新增一级科室(返回科室Id)
# # varFirstOfficeId = Yhz_PO.createOffice(varOrgName, varFirstOffice)
#
# '''医生管理'''
# Level_PO.getError(Level_PO.clickLinktext(u"医生管理", 2), u"医生管理链接未找到！", sys._getframe().f_lineno)
# Level_PO.getError(Level_PO.clickLinktext(u"新建医生档案", 2), u"新建医生档案链接未找到！", sys._getframe().f_lineno)
# # 新建医生
# varDoctorId, varDoctorAccount = Yhz_PO.createDoctor(u"verify", varDoctorName, varDoctorIdCard, varDoctorPhone, varDoctorAccount, varDoctorOrg, varDoctorTitle, varDoctorPosition, varDoctorOffice, varDoctorJobNumber, varHZ, varJX, varHY, varKszr, varAccountType)
# print varDoctorId
# print varDoctorAccount
# '''患者管理'''
# Level_PO.getError(Level_PO.clickLinktext(u"患者管理", 2), u"患者管理链接未找到！", sys._getframe().f_lineno)
# Level_PO.getError(Level_PO.clickLinktext(u"新建患者档案", 2), u"新建患者档案链接未找到！", sys._getframe().f_lineno)
# # 新建患者
# varPatientId = Yhz_PO.createPatient(u"verify", varPatientName, varPatientIdCard, varPatientPhone, varPatientGender, varPatientAge, varPatientAddress, varPatientDiagnosisNo, varPatientOrg, varOffice, varPatientYibaoNo, varPatientDiseasyHistory)



'''医生登录'''
Yhz_PO.loginDoctor(varDoctorUrl, u"Dzmg350", varOrgPass, varDoctorOrg)
# Yhz_PO.login(varDoctorUrl, varDoctorAccount, varOrgPass, varDoctorOrg)

# '''会诊预约'''
varSubject = u"血小板复查诊断" + Third_PO.randomDigit(5)

# Level_PO.getError(Level_PO.clickLinktext(u"会诊预约", 2), u"会诊预约链接未找到！", sys._getframe().f_lineno)
# Level_PO.inputId(u"title", u"血小板复查诊断")  # 会诊主题
# Level_PO.clickXpath(u"//button[@data-target='#member-list']", 2)  # 添加  会诊邀请
# Level_PO.inIframeXPATH(u"//iframe[@name='member_iframe']", 2)  # 选择医生
# Level_PO.selectIdText(u"org", varOrgName)  # 医疗机构
# Level_PO.selectIdText(u"office", u"全部")   # 所属科室
# Level_PO.selectNameText(u"title", u"全部")  # 职称
# Level_PO.selectNameText(u"position", u"全部")  # 职位
# Level_PO.clickXpath(u"//button[@class='btn btn-primary' and @type='submit']", 2)  # 搜索
# Level_PO.clickXpath(u"//input[@name='id[]']", 2)  # 默认选择第一条记录
# varInviteDoctorId = Level_PO.getXpathAttr(u"//input[@name='id[]']",u"value")
# Level_PO.outIframe(2)
# Level_PO.clickID(u"select-member", 2)
# Level_PO.clickXpath(u"//input[@name='isAdmin[" + str(varInviteDoctorId) + u"]']", 2)   # 是否会诊室管理者
# Level_PO.clickID(u"patient_name", 2)  # 患者姓名
# Level_PO.inIframeXPATH(u"//iframe[@name='patient_iframe']", 2)  # 选择患者
# Level_PO.clickXpath(u"//input[@name='id']", 2)  # 默认选择第一个
# Level_PO.outIframe(2)
# Level_PO.clickID(u"select-patient", 2)
# Level_PO.selectNameText(u"isPatientParticipate", u"否")  # 患者参与
# Level_PO.clickID(u"shadow-select", 2)  # 影像
# Level_PO.inIframe(u"shadow-iframe", 2)  # 选择患者
# Level_PO.clickXpath(u"//input[@value='0' and @name='pacsId']", 1)
# Level_PO.clickXpath(u"//input[@value='2' and @name='pacsId']", 1)
# Level_PO.outIframe(2)
# Level_PO.clickID(u"select-shadow", 2)
# # Level_PO.inputId(u"attach", u"//Users//linghuchong//Desktop//testpic//1.txt")  # 附件 ??写法有问题
# Level_PO.inputId(u"currentDiagnosis", u"患者之前没有会诊记录，当前诊断未知")  # 当前诊断
# Level_PO.inputId(u"illnessDesc", u"患者由于长时间未治疗，病情已开始恶化，需要化疗")  # 病情描述
# Level_PO.inputId(u"destination", u"通过化疗观察病情")  # 会诊目的
# Level_PO.inputName(u"remark", u"备注信息123")  # 备注
# Level_PO.selectNameText(u"mode", u"2方会诊室")  # 会诊室规模
# Level_PO.clickXpath(u"//input[@onclick='submitForm();']", 2)  # 确定

''' 获取会诊单据号 '''
connNCZ.commit()
tblSubject = curNCZ.execute('select meeting_id from tt_consultation where title="%s" order by meeting_id DESC ' % (varSubject))
if tblSubject > 0:
    tmp = curNCZ.fetchone()
    tblMeetingId = tmp[0]


'''logout'''
Level_PO.clickXpath(u"//a[@data-toggle='dropdown']", 2)
Level_PO.getError(Level_PO.clickLinktext(u"退出登录", 2), u"退出登录链接未找到！", sys._getframe().f_lineno)

'''审核人登录'''
Yhz_PO.loginDoctor(varDoctorUrl, varOrgAuditorAccount, varOrgPass, varDoctorOrg)

'''会诊审核'''
Level_PO.getError(Level_PO.clickLinktext(u"会诊审核", 2), u"会诊审核链接未找到！", sys._getframe().f_lineno)
Level_PO.selectIdText(u"form_status", u"待审核")  # 查询待审核的会诊
Level_PO.clickXpath(u"//button[@class='btn btn-primary']", 2)
Level_PO.clickXpath(u"//a[@href='/yhzv2-doctor/web/app.php/huizhen/shenhe/detail/" + str(tblMeetingId) + u"']", 2)  # 查看详情
Level_PO.clickXpath(u"//button[@onclick='accept()']", 2)  # 接受该会诊

'''logout'''
Level_PO.clickXpath(u"//a[@data-toggle='dropdown']", 2)
Level_PO.getError(Level_PO.clickLinktext(u"退出登录", 2), u"退出登录链接未找到！", sys._getframe().f_lineno)

