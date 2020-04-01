# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2018-3-15
# Description: 电科智药，审方处方web，PrescriptionPO 对象库
#***************************************************************

from Public.PageObject.DatabasePO import *
Database_PO = DatabasePO('10.111.3.4', 3306, 'cetc', '20121221', 'cetchis')

class PrescriptionPO(object):

    def __init__(self, Level_PO):
        self.Level_PO = Level_PO

    def login(self, varUser, varPass):
        '''login'''
        self.Level_PO.inputId(u"loginName", varUser)
        self.Level_PO.inputId(u"password", varPass)
        self.Level_PO.clickXpath(u"//button[@onclick='doLogin()']", 2)

    def diagnosis(self):
        '''医生 日常接诊'''
        pass

    def prescriptionStatistic(self):
        '''医生 处方统计'''
        pass

    def historyPrescription(self):
        '''医生 历史处方'''
        pass

    def drugServer(self):
        '''药师 药事服务'''
        self.Level_PO.inIframe("myFrame", 2)
        varStatus = self.Level_PO.getXpathText("//div[@id='no-patient-warn']/div/div/p")
        if varStatus == u"当前无患者咨询，请等待..." :
            print u"当前无患者咨询，请等待..."
        else:
            self.Level_PO.clickXpath("//button[@onclick='goTreat(this);']", 2)
            self.Level_PO.inputId("message-content", u"test")
            self.Level_PO.clickId("send_message", 2)
            self.Level_PO.clickXpath("//i[@ng-click='disconnetc()']", 2)

    def serverStatistic(self):
        '''药师 服务统计'''
        pass

    def historyAudit(self):
        '''药师 历史审核处方'''
        pass

    def drugInfo(self):
        '''药师 药品信息查询'''
        self.Level_PO.inIframe("myFrame", 2)

        # '查询药品名称'
        # self.Level_PO.inputName("name", "1")
        # self.Level_PO.clickId("btnQuery", 2)
        # # 检查查询结果 ？
        #
        # '重置查询结果'
        # self.Level_PO.clickId("btnReset", 2)
        # self.Level_PO.inputName("spell", "aj")
        # self.Level_PO.clickId("btnQuery", 2)
        # # 检查查询结果 ？

        '点击 新增'
        # self.Level_PO.clickXpath("//button[@onclick='addDrug()']", 2)

        '新增药品弹框'
        # self.Level_PO.inIframe("layui-layer-iframe100001", 2)
        # self.Level_PO.inputName("dbbundle_ttdruginfo[name]", u"六味地黄丸")  # *药品名称
        # self.Level_PO.inputName("dbbundle_ttdruginfo[chemicName]", u"化学名eelkwjr")  # 化学名
        # self.Level_PO.inputId("spec", u"1mg x 14片/盒装经典版本")  # 规格
        # self.Level_PO.inputName("dbbundle_ttdruginfo[spell]", u"lwdww")  # *首拼
        # self.Level_PO.selectNameText("dbbundle_ttdruginfo[classify]", u"草药")  # *药品类型
        # self.Level_PO.inputName("dbbundle_ttdruginfo[baseUnit]", u"粒")  # 基本单位
        # self.Level_PO.inputId("form", u"药剂型xyz1234567")  # 药品剂型
        # self.Level_PO.inputName("dbbundle_ttdruginfo[price]", "100.00")  # *单价
        # self.Level_PO.inputName("dbbundle_ttdruginfo[packUnit]", u"硬壳材料")  # 包装单位
        # self.Level_PO.inputName("dbbundle_ttdruginfo[remark]", u"备注信息")  # 备注
        # self.Level_PO.clickId("btnSave", 2)
        # self.Level_PO.clickLinktext(u"是", 2)
        # self.Level_PO.outIframe(2)
        # self.Level_PO.inIframe("myFrame", 2)

        '详情'
        Database_PO.cur.execute('select drug_id from tt_druginfo where name="%s" order by drug_id Desc limit 1' % (u"六味地黄丸"))
        t1 = Database_PO.cur.fetchone()
        self.Level_PO.clickXpath("//a[@onclick=\"userDetail('" + str(t1[0]) + "');\"]", 2)

        '查看药品详细信息'
        self.Level_PO.inIframe("layui-layer-iframe100001", 2)
        self.Level_PO.clickXpath("//button[@onclick='closeDialogInIframe()']", 2)  # 确定
        self.Level_PO.outIframe(1)

    def diagnosisRecord(self, varRole):
        '''医生 药师 问诊记录'''
        self.Level_PO.inIframe(u"myFrame", 2)
        self.Level_PO.inputName(u"createSymd", u"2017/01/01")  # 起始日期
        self.Level_PO.selectNameValue(u"approveStatus", u"2")  # 状态 2 = 审核通过
        self.Level_PO.inputName(u"hisRecipeId", u"95c0d834800336f1fecfeb73bc7f5f82")  # 处方编号
        self.Level_PO.clickXpath(u"//button[@id='btnQuery']", 2)  # 查询
        list = self.Level_PO.getXpathsText("//tr")
        if u"95c0d834800336f1fecfeb73bc7f5f82" in list[1]:
            print "OK， 找到处方编号"
        if u"本草堂 本草堂药店2" and u"11" and u"男" and u"25" and u"33" and u"头孢克肟颗粒" and u"￥0.0" and u"未评价" and u"审核通过" in list[2]:
            print "OK， 找到药品信息"

        # Level_B.inputNameClear(u"hisRecipeId","")  # 处方编号
        # Level_B.clickXpath(u"//button[@id='btnQuery']", 2)  # 查询
        # list2 = Level_B.getXpathsText("//tr")
        # print len(list2)
        # print list2[1]
        # print list2[2]
        # print list2[3]
        # print list2[4]
        self.Level_PO.outIframe(2)