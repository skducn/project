# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description:  电子健康档案数据监控中心（PC端）EHR对象库
# *****************************************************************

from instance.zyjk.EHR.config.config import *
import string,numpy
from string import digits

from PO.HtmlPO import *
from PO.ListPO import *
List_PO = ListPO()
from PO.StrPO import *
Str_PO = StrPO()
from PO.TimePO import *
Time_PO = TimePO()
from PO.ColorPO import *
Color_PO = ColorPO()

from PO.WebPO import *

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHRDC")

Web_PO = WebPO("chrome")
Web_PO.openURL(varURL)
Web_PO.driver.maximize_window()  # 全屏
# Web_PO.driver.set_window_size(1366,768)  # 按分辨率1366*768打开


class DataMonitorPO():

    def __init__(self):
        self.List_PO = ListPO()
        self.Color_PO = ColorPO()


    def login(self, varUser, varPass):

        ''' 登录 '''

        Web_PO.inputXpath("//input[@type='text']", varUser)
        Web_PO.inputXpath("//input[@type='password']", varPass)
        Web_PO.clickXpath("//button[@type='button']", 2)

        # # 获取所属社区
        # self.getCommunity(varUser)
        #
        # # 获取数据更新截止至时间
        # self.getUpdateDate(varUser)

    def clickMenu(self, varMenu1, varMenu2=""):

        ''' 点击左侧菜单 '''

        print("-" * 150)
        # 获取一级菜单列表(只有一级菜单)
        l_menu1 = Web_PO.getXpathsText("//li[@tabindex='-1']")
        # print(l_menu1)  # ['首页', '', '', '', '', '', '数据质量测评分析', '质控分析报告（社区）']
        if varMenu1 in str(l_menu1):
            d_menuOneLevel = self.List_PO.lists2dict(self.List_PO.listBatchDel(l_menu1, ""), Web_PO.getXpathsAttr("//div/ul/li/a", "href"))
            # print(d_menuOneLevel)  # {'首页': 'http://192.168.0.243:8082/#/index', '数据质量测评分析': 'http://192.168.0.243:8082/#/appraisal', '质控分析报告（社区）': 'http://192.168.0.243:8082/#/healthReport'}
            for k in d_menuOneLevel:
                if k == varMenu1:
                    Web_PO.clickXpathsContain("//a", "href", str(d_menuOneLevel[k]), 1)
            # self.Color_PO.consoleColor("31", "36", "[" + varMenu1 + "]", "")
            print("[" + varMenu1 + "]")
            print('\033[1;34;40m', '[' + varMenu1 + "]", '\033[0m')

        else:
            # 获取一二级菜单列表（必须有第二级菜单）
            l_tmp = Web_PO.getXpathsText("//li")
            l_menu1 = self.List_PO.listBatchDel(l_tmp, "")
            # print(l_menu1)  # ['首页', '质控结果分析', '数据质量测评分析', '质控分析报告（社区）']
            for l in range(len(l_menu1)):
                if varMenu1 == l_menu1[l]:
                    Web_PO.clickXpath("//div[@class='el-scrollbar__view']/ul/li[" + str(l+1) + "]", 2)
                    l_menuTwoName = Web_PO.getXpathsText("//li")
                    l_menuTwoHref = Web_PO.getXpathsAttr("//li[@aria-expanded='true']/ul/li//a", "href")
                    for p in l_menuTwoName:
                        if varMenu1 in p and varMenu2 in p :
                            l_menuTwoName = (p.split("\n"))
                            l_menuTwoName.pop(0)
                            # break
                    # print(l_menuTwoName)
                    # print(l_menuTwoHref)
                    d_menuTwo = self.List_PO.lists2dict(l_menuTwoName, l_menuTwoHref)
                    # print(d_menuTwo)  # {'区级': 'http://192.168.0.243:8082/#/recordService/district', '社区': 'http://192.168.0.243:8082/#/recordService/community'}
                    for k2 in d_menuTwo:
                        if k2 == varMenu2:
                            Web_PO.clickXpathsContain("//a", "href", str(d_menuTwo[k2]), 1)
            # self.Color_PO.consoleColor("31", "36", "[" + varMenu1 + "] - [" + varMenu2 + "]", "")
            # print("[" + varMenu1 + "] - [" + varMenu2 + "]")
            print('\033[1;34;40m', '[' + varMenu1 + '] - [' + varMenu2 + ']', '\033[0m')

    def getUpdateDate(self):
        ''' 获取质控数据截止日期 '''

        s_tmp = Web_PO.getXpathText("//div[@class='content_left']")
        updateDate = s_tmp.split("质控数据截止日期")[1]

        return updateDate.strip()  # 返回字符串日期

    def isDate(self, varStrDate):
        ''' 判断是有效日期 '''
        if Str_PO.str2date(varStrDate):
            return Str_PO.str2date(varStrDate)
        else:
            None


    def checkDate(self, varMsg, varEndDate, varReducedTime):
        ''' 判断日期质控日期不能早于 varDate '''

        if Time_PO.isDate1GTdate2(varEndDate, varReducedTime):
            self.Color_PO.consoleColor("31", "36", "[OK]" + str(varMsg) + str(varEndDate), "")
        else:
            self.Color_PO.consoleColor("31", "31", "[ERROR]" + str(varMsg) + str(varEndDate), "")


    def checkDigitalborder(self, varMsg, varActualValue, varSign, varBaseValue):
        if varSign == ">":
            if varActualValue > varBaseValue:
                self.Color_PO.consoleColor("31", "36", "[OK]" + str(varMsg), "")
            else:
                self.Color_PO.consoleColor("31", "31", "[ERROR]", str(varMsg) + ", 实测值：" + str(varActualValue))
        elif varSign == "<":
            if varActualValue < varBaseValue:
                self.Color_PO.consoleColor("31", "36", "[OK]" + str(varMsg), "")
            else:
                self.Color_PO.consoleColor("31", "31", "[ERROR]", str(varMsg) + ", 实测值：" + str(varActualValue))
        elif varSign == "<=":
            if varActualValue <= varBaseValue:
                self.Color_PO.consoleColor("31", "36", "[OK]" + str(varMsg), "")
            else:
                self.Color_PO.consoleColor("31", "31", "[ERROR]", str(varMsg) + ", 实测值：" + str(varActualValue))
        elif varSign == ">=":
            if varActualValue >= varBaseValue:
                self.Color_PO.consoleColor("31", "36", "[OK]" + str(varMsg), "")
            else:
                self.Color_PO.consoleColor("31", "31", "[ERROR]", str(varMsg) + ", 实测值：" + str(varActualValue))
        elif varSign == "!=":
            if varActualValue != varBaseValue:
                self.Color_PO.consoleColor("31", "36", "[OK]" + str(varMsg), "")
            else:
                self.Color_PO.consoleColor("31", "31", "[ERROR]", str(varMsg) + ", 实测值：" + str(varActualValue))

    def getDistrictLevel(self):
        ''' 质控结果分析 - 区级'''
        
        strTmp = Web_PO.getXpathText("//div[@class='resident']")

        # 辖区常住人口
        czrk = str(strTmp).split("辖区常住人口（人）\n")[1].split("\n建档率：")[0]
        sql_czrk = self.testSql('select top 1 (select sum(live_people_num) from (select live_people_num,org_name from report_qyyh group by org_code,org_name,live_people_num) a)  livePeopleNum from report_qyyh')
        Web_PO.assertEqualValue(str(czrk), str(sql_czrk), "辖区常住人口（人）", "辖区常住人口（人）")

        # 建档率
        jdl = str(strTmp).split("建档率：")[1].split("\n截止日期：")[0]
        sql_jdl = self.testSql('SELECT count(*) FROM report_qyyh WHERE A4=%s' % (1))
        sql_jdl = sql_jdl / sql_czrk * 100
        tmp = str(round(sql_jdl, 1)) + "%"
        Web_PO.assertEqualValue(str(jdl), str(tmp), "建档率", "建档率")

        # 截止日期
        jzrq = str(strTmp).split("截止日期：")[1].strip()

        # 1+1+1签约居民人数（人）
        strTmp = Web_PO.getXpathText("//div[@class='contract']")
        qyjm = str(strTmp).split("?\n")[1].split("\n签约率")[0]
        sql_qyjmrs = self.testSql('SELECT count(*) FROM report_qyyh')
        Web_PO.assertEqualValue(str(qyjm), str(sql_qyjmrs), "1+1+1签约居民人数（人）", "1+1+1签约居民人数（人）")

        # 签约率
        qyl = str(strTmp).split("签约率 ")[1].split("\n签约完成率")[0]
        sql_qyl = sql_qyjmrs / sql_czrk * 100
        tmp = str(round(sql_qyl, 1)) + "%"
        Web_PO.assertEqualValue(str(qyl), tmp, "签约率", "签约率")

        # 签约完成率
        qywcl = str(strTmp).split("签约完成率 ")[1].split("\n签约机构与档案管理机构不一致人数：")[0]
        sql_qywcl = sql_qyjmrs / (sql_czrk * 0.3)
        tmp = str(round(sql_qywcl * 100, 1)) + "%"
        Web_PO.assertEqualValue(str(qywcl), tmp, "签约完成率", "签约完成率")

        # 签约机构与档案管理机构不一致人数
        byz = str(strTmp).split("签约机构与档案管理机构不一致人数：")[1].split("\n人")[0]
        sql_byz = self.testSql(
            'select count(*) from report_qyyh where A411=%s and A4=%s SELECT count(*) FROM QYYH t1 INNER JOIN HrCover t2 ON t1.ArchiveUnitCode<>t2.ArchiveUnitCode and t2.ArchiveNum=t1.SFZH select count(*) from HrCover r1 INNER JOIN  QYYH r2 on r1.ArchiveUnitCode=r2.ArchiveUnitCode AND r1.ArchiveNum= r2.SFZH' % (
            1, 1))
        Web_PO.assertEqualValue(str(byz), str(sql_byz) + "人", "签约机构与档案管理机构不一致人数", "签约机构与档案管理机构不一致人数")


        # 签约居民分类之重点人群
        focusGroup = Web_PO.getXpathText("//div[@class='left_content']")
        sql_focusGroup = self.testSql('SELECT(SELECT SUM(IIF( A15 + A5 + A6 + A7 > 0, 1, 0 )) FROM report_qyyh ) * 100 / ( SELECT COUNT ( 1 ) FROM report_qyyh )')
        Web_PO.assertEqualValue(str(focusGroup), str(sql_focusGroup) + "%", "重点人群占比", "重点人群占比")

        # 签约居民分类之非重点人群
        noFocusGroup = Web_PO.getXpathText("//div[@class='right_content']")
        sql_noFocusGroup = 100 - sql_focusGroup
        Web_PO.assertEqualValue(str(noFocusGroup), str(sql_noFocusGroup) + "%", "非重点人群占比", "非重点人群占比")

        return czrk, sql_jdl, jzrq, qyjm, sql_qyl, sql_qywcl, sql_byz, sql_focusGroup, sql_noFocusGroup

    def getCommunity(self):
        ''' 质控结果分析 - 社区'''
        
        print("-" * 50)

        # 辖区常住人口（人）
        strTmp = Web_PO.getXpathText("//div[@class='resident']")
        czrk = str(strTmp).split("辖区常住人口（人）\n")[1].split("\n建档率：")[0]
        sql_czrk = self.testSql2('Select sum(live_people_num) from dict_org_info where hr_service_code=%s', "310118001")
        Web_PO.assertEqualValue(str(czrk), str(sql_czrk), "辖区常住人口（人）", "辖区常住人口（人）")

        # 建档率
        jdl = str(strTmp).split("建档率：")[1].split("\n截止日期：")[0]
        sql_jdl = self.testSql('SELECT count(*) FROM report_qyyh WHERE  A4=%s and hr_service_code=%s' % ("1", "310118001"))
        sql_jdl = sql_jdl / sql_czrk * 100
        tmp = str(round(sql_jdl, 1)) + "%"
        Web_PO.assertEqualValue(str(jdl), tmp, "建档率", "建档率")

        # 截止日期
        jzrq = str(strTmp).split("截止日期：")[1].strip()

        # 1+1+1签约居民人数
        strTmp = Web_PO.getXpathText("//div[@class='contract']")
        qyjm = str(strTmp).split("?\n")[1].split("\n签约率")[0]
        sql_qyjm = self.testSql('SELECT count(*) FROM report_qyyh where hr_service_code=%s' % ("310118001"))
        Web_PO.assertEqualValue(str(qyjm), str(sql_qyjm), "1+1+1签约居民人数（人）", "1+1+1签约居民人数（人）")

        # 签约率
        qyl = str(strTmp).split("签约率 ")[1].split("\n签约完成率")[0]
        sql_qyl = sql_qyjm / sql_czrk * 100
        tmp = str(round(sql_qyl, 1)) + "%"
        Web_PO.assertEqualValue(str(qyl), tmp, "签约率", "签约率")

        # 签约完成率
        qywcl = str(strTmp).split("签约完成率 ")[1].split("\n签约机构与档案管理机构不一致人数：")[0]
        sql_qywcl = sql_qyjm / (sql_czrk * 0.3)
        tmp = str(round(sql_qywcl * 100, 1)) + "%"
        Web_PO.assertEqualValue(str(qywcl), tmp, "签约完成率", "签约完成率")

        # 签约机构与档案管理机构不一致人数
        byz = str(strTmp).split("签约机构与档案管理机构不一致人数：")[1].split("\n人")[0]
        sql_byz = self.testSql(
            'select count(*) from report_qyyh where A411=%s and A4=%s and hr_service_code=%s SELECT count(*) FROM QYYH t1 INNER JOIN HrCover t2 ON t1.ArchiveUnitCode<>t2.ArchiveUnitCode and t2.ArchiveNum=t1.SFZH select count(*) from HrCover r1 INNER JOIN  QYYH r2 on r1.ArchiveUnitCode=r2.ArchiveUnitCode AND r1.ArchiveNum= r2.SFZH' % (
            1, 1, 310118001))
        Web_PO.assertEqualValue(byz, str(sql_byz) + "人", "签约机构与档案管理机构不一致人数", "签约机构与档案管理机构不一致人数")

        # 签约居民分类之重点人群
        focusGroup = Web_PO.getXpathText("//div[@class='left_content']")
        sql_focusGroup = self.testSql(
            'SELECT ( SELECT SUM ( IIF ( A15 + A5 + A6 + A7 > 0, 1, 0 )) FROM report_qyyh where  hr_service_code=%s ) * 100 / ( SELECT COUNT ( 1 ) FROM report_qyyh where  hr_service_code=%s)' % (
            "310118001", "310118001"))
        Web_PO.assertEqualValue(str(focusGroup), str(sql_focusGroup) + "%", "重点人群占比", "重点人群占比")

        # 签约居民分类之非重点人群
        noFocusGroup = Web_PO.getXpathText("//div[@class='right_content']")
        sql_noFocusGroup = 100 - sql_focusGroup
        Web_PO.assertEqualValue(str(noFocusGroup), str(sql_noFocusGroup) + "%", "非重点人群占比", "非重点人群占比")

        return czrk, sql_jdl, jzrq, qyjm, sql_qyl, sql_qywcl, sql_byz, sql_focusGroup, sql_noFocusGroup


    def getDoctor(self):
        '''  [质控结果分析] - [家庭医生]  '''

        strTmp = Web_PO.getXpathText("//div[@class='resident']")

        # 1+1+1签约居民人数（人）
        qyjm = str(strTmp).split("1+1+1签约居民人数（人）\n")[1].split("\n签约机构与档案管理机构不一致人数：")[0]
        sql_qyjm = self.testSql('SELECT count(*) FROM report_qyyh WHERE CZRYBM=%s and org_code=%s' % ('0041', "310118001"))
        Web_PO.assertEqualValue(str(qyjm), str(sql_qyjm), "1+1+1签约居民人数（人）", "1+1+1签约居民人数（人）")

        # 签约机构与档案管理机构不一致人数
        byz = str(strTmp).split("签约机构与档案管理机构不一致人数：")[1].split("人")[0]
        sql_byzrs = self.testSql('select count(*) from report_qyyh where A411=%s and A4=%s and hr_service_code=%s and CZRYBM=%s SELECT count(*) FROM QYYH t1 INNER JOIN HrCover t2 ON t1.ArchiveUnitCode<>t2.ArchiveUnitCode and t2.ArchiveNum=t1.SFZH select count(*) from HrCover r1 INNER JOIN  QYYH r2 on r1.ArchiveUnitCode=r2.ArchiveUnitCode AND r1.ArchiveNum= r2.SFZH' % (1, 1, "310118001", "0041"))
        Web_PO.assertEqualValue(str(byz), str(sql_byzrs), "签约机构与档案管理机构不一致人数", "签约机构与档案管理机构不一致人数")

        # 签约居民分类 - 重点人群
        focusGroup = Web_PO.getXpathText("//div[@class='left_content']")
        sql_focusGroup = self.testSql('select( SELECT SUM ( IIF ( A15 + A5 + A6 + A7 > 0, 1, 0 )) FROM report_qyyh  WHERE CZRYBM=%s and org_code=%s) * 100 / ( SELECT COUNT ( 1 ) FROM report_qyyh WHERE CZRYBM=%s and org_code=%s)' % ("0041", "310118001", "0041", "310118001"))
        Web_PO.assertEqualValue(str(focusGroup), str(sql_focusGroup) + "%", "重点人群占比", "重点人群占比")

        # 签约居民分类 - 非重点人群
        noFocusGroup = Web_PO.getXpathText("//div[@class='right_content']")
        sql_noFocusGroup = 100 - sql_focusGroup
        Web_PO.assertEqualValue(str(noFocusGroup), str(sql_noFocusGroup) + "%", "非重点人群占比", "非重点人群占比")

        return qyjm, byz, sql_focusGroup, sql_noFocusGroup


    def getCommunityNew(self):

        strTmp = Web_PO.getXpathText("//div")

        a = str(strTmp).split("签约居民中重点人群\n")[1].split(" 人")[0]
        b = str(strTmp).split("签约未建档人数：")[1].split("人")[0]
        c = str(strTmp).split("签约未建档人数：")[1].split("老年人")[0]
        # print(c)
        list1 = c.replace("\n", ",").replace("人", "").split(",")
        list1.pop(0)
        list1.pop(-1)
        # print("老年人:" + list1[0])
        # print("糖尿病:" + list1[1])
        # print("高血压:" + list1[2])
        # print("老年人与糖尿病:" + list1[3])
        # print("既是老年人又是高血压与糖尿病:" + list1[4])
        # print("老年人与高血压:" + list1[5])
        # print("糖尿病与高血压:" + list1[6])

        d = str(strTmp).split("60岁以上签约居民\n")[1].split(" 人")[0]
        e = str(strTmp).split("签约率：")[1].split("%")[0]
        f = str(strTmp).split("签约建档率：")[1].split("%")[0]
        g = str(strTmp).split("签约居民中非重点人群\n")[1].split(" 人")[0]
        h = str(strTmp).split("签约未建档人数：")[2].split("人")[0]
        i = str(strTmp).split("签约率\n")[1].split("%")[0]
        j = str(strTmp).split("签约建档率\n")[1].split("%")[0]
        k = str(strTmp).split("规范建档占比\n")[1].split("%")[0]
        l = str(strTmp).split("更新率\n")[1].split("%")[0]
        m = str(strTmp).split("利用率\n")[1].split("%")[0]

        return a,b,list1,d,e,f,g,h,i,j,k,l,m



    def openNewLabel(self, varURL):
        Web_PO.openNewLabel(varURL)
        Web_PO.switchLabel(1)  # 切换到新Label


    def recordService(self, varLabel, varPage=1):
        ''' 质控结果分析 - 区级 - 医疗机构名称 '''
        ''' 质控结果分析 - 区级 - 签约医生 '''
        ''' 质控结果分析 - 社区 - 签约医生 '''

        print("-" * 150)
        print('\033[1;34;40m', '[' + varLabel + "]" + " - 第" + str(varPage) + "页", '\033[0m')

        if varLabel == "签约医生":
            Web_PO.clickId("tab-doctor")

            # 切换到第2页 li[2]
            Web_PO.clickXpath("//*[@id='pane-doctor']/div/div/div[3]/div[2]/ul/li[" + str(varPage) + "]", 2)
            list1 = Web_PO.getXpathsText("//div")
            str1 = str(list1[0]).replace("\n", ",")
            # print(str1)

            l_title = []

            title = str1.split("导出,")[1].split("归属医疗机构名称,")[0]
            value = str1.rsplit("归属医疗机构名称,", 1)[1].split("签约医生,")[0]
            org = str1.rsplit("签约医生,", 1)[1].split(",共")[0]
            for i in range(len(title.split(",")) - 1):
                l_title.append(title.split(",")[i])
            l_title.insert(0, "签约医生")
            l_title.append("归属医疗机构名称")
            fields = 15

            print(l_title) # [['签约医生', '签约居民人数(人)', '新增签约居民人数(人)', '建档率(%)', '规范建档占比(%)', '档案更新率(%)', '档案利用率(%)', '档案封面及个人基本信息表错误项目总数（个）', '档案封面及个人基本信息表错误项目总数占比(%)', '健康体检表错误项目总数（个）', '健康体检表错误项目总数占比(%)', '高血压随访表错误项目总数（个）', '高血压随访表错误项目总数占比(%)', '糖尿病随访表错误项目总数（个）', '糖尿病随访表错误项目总数占比(%)'],


            # 签约医生字段
            l_org = []
            for i in range(len(org.split(","))):
                l_org.append(org.split(",")[i])
            # print(l_org)  # ['武*茜', '李*琳', '窦*青', '洪*娟', '孟*珺', '马*佳', '金*明', '张*琴', '黄*美', '张*芳']

            l_value = []
            # print(value)
            for i in range(len(value.split(",")) - 1):
                l_value.append(value.split(",")[i])
            l_valueAll = (List_PO.listSplitSubList(l_value, fields))
            # print(l_valueAll)  # 签约医生后面14个字段的值

            for i in range(len(l_org)):
                l_valueAll[i].insert(0, l_org[i])
            for i in range(len(l_org)):
                print(l_valueAll[i])  # ['武*茜', '281', '0', '86.5', '63.4', '87.6', '0', '8504', '61.8', '9349', '26.7', '0', '0', '0', '0', '上海市青浦区夏阳街道社区卫生服务中心']

            # 合并标题
            l_valueAll.insert(0, l_title)
            return l_valueAll

        elif varLabel == "医疗机构名称":
            Web_PO.clickId("tab-org")
            list1 = Web_PO.getXpathsText("//div")
            str1 = str(list1[0]).replace("\n", ",")
            title = str1.split("导出,")[1].split("档案利用率(%),")[0]
            value = str1.split("档案利用率(%),")[1].split("医疗机构名称,")[0]
            org = str1.split("医疗机构名称,")[1].split(",共")[0]
            l_title = []
            for i in range(len(title.split(","))-1):
                l_title.append(title.split(",")[i])
            l_title.insert(0, "医疗机构名称")
            l_title.append("档案利用率(%)")
            print(l_title)
            fields = 6

            # 医疗结构名称
            l_org = []
            for i in range(len(org.split(","))):
                l_org.append(org.split(",")[i])
            # print(l_org)  # ['上海市青浦区夏阳街道社区卫生服务中心', '上海市青浦区练塘镇社区卫生服务中心']

            l_value = []
            # print(value)
            for i in range(len(value.split(",")) - 1):
                l_value.append(value.split(",")[i])
            l_valueAll = (List_PO.listSplitSubList(l_value, fields))
            # print(l_valueAll)  # [['2702', '0', '88.9', '27.3', '95.6', '0'], ['765', '0', '89.5', '4.1', '15.9', '0']]

            for i in range(len(l_org)):
                l_valueAll[i].insert(0, l_org[i])
            for i in range(len(l_org)):
                print(l_valueAll[i])  # [['上海市青浦区夏阳街道社区卫生服务中心', '2702', '0', '88.9', '27.3', '95.6', '0'], ['上海市青浦区练塘镇社区卫生服务中心', '765', '0', '89.5', '4.1', '15.9', '0']]

            # 合并标题
            l_valueAll.insert(0, l_title)
            return l_valueAll

    def getRecordServiceValue(self, l_all, varOrg, varTitle):
        for i in range(len(l_all[0])):
            if varTitle == l_all[0][i]:
                sign = i
                break
        # print(sign)
        for i in range(len(l_all)):
            if l_all[i][0] == varOrg:
                return l_all[i][sign]


    def recordServiceCommunity(self, varLabel, varPage=1):

        ''' 质控结果分析 - 社区  '''

        print("-" * 150)
        print('\033[1;34;40m', '[' + varLabel + "]" + " - 第" + str(varPage) + "页", '\033[0m')

        if varLabel == "签约医生":
            Web_PO.clickId("tab-doctor")

            # 切换到第2页 li[2]
            Web_PO.clickXpath("//*[@id='pane-doctor']/div/div/div[3]/div[2]/ul/li[" + str(varPage) + "]", 2)
            list1 = Web_PO.getXpathsText("//div")
            str1 = str(list1[0]).replace("\n", ",")
            # print(str1)

            l_title = []

            # 社区
            title = str1.split("导出,")[1].split("糖尿病随访表错误项目总数占比(%),")[0]
            value = str1.rsplit("糖尿病随访表错误项目总数占比(%)", 1)[1].split("签约医生,")[0]
            org = str1.rsplit("签约医生,", 1)[1].split(",共")[0]
            for i in range(len(title.split(",")) - 1):
                l_title.append(title.split(",")[i])
            l_title.insert(0, "签约医生")
            l_title.append("糖尿病随访表错误项目总数占比(%)")
            fields = 14
            print(
                l_title)  # [['签约医生', '签约居民人数(人)', '新增签约居民人数(人)', '建档率(%)', '规范建档占比(%)', '档案更新率(%)', '档案利用率(%)', '档案封面及个人基本信息表错误项目总数（个）', '档案封面及个人基本信息表错误项目总数占比(%)', '健康体检表错误项目总数（个）', '健康体检表错误项目总数占比(%)', '高血压随访表错误项目总数（个）', '高血压随访表错误项目总数占比(%)', '糖尿病随访表错误项目总数（个）', '糖尿病随访表错误项目总数占比(%)'],

            # 签约医生字段
            l_org = []
            for i in range(len(org.split(","))):
                l_org.append(org.split(",")[i])
            # print(l_org)  # ['武*茜', '李*琳', '窦*青', '洪*娟', '孟*珺', '马*佳', '金*明', '张*琴', '黄*美', '张*芳']

            l_value = []
            # print(value)
            for i in range(len(value.split(",")) - 1):
                l_value.append(value.split(",")[i])
            l_value.pop(0)
            l_valueAll = (List_PO.listSplitSubList(l_value, fields))
            # print(l_valueAll)  # 签约医生后面14个字段的值

            for i in range(len(l_org)):
                l_valueAll[i].insert(0, l_org[i])
            for i in range(len(l_org)):
                print(l_valueAll[
                          i])  # ['武*茜', '281', '0', '86.5', '63.4', '87.6', '0', '8504', '61.8', '9349', '26.7', '0', '0', '0', '0', '上海市青浦区夏阳街道社区卫生服务中心']

            # 合并标题
            l_valueAll.insert(0, l_title)
            return l_valueAll

        elif varLabel == "签约居民列表":

            Web_PO.clickId("tab-personnel")

            # 切换到第2页 li[2]
            Web_PO.clickXpath("//*[@id='pane-personnel']/div/div[1]/div[3]/div[2]/ul/li[" + str(varPage) + "]", 2)


            l_groupDeficiency = (Web_PO.getXpathsText("//div[@class='ellipsis el-popover__reference']"))
            # l_groupDeficiency = [i for i in l_groupDeficiency if i != '']  # 去掉空元素 ,如 [, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            # l_groupDeficiency = [str(i).replace("\n", "") for i in l_groupDeficiency if i != '']  # 去掉空元素 ,如 [, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            l_deficiency = []
            for i in range(20):
                if l_groupDeficiency[i] == '':
                    l_deficiency.append("空")
                else:
                    l_deficiency.append(l_groupDeficiency[i])
            # print(l_deficiency) # ['老', '空', '老 糖', '糖\n1', '老', '空', '糖', '糖\n1', '糖', '空', '老 高', '高\n2', '老', '空', '老 高', '高\n2', '老 高 糖', '高\n1\n糖\n1', '老 高', '高\n2']


            list1 = Web_PO.getXpathsText("//div")
            str1 = str(list1[0]).replace("\n", ",")
            # print(str1)
            title = str1.split("导出,")[1].split("糖尿病随访表,")[0]
            value = str1.split("糖尿病随访表,")[1].split("签约医生")[0]
            org = str1.split("签约医生 身份证号")[1].split(",共")[0]
            l_title = []
            for i in range(len(title.split(",")) - 1):
                l_title.append(title.split(",")[i])
            # print(l_title)
            l_1 = l_title.pop(0).split(" ")  # ['联系电话 姓名 人群分类 档案问题 规范建档占比(%)'
            l_1.insert(0, "身份证号")
            l_1.insert(0, "签约医生")
            l_2 = [i for i in l_title if i != '']   # 删除列表中空白元素，不能使用for，
            l_2.append("糖尿病随访表")
            l_2.remove("各表单质控错误项目数量（个）")
            # print(l_2)  # ['档案封面', '个人基本信息表', '健康体检表', '高血压随访表', '糖尿病随访表']
            l_title = []
            l_title = l_1 + l_2
            l_title.append("缺失表单类型")
            print(l_title)  # ['签约医生', '身份证号', '联系电话', '姓名', '人群分类', '档案问题', '规范建档占比(%)', '档案封面', '个人基本信息表', '健康体检表', '高血压随访表', '糖尿病随访表', '缺失表单类型']
            fields = 10

            # ['签约医生', '身份证号']
            l_org = []
            for i in range(len(org.split(","))):
                l_org.append(org.split(",")[i].replace(" ", ""))
            l_org = [i for i in l_org if i != '']
            # print(l_org)  # ['古*尔', '000000000000000000', '戴*星', '110108195005133414', '戴*星', '130102197708161811', '马*佳', '130206194905170351', '洪*娟', '130602195509150931', '张*琴']

            # l_value = []
            # 除['签约医生', '身份证号']外，其他值
            l_33 = [i for i in str(value).split(",") if i != '']  # 等同于 # l_33 = str(value).split(",")   # l_33 = [i for i in l_33 if i != '']
            # print(l_33)
            l4 = []
            for i in range(len(l_33)):
                if "*" in l_33[i] and i == 0:
                    l4.append("空")
                    l4.append(l_33[i])
                    l4.append(l_33[i + 1])
                    l4.append(l_33[i + 2])
                    l4.append(l_33[i + 3])
                    l4.append(l_33[i + 4])
                    l4.append(l_33[i + 5])
                    l4.append(l_33[i + 6])
                    l4.append(l_33[i + 7])
                    l4.append(l_33[i + 8])
                elif "*" in l_33[i]:
                    if len(l_33[i - 1]) < 7:
                        l4.append("空")
                    else:
                        l4.append(l_33[i - 1])
                    l4.append(l_33[i])
                    l4.append(l_33[i + 1])
                    l4.append(l_33[i + 2])
                    l4.append(l_33[i + 3])
                    l4.append(l_33[i + 4])
                    l4.append(l_33[i + 5])
                    l4.append(l_33[i + 6])
                    l4.append(l_33[i + 7])
                    l4.append(l_33[i + 8])
            # print(l4)

            # 当前页的签约居民列表明细
            l_valueAll = []
            for i in range(int(len(l_org)/2)):
                l_value = List_PO.listSplitSubList(l_org, 2)[i] + List_PO.listSplitSubList(l4, 10)[i]
                l_value.append(l_deficiency[i*2+1])
                # print(l_value)
                x = List_PO.listClearSpecialChar(l_value)
                print(x)
                l_valueAll.append(x)

            # 合并标题
            l_valueAll.insert(0, l_title)
            return l_valueAll

    def recordServiceCommunityCol(self, l_all, varTitle):
        for i in range(len(l_all[0])):
            if varTitle == l_all[0][i]:
                sign = i
                break
        # print(sign)
        l_tmp = []
        for i in range(1, len(l_all)):
            l_tmp.append(l_all[i][sign])

        return l_tmp

    def testPercentage(self, l_all):
        # 检查所有包含%字段的值，判断是否大于100?
        # error, 建档率(%) - ['197.5', '195', '1100']
        sign = 0
        l_tmp = []
        tmp = ""
        list1 = []
        for i in range(len(l_all[0])):
            if "(%)" in l_all[0][i]:
                sign = i
                for j in range(1, len(l_all)):
                    l_tmp.append(l_all[j][sign])
                for k in range(len(l_tmp)):
                    if float(l_tmp[k]) > 100:
                        list1.append(l_tmp[k])
                if len(list1) > 0:
                    print("error, " + l_all[0][sign] + " - " + str(list1))  # error, 建档率(%) - ['97.5', '95', '100']
                list1 = []
                l_tmp = []


    def testSql(self, varSql):
        # cursor.execute('SELECT * FROM persons WHERE salesrep=%s' %s ('John Doe'))
        l_result = Sqlserver_PO.ExecQuery(varSql)
        return (l_result[0][0])

    def testSql2(self, varSql, varParam):
        # cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
        l_result = Sqlserver_PO.ExecQuery2(varSql, varParam)
        return (l_result[0][0])



    def homePage_indicator(self):

        '''总体指标分布'''

        l_text = Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
        l_overallIndex = l_text[0].split("总体指标分布\n")[1].split("\n更新档案总数(份)")[0]
        l_overallIndex = l_overallIndex.split('\n')
        self.Color_PO.consoleColor("31", "36", l_overallIndex.pop(0), "\n")  # 数据更新截止至时间：2020年07月15日
        l_overallIndex.append("更新档案总数(份)")
        d_overallIndex = (self.List_PO.list2dictBySerial(l_overallIndex))
        d_overallIndex = {value: key for key, value in d_overallIndex.items()}
        self.Color_PO.consoleColor("31", "31", "[总体指标分布]", "")  # [总体指标分布]
        print(d_overallIndex)  # {'常住人口(人)': '111111', '户籍人口(人)': '1212', '目标建档总数(份)': '83334', '问题档案数量(份)': '20000', '更新档案总数(份)': '0'}
        l_overallIndex2 = l_text[0].split("更新档案总数(份)\n")[1].split("\n电子健康档案分布图")[0]
        l_overallIndex2 = l_overallIndex2.split('\n')
        d_overallIndex2 = (self.List_PO.list2dictBySerial(l_overallIndex2))
        del d_overallIndex2["标准"]
        d_overallIndex2 = {value: key for key, value in d_overallIndex2.items()}
        print(d_overallIndex2)  # {'户籍人口占比': '1.09%', '实际建档率': '18%', '问题档案占比': '100%', '档案更新率': '0%'}
    def homePage_EhrMap(self):

        '''电子健康档案分布图'''

        l_text = Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
        self.Color_PO.consoleColor("31", "31", "\n[电子健康档案分布图]", "")  # [电子健康档案分布图]
        l_ehrMap = l_text[0].split("家庭医生团队分布\n")[1].split("\n前往页")[0]
        l_ehrMap = l_ehrMap.split('\n')
        l_ehrMap.pop(-1)
        x = (self.List_PO.listSplitSubList(l_ehrMap, 4))  # [['团队', '建档数量(份)', '问题档案数量(份）', '问题档案占比'], ['王敬丽团队', '1959', '1959', '100.00%'], ['周坤团队', '1754', '1754', '100.00%'], ['中心团队', '1116', '1116', '100.00%'], ['郁红娟团队', '955', '955', '100.00%'], ['严慧艳团队', '945', '945', '100.00%'], ['12']]
        for i in x:
            print(i)
    def homePage_signDoctor(self):

        '''签约医生分布'''

        l_text = Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
        self.Color_PO.consoleColor("31", "31", "\n[签约医生分布]", "")  # [签约医生分布]
        l_signDoctor = l_text[0].split("问题统计列表\n")[1].split("\n前往页")[0]
        l_signDoctor = l_signDoctor.split('\n')
        l_signDoctor.pop(-1)
        x = (self.List_PO.listSplitSubList(l_signDoctor, 6))
        for i in x:
            print(i)
    def homePage_age(self):

        '''年龄分布'''

        l_text = Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
        self.Color_PO.consoleColor("31", "31", "\n[年龄分布]", "")  # [年龄分布]
        l_age = l_text[0].split("年龄分布\n")[1].split("\n前往页")[0]
        l_age = l_age.split('\n')
        l_age.pop(-1)
        x = (self.List_PO.listSplitSubList(l_age, 4))  # [['年龄', '建档数量(份)', '问题档案数量(份)', '问题档案占比'], ['7-64岁', '12727', '12727', '100.00%'], ['65岁以上', '4496', '4496', '100.00%'], ['0-6岁', '2776', '2776', '100.00%']]
        for i in x:
            print(i)
    def homePage_disease(self):

        '''疾病分布'''

        l_text = Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
        self.Color_PO.consoleColor("31", "31", "\n[疾病分布]", "")  # [疾病分布]
        l_disease = l_text[0].split("疾病分布\n")[1].split("\n前往页")[0]
        l_disease = l_disease.split('\n')
        l_disease.pop(-1)
        x = (self.List_PO.listSplitSubList(l_disease, 4))  # [['疾病', '建档数量(份)', '问题档案数量(份)', '问题档案占比']]
        for i in x:
            print(i)
    def homePage_specialPeople(self):

        '''特殊人群分布'''

        l_text = Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
        self.Color_PO.consoleColor("31", "31", "\n[特殊人群分布]", "")  # [特殊人群分布]
        l_specialPeople = l_text[0].split("特殊人群分布\n")[1].split("\n前往页")[0]
        l_specialPeople = l_specialPeople.split('\n')
        l_specialPeople.pop(-1)
        x = (self.List_PO.listSplitSubList(l_specialPeople, 4))  # [['疾病', '建档数量(份)', '问题档案数量(份)', '问题档案占比']]
        for i in x:
            print(i)
    def qcAnalysis_dropDownList1(self, varSelectName):

        ''' 档案质控分析 - 档案质控总体情况 - 下拉框选值'''

        self.Color_PO.consoleColor("31", "31", "\n[档案质控总体情况 - 查询 - " + varSelectName + "]", "")
        Web_PO.clickXpath("//input[@placeholder='请选择质控时间']", 2)
        l_text2 = Web_PO.getXpathsTextPart("//body/div[2]/div/div/ul/li/span", "Copyright © 2019上海智赢健康科技有限公司出品")
        l_text2 = self.List_PO.listSerialNumber(l_text2, 1)
        d_text2 = self.List_PO.list2dictByTuple(l_text2)
        d_text2 = {v: k for k, v in d_text2.items()}
        for k in d_text2:
            if k == varSelectName:
                Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(d_text2[k]) + "]", 2)

        # 显示搜索结果
        l_text = Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")
        l_qcOverall = l_text[0].split("重置\n")[1].split("\n本页")[0]
        l_qcOverall = l_qcOverall.split('\n')
        str1 = l_qcOverall.pop(0)
        print(str1)  # '质控时间 质控档案总数量 问题档案数量 规范建档率 操作'
        global list3
        list3 = []
        x = (self.List_PO.listSplitSubList(l_qcOverall, 6))
        for i in x:
            print(i)
            list3.append(i[0])
    def qcAnalysis_dropDownList1_opr(self, varKey, varOpr, varRule="", varPageNum=1):

        ''' 档案质控分析 - 档案质控总体情况 - 操作（详情，规范建档率提升分析）'''

        a = [list3.index(x) for x in list3 if x == varKey][0]
        if varOpr == "规范建档率提升分析":
            self.Color_PO.consoleColor("31", "31", "\n[规范建档率提升分析]", "")
            Web_PO.clickXpath("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr[" + str(a + 1) + "]/td[5]/div/div/div[2]/button", 2)  # 点击 记录规范建档率提升分析
            l_text = Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
            l_standardAnalysis = l_text[0].split("规范建档率提升分析\n序")[1].split("\n问题档案列表")[0]
            l_standardAnalysis = l_standardAnalysis.split('\n')
            tmp1 = l_standardAnalysis.pop(0)
            print("序" + tmp1)  # '序号 规则类型 问题档案数量(份) 规范建档率提升至'
            x = (self.List_PO.listSplitSubList(l_standardAnalysis, 4))
            x.pop(-1)
            for i in x:
                print(i)
        elif varOpr == "详情":
            # 点击 档案质控总体情况列表中的详情
            Web_PO.clickXpath("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr[" + str(a + 1) + "]/td[5]/div/div/div[1]/button", 2)
            if varRule == "":   # 默认不勾选规则类型
                self.Color_PO.consoleColor("31", "31", "\n[问题档案列表]", "")
            else:
                self.Color_PO.consoleColor("31", "31", "\n[问题档案列表 - " + varRule + "]", "")
                Web_PO.scrollIntoView("//div[@class='el-checkbox-group']/label[1]", 2)
                l_rule = Web_PO.getXpathsText("//div[@class='el-checkbox-group']/label")  # ['规范性 (10.99%)', '完整性 (59.47%)', '有效性 (29.54%)']
                l_rule = self.List_PO.listSerialNumber(l_rule, 1)
                d_rule = self.List_PO.list2dictByTuple(l_rule)
                d_rule = {value: key for key, value in d_rule.items()}

                # 选择规则类型
                varQty = varRule.split(",")
                if len(varQty) == 1:
                    for k in d_rule:
                        if varRule in k:
                            Web_PO.clickXpath("//div[@class='el-checkbox-group']/label[" + str(d_rule[k]) + "]", 2)
                else:
                    for i in range(len(varQty)):
                        for k in d_rule:
                            if varQty[i] in k:
                                Web_PO.clickXpath("//div[@class='el-checkbox-group']/label[" + str(d_rule[k]) + "]", 2)

            # 前往第几页（默认第一页）
            Web_PO.scrollIntoView("//input[@placeholder='请选择']", 2)
            Web_PO.inputXpathClearEnter("//div[@class='block']/div[2]/span/div/input", varPageNum)

            l_text = Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
            l_problemList = l_text[0].split("问题档案列表\n")[1].split("\n操作")[0]
            l_problemList = l_problemList.split('\n')
            # x = (self.List_PO.listSplitSubList(l_problemList, 5))
            for i in l_problemList:
                print(i)  # ['规则类型:', '规范性 (10.99%)', '完整性 (59.47%)', '有效性 (29.54%)']
            l_problemList = l_text[0].split("错误描述\n")[1].split("\n选择当前页数显示")[0]
            l_problemList = l_problemList.split('\n')
            l_problemList1 = (self.List_PO.listSplitSubList(l_problemList, 8))
            for i in l_problemList1:
                print(i)
            return l_problemList1
    def qcAnalysis_problem_opr(self,varList1, varIdCard):

        ''' 档案质控分析 - 问题档案列表 - 操作（患者身份证）
        获取患者质控项目汇总列表（健康档案封面 和 个人基本信息表）'''

        try:
            for i in range(len(varList1)):
                if varIdCard == varList1[i][1]:
                    varPatient = Web_PO.getXpathText("//div[@class='tableEHRss']/div/div/div[" + str(i + 1) + "]/div[3]")
                    Web_PO.clickXpath("//div[@class='tableEHRss']/div/div/div[" + str(i + 1) + "]/div[1]/div/span", 2)
                    break
            self.Color_PO.consoleColor("31", "31", "\n[质控项目汇总 - " + str(varIdCard) + "(" + varPatient + ")]", "")
            self.Color_PO.consoleColor("31", "33", "\n[健康档案封面]", "")
            l_text = Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
            l_cover = l_text[0].split("健康档案封面\n")[1].split("\n个人基本信息表")[0]
            l_cover = l_cover.split('\n')
            # print(l_cover)
            # 格式化 健康档案封面
            l_cover_format = []
            for i in range(len(l_cover)):
                if i < len(l_cover):
                    if ":" in l_cover[i] and "(" not in l_cover[i + 1]:
                        l_cover_format.append(l_cover[i] + l_cover[i + 1])
                        l_cover.pop(i + 1)
                    else:
                        l_cover_format.append(l_cover[i])
            print(l_cover_format.pop(0))  # 问题数：1
            d_cover_format = self.List_PO.list2dictBySerial(l_cover_format)
            for k in d_cover_format:
                print(k, d_cover_format[k])

            self.Color_PO.consoleColor("31", "33", "\n[个人基本信息表]", "")
            l_basic = l_text[0].split("个人基本信息表\n")[1].split("\n健康档案封面")[0]
            l_basic = l_basic.split('\n')
            # print(l_basic)
            # 格式化 个人基本信息表
            l_basic_format = []
            for i in range(len(l_basic)):
                if i < len(l_basic):
                    if ":" in l_basic[i] and "(" not in l_basic[i + 1]:
                        l_basic_format.append(l_basic[i] + l_basic[i + 1])
                        l_basic.pop(i + 1)
                    else:
                        l_basic_format.append(l_basic[i])
            print(l_basic_format.pop(0))  # 问题数：19
            d_basic_format = self.List_PO.list2dictBySerial(l_basic_format)
            for k in d_basic_format:
                print(k, d_basic_format[k])
        except:
            self.Color_PO.consoleColor("31", "31", "[ERROR]", "身份证号(" + str(varIdCard) + ")有误，请检查！")
    def qcAnalysis_problem_page(self, varPageNum):

        ''' 档案质控分析 - 问题档案列表 - 翻页 '''

        Web_PO.scrollIntoView("//input[@placeholder='请选择']", 2)
        Web_PO.inputXpathClearEnter("//div[@class='block']/div[2]/span/div/input", varPageNum)
    def sys_userList(self):

        '''用户列表'''

        self.Color_PO.consoleColor("31", "31", "\n[用户列表]", "")
        l_text = Web_PO.getXpathsText("//td/div")
        if varUser_session == "admin":
            l_userList = (self.List_PO.listSplitSubList(l_text, 7))
        else:
            l_userList = (self.List_PO.listSplitSubList(l_text, 6))
        l_userList2 = []
        for i in range(len(l_userList)):
            if l_userList[i][0] != "":
                l_userList2.append(l_userList[i])
        for i in l_userList2:
            print(i)
    def sys_user_search(self, varType, varValue):

        ''' 系统管理 - 用户管理 - 搜索（用户名、昵称、手机号）'''
        try:
            Web_PO.clickXpath("//form[@class='el-form login-form el-form--inline']/div[1]/div/div/div/div/div/input", 2)  # 请选择
            if varType == '用户名':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[1]", 2)  # 用户名
            elif varType == '昵称':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[2]", 2)  # 昵称
            elif varType == '手机':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[3]", 2)  # 手机
            else:
                exit()
            Web_PO.inputXpathClear("//input[@placeholder='请输入搜索内容']", varValue)  # 输入搜索内容
            Web_PO.clickXpath("//form[@class='el-form login-form el-form--inline']/div[2]/div/button[1]", 2)  # 查找
            l_text = Web_PO.getXpathsText("//td/div")
            if l_text == None:
                return False
            else:
                l_userList = (self.List_PO.listSplitSubList(l_text, 6))
                # print(l_userList)
                for i in range(len(l_userList)):
                    if l_userList[i][1] == varValue:
                        return True
                return False
        except:
            exit()
    def sys_user_add(self, varAccount, varNickName, varPhone, varAttr, varCommunity=""):

        '''系统公里 - 用户管理 - 增加用户'''

        try:
            self.Color_PO.consoleColor("31", "31", "\n[增加用户]", "")
            varResult = self.sys_user_search("用户名", varAccount)  # 依据用户名搜索
            if varResult == False:
                Web_PO.clickXpath("//button[@class='el-button el-button--success el-button--mini']", 2)  # 点击 新增
                Web_PO.inputXpath("//input[@placeholder='用户名']", varAccount)  # 用户名不能重复，且不能是中文
                Web_PO.inputXpath("//input[@placeholder='昵称']", varNickName)
                Web_PO.inputXpath("//input[@placeholder='手机']", varPhone)
                Web_PO.clickXpath("//tr[@class='el-table__row']/td[5]", 2)  # 点击 用户属性
                l_text = Web_PO.getXpathsText("//div/div/div/ul/li")
                l_text = self.List_PO.listIntercept(l_text, '1', 1)
                l_text = self.List_PO.listBatchDel(l_text, "")  # ['家庭医生', '家庭医生助理', '院长', '护士']
                for i in range(len(l_text)):
                    if l_text[i] == varAttr:
                        Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(i+1) + "]", 2)  # 选择用户属性
                        break
                if varUser_session == "admin":
                    Web_PO.clickXpath("//tr[@class='el-table__row']/td[5]", 2)  # 点击 用户属性
                    l_text = Web_PO.getXpathsText("//div/div[1]/div[1]/ul/li")
                    l_text = self.List_PO.listBatchDel(l_text, "")  # ['家庭医生', '家庭医生助理', '院长', '护士']
                    l_text.pop(0)
                    for i in range(len(l_text)):
                        if l_text[i] == varAttr:
                            Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(i + 1) + "]", 2)  # 选择用户属性
                            break
                    Web_PO.clickXpath("//tr[@class='el-table__row']/td[6]", 2)  # 点击 所属社区
                    l_text = Web_PO.getXpathsText("//div/div[1]/div[1]/ul/li")
                    l_text = self.List_PO.listBatchDel(l_text, "")  # ['临汾路街道社区卫生服务中心', '芷江西路街道社区卫生服务中心', '北站街道社区卫生服务中心', '宝山路街道社区卫生服务中心', '彭浦新村街道社区卫生服务中心', '彭浦镇社区卫生服务中心', '天目西路街道社区卫生服务中心', '共和新路街道社区卫生服务中心', '大宁路街道社区卫生服务中心', '大桥社区卫生服务中心', '四平社区卫生服务中心', '延吉社区卫生服务中心', '五角场镇社区卫生服务中心', '殷行社区卫生服务中心', '平凉社区卫生服务中心', '长白社区卫生服务中心', '江浦社区卫生服务中心', '控江社区卫生服务中心', '五角场街道社区卫生服务中心', '定海社区卫生服务中心', '金泽镇社区卫生服务中心', '练塘镇社区卫生服务中心', '白鹤社区卫生服务中心', '华新镇社区卫生服务中心', '香花桥街道社区卫生服务中心', '盈浦街道社区卫生服务中心', '朱家角镇社区卫生服务中心', '徐泾镇社区卫生服务中心', '重固镇社区卫生服务中心', '赵巷镇社区卫生服务中心', '潍坊社区卫生服务中心', '周家渡社区卫生服务中心', '金杨社区卫生服务中心', '沪东社区卫生服务中心', '塘桥社区卫生服务中心', '金桥社区卫生服务中心', '南码头社区卫生服务中心', '上钢社区卫生服务中心', '东明社区卫生服务中心', '陆家嘴社区卫生服务中心', '洋泾社区卫生服务中心', '浦兴社区卫生服务中心', '联洋社区卫生服务中心', '花木社区卫生服务中心', '三林社区卫生服务中心', '北蔡社区卫生服务中心', '唐镇社区卫生服务中心', '高东社区卫生服务中心', '高行社区卫生服务中心', '张江社区卫生服务中心', '曹路社区卫生服务中心', '机场社区卫生服务中心', '江镇社区卫生服务中心', '合庆社区卫生服务中心', '王港社区卫生服务中心', '川沙社区卫生服务中心', '黄楼社区卫生服务中心', '高桥社区卫生服务中心', '凌桥社区卫生服务中心', '迎博社区卫生服务中心', '孙桥社区卫生服务中心', '芦潮港社区卫生服务中心', '航头社区卫生服务中心', '新场社区卫生服务中心', '宣桥社区卫生服务中心', '六灶社区卫生服务中心', '祝桥社区卫生服务中心', '惠南社区卫生服务中心', '大团社区卫生服务中心', '周浦社区卫生服务中心', '泥城社区卫生服务中心', '书院社区卫生服务中心', '万祥社区卫生服务中心', '老港社区卫生服务中心', '康桥社区卫生服务中心', '朱泾社区卫生服务中心', '朱泾镇新农社区卫生服务中心', '亭林镇社区卫生服务中心', '廊下镇社区卫生服务中心', '山阳镇社区卫生服务中心', '吕巷镇社区卫生服务中心', '吕巷镇干巷镇社区卫生服务中心', '枫泾镇社区卫生服务中心', '枫泾镇兴塔社区卫生服务中心', '张堰镇社区卫生服务中心', '漕泾镇社区卫生服务中心', '金山卫镇社区卫生服务中心', '金山工业区社区卫生服务中心', '石化街道社区卫生服务中心', '马陆镇社区卫生服务中心', '嘉定工业区社区卫生服务中心', '嘉定区真新社区卫生服务中心', '嘉定区迎园医院/新成街道社区卫生服务中心', '嘉定区徐行镇社区卫生服务中心', '嘉定区华亭镇社区卫生服务中心', '嘉定镇街道社区卫生服务中心', '外冈镇社区卫生服务中心', '安亭镇社区卫生服务中心', '安亭镇黄渡社区卫生服务中心', '江桥镇社区卫生服务中心', '菊园社区卫生服务中心', '南翔镇社区卫生服务中心', '打浦桥街道社区卫生服务中心', '淮海中路街道社区卫生服中心', '瑞金二路街道社区卫生服务中心', '五里桥街道社区卫生服务中心', '南京东路街道社区卫生服务中心', '外滩街道社区卫生服务中心', '小东门街道社区卫生服务中心', '老西门街道社区卫生服务中心', '半淞园街道社区卫生服务中心', '豫园街道社区卫生服务中心', '曲阳路街道社区卫生服务中心', '凉城新村街道社区卫生服务中心', '广中路街道社区卫生服务中心', '欧阳路街道社区卫生服务中心', '嘉兴路街道社区卫生服务中心', '提篮桥街道社区卫生服务中心', '江湾镇街道社区卫生服务中心', '四川北路街道社区卫生服务中心', '南桥镇社区卫生服务中心', '西渡社区卫生服务中心', '光明社区卫生服务中心', '庄行镇社区卫生服务中心', '邬桥社区卫生服务中心', '金汇镇社区卫生服务中心', '泰日社区卫生服务中心', '齐贤社区卫生服务中心', '柘林镇社区卫生服务中心', '胡桥社区卫生服务中心', '新寺社区卫生服务中心', '青村镇社区卫生服务中心', '钱桥社区卫生服务中心', '奉城镇社区卫生服务中心', '塘外社区卫生服务中心', '头桥社区卫生服务中心', '四团镇社区卫生服务中心', '平安社区卫生服务中心', '海湾镇社区卫生服务中心', '五四社区卫生服务中心', '燎原社区卫生服务中心', '海湾镇社区卫生服务中心奉新分中心', '四团镇社区卫生服务中心邵场分中心', '南桥镇社区卫生服务中心贝港分中心', '横沙乡社区卫生服务中心', '新村乡社区卫生服务中心', '堡镇社区卫生服务中心', '中兴镇社区卫生服务中心', '新海镇社区卫生服务中心', '竖新镇社区卫生服务中心', '向化镇社区卫生服务中心', '港沿镇社区卫生服务中心', '东平镇社区卫生服务中心', '新河镇社区卫生服务中心', '三星镇社区卫生服务中心', '港西镇社区卫生服务中心', '陈家镇社区卫生服务中心', '庙镇社区卫生服务中心', '长兴镇社区卫生服务中心', '建设镇社区卫生服务中心', '绿华镇社区卫生服务中心', '城桥镇社区卫生服务中心', '程家桥街道社区卫生服务中心', '北新泾街道社区卫生服务中心', '虹桥街道社区卫生服务中心', '华阳街道社区卫生服务中心', '仙霞街道社区卫生服务中心', '江苏街道社区卫生服务中心', '周桥街道社区卫生服务中心', '新华街道社区卫生服务中心', '新泾镇社区卫生服务中心', '天山社区卫生服务中心', '杨行镇社区卫生服务中心', '大场镇祁连社区卫生服务中心', '顾村镇社区卫生服务中心', '罗店镇社区卫生服务中心', '罗泾镇社区卫生服务中心', '吴淞街道社区卫生服务中心', '月浦镇月浦社区卫生服务中心', '淞南镇社区卫生服务中心', '庙行镇社区卫生服务中心', '张庙街道长江路社区卫生服务中心', '高境镇社区卫生服务中心', '大场镇大场社区卫生服务中心', '张庙街道泗塘社区卫生服务中心', '月浦镇盛桥社区卫生服务中心', '友谊街道社区卫生服务中心', '顾村镇菊泉新城社区卫生服务中心', '大场镇第三社区卫生服务中心', '南京西路街道社区卫生服务中心', '石门二路街道社区卫生服务中心', '江宁路街道社区卫生服务中心', '静安寺街道社区卫生服务中心', '曹家渡街道社区卫生服务中心', '曹杨街道社区卫生服务中心', '甘泉街道社区卫生服务中心', '长风街道长风社区卫生服务中心', '长风街道白玉社区卫生服务中心', '长寿街道社区卫生服务中心', '宜川街道社区卫生服务中心', '石泉街道社区卫生服务中心', '真如镇社区卫生服务中心', '长征镇社区卫生服务中心', '桃浦镇社区卫生服务中心', '岳阳街道社区卫生服务中心', '新桥街道社区卫生服务中心', '九亭街道社区卫生服务中心', '方松街道社区卫生服务中心', '泗泾街道社区卫生服务中心', '车墩街道社区卫生服务中心', '永丰街道社区卫生服务中心', '中山街道社区卫生服务中心', '洞泾镇社区卫生服务中心', '佘山镇社区卫生服务中心分中心', '石湖荡镇社区卫生服务中心', '泖港镇社区卫生服务中心', '新浜镇社区卫生服务中心', '小昆山镇社区卫生服务中心', '叶榭镇社区卫生服务中心', '吴泾社区卫生服务中心', '马桥社区卫生服务中心', '华漕社区卫生服务中心', '浦江社区卫生服务中心', '颛桥社区卫生服务中心', '梅陇社区卫生服务中心', '古美社区卫生服务中心', '七宝社区卫生服务中心', '龙柏社区卫生服务中心', '虹桥社区卫生服务中心', '新虹社区卫生服务中心', '莘庄社区卫生服务中心', '江川社区卫生服务中心', '枫林街道社区卫生服务中心', '虹梅街道社区卫生服务中心', '田林街道社区卫生服务中心', '凌云街道社区卫生服务中心', '斜土街道社区卫生服务中心', '龙华街道社区卫生服务中心', '天平街道社区卫生服务中心', '康健街道社区卫生服务中心', '漕河泾街道社区卫生服务中心', '徐家汇街道社区卫生服务中心', '华泾镇社区卫生服务中心', '长桥街道社区卫生服务中心', '上海市白茅岭医院', '上海市军天湖医院']
                    l_text.pop(0)
                    # print(l_text)
                    for i in range(len(l_text)):
                        if l_text[i] == varCommunity:
                            Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(i + 1) + "]" , 2)  # 选择用户属性
                            break
                    Web_PO.clickXpath("//td[@class='el-table_1_column_7 is-center role-edit-row']/div/button[2]", 2)  # 保存
                else:
                    # pass
                    Web_PO.clickXpath("//td[@class='el-table_1_column_6 is-center role-edit-row']/div/button[2]", 2)  # 保存
                print("[已增加] => " + varAccount + ", " + varNickName + ", " + varPhone + ", " + varAttr)
            else:
                print("[已存在] => " + varAccount)
        except:
            exit()
    def sys_user_edit(self, varAccountOld, varAccount, varNickName, varPhone, varAttr):

        '''系统管理 - 用户管理 - 编辑'''
        try:
            self.Color_PO.consoleColor("31", "31", "\n[编辑用户]", "")
            varResult = self.sys_user_search("用户名", varAccountOld)  # 依据用户名搜索
            if varResult == True :
                Web_PO.clickXpath("//td[@class='el-table_1_column_6 is-center role-edit-row']/div/button[2]", 2)  # 编辑
                Web_PO.inputXpathClear("//input[@placeholder='用户名']", varAccount)  # 用户名不能重复，且不能是中文
                Web_PO.inputXpathClear("//input[@placeholder='昵称']", varNickName)
                Web_PO.inputXpathClear("//input[@placeholder='手机']", varPhone)
                Web_PO.clickXpath("//td[@class='el-table_1_column_5  ']/div/div/div/div/input", 2)  # 点击 用户属性
                l_text = Web_PO.getXpathsText("//div/div/div/ul/li")
                l_text = self.List_PO.listIntercept(l_text, '1', 0)
                l_text = self.List_PO.listBatchDel(l_text, "")
                for i in range(len(l_text)):
                    if l_text[i] == varAttr:
                        Web_PO.clickXpath("//div[@x-placement='bottom-start']/div/div/ul/li[" + str(i + 1) + "]", 2)  # 选择用户属性
                        break
                Web_PO.clickXpath("//td[@class='el-table_1_column_6 is-center role-edit-row']/div/button[2]", 2)  # 保存
                print("[已编辑] => " + varAccount + ", " + varNickName + ", " + varPhone + ", " + varAttr)
            else:
                print("[未找到] => " + varAccountOld)
        except:
            exit()
    def sys_user_role(self, varAccount, *t_role):

        '''系统管理 - 用户管理 - 角色'''
        try:
            self.Color_PO.consoleColor("31", "31", "\n[角色用户]", "")
            varResult = self.sys_user_search("用户名", varAccount)  # 依据用户名搜索
            if varResult == True :
                Web_PO.clickXpath("//td[@class='el-table_1_column_6 is-center role-edit-row']/div/button[1]", 2)  # 点击 角色
                Web_PO.clickXpath("//div[@class='el-select__tags']/input", 2)  # 选择角色
                x = Web_PO.getXpathsText("//div[@class='el-select-dropdown el-popper is-multiple']/div/div/ul/li")
                # print(x)  # ['社区机构管理员', '家庭医生', 'ai核对管理员', '档案查看管理员', '安全审计员', '测试管理人员']
                Web_PO.clickXpaths("//i[@class='el-tag__close el-icon-close']", 2)
                if len(t_role) == 1:
                    for i in range(len(x)):
                        if x[i] == t_role[0]:
                            Web_PO.clickXpath("//div[@class='el-select-dropdown el-popper is-multiple']/div/div/ul/li[" + str(i+1) + "]", 0)  # 选择 角色
                else:
                    for j in range(len(t_role)):
                        for i in range(len(x)):
                            if x[i] == t_role[j]:
                                Web_PO.clickXpath("//div[@class='el-select-dropdown el-popper is-multiple']/div/div/ul/li[" + str(i + 1) + "]", 0)  # 选择 角色
                Web_PO.clickXpath("//div[@class='el-dialog__footer']/span/button[3]", 2)  # 确认
                print("[已角色] => " + str(t_role))
            else:
                print("[未找到] => " + str(varAccount))
        except:
            exit()
    def sys_user_del(self, varAccount):

        '''系统管理 - 用户管理 - 删除'''

        try:
            self.Color_PO.consoleColor("31", "31", "\n[删除用户]", "")
            varResult = self.sys_user_search("用户名", varAccount)  # 依据用户名搜索
            if varResult == True:
                Web_PO.clickXpath("//td[@class='el-table_1_column_6 is-center role-edit-row']/div/button[3]", 2)  # 删除
                Web_PO.clickXpath("//div[@class='el-message-box']/div[3]/button[2]", 2)  # 二次确定。
                print("[已删除] => " + str(varAccount))
            else:
                print("[未找到] => " + str(varAccount))
        except:
            exit()
    def sys_user_admin_add(self):
        pass
        # if varType == "建档专员":
        #     Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[1]", 2)  # 选择建档专员
        # else:
        #     Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[2]", 2)  # 选择医生
        # Web_PO.clickXpath("//td[@class='el-table_1_column_6  ']/div/div/div/div/input", 2)  # 选择 是否医院人员
        # if varIsThird == "否":
        #     Web_PO.clickXpath("//body/div[3]/div[1]/div[1]/ul/li[1]", 2)  # 选择 否
        # else:
        #     Web_PO.clickXpath("//body/div[3]/div[1]/div[1]/ul/li[2]", 2)  # 选择 是
        # Web_PO.clickXpath("//td[@class='el-table_1_column_7  ']/div/div/div/div/input", 2)  # 选择 所属社区
        #
        # x = Web_PO.getXpathsText("//body/div[4]/div[1]/div[1]/ul/li")  # 遍历社区
        # for i in range(len(x)):
        #     if x[i] == varCommunity:
        #         Web_PO.clickXpath("//body/div[4]/div[1]/div[1]/ul/li[" + str(i + 1) + "]", 2)  # 选择所属社区
        #
        # Web_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/button[2]",
        #                        2)  # 保存
    def sys_user_admin_edit(self, varAccount, varNickName, varPhone, varAttr):

        '''系统管理 - 用户管理 - 编辑'''

        Web_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/button[2]", 2)  # 点击 编辑
        Web_PO.inputXpathClear("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr/td[2]/div/div/div/input", varAccount)
        Web_PO.inputXpathClear("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr/td[3]/div/div/div/input", varNickName)
        Web_PO.inputXpathClear("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr/td[4]/div/div/div/input", varPhone)
        Web_PO.clickXpath("//td[@class='el-table_1_column_5  ']/div/div/div/div/input", 2)  # 选择 建档专员或医生
        if varType2 == "建档专员":
            Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[1]", 2)  # 选择建档专员
        else:
            Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[2]", 2)  # 选择医生
        Web_PO.clickXpath("//td[@class='el-table_1_column_6  ']/div/div/div/div/input", 2)  # 选择 是否医院人员
        if varIsThird == "否":
            Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[1]", 2)  # 选择 否
        else:
            Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[2]", 2)  # 选择 是
        Web_PO.clickXpath("//td[@class='el-table_1_column_7  ']/div/div/div/div/input", 2)  # 选择 所属社区

        # x = Web_PO.getXpathsText("//body/div[5]/div[1]/div[1]/ul/li")
        x = Web_PO.getXpathsText("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li")
        # 遍历社区
        for i in range(len(x)):
            if x[i] == varCommunity:
                Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[" + str(i + 1) + "]", 2)  # 选择所属社区

        Web_PO.clickXpath("//div[@class='el-table__fixed-right']/div[2]/table/tbody/tr/td[8]/div/button[2]", 2)  # 保存


    # def searchField(self, varName):
    #
    #     ''' 查找字段名称,返回找到的数量及字段列表 '''
    #
    #     self.Web_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 定位第一下拉框
    #     self.Web_PO.clickXpath("//div[@class='el-select-dropdown__wrap el-scrollbar__wrap']/ul/li[1]", 2)  # 选择字段名称
    #     self.Web_PO.inputXpath("//input[@placeholder='请输入字段名']", varName)  # 第二输入框输入身高
    #     self.Web_PO.clickXpath("//button[@type='button']", 2)  # 点击查找
    #     # 将查找结果保存到列表[字段名称，更新渠道，设置]
    #     l_result = []
    #     varList = Web_PO.getXpathsText("//table[@class='el-table__body']")
    #     if varList != "error":
    #         x = str(varList[0])
    #         y = x.replace("编辑 ", "").split("\n")
    #         for i in range(len(y)):
    #             l_result.append(y[i].strip(string.digits))
    #         for i in l_result:
    #             if i == '':
    #                 l_result.remove(i)
    #         # print(l_result)  # ['身高', '预检', '停用']
    #         l_result2 = numpy.array_split(l_result, int(len(l_result) / 3))
    #         return l_result2, int(len(l_result)/3)
    #     else:
    #         exit()
    #
    #     # [4, ['体温', '预检', '停用', '体重', '预检', '停用', '体质指数', '预检', '停用', '体育锻炼', '预检', '停用']]
    #
    # def getAllFieldByChannel(self, varChannel):
    #
    #     ''' 获取某更新渠道下所有字段名称的列表 '''
    #
    #     Web_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 定位第一下拉框
    #     Web_PO.clickXpath("//div[@class='el-select-dropdown__wrap el-scrollbar__wrap']/ul/li[2]", 2)  # 选择更新渠道
    #     Web_PO.clickXpath("//input[@placeholder='请选择更新渠道']", 2)  # 定位第二下拉框
    #     if varChannel == "预检":
    #         Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[1]", 2)  # 预检
    #     elif varChannel == "挂号":
    #         Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[2]", 2)  # 挂号
    #     elif varChannel == "诊前":
    #         Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[3]", 2)  # 诊前
    #     elif varChannel == "门诊":
    #         Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[4]", 2)  # 门诊
    #     else:
    #         return []
    #     Web_PO.clickXpath("//button[@type='button']", 2)  # 点击查找
    #     # 将所有字段名称保存到列表
    #     l_AllField = []
    #     varList = Web_PO.getXpathsText("//table[@class='el-table__body']")
    #     x = str(varList[0])
    #     y = x.replace("\n", "").replace("编辑 启用", "").replace("编辑 停用", "").split(varChannel)
    #     for i in range(len(y) - 1):
    #         l_AllField.append(y[i].strip(string.digits))
    #     # print(l_fieldName)  # ['姓名', '现住址', '户籍地址', '联系电话', '联系人姓名', '联系人电话']
    #
    #     return l_AllField,len(y)-1
    #
    # def getFieldSetupByChannel(self, varChannel):
    #
    #     ''' 获取某更新渠道下所有字段名称、渠道的列表 '''
    #
    #     Web_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 定位第一下拉框
    #     Web_PO.clickXpath("//div[@class='el-select-dropdown__wrap el-scrollbar__wrap']/ul/li[2]", 2)  # 选择更新渠道
    #     Web_PO.clickXpath("//input[@placeholder='请选择更新渠道']", 2)  # 定位第二下拉框
    #     if varChannel == "预检":
    #         Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[1]", 2)  # 预检
    #     elif varChannel == "挂号":
    #         Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[2]", 2)  # 挂号
    #     elif varChannel == "诊前":
    #         Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[3]", 2)  # 诊前
    #     elif varChannel == "门诊":
    #         Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[4]", 2)  # 门诊
    #     else:
    #         return []
    #     Web_PO.clickXpath("//button[@type='button']", 2)  # 点击查找
    #     list2 = []
    #     varList = Web_PO.getXpathsText("//table[@class='el-table__body']")
    #     x = str(varList[0])
    #     z = x.replace("启用\n", "启用??").replace("停用\n", "停用??").replace("\n" + varChannel + "\n编辑", "").split("??")
    #     for i in range(0, len(z)):
    #         remove_digits = str.maketrans('', '', digits)  # 去掉数字编号
    #         d = z[i].translate(remove_digits).replace("\n", "").split(" ")  # 去掉数字编号
    #         list2.append(d[0])
    #         list2.append(d[1])
    #     d_fieldstatus = {}
    #     if len(list2) % 2 == 0:
    #         for i in range(0, len(list2), 2):
    #             d_fieldstatus.update({list2[i]: list2[i + 1]})
    #         # print(d_fieldstatus)  # {'姓名': '启用', '现住址': '启用', '户籍地址': '启用', '联系电话': '启用', '联系人姓名': '启用', '联系人电话': '启用'}
    #     return len(z),d_fieldstatus
    #
    # def updateChannel(self, varChannel, varFieldName, varToChannel, l_FieldName):
    #
    #     ''' # 遍历编辑更新渠道 ，如 将联系电话 的 挂号 改为 诊前 '''
    #
    #     # 先判断 l_FieldName 中是否有 varFieldName
    #     if (varFieldName not in l_FieldName):
    #         print("error，" + str(l_FieldName) + "中没有找到‘" +  str(varFieldName) + "’字段，程序中断！")
    #         exit()
    #
    #     if varChannel == "预检":
    #         if varToChannel == '诊前':
    #             varU = '2'
    #         else:
    #             return []
    #     elif varChannel == "挂号":
    #         if varToChannel == '预检':
    #             varU = '1'
    #         elif varToChannel == '诊前':
    #             varU = '3'
    #         else:
    #             return []
    #     elif varChannel == "诊前":
    #         if varToChannel == '预检':
    #             varU = '1'
    #         else:
    #             return []
    #     elif varChannel == "门诊":
    #         if varToChannel == '预检':
    #             varU = '1'
    #         elif varToChannel == '诊前':
    #             varU = '2'
    #         else:
    #             return []
    #     else:
    #         return []
    #
    #     Web_PO.clickXpathsNum("//tr[@class='el-table__row']/td[4]/div/button[1]", l_FieldName.index(varFieldName) + 1, 2)  # 编辑
    #     Web_PO.clickXpathsNum("//input[@placeholder='请选择']", 2, 2)  # 定位 更新渠道
    #     Web_PO.clickXpath("//body//div[4]/div/div[1]/ul/li[" + varU + "]", 2)  # 选择 诊前
    #     Web_PO.clickXpathsNum("//tr[@class='el-table__row']/td[4]/div/button[2]", l_FieldName.index(varFieldName) + 1, 2)  # 保存
    #
    #     # 检查更新渠道转移后是否更新成功，如将 联系电话 转移到 诊前
    #     Web_PO.clickXpath("//input[@placeholder='请选择更新渠道']", 2)  # 定位第二下拉框
    #     if varToChannel == "预检":
    #         varU1 = '1'
    #     elif varToChannel == "挂号":
    #         varU1 = '2'
    #     elif varToChannel == "诊前":
    #         varU1 = '3'
    #     elif varToChannel == "门诊":
    #         varU1 = '4'
    #     Web_PO.clickXpath("//body//div[3]/div/div[1]/ul/li[" + varU1 + "]", 2)  # 选择 更新渠道
    #     Web_PO.clickXpath("//button[@type='button']", 2)  # 点击查找
    #
    #     # # 遍历所有诊前字段名称保存到列表
    #     l_fieldname = []
    #     varList = Web_PO.getXpathsText("//table[@class='el-table__body']")
    #     x = str(varList[0])
    #     y = x.replace("\n", "").replace("编辑 启用", "").replace("编辑 停用", "").split(varToChannel)
    #     for i in range(len(y) - 1):
    #         l_fieldname.append(y[i].strip(string.digits))
    #     # print(l_fieldname)  # ['姓名', '现住址', '户籍地址', '联系电话', '联系人姓名', '联系人电话']
    #     return l_fieldname
    #
    # def getAllFieldStatus(self, varChannel):
    #
    #     ''' 将某个更新渠道中所有字段及状态（启用或停用）保存到字典 ，如 {'姓名': '启用', '现住址': '启用'}'''
    #
    #     list2 = []
    #     varList = Web_PO.getXpathsText("//table[@class='el-table__body']")
    #     x = str(varList[0])
    #     z = x.replace("启用\n", "启用??").replace("停用\n", "停用??").replace("\n" + varChannel + "\n编辑", "").split("??")
    #     for i in range(0, len(z)):
    #         remove_digits = str.maketrans('', '', digits)     # 去掉数字编号
    #         d = z[i].translate(remove_digits).replace("\n", "").split(" ")   # 去掉数字编号
    #         list2.append(d[0])
    #         list2.append(d[1])
    #     d_AllFieldStatus = {}
    #     if len(list2) % 2 == 0:
    #         for i in range(0, len(list2), 2):
    #             d_AllFieldStatus.update({list2[i]:list2[i+1]})
    #         return (d_AllFieldStatus)   # {'姓名': '启用', '现住址': '启用', '户籍地址': '启用', '联系电话': '启用', '联系人姓名': '启用', '联系人电话': '启用'}
    #     else:
    #         exit()
    #
    # def setSingleFieldStatus(self, d_AllFieldStatus,varFieldName,varStatus,l_fieldName):
    #
    #     ''' 遍历所有字段，对指定字段设置启用或停用'''
    #     # self.setSingleFieldStatus(d_AllFieldStatus, "户籍地址", "停用", l_AllField)
    #     for key in d_AllFieldStatus:
    #         if key == varFieldName and d_AllFieldStatus[key] != varStatus:
    #             Web_PO.clickXpathsNum("//tr[@class='el-table__row']/td[4]/div/button[2]", l_fieldName.index(varFieldName) + 1, 2)
    #
    #     print("[OK] 已" + varStatus + varFieldName)
    #
    # def setAllFieldStatus(self, varStatus):
    #
    #     ''' 遍历所有字段，设置所有字段全部 启用或停用'''
    #     # self.setAllFieldStatus("启用")
    #     x = Web_PO.getXpathsText("//tr[@class='el-table__row']/td[4]/div/button[2]/span")
    #     for i in range(len(x)):
    #         if x[i] != varStatus:
    #             Web_PO.clickXpathsNum("//tr[@class='el-table__row']/td[4]/div/button[2]", i+1, 2)
    #     print("[OK] 已" + varStatus + "所有字段")
    #
    # def ruleManage_getRuleList(self):
    #
    #     ''' 规则管理 - 获取规则列表（包括编号、规则名称、状态）'''
    #     l_rule = []
    #     l_tmp = Web_PO.getXpathsText("//tr")
    #     l_tmp = [''.join([i.strip() for i in price.strip().replace("\n", ", ")]) for price in l_tmp]
    #     for i in range(len(l_tmp)):
    #         if l_tmp[i] != '操作' and l_tmp[i] != '编辑停用' and l_tmp[i] != '编辑使用' and l_tmp[i] != '编号规则名称':
    #             l_rule.append(l_tmp[i])
    #     # print(l_rule)
    #     l_status = Web_PO.getXpathsText("//div[@class='el-table__fixed-body-wrapper']/table/tbody/tr")
    #     l_status = [''.join([i.strip() for i in price.strip().replace("编辑", "")]) for price in l_status]
    #     # print(l_status)
    #     l_merge = []
    #     for i in range(len(l_rule)):
    #         x = str(l_status[i]) + " => " + str(l_rule[i])
    #         l_merge.append(x)
    #         x = ""
    #     return(l_merge)

    def user_printList(self,varPage):

        ''' 用户管理 - 输出某一页的用户列表（包括编号、用户名、昵称、手机、用户类型、是否医院人员、所属社区）'''
        Web_PO.script('document.querySelector("input[type=number]").value="";', 2)  # js方式清空输入框
        Web_PO.inputXpathClearEnter("//input[@type='number']", varPage)
        l_user = []
        l_tmp = []
        l_tmp = Web_PO.getXpathsText("//tr")
        l_tmp = [''.join([i.strip() for i in price.strip().replace("\n", ", ")]) for price in l_tmp]
        varPage = str(varPage) + " - "
        for i in range(len(l_tmp)):
            if l_tmp[i] != '编号用户名昵称手机用户类型是否医院人员所属社区' and l_tmp[i] != '操作' and l_tmp[i] != '角色编辑删除':
                c = varPage + l_tmp[i]
                l_user.append(c)

        for i in range(len(l_user)):
            print(l_user[i])





    # def permission_printList(self, varPage):
    #
    #     ''' 权限管理 - 输出某一页的权限列表（包括编号、菜单名称、权限值、路径、是否显示、模块、状态、图标、所属系统、所属上级）'''
    #     Web_PO.script('document.querySelector("input[type=number]").value="";', 2)  # js方式清空输入框
    #     Web_PO.inputXpathClearEnter("//input[@type='number']", varPage)
    #     l_permission = []
    #     l_tmp = []
    #     l_tmp = Web_PO.getXpathsText("//tr")
    #     l_tmp = [''.join([i.strip() for i in price.strip().replace("\n", ", ")]) for price in l_tmp]
    #     varPage = str(varPage) + " - "
    #     for i in range(len(l_tmp)):
    #         if l_tmp[i] != '编号菜单名称权限值路径是否显示模块状态图标所属系统所属上级' and l_tmp[i] != '编辑删除' and l_tmp[i] != '操作':
    #             c = varPage + l_tmp[i]
    #             l_permission.append(c)
    #     for i in range(len(l_permission)):
    #         print(l_permission[i])
    #     print("\n")
    #
    # def permission_addMenu(self, varMenu, varPower, varPath, varIsShow, varModel, varStatus, varIcon, varSystem, varLead):
    #
    #     '''权限管理 - 新增菜单'''
    #
    #     Web_PO.clickXpath("//button[@class='el-button el-button--success el-button--mini']", 2)  # 点击 新增
    #     Web_PO.inputXpath("//input[@placeholder='菜单名称']", varMenu)  # 用户名不能重复，且不能是中文
    #     Web_PO.inputXpath("//input[@placeholder='权限值']", varPower)
    #     Web_PO.inputXpath("//input[@placeholder='路径']", varPath)
    #
    #     Web_PO.clickXpath("//td[@class='el-table_1_column_5  ']/div/div/div/div/input", 2)  # 选择 是否显示
    #     if varIsShow == "展示":
    #         Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[1]", 2)  # 选择 展示
    #     else:
    #         Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[2]", 2)  # 选择 隐藏
    #
    #     Web_PO.inputXpath("//input[@placeholder='模块']", varModel)
    #
    #     Web_PO.clickXpath("//td[@class='el-table_1_column_7  ']/div/div/div/div/input", 2)  # 选择 状态
    #     if varStatus == "禁止":
    #         Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[1]", 2)  # 选择 禁止
    #     else:
    #         Web_PO.clickXpath("//div[@x-placement='bottom-start']/div[1]/div[1]/ul/li[2]", 2)  # 选择 正常
    #
    #     Web_PO.inputXpath("//input[@placeholder='图标']", varIcon)
    #     Web_PO.inputXpath("//input[@placeholder='所属系统']", varSystem)
    #     Web_PO.inputXpathClear("//input[@placeholder='所属上级']", varLead)
    #     Web_PO.clickXpath("//td[@class='el-table_1_column_11 is-center ']/div/button[2]", 2)  # 保存