# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2018-3-15
# Description: 电科智药，审方处方web，DrugstorePO 对象库
#***************************************************************

from time import sleep

class DrugstorePO(object):

    def __init__(self, Level_PO):
        self.Level_PO = Level_PO

    def login(self, varUser, varPass):

        '''login'''
        self.Level_PO.inputName(u"_username", varUser)
        self.Level_PO.inputName(u"_password", varPass)
        self.Level_PO.clickXpath(u"//button[@type='submit']", 2)


    def revisePass(self, orgPass, newPass):

        '''修改密码'''
        pass

    def drugManager_add(self, varCode, varProductName, varName, varFactoryName, varSpec, varFactoryShortName, varPrice):

        '''药店管理之药品添加'''
        # 添加药品
        self.Level_PO.clickXpath("//button[@data-target='#popup-drug-add']", 3)
        self.Level_PO.inputId("add-code", varCode)  # 批准文号
        sleep(1)
        self.Level_PO.inputName("product_name", varProductName)  # 商品名
        sleep(1)
        self.Level_PO.inputId("add-name", varName)  # 药品通用名
        sleep(1)
        self.Level_PO.inputId("add-factory-name", varFactoryName)  # 生产厂家
        sleep(1)
        self.Level_PO.inputId("add-spec", varSpec)  # 规格包装
        sleep(1)
        self.Level_PO.inputId("add_factory_short_name", varFactoryShortName)  # 厂家简称
        sleep(1)
        self.Level_PO.inputId("add_price", varPrice)  # 价格
        self.Level_PO.clickXpath("//label[@for='onoffswitch-add']", 2)  # 推荐
        self.Level_PO.clickXpath("//button[@onclick='doCreate();']", 2)  # 保存
        self.Level_PO.clickXpath("//button[@onclick='confirmCreate();']", 2)  # 再次确认
        return (varName ,varProductName)


    def drugManager_edit(self):

        '''药店管理之药品编辑'''
        pass


    def drugManager_del(self):

        '''药店管理之药品删除'''
        pass

    def drugManager_import(self):

        '''药店管理之批量导入'''
        pass

    def drugManager_search(self):

        '''药店管理之搜索（全部，推荐，药品类型，批准文号，关键字）'''
        pass

    def drugManager_page(self):

        '''药店管理之翻页、页码、记录数'''
        pass

    def recommend_add(self):

        '''建议搭配之添加'''
        pass

    def recommend_del(self):

        '''建议搭配之删除'''
        pass

    def prescriptionManager_search(self):

        '''处方管理之搜索（日期，状态，处方变化/姓名）'''
        pass

    def prescriptionManager_info(self):

        '''处方管理之详情'''
        pass

    def prescriptionManager_print(self):

        '''处方管理之打印'''
        pass

    def statistics_dealRank(self):

        '''业务统计之药店交易排行榜'''
        pass

    def statistics_deal(self):

        '''业务统计之药店交易'''
        pass

    def statistics_prescriptionAudit(self):

        '''业务统计之处方审核'''
        pass

    def statistics_consult(self):

        '''业务统计之医生咨询'''
        pass

    def statistics_prescriptionPass(self):

        '''业务统计之处方通过率'''
        pass
