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
        '''  质控结果分析 - 家庭医生 '''

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
            # Web_PO.clickXpath("//form[@class='el-form login-form el-form--inline']/div[2]/div/button[2]", 2)  # 重置
            Web_PO.clickXpath("//form[@class='el-form login-form el-form--inline']/div[1]/div/div/div/div/div/input", 2)  # 请选择
            if varType == '用户名':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[1]", 2)  # 用户名
            elif varType == '昵称':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[2]", 2)  # 昵称
            elif varType == '手机':
                Web_PO.clickXpath("//body/div[2]/div[1]/div[1]/ul/li[3]", 2)  # 手机
            else:
                exit()
            Web_PO.clickXpath("//form[@class='el-form login-form el-form--inline']/div[2]/div/button[2]", 2)  # 重置
            Web_PO.inputXpathClear("//input[@placeholder='请输入搜索内容']", varValue)  # 输入搜索内容
            Web_PO.clickXpath("//form[@class='el-form login-form el-form--inline']/div[2]/div/button[1]", 2)  # 查找

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
                Web_PO.clickXpath("//button[@class='el-button el-button--success el-button--mini']", 2)  # 新增
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
                Web_PO.clickXpath("//div[@class='el-select__tags']/input", 2)  # 点击下拉框
                x = Web_PO.getXpathsText("//div[@class='el-select-dropdown el-popper is-multiple']/div/div/ul/li")
                # print(x)  # # 角色：['社区管理员', '家庭医生', '区级管理员', '规则和指标强度管理', '系统管理模块权限', '数据评测质量分析']
                # 清空原有的角色
                if Web_PO.isElementXpath("//i[@class='el-tag__close el-icon-close']"):
                    Web_PO.clickXpaths("//i[@class='el-tag__close el-icon-close']", 2)
                if len(t_role) == 0:
                    Web_PO.clickXpath("//div[@class='el-select__tags']/input", 2)  # 点击下拉框
                    Web_PO.clickXpath("//div[@class='el-dialog__footer']/span/button[3]", 2)  # 确认
                    Color_PO.consoleColor("31", "36", "[OK] 已清空角色", "")
                else:
                    for j in range(len(t_role)):
                        for i in range(len(x)):
                            if x[i] == t_role[j]:
                                Web_PO.clickXpath("//div[@class='el-select-dropdown el-popper is-multiple']/div/div/ul/li[" + str(i + 1) + "]", 0)  # 选择 角色
                    Web_PO.clickXpath("//div[@class='el-dialog__footer']/span/button[3]", 2)  # 确认
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
            Web_PO.clickXpath("//form[@class='el-form login-form el-form--inline']/div[1]/div/div/div/div/div/input", 2)  # 请选择
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
            Web_PO.clickXpath("//form[@class='el-form login-form el-form--inline']/div[2]/div/button[1]", 2)  # 查找

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
                Web_PO.clickXpath("//button[@class='el-button el-button--success el-button--mini']", 2)  # 点击 新增
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
                for i in range(len(l_result)):
                    if l_result[i][1] == varMenu:
                        Web_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[2]/table/tbody/tr[' + str(i+1) + ']/td[15]/div/button[2]', 2)  # 删除
                        Web_PO.clickXpath('/html/body/div[3]/div/div[3]/button[2]/span', 2)  # 二次确定。
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
            # Web_PO.clickXpath("//form[@class='el-form login-form el-form--inline']/div[2]/div/button[2]", 2)  # 重置
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

                            Color_PO.consoleColor("31", "36","[OK] 编辑名称（" + varNameOld + "）信息后：" + str(varName) + ", " + str(varTitle) + ", " + str(varInfo) + ", " + str(varSort), "")
                        else:
                            Color_PO.consoleColor("31", "33", "[WARNING]", "名称（" + str(varNameOld) + "）未找到，无法编辑！")
        except:
            exit()










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
            self.Color_PO.consoleColor("31", "31", "\n[质控项目汇总 - " + str(varIdCard) + "（" + varPatient + ")]", "")
            self.Color_PO.consoleColor("31", "33", "\n[健康档案封面]", "")
            l_text = Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
            l_cover = l_text[0].split("健康档案封面\n")[1].split("\n个人基本信息表")[0]
            l_cover = l_cover.split('\n')
            # print(l_cover)
            # 格式化 健康档案封面
            l_cover_format = []
            for i in range(len(l_cover)):
                if i < len(l_cover):
                    if ":" in l_cover[i] and "（" not in l_cover[i + 1]:
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
                    if ":" in l_basic[i] and "（" not in l_basic[i + 1]:
                        l_basic_format.append(l_basic[i] + l_basic[i + 1])
                        l_basic.pop(i + 1)
                    else:
                        l_basic_format.append(l_basic[i])
            print(l_basic_format.pop(0))  # 问题数：19
            d_basic_format = self.List_PO.list2dictBySerial(l_basic_format)
            for k in d_basic_format:
                print(k, d_basic_format[k])
        except:
            self.Color_PO.consoleColor("31", "31", "[ERROR]", "身份证号（" + str(varIdCard) + "）有误，请检查！")
    def qcAnalysis_problem_page(self, varPageNum):

        ''' 档案质控分析 - 问题档案列表 - 翻页 '''

        Web_PO.scrollIntoView("//input[@placeholder='请选择']", 2)
        Web_PO.inputXpathClearEnter("//div[@class='block']/div[2]/span/div/input", varPageNum)


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




