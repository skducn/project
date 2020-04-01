# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: 配置文件
# ********************************************************************************************************************

import os, sys, MySQLdb, winrm, unittest, xlwt, xlrd, datetime, random, socket, struct, datetime

varTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 当天日期时间时分秒，格式：20170914143616982，类型是 str，
varYMD = datetime.datetime.now().strftime('%Y-%m-%d')  # 当天日期年月格式：2016-06-28 ， 类型是 str

# reload(sys)
# sys.setdefaultencoding("utf-8")
from selenium import webdriver
from Public.PageObject.LevelPO import *
from Public.PageObject.ThirdPO import *
# from Public.PageObject.netPO import *
from xlutils.copy import copy
from pytesseract import *
from PIL import Image
from PIL import ImageGrab


Third_PO = ThirdPO()

# ********************************************************************************************************************

# ''' 测试用例 '''
# varExcel = os.path.join(os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir)), u'TestData/resource.xls')
# varExcelSheetName = u"main,testcase"
#
# # 【log文件的前缀】
# varLogPrefixPath = os.path.join(os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir)), u'log/YHZ_')
#
# # 【数据库 - 云慧诊 统一综合管理平台V2.0】
# connManage = MySQLdb.connect(host="10.111.3.6", user='cetc', passwd='20121221', db='yunhuizhen_v2', port=3306, use_unicode=True)
# curManage = connManage.cursor();curManage.execute('SET NAMES utf8;');connManage.set_character_set('utf8');curManage.execute('show tables')
#
# # 【数据库 - 云慧诊 脑卒中】
# connNCZ = MySQLdb.connect(host="10.111.3.4", user='cetc', passwd='20121221', db='yunhuizhen_ncz', port=3306, use_unicode=True)
# curNCZ = connNCZ.cursor();curNCZ.execute('SET NAMES utf8;');connNCZ.set_character_set('utf8');curNCZ.execute('show tables')

''' Webdriver '''
# driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/usr/local/bin/geckodriver', firefox_options=None, log_path='geckodriver.log')
driver = webdriver.Firefox()
driver.implicitly_wait(10)
Level_PO = LevelPO(driver)

#
# # ********************************************************************************************************************
#
# ''' 测试环境 '''
#
# # 云慧诊 - 统一综合管理平台V2.0
# varURLmanage = u"http://10.111.3.5:88/yhzv2/web/app_test.php/curuser/security/login"
#
# # 云慧诊 - 机构 管理后台
# varOrgUrl = u"https://cetc.iotcetc.com:8084/yhzv2/web/app.php/curuser/security/login?sign=ncz"  # 脑卒中
#
# # 云慧诊 - 医生 管理后台
# varDoctorUrl = u"https://cetc.iotcetc.com:8084/yhzv2-doctor/web/app.php/login?sign=ncz"  # 脑卒中


#
#
# ''' 上 海 第 五 人 民 医 院 '''
#
# '''机构信息'''
# varOrgAccount = u"gdwrm"  # 机构管理员
# varOrgPass = u"123456"   # 管理员密码
# varOrgName = u"上海第五人民医院"  # 机构名称
#
# ''' 获取审核者 '''
# connNCZ.commit()
# tblOrgName = curNCZ.execute('select doctor_id from tm_doctor where org_name="%s" and is_ywk=1 ' % (varOrgName))
# if tblOrgName == 1:
#     tmp = curNCZ.fetchone()
#     tblDoctorId = tmp[0]
#     # tblOfficeName = tmp[1]
#
#
# # 自动获取审核者，如没有则添加一个
# varOrgAdmin = u"五院管理员"  # 机构管理员姓名
# varOrgAdminPhone = u"13816101111"  # 机构管理员电话
#
# '''机构审核者'''
# varOrgAuditorAccount = u"Dwy001"   # 陈医生 ，神经内科
#
# '''科室主任'''
# # 肿瘤科的科室主任
# # 机构科室主任
#
#
#
# # 肿瘤科，科室主任
# # var =
#
#
#
# '''科室信息'''
# varFirstOffice = u"肿瘤科"   # 一级科室名称
# varSecondOffice = u"脑部甲级肿瘤" # 二级科室名称
# varThirdOffice = u"脑部左翼三级"  # 三级科室名称
#
#
# '''医生信息, 13个必填项'''
# varDoctorName = Third_PO.randomUserName()  # *姓名
# varDoctorIdCard = Third_PO.randomIdCard()  # *身份证号
# varDoctorPhone = Third_PO.randomPhone()  # *手机号码
# varDoctorGender = Third_PO.getGender(varDoctorIdCard)  # 性别
# varDoctorAccount = Third_PO.getUserNameinitial(varDoctorName) + Third_PO.randomDigit(3)  # *登录帐号 （规则：D + 用户名首字母 + 3个数字）
# varDoctorOrg = u"上海第五人民医院"  # *机构名称
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
# '''患者信息, 6个必填项'''
# varPatientName = Third_PO.randomUserName()  # *患者姓名
# varPatientIdCard = Third_PO.randomIdCard()  # *患者身份证
# varPatientPhone = Third_PO.randomPhone()  # *患者电话
# varPatientGender = Third_PO.getGender(varPatientIdCard)  # 性别
# varPatientAge = Third_PO.getAge(varPatientIdCard)  # 年龄
# varPatientAddress = u"上海市浦东新区南泉北路1200弄23号1203室"  # 家庭地址
# varPatientDiagnosisNo = Third_PO.randomDigit(7)   # *就诊号
# varPatientOrg = u"上海第五人民医院"  # *医疗机构
# varOffice = u"肿瘤科"   #  *所属科室
# varPatientYibaoNo = Third_PO.getUserNameinitial(varPatientName) + Third_PO.randomDigit(7)   # 医保号码
# # 主治医生依据 医疗机构和所属科室自动匹配，默认匹配到的第一个医生。
# varPatientDiseasyHistory = u"10年前得过血小板减少"  #  简要病史



# # 脑卒中，机构信息
# # 机构管理员
# varOrgAccount = u"gncz"
# varOrgPass = u"123456"
# # 机构名
# varOrgName = u"脑卒中智慧医联体"
# # 机构名ID
# curNCZ.execute('select org_id from tt_org where name="%s" ' % (varOrgName))
# data0 = curNCZ.fetchone()
# varOrgId = data0[0]
# # 机构名管理员ID
# curNCZ.execute('select doctor_id from vw_doctor where org_name="%s" ' % (varOrgName))
# data1 = curNCZ.fetchone()
# varOrgAdminId = data1[0]






