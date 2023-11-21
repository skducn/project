# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description:  电子健康档案数据监控中心（PC端）EHR对象库
# *****************************************************************

from instance.zyjk.EHR.config.config import *
import string, numpy
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

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHRDC")

from PO.WebPO import *
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

        global globalUser
        globalUser = varUser

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
                    Web_PO.clickXpath("//div[@类与实例='el-scrollbar__view']/ul/li[" + str(l+1) + "]", 2)
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

        s_tmp = Web_PO.getXpathText("//div[@类与实例='content_left']")
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
        '''检查数字取值范围是否超界'''

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

    def openNewLabel(self, varURL):
        Web_PO.openNewLabel(varURL)
        Web_PO.switchLabel(1)  # 切换到新Label

    def testSql(self, varSql):
        # cursor.execute('SELECT * FROM persons WHERE salesrep=%s' %s ('John Doe'))
        l_result = Sqlserver_PO.ExecQuery(varSql)
        return (l_result[0][0])

    def testSql2(self, varSql, varParam):
        # cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
        l_result = Sqlserver_PO.ExecQuery2(varSql, varParam)
        return (l_result[0][0])



    # 质控结果分析功能

    def getDistrictLevel(self):
        ''' 质控结果分析 - 区级'''
        
        strTmp = Web_PO.getXpathText("//div[@类与实例='resident']")

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
        strTmp = Web_PO.getXpathText("//div[@类与实例='contract']")
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
        focusGroup = Web_PO.getXpathText("//div[@类与实例='left_content']")
        sql_focusGroup = self.testSql('SELECT(SELECT SUM(IIF( A15 + A5 + A6 + A7 > 0, 1, 0 )) FROM report_qyyh ) * 100 / ( SELECT COUNT ( 1 ) FROM report_qyyh )')
        Web_PO.assertEqualValue(str(focusGroup), str(sql_focusGroup) + "%", "重点人群占比", "重点人群占比")

        # 签约居民分类之非重点人群
        noFocusGroup = Web_PO.getXpathText("//div[@类与实例='right_content']")
        sql_noFocusGroup = 100 - sql_focusGroup
        Web_PO.assertEqualValue(str(noFocusGroup), str(sql_noFocusGroup) + "%", "非重点人群占比", "非重点人群占比")

        return czrk, sql_jdl, jzrq, qyjm, sql_qyl, sql_qywcl, sql_byz, sql_focusGroup, sql_noFocusGroup

    def getCommunity(self):
        ''' 质控结果分析 - 社区'''
        
        print("-" * 50)

        # 辖区常住人口（人）
        strTmp = Web_PO.getXpathText("//div[@类与实例='resident']")
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
        strTmp = Web_PO.getXpathText("//div[@类与实例='contract']")
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
        focusGroup = Web_PO.getXpathText("//div[@类与实例='left_content']")
        sql_focusGroup = self.testSql(
            'SELECT ( SELECT SUM ( IIF ( A15 + A5 + A6 + A7 > 0, 1, 0 )) FROM report_qyyh where  hr_service_code=%s ) * 100 / ( SELECT COUNT ( 1 ) FROM report_qyyh where  hr_service_code=%s)' % (
            "310118001", "310118001"))
        Web_PO.assertEqualValue(str(focusGroup), str(sql_focusGroup) + "%", "重点人群占比", "重点人群占比")

        # 签约居民分类之非重点人群
        noFocusGroup = Web_PO.getXpathText("//div[@类与实例='right_content']")
        sql_noFocusGroup = 100 - sql_focusGroup
        Web_PO.assertEqualValue(str(noFocusGroup), str(sql_noFocusGroup) + "%", "非重点人群占比", "非重点人群占比")

        return czrk, sql_jdl, jzrq, qyjm, sql_qyl, sql_qywcl, sql_byz, sql_focusGroup, sql_noFocusGroup

    def getDoctor(self):
        '''  质控结果分析 - 家庭医生 '''

        strTmp = Web_PO.getXpathText("//div[@类与实例='resident']")

        # 1+1+1签约居民人数（人）
        qyjm = str(strTmp).split("1+1+1签约居民人数（人）\n")[1].split("\n签约机构与档案管理机构不一致人数：")[0]
        sql_qyjm = self.testSql('SELECT count(*) FROM report_qyyh WHERE CZRYBM=%s and org_code=%s' % ('0041', "310118001"))
        Web_PO.assertEqualValue(str(qyjm), str(sql_qyjm), "1+1+1签约居民人数（人）", "1+1+1签约居民人数（人）")

        # 签约机构与档案管理机构不一致人数
        byz = str(strTmp).split("签约机构与档案管理机构不一致人数：")[1].split("人")[0]
        sql_byzrs = self.testSql('select count(*) from report_qyyh where A411=%s and A4=%s and hr_service_code=%s and CZRYBM=%s SELECT count(*) FROM QYYH t1 INNER JOIN HrCover t2 ON t1.ArchiveUnitCode<>t2.ArchiveUnitCode and t2.ArchiveNum=t1.SFZH select count(*) from HrCover r1 INNER JOIN  QYYH r2 on r1.ArchiveUnitCode=r2.ArchiveUnitCode AND r1.ArchiveNum= r2.SFZH' % (1, 1, "310118001", "0041"))
        Web_PO.assertEqualValue(str(byz), str(sql_byzrs), "签约机构与档案管理机构不一致人数", "签约机构与档案管理机构不一致人数")

        # 签约居民分类 - 重点人群
        focusGroup = Web_PO.getXpathText("//div[@类与实例='left_content']")
        sql_focusGroup = self.testSql('select( SELECT SUM ( IIF ( A15 + A5 + A6 + A7 > 0, 1, 0 )) FROM report_qyyh  WHERE CZRYBM=%s and org_code=%s) * 100 / ( SELECT COUNT ( 1 ) FROM report_qyyh WHERE CZRYBM=%s and org_code=%s)' % ("0041", "310118001", "0041", "310118001"))
        Web_PO.assertEqualValue(str(focusGroup), str(sql_focusGroup) + "%", "重点人群占比", "重点人群占比")

        # 签约居民分类 - 非重点人群
        noFocusGroup = Web_PO.getXpathText("//div[@类与实例='right_content']")
        sql_noFocusGroup = 100 - sql_focusGroup
        Web_PO.assertEqualValue(str(noFocusGroup), str(sql_noFocusGroup) + "%", "非重点人群占比", "非重点人群占比")

        return qyjm, byz, sql_focusGroup, sql_noFocusGroup

    def getCommunityNew(self):
        '''  质控结果分析 - (社区)签约居民-新  '''

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


            l_groupDeficiency = (Web_PO.getXpathsText("//div[@类与实例='ellipsis el-popover__reference']"))
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



    # 用户管理（搜索、新增、编辑、角色、删除）

    def sys_userList(self):

        '''用户管理详情页'''

        self.Color_PO.consoleColor("31", "31", "\n[用户列表]", "")
        l_text = Web_PO.getXpathsText("//td/div")
        # print(l_text)
        l_userList = (self.List_PO.listSplitSubList(l_text, 8))
        # print(l_userList)
        l_userList2 = []
        for i in range(len(l_userList)):
            if l_userList[i][0] != "":
                l_userList2.append(l_userList[i])
        for i in range(len(l_userList2)):
            l_userList2[i].pop()
            print(l_userList2[i])

        return l_userList2

    def sys_user_search(self, varType, varValue):
        ''' 系统管理 - 用户管理 - 搜索（用户名、昵称、手机号）'''

        try:
            Web_PO.driver.refresh()
            # Web_PO.clickXpath("//form[@类与实例='el-form login-form el-form--inline']/div[2]/div/button[2]", 2)  # 重置
            Web_PO.clickXpath("//form[@类与实例='el-form login-form el-form--inline']/div[1]/div/div/div/div/div/input", 2)  # 请选择
            if varType == '用户名':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[1]", 2)  # 用户名
            elif varType == '昵称':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[2]", 2)  # 昵称
            elif varType == '手机':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[3]", 2)  # 手机
            else:
                exit()
            Web_PO.clickXpath("//form[@类与实例='el-form login-form el-form--inline']/div[2]/div/button[2]", 2)  # 重置
            Web_PO.inputXpathClear("//input[@placeholder='请输入搜索内容']", varValue)  # 输入搜索内容
            Web_PO.clickXpath("//form[@类与实例='el-form login-form el-form--inline']/div[2]/div/button[1]", 2)  # 查找

            l_text = Web_PO.getXpathsText("//td/div")
            if l_text == None:
                Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "）不存在！")
                return False
            else:
                l_tmp = (self.List_PO.listSplitSubList(l_text, 8))
                l_userList = []
                for i in range(len(l_tmp)):
                    if l_tmp[i] != ['', '', '', '', '', '', '', '角色 编辑 删除']:
                        l_userList.append(l_tmp[i])
                for i in range(len(l_userList)):
                    if varType == '用户名':
                        if l_userList[0][1] == varValue:
                            Color_PO.consoleColor("31", "36", "[OK]", "搜索" + varType + "（" + varValue + "） => " + str(l_userList))
                            return Web_PO.assertTrue(Web_PO.assertEqualTrue(varValue, l_userList[0][1]), "[WARNING] 搜索用户名（" + varValue + "）不存在！")
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "）不存在！")
                            return False
                    elif varType == '昵称':
                        if l_userList[0][2] == varValue:
                            Color_PO.consoleColor("31", "36", "[OK]", "搜索" + varType + "（" + varValue + ") => " + str(l_userList))
                            return Web_PO.assertTrue(Web_PO.assertEqualTrue(varValue, l_userList[0][2]), "[WARNING] 搜索昵称（" + varValue + "）不存在！")
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "）不存在！")
                            return False
                    elif varType == '手机':
                        if l_userList[0][3] == varValue:
                            Color_PO.consoleColor("31", "36", "[OK]", "搜索" + varType + "（" + varValue + "）=> " + str(l_userList))
                            return Web_PO.assertTrue(Web_PO.assertEqualTrue(varValue, l_userList[0][3]), "[WARNING] 搜索手机（" + varValue + "）不存在！")
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "） 不存在！")
                            return False
        except:
            exit()

    def sys_user_add(self, varUser, varNickName, varPhone, varThirdCode, varAttr, varCommunity):
        '''系统管理 - 用户管理 - 增加用户'''

        try:
            # 搜索用户名，如果不存在则新增
            varResult = self.sys_user_search("用户名", varUser)
            if varResult == False:
                Web_PO.clickXpath("//button[@类与实例='el-button el-button--success el-button--mini']", 2)  # 新增
                Web_PO.inputXpath("//input[@placeholder='用户名']", varUser)  # 用户名（用户名不能重复，且不能是中文）
                Web_PO.inputXpath("//input[@placeholder='昵称']", varNickName)  # 昵称
                Web_PO.inputXpath("//input[@placeholder='手机']", varPhone)  # 手机
                Web_PO.inputXpath("//input[@placeholder='第三方用户编码']", varThirdCode)  # 第三方用户编码
                # 用户属性
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/table/tbody/tr/td[6]/div/div/div/div[1]/input', 2)
                l_tmp = Web_PO.getXpathsText("//div/div/div/ul/li")
                l_tmp = self.List_PO.listSplit(l_tmp, '1', 1)
                l_tmp = self.List_PO.listBatchDel(l_tmp, "")
                # print(l_tmp)  # ['家庭医生', '家庭医生助理', '院长', '护士']
                for i in range(len(l_tmp)):
                    if l_tmp[i] == varAttr:
                        Web_PO.clickXpath("/html/body/div[3]/div[1]/div[1]/ul/li[" + str(i+1) + "]/span", 2)  # 选择用户属性
                        break
                # 所属社区
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/table/tbody/tr/td[7]/div/div/div/div[1]/input', 2)
                l_tmp = Web_PO.getXpathsText("//div/div[1]/div[1]/ul/li")
                l_tmp = self.List_PO.listBatchDel(l_tmp, "")
                l_tmp.pop(0)
                l_tmp.pop(0)
                # print(l_text)  # ['上海市青浦区夏阳街道社区卫生服务中心', '上海市青浦区盈浦街道社区卫生服务中心', '上海市青浦区香花桥街道社区卫生服务中心', '上海市青浦区朱家角镇社区卫生服务中心', '上海市青浦区练塘镇社区卫生服务中心', '上海市青浦区金泽镇社区卫生服务中心', '上海市青浦区赵巷镇社区卫生服务中心', '上海市青浦区徐泾镇社区卫生服务中心', '上海市青浦区华新镇社区卫生服务中心', '上海市青浦区重固镇社区卫生服务中心']
                for i in range(len(l_tmp)):
                    if l_tmp[i] == varCommunity:
                        Web_PO.clickXpath("/html/body/div[4]/div[1]/div[1]/ul/li[" + str(i + 1) + "]/span", 2)  # 选择所属社区
                        break
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td[8]/div/button[2]/span', 2)  # 保存

                Color_PO.consoleColor("31", "36", "[OK] 新增用户信息：" + str(varUser) + ", " + str(varNickName) + ", " + str(varPhone) + ", " + str(varThirdCode) + ", " + str(varAttr) + ", " + str(varCommunity), "")
            else:
                Color_PO.consoleColor("31", "33", "[WARNING]", "用户（" + str(varUser) + "）已存在，无法新增！")

        except:
            exit()

    def sys_user_edit(self, varUserOld, varUser, varNickName, varPhone, varThirdCode, varAttr, varCommunity):
        '''系统管理 - 用户管理 - 编辑'''

        try:
            varResult = self.sys_user_search("用户名", varUserOld)  # 搜索用户名
            if varResult == True :
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td[8]/div/button[2]/span', 2)  # 编辑
                Web_PO.inputXpathClear("//input[@placeholder='用户名']", varUser)  # 用户名不能重复，且不能是中文
                Web_PO.inputXpathClear("//input[@placeholder='昵称']", varNickName)
                Web_PO.inputXpathClear("//input[@placeholder='手机']", varPhone)
                Web_PO.inputXpathClear("//input[@placeholder='第三方用户编码']", varThirdCode)
                # 用户属性
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/table/tbody/tr/td[6]/div/div/div/div[1]/input',2)
                l_tmp = Web_PO.getXpathsText("//div/div/div/ul/li")
                l_tmp = self.List_PO.listSplit(l_tmp, '1', 1)
                l_tmp = self.List_PO.listBatchDel(l_tmp, "")
                # print(l_tmp)  # ['家庭医生', '家庭医生助理', '院长', '护士']
                for i in range(len(l_tmp)):
                    if l_tmp[i] == varAttr:
                        Web_PO.clickXpath("/html/body/div[3]/div[1]/div[1]/ul/li[" + str(i + 1) + "]/span", 2)  # 选择用户属性
                        break

                # 所属社区
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/table/tbody/tr/td[7]/div/div/div/div[1]/input',2)
                l_tmp = Web_PO.getXpathsText("//div/div[1]/div[1]/ul/li")
                l_tmp = self.List_PO.listBatchDel(l_tmp, "")
                l_tmp.pop(0)
                l_tmp.pop(0)
                # print(l_text)  # ['上海市青浦区夏阳街道社区卫生服务中心', '上海市青浦区盈浦街道社区卫生服务中心', '上海市青浦区香花桥街道社区卫生服务中心', '上海市青浦区朱家角镇社区卫生服务中心', '上海市青浦区练塘镇社区卫生服务中心', '上海市青浦区金泽镇社区卫生服务中心', '上海市青浦区赵巷镇社区卫生服务中心', '上海市青浦区徐泾镇社区卫生服务中心', '上海市青浦区华新镇社区卫生服务中心', '上海市青浦区重固镇社区卫生服务中心']
                for i in range(len(l_tmp)):
                    if l_tmp[i] == varCommunity:
                        Web_PO.clickXpath("/html/body/div[4]/div[1]/div[1]/ul/li[" + str(i + 1) + "]/span", 2)  # 选择所属社区
                        break
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td[8]/div/button[2]/span',2)  # 保存

                Color_PO.consoleColor("31", "36", "[OK] 编辑用户（" + varUserOld + "）信息后：" + varUser + ", " + varNickName + ", " + varPhone + ", " + varThirdCode + ", " + varAttr + ", " + varCommunity,"")
            else:
                Color_PO.consoleColor("31", "33", "[WARNING]", "用户（" + str(varUserOld) + "）未找到，无法编辑！")                

        except:
            exit()

    def sys_user_role(self, varUser, *t_role):
        '''系统管理 - 用户管理 - 角色'''

        try:
            Web_PO.driver.refresh()
            varResult = self.sys_user_search("用户名", varUser)  # 依据用户名搜索
            if varResult == True :
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td[8]/div/button[1]/span', 2)  # 点击 角色
                Web_PO.clickXpath("//div[@类与实例='el-select__tags']/input", 2)  # 点击下拉框
                x = Web_PO.getXpathsText("//div[@类与实例='el-select-dropdown el-popper is-multiple']/div/div/ul/li")
                # print(x)  # # 角色：['社区管理员', '家庭医生', '区级管理员', '规则和指标强度管理', '系统管理模块权限', '数据评测质量分析']
                # 清空原有的角色
                if Web_PO.isElementXpath("//i[@类与实例='el-tag__close el-icon-close']"):
                    Web_PO.clickXpaths("//i[@类与实例='el-tag__close el-icon-close']", 2)
                if len(t_role) == 0:
                    Web_PO.clickXpath("//div[@类与实例='el-select__tags']/input", 2)  # 点击下拉框
                    Web_PO.clickXpath("//div[@类与实例='el-dialog__footer']/span/button[3]", 2)  # 确认
                    Color_PO.consoleColor("31", "36", "[OK] 已清空角色", "")
                else:
                    for j in range(len(t_role)):
                        for i in range(len(x)):
                            if x[i] == t_role[j]:
                                Web_PO.clickXpath("//div[@类与实例='el-select-dropdown el-popper is-multiple']/div/div/ul/li[" + str(i + 1) + "]", 0)  # 选择 角色
                    Web_PO.clickXpath("//div[@类与实例='el-dialog__footer']/span/button[3]", 2)  # 确认
                    Color_PO.consoleColor("31", "36", "[OK] 已选角色" + str(t_role), "")
        except:
            exit()

    def sys_user_del(self, varUser):
        '''系统管理 - 用户管理 - 删除'''

        try:
            varResult = self.sys_user_search("用户名", varUser)  # 搜索用户名
            if varResult == True:
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td[8]/div/button[3]/span', 2)  # 删除
                Web_PO.clickXpath('/html/body/div[3]/div/div[3]/button[2]/span', 2)  # 二次确定。
                self.Color_PO.consoleColor("31", "36", "[OK] 已删除用户（" + str(varUser) + "）", "")
            else:
                self.Color_PO.consoleColor("31", "33", "[WARNING]", "用户（" + str(varUser) + "）不存在，无法删除！")
        except:
            exit()



    # 权限管理（搜索、新增、编辑、删除）

    def sys_power_search(self, varType, varValue):
        ''' 系统管理 - 权限管理 - 搜索(菜单名称、权限值、路径、模块、位置排序)'''

        try:
            Web_PO.driver.refresh()
            Web_PO.clickXpath("//form[@类与实例='el-form login-form el-form--inline']/div[1]/div/div/div/div/div/input", 2)  # 请选择
            if varType == '菜单名称':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[1]", 2)
            elif varType == '权限值':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[2]", 2)
            elif varType == '路径':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[3]", 2)
            elif varType == '模块':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[4]", 2)
            elif varType == '位置排序':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[5]", 2)
            else:
                exit()
            Web_PO.inputXpathClear("//input[@placeholder='请输入搜索内容']", varValue)  # 输入搜索内容
            Web_PO.clickXpath("//form[@类与实例='el-form login-form el-form--inline']/div[2]/div/button[1]", 2)  # 查找

            l_text = Web_PO.getXpathsText("//td/div")
            # print(l_text)
            if l_text == None:
                Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "）不存在！")
                return False
            else:
                l_tmp = (self.List_PO.listSplitSubList(l_text, 15))
                l_userList = []
                for i in range(len(l_tmp)):
                    if l_tmp[i] != [ '', '', '', '', '', '', '', '', '', '', '', '', '', '', '编辑 删除']:
                        l_userList.append(l_tmp[i])
                for i in range(len(l_userList)):
                    if varType == '菜单名称':
                        if varValue in l_userList[0][1]:
                            Color_PO.consoleColor("31", "36", "[OK]", "搜索" + varType + "（" + varValue + "） => " + str(l_userList))
                            return True, l_userList
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "）不存在！")
                            return False
                    elif varType == '权限值':
                        if varValue in l_userList[0][2]:
                            Color_PO.consoleColor("31", "36", "[OK]", "搜索" + varType + "（" + varValue + "） => " + str(l_userList))
                            return True
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "）不存在！")
                            return False
                    elif varType == '路径':
                        if varValue in l_userList[0][3]:
                            Color_PO.consoleColor("31", "36", "[OK]", "搜索" + varType + "（" + varValue + "） => " + str(l_userList))
                            return True
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "）不存在！")
                            return False
                    elif varType == '模块':
                        if varValue in l_userList[0][5]:
                            Color_PO.consoleColor("31", "36", "[OK]", "搜索" + varType + "（" + varValue + "） => " + str(l_userList))
                            return True
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "）不存在！")
                            return False
                    elif varType == '位置排序':
                        if varValue in l_userList[0][9]:
                            Color_PO.consoleColor("31", "36", "[OK]", "搜索" + varType + "（" + varValue + "） => " + str(l_userList))
                            return True
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "）不存在！")
                            return False

        except:
            exit()

    def sys_power_add(self, varMenu, varPower, varPath, varIsShow, varModel, varStatus, varIsCache, varIcon, varSort, varSuperiors, varType, varSystem):
        '''权限管理 - 增加菜单'''

        try:
            # 搜索用户名，如果不存在则新增
            varResult = self.sys_power_search("菜单名称", varMenu)
            if varResult == False:
                Web_PO.clickXpath("//button[@类与实例='el-button el-button--success el-button--mini']", 2)  # 点击 新增
                Web_PO.inputXpath("//input[@placeholder='菜单名称']", varMenu)  # 不能重复，且不能是中文
                Web_PO.inputXpath("//input[@placeholder='权限值']", varPower)
                Web_PO.inputXpath("//input[@placeholder='路径']", varPath)
                # 是否显示
                # Web_PO.jsXpathReadonly('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/table/tbody/tr[1]/td[5]/div/div/div/div/input',2)
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/table/tbody/tr[1]/td[5]/div/div/div/div/input', 2)
                if varIsShow == "展示":
                    Web_PO.clickXpath("/html/body/div[3]/div[1]/div[1]/ul/li[1]", 2)  # 展示
                else:
                    Web_PO.clickXpath("/html/body/div[3]/div[1]/div[1]/ul/li[2]", 2)  # 隐藏
                Web_PO.inputXpath("//input[@placeholder='模块']", varModel)  # 模块
                # 状态
                # Web_PO.jsXpathReadonly('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/table/tbody/tr[1]/td[7]/div/div/div/div/input',2)
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/table/tbody/tr[1]/td[7]/div/div/div/div/input', 2)
                if varStatus == "禁止":
                    Web_PO.clickXpath("/html/body/div[4]/div[1]/div[1]/ul/li[1]", 2)  # 禁止
                else:
                    Web_PO.clickXpath("/html/body/div[4]/div[1]/div[1]/ul/li[2]", 2)  # 显示
                # 是否缓存
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/table/tbody/tr[1]/td[8]/div/div/div/div/input', 2)
                if varIsCache == "不缓存":
                    Web_PO.clickXpath("/html/body/div[5]/div[1]/div[1]/ul/li[1]", 2)  # 不缓存
                else:
                    Web_PO.clickXpath("/html/body/div[5]/div[1]/div[1]/ul/li[2]", 2)  # 缓存
                Web_PO.inputXpath("//input[@placeholder='图标']", varIcon)  # 图标
                Web_PO.inputXpath("//input[@placeholder='位置排序']", varSort)  # 位置排序
                Web_PO.inputXpathClear("//input[@placeholder='所属上级']", varSuperiors)  # 所属上级
                Web_PO.inputXpath("//input[@placeholder='类型']", varType)  # 类型
                Web_PO.inputXpath("//input[@placeholder='所属系统']", varSystem)

                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr[1]/td[15]/div/button[2]/span', 2)  # 保存

                Color_PO.consoleColor("31", "36", "[OK] 新增菜单信息：" + varMenu + ", " + varPower + ", " + varPath + ", " + varIsShow + ", " + varModel + ", " + varStatus + ", " + varIsCache + ", " + varSort + ", " + varSuperiors + ", " + varType + ", " + varSystem, "")
            else:
                Color_PO.consoleColor("31", "33", "[WARNING]", "菜单名（" + str(varMenu) + "）已存在，无法新增！")

        except:
            exit()

    def sys_power_edit(self, varMenuOld, varMenu, varPower, varPath, varIsShow, varModel, varStatus, varIsCache, varIcon, varSort, varSuperiors, varType, varSystem):
        '''系统管理 - 权限管理 - 编辑'''

        try:
            varResult,l_result = self.sys_power_search("菜单名称", varMenuOld)
            if varResult == True :
                # print(l_result)
                for i in range(len(l_result)):
                    if l_result[i][1] == varMenuOld:
                        Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr[' + str(i+1) + ']/td[15]/div/button[1]', 2)  # 编辑
                        Web_PO.inputXpathClear("//input[@placeholder='菜单名称']", varMenu)  # 不能重复，且不能是中文
                        Web_PO.inputXpathClear("//input[@placeholder='权限值']", varPower)
                        Web_PO.inputXpathClear("//input[@placeholder='路径']", varPath)
                        # 是否显示
                        Web_PO.clickXpath(
                            '//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/table/tbody/tr[1]/td[5]/div/div/div/div/input',
                            2)
                        if varIsShow == "展示":
                            Web_PO.clickXpath("/html/body/div[3]/div[1]/div[1]/ul/li[1]", 2)  # 展示
                        else:
                            Web_PO.clickXpath("/html/body/div[3]/div[1]/div[1]/ul/li[2]", 2)  # 隐藏
                        Web_PO.inputXpath("//input[@placeholder='模块']", varModel)  # 模块
                        # 状态
                        Web_PO.clickXpath(
                            '//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/table/tbody/tr[1]/td[7]/div/div/div/div/input',
                            2)
                        if varStatus == "禁止":
                            Web_PO.clickXpath("/html/body/div[4]/div[1]/div[1]/ul/li[1]", 2)  # 禁止
                        else:
                            Web_PO.clickXpath("/html/body/div[4]/div[1]/div[1]/ul/li[2]", 2)  # 显示
                        # 是否缓存
                        Web_PO.clickXpath(
                            '//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/table/tbody/tr[1]/td[8]/div/div/div/div/input',
                            2)
                        if varIsCache == "不缓存":
                            Web_PO.clickXpath("/html/body/div[5]/div[1]/div[1]/ul/li[1]", 2)  # 不缓存
                        else:
                            Web_PO.clickXpath("/html/body/div[5]/div[1]/div[1]/ul/li[2]", 2)  # 缓存
                        Web_PO.inputXpathClear("//input[@placeholder='图标']", varIcon)  # 图标
                        Web_PO.inputXpathClear("//input[@placeholder='位置排序']", varSort)  # 位置排序
                        Web_PO.inputXpathClear("//input[@placeholder='所属上级']", varSuperiors)  # 所属上级
                        Web_PO.inputXpathClear("//input[@placeholder='类型']", varType)  # 类型
                        Web_PO.inputXpathClear("//input[@placeholder='所属系统']", varSystem)

                        Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td[15]/div/button[2]', 2)  # 保存

                        Color_PO.consoleColor("31", "36",
                                "[OK] 编辑菜单名称（" + varMenuOld + "）信息后：" + varMenu + ", " + varPower + ", " + varPath + ", " + varIsShow + ", " + varModel + ", " + varStatus + ", " + varIsCache + ", " + varSort + ", " + varSuperiors + ", " + varType + ", " + varSystem,
                                  "")
                    else:
                        Color_PO.consoleColor("31", "33", "[WARNING]", "菜单名（" + str(varMenuOld) + "）未找到，无法编辑！")

        except:
            exit()

    def sys_power_del(self, varMenu):
        '''系统管理 - 用户管理 - 删除'''

        try:
            count = 0
            varResult, l_result = self.sys_power_search("菜单名称", varMenu)
            # print(l_result)
            if varResult == True:
                if len(l_result) == 1:
                    Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td[15]/div/button[2]', 2)  # 删除
                    Web_PO.clickXpath('/html/body/div[3]/div/div[3]/button[2]', 2)  # 二次确定。
                else:
                    for i in range(len(l_result)):
                        if l_result[i][1] == varMenu:
                            Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr[' + str(i+1) + ']/td[15]/div/button[2]', 2)  # 删除
                            Web_PO.clickXpath('/html/body/div[3]/div/div[3]/button[2]', 2)  # 二次确定。
                            self.Color_PO.consoleColor("31", "36", "[OK] 已删除菜单名称（" + str(varMenu) + "）", "")
                            exit()
                        count += 1
                    if count > 0 :
                        self.Color_PO.consoleColor("31", "33", "[WARNING]", "菜单名称（" + str(varMenu) + "）不存在，无法删除！")
            else:
                self.Color_PO.consoleColor("31", "33", "[WARNING]", "菜单名称（" + str(varMenu) + "）不存在，无法删除！")
        except:
            exit()


    # 角色管理（搜索、新增、编辑、删除）

    def sys_roleList(self):
        '''角色管理详情页'''

        self.Color_PO.consoleColor("31", "31", "\n[角色列表]", "")
        l_text = Web_PO.getXpathsText("//td/div")
        # print(l_text)
        l_roleList = (self.List_PO.listSplitSubList(l_text, 6))
        # print(l_roleList)
        l_roleList2 = []
        for i in range(len(l_roleList)):
            if l_roleList[i][0] != "":
                l_roleList2.append(l_roleList[i])
        for i in range(len(l_roleList2)):
            l_roleList2[i].pop()
            print(l_roleList2[i])
        print()

        return l_roleList2

    def sys_role_search(self, varType, varValue):
        ''' 系统管理 - 角色管理 - 搜索（名称、标题、描述）'''

        try:
            Web_PO.driver.refresh()
            Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[1]/div/form/div[1]/div/div/div/div/div/input', 2)  # 请选择
            if varType == '名称':
                Web_PO.clickXpath("/html/body/div[2]/div[1]/div[1]/ul/li[1]", 2)  # 名称
            elif varType == '标题':
                Web_PO.clickXpath("/html/body/div[2]/div[1]/div[1]/ul/li[2]", 2)  # 标题
            elif varType == '描述':
                Web_PO.clickXpath("/html/body/div[2]/div[1]/div[1]/ul/li[3]", 2)  # 描述
            else:
                exit()
            # Web_PO.clickXpath("//form[@类与实例='el-form login-form el-form--inline']/div[2]/div/button[2]", 2)  # 重置
            Web_PO.inputXpathClear("//input[@placeholder='请输入搜索内容']", varValue)  # 输入搜索内容
            Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[1]/div/form/div[2]/div/button[1]', 2)  # 查找

            l_text = Web_PO.getXpathsText("//td/div")
            # print(l_text)
            if l_text == None:
                Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "）不存在！")
                return False
            else:
                l_tmp = (self.List_PO.listSplitSubList(l_text, 6))
                l_userList = []
                for i in range(len(l_tmp)):
                    if l_tmp[i] != ['', '', '', '', '', '权限 编辑 删除']:
                        l_userList.append(l_tmp[i])
                for i in range(len(l_userList)):
                    if varType == '名称':
                        if l_userList[0][1] == varValue:
                            Color_PO.consoleColor("31", "36", "[OK]", "搜索" + varType + "（" + varValue + "） => " + str(l_userList))
                            # return Web_PO.assertTrue(Web_PO.assertEqualTrue(varValue, l_userList[0][1]), "[WARNING] 搜索名称（" + varValue + "）不存在！")
                            return True, l_userList
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "）不存在！")
                            return False
                    elif varType == '标题':
                        if l_userList[0][2] == varValue:
                            Color_PO.consoleColor("31", "36", "[OK]", "搜索" + varType + "（" + varValue + ") => " + str(l_userList))
                            return Web_PO.assertTrue(Web_PO.assertEqualTrue(varValue, l_userList[0][2]), "[WARNING] 搜索标题（" + varValue + "）不存在！")
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "）不存在！")
                            return False
                    elif varType == '描述':
                        if l_userList[0][3] == varValue:
                            Color_PO.consoleColor("31", "36", "[OK]", "搜索" + varType + "（" + varValue + "）=> " + str(l_userList))
                            return Web_PO.assertTrue(Web_PO.assertEqualTrue(varValue, l_userList[0][3]), "[WARNING] 搜索描述（" + varValue + "）不存在！")
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "搜索" + varType + "（" + varValue + "） 不存在！")
                            return False
        except:
            exit()

    def sys_role_add(self, varName, varTitle, varInfo, varSort):
        '''系统管理 - 角色管理 - 增加名称'''

        try:
            # 搜索名称，如果不存在则新增
            varResult = self.sys_role_search("名称", varName)
            if varResult == False:
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[1]/div/button/span', 2)  # 新增
                Web_PO.inputXpath("//input[@placeholder='名称']", varName)  # 名称不能重复，且不能是中文
                Web_PO.inputXpath("//input[@placeholder='标题']", varTitle)
                Web_PO.inputXpath("//input[@placeholder='描述']", varInfo)
                Web_PO.inputXpath("//input[@placeholder='排序']", varSort)
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr[1]/td[6]/div/button[2]', 2)  # 保存

                Color_PO.consoleColor("31", "36", "[OK] 新增名称信息：" + str(varName) + ", " + str(varTitle) + ", " + str(varInfo) + ", " + str(varSort), "")
            else:
                Color_PO.consoleColor("31", "33", "[WARNING]", "名称（" + str(varName) + "）已存在，无法新增！")

        except:
            exit()

    def sys_role_edit(self, varMameOld, varName, varTitle, varInfo, varSort):
        '''系统管理 - 角色管理 - 编辑'''

        try:
            varResult, l_result = self.sys_role_search("名称", varMameOld)  # 搜索名称
            if varResult == True:
                for i in range(len(l_result)):
                    if len(l_result) == 1:
                        if l_result[i][1] == varMameOld:
                            Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td[6]/div/button[2]', 2)  # 编辑
                            Web_PO.inputXpathClear("//input[@placeholder='名称']", varName)  # 不能重复，且不能是中文
                            Web_PO.inputXpathClear("//input[@placeholder='标题']", varTitle)
                            Web_PO.inputXpathClear("//input[@placeholder='描述']", varInfo)
                            Web_PO.inputXpathClear("//input[@placeholder='排序']", varSort)
                            Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr[1]/td[6]/div/button[2]',2)  # 保存
                            Color_PO.consoleColor("31", "36", "[OK] 编辑名称（" + varMameOld + "）信息后：" + str(varName) + ", " + str(varTitle) + ", " + str(varInfo) + ", " + str(varSort), "")
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "名称（" + str(varMameOld) + "）未找到，无法编辑！")
                    else:
                        if l_result[i][1] == varMameOld:
                            Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr[' + str(i+1) + ']/td[6]/div/button[2]', 2)  # 编辑
                            Web_PO.inputXpathClear("//input[@placeholder='名称']", varName)  # 不能重复，且不能是中文
                            Web_PO.inputXpathClear("//input[@placeholder='标题']", varTitle)
                            Web_PO.inputXpathClear("//input[@placeholder='描述']", varInfo)
                            Web_PO.inputXpathClear("//input[@placeholder='排序']", varSort)
                            Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr[1]/td[6]/div/button[2]', 2)  # 保存

                            Color_PO.consoleColor("31", "36", "[OK] 编辑名称（" + varMameOld + "）信息后：" + str(varName) + ", " + str(varTitle) + ", " + str(varInfo) + ", " + str(varSort), "")
                        else:
                            Color_PO.consoleColor("31", "33",  "[WARNING]", "名称（" + str(varMameOld) + "）未找到，无法编辑！")
        except:
            exit()

    def sys_role_del(self, varMenu):
        '''系统管理 - 用户管理 - 删除'''

        try:
            count = 0
            varResult, l_result = self.sys_role_search("名称", varMenu)
            print(l_result)
            if varResult == True:
                if len(l_result) == 1:
                    Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td[6]/div/button[3]', 2)  # 删除
                    Web_PO.clickXpath('/html/body/div[3]/div/div[3]/button[2]', 2)  # 二次确定。
                else:
                    for i in range(len(l_result)):
                        if l_result[i][1] == varMenu:
                            Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr[' + str(i+1) + ']/td[6]/div/button[3]', 2)  # 删除
                            Web_PO.clickXpath('/html/body/div[3]/div/div[3]/button[2]', 2)  # 二次确定。
                            self.Color_PO.consoleColor("31", "36", "[OK] 已删除菜单名称（" + str(varMenu) + "）", "")
                            exit()
                        count += 1
                    if count > 0 :
                        self.Color_PO.consoleColor("31", "33", "[WARNING]", "菜单名称（" + str(varMenu) + "）不存在，无法删除！")
            else:
                self.Color_PO.consoleColor("31", "33", "[WARNING]", "菜单名称（" + str(varMenu) + "）不存在，无法删除！")
        except:
            exit()

    def sys_role_power(self, varName, *t_power):
        '''系统管理 - 角色管理 - 权限'''

        try:
            Web_PO.driver.refresh()
            varResult, varValue = self.sys_role_search("名称", varName)  # 搜索名称
            list3 = []
            # print(varResult)
            if varResult == True :
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr/td[6]/div/button[1]', 2)  # 点击 权限
                l_power = Web_PO.getXpathsText('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]')  # 获取权限管理数据
                list2 = str(l_power[0]).split("\n")
                # print(list2) # ['循环质量测评分析', '质控分析报告详情', '质控分析报告（社区）', '质控结果分析', '指标强度管理', '质控规则管理', '数据质量测评分析', '系统管理', '首页']
                # 先清空所有勾选框
                if Web_PO.isElementXpath("//span[@类与实例='el-checkbox__input is-checked']"):
                    Web_PO.clickXpaths("//span[@类与实例='el-checkbox__input is-checked']", 2)
                # 没有权限则直接确认
                if len(t_power) == 0:
                    Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[3]/span/button[3]', 2)  # 确认
                    Color_PO.consoleColor("31", "36", "[OK] 已清空所有权限", "")
                # 勾选参数中的权限项
                else:

                    for i in range(len(t_power)):
                        for j in range(len(list2)):
                            # 主权限中部分子权限
                            if isinstance(t_power[i], list):
                                if list2[j] == t_power[i][0]:
                                    Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div[' + str(j + 1) + ']/div[1]/span[1]', 2)  # 展开主权限
                                    sub_power_total = Web_PO.getXpathsQty('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div['+ str(j + 1) + ']/div[2]/div')  # 获取展开后子权限的数量
                                    # print(sub_power_total)
                                    for l in range(sub_power_total):
                                        for m in range(len(t_power[i])):
                                            web_sub_power = Web_PO.getXpathText('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div[' + str(j + 1) + ']/div[2]/div[' + str(l + 1) + ']/div/span[2]')
                                            # print(web_sub_power)
                                            if web_sub_power == t_power[i][m]:
                                                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div[' + str(j + 1) + ']/div[2]/div[' + str(l+1) + ']/div/label/span/span', 2)  # 点击 子权限
                            # 主权限
                            elif list2[j] == t_power[i]:
                                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div[' + str(j+1) + ']/div/label/span/span', 2)
                    Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[3]/span/button[3]', 2)  # 确认
                    Color_PO.consoleColor("31", "36", "[OK] 已选权限" + str(t_power), "")
        except:
            exit()


    # 日志查询

    def sys_logList(self):
        '''日志查询详情页'''

        self.Color_PO.consoleColor("31", "31", "\n[日志查询列表]", "")
        l_text = Web_PO.getXpathsText("//td/div")
        # print(l_text)
        l_roleList = (self.List_PO.listSplitSubList(l_text, 4))
        # print(l_roleList)
        l_roleList2 = []
        for i in range(len(l_roleList)):
            if l_roleList[i][0] != "":
                l_roleList2.append(l_roleList[i])
        for i in range(len(l_roleList2)):
            # l_roleList2[i].pop()
            print(l_roleList2[i])
        print()

        return l_roleList2

    def sys_log_search(self, *varValue):
        ''' 系统管理 - 日志查询 - 查询账号、记录类型、起始日期'''

        try:
            Web_PO.driver.refresh()
            if len(varValue) == 1:
                Web_PO.inputXpathClear("//input[@placeholder='请输入账号']", varValue[0])  # 输入账号
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[1]/div[4]/div/div/button[1]/span', 2)  #  查询
                l_text = Web_PO.getXpathsText("//td/div")
                l_tmp = (self.List_PO.listSplitSubList(l_text, 4))
                Color_PO.consoleColor("31", "36", "[OK]", "搜索账号（" + str(varValue[0]) + "） => " + str(l_tmp))
            elif len(varValue) == 2:
                Web_PO.inputXpathClear("//input[@placeholder='请输入账号']", varValue[0])  # 输入账号
                Web_PO.inputXpathClear("//input[@placeholder='请输入记录类型']", varValue[1])  # 输入记录类型
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[1]/div[4]/div/div/button[1]/span', 2)  # 查询
                l_text = Web_PO.getXpathsText("//td/div")
                l_tmp = (self.List_PO.listSplitSubList(l_text, 4))
                Color_PO.consoleColor("31", "36", "[OK]", "搜索账号（" + str(varValue[0]) + "）、记录类型（" + str(varValue[1]) + "） => " + str(l_tmp))
            elif len(varValue) == 3:
                Web_PO.inputXpathClear("//input[@placeholder='请输入账号']", varValue[0])  # 输入账号
                Web_PO.inputXpathClear("//input[@placeholder='请输入记录类型']", varValue[1])  # 输入记录类型
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[1]/div[3]/div/input[1]', 2)  # 点击 开始日期-结束日期
                Web_PO.inputXpathClear('/html/body/div[2]/div[1]/div/div[1]/span[1]/span[1]/div/input', varValue[2])  # 输入开始日期
                Web_PO.inputXpathClear('/html/body/div[2]/div[1]/div/div[1]/span[1]/span[2]/div[1]/input', "00:00:00")  # 输入开始时间
                Web_PO.clickXpath('/html/body/div[2]/div[1]/div/div[1]/span[1]/span[2]/div[2]/div[2]/button[2]', 1)  # 确定
                Web_PO.inputXpathClear('/html/body/div[2]/div[1]/div/div[1]/span[3]/span[2]/div[1]/input', "23:59:59")  # 输入开始时间
                Web_PO.clickXpath('/html/body/div[2]/div[1]/div/div[1]/span[3]/span[2]/div[2]/div[2]/button[2]', 1)  # 确定

                Web_PO.clickXpath('/html/body/div[2]/div[2]/button[2]/span', 2)
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[1]/div[4]/div/div/button[1]/span', 2)  # 查询
                l_text = Web_PO.getXpathsText("//td/div")
                if l_text == None:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "搜索账号（" + str(varValue[0]) + "）、记录类型（" + str(varValue[1]) + "）、起始日期（" + str(varValue[2]) + " 至 " + str(varValue[2]) + "） => 无结果！")
                    return False
                else:
                    l_tmp = (self.List_PO.listSplitSubList(l_text, 4))
                    # print(l_tmp)
                    l_tmp2 = []
                    for i in range(len(l_tmp)):
                        if l_tmp[i][0] != "":
                            l_tmp2.append(l_tmp[i])
                    # print(l_tmp2)
                    Color_PO.consoleColor("31", "36", "[OK]", "搜索账号（" + str(varValue[0]) + "）、记录类型（" + str(varValue[1]) + "）、起始日期（" + str(varValue[2]) + " 至 " + str(varValue[2]) + "） => " + str(l_tmp2[0]))
            elif len(varValue) == 4:
                Web_PO.inputXpathClear("//input[@placeholder='请输入账号']", varValue[0])  # 输入账号
                Web_PO.inputXpathClear("//input[@placeholder='请输入记录类型']", varValue[1])  # 输入记录类型
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[1]/div[3]/div/input[1]', 2)  # 点击 开始日期-结束日期
                Web_PO.inputXpath('/html/body/div[2]/div[1]/div/div[1]/span[1]/span[1]/div/input', varValue[2])  # 输入开始日期
                Web_PO.inputXpathClear('/html/body/div[2]/div[1]/div/div[1]/span[1]/span[2]/div[1]/input', "00:00:00")  # 输入开始时间
                Web_PO.inputXpathClear('/html/body/div[2]/div[1]/div/div[1]/span[3]/span[1]/div/input', varValue[3])  # 输入结束日期
                Web_PO.inputXpathClear('/html/body/div[2]/div[1]/div/div[1]/span[3]/span[2]/div[1]/input', "00:00:00")  # 输入开始时间
                Web_PO.clickXpath('/html/body/div[2]/div[2]/button[2]/span', 2)
                Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[1]/div[4]/div/div/button[1]/span', 2)  # 查询
                l_text = Web_PO.getXpathsText("//td/div")
                l_tmp = (self.List_PO.listSplitSubList(l_text, 4))
                l_tmp2 = []
                for i in range(len(l_tmp)):
                    if l_tmp[i][0] != "":
                        l_tmp2.append(l_tmp[i])
                Color_PO.consoleColor("31", "36", "[OK]", "搜索账号（" + str(varValue[0]) + "）、记录类型（" + str(varValue[1]) + "）、起始日期（" + str(varValue[2]) + " 至 " + str(varValue[3]) + "） => " + str(l_tmp2))

        except:
            exit()
