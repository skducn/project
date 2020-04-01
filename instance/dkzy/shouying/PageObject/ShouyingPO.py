# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2018-3-15
# Description: 首营 对象库
#***************************************************************

import sys, os, platform
sys.path.append("..")
from config.config import *

class ShouyingPO(object):

    def __init__(self, Level_PO):
         self.Level_PO = Level_PO

    def getEnterpriseTypeAndName(self, varPhone):
        # 通过手机号获得企业名称和企业类型（非数字）
        Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (varPhone))
        t0 = Database_PO.cur.fetchone()
        Database_PO.cur.execute('select name,type from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (t0[0]))
        t1 = Database_PO.cur.fetchone()
        varCompanyName = t1[0]
        if t1[1] == 1:
            varCompanyType = u"生产企业"
        elif t1[1] == 2:
            varCompanyType = u"经营企业"
        elif t1[1] == 3:
            varCompanyType = u"医疗机构 - 公立医院"
        elif t1[1] == 4:
            varCompanyType = u"医疗机构 - 私立医院"
        elif t1[1] == 5:
            varCompanyType = u"医疗机构 - 诊所"
        elif t1[1] == 6:
            varCompanyType = u"零售药店"
        return (varCompanyName,varCompanyType)

    '''1、注册账号'''
    def register(self, varEmail, varPass, varCompanyName, varType, varPhone):
        '''注册账号'''

        self.Level_PO.inputId("email", varEmail)  # 邮箱
        self.Level_PO.inputId("password", varPass)  # 密码
        self.Level_PO.inputId("re-password", varPass)  # 确认密码
        self.Level_PO.inputId("company-name", varCompanyName)  # 公司名称
        self.Level_PO.selectNameText("company-type", varType)  # 企业类型
        self.Level_PO.inputId("phone-number", varPhone)  # 手机号
        self.Level_PO.clickXpath("//input[@id='protocol']", 2)  # 勾选我已阅读并同意
        self.Level_PO.clickLinktext(u"发送验证码", 2)
        varCaptcha = connRedis.get('sms_' + varPhone)
        if varCaptcha == None :
            x = self.Level_PO.getXpathText("//p[@id='message']")
            printColor('\033[1;31;47m', 'printRed', x)
            self.Level_PO.close_driver()
            sys.exit()
        else:
            self.Level_PO.inputId("captcha", varCaptcha.split('code":"')[1].split('"')[0])  # 验证码
            self.Level_PO.clickXpath("//button[@type='submit']", 1)  # 立即注册
        # 检查表中记录是否存在，企业类型是否正确。
        if self.Level_PO.getXpathText("//p[@id='message']") == u"error":
            tblCount = 0
            tblCount = Database_PO.cur.execute('select type from tt_enterprise where link_phone="%s" order by enterprise_id desc limit 1' % (varPhone))
            if tblCount == 1:
                t1 = Database_PO.cur.fetchone()
                if t1[0] == 1: printColor('\033[1;31;47m', 'printGreen', u"1、恭喜您，生产企业（" + varPhone + u"）注册成功。下一步资料认证：python authenticate.py " + varPhone)
                elif t1[0] == 2: printColor('\033[1;31;47m', 'printGreen', u"1、恭喜您，经营企业（" + varPhone + u"）注册成功。下一步资料认证：python authenticate.py " + varPhone)
                elif t1[0] == 3: printColor('\033[1;31;47m', 'printGreen', u"1、恭喜您，公立医院（" + varPhone + u"）注册成功。下一步资料认证：python authenticate.py " + varPhone)
                elif t1[0] == 4: printColor('\033[1;31;47m', 'printGreen', u"1、恭喜您，私立医院（" + varPhone + u"）注册成功。下一步资料认证：python authenticate.py " + varPhone)
                elif t1[0] == 5: printColor('\033[1;31;47m', 'printGreen', u"1、恭喜您，诊所（" + varPhone + u"）注册成功。下一步资料认证：python authenticate.py " + varPhone)
                elif t1[0] == 6: printColor('\033[1;31;47m', 'printGreen', u"1、恭喜您，零售药店（" + varPhone + u"）注册成功。下一步资料认证：python authenticate.py " + varPhone)
            else:
                printColor('\033[1;31;47m', 'printRed', u"1、很抱歉，企业账号（" + varPhone + u"）注册失败。")
        else:
            print self.Level_PO.getXpathText("//p[@id='message']")

    def login(self, varUser, varPass):
        '''登录'''
        self.Level_PO.inputName("username", varUser)
        self.Level_PO.inputName("password", varPass)
        self.Level_PO.inputId("captcha", "00000")
        self.Level_PO.clickXpath(u"//button[@type='submit']", 2)

    '''2、资料认证2'''
    def licence(self, varCompanyType, varScope, drugCode, drugIndate, drugPic, GMPPic, makeupPic, makeupIndate, makeupPic2, foodCode, foodIndate, foodPic, equipmentPic):
        ''' 经营范围之许可证'''
        '''生产企业'''
        if varCompanyType == u"生产企业":
            # 7.药品生产许可证
            self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/input", drugCode)  # 药品生产许可证编号
            self.Level_PO.inputXpath("//input[@ng-model='a.value.from']", drugIndate)  # 药品生产许可证有效期：
            self.Level_PO.script('document.getElementById("file2").style.display="block"', 2) # 上传图片,请上传药品生产许可证照片
            self.Level_PO.sendKeysId_mac("file2", drugPic)
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
            # 8.GMP药品生产质量管理规范认证证书
            self.Level_PO.script('document.getElementById("file0").style.display="block"', 2)
            self.Level_PO.sendKeysId_mac("file0", GMPPic)  # 上传图片,
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
            # 9.消毒产品卫生
            self.Level_PO.script('document.getElementById("file0").style.display="block"', 2)
            self.Level_PO.sendKeysId_mac("file0", foodPic)  # 上传图片,上传食品生产许可证:
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
            # 10.食品卫生许可证
            self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/input", foodCode)  # 食品生产许可证编号:
            self.Level_PO.inputXpath("//input[@ng-model='a.value.from']", foodIndate)  # 食品生产许可证有效期：
            self.Level_PO.script('document.getElementById("file2").style.display="block"', 2)
            self.Level_PO.sendKeysId_mac("file2", foodPic)  # 上传图片,上传食品生产许可证:
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
            # 11.医疗机械生产
            self.Level_PO.script('document.getElementById("file0").style.display="block"', 2)
            self.Level_PO.sendKeysId_mac("file0", equipmentPic)  # 上传图片,上传医疗器械生产许可证：
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
            # 12.化妆品生产
            self.Level_PO.script('document.getElementById("file0").style.display="block"', 2)  #
            self.Level_PO.sendKeysId_mac("file0", makeupPic)  # 上传图片, 上传化妆品生产许可证或化妆品生产企业卫生许可证：
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
            # 13.全国工业产品生产许可证
            self.Level_PO.inputXpath("//input[@ng-model='a.value.from']", makeupIndate)  # 全国工业产品生产许可证有效期：
            self.Level_PO.script('document.getElementById("file1").style.display="block"', 2)  #
            self.Level_PO.sendKeysId_mac("file1", makeupPic2)  # 上传图片, 上传全国工业产品生产许可证：（截止2016年12月31日）：
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认

        '''经营企业、零售药店'''
        if varCompanyType == u"经营企业" or varCompanyType == u"零售药店":
            # 7. 药品经营许可证
            self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/input", drugCode)  # 药品经营许可证编号
            self.Level_PO.inputXpath("//input[@ng-model='a.value.from']", drugIndate)  # 药品经营许可证有效期
            self.Level_PO.script('document.getElementById("file2").style.display="block"', 2) # 上传药品经营许可证照片
            self.Level_PO.sendKeysId_mac("file2", drugPic)
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
            # 8. GSP药品经营质量管理规范认证证书
            self.Level_PO.script('document.getElementById("file0").style.display="block"', 2)
            self.Level_PO.sendKeysId_mac("file0", GMPPic)
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
            # 9.食品经营许可证
            self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/input", foodCode)  # 食品生产许可证编号:
            self.Level_PO.inputXpath("//input[@ng-model='a.value.from']", foodIndate)  # 食品生产许可证有效期：
            self.Level_PO.script('document.getElementById("file2").style.display="block"', 2)
            self.Level_PO.sendKeysId_mac("file2", foodPic)  # 上传图片,上传食品生产许可证:
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
            # 10.医疗器械经营
            self.Level_PO.script('document.getElementById("file0").style.display="block"', 2)
            self.Level_PO.sendKeysId_mac("file0", equipmentPic)  # 上传图片,上传医疗器械生产许可证：
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
    def authenticate(self, varCompanyType, varType, varBusinessLicence, varProvince, varMunicipal, varAddress, varSdate, varEdate, isLongValid, varBusinessLicencePic, varZZJGDMZ, varZZJGDMZpic,varAccountName, varAccountCode, varAccountBank, varAccountAddress, varAccountPic,varOprName, varOprIdcard, varOprTelephone, varOprIdcardPic1, varOprIdcardPic2, varOprLettePic1,varAuthorizationPic, varOfficialPic, varQualityPic, varRange,drugCode, drugIndate, drugPic, GMPPic, makeupPic, makeupIndate, makeupPic2, foodCode, foodIndate, foodPic, equipmentPic, varMedicalCode, varMedicalIndate, varMedicalPic):
        ''' 认证'''
        # 1，企业类型，证件类型，企业全称，营业执照注册号，企业所在省份，地区，详细地址，有效期开始，有效期结束，长期有效，营业执照PIC，[组织机构代码证号码，组织机构代码证PIC]
        # 2，开户名称，开会账号，开户银行，开户所在地，开户许可证PIC
        # 3，经办人姓名，身份证号码，手机号码，固定电话，工作邮箱，身份证前，身份证后，经办授权委托书
        # 4，企业授权书PIC，行政公章PIC，质量管理部门印章PIC，经营范围
        # 5，生产企业之许可证（药品编号，药品有效期，药品PIC，GMPPIC, 化妆品PIC1,化妆品有效期，化妆品PIC2，食品编号，食品有效期，食品PIC，医疗器械PIC）
        # 5，经营企业之许可证（药品编号，药品有效期，药品PIC，GSPPIC, 食品编号，食品有效期，食品PIC，医疗器械PIC）
        if varCompanyType == u"医疗机构 - 公立医院":
            # 1.医疗机构执业许可证
            self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/input", varMedicalCode)  # 医疗机构执业许可证登记号
            self.Level_PO.inputXpath("//input[@ng-model='a.value.from']", varMedicalIndate)  # 医疗机构执业许可证有效期
            self.Level_PO.script('document.getElementById("file2").style.display="block"', 2)
            self.Level_PO.sendKeysId_mac("file2", varMedicalPic)  # 上传图片:  医疗机构执业许可证PIC
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
        else:
            # 1.营业执照
            if varType == u"普通营业执照":  # 证件类型 (普通营业执照,多证合一营业执照)
                self.Level_PO.clickXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/div[1]/label/input", 2)
            else:  # 多证合一营业执照
                self.Level_PO.clickXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/div[2]/label/input", 2)
            self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[3]/div/div/input", varBusinessLicence)  # 营业执照注册号
            self.Level_PO.selectXpathText("//section[@id='material_edit']/div/div[2]/form/div[4]/div/div/div/div[1]/select", varProvince)  # 企业所在地区 省市
            sleep(2)
            self.Level_PO.selectXpathText("//section[@id='material_edit']/div/div[2]/form/div[4]/div/div/div/div[2]/select", varMunicipal)  # 企业所在地区 区县
            self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[5]/div/div/input", varAddress)  # 详细地址
            self.Level_PO.inputXpath("//input[@ng-model='a.value.from']", varSdate)  # 有效期 开始时间
            self.Level_PO.inputXpath("//input[@ng-model='a.value.to']", varSdate)  # 有效期 结束时间
            if isLongValid == "on":
                self.Level_PO.clickXpath("//input[@ng-model='a.no_expire']", varSdate)  # 勾选 长期有
            self.Level_PO.script('document.getElementById("file6").style.display="block"', 2)  # 上传图片: 多证合一营业执照
            self.Level_PO.sendKeysId_mac("file6", varBusinessLicencePic)
            # 组织机构代码证 for 普通营业执照
            if varType == u"普通营业执照":
                self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[8]/div/div/input", varZZJGDMZ)  # 组织机构代码证号码
                self.Level_PO.script('document.getElementById("file8").style.display="block"', 2)
                self.Level_PO.sendKeysId_mac("file0", varZZJGDMZpic)  # 上传图片: 请上传组织机构代码证
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认

        if varCompanyType == u"医疗机构 - 私立医院" or varCompanyType == u"医疗机构 - 诊所":
            # 2.医疗机构执业许可证
            self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/input", varMedicalCode)  # 医疗机构执业许可证登记号
            self.Level_PO.inputXpath("//input[@ng-model='a.value.from']", varMedicalIndate)  # 医疗机构执业许可证有效期
            self.Level_PO.script('document.getElementById("file2").style.display="block"', 2)
            self.Level_PO.sendKeysId_mac("file2", varMedicalPic)  # 上传图片:  医疗机构执业许可证PIC
            self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
            self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认

        # 2.开户许可证
        self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/input", varAccountName)  # 开户名称
        self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[2]/div/div/input", varAccountCode)  # 开户账号
        self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[3]/div/div/input", varAccountBank)  # 开户银行
        self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[4]/div/div/input", varAccountAddress)  # 开户所在地
        self.Level_PO.script('document.getElementById("file4").style.display="block"', 2)
        self.Level_PO.sendKeysId_mac("file4", varAccountPic)  # 上传图片: 请上传开户许可证照片
        self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认

        # 3.经办人信息
        self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/input", varOprName)  # 经办人姓名
        self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[2]/div/div/input", varOprIdcard)  # 身份证号码
        self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[3]/div/div/input", varOprTelephone)  # 固定电话: (多个固定电话以','分隔)
        self.Level_PO.script('document.getElementById("file3").style.display="block"', 2)
        self.Level_PO.sendKeysId_mac("file3", varOprIdcardPic1)  # 上传图片,身份证前
        self.Level_PO.script('document.getElementById("file4").style.display="block"', 2)
        self.Level_PO.sendKeysId_mac("file4", varOprIdcardPic2)  # 上传图片,身份证后
        self.Level_PO.script('document.getElementById("file5").style.display="block"', 2)
        self.Level_PO.sendKeysId_mac("file5", varOprLettePic1)  # 上传图片,经办授权委托书
        self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认

        # 4.企业授权书
        self.Level_PO.script('document.getElementById("file0").style.display="block"', 2)
        self.Level_PO.sendKeysId_mac("file0", varAuthorizationPic)  # 上传图片,企业授权书
        self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认

        # 5.印章备案样式
        self.Level_PO.script('document.getElementById("file0").style.display="block"', 2)
        self.Level_PO.sendKeysId_mac("file0", varOfficialPic)  # 上传图片,行政公章
        self.Level_PO.script('document.getElementById("file1").style.display="block"', 2)
        self.Level_PO.sendKeysId_mac("file1", varQualityPic)  # 上传图片,质量管理部门印章
        self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认

        # 6.经营范围 - （写死全选经营范围）
        varRangeToNum = str(varRange).replace(u"药品", "1").replace(u"中药饮片", "2").replace(u"化妆品", "3").replace(u"食品", "4").replace(u"日用品", "5").replace(u"消毒产品", "6").replace(u"保健4", "7").replace(u"医疗器械", "8")
        if ',' in varRangeToNum:
            # 勾选多个经营范围
            x = len(str(varRangeToNum).split(','))
            for i in range(x):
                self.Level_PO.clickXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/div[" + str(varRangeToNum).split(',')[i] + "]/label/input", 2)
        else:
            # 勾选单个经营范围
            self.Level_PO.clickXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/div[" + str(varRangeToNum) + "]/label/input", 2)
        self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认

        if varCompanyType == u"生产企业" or varCompanyType == u"经营企业" or varCompanyType == u"零售药店":
            # 经营范围 - 遍历许可证（写死全选经营范围）
            self.licence(varCompanyType, varRange, drugCode, drugIndate, drugPic, GMPPic, makeupPic, makeupIndate, makeupPic2, foodCode, foodIndate, foodPic, equipmentPic)

        self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认

        # 企业信息已提交成功
        return self.Level_PO.getXpathText("//div[@class='box-body']/p[1]")


        # '''公立医院'''
        # if varCompanyType == u"医疗机构 - 公立医院":
        #     # 医疗机构执业许可证
        #     self.Level_PO.inputXpath("//section[@id='material_edit']/form/div[1]/div/div[2]/div[1]/div/div/input", varMedicalCode)  # 医疗机构执业许可证登记号
        #     self.Level_PO.inputXpath("//section[@id='material_edit']/form/div[1]/div/div[2]/div[2]/div/div[1]/input", varMedicalIndate)  # 医疗机构执业许可证有效期
        #     self.Level_PO.script('document.getElementById("file02").style.display="block"', 2)
        #     self.Level_PO.sendKeysId_mac("file02", varMedicalPic)  # 上传图片:  医疗机构执业许可证PIC

            # # 开户许可证
            # self.Level_PO.inputXpath("//section[@id='material_edit']/form/div[2]/div/div[2]/div[1]/div/div/input", varAccountName)  # 开户名称
            # self.Level_PO.inputXpath("//section[@id='material_edit']/form/div[2]/div/div[2]/div[2]/div/div/input", varAccountCode)  # 开户账号
            # self.Level_PO.inputXpath("//section[@id='material_edit']/form/div[2]/div/div[2]/div[3]/div/div/input", varAccountBank)  # 开户银行
            # self.Level_PO.inputXpath("//section[@id='material_edit']/form/div[2]/div/div[2]/div[4]/div/div/input", varAccountAddress)  # 开户所在地
            # self.Level_PO.script('document.getElementById("file14").style.display="block"', 2)
            # self.Level_PO.sendKeysId_mac("file14", varAccountPic)  # 上传图片: 请上传开户许可证照片
            # # 公立医院 - 经办人信息
            # self.Level_PO.inputXpath("//section[@id='material_edit']/form/div[3]/div/div[2]/div[1]/div/div/input", varOprName)  # 经办人姓名
            # self.Level_PO.inputXpath("//section[@id='material_edit']/form/div[3]/div/div[2]/div[2]/div/div/input", varOprIdcard)  # 身份证号码
            # self.Level_PO.inputXpath("//section[@id='material_edit']/form/div[3]/div/div[2]/div[4]/div/div/input", varOprTelephone)  # 固定电话
            # self.Level_PO.script('document.getElementById("file25").style.display="block"', 2)
            # self.Level_PO.sendKeysId_mac("file25", varOprIdcardPic1)  # 上传图片,身份证前
            # self.Level_PO.script('document.getElementById("file26").style.display="block"', 2)
            # self.Level_PO.sendKeysId_mac("file26", varOprIdcardPic2)  # 上传图片,身份证后
            # self.Level_PO.script('document.getElementById("file27").style.display="block"', 2)
            # self.Level_PO.sendKeysId_mac("file27", varOprLettePic1)  # 上传图片,经办授权委托书
            # # 公立医院 - 企业授权书
            # self.Level_PO.script('document.getElementById("file30").style.display="block"', 2)
            # self.Level_PO.sendKeysId_mac("file30", varAuthorizationPic)  # 上传图片,企业授权书
            # # 公立医院 - 印章备案
            # self.Level_PO.script('document.getElementById("file40").style.display="block"', 2)
            # self.Level_PO.sendKeysId_mac("file40", varOfficialPic)  # 上传图片,行政公章
            # self.Level_PO.script('document.getElementById("file41").style.display="block"', 2)
            # self.Level_PO.sendKeysId_mac("file41", varQualityPic)  # 上传图片,质量管理部门印章
            # # 公立医院 - 经营范围
            # varRangeToNum = str(varRange).replace(u"药品", "1").replace(u"中药饮片", "2").replace(u"化妆品", "3").replace(u"食品", "4").replace(u"日用品", "5").replace(u"消毒产品", "6").replace(u"保健4", "7").replace(u"医疗器械", "8")
            # if ',' in varRangeToNum:
            #     # 勾选多个经营范围
            #     x = len(str(varRangeToNum).split(','))
            #     for i in range(x):
            #         self.Level_PO.clickXpath("//section[@id='material_edit']/form/div[6]/div/div[2]/div/div/div/div[" + str(varRangeToNum).split(',')[i] + "]/label/input", 2)
            #         self.licence(varCompanyType, str(varRange).split(',')[i], drugCode, drugIndate, drugPic, GMPPic, makeupPic, makeupIndate, makeupPic2, foodCode, foodIndate, foodPic, equipmentPic)
            # else:
            #     # 勾选单个经营范围
            #     self.Level_PO.clickXpath("//section[@id='material_edit']/form/div[6]/div/div[2]/div/div/div/div[" + str(varRangeToNum) + "]/label/input", 2)
            #     # 经营范围的许可证
            #     self.licence(varCompanyType, varRange, drugCode, drugIndate, drugPic, GMPPic, makeupPic, makeupIndate, makeupPic2, foodCode, foodIndate, foodPic, equipmentPic)

        # elif varCompanyType == u"医疗机构 - 私立医院" or varCompanyType == u"医疗机构 - 诊所":
        #
        #     '''私立医院、诊所'''
        #     # 1.营业执照
        #     if varType == u"普通营业执照":  # 证件类型 (普通营业执照,多证合一营业执照)
        #         self.Level_PO.clickXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/div[1]/label/input", 2)
        #     else:  # 多证合一营业执照
        #         self.Level_PO.clickXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/div[2]/label/input", 2)
        #     self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[3]/div/div/input", varBusinessLicence)  # 营业执照注册号
        #     self.Level_PO.selectXpathText("//section[@id='material_edit']/div/div[2]/form/div[4]/div/div/div/div[1]/select", varProvince)  # 企业所在地区 省市
        #     sleep(2)
        #     self.Level_PO.selectXpathText("//section[@id='material_edit']/div/div[2]/form/div[4]/div/div/div/div[2]/select", varMunicipal)  # 企业所在地区 区县
        #     self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[5]/div/div/input", varAddress) # 详细地址
        #     self.Level_PO.inputXpath("//input[@ng-model='a.value.from']", varSdate) # 有效期 开始时间
        #     self.Level_PO.inputXpath("//input[@ng-model='a.value.to']", varSdate) # 有效期 结束时间
        #     if isLongValid == "on":
        #         self.Level_PO.clickXpath("//input[@ng-model='a.no_expire']", varSdate)  # 勾选 长期有
        #     self.Level_PO.script('document.getElementById("file6").style.display="block"', 2) # 上传图片: 多证合一营业执照
        #     self.Level_PO.sendKeysId_mac("file6", varBusinessLicencePic)
        #     # 组织机构代码证 for 普通营业执照
        #     if varType == u"普通营业执照":
        #         self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[8]/div/div/input", varZZJGDMZ)  # 组织机构代码证号码
        #         self.Level_PO.script('document.getElementById("file8").style.display="block"', 2)
        #         self.Level_PO.sendKeysId_mac("file0", varZZJGDMZpic)  # 上传图片: 请上传组织机构代码证
        #     self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        #     self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
        #
        #     # 2.医疗机构执业许可证
        #     self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/input", varMedicalCode) # 医疗机构执业许可证登记号
        #     self.Level_PO.inputXpath("//input[@ng-model='a.value.from']", varMedicalIndate) # 医疗机构执业许可证有效期
        #     self.Level_PO.script('document.getElementById("file2").style.display="block"', 2)
        #     self.Level_PO.sendKeysId_mac("file2", varMedicalPic)  # 上传图片:  医疗机构执业许可证PIC
        #     self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        #     self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
        #
        #     # 3.开户许可证
        #     self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/input", varAccountName)  # 开户名称
        #     self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[2]/div/div/input", varAccountCode)  # 开户账号
        #     self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[3]/div/div/input", varAccountBank)  # 开户银行
        #     self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[4]/div/div/input", varAccountAddress)  # 开户所在地
        #     self.Level_PO.script('document.getElementById("file4").style.display="block"', 2)
        #     self.Level_PO.sendKeysId_mac("file4", varAccountPic)  # 上传图片: 请上传开户许可证照片
        #     self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        #     self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
        #
        #     # 4.经办人信息
        #     self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/input", varOprName) # 经办人姓名
        #     self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[2]/div/div/input", varOprIdcard)  # 身份证号码
        #     self.Level_PO.inputXpath("//section[@id='material_edit']/div/div[2]/form/div[4]/div/div/input", varOprTelephone)  # 固定电话
        #     self.Level_PO.script('document.getElementById("file5").style.display="block"', 2)
        #     self.Level_PO.sendKeysId_mac("file5", varOprIdcardPic1)  # 上传图片,身份证前
        #     self.Level_PO.script('document.getElementById("file6").style.display="block"', 2)
        #     self.Level_PO.sendKeysId_mac("file6", varOprIdcardPic2)  # 上传图片,身份证后
        #     self.Level_PO.script('document.getElementById("file7").style.display="block"', 2)
        #     self.Level_PO.sendKeysId_mac("file7", varOprLettePic1)  # 上传图片,经办授权委托书
        #     self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        #     self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
        #
        #     # 5.企业授权书
        #     self.Level_PO.script('document.getElementById("file0").style.display="block"', 2)
        #     self.Level_PO.sendKeysId_mac("file0", varAuthorizationPic)  # 上传图片,企业授权书
        #     self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        #     self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
        #
        #     # 6.印章备案样式
        #     self.Level_PO.script('document.getElementById("file0").style.display="block"', 2)
        #     self.Level_PO.sendKeysId_mac("file0", varOfficialPic)  # 上传图片,行政公章
        #     self.Level_PO.script('document.getElementById("file1").style.display="block"', 2)
        #     self.Level_PO.sendKeysId_mac("file1", varQualityPic)  # 上传图片,质量管理部门印章
        #     self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        #     self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
        #
        #     # 7.经营范围
        #     varRangeToNum = str(varRange).replace(u"药品", "1").replace(u"中药饮片", "2").replace(u"化妆品", "3").replace(u"食品","4").replace(u"日用品", "5").replace(u"消毒产品", "6").replace(u"保健4", "7").replace(u"医疗器械", "8")
        #     if ',' in varRangeToNum:
        #         # 勾选多个经营范围
        #         x = len(str(varRangeToNum).split(','))
        #         for i in range(x):
        #             self.Level_PO.clickXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/div[" + str(varRangeToNum).split(',')[i] + "]/label/input", 2)
        #             self.licence(varCompanyType, str(varRange).split(',')[i], drugCode, drugIndate, drugPic, GMPPic, makeupPic, makeupIndate, makeupPic2, foodCode, foodIndate, foodPic, equipmentPic)
        #     else:
        #         # 勾选单个经营范围
        #         self.Level_PO.clickXpath("//section[@id='material_edit']/div/div[2]/form/div[1]/div/div/div[" +str(varRangeToNum) + "]/label/input", 2)
        #         # 经营范围的许可证
        #         self.licence(varCompanyType, varRange, drugCode, drugIndate, drugPic, GMPPic, makeupPic, makeupIndate, makeupPic2, foodCode, foodIndate, foodPic, equipmentPic)
        #     self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 下一步
        #     self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
        #
        # else:
        #     pass

        # self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 提交
        # self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 4)  # 确认

    '''5、交换设置5'''
    def setExchange_enterprise(self):
        # 企业交换资料 - 生产企业
        if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_business_licence']") == False:
            self.Level_PO.clickId("standardClassEId_business_licence", 2)  # 营业执照
            printColor('\033[1;31;47m', 'printGreen', u"已勾选，1、营业执照。")
        # if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_gmp']") == False:
        #     self.Level_PO.clickId("standardClassEId_gmp", 2)  # GMP药品生产质量管理规范认证证书
        #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，2、GMP药品生产质量管理规范认证证书。")
        # if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_industry_product_licence']") == False:
        #     self.Level_PO.clickId("standardClassEId_industry_product_licence", 2)  # 全国工业产品生产许可证
        #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，3、全国工业产品生产许可证。")
        # if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_produce_authorize']") == False:
        #     self.Level_PO.clickId("standardClassEId_produce_authorize", 2)  # 药品生产许可证
        #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，4、药品生产许可证。")
        # if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_cosmetics_licence']") == False:
        #     self.Level_PO.clickId("standardClassEId_cosmetics_licence", 2)  # 化妆品生产
        #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，5、化妆品生产。")
        # if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_food_produce_authorize']") == False:
        #     self.Level_PO.clickId("standardClassEId_food_produce_authorize", 2)  # 食品生产许可证
        #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，6、食品生产许可证。")
        # if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_disinfect_license']") == False:
        #     self.Level_PO.clickId("standardClassEId_disinfect_license", 2)  # 消毒产品生产
        #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，7、消毒产品生产。")
        # if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_medical_instrument_licence']") == False:
        #     self.Level_PO.clickId("standardClassEId_medical_instrument_licence", 2)  # 医疗器械生产
        #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，8、医疗器械生产。")
    def setExchange_operate(self):
        # 企业交换资料 - 经营企业
        if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_business_licence']") == False:
            self.Level_PO.clickId("standardClassEId_business_licence", 2)  # 营业执照
            printColor('\033[1;31;47m', 'printGreen', u"已勾选，1、营业执照。")
        # if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_sale_authorize']") == False:
        #     self.Level_PO.clickId("standardClassEId_sale_authorize", 2)  # 药品经营许可证
        #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，2、药品经营许可证。")
        # if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_gsp']") == False:
        #     self.Level_PO.clickId("standardClassEId_gsp", 2)  # GSP药品经营质量管理规范认证证书
        #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，3、GSP药品经营质量管理规范认证证书。")
        # if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_food_business']") == False:
        #     self.Level_PO.clickId("standardClassEId_food_business", 2)  # 食品经营许可证
        #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，4、食品经营许可证。")
        # if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_medical_instrument_business_licence']") == False:
        #     self.Level_PO.clickId("standardClassEId_medical_instrument_business_licence", 2)  # 医疗器械经营
        #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，5、医疗器械经营。")
    def setExchange_public(self):
        # 企业交换资料 - 公立医院
        if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_medical_practice_license']") == False:
            self.Level_PO.clickId("standardClassEId_medical_practice_license", 2)  # 医疗机构执业许可证
            printColor('\033[1;31;47m', 'printGreen', u"已勾选，1、医疗机构执业许可证。")
    def setExchange_private(self):
        # 企业交换资料 - 私立医院
        if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_business_licence']") == False:
            self.Level_PO.clickId("standardClassEId_business_licence", 2)  # 营业执照
            printColor('\033[1;31;47m', 'printGreen', u"已勾选，1、营业执照。")
        if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_medical_practice_license']") == False:
            self.Level_PO.clickId("standardClassEId_medical_practice_license", 2)  # 医疗机构执业许可证
            printColor('\033[1;31;47m', 'printGreen', u"已勾选，2、医疗机构执业许可证。")
    def setExchange_clinic(self):
        # 企业交换资料 - 诊所
        if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_business_licence']") == False:
            self.Level_PO.clickId("standardClassEId_business_licence", 2)  # 营业执照
            printColor('\033[1;31;47m', 'printGreen', u"已勾选，1、营业执照。")
        if self.Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_medical_practice_license']") == False:
            self.Level_PO.clickId("standardClassEId_medical_practice_license", 2)  # 医疗机构执业许可证
            printColor('\033[1;31;47m', 'printGreen', u"已勾选，2、医疗机构执业许可证。")

    '''6、发起企业首营7'''
    def statisticsShouying(self, var1):
        # 首页 - 首营交换统计
        # 我收到的申请
        self.Level_PO.clickLinktext(u"首页", 2)
        varReceiveMain = self.Level_PO.getXpathText("//div[@class='item ']/div[1]/div[1]")  # 我收到的申请
        varReceiveleft = self.Level_PO.getXpathText("//div[@class='item ']/div[2]/div/div/div[1]/a/h4")  # 企业首营数
        varReceiveRight = self.Level_PO.getXpathText("//div[@class='item ']/div[2]/div/div/div[2]/a/h4")  # 品种首营数
        # 我发起的申请
        varSendMain = self.Level_PO.getXpathText("//div[@class='item item2']/div[1]/div[1]")  # 我发起的申请
        varSendLeft = self.Level_PO.getXpathText("//div[@class='item item2']/div[2]/div/div/div[1]/a/h4")  # 企业首营数
        varSendRight = self.Level_PO.getXpathText("//div[@class='item item2']/div[2]/div/div/div[2]/a/h4")  # 品种首营数
        # 交换中
        varSwitchMain = self.Level_PO.getXpathText("//div[@class='item item3']/div[1]/div[1]")  # 交换中
        varSwitchLeft = self.Level_PO.getXpathText("//div[@class='item item3']/div[2]/div/div/div[1]/a/h4")  # 企业首营数
        varSwitchright = self.Level_PO.getXpathText("//div[@class='item item3']/div[2]/div/div/div[2]/h4")  # 品种首营数
        # 我拒绝的申请
        varRefuseMain = self.Level_PO.getXpathText("//div[@class='item item4']/div[1]/div[1]")  # 我拒绝的申请
        varRefuseLeft = self.Level_PO.getXpathText("//div[@class='item item4']/div[2]/div/div/div[1]/a/h4")  # 企业首营数
        varRefuseRight = self.Level_PO.getXpathText("//div[@class='item item4']/div[2]/div/div/div[2]/a/h4")  # 品种首营数
        # 我接收的资料
        varMessageMain = self.Level_PO.getXpathText("//div[@class='item item5']/div[1]/div[1]")  # 我接收的资料
        varMessageLeft = self.Level_PO.getXpathText("//div[@class='item item5']/div[2]/div/div/div[1]/a/h4")  # 企业首营数
        varMessageRight = 0
        if var1 != 1 :  # 生产企业没有品种首营
            varMessageRight = self.Level_PO.getXpathText("//div[@class='item item5']/div[2]/div/div/div[2]/a/h4")  # 品种首营数
        if str(varReceiveMain) != "0" :
            print u"我收到的申请 " + str(varReceiveMain) + u" -> 企业首营：" + str(varReceiveleft) + u"，品种首营：" + str(varReceiveRight)
        if str(varSendMain) != "0":
            print u"我发起的申请 " + str(varSendMain) + u" -> 企业首营：" + str(varSendLeft) + u"，品种首营：" + str(varSendRight)
        if str(varSwitchMain) != "0":
            print u"交   换   中 " + str(varSwitchMain) + u" -> 企业首营：" + str(varSwitchLeft) + u"，品种首营：" + str(varSwitchright)
        if str(varRefuseMain) != "0":
            print u"我拒绝的申请 " + str(varRefuseMain) + u" -> 企业首营：" + str(varRefuseLeft) + u"，品种首营：" + str(varRefuseRight)
        if str(varMessageMain) != "0":
            print u"我接收的资料 " + str(varMessageMain) + u" -> 企业首营：" + str(varMessageLeft) + u"，品种首营：" + str(varMessageRight)
    def statistic(self, varPhone):
        # 统计首营
        Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (varPhone))
        varEnterpriseId = Database_PO.cur.fetchone()
        Database_PO.cur.execute('select type from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (varEnterpriseId[0]))
        varEnterpriseType = Database_PO.cur.fetchone()  # 企业类型（1=生产企业，2=经营企业，3...）
        # 首营统计首营方式
        if str(varEnterpriseType[0]) == "1":
            self.statisticsShouying(1)   # 生产企业
        else:
            self.statisticsShouying(0)  # 经营企业
    def trustDeed(self, t):
        self.Level_PO.clickXpath("//input[@ng-click='checkall($event)']", 2)  # 全选 （选择要发送的企业资料）
        # 上传采购或销售委托书
        self.Level_PO.script('document.getElementById("file10").style.display="block"', 2)
        self.Level_PO.sendKeysId_mac("file10", varGif)  # 上传委托书*（已签字盖章的扫描件）
        self.Level_PO.jsRemoveReadonlyId("expire0")
        self.Level_PO.inputXpath("//input[@ng-model='upload.expire']", u"2022-12-12")  # 有效期 *
        self.Level_PO.inputXpath("//input[@ng-model='upload.user_name']", Third_PO.randomUserName())  # 委托人姓名 *
        self.Level_PO.inputXpath("//input[@ng-model='upload.user_id_number']", Third_PO.randomIdCard())  # 委托人身份证 *
        self.Level_PO.script('document.getElementById("file20").style.display="block"', 2)
        self.Level_PO.sendKeysId_mac("file20", varJpg)  # 身份证1
        self.Level_PO.script('document.getElementById("file30").style.display="block"', 2)
        self.Level_PO.sendKeysId_mac("file30", varJpg)  # 身份证2
        self.Level_PO.clickXpath("//button[@ng-click='send()']", 2)  # 提交
        self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
        # # 选择印章
        self.Level_PO.clickXpath("//section[@id='sign']/div/div/div/div/div[1]/a/div/img", 2)  # 行政公章
        self.Level_PO.clickXpathsXpath("//a[@ng-click='sign($index)']", "//button[@ng-click='finish()']", 2)

        # 系统正在处理您的请求，处理结果将以站内信的方式通知给您。
        if self.Level_PO.isElementText("//div[@class='tab-content ng-scope']/div/p", u"系统正在处理您的请求，处理结果将以站内信的方式通知给您。"):
            print u"系统正在处理您的请求，处理结果将以站内信的方式通知给您。"
        sleep(t)

    def shouyingFrom(self, varPhoneFrom, varPhoneTo):
        # 发起首营(发起方)
        self.statistic(varPhoneFrom)  # 发起前统计首营
        print u"-------------------------------操作后-------------------------------"

        # 对方企业名称
        Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (varPhoneTo))
        receiveEnterpriseId = Database_PO.cur.fetchone()
        Database_PO.cur.execute('select name from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (receiveEnterpriseId[0]))
        receiveName = Database_PO.cur.fetchone()

        self.Level_PO.clickLinktext(u"首营管理", 2)
        self.Level_PO.clickLinktext(u"发起首营", 2)
        self.Level_PO.inputName("s", receiveName[0])  # 搜索对方企业
        self.Level_PO.clickXpath("//input[@type='submit']", 2)  # 搜索
        self.Level_PO.clickLinktext(u"发起企业首营", 2)
        self.trustDeed(4)   # 上传采购或销售委托书 + 印章

        self.Level_PO.clickLinktext(u"首页", 2)
        self.statistic(varPhoneFrom)  # 发起后统计首营

    def shouyingTo(self, varPhoneTo, varSwap, varReasion):
        # 对方接收或拒绝
        self.statistic(varPhoneTo)  # 发起前统计首营
        print u"-------------------------------操作后-------------------------------"

        self.Level_PO.clickXpath(u"//ul[@class='sidebar-menu tree']/li[2]/a", 2)  # 首营管理
        self.Level_PO.clickXpath(u"//a[@href='/shouying/web/app.php/shouying/company']", 2)  # 企业首营管理
        list1 = []
        varLink = ""
        list1 = self.Level_PO.getXpathsText("//td")
        for i in range(len(list1)):
            if u"查看企业资料" in list1[i]:
                break
            else:
                varLink = varLink + u"，" + list1[i]
        print varLink.lstrip(u"，")
        varLink = ""

        if varSwap == u"pass":
            self.Level_PO.clickLinktext(u"接受交换", 2)
            self.trustDeed(4)  # 上传采购或销售委托书

            # list2 = []
            # list2 = self.Level_PO.getXpathsText("//td")
            # for i in range(len(list2)):
            #     if list2[i] == u"查看企业资料":
            #         break
            #     else:
            #         varLink = varLink + u"，" + list2[i]
            # print varLink.lstrip(u"，")
        elif varSwap == u"refuse":
            self.Level_PO.clickLinktext(u"拒绝交换", 2)
            self.Level_PO.inputXpath("//textarea[@ng-model='reason']", varReasion)  # 拒绝原因
            self.Level_PO.clickXpath("//button[@ng-click='reject()']", 2)  # 提交
            list2 = self.Level_PO.getXpathsText("//td")
            for i in range(len(list2)):
                if list2[i] == u"查看企业资料":
                    break
                else:
                    varLink = varLink + u"，" + list2[i]
            print u"-------------------------------操作后-------------------------------"
            print varLink.lstrip(u"，")

        self.Level_PO.clickLinktext(u"首页", 2)
        self.statistic(varPhoneTo)  # 发起后统计首营



    def shouyingFromAgain(self, varPhoneFrom):
        # 发起方再次申请首营交换

        self.statistic(varPhoneFrom)    # 发起前统计首营
        print u"-------------------------------操作后-------------------------------"

        self.Level_PO.clickLinktext(u"首营管理", 2)
        self.Level_PO.clickLinktext(u"企业首营管理", 2)
        self.Level_PO.clickLinktext(u"再次申请", 2)
        self.trustDeed(4)  # 上传采购或销售委托书

        self.Level_PO.clickLinktext(u"首页", 2)
        self.statistic(varPhoneFrom)  # 发起后统计首营

        # list1 = []
        # varLink = ""
        # list1 = self.Level_PO.getXpathsText("//td")
        # for i in range(len(list1)):
        #     if list1[i] == u"查看企业资料":
        #         break
        #     else:
        #         varLink = varLink + u"，" + list1[i]
        # print varLink.lstrip(u"，")

    def normalManagerAudit(self, varPhoneFrom, auditStatus):
        # 审核流程（发起方或接受方的普通管理员）
        from selenium.webdriver.common.by import By
        self.statistic(varPhoneFrom)  # 发起前统计首营
        print u"-------------------------------操作后-------------------------------"

        self.Level_PO.clickXpath("//ul[@class='sidebar-menu tree']/li[2]/a", 2)  # 首营管理
        self.Level_PO.clickLinktext(u"企业首营管理", 2)
        self.Level_PO.clickLinktext(u"查看企业资料", 4)
        if auditStatus == "pass":
            self.Level_PO.clickXpathsConfirm("//a[@ng-click='accept(r)']", "//div[@id='confirmDialog']/div/div/div[2]/button[2]", 2)
            self.Level_PO.clickXpath("//button[@ng-click='finish()']", 2)  # 提交下一位审核人
            self.Level_PO.clickXpath("//div[@id='confirmDialog']/div/div/div[2]/button[2]", 2)  # 确认
        elif auditStatus == "refuse":
            # 审核拒绝且确认
            for a in self.Level_PO.find_elements(*(By.XPATH, "//a[@ng-click='showRejectModal(r)']")):
                a.click()
                sleep(2)
                self.Level_PO.inputXpath("//textarea[@ng-model='reason']", u"拒绝理由123")
                self.Level_PO.clickXpath("//button[@ng-click='reject()']", 2)
                sleep(2)
        list1 = []
        varLink = ""
        list1 = self.Level_PO.getXpathsText("//td")
        for i in range(len(list1)):
            if list1[i] == u"查看":
                varLink = varLink + u"，" + list1[i]
                print varLink.lstrip(u"，")
                varLink = ""
            elif list1[i] != u"":
                varLink = varLink + u"，" + list1[i]

        self.Level_PO.clickLinktext(u"首页", 2)
        self.statistic(varPhoneFrom)  # 发起后统计首营

    def shouyingToRetry(self, varPhoneTo):
        # 对方重新签发
        self.statistic(varPhoneTo)  # 重新签发前统计首营
        print u"-------------------------------操作后-------------------------------"

        self.Level_PO.clickXpath("//ul[@class='sidebar-menu tree']/li[2]/a", 2)  # 首营管理
        self.Level_PO.clickLinktext(u"企业首营管理", 2)
        self.Level_PO.clickLinktext(u"查看企业资料", 2)
        self.Level_PO.clickLinktext(u"发出企业资料", 4)
        # 重新签发且确认( 写死循环15次， ?有问题无法遍历)
        for i in range(15):
            if self.Level_PO.isElementXpath("//a[@ng-click='resend(r)']"):
                self.Level_PO.clickXpath("//a[@ng-click='resend(r)']", 2)
                self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)
                # # 选择印章
                self.Level_PO.clickXpath("//section[@id='sign']/div/div/div/div/div[1]/a/div/img", 2)  # 行政公章
                self.Level_PO.clickXpathsXpath("//a[@ng-click='sign($index)']", "//button[@ng-click='finish()']", 6)
                self.Level_PO.clickLinktext(u"企业首营管理", 2)
                self.Level_PO.clickLinktext(u"查看企业资料", 2)
                self.Level_PO.clickLinktext(u"发出企业资料", 2)
            else:
                break

        self.Level_PO.clickLinktext(u"首页", 2)
        self.statistic(varPhoneTo)  # 发起后统计首营

    def enterpriseManagerAudit(self, varPhoneFrom, auditStatus):
        # 审核流程（发起方或接受方的企业管理员）

        self.statistic(varPhoneFrom)  # 发起前统计首营
        print u"-------------------------------操作后-------------------------------"

        self.Level_PO.clickLinktext(u"首营管理", 2)
        self.Level_PO.clickLinktext(u"企业首营管理", 2)
        self.Level_PO.clickId("close-message-box", 2)  # 关闭弹框通知
        self.Level_PO.clickLinktext(u"查看企业资料", 2)
        if auditStatus == u"pass":
            self.Level_PO.clickId("close-message-box", 2)  # 关闭弹框通知
            # 审核通过且确认
            self.Level_PO.clickXpathsConfirm("//a[@ng-click='accept(r)']", "//div[@id='confirmDialog']/div/div/div[2]/button[2]", 2)
            self.Level_PO.clickXpath("//button[@ng-click='finish()']", 2)  # 提交下一位审核人
            self.Level_PO.clickXpath("//div[@id='confirmDialog']/div/div/div[2]/button[2]", 2)  # 确认
        elif auditStatus == u"refuse":
            # 审核拒绝且确认
            for a in self.Level_PO.driver.find_elements_by_xpath("//a[@ng-click='showRejectModal(r)']"):
                a.click()
                sleep(1)
                self.Level_PO.driver.find_element_by_xpath("//textarea[@ng-model='reason']").send_keys("1")
                self.Level_PO.driver.find_element_by_xpath("//button[@ng-click='reject()']").click()
                sleep(1)
        list1 = []
        varLink = ""
        list1 = self.Level_PO.getXpathsText("//td")
        for i in range(len(list1)):
            if list1[i] == u"查看":
                varLink = varLink + u"，" + list1[i]
                print varLink.lstrip(u"，")
                varLink = ""
            elif list1[i] != u"":
                varLink = varLink + u"，" + list1[i]

        self.Level_PO.clickLinktext(u"首页", 2)
        self.statistic(varPhoneFrom)  # 发起后统计首营

    '''8、审核产品'''
    def productApprove(self, varProductName, varStatus):
        # 后台搜索品种名称勾选后通过审核
        self.Level_PO.clickLinktext(u"审核管理", 2)
        self.Level_PO.clickLinktext(u"品种资料审核", 2)
        self.Level_PO.inputId("product_name", varProductName)  # 搜索 品种名称
        self.Level_PO.clickXpath("//button[@type='submit']", 2)  # 搜索
        list0 = []
        x = 0
        list0 = self.Level_PO.getXpathsText("//td")
        for i in range(len(list0)):
            # print list0[i]
            if u"没有数据信息" in list0[i]:
                x = 1
                break
        if x == 1:
            printColor('\033[1;31;47m', 'printRed', u"8、很抱歉，\"" + varProductName + u"\" 不存在或已审核通过。")
            os._exit(0)
            self.Level_PO.close_driver()

        if varStatus == u"pass":  # 批量通过
            '审核通过'
            self.Level_PO.clickXpath("//input[@class='cetc-page-lists-check-all']", 2)  # 全选
            self.Level_PO.clickXpath("//button[@id='batchThrough']", 2)  # 批量确认
            self.Level_PO.clickXpath("//div[@class='cetc-popup']/div[3]/button", 2)  # 二次确认
            self.Level_PO.clickLinktext(u"已通过", 2)
            self.Level_PO.inputId("product_name", varProductName)
            self.Level_PO.clickXpath("//button[@type='submit']", 2)  # 搜索
            list1 = []
            x = 0
            list1 = self.Level_PO.getXpathsText("//td")
            for i in range(len(list1)):
                if list1[i] == varProductName:
                    x = 1
                    break
            if x == 1:
                # 获取此产品添加者手机号
                Database_PO.cur.execute('select enterprise_id from tt_product where name="%s" order by product_id desc limit 1' % (varProductName))
                n0 = Database_PO.cur.fetchone()
                Database_PO.cur.execute('select phone_number from tt_enterprise_user where enterprise_id="%s" order by enterprise_id desc limit 1' % (n0[0]))
                n1 = Database_PO.cur.fetchone()
                varCompanyType = n1[0]
                printColor('\033[1;31;47m', 'printGreen', u"8、恭喜您，\"" + varProductName + u"\" 已审核通过。下一步药检单：python drugList.py " + str(n1[0]) + u" " + str(int(n1[0])+1) + u" " + str(int(n1[0])+2) + u" " + varProductName + u" pass")

        elif varStatus == u"refuse":  # 拒绝   ? 未写完
            '审核拒绝'
            self.Level_PO.clickLinktext(u"拒绝", 2)
            Database_PO.cur.execute('select product_id from tt_product where name="%s" order by product_id desc limit 1' % (varProductName))
            varProductId = Database_PO.cur.fetchone()
            self.Level_PO.inputId("refuse-cause-" + str(varProductId[0]), u"我当时是拒绝的")
            # varRefuseId = self.Level_PO.getXpathAttr("//input[@name='refuse-cause']", u"id")
            # self.Level_PO.inputName("refuse-cause", u"测试，内容不完成所以拒绝!!!")  # 输入拒绝理由
            self.Level_PO.clickXpath("//button[@onclick='approveNoThroughFunction(this," + str(varProductId[0]) + ")']", 2)  # 确认
            # self.Level_PO.clickXpath("//div[@class='cetc-popup-footer']/button", 4)  # 二次确认
            '检查认证状态及拒绝原因'
            self.Level_PO.clickLinktext(u"已拒绝", 2)
            self.Level_PO.inputId("product_name", varProductName)
            self.Level_PO.clickXpath("//button[@type='submit']", 2)  # 搜索
            list1 = []
            x = 0
            list1 = self.Level_PO.getXpathsText("//td")
            for i in range(len(list1)):
                if list1[i] == varProductName:
                    x = 1
                    break
            if x == 1:
                printColor('\033[1;31;47m', 'printGreen', u"8、很抱歉，产品资料（" + varProductName + u"）已拒绝。")

        self.Level_PO.close_driver()

    '''9、药检单4'''
    def noResult(self, varProductName, checkData):
        # 在列表页，对列表内容进行检查，用于搜索关键字后是否有对应的结果。
        x = 0
        list0 = self.Level_PO.getXpathsText("//td")
        for i in range(len(list0)):
            if checkData in list0[i]:
                x = 1
                break
        if x == 1:
            printColor('\033[1;31;47m', 'printRed', u"很抱歉，您搜索的内容（" + varProductName + u"）不存在。\n")
            self.Level_PO.close_driver()
            os._exit(0)
    def isResult(self, varProductName, varPihao):
        # 在列表页，对列表内容进行检查，用于搜索关键字后是否有对应的结果。
        x = 0
        list1 = self.Level_PO.getXpathsText("//td")
        for i in range(len(list1)):
            if list1[i] == varProductName or list1[i] == varPihao:
                x = x + 1
        if x == 2:
            printColor('\033[1;31;47m', 'printGreen', u"恭喜您，已完成。\n")
        else:
            printColor('\033[1;31;47m', 'printRed', u"很抱歉，您搜索的内容（" + varProductName + u"）不存在。")
            self.Level_PO.close_driver()
            os._exit(0)
    def drugList_addDrug(self, varProductName, varPihao):
        # 药检单管理， 生产企业新建药检单并发送给下游企业
        Database_PO.cur.execute('select classify from tt_product where name="%s" order by product_id desc limit 1' % (varProductName))
        t2 = Database_PO.cur.fetchone()
        varClassify = t2[0]
        if varClassify != 1 :
            printColor('\033[1;31;47m', 'printRed', u"9、很抱歉，当前产品（" + varProductName+ u"）不是药品，只有药品产品才能新建药检单。")
            self.Level_PO.close_driver()
            os._exit(0)
        self.Level_PO.clickLinktext(u"药检单管理", 2)
        self.Level_PO.clickLinktext(u"新建药检单", 2)
        self.Level_PO.inputName("name", varProductName)  # 搜索品种名称
        self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
        self.noResult(varProductName, u"没有数据信息")
        Database_PO.cur.execute('select product_id from tt_product where name="%s" order by product_id desc limit 1' % (varProductName))
        tblProductId = Database_PO.cur.fetchone()
        self.Level_PO.clickXpath("//a[@href='/shouying/web/app.php/drug-check/new?productId=" + str(tblProductId[0]) + "']", 2)  # 新建药检单
        self.Level_PO.inputName("produce_batch_no", varPihao)  # 生产批号 *
        self.Level_PO.jsRemoveReadonlyName("valid_date")  # 有效期至
        self.Level_PO.inputXpath("//input[@name='valid_date']", u"2038-11-11")  # 有效期至
        self.Level_PO.inputXpath("//input[@name='file']",varJpg)  # 上传文件
        self.Level_PO.clickXpath("//input[@onclick='submitForm();']", 2)  # 提交
        # 检查记录是否存在，药检单列表
        self.Level_PO.inputName("name", varProductName)  # 品种名称
        self.Level_PO.inputName("produce_batch_no", varPihao)  # 生产批号
        self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
        self.isResult(varProductName, varPihao)  # 检查是否有结果


    def drugList_sendDrug(self, varPhoneTo, varProductName, varPihao):
        # 药检单管理 ， 上游企业给下游企业发送药检单
        self.Level_PO.clickLinktext(u"药检单列表", 2)
        self.Level_PO.inputName("name", varProductName)  # 品种名称
        self.Level_PO.inputName("produce_batch_no", varPihao)  # 生产批号
        self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
        self.Level_PO.clickLinktext(u"发送药检单", 2)
        Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (varPhoneTo))
        t0 = Database_PO.cur.fetchone()
        Database_PO.cur.execute('select name from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (t0[0]))
        t1 = Database_PO.cur.fetchone()
        tblCompanyName = t1[0]
        self.Level_PO.inIframe("iframe-drugCheck-send", 2)
        self.Level_PO.inputName("name", tblCompanyName)  # 检索企业名称
        self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
        self.Level_PO.clickId("checkAll", 2)  # 全选
        self.Level_PO.clickXpath("//button[@onclick='selectEnterprise();']", 2)  # 确定
        self.Level_PO.outIframe(2)
        # 检查记录是否存在，我发出的药检单 - 待签收药检单
        self.Level_PO.inputName("name", varProductName)  # 品种名称
        self.Level_PO.inputName("produce_batch_no", varPihao)  # 生产批号
        self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
        self.isResult(varProductName, varPihao)  # 检查是否有结果
    def drugList_receiveDrug(self, varProductName, varPihao, operation):
        # 药检单管理 ， 下游企业接收上游企业发来的药检单
        self.Level_PO.clickLinktext(u"药检单管理", 2)
        self.Level_PO.clickLinktext(u"我收到的药检单", 2)
        self.Level_PO.inputName("name", varProductName)  # 产品名称
        self.Level_PO.inputName("produce_batch_no", varPihao)  # 生产批号
        self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
        if operation == "pass" :
            # 接收
            self.Level_PO.clickLinktext(u"接收", 2)
            self.Level_PO.clickXpath("//button[@onclick='accept();']", 6)  # 确定
            # 检查记录是否在指定标签列显示
            self.Level_PO.clickLinktext(u"已签收药检单", 2)
            self.Level_PO.clickXpath("//a[@href='?tab=2']", 2)  # u"已签收药检单"
            self.Level_PO.inputName("name", varProductName)  # 产品名称
            self.Level_PO.inputName("produce_batch_no", varPihao)  # 生产批号
            self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
            self.isResult(varProductName, varPihao)  # 检查是否有结果
        else:
            self.Level_PO.clickLinktext(u"拒绝", 2)
            self.Level_PO.inputXpath("//textarea[@id='refuseCause']", u"拒绝内容213")  # 拒绝原因
            self.Level_PO.clickXpath("//button[@onclick='reject();']", 6)  # 确定
            # 检查记录是否在指定标签列显示
            self.Level_PO.clickLinktext(u"已拒绝药检单", 2)
            self.Level_PO.clickXpath("//a[@href='?tab=3']", 2)  # u"已拒绝药检单"
            self.Level_PO.inputName("name", varProductName)  # 产品名称
            self.Level_PO.inputName("produce_batch_no", varPihao)  # 生产批号
            self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
            self.isResult(varProductName, varPihao)  # 检查是否有结果


    '''10、发起品种首营3'''
    def productFrom(self, varPhoneFrom, varCompanyTo, varProductName):
        # 品种首营资料发起方

        self.statistic(varPhoneFrom)  # 发起前统计首营
        print u"-------------------------------操作后-------------------------------"

        self.Level_PO.clickLinktext(u"首营管理", 2)
        self.Level_PO.clickLinktext(u"发起首营", 2)
        self.Level_PO.inputName("s", varCompanyTo)  # 搜索对方企业
        self.Level_PO.clickXpath("//input[@type='submit']", 2)  # 搜索
        self.Level_PO.clickLinktext(u"发起品种首营", 2)
        self.Level_PO.inputXpath("//input[@ng-model='query.name']", unicode(varProductName, "gbk"))  # 搜索品种名称
        self.Level_PO.clickXpath("//button[@ng-click='search(1)']", 2)  # 搜索
        self.Level_PO.clickXpath("//input[@ng-click='checkall($event)']", 2)  # 全选
        self.Level_PO.clickXpath("//button[@ng-click='start()']", 2)  # 批量发起
        self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 提交
        self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 二次确认
        self.Level_PO.clickLinktext(u"发出的品种", 2)
        self.Level_PO.inputXpath("//input[@ng-model='query.name']", unicode(varProductName, "gbk"))  # 搜索品种名称
        self.Level_PO.clickXpath("//button[@ng-click='search(1)']", 2)  # 搜索
        self.Level_PO.clickLinktext(u"签发", 2)
        # # 选择印章
        self.Level_PO.clickXpath("//section[@id='sign']/div/div/div/div/div[1]/a/div/img", 2)  # 行政公章
        self.Level_PO.clickXpathsXpath("//a[@ng-click='sign($index)']", "//button[@ng-click='finish()']", 6)

        self.Level_PO.clickLinktext(u"首页", 2)
        self.statistic(varPhoneFrom)  # 发起后统计首营
    def productToAudit(self, varManagerTo, varProductName, varSwap):
        # 接收方审核（按照审核流程设置）

        self.statistic(varManagerTo)  # 发起前统计首营
        print u"-------------------------------操作后-------------------------------"

        self.Level_PO.clickXpath("//ul[@class='sidebar-menu tree']/li[2]/a", 2)  # 首营管理
        self.Level_PO.clickXpath("//ul[@class='sidebar-menu tree']/li[2]/ul/li[3]/a", 2)  # 品种首营管理
        self.Level_PO.clickXpath("//section[@id='medicine_page']/div/ul/li[4]/a", 2)  # 收到的品种
        self.Level_PO.inputXpath("//input[@ng-model='query.name']", varProductName)  # 搜索品种名称
        self.Level_PO.clickXpath("//button[@ng-click='search(1)']", 2)  # 搜索
        self.Level_PO.clickXpath("//input[@ng-click='checkAll($event)']", 2)  # 全选

        if varSwap == u"全选且批量同意":
            self.Level_PO.clickXpath("//button[@ng-click='batchAccept()']", 2)  # 批量同意
            self.Level_PO.clickXpath("//div[@id='confirmDialog']/div/div/div[2]/button[2]", 2)  # 确认
        elif varSwap == u"全选且批量拒绝":
            self.Level_PO.clickXpath("//button[@ng-click='batchReject()']", 2)  # 批量拒绝
            self.Level_PO.inputXpath("//textarea[@ng-model='reason']", "666")  # 拒绝原因
            self.Level_PO.clickXpath("//button[@ng-click='reject()']", 2)  # 提交
        elif varSwap == u"pass":
            # 通过且确认
            self.Level_PO.clickXpathsConfirm("//a[@ng-click='accept(item)']", "//div[@id='confirmDialog']/div/div/div[2]/button[2]", 2)
            varLink = ""
            list1 = self.Level_PO.getXpathsText("//td")
            for i in range(len(list1)):
                if list1[i] == u"查看":
                    break
                else:
                    varLink = varLink + u", " + list1[i]
            print varLink.lstrip(" ,")
            if u"已接收" in varLink:
                printColor('\033[1;31;47m', 'printGreen', u"恭喜您，已接收品种首营交换。")
        elif varSwap == u"refuse":
            # 拒绝且确认
            for a in self.Level_PO.driver.find_elements_by_xpath("//button[@ng-click='showRejectModal(item)']"):
                a.click()
                sleep(2)
                self.Level_PO.inputXpath("//textarea[@ng-model='reason']", "1")
                self.Level_PO.clickXpath("//button[@ng-click='reject()']", 2)
                sleep(2)
            varLink = ""
            list1 = self.Level_PO.getXpathsText("//td")
            for i in range(len(list1)):
                if list1[i] == u"查看":
                    break
                else:
                    varLink = varLink + u", " + list1[i]
            print varLink.lstrip(" ,")
            if u"已拒绝" in varLink:
                printColor('\033[1;31;47m', 'printGreen', u"恭喜您，已拒绝品种首营交换。")

        self.Level_PO.clickLinktext(u"首页", 2)
        self.statistic(varManagerTo)  # 发起后统计首营
    def productFromAgain(self):
        # 发起者再次发起
        self.Level_PO.clickLinktext(u"首营管理", 2)
        self.Level_PO.clickLinktext(u"品种首营管理", 2)
        self.Level_PO.clickLinktext(u"发出的品种", 2)
        self.Level_PO.clickLinktext(u"签发", 2)
        # self.Level_PO.clickXpath("//button[@ng-click='submit()']", 2)  # 提交
        # self.Level_PO.clickXpath("//div[@id='alertDialog']/div/div/div[2]/button", 2)  # 确认
        # # 选择印章
        self.Level_PO.clickXpath("//section[@id='sign']/div/div/div/div/div[1]/a/div/img", 2)  # 行政公章
        self.Level_PO.clickXpathsXpath("//a[@ng-click='sign($index)']", "//button[@ng-click='finish()']", 6)

    '''11、特药出入库'''
    def newStockOut(self, dimProductName, dimPihao, dimQuantity, dimStockOutDate, dimJpg, dimOperateCompany):
        # 新建出库单（搜索品种，新建出库单，验证出库单状态）
        Database_PO.cur.execute('select product_id from tt_product where name="%s" order by product_id desc limit 1' % (dimProductName))
        t1 = Database_PO.cur.fetchone()
        varProductId = t1[0]  # 产品id
        # 搜索品种
        self.Level_PO.inputXpath("//input[@name='name']", dimProductName)  # 品种名称
        self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
        # 新建出库单
        self.Level_PO.clickXpath("//a[@href='/shouying/web/app.php/outStorage/createView?productId=" + str(varProductId) + "']", 2)  # 点击 新建出库单
        self.Level_PO.inputXpath("//input[@name='produceBatchNo']", dimPihao)  # 生产批号 *
        self.Level_PO.inputXpath("//input[@name='amount']", dimQuantity)  # 数量 *
        self.Level_PO.inputXpath("//input[@name='checkoutDate']", str(dimStockOutDate))  # 出库日期 *
        self.Level_PO.inputXpath("//input[@name='file']", dimJpg)  # 上传出库单图片 *
        self.Level_PO.clickLinktext(u"提交", 2)
        # 选择发送目标
        self.Level_PO.inIframe("iframe-choice-enterprise", 2)
        self.Level_PO.inputName("enterpriseName", dimOperateCompany)  # 搜索企业名称（下游企业）
        self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
        self.Level_PO.clickXpath("//input[@name='enterpriseId']", 2)  # 勾选 交换公司
        self.Level_PO.clickXpath("//a[@onclick='choiceEnterprise(this)']", 2)  # 提交
        self.Level_PO.outIframe(2)
        # 我发出的出库单，验证出库单状态为“待接收”
        self.Level_PO.inputXpath("//input[@name='outStorageDate']", str(dimStockOutDate))  # 出库时间
        self.Level_PO.inputXpath("//input[@name='productName']", dimProductName)  # 药品名称
        self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
        list1 = []
        varLink = ""
        list1 = self.Level_PO.getXpathsText("//td")
        for i in range(len(list1)):
            if u"查看" in list1[i]:
                break
            else:
                varLink = varLink + u"，" + list1[i]
        if u"待接收" in varLink:
            print varLink.lstrip(u"，")
        else:
            self.Level_PO.printColor('\033[1;31;47m', 'printRed', u"我发出的出库单，出库单中对方处理状态有误，应该是‘待接收’。")
        varLink = ""

    def StockIn(self, dimProductName, dimStockOutDate, dimPihao, dimStockInDate, dimJpg):
        # 我收到的出库申请（搜索状态，全部入库，搜索状态）
        # 搜索
        self.Level_PO.inputXpath("//input[@name='outStorageDate']", dimStockOutDate)  # 出库时间
        self.Level_PO.inputXpath("//input[@name='productName']", dimProductName)  # 药品名称
        self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
        list1 = []
        varLink = ""
        list1 = self.Level_PO.getXpathsText("//td")
        for i in range(len(list1)):
            if u"查看" in list1[i]:
                break
            else:
                varLink = varLink + u"，" + list1[i]
        if u"待接收" in varLink:
            print varLink.lstrip(u"，")
        else:
            self.Level_PO.printColor('\033[1;31;47m', 'printRed', u"出库单对方处理状态有误，应该是‘待接收’。")
        varLink = ""
        self.Level_PO.clickLinktext(u"查看", 2)
        # 全部入库并发送回执
        self.Level_PO.clickLinktext(u"全部入库并发送回执", 2)
        self.Level_PO.inputName("produceBatchNo", dimPihao)  # 生产批号 *
        self.Level_PO.inputXpath("//input[@name='checkoutDate']", dimStockInDate)  # 入库日期
        self.Level_PO.inputXpath("//input[@name='file']", dimJpg)  # 上传入库单
        self.Level_PO.inputXpath("//input[@name='returnFile']", dimJpg)  # 上传入库回执
        self.Level_PO.clickXpath("//a[@onclick='submitForm()']", 2)  # 提交
        # 搜索，检查出库后记录的状态，应为“已接受”
        self.Level_PO.clickLinktext(u"我收到的出库申请", 2)
        self.Level_PO.inputXpath("//input[@name='outStorageDate']", dimStockOutDate)  # 出库时间
        self.Level_PO.inputXpath("//input[@name='productName']", dimProductName)  # 搜索产品名
        self.Level_PO.clickXpath("//button[@id='btnQuery']", 2)  # 搜索
        list1 = []
        varLink = ""
        list1 = self.Level_PO.getXpathsText("//td")
        for i in range(len(list1)):
            if u"查看" in list1[i]:
                break
            else:
                varLink = varLink + u"，" + list1[i]
        if u"已接受" in varLink:
            print varLink.lstrip(u"，")
        else:
            self.Level_PO.printColor('\033[1;31;47m', 'printRed', u"出库单对方处理状态有误，应该是‘已接受’。")
        varLink = ""


    def editAccountInfo(self, varPhone, varMail, isSMSNotice, isEmailNotice):
        '''账户管理 - 账户信息'''
        # # 修改手机号
        self.Level_PO.clickXpath(u"//a[@data-target='#popup-edit-phoneNumber']", 2)  # 点击修改
        self.Level_PO.inputId("phoneNumber", varPhone)
        self.Level_PO.clickXpath("//input[@onclick='sendSms();']", 2)
        varCaptcha = connRedis.get('sms_' + varPhone)
        self.Level_PO.inputName("validateCode",  varCaptcha.split('code":"')[1].split('"')[0])
        self.Level_PO.clickXpath("//button[@onclick='doConfirmPhoneNumber();']", 2)
        # # 修改企业邮箱
        self.Level_PO.clickXpath(u"//a[@data-target='#popup-edit-email']", 2)  # 点击修改
        self.Level_PO.inputId("email", varMail)
        self.Level_PO.clickXpath("//button[@onclick='doConfirmEmail();']", 4)
        self.Level_PO.clickXpath("//div[@id='hind-modal']/div/div/div[2]/div[2]/button", 2)

        # 通用设置
        # 是否开启短信实时通知：
        if isSMSNotice == "on":
            self.Level_PO.clickXpath("//input[@id='openSms']", 2)  # 打开
        else:
            self.Level_PO.clickXpath("//input[@id='closeSms']", 2)  # 关闭
        # 是否开启邮件实时通知：
        if isEmailNotice == "on":
            self.Level_PO.clickXpath("//input[@id='openEmail']", 2)  # 打开
        else:
            self.Level_PO.clickXpath("//input[@id='closeEmail']", 2)  # 关闭
        # 保存设置
        self.Level_PO.clickXpath("//input[@onclick='saveConfig();']", 2)
        self.Level_PO.clickXpath("//div[@id='hind-modal']/div/div/div[2]/div[2]/button", 2)

    def addSealManage(self, varAdministrativeOfficialSeal, varQualityManagementDepartmentSeal):
        '''账户管理 - 证书管理 - 印章管理'''
        # 提交印章
        self.Level_PO.inputName("administrativeOfficialSeal", varAdministrativeOfficialSeal)  # 行政公章
        self.Level_PO.inputName("qualityManagementDepartmentSeal", varQualityManagementDepartmentSeal)  # 质量管理部门印章
        self.Level_PO.clickXpath("//input[@onclick='doSubmit()']", 2)  # 提交
        self.Level_PO.clickXpath("//div[@id='hind-modal']/div/div/div[2]/div[2]/button", 2)  # 确定

    def signRecord(self, varSdate, varEdate, varOperate):
        '''账户管理 - 证书管理 - 签署记录'''
        # 查询签署记录 ，默认全部时间
        self.Level_PO.inputId("form_sdate", varSdate)  # 开始时间
        self.Level_PO.inputId("form_edate", varEdate)  # 结束时间
        self.Level_PO.selectNameText("userId", varOperate)  # 操作人
        self.Level_PO.clickLinktext(u"搜索", 2)

    def editManager(self, varName, varPhone, varMail, varIdCard, varResetPass):
        ''' 账户管理 - 账户管理 - 管理员列表 '''
        # 修改 企业管理员信息及密码
        self.Level_PO.clickLinktext("修改", 2)
        self.Level_PO.inputIdClear("edit_name", varName)  # 随机管理员姓名
        self.Level_PO.inputIdClear("edit_phoneNumber", varPhone)  # 随机生成11位数字
        self.Level_PO.inputIdClear("edit_email", varMail)   # 随机生成邮箱
        self.Level_PO.inputIdClear("edit_idCard", varIdCard)  # 随机身份证
        self.Level_PO.clickXpath("//button[@onclick='doEdit();']", 2)  # 提交
        self.Level_PO.clickXpath("//button[@onclick='closeHindModal();']", 2)  # 确定
        self.Level_PO.clickLinktext("重置密码", 2)
        self.Level_PO.inputIdClear("reset_password", varResetPass)  # 重置密码
        self.Level_PO.clickXpath("//button[@onclick='doEditPwd();']", 2)  # 提交
        self.Level_PO.clickXpath("//button[@onclick='closeHindModal();']", 2)  # 确定

    def addManager(self, varName, varPhone, varMail, varIdCard, varPass):
        ''' 账户管理 - 账户管理 - 管理员列表 - 新增'''
        # 新增 管理员
        self.Level_PO.inputId("add_name", varName)  # 随机管理员姓名
        self.Level_PO.inputId("add_phoneNumber", varPhone)  # 随机生成11位数字
        self.Level_PO.inputId("add_email", varMail)   # 随机生成邮箱
        self.Level_PO.inputId("add_idCard", varIdCard)  # 随机身份证
        self.Level_PO.inputId("add_password", varPass)   # 登录密码
        self.Level_PO.clickXpath("//button[@onclick='doCreate();']", 2)  # 提交
        self.Level_PO.clickXpath("//button[@onclick='closeHindModal();']", 2)  # 确定

    def operateRecord(self, varSdate, varEdate, varOperate):
        '''账户管理 - 操作记录'''
        # 查询操作记录 , 默认全部时间
        self.Level_PO.inputId("form_sdate", varSdate)  # 开始时间
        self.Level_PO.inputId("form_edate", varEdate)  # 结束时间
        self.Level_PO.inputXpath("//input[@type='text']", varOperate, 2)  # 操作人
        self.Level_PO.clickXpath("//input[@type='submit']", 2)  # 搜索

    def productList(self, varName, varCode, varFactory, varClassify):
        ''' 产品管理 - 产品列表'''
        # 查询产品
        self.Level_PO.inputName("name", varName)  # 产品名称
        self.Level_PO.inputName("authentication_code", varCode)  # 批准文号
        self.Level_PO.inputName("factory_name", varFactory)  # 生产企业
        self.Level_PO.selectNameText("classify", varClassify)  # 产品类别
        self.Level_PO.clickId("btnQuery", 2)  # 搜索

    def noCertificationProduct(self, varName, varCode, varClassify):
        ''' 产品管理 - 待认证产品'''
        # 查询待认证产品
        self.Level_PO.inputName("name", varName)  # 产品名称
        self.Level_PO.inputName("authentication_code", varCode)  # 批准文号
        self.Level_PO.selectNameText("classify", varClassify)  # 产品类别
        self.Level_PO.clickId("btnQuery", 2)  # 搜索

    def createProductInfo(self, varType, varName, varSpec, varAuthenticationCode, varAuthenticationCodePic, varAcValidDate, varFactory, varInternalCode, varForm, varQualityStandard, varRegistration, varAcValidDate2, varInspectionReport, varRecord, varPackageLabelInstruction, varInstruction):

        '''新建产品资料'''
        self.Level_PO.selectNameText("classify", varType)  # 产品类别 *
        self.Level_PO.inputId("name", varName)  # 产品（品种）名称 *
        self.Level_PO.inputId("spec", varSpec)  # 规格 *
        self.Level_PO.inputId("authenticationCode", varAuthenticationCode)  # 药品生产批件、药品注册证 *
        self.Level_PO.inputName("factory_name", varFactory)  # 生产企业 *
        if varType == u"药品" :
            self.Level_PO.inputXpath("//input[@desc='registration']", varRegistration)  # 药品生产批件、药品注册证（图）
            self.Level_PO.jsRemoveReadonlyId("registration_validEnd")  # 证件有效期
            self.Level_PO.inputXpath("//input[@id='registration_validEnd']", varAcValidDate)  # 证件有效期
            self.Level_PO.inputName("internal_code", varInternalCode)  # 企业内部编码
            self.Level_PO.inputId("form", varForm)  # 剂型
            self.Level_PO.inputXpath("//input[@desc='qualityStandard']", varQualityStandard)  # 药品质量标准:
            self.Level_PO.inputXpath("//input[@desc='inspectionReport']", varInspectionReport)  # 药品检验报告书（省检或厂检）
            self.Level_PO.inputXpath("//input[@desc='record']", varRecord)  # 药品包装盒、说明书备案:
            self.Level_PO.inputXpath("//input[@desc='packageLabelInstruction']", varPackageLabelInstruction)  # 药品包装、标签、说明书实样和变更包装、标签、说明书材料
            self.Level_PO.inputXpath("//input[@desc='instruction']", varInstruction)  # 产品说明书
        elif varType == u"中药饮片" :
            self.Level_PO.inputXpath("//input[@desc='registration']", varRegistration)  # 药品生产批件、药品注册证(图)
            self.Level_PO.jsRemoveReadonlyId("registration_validEnd")  # 证件有效期
            self.Level_PO.inputXpath("//input[@id='registration_validEnd']", varAcValidDate2)  # 证件有效期
            self.Level_PO.inputName("production_place", u"上海")  # 产地 *
            self.Level_PO.inputName("internal_code", varInternalCode)  # 企业内部编码
            self.Level_PO.inputName("form", varForm)  # 剂型
            self.Level_PO.inputXpath("//input[@desc='qualityStandard']", varQualityStandard)  # 药品质量标准:
        elif varType == u"化妆品":
            self.Level_PO.inputXpath("//input[@desc='authenticationCode']", varAuthenticationCodePic)  # 批准文号(图)
            self.Level_PO.jsRemoveReadonlyId("acValidDate")  # 证件有效期
            self.Level_PO.inputXpath("//input[@id='acValidDate']", varAcValidDate)  # 证件有效期
            self.Level_PO.inputName("internal_code", varInternalCode)  # 企业内部编码
            self.Level_PO.inputXpath("//input[@desc='cosmeticsBackup']", varInspectionReport)  # 化妆品网上备案打印件
            self.Level_PO.inputXpath("//input[@desc='executeStandard']", varInspectionReport)  # 执行标准
            self.Level_PO.inputXpath("//input[@desc='thirdRartyDetectReport']", varRecord)  # 第三方检测报告
            self.Level_PO.inputXpath("//input[@desc='packBoxManual']", varPackageLabelInstruction)  # 包装盒说明书实物或复印件
            self.Level_PO.inputXpath("//input[@desc='instruction']", varInstruction)  # 产品说明书
        elif varType == u"食品":
            self.Level_PO.inputXpath("//input[@desc='authenticationCode']", varAuthenticationCodePic)  # 批准文号(图)
            self.Level_PO.jsRemoveReadonlyId("acValidDate")  # 证件有效期
            self.Level_PO.inputXpath("//input[@id='acValidDate']", varAcValidDate)  # 证件有效期
            self.Level_PO.inputName("internal_code", varInternalCode)  # 企业内部编码
            self.Level_PO.inputXpath("//input[@desc='executeStandard']", varInspectionReport)  # 执行标准
            self.Level_PO.inputXpath("//input[@desc='detectReport']", varInspectionReport)  # 疾控中心检测报告：必填
            self.Level_PO.inputXpath("//input[@desc='productLicense']", varRecord)  # 生产许可证 （QS或SC证书）
            self.Level_PO.inputXpath("//input[@desc='packBoxManual']", varPackageLabelInstruction)  # 包装盒说明书实物或复印件
            self.Level_PO.inputXpath("//input[@desc='instruction']", varInstruction)  # 产品说明书
        elif varType == u"日用品":
            self.Level_PO.inputXpath("//input[@desc='authenticationCode']", varAuthenticationCodePic)  # 批准文号(图)
            self.Level_PO.jsRemoveReadonlyId("acValidDate")  # 证件有效期
            self.Level_PO.inputXpath("//input[@id='acValidDate']", varAcValidDate)  # 证件有效期
            self.Level_PO.inputName("internal_code", varInternalCode)  # 企业内部编码
            self.Level_PO.inputXpath("//input[@desc='executeStandard']", varInspectionReport)  # 执行标准
            self.Level_PO.inputXpath("//input[@desc='thirdRartyDetectReport']", varRecord)  # 第三方检测报告
            self.Level_PO.inputXpath("//input[@desc='packBoxManual']", varPackageLabelInstruction)  # 包装盒说明书实物或复印件
            self.Level_PO.inputXpath("//input[@desc='instruction']", varInstruction)  # 产品说明书
        elif varType == u"消毒产品":
            self.Level_PO.inputXpath("//input[@desc='authenticationCode']", varAuthenticationCodePic)  # 批准文号(图)
            self.Level_PO.jsRemoveReadonlyId("acValidDate")  # 证件有效期
            self.Level_PO.inputXpath("//input[@id='acValidDate']", varAcValidDate)  # 证件有效期
            self.Level_PO.inputName("internal_code", varInternalCode)  # 企业内部编码
            self.Level_PO.inputXpath("//input[@desc='healthSafetyAssessmentReport']", varInspectionReport)  # 卫生安全评价报告
            self.Level_PO.inputXpath("//input[@desc='recordCertificate']", varInspectionReport)  # 备案凭证
            self.Level_PO.inputXpath("//input[@desc='executeStandard']", varInspectionReport)  # 执行标准
            self.Level_PO.inputXpath("//input[@desc='disinfectProductEquatur']", varInspectionReport)  # 消毒产品卫生许可证书
            self.Level_PO.inputXpath("//input[@desc='thirdRartyDetectReport']", varRecord)  # 第三方检测报告
            self.Level_PO.inputXpath("//input[@desc='packBoxManual']", varPackageLabelInstruction)  # 包装盒说明书实物或复印件
            self.Level_PO.inputXpath("//input[@desc='instruction']", varInstruction)  # 产品说明书
        elif varType == u"保健食品":
            self.Level_PO.inputXpath("//input[@desc='authenticationCode']", varAuthenticationCodePic)  # 批准文号(图)
            self.Level_PO.jsRemoveReadonlyId("acValidDate")  # 证件有效期
            self.Level_PO.inputXpath("//input[@id='acValidDate']", varAcValidDate)  # 证件有效期
            self.Level_PO.inputName("internal_code", varInternalCode)  # 企业内部编码
            self.Level_PO.inputXpath("//input[@desc='healthFoodApprovalCertificate']", varInspectionReport)  # 保健食品批准证书
            self.Level_PO.inputXpath("//input[@desc='packBoxManual']", varPackageLabelInstruction)  # 包装盒说明书实物或复印件
            self.Level_PO.inputXpath("//input[@desc='instruction']", varInstruction)  # 产品说明书
        elif varType == u"医疗器械":
            self.Level_PO.inputXpath("//input[@desc='authenticationCode']", varAuthenticationCodePic)  # 批准文号(图)
            self.Level_PO.jsRemoveReadonlyId("acValidDate")  # 证件有效期
            self.Level_PO.inputXpath("//input[@id='acValidDate']", varAcValidDate)  # 证件有效期
            self.Level_PO.inputName("internal_code", varInternalCode)  # 企业内部编码
            self.Level_PO.inputXpath("//input[@desc='executeStandard']", varInspectionReport)  # 执行标准
            self.Level_PO.inputXpath("//input[@desc='factoryInspection']", varInspectionReport)  # 医疗器械质量检验监督中心检验报告或一类厂检 *
            # 器械类别 *  (# 一类器械 or 二类、三类器械 任选其一)
            # self.Level_PO.selectNameText("instrumentType", u"一类器械")

            # 一类器械证书 * （1医疗器械注册证和医疗器械注册登记表 or 2第一类医疗器械备案凭证和第一类医疗器械备案信息表 任选其一）
            # self.Level_PO.clickId("aClassInstrumentCert1", 2)  # 1医疗器械注册证和医疗器械注册登记表
            # self.Level_PO.inputXpath("//input[@desc='firstKindMedicalApparatusCert']", varInspectionReport)  # 第一类医疗器械备案凭证
            # self.Level_PO.inputXpath("//input[@desc='recordInfoTable']", varInspectionReport)  # 第一类医疗器械备案信息表
            # or
            # self.Level_PO.clickId("aClassInstrumentCert2", 2)  # 2第一类医疗器械备案凭证和第一类医疗器械备案信息表
            # self.Level_PO.inputXpath("//input[@desc='medicalDeviceRegistration']", varInspectionReport)  # 医疗器械注册证:
            # self.Level_PO.inputXpath("//input[@desc='medicalDeviceRegistrationTable']", varInspectionReport)  # 医疗器械注册登记表:

            # =================================================================

            self.Level_PO.selectNameText("instrumentType", u"二类、三类器械")
            # 二类、三类器械证书 * （1医疗器械注册证和医疗器械注册登记表 or 2中华人民共和国医疗器械注册证  任选其一）
            self.Level_PO.clickId("twoOrThreeClassInstrumentCert1", 2)  # 1医疗器械注册证和医疗器械注册登记表（默认）
            self.Level_PO.inputXpath("//input[@desc='medicalDeviceRegistration2']", varInspectionReport)  # 医疗器械注册证:
            self.Level_PO.inputXpath("//input[@desc='medicalDeviceRegistrationTable2']", varInspectionReport)  # 医疗器械注册登记表:

            # self.Level_PO.clickId("twoOrThreeClassInstrumentCert2", 2)  # 中华人民共和国医疗器械注册证
            # self.Level_PO.inputXpath("//input[@desc='prcMedicalDeviceRegistration']", varInspectionReport)  # 中华人民共和国医疗器械注册证:

        self.Level_PO.clickXpath("//input[@onclick='doSubmit();']", 2)  # 提交
        self.Level_PO.clickXpath("//div[@id='hind-modal']/div/div/div[2]/div[2]/button", 2)  # 确定

    def enterpriseShouying(self, varName):
        '''首营管理 - 发起首营'''
        # 搜索企业，发起企业首营
        self.Level_PO.inputName("s", varName)  # 企业名称
        self.Level_PO.clickXpath("//input[@type='submit']", 2)  # 搜索
        self.Level_PO.clickXpath("//a[@href='/shouying/web/app.php/shouying/company/start?id=2']", 2)  # 发起企业首营

    def seeEnterpriseInfo(self, varName):
        '''首营管理 - 发起首营'''
        # 搜索企业，查看企业资料
        self.Level_PO.inputName("s", varName)  # 企业名称
        self.Level_PO.clickXpath("//input[@type='submit']", 2)  # 搜索
        self.Level_PO.clickXpath("//a[@href='/shouying/web/app.php/shouying/company/view?id=2']", 2)  # 查看企业资料

    def enterpriseShouyingManage(self):
        '''首营管理 - 企业首营管理'''
        pass

    def inbox(self):
        ''' 站内信 - 收件箱'''
        pass

    def outbox(self):
        '''站内信 - 发件箱'''
        pass

    def sendInstation(self, varTitle, varName, varContent):
        '''站内信 - 发送站内信'''
        self.Level_PO.inputId("title", varTitle)  # 标题
        self.Level_PO.clickId("receivers-hint", 2)  # 点击收件人
        self.Level_PO.inputId("enterprise-name", varName)  # 企业名称
        self.Level_PO.clickId("search-friends", 2)  # 搜索
        self.Level_PO.inputXpath("//input[@data-value='上海本草堂123']", 2)  # 勾选交换公司
        self.Level_PO.clickId("btn-choose-friends", 2)  # 点击确定
        self.Level_PO.inputId("um-editor", varContent)  # 正文
        self.Level_PO.clickXpath("//input[@name='email']", 2)  # 勾选邮件通知
        self.Level_PO.clickXpath("//input[@name='sms']", 2)  # 勾选短信通知（请勿过于频繁使用通知功能）

    def houtaiLogin(self, varUser, varPass):
        '''登录'''
        self.Level_PO.inputName("_username", varUser)
        self.Level_PO.inputName("_password", varPass)
        # 获取验证码,万能码：000000
        self.Level_PO.inputId("_captcha", "000000")
        self.Level_PO.clickXpath(u"//button[@type='submit']", 2)



