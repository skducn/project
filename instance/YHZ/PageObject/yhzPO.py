# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2017-12-6
# Description: YHZ
#***************************************************************


from YHZ.Config.config import *

class YhzPO(object):

    def __init__(self, Level_PO):
        self.Level_PO = Level_PO

    def logout(self):

        ''' 关闭浏览器 '''

        Level_PO.close_driver()

    def login(self, dimUrl, dimUsername, dimPassword, dimOrg):

        ''' 机构登录 '''

        Level_PO.openURL("http://192.168.0.81:8324/login", 1)
        Level_PO.inputXpath("//input[@placeholder='请输入用户名']", "007")

        # Level_PO.inputIdClear(u"_username", dimUsername)
        # Level_PO.inputIdClear(u"_password", dimPassword)
        # x = Level_PO.getCode(u"yhzncz.jpg", 2035, 876, 2175, 933)
        # y = x.replace(" ", "").replace("'", "").replace(".", "").replace("?", "").replace("‘", "").replace("”", "").replace("’","").replace("ﬁr","").replace("ﬁ","")\
        #     .replace("[","").replace("ﬂ","").replace("“","")
        # print y
        # Level_PO.inputId(u"_captcha", y)  # 获取并输入验证码
        # Level_PO.clickXpath(u"//button[@class='btn btn-primary btn-block']", 2)
        # if Level_PO.isElementText(dimOrg):
        #     pass
        # else:
        #     # 错误提示后，遍历10次验证码
        #     for i in range(10):
        #         if Level_PO.isElementId(u"_captcha"):
        #             Level_PO.inputIdClear(u"_username", dimUsername)
        #             Level_PO.inputIdClear(u"_password", dimPassword)
        #             x = Level_PO.getCode(u"yhzncz.jpg", 2035, 815, 2175, 872)
        #             y = x.replace(" ", "").replace("'", "").replace(".", "").replace("?", "").replace("‘", "").replace(
        #                 "”", "").replace("’", "").replace("ﬁr","").replace("ﬁ","").replace("[","").replace("ﬂ","").replace("“","")
        #             print y
        #             Level_PO.inputId(u"_captcha", y)  # 获取并输入验证码
        #             Level_PO.clickXpath(u"//button[@class='btn btn-primary btn-block']", 2)
        #         else:
        #             break
        # Level_PO.setMaximize()
        # print u"[done], 机构登录, " + dimUsername + u"(" + dimOrg + u")"

    #
    # def loginDoctor(self, dimUrl, dimUsername, dimPassword, dimOrg):
    #
    #     ''' 医生登录 '''
    #
    #     Level_PO.openURL(1200, 900, dimUrl, 1)
    #     Level_PO.inputIdClear(u"account", dimUsername)
    #     Level_PO.inputName(u"password", dimPassword)
    #     x = Level_PO.getCode(u"yhzncz.jpg", 2035, 872, 2175, 933)
    #     y = x.replace(" ", "").replace("'", "").replace(".", "").replace("?", "").replace("‘", "").replace("”", "").replace("’","").replace("ﬁr","").replace("ﬁ","")\
    #         .replace("[","").replace("ﬂ","").replace("“","")
    #     print y
    #     Level_PO.inputId(u"yzm", y)  # 获取并输入验证码
    #     Level_PO.clickXpath(u"//button[@class='btn btn-primary btn-block']", 2)
    #
    #     # if Level_PO.isElementText(dimOrg):
    #     #     pass
    #     # else:
    #     #     # 错误提示后，遍历10次验证码
    #     #     for i in range(10):
    #     #         if Level_PO.isElementId(u"yzm"):
    #     #             Level_PO.inputIdClear(u"account", dimUsername)
    #     #             Level_PO.inputName(u"password", dimPassword)
    #     #             x = Level_PO.getCode(u"yhzncz.jpg", 2035, 815, 2175, 872)
    #     #             y = x.replace(" ", "").replace("'", "").replace(".", "").replace("?", "").replace("‘", "").replace(
    #     #                 "”", "").replace("’", "").replace("ﬁr","").replace("ﬁ","").replace("[","").replace("ﬂ","")
    #     #             print y
    #     #             Level_PO.inputId(u"yzm", y)  # 获取并输入验证码
    #     #             Level_PO.clickXpath(u"//button[@class='btn btn-primary btn-block']", 2)
    #     #         else:
    #     #             break
    #     Level_PO.setMaximize()
    #     print u"[done], 医生登录, " + dimUsername + u"(" + dimOrg + u")"
    #
    #
    # def createDoctor(self, isVerify, dimDoctorName, dimDoctorIdCard, dimDoctorPhone, dimDoctorGender, dimDoctorAccount, dimOrgName, dimDoctorTitle, dimDoctorPosition, dimDoctorOffice, dimDoctorJobNumber, dimHZ, dimJX, dimHY, dimKszr, dimAccountType):
    #
    #     ''' 新建医生 '''
    #
    #     ''' 检查表中医生是否存在，存在则不能重复添加，关键字是手机号 '''
    #     tblDoctorPhone = curNCZ.execute('select doctor_id from tm_doctor where phone_number="%s" ' % (dimDoctorPhone))
    #     if tblDoctorPhone == 0:
    #         Level_PO.inputId(u"doctorbundle_tmdoctor_name", u"" + dimDoctorName)  # 姓名
    #         Level_PO.inputId(u"doctorbundle_tmdoctor_idCard", dimDoctorIdCard)  # 身份证号
    #         Level_PO.inputId(u"doctorbundle_tmdoctor_phoneNumber", dimDoctorPhone)  # 手机号码
    #         Level_PO.selectIdText(u"doctorbundle_tmdoctor_gender", dimDoctorGender)  # 性别
    #         Level_PO.inputId(u"doctorbundle_tmdoctor_userName", dimDoctorAccount)  # 登录帐号
    #         Level_PO.selectIdText(u"doctorbundle_tmdoctor_org", dimOrgName)  # 医疗机构
    #         Level_PO.selectIdText(u"doctorbundle_tmdoctor_title", dimDoctorTitle)  # 职称
    #         Level_PO.selectIdText(u"doctorbundle_tmdoctor_position", dimDoctorPosition)  # 职位
    #         Level_PO.selectIdText(u"doctorbundle_tmdoctor_office", dimDoctorOffice)  # 所属科室
    #         Level_PO.inputId(u"doctorbundle_tmdoctor_jobNumber", dimDoctorJobNumber)  # 工号
    #         Level_PO.selectIdText(u"doctorbundle_tmdoctor_privListHZ", dimHZ)  # 会诊
    #         Level_PO.selectIdText(u"doctorbundle_tmdoctor_privListJX", dimJX)  # 教学
    #         Level_PO.selectIdText(u"doctorbundle_tmdoctor_privListHY", dimHY)  # 会议
    #         Level_PO.selectIdText(u"doctorbundle_tmdoctor_isKszr", dimKszr)  # 科室主任
    #         Level_PO.selectIdText(u"doctorbundle_tmdoctor_accountType", dimAccountType)  # 机构管理员
    #         Level_PO.clickID(u"form-submit", 2)
    #
    #         ''' 检查表中医生id是否创建成功 '''
    #         connNCZ.commit()
    #         tblDoctorPhone = curNCZ.execute('select doctor_id from tm_doctor where phone_number="%s"' % (dimDoctorPhone))
    #         if tblDoctorPhone == 1:
    #             tmp = curNCZ.fetchone()
    #             tblDoctorId = tmp[0]
    #             # tblDoctorUserName = tmp[1]
    #             print u"[done], 新建医生, 医生: " + str(dimDoctorName) + u", " + str(dimDoctorPhone) + u", " + str(dimDoctorAccount) + u", " + dimOrgName + u", " + dimDoctorOffice + u", 会诊(" + dimHZ + u"), 教学(" + dimJX + u"), 会议(" + dimHY + u"), 科室主任(" + dimKszr + u"), 机构管理员(" + dimAccountType + u")"
    #         elif tblDoctorPhone == 0:
    #             Level_PO.getError(u"error", u"yhzPO.py, tm_doctor表, 医生（" + str(dimDoctorName) + u", " + str(dimDoctorPhone) + u"）记录不存在！", sys._getframe().f_lineno)
    #         elif tblDoctorPhone > 1:
    #             Level_PO.getError(u"error", u"yhzPO.py, tm_doctor表, 医生（" + str(dimDoctorName) + u", " + str(dimDoctorPhone) + u"）记录有多条！", sys._getframe().f_lineno)
    #
    #         if isVerify == u"verify":
    #             pass
    #
    #         return tblDoctorId
    #     else:
    #         Level_PO.getError(u"error", u"yhzPO.py, tm_doctor表, 医生（" + str(dimDoctorName) + u", " + str(dimDoctorPhone) + u"）记录已存在, 新增失败！", sys._getframe().f_lineno)
    #
    # def doctorStatus(self, isStatus, dimDoctorJobNumber, dimDoctorId):
    #
    #         ''' 停用/启用医生 '''
    #
    #         # 先查询 工号
    #         Level_PO.inputName(u"jobNumber", dimDoctorJobNumber)
    #         Level_PO.clickXpath(u"//button[@class='btn btn-info']", 2)
    #
    #         if isStatus == u"disable":
    #
    #             ''' 停用医生 '''
    #             try:
    #                 Level_PO.clickXpath(u"//a[@href='/yhzv2/web/app.php/doctor/doctor_tmdoctor/" + str(dimDoctorId) + u"/disable']", 2)
    #                 Level_PO.clickXpath(u"//button[@class='btn btn-danger btn-sm pull-right']", 2)
    #
    #                 ''' 检查表医生id是否被停用 ，1=启用、0=停用'''
    #                 connNCZ.commit()
    #                 curNCZ.execute('select status,user_name,name,phone_number from tm_doctor where doctor_id="%s"' % (dimDoctorId))
    #                 tmp = curNCZ.fetchone()
    #                 if tmp[0] != 0:
    #                     Level_PO.getError(u"error", u"yhzPO.py, tm_doctor表, 医生(ID = " + str(dimDoctorId) + u")记录状态为 '启用'!", sys._getframe().f_lineno)
    #                 else:
    #                     print u"[done], 停用医生, 医生（帐号：" + str(tmp[1]) + u", " + str(tmp[2]) + u", " + str(tmp[3]) + u"）"
    #             except:
    #                 Level_PO.getError(u"error", u"yhzPO.py, 当前(ID = " + str(dimDoctorId) + u")已经是停用状态, 暂停操作!", sys._getframe().f_lineno)
    #
    #
    #
    #         elif isStatus == u"enable":
    #
    #             ''' 启用医生 '''
    #             try:
    #                 # 先查找
    #                 Level_PO.clickXpath(
    #                     u"//a[@href='/yhzv2/web/app.php/doctor/doctor_tmdoctor/" + str(dimDoctorId) + u"/enable']", 2)
    #                 Level_PO.clickXpath(u"//button[@class='btn btn-sm pull-right']", 2)
    #
    #                 ''' 检查表医生id是否被停用 ，1=启用、0=停用'''
    #                 connNCZ.commit()
    #                 curNCZ.execute('select status,user_name,name,phone_number from tm_doctor where doctor_id="%s"' % (dimDoctorId))
    #                 tmp = curNCZ.fetchone()
    #                 if tmp[0] != 1:
    #                     Level_PO.getError(u"error", u"yhzPO.py, tm_doctor表, 医生(ID = " + str(dimDoctorId) + u")记录状态为 '停用'!",sys._getframe().f_lineno)
    #                 else:
    #                     print u"[done], 启用医生, 医生（帐号：" + str(tmp[1]) + u", " + str(tmp[2]) + u", " + str(tmp[3]) + u"）"
    #             except:
    #                 Level_PO.getError(u"error", u"yhzPO.py, 当前(ID = " + str(dimDoctorId) + u")已经是启用状态, 暂停操作!", sys._getframe().f_lineno)
    #
    # def createPatient(self, isVerify, dimPatientName, dimPatientIdCard, dimPatientPhone, dimPatientGender, dimPatientAge, dimPatientAddress, dimPatientDiagnosisNo, dimOrgName, dimOffice, dimPatientYibaoNo, dimDoctorId, dimPatientDiseasyHistory):
    #
    #     ''' 新建患者 '''
    #
    #     ''' 检查患者是否存在，关键字是手机号 '''
    #     tblPatientPhone = curNCZ.execute('select user_id from tt_patient where phone_number="%s" ' % (dimPatientPhone))
    #     if tblPatientPhone == 0:
    #         Level_PO.inputId(u"patientbundle_ttpatient_name", u"" + dimPatientName)  # 姓名
    #         Level_PO.inputId(u"patientbundle_ttpatient_idCard", dimPatientIdCard)   # 身份证
    #         Level_PO.inputId(u"patientbundle_ttpatient_phoneNumber", dimPatientPhone)   # 手机号码
    #         Level_PO.selectIdText(u"patientbundle_ttpatient_gender", dimPatientGender)  # 性别
    #         Level_PO.inputId(u"patientbundle_ttpatient_age", dimPatientAge)   # 年龄
    #         Level_PO.inputId(u"patientbundle_ttpatient_address", dimPatientAddress)    # 家庭地址
    #         Level_PO.inputId(u"patientbundle_ttpatient_diagnosisNo", dimPatientDiagnosisNo)  # 就诊号
    #         Level_PO.selectIdText(u"patientbundle_ttpatient_org", dimOrgName)  # 医疗机构
    #         ''' 获取机构的id '''
    #         connNCZ.commit()
    #         curNCZ.execute('select org_id from tt_org where name="%s" ' % (dimOrgName))
    #         tmp = curNCZ.fetchone()
    #         tblOrgId = tmp[0]
    #
    #         sleep(1)
    #
    #         Level_PO.selectIdStyle(u"patientbundle_ttpatient_office", dimOffice)  # 所属科室( 与医疗机构集联)
    #         ''' 获取所属科室的id '''
    #         connNCZ.commit()
    #         curNCZ.execute('select office_id from tm_office where org_id="%s" and office_name="%s" ' % (tblOrgId, dimOffice))
    #         tmp = curNCZ.fetchone()
    #         tblOfficeId = tmp[0]
    #
    #         Level_PO.inputId(u"patientbundle_ttpatient_yibaoNo", dimPatientYibaoNo)  # 医保号
    #         Level_PO.clickXpath(u"//input[@name='doctorName']", 2)  # 主治医生
    #
    #         if dimDoctorId == u"":
    #             ''' 获取最近添加的主治医生id '''
    #             connNCZ.commit()
    #             curNCZ.execute('select doctor_id from tm_doctor where org_id="%s" and office_id="%s" order by doctor_id DESC ' % (tblOrgId, tblOfficeId))
    #             tmp = curNCZ.fetchone()
    #             dimDoctorId = tmp[0]
    #
    #         Level_PO.inIframeXPATH(u"//iframe[@src='https://cetc.iotcetc.com:8084/yhzv2/web/app.php/patient/patient_ttpatient/doctorlist?orgId=" + str(tblOrgId) + u"&officeId=" + str(tblOfficeId) + u"']", 2)
    #         Level_PO.clickXpath(u"//input[@value='" + str(dimDoctorId) + u"']", 2)
    #         Level_PO.outIframe(2)
    #         Level_PO.clickXpath(u"//button[@onclick='doAddDoctorForPatient(this)']", 2)
    #         Level_PO.inputId(u"patientbundle_ttpatient_diseasyHistory", dimPatientDiseasyHistory)   # 病史
    #         Level_PO.clickXpath(u"//button[@class='btn btn-primary']", 2)
    #
    #         ''' 获取主治医生Name '''
    #         connNCZ.commit()
    #         curNCZ.execute('select name from tm_doctor where doctor_id="%s" order by doctor_id DESC ' % (dimDoctorId))
    #         tmp = curNCZ.fetchone()
    #         dimDoctorName = tmp[0]
    #
    #         ''' 检查表中患者id是否创建成功 '''
    #         connNCZ.commit()
    #         tblPatientPhone = curNCZ.execute('select user_id from tt_patient where phone_number="%s"' % (dimPatientPhone))
    #         if tblPatientPhone == 1:
    #             tmp = curNCZ.fetchone()
    #             tblPatientId = tmp[0]
    #             print u"[done], 新建患者, 患者: " + str(dimPatientName) + u", " + str(dimPatientPhone) + u", " + dimOrgName + u", " + dimOffice + u", 主治医生: " + dimDoctorName + u""
    #         elif tblPatientPhone == 0:
    #             Level_PO.getError(u"error", u"yhzPO.py, tt_patient表, 患者（" + str(dimPatientName) + u", " + str(dimPatientPhone) + u"）记录不存在！", sys._getframe().f_lineno)
    #         elif tblPatientPhone > 1:
    #             Level_PO.getError(u"error", u"yhzPO.py, tt_patient表, 患者（" + str(dimPatientName) + u", " + str(dimPatientPhone) + u"）记录有多条！", sys._getframe().f_lineno)
    #
    #         if isVerify == u"verify":
    #             pass
    #
    #         return tblPatientId
    #     else:
    #         Level_PO.getError(u"error", u"yhzPO.py, tt_patient表, 患者（" + str(dimPatientName) + u", " + str(dimPatientPhone) + u"）记录已存在, 创建失败！", sys._getframe().f_lineno)
    #
    # def delPatient(self, dimPatientIdCard):
    #
    #     ''' 删除患者 '''
    #
    #     # 先查询 身份证
    #     Level_PO.inputName(u"idCard", dimPatientIdCard)
    #     Level_PO.clickXpath(u"//button[@class='btn btn-info']", 2)
    #     ''' 获取患者的Id '''
    #     connNCZ.commit()
    #     curNCZ.execute('select user_id,name,phone_number from tt_patient where id_card="%s" ' % (dimPatientIdCard))
    #     tmp = curNCZ.fetchone()
    #     tblPatientId = tmp[0]
    #
    #     # 删除患者
    #     Level_PO.clickXpath(u"//a[@href='/yhzv2/web/app.php/patient/patient_ttpatient/" + str(tblPatientId) + u"/delete']", 2)
    #     Level_PO.clickID(u"delete_form_btn_" + str(tblPatientId), 2)
    #
    #     ''' 检查表中患者id是否存在 '''
    #     connNCZ.commit()
    #     tt = curNCZ.execute('select user_id from tt_patient where id_card="%s" ' % (dimPatientIdCard))
    #     if tt != 0:
    #         Level_PO.getError(u"error", u"yhzPO.py, tt_patient表, 患者（" + str(tblPatientId) + u", " + str(tmp[2]) + u"）未被删除，请检查!",sys._getframe().f_lineno)
    #     else:
    #         print u"[done], 删除患者, 患者（" + str(tmp[1]) + u", " + str(tmp[2]) + u"）"
    #
    # def createOffice(self, dimOrgName, dimFirstOffice):
    #
    #     '''新建一级科室'''
    #
    #     # 先查询机构
    #     Level_PO.getError(Level_PO.selectNameText(u"orgId", dimOrgName), dimOrgName + u"未找到！", sys._getframe().f_lineno)
    #     Level_PO.getError(Level_PO.clickXpath(u"//button[@class='btn btn-info']", 2), u"查询按钮未找到！", sys._getframe().f_lineno)
    #
    #     # 新建一级科室
    #     Level_PO.getError(Level_PO.clickLINKTEXT(u"新建一级科室", 2), u"新建一级科室链接未找到！", sys._getframe().f_lineno)
    #     Level_PO.inputId(u"officebundle_tmoffice_officeName", dimFirstOffice)
    #     Level_PO.getError(Level_PO.clickXpath(u"//button[@class='btn btn-primary']", 2), u"提交按钮未找到！",sys._getframe().f_lineno)
    #
    #     ''' 获取机构id '''
    #     connNCZ.commit()
    #     curNCZ.execute('select org_id from tt_org where  name="%s"' % (dimOrgName))
    #     tmp = curNCZ.fetchone()
    #     tblOrgId = tmp[0]
    #
    #     '''获取一级科室的id'''
    #     connNCZ.commit()
    #     tt = curNCZ.execute('select office_id,level from tm_office where office_name="%s" and org_id="%s"' % (dimFirstOffice, tblOrgId))
    #     tmp = curNCZ.fetchone()
    #     if tt == 1 and tmp[1] == 1:
    #         tblFirstOfficeId = tmp[0]
    #         print u"[done], 新建一级科室, " + dimOrgName + u" - 一级科室（" + dimFirstOffice + u"）"
    #     else:
    #         Level_PO.getError(u"error", u"yhzPO.py, tm_office表, 新建一级科室, " + dimOrgName + u" - 一级科室（" + dimFirstOffice + u"）", sys._getframe().f_lineno)
    #
    #     return tblFirstOfficeId
    #
    # def getOfficeList(self, dimOrgName):
    #
    #     '''遍历一级科室列表'''
    #
    #     # 先选择机构
    #     Level_PO.getError(Level_PO.selectNameText(u"orgId", dimOrgName), dimOrgName + u"未找到！", sys._getframe().f_lineno)
    #     Level_PO.getError(Level_PO.clickXpath(u"//button[@class='btn btn-info']", 2), u"查询按钮未找到！", sys._getframe().f_lineno)
    #
    #     # 获取所有一级科室名
    #     l_dimOfficeName = Level_PO.getXpathsText(u"//div[@class='text-left']")
    #
    #     # 获取所有一级科室名的value值
    #     l_dim1 = Level_PO.getXpathsAttr(u"//div[@class='text-left']", u"innerHTML")
    #
    #     l_dimOfficeValue = []
    #     for i in range(len(Level_PO.getXpathsAttr(u"//div[@class='text-left']", u"innerHTML"))):
    #         l_dimOfficeValue.append(l_dim1[i].split('value="')[1].split('"')[0])
    #
    #     # 生成科室字典，如（科室名：科室值）
    #     d_dimOffice = dict(zip(l_dimOfficeName, l_dimOfficeValue))
    #     return d_dimOffice
    #
    # def editOffice(self, d_dimFirstOfficeList, dimOrgName, dimFirstOffice, dimFirstOfficeRevise):
    #
    #     ''' 编辑一级科室 '''
    #
    #     # 先选择机构
    #     Level_PO.getError(Level_PO.selectNameText(u"orgId", dimOrgName), dimOrgName + u"未找到！", sys._getframe().f_lineno)
    #     Level_PO.getError(Level_PO.clickXpath(u"//button[@class='btn btn-info']", 2), u"查询按钮未找到！", sys._getframe().f_lineno)
    #
    #     for key in d_dimFirstOfficeList:
    #         if key == dimFirstOffice:
    #             # 编辑 - 新增的科室
    #             tmpFirstOfficeId = d_dimFirstOfficeList[key]
    #             Level_PO.clickXpath(u"//a[@href='/yhzv2/web/app.php/office/office_tmoffice/" + d_dimFirstOfficeList[key] + u"/edit']", 2)
    #             Level_PO.inputIdClear(u"officebundle_tmoffice_officeName", dimFirstOfficeRevise)
    #             Level_PO.getError(Level_PO.clickXpath(u"//button[@class='btn btn-primary']", 2), u"提交按钮未找到！",sys._getframe().f_lineno)
    #
    #             ''' 检查表中修改一级科室是否正确'''
    #             connNCZ.commit()
    #             curNCZ.execute('select office_name from tm_office where office_id="%s" ' % (tmpFirstOfficeId))
    #             pp = curNCZ.fetchone()
    #             if pp[0] == dimFirstOfficeRevise:
    #                 print u"[done], 编辑一级科室, " + dimOrgName + u" - 将 '" + dimFirstOffice + u"' 改为 '" + dimFirstOfficeRevise + u"'"
    #             else:
    #                 Level_PO.getError(u"error", u"yhzPO.py, tm_office表, 编辑一级科室, " + dimOrgName + u" - 将 '" + dimFirstOffice + u"' 改为 '" + dimFirstOfficeRevise + u"'", sys._getframe().f_lineno)
    #             break
    #
    # def newSubOffice(self, d_dimFirstOfficeList, dimOrgName, dimFirstOffice, dimSecondOffice):
    #
    #     ''' 新建二级科室（关联一级科室）'''
    #
    #     # 先选择机构
    #     Level_PO.getError(Level_PO.selectNameText(u"orgId", dimOrgName), dimOrgName + u"未找到！", sys._getframe().f_lineno)
    #     Level_PO.getError(Level_PO.clickXpath(u"//button[@class='btn btn-info']", 2), u"查询按钮未找到！", sys._getframe().f_lineno)
    #
    #     ''' 获取机构id '''
    #     connNCZ.commit()
    #     curNCZ.execute('select org_id from tt_org where  name="%s"' % (dimOrgName))
    #     tmp = curNCZ.fetchone()
    #     tblOrgId = tmp[0]
    #
    #     ''' 获取一级科室的id '''
    #     connNCZ.commit()
    #     curNCZ.execute('select office_id from tm_office where office_name="%s" and org_id="%s"' % (dimFirstOffice, tblOrgId))
    #     tmp = curNCZ.fetchone()
    #     tblFirstOfficeId = tmp[0]
    #
    #     for key in d_dimFirstOfficeList:
    #         if key == dimFirstOffice:
    #             Level_PO.clickXpath(u"//a[@href='/yhzv2/web/app.php/office/office_tmoffice/new/" + str(tblOrgId) + u"/" + d_dimFirstOfficeList[key] + u"']", 2)
    #             Level_PO.inputIdClear(u"officebundle_tmoffice_officeName", dimSecondOffice)
    #             Level_PO.getError(Level_PO.clickXpath(u"//button[@class='btn btn-primary']", 2), u"提交按钮未找到！", sys._getframe().f_lineno)
    #
    #             ''' 检查新增的子科室是否正确 '''
    #             connNCZ.commit()
    #             tt = curNCZ.execute('select level from tm_office where org_id="%s" and top_office_id="%s" ' % (tblOrgId, tblFirstOfficeId))
    #             if tt == 1:
    #                 pp = curNCZ.fetchone()
    #                 if pp[0] == 2:
    #                     print u"[done], 新建二级科室, " + dimOrgName + u" - 一级科室（" + dimFirstOffice + u"）, 二级科室（" + dimSecondOffice + u"）"
    #                 else:
    #                     Level_PO.getError(u"error", u"yhzPO.py, tm_office表, 新建二级科室, " + dimOrgName + u" -  一级科室（" + dimFirstOffice + u"）, 二级科室（" + dimSecondOffice + u"）", sys._getframe().f_lineno)
    #                 break
    #             else:
    #                 print u"errorrrrrrrrrr, 新建二级子科室失败。"
    #
    # def delOffice(self, d_dimFirstOfficeList, dimOrgName, dimFirstOffice):
    #
    #     ''' 删除一级科室 '''
    #
    #     # 先选择机构
    #     Level_PO.getError(Level_PO.selectNameText(u"orgId", dimOrgName), dimOrgName + u"未找到！", sys._getframe().f_lineno)
    #     Level_PO.getError(Level_PO.clickXpath(u"//button[@class='btn btn-info']", 2), u"查询按钮未找到！",sys._getframe().f_lineno)
    #
    #     for key in d_dimFirstOfficeList:
    #         if key == dimFirstOffice:
    #             Level_PO.clickXpath(u"//a[@href='/yhzv2/web/app.php/office/office_tmoffice/" + d_dimFirstOfficeList[key] + u"/delete']", 2)
    #             Level_PO.clickID(u"delete_form_btn_" + d_dimFirstOfficeList[key], 2)
    #
    #             ''' 检查新增的一级科室是否被删除 '''
    #             connNCZ.commit()
    #             kk = curNCZ.execute('select * from tm_office where office_id="%s" ' % (d_dimFirstOfficeList[key]))
    #             if kk == 0:
    #                 print u"[done], 删除一级科室, " + dimOrgName + u" - 一级科室（" + dimFirstOffice + u"）删除成功。"
    #             else:
    #                 Level_PO.getError(u"error", u"yhzPO.py, tm_office表, 删除一级科室, " + dimOrgName + u" - 一级科室（" + dimFirstOffice + u"）删除失败。", sys._getframe().f_lineno)
    #             break
    #
    #
    # def getAuditor(self, dimOrg, dimOffice):
    #
    #     '''设置审核者
    #     如果审核者不存在，系统指派或创建医生一名审核者'''
    #
    #     # 检查机构下的审核者是否存在
    #     curNCZ.execute('select org_id from tt_org where name="%s" ' % (dimOrg))
    #     data0 = curNCZ.fetchone()
    #     tblOrgId = data0[0]  # 机构ID
    #
    #     tblisDoctor = curNCZ.execute('select office_name,doctor_id,name,user_name from tm_doctor where is_ywk=1 and org_id=%s ' % (tblOrgId))
    #     if tblisDoctor == 0:
    #         # 审核者不存在，指派肿瘤科医生一名，如无则自动生成医生
    #         tblisDoctor2 = curNCZ.execute('select office_name,doctor_id,name,user_name from tm_doctor where org_id="%s" and office_name="%s" ' % (tblOrgId, dimOffice))
    #         if tblisDoctor2 == 0:
    #             # 新增医生一名，并设置为审核者
    #             tmpDoctorId = self.createDoctor(u"verify", varDoctorName, varDoctorIdCard, varDoctorPhone,
    #                                               varDoctorGender, varDoctorAccount,
    #                                               varDoctorOrg, varDoctorTitle, varDoctorPosition, varDoctorOffice,
    #                                               varDoctorJobNumber, varHZ, varJX, varHY, varKszr, varAccountType)
    #             # 修改此医生为审核者
    #             curNCZ.execute('update tm_doctor set is_ywk=1,account_type=1 where doctor_id=%s' % (tmpDoctorId))
    #             connNCZ.commit()
    #
    #             curNCZ.execute('select office_name,name,user_name from tm_doctor where doctor_id="%s" ' % (tmpDoctorId))
    #             dd = curNCZ.fetchone()
    #             tblOfficeName = dd[0]
    #             tblUserName = dd[1]
    #             tblLoginName = dd[2]
    #             tblDoctorId = tmpDoctorId
    #
    #         else:
    #             # 系统中指派一名已存在的肿瘤科医生作为审核者
    #             kk = curNCZ.fetchone()
    #             tblOfficeName = kk[0]
    #             tblDoctorId = kk[1]
    #             tblUserName = kk[2]
    #             tblLoginName = kk[3]
    #
    #             # 修改此医生为审核者
    #             curNCZ.execute('update tm_doctor set is_ywk=1,account_type=1 where doctor_id=%s' % (tblDoctorId))
    #             connNCZ.commit()
    #
    #         print u"[done], 当前机构（" + dimOrg + u"）的审核者是 " + tblOfficeName + u" 的" + tblUserName + u"(" + str(tblDoctorId) + u"), " + tblLoginName
    #
    #         return tblLoginName
    #
    #     elif tblisDoctor == 1:
    #         # 审核者存在, 获取当前审核者信息
    #         uu = curNCZ.fetchone()
    #         tblOfficeName = uu[0]
    #         tblDoctorId = uu[1]
    #         tblUserName = uu[2]
    #         tblLoginName = uu[3]
    #         print u"[done], 当前机构（" + dimOrg + u"）的审核者是 " + tblOfficeName + u" 的" + tblUserName + u"(" + str(tblDoctorId) + u"), " + tblLoginName
    #
    #         return tblLoginName
    #
    #     else:
    #         # 审核者有多个
    #         Level_PO.getError(u"error", u"yhzPO.py, tm_doctor表, 机构(" + str(dimOrg) + u")只能有一个审核者，发现表中有" + str(tblisDoctor) + u"个审核者记录!", sys._getframe().f_lineno)
