# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2017-12-6
# Description: 云慧诊 脑卒中 web2.1, 医生机构平台
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from YHZ.PageObject.yhzPO import *
Yhz_PO = YhzPO(Level_PO)

# 业务场景1：
# 机构管理者
# 1、编辑机构管理员信息及重置密码，
# 2、一级科室的新增、编辑、删除，二级子科室的新增
# 3、新增医生并删除
# 4、新增患者并删除患者



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'''机构登录'''
Yhz_PO.loginDoctor(varDoctorUrl, u"Djf906", u"123456", "123")
Level_PO.getError(Level_PO.clickLinktext(u"会诊审核", 2), u"科室管理链接未找到！", sys._getframe().f_lineno)
sleep(3)
Level_PO.selectIdText(u"form_status", u"审核中")
sleep(1212)

# '''机构管理'''
# Level_PO.clickLINKTEXT(u"机构管理", 2)
# # '''机构管理 - 查看详情'''
# curNCZ.execute('select org_id from tt_org where name="%s" ' % (varOrgName))
# data0 = curNCZ.fetchone()
# varOrgId = data0[0]  # 机构ID
# Level_PO.clickXPATH(u"//a[@href='/yhzv2/web/app.php/org/ttorg/" + str(varOrgId) + u"/edit']", 2)
#
# # '''机构管理 - 编辑管理员帐号 '''
# curNCZ.execute('select doctor_id from vw_doctor where org_name="%s" ' % (varOrgName))
# data1 = curNCZ.fetchone()
# varOrgAdminId = data1[0]  # 机构管理员ID
# Level_PO.clickXPATH(u"//a[@href='/yhzv2/web/app.php/org/ttorg/" + str(varOrgAdminId) + u"/doctoredit']", 2)  # 点击编辑
# Level_PO.inputClearId(u"tm_doctor_g_edit_name", varOrgAdmin)
# Level_PO.inputClearId(u"tm_doctor_g_edit_phoneNumber", varOrgAdminPhone)
# Level_PO.clickID(u"password_form_btn_" + str(varOrgAdminId), 2)
# print u"[done], 编辑机构管理者帐号信息"
#
# # '''机构管理 - 重置密码 '''
# Level_PO.clickXPATH(u"//a[@href='/yhzv2/web/app.php/org/ttorg/" + str(varOrgAdminId) + u"/doctorresetpwd']", 2)
# Level_PO.clickID(u"password_form_btn_" + str(varOrgAdminId), 2)
# print u"[done], 重置机构管理者密码"


'''科室管理'''
Level_PO.getError(Level_PO.clickLINKTEXT(u"科室管理", 2), u"科室管理链接未找到！", sys._getframe().f_lineno)

# 新增一级科室(返回科室Id)
varFirstOfficeId = Yhz_PO.createOffice(varOrgName, varFirstOffice)

# 遍历科室列表（返回字典形一级科室列表）
d_firstOfficeList = Yhz_PO.getOfficeList(varOrgName)

# 新增子科室（二级科室，需级联一级科室）
Yhz_PO.newSubOffice(d_firstOfficeList, varOrgName, varFirstOffice, varSecondOffice)

# 编辑一级科室
Yhz_PO.editOffice(d_firstOfficeList, varOrgName, varFirstOffice, varFirstOffice + u"edit")

# # 删除一级科室（ta的下级科室一并删除）
# Yhz_PO.delOffice(d_firstOfficeList, varOrgName, varFirstOffice)



'''医生管理'''
Level_PO.getError(Level_PO.clickLINKTEXT(u"医生管理", 2), u"医生管理链接未找到！", sys._getframe().f_lineno)
Level_PO.getError(Level_PO.clickLINKTEXT(u"新建医生档案", 2), u"新建医生档案链接未找到！", sys._getframe().f_lineno)

# 新建医生
varDoctorId = Yhz_PO.createDoctor(u"verify", varDoctorName, varDoctorIdCard, varDoctorPhone, varDoctorGender, varDoctorAccount, varDoctorOrg, varDoctorTitle, varDoctorPosition, varDoctorOffice, varDoctorJobNumber, varHZ, varJX, varHY, varKszr, varAccountType)

Level_PO.getError(Level_PO.clickLINKTEXT(u"医生管理", 2), u"医生管理链接未找到！", sys._getframe().f_lineno)
# 停用医生
Yhz_PO.doctorStatus(u"disable", varDoctorJobNumber, varDoctorId)
# 启用医生
Yhz_PO.doctorStatus(u"enable", varDoctorJobNumber, varDoctorId)



'''患者管理'''
Level_PO.getError(Level_PO.clickLINKTEXT(u"患者管理", 2), u"患者管理链接未找到！", sys._getframe().f_lineno)
Level_PO.getError(Level_PO.clickLINKTEXT(u"新建患者档案", 2), u"新建患者档案链接未找到！", sys._getframe().f_lineno)

# 新建患者
varPatientId = Yhz_PO.createPatient(u"verify", varPatientName, varPatientIdCard, varPatientPhone, varPatientGender, varPatientAge, varPatientAddress, varPatientDiagnosisNo, varPatientOrg, varOffice, varPatientYibaoNo, varPatientDiseasyHistory)

Level_PO.getError(Level_PO.clickLINKTEXT(u"患者管理", 2), u"患者管理链接未找到！", sys._getframe().f_lineno)
# 删除患者
Yhz_PO.delPatient(varPatientIdCard)

