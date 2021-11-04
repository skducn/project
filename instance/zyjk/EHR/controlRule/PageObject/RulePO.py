# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-5-12
# Description: 质控对象库
# 依据：D:\1zy\6 研发二部\1 电子健康档案\2.3.1\V2.3.1开发测试任务.xlsx
# curl -X  GET "http://192.168.0.243:8090/healthRecordRules/rulesEngine/execute/310110193902060067" -H  "accept: */*" -o /dev/null -s
# select * from HrRule r1 inner join HrRuleRecord r2 on r1.RuleId=r2.RuleId where r2.ArchiveNum='%s' AND r1.RuleSql='com.benetech.rules.modules.myrules.traceability.DiabetesVisit3991'
# *****************************************************************

from instance.zyjk.EHR.controlRule.config.config import *

class RulePO(object):

    def __init__(self):
        self.Time_PO = TimePO()
        self.max_row = l_RowCol[0]
        self.l_ruleId = l_ruleId
        self.l_ruleSql = l_ruleSql
        self.l_comment = l_comment
        self.l_isRun = l_isRun
        self.l_exec = l_exec
        self.l_diabetes = l_diabetes
        # self.Log_PO = LogPO(logFile, fmt='%(levelname)s - %(message)s - %(asctime)s')  # 输出日志

    # 1，执行sql文件
    def execSqlFile(self, varSqlFile):
        Sqlserver_PO.execQueryBySQL(File_PO.getLayerPath("./config") + "\\" + varSqlFile)

    # 2，执行SQL命令
    def execQuery(self, varSQL):
        x = Sqlserver_PO.execQuery(varSQL)
        return x

    # 3，执行存储过程
    def execProcedure(self, varProcedureName):
        Sqlserver_PO.ExecProcedure(varProcedureName)

    # 4，执行sql文件
    def execSqlFile1(self, varSqlFile):
        Sqlserver_PO.execQueryBySQL1(File_PO.getLayerPath("./config") + "\\" + varSqlFile)

    # 5, 质控
    def runRule(self, varWay, ruleSql, idCardNo, varMsg):

        count = 0
        # 1） 执行质控
        os.system('curl -X  GET "http://192.168.0.243:8090/healthRecordRules/rulesEngine/execute/' + str(idCardNo) + '" -H  "accept: */*" -o /dev/null -s')
        # 2） 检查结果
        result = self.execQuery("select * from HrRule r1 inner join HrRuleRecord r2 on r1.RuleId=r2.RuleId where r2.ArchiveNum='%s' AND r1.RuleSql='%s'" % (idCardNo, ruleSql))
        if varWay == "":
            # 反向测试
            if len(result) > 0:
                Color_PO.consoleColor("31", "31", "[ERRORRRRRRRRRR]", varMsg)
            else:
                Color_PO.consoleColor("31", "33", "[OK]反", varMsg)
                count +=1
        else:
            # 正向测试
            if len(result) > 0:
                Color_PO.consoleColor("31", "36", "[OK]正", varMsg)
                count += 1
            else:
                Color_PO.consoleColor("31", "31", "[ERRORRRRRRRRRR]", varMsg)

        return count

    # 6, # 判断测试数据（身份证）是否存在？
    def isTestData(self, idCardNo):

        n = self.execQuery("select count(*) from tb_empi_index_root where idCardNo='%s'" % idCardNo)
        if n[0][0] != 1:
            Color_PO.consoleColor("31", "31", "[ERROR]" + " select * from tb_empi_index_root where idCardNo='" + str(idCardNo) +"'", ", 此身份证不存在或重复！")
            exit()


    def getValuesByIdCardNo(self, idCardNo, varTable, l_varFields):
        # 通过身份证获取某表的字段的值
        # x = Rule_PO.getValuesByIdCardNo("31011019371125044X", "tb_dc_htn_visit", ["*"])
        # x = Rule_PO.getValuesByIdCardNo("31011019371125044X", "tb_dc_htn_visit", ["empiGuid", "orgCode"])
        # x = Rule_PO.getValuesByIdCardNo("31011019371125044X", "tb_dc_htn_visit", ["empiGuid", "orgCode", "cardId"])
        # x = Rule_PO.getValuesByIdCardNo("31011019371125044X", "tb_dc_htn_visit", ["empiGuid", "orgCode", "cardId", "name"])
        # x = Rule_PO.getValuesByIdCardNo("31011019371125044X", "tb_dc_htn_visit", ["empiGuid", "orgCode", "cardId", "name", "visitWayValue"])
        try:
            if len(l_varFields) == 1:
                return self.execQuery("SELECT htn.{varFields} FROM {varTable} AS htn inner join tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'".format(varTable=varTable,varFields=l_varFields[0]) % idCardNo)

            elif len(l_varFields) == 2:
                return self.execQuery("SELECT htn.{list1},htn.{list2} FROM {varTable} AS htn inner join tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'".format(varTable=varTable, list1=l_varFields[0], list2=l_varFields[1]) % idCardNo)

            elif len(l_varFields) == 3:
                return self.execQuery("SELECT htn.{list1},htn.{list2},htn.{list3} FROM {varTable} AS htn inner join tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'".format(varTable=varTable, list1=l_varFields[0], list2=l_varFields[1],list3=l_varFields[2]) % idCardNo)

            elif len(l_varFields) == 4:
                return self.execQuery("SELECT htn.{list1},htn.{list2},htn.{list3},htn.{list4} FROM {varTable} AS htn inner join tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'".format(varTable=varTable, list1=l_varFields[0], list2=l_varFields[1], list3=l_varFields[2], list4=l_varFields[3]) % idCardNo)

            elif len(l_varFields) == 5:
                return self.execQuery("SELECT htn.{list1}, htn.{list2}, htn.{list3}, htn.{list4}, htn.{list5} FROM {varTable} AS htn inner join tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'".format(varTable=varTable, list1=l_varFields[0], list2=l_varFields[1], list3=l_varFields[2], list4=l_varFields[3], list5=l_varFields[4]) % idCardNo)
        except:
            print("error, 表或字段错误！")

    # ***************************************************************************************************************************************************************************************************


    # 糖尿病，本次随访管理状态代码 与 XXX未填写 （字符型或日期）
    def dm5(self, ruleId, idCardNo, varTable, varField):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:
                    # 1，检查点
                    if varField == "nextVisiDate" or varField == "sportTime" or varField == "visitDate":
                        orig_fields = self.execQuery("SELECT dm.guid, dm.visitDate FROM tb_dc_dm_visit AS dm inner join tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)

                    # 1，检查点
                    # 检查点1（正向）

                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    self.execQuery("            UPDATE {varTable} SET {varField} = null FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, varField=varField) % idCardNo)

                    count = self.runRule("正向", self.l_ruleSql[0][i], idCardNo, "检查点1（正向），本次随访管理状态代码 = Null，" + self.l_comment[0][i].replace("未填写", "") + " = Null")
                    total = total + count

                    # # 检查点2（正向）
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1 FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    self.execQuery("UPDATE {varTable} SET {varField} = null FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, varField=varField) % idCardNo)
                    count = self.runRule("正向", self.l_ruleSql[0][i], idCardNo, "检查点2（正向），本次随访管理状态代码 = 1，" + self.l_comment[0][i].replace("未填写", "") + " = Null")
                    total = total + count

                    # 检查点3（反向）
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 2 FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    self.execQuery("UPDATE {varTable} SET {varField} = null FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, varField=varField) % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点3（反向），本次随访管理状态代码 = 2，" + self.l_comment[0][i].replace("未填写", "") + " = Null")
                    total = total + count

                    # # 检查点4（反向）
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1 FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    if varField == "nextVisiDate" or varField == "sportTime" or varField == "visitDate":
                        for j in range(len(orig_fields)):
                            self.execQuery("update {varTable} set {varField} =CONVERT(varchar(100), '%s', 20) where guid='%s' and guid in (SELECT htn.guid FROM tb_dc_dm_visit AS htn inner join tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s')".format(varTable=varTable, varField=varField) %(orig_fields[j][1], orig_fields[j][0], idCardNo))
                    else:
                        self.execQuery("UPDATE {varTable} SET {varField} = '1' FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, varField=varField) % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点4（反向），本次随访管理状态代码 = 1，" + self.l_comment[0][i].replace("未填写", "") + " != Null")
                    total = total + count

                    # # 检查点5（反向）
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 2 FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点5（反向），本次随访管理状态代码 = 2，" + self.l_comment[0][i].replace("未填写", "") + " != Null")
                    total = total + count

                    if total == 5:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 随机血糖未填写
    def sql2213(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 1，检查点
                    # 检查点1
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = '1',fastingBloodSugarValue = NULL,fastingBloodSugarOGTTValue = NULL,twoHBloodSugarOGTTValue = NULL,randomBloodSugarValue = NULL FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，空腹血糖、空腹血糖（OGTT)、餐后两小时血糖（OGTT）、随机血糖均为 Null")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = NULL,fastingBloodSugarValue = NULL,fastingBloodSugarOGTTValue = NULL,twoHBloodSugarOGTTValue = NULL,randomBloodSugarValue = NULL FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 、空腹血糖、空腹血糖（OGTT)、餐后两小时血糖（OGTT）、随机血糖均为 Null")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = NULL,fastingBloodSugarValue = 1,fastingBloodSugarOGTTValue = NULL,twoHBloodSugarOGTTValue = NULL,randomBloodSugarValue = NULL FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c3，空腹血糖 = 1，本次随访管理状态代码 、空腹血糖（OGTT)、餐后两小时血糖（OGTT）、随机血糖均为 Null")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = NULL,fastingBloodSugarValue = NULL,fastingBloodSugarOGTTValue = 1,twoHBloodSugarOGTTValue = NULL,randomBloodSugarValue = NULL FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c4，空腹血糖（OGTT) = 1，本次随访管理状态代码 、空腹血糖、餐后两小时血糖（OGTT）、随机血糖均为 Null")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = NULL,fastingBloodSugarValue = NULL,fastingBloodSugarOGTTValue = NULL,twoHBloodSugarOGTTValue = 1,randomBloodSugarValue = NULL FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，餐后两小时血糖（OGTT） = 1，本次随访管理状态代码 、空腹血糖、空腹血糖（OGTT) 、随机血糖均为 Null")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = NULL,fastingBloodSugarValue = NULL,fastingBloodSugarOGTTValue = NULL,twoHBloodSugarOGTTValue = NULL,randomBloodSugarValue = 1 FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，随机血糖 = 1，本次随访管理状态代码 、空腹血糖、空腹血糖（OGTT) 、餐后两小时血糖（OGTT）均为 Null")
                    total = total + count

                    # 检查点7
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 2,fastingBloodSugarValue = NULL,fastingBloodSugarOGTTValue = NULL,twoHBloodSugarOGTTValue = NULL,randomBloodSugarValue = NULL FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo,"c7，本次随访管理状态代码 = 2，空腹血糖、空腹血糖（OGTT)、餐后两小时血糖（OGTT）、随机血糖均为 Null")
                    total = total + count

                    if total == 7:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 日吸烟量未填写
    def sql2156(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 1，检查点（smokingStatusCode 1=从不吸烟，2=过去吸烟已戒烟， 3=吸烟）
                    # 检查点1
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, smokingStatusCode = 1, smokingVolume = null  FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，吸烟状况 = 1，日吸烟量 = Null")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null, smokingStatusCode = 1, smokingVolume = null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = Null，吸烟状况 = 1，日吸烟量 = Null")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, smokingStatusCode = null, smokingVolume = null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，吸烟状况 = Null，日吸烟量 = Null")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null, smokingStatusCode = null, smokingVolume = NULL FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = Null，吸烟状况 = Null，日吸烟量 = Null")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 2, smokingStatusCode = null, smokingVolume = null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 2，吸烟状况 = Null，日吸烟量 = Null")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null, smokingStatusCode = 4, smokingVolume = Null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，吸烟状况 = 3，日吸烟量 = Null")
                    total = total + count

                    # 检查点7
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, smokingStatusCode = 4, smokingVolume = 1 FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c7，本次随访管理状态代码 = 1，吸烟状况 = 4，日吸烟量 = 1")
                    total = total + count


                    if total == 7:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 活动种类未填写
    def sql2120(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, isLawSport=1, sportTypeCode=null  FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，规律活动 = 1，活动种类 = Null")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null, isLawSport=1, sportTypeCode=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = Null，规律活动 = 1，活动种类 = Null")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, isLawSport=null, sportTypeCode=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，规律活动 = Null，活动种类 = Null")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null, isLawSport=null, sportTypeCode=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = Null，规律活动 = Null，活动种类 = Null")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, isLawSport=2, sportTypeCode=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 2，规律活动 = 2，活动种类 = Null")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_dm_visit SET  vistStatusCode = 1, isLawSport=1, sportTypeCode=1 FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，规律活动 = 1，活动种类 = 1")
                    total = total + count

                    # 检查点7
                    self.execQuery("UPDATE tb_dc_dm_visit SET  vistStatusCode = 2, isLawSport=null, sportTypeCode=null  FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c7，本次随访管理状态代码 = 1，规律活动 = null，活动种类 = null")
                    total = total + count


                    if total == 7:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标体质指数未填写
    def sql2151(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, targetWeight=60,BMI='24',targetBMI=null  FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，目标体重 = 60，本次BMI≥24， 目标体质指数= Null")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null, targetWeight=60,BMI='24',targetBMI=null  FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = Null，目标体重 = 60，本次BMI≥24， 目标体质指数= Null")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, targetWeight=60,BMI='24.23',targetBMI=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，目标体重 = 60，本次BMI=24.23， 目标体质指数= Null")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, targetWeight=null, BMI=null, targetBMI=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 1，目标体重 = null，本次BMI = null， 目标体质指数= Null")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, targetWeight=null, BMI='24.23',targetBMI=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 1，目标体重 = null，本次BMI = 24.23， 目标体质指数= Null")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, targetWeight=null, BMI='23',targetBMI=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，目标体重 = null，本次BMI = 23， 目标体质指数= Null")
                    total = total + count

                    # 检查点7
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, targetWeight=null, BMI=null, targetBMI=1  FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c7，本次随访管理状态代码 = 1，目标体重 = null，本次BMI = null， 目标体质指数= 1")
                    total = total + count

                    if total == 7:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标日饮酒量未填写
    def sql2174(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, drinkingFrequencyCode=2,targetDrink=null  FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，本次糖尿病随访表《饮酒频率》 = 2，目标日饮酒量= Null")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = NULL, drinkingFrequencyCode=3, targetDrink=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = NULL，本次糖尿病随访表《饮酒频率》 = 3，目标日饮酒量= Null")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, drinkingFrequencyCode=3, targetDrink=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，本次糖尿病随访表《饮酒频率》 = 3，目标日饮酒量= Null")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1 , drinkingFrequencyCode=null, targetDrink=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 1，本次糖尿病随访表《饮酒频率》 = null，目标日饮酒量= Null")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 2, drinkingFrequencyCode=3, targetDrink=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 2，本次糖尿病随访表《饮酒频率》 = 3，目标日饮酒量= Null")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, drinkingFrequencyCode=1,targetDrink=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，本次糖尿病随访表《饮酒频率》 = 1，目标日饮酒量= Null")
                    total = total + count

                    # 检查点7
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, drinkingFrequencyCode=2,targetDrink=1 FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c7，本次随访管理状态代码 = 1，本次糖尿病随访表《饮酒频率》 = 2，目标日饮酒量= 1")
                    total = total + count

                    if total == 7:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标吸烟量未填写
    def sql2164(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, smokingStatusCode=1,targetSmoke=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，本次糖尿病随访表《吸烟状况》 = 1，目标吸烟量= Null")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, smokingStatusCode=2,targetSmoke=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = NULL，本次糖尿病随访表《饮酒频率》 = 3，目标日饮酒量= Null")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, smokingStatusCode=null,targetSmoke=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，本次糖尿病随访表《饮酒频率》 = 3，目标日饮酒量= Null")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null, smokingStatusCode=null,targetSmoke=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 1，本次糖尿病随访表《饮酒频率》 = null，目标日饮酒量= Null")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 2, smokingStatusCode=null,targetSmoke=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 2，本次糖尿病随访表《饮酒频率》 = 3，目标日饮酒量= Null")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, smokingStatusCode=4,targetSmoke=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，本次糖尿病随访表《饮酒频率》 = 1，目标日饮酒量= Null")
                    total = total + count

                    # 检查点7
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, smokingStatusCode=null,targetSmoke=1 FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c7，本次随访管理状态代码 = 1，本次糖尿病随访表《饮酒频率》 = 2，目标日饮酒量= 1")
                    total = total + count

                    if total == 7:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标每周运动次数未填写
    def sql2181(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1,sportFrequence=0,targetSportFrequencyCode=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，本次糖尿病随访表《每周运动次数》 = 0，目标每周运动次数= Null")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, sportFrequence=null,targetSportFrequencyCode=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = 1，本次糖尿病随访表《每周运动次数》 = null，目标每周运动次数= Null")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null, sportFrequence=null,targetSportFrequencyCode=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = null，本次糖尿病随访表《每周运动次数》 = null，目标每周运动次数= Null")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 2, sportFrequence=null,targetSportFrequencyCode=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 2，本次糖尿病随访表《每周运动次数》 =null，目标每周运动次数= Null")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, sportFrequence=2,targetSportFrequencyCode=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 1，本次糖尿病随访表《每周运动次数》 = 2，目标每周运动次数= Null")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, sportFrequence=null,targetSportFrequencyCode=1 FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，本次糖尿病随访表《每周运动次数》 =null，目标每周运动次数= 1")
                    total = total + count



                    if total == 6:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标每次运动时间未填写
    def sql2190(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1,sportTimes=0,targetSportTimes=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，本次糖尿病随访表《每次运动时间》 = 0，目标每次运动时间 = Null")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null, sportTimes=0,targetSportTimes=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = null，本次糖尿病随访表《每次运动时间》 = 0，目标每次运动时间 = Null")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, sportTimes=null, targetSportTimes=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，本次糖尿病随访表《每次运动时间》 = null，目标每次运动时间 = Null")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 2, sportTimes=0, targetSportTimes=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 2，本次糖尿病随访表《每次运动时间》 = 0，目标每次运动时间 = Null")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, sportTimes=1, targetSportTimes=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 1，本次糖尿病随访表《每次运动时间》 = 1，目标每次运动时间 = Null")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, sportTimes=null, targetSportTimes=1 FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，本次糖尿病随访表《每次运动时间》 = null，目标每次运动时间 = 1")
                    total = total + count



                    if total == 6:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标体重未填写
    def sql2143(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1,BMI=24,targetWeight=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，本次BMI=24，目标体重 = Null")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null, BMI=24,targetWeight=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = null，本次BMI=24，目标体重 = Null")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1,BMI=25,targetWeight=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，本次BMI=25，目标体重 = Null")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1,BMI=null,targetWeight=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 1，本次BMI = Null，目标体重 = Null")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 2,BMI=null,targetWeight=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 2，本次BMI = Null，目标体重 = Null")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, BMI=23,targetWeight=null FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，本次BMI=23，目标体重 = Null")
                    total = total + count

                    # 检查点7
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1, BMI=24,targetWeight=1 FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，本次BMI=24，目标体重 = 1")
                    total = total + count

                    if total == 7:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 日饮酒量未填写
    def sql1553(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,drinkingFrequencyCode=2,drinkingVolume = NULL FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，饮酒频率=2，日饮酒量 = Null")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = null, drinkingFrequencyCode=2,drinkingVolume = NULL FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = null，饮酒频率=2，日饮酒量 = Null")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = NULL,drinkingFrequencyCode=NULL,drinkingVolume = NULL FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = NULL，饮酒频率=NULL，日饮酒量 = Null")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,drinkingFrequencyCode=1,drinkingVolume = NULL FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 1，饮酒频率=1，日饮酒量 = Null")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,drinkingFrequencyCode=2,drinkingVolume = 1 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 1，饮酒频率=2，日饮酒量 = 1")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 2, drinkingFrequencyCode=2,drinkingVolume = NULL FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 2，饮酒频率=2，日饮酒量 = Null")
                    total = total + count

                    if total == 6:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 日吸烟量未填写
    def sql1541(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,smokingStatusCode = 1,smokingVolume=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，吸烟状况=1，日吸烟量 = Null")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = null, smokingStatusCode = 1,smokingVolume=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = null，吸烟状况=1，日吸烟量 = Null")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,smokingStatusCode = null,smokingVolume=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，吸烟状况=null，日吸烟量 = Null")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,smokingStatusCode = 2,smokingVolume=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 1，吸烟状况=2，日吸烟量 = Null")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,smokingStatusCode = 3,smokingVolume=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 1，吸烟状况=3，日吸烟量 = Null")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 2, smokingStatusCode = 1,smokingVolume=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 2，吸烟状况=1，日吸烟量 = Null")
                    total = total + count

                    # 检查点7
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1,smokingStatusCode = 4,smokingVolume=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c7，本次随访管理状态代码 = 1，吸烟状况=4，日吸烟量 = Null")
                    total = total + count

                    # 检查点8
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,smokingStatusCode = 1,smokingVolume=1 FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.visitOrgCode = cMain.orgCode  AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c8，本次随访管理状态代码 = 1，吸烟状况=1，日吸烟量 = 1")
                    total = total + count

                    if total == 8:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标体质指数未填写
    def sql1532(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,BMI =24.2,targetBMI=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，本次BMI=24.2，目标体质指数 = Null")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = null, BMI =24.2,targetBMI=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = null，吸烟状况=24.2，日吸烟量 = Null")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,BMI =24,targetBMI=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，吸烟状况=24，日吸烟量 = Null")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,BMI =NULL,targetBMI=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 1，吸烟状况=NULL，日吸烟量 = Null")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,BMI =22,targetBMI=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 1，吸烟状况=22，日吸烟量 = Null")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 2, BMI =24.2,targetBMI=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 2，吸烟状况=24.2，日吸烟量 = Null")
                    total = total + count

                    # 检查点7
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1,BMI =24.2,targetBMI=22.3 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c7，本次随访管理状态代码 = 1，吸烟状况=4，日吸烟量 = 22.3")
                    total = total + count

                    if total == 7:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标日饮酒量未填写
    def sql1559(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,drinkingFrequencyCode =2,targetDrink=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，本次高血压随访表《饮酒频率》=2，目标日饮酒量 = NULL")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = null, drinkingFrequencyCode =2,targetDrink=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = null，本次高血压随访表《饮酒频率》=2，目标日饮酒量 = NULL")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,drinkingFrequencyCode =3,targetDrink=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，本次高血压随访表《饮酒频率》=3，目标日饮酒量 = NULL")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,drinkingFrequencyCode =4,targetDrink=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 1，本次高血压随访表《饮酒频率》=4，目标日饮酒量 = NULL")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,drinkingFrequencyCode =NULL,targetDrink=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 1，本次高血压随访表《饮酒频率》=NULL，目标日饮酒量 = NULL")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 2, drinkingFrequencyCode =2,targetDrink=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 2，本次高血压随访表《饮酒频率》=2，目标日饮酒量 = NULL")
                    total = total + count

                    # 检查点7
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1,drinkingFrequencyCode =1,targetDrink=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c7，本次随访管理状态代码 = 1，本次高血压随访表《饮酒频率》=1，目标日饮酒量 = NULL")
                    total = total + count

                    if total == 7:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标摄盐情况未填写
    def sql1583(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,saltUptakeStatus =2,targetSaltUptakeStatus=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，本次高血压随访表《摄盐情况》=2，目标摄盐情况 = NULL")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = null, saltUptakeStatus =2,targetSaltUptakeStatus=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = null，本次高血压随访表《摄盐情况》=2，目标摄盐情况 = NULL")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,saltUptakeStatus =NULL,targetSaltUptakeStatus=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，本次高血压随访表《摄盐情况》=NULL，目标摄盐情况 = NULL")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,saltUptakeStatus =1,targetSaltUptakeStatus=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 1，本次高血压随访表《摄盐情况》=1，目标摄盐情况 = NULL")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 2,saltUptakeStatus =2,targetSaltUptakeStatus=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 1，本次高血压随访表《摄盐情况》=2，目标摄盐情况 = NULL")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1, saltUptakeStatus =2,targetSaltUptakeStatus=1 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，本次高血压随访表《摄盐情况》=2，目标摄盐情况 = 1")
                    total = total + count

                    if total == 6:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标吸烟量未填写
    def sql1549(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,smokingStatusCode =1,targetSmoke=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，本次高血压随访表《吸烟状况》=1，目标吸烟量 = NULL")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1, smokingStatusCode =2,targetSmoke=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = 1，本次高血压随访表《吸烟状况》=2，目标吸烟量 = NULL")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = NULL,smokingStatusCode =2,targetSmoke=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = NULL，本次高血压随访表《吸烟状况》=2，目标吸烟量 = NULL")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,smokingStatusCode =NULL,targetSmoke=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 1，本次高血压随访表《吸烟状况》=NULL，目标吸烟量 = NULL")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 2,smokingStatusCode =NULL,targetSmoke=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 2，本次高血压随访表《吸烟状况》=NULL，目标吸烟量 = 1")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1, smokingStatusCode =3,targetSmoke=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，本次高血压随访表《吸烟状况》=3，目标吸烟量 = 1")
                    total = total + count

                    # 检查点7
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1, smokingStatusCode =1,targetSmoke=1 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c7，本次随访管理状态代码 = 1，本次高血压随访表《吸烟状况》=1，目标吸烟量 = 1")
                    total = total + count

                    if total == 7:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标每周运动次数未填写
    def sql1566(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,sportFrequence =0,targetSportFrequencyCode=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，本次高血压随访表《每周运动次数》=0，目标每周运动次数 = NULL")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = NULL, sportFrequence =0,targetSportFrequencyCode=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = NULL，本次高血压随访表《每周运动次数》=0，目标每周运动次数 = NULL")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = NULL,sportFrequence =NULL,targetSportFrequencyCode=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = NULL，本次高血压随访表《每周运动次数》=NULL，目标每周运动次数 = NULL")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = NULL,sportFrequence =1,targetSportFrequencyCode=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = NULL，本次高血压随访表《每周运动次数》=1，目标每周运动次数 = NULL")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 2,sportFrequence =0,targetSportFrequencyCode=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 2，本次高血压随访表《每周运动次数》=0，目标每周运动次数 = NULL")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,sportFrequence =0,targetSportFrequencyCode=1 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，本次高血压随访表《每周运动次数》=0，目标每周运动次数 = 1")
                    total = total + count


                    if total == 6:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标每次运动时间未填写
    def sql1575(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,sportTime =0,targetSportTimes=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，本次高血压随访表《每次运动时间》=0，目标每次运动时间 = NULL")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = null, sportTime =0,targetSportTimes=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = null，本次高血压随访表《每次运动时间》=0，目标每次运动时间 = NULL")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,sportTime =null,targetSportTimes=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，本次高血压随访表《每次运动时间》=null，目标每次运动时间 = NULL")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 2,sportTime =0,targetSportTimes=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 2，本次高血压随访表《每次运动时间》=0，目标每次运动时间 = NULL")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,sportTime =1,targetSportTimes=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 1，本次高血压随访表《每次运动时间》=1，目标每次运动时间 = NULL")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1, sportTime =0,targetSportTimes=1 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 1，本次高血压随访表《每次运动时间》=0，目标每次运动时间 = 1")
                    total = total + count



                    if total == 6:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 目标体重未填写
    def sql1524(self, ruleId, idCardNo):
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:

                    # 检查点1
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,BMI =24,targetWeight=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c1，本次随访管理状态代码 = 1，本次BMI=24 ，目标体重 = NULL")
                    total = total + count

                    # # 检查点2
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = NULL,BMI =24,targetWeight=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c2，本次随访管理状态代码 = NULL，本次BMI=24 ，目标体重 = NULL")
                    total = total + count

                    # 检查点3
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,BMI =24.2,targetWeight=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c3，本次随访管理状态代码 = 1，本次BMI=24.2 ，目标体重 = NULL")
                    total = total + count

                    # 检查点4
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,BMI =NULL,targetWeight=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "c4，本次随访管理状态代码 = 1，本次BMI=NULL ，目标体重 = NULL")
                    total = total + count

                    # 检查点5
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1,BMI =22.5,targetWeight=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c5，本次随访管理状态代码 = 1，本次BMI=22.2 ，目标体重 = NULL")
                    total = total + count

                    # 检查点6
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 2, BMI =24,targetWeight=null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c6，本次随访管理状态代码 = 2，本次BMI=24 ，目标体重 = NULL")
                    total = total + count

                    # 检查点7
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1, BMI =24,targetWeight=2 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.visitOrgCode = cMain.orgCode  AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode  AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "c7，本次随访管理状态代码 = 1，本次BMI=24 ，目标体重 = 2")
                    total = total + count

                    if total == 7:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()




    def dm10(self, ruleId, idCardNo, hospitalLevel, varField, varValue):
        # 一级医院有检验结果（ACR）3991
        # 二级医院有检验结果（ACR）3990
        # 三级医院有检验结果（ACR）3989
        # 与一级医院实验室检验结果逻辑不符合（总胆固醇）2226
        # 与二级医院实验室检验结果逻辑不符合（总胆固醇）2225
        # 与三级医院实验室检验结果逻辑不符合（总胆固醇）2224
        # 一级医院有检验结果（糖化血红蛋白）3988
        # 二级医院有检验结果（糖化血红蛋白）3987
        # 三级医院有检验结果（糖化血红蛋白）3986

        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m',str(i + 2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i] + ", " + self.l_ruleSql[0][i], '\033[0m')

                try:
                    # 1，数据准备

                    # 初始化数据，测试需要3条记录
                    m = self.execQuery("SELECT count(*) FROM tb_empi_index_root t1 INNER JOIN tb_dc_chronic_info t2 ON t1.guid = t2.empiGuid  INNER JOIN tb_dc_chronic_main t3 ON t2.manageNum = t3.manageNum AND t2.orgCode = t3.orgCode INNER JOIN tb_dc_dm_visit t4 ON t3.visitNum = t4.cardId AND t3.orgCode = t4.orgCode WHERE t1.idCardNo = '%s'" % idCardNo)
                    if m[0][0] == 0:
                        exit()
                    else:
                        # 获取 cardId,orgCode,empiGuid
                        sql = self.execQuery("SELECT top 1 t4.cardId,t4.orgCode,t4.empiGuid FROM tb_empi_index_root t1 INNER JOIN tb_dc_chronic_info t2 ON t1.guid = t2.empiGuid INNER JOIN tb_dc_chronic_main t3 ON t2.manageNum = t3.manageNum AND t2.orgCode = t3.orgCode INNER JOIN tb_dc_dm_visit t4 ON t3.visitNum = t4.cardId AND t3.orgCode = t4.orgCode WHERE t1.idCardNo ='%s'" % idCardNo)
                        if m[0][0] == 2:
                            # 将第一条随访日期修改为 2020-10-1
                            self.execQuery("update tb_dc_dm_visit set visitDate='2020-10-1' where guid='%s'" % sql[0][2])
                            # 新增1条记录，随访日期为 2019-01-16
                            self.execQuery("INSERT INTO tb_dc_dm_visit([guid], [cardId], [name], [ehrNum], [orgCode], [visitDate], [visitWayCode], [visitWayValue], [otherVisit], [visitDocNo], [visitDocName], [visitOrgCode], [visitOrgName], [vistStatusCode], [visitStatusValue], [nextVisiDate], [lostVisitCode], [lostVisitName], [lostVisitDate], [otherLostVIsitName], [deathReason], [targetDistrictCode], [targetDistrictName], [targetOrgCode], [targetOrgName], [moveProvinceCode], [moveProvinceValue], [moveCityCode], [moveCityValue], [moveDistrictCode], [moveDistrictValue], [moveStreetCode], [moveStreetValue], [moveNeighborhoodCode], [moveNeighborhoodValue], [moveVillageValue], [moveHouseNumber], [moveOrgCode], [moveOrgName], [hasPaperCard], [isAcceptHealthEdu], [healthEduType], [clinicalSymptomsCode], [clinicalSymptomsValue], [otherClinicalSymptoms], [symptomStatus], [clinicalInfo], [sbp], [dbp], [height], [weight], [waistline], [hipline], [targetWeight], [BMI], [targetBMI], [dorsalArteryOfFootLeftCode], [dorsalArteryOfFootLeftName], [dorsalArteryOfFootRightCode], [dorsalArteryOfFootRightName], [hypoglycemia], [familyHistory], [isLawSport], [sportTypeCode], [sportTypeName], [sportFrequence], [sportTimes], [dietCode], [dietName], [stapleFood], [targetStapleFood], [smokingVolume], [drinkingVolume], [targetSportFrequencyCode], [targetSportFrequencyName], [targetSportTimes], [smokingStatusCode], [smokingStatusName], [targetSmoke], [quitSmoking], [drinkingFrequencyCode], [drinkingFrequencyName], [targetDrink], [psychologyStatusCode], [psychologyStatusName], [complianceStatusCode], [complianceStatusName], [referralReason], [referralOrgDept], [visitType], [fastingBloodSugarCode], [fastingBloodSugarName], [fastingBloodSugarValue], [fastingBloodSugarGatherCode], [fastingBloodSugarGatherName], [randomBloodSugarCode], [randomBloodSugarName], [randomBloodSugarValue], [randomBloodSugarGatherCode], [randomBloodSugarGatherName], [fastingBloodSugarOGTTCode], [fastingBloodSugarOGTTName], [fastingBloodSugarOGTTValue], [fastingBloodSugarOGTTGatherCode], [fastingBloodSugarOGTTGatherName], [twoHBloodSugarOGTTCode], [twoHBloodSugarOGTTName], [twoHBloodSugarOGTTValue], [twoHBloodSugarOGTTGatherCode], [twoHBloodSugarOGTTGatherName], [hbAlc], [hbAlcDate], [cholesterol], [triglycerides], [highCholesterol], [lowCholesterol], [acr], [urineProtein], [ghGaterWayCode], [ghGaterWayName], [drugComplianceCode], [drugComplianceName], [useDrug], [hasUseDrugSideEffects], [UseDrugSideEffects], [interveneCount], [beforeInterveneDate], [isIntervene], [syndrome], [interveneMeasures], [measuresContent], [otherInterveneMeasures], [otherMeasuresContent], [proposal], [otherProposal], [synStatus], [age], [empiGuid], [isGovernance]) VALUES ('99', '%s', '黄*珍', 'K0616970X', '%s', '2019-01-16 00:00:00.000', NULL, '家庭', NULL, '1015', '李*琳', '310118001', '上海市青浦区夏阳街道社区卫生服务中心', '1', '继续随访', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '4', '30', NULL, NULL, NULL, NULL, '2', NULL, NULL, NULL, NULL, '3', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, '', NULL, '1', NULL, '', NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '%s', '0')" % (sql[0][0],sql[0][1],sql[0][2]))
                        elif m[0][0] == 1:
                            # 新增2条，随访日期分别为 2019-01-16 和 2020-10-1
                            self.execQuery("INSERT INTO tb_dc_dm_visit([guid], [cardId], [name], [ehrNum], [orgCode], [visitDate], [visitWayCode], [visitWayValue], [otherVisit], [visitDocNo], [visitDocName], [visitOrgCode], [visitOrgName], [vistStatusCode], [visitStatusValue], [nextVisiDate], [lostVisitCode], [lostVisitName], [lostVisitDate], [otherLostVIsitName], [deathReason], [targetDistrictCode], [targetDistrictName], [targetOrgCode], [targetOrgName], [moveProvinceCode], [moveProvinceValue], [moveCityCode], [moveCityValue], [moveDistrictCode], [moveDistrictValue], [moveStreetCode], [moveStreetValue], [moveNeighborhoodCode], [moveNeighborhoodValue], [moveVillageValue], [moveHouseNumber], [moveOrgCode], [moveOrgName], [hasPaperCard], [isAcceptHealthEdu], [healthEduType], [clinicalSymptomsCode], [clinicalSymptomsValue], [otherClinicalSymptoms], [symptomStatus], [clinicalInfo], [sbp], [dbp], [height], [weight], [waistline], [hipline], [targetWeight], [BMI], [targetBMI], [dorsalArteryOfFootLeftCode], [dorsalArteryOfFootLeftName], [dorsalArteryOfFootRightCode], [dorsalArteryOfFootRightName], [hypoglycemia], [familyHistory], [isLawSport], [sportTypeCode], [sportTypeName], [sportFrequence], [sportTimes], [dietCode], [dietName], [stapleFood], [targetStapleFood], [smokingVolume], [drinkingVolume], [targetSportFrequencyCode], [targetSportFrequencyName], [targetSportTimes], [smokingStatusCode], [smokingStatusName], [targetSmoke], [quitSmoking], [drinkingFrequencyCode], [drinkingFrequencyName], [targetDrink], [psychologyStatusCode], [psychologyStatusName], [complianceStatusCode], [complianceStatusName], [referralReason], [referralOrgDept], [visitType], [fastingBloodSugarCode], [fastingBloodSugarName], [fastingBloodSugarValue], [fastingBloodSugarGatherCode], [fastingBloodSugarGatherName], [randomBloodSugarCode], [randomBloodSugarName], [randomBloodSugarValue], [randomBloodSugarGatherCode], [randomBloodSugarGatherName], [fastingBloodSugarOGTTCode], [fastingBloodSugarOGTTName], [fastingBloodSugarOGTTValue], [fastingBloodSugarOGTTGatherCode], [fastingBloodSugarOGTTGatherName], [twoHBloodSugarOGTTCode], [twoHBloodSugarOGTTName], [twoHBloodSugarOGTTValue], [twoHBloodSugarOGTTGatherCode], [twoHBloodSugarOGTTGatherName], [hbAlc], [hbAlcDate], [cholesterol], [triglycerides], [highCholesterol], [lowCholesterol], [acr], [urineProtein], [ghGaterWayCode], [ghGaterWayName], [drugComplianceCode], [drugComplianceName], [useDrug], [hasUseDrugSideEffects], [UseDrugSideEffects], [interveneCount], [beforeInterveneDate], [isIntervene], [syndrome], [interveneMeasures], [measuresContent], [otherInterveneMeasures], [otherMeasuresContent], [proposal], [otherProposal], [synStatus], [age], [empiGuid], [isGovernance]) VALUES ('100', '%s', '黄*珍', 'K0616970X', '%s', '2019-01-16 00:00:00.000', NULL, '家庭', NULL, '1015', '李*琳', '310118001', '上海市青浦区夏阳街道社区卫生服务中心', '1', '继续随访', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '4', '30', NULL, NULL, NULL, NULL, '2', NULL, NULL, NULL, NULL, '3', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, '', NULL, '1', NULL, '', NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '%s', '0')" % (sql[0][0],sql[0][1],sql[0][2]))
                            self.execQuery("INSERT INTO tb_dc_dm_visit([guid], [cardId], [name], [ehrNum], [orgCode], [visitDate], [visitWayCode], [visitWayValue], [otherVisit], [visitDocNo], [visitDocName], [visitOrgCode], [visitOrgName], [vistStatusCode], [visitStatusValue], [nextVisiDate], [lostVisitCode], [lostVisitName], [lostVisitDate], [otherLostVIsitName], [deathReason], [targetDistrictCode], [targetDistrictName], [targetOrgCode], [targetOrgName], [moveProvinceCode], [moveProvinceValue], [moveCityCode], [moveCityValue], [moveDistrictCode], [moveDistrictValue], [moveStreetCode], [moveStreetValue], [moveNeighborhoodCode], [moveNeighborhoodValue], [moveVillageValue], [moveHouseNumber], [moveOrgCode], [moveOrgName], [hasPaperCard], [isAcceptHealthEdu], [healthEduType], [clinicalSymptomsCode], [clinicalSymptomsValue], [otherClinicalSymptoms], [symptomStatus], [clinicalInfo], [sbp], [dbp], [height], [weight], [waistline], [hipline], [targetWeight], [BMI], [targetBMI], [dorsalArteryOfFootLeftCode], [dorsalArteryOfFootLeftName], [dorsalArteryOfFootRightCode], [dorsalArteryOfFootRightName], [hypoglycemia], [familyHistory], [isLawSport], [sportTypeCode], [sportTypeName], [sportFrequence], [sportTimes], [dietCode], [dietName], [stapleFood], [targetStapleFood], [smokingVolume], [drinkingVolume], [targetSportFrequencyCode], [targetSportFrequencyName], [targetSportTimes], [smokingStatusCode], [smokingStatusName], [targetSmoke], [quitSmoking], [drinkingFrequencyCode], [drinkingFrequencyName], [targetDrink], [psychologyStatusCode], [psychologyStatusName], [complianceStatusCode], [complianceStatusName], [referralReason], [referralOrgDept], [visitType], [fastingBloodSugarCode], [fastingBloodSugarName], [fastingBloodSugarValue], [fastingBloodSugarGatherCode], [fastingBloodSugarGatherName], [randomBloodSugarCode], [randomBloodSugarName], [randomBloodSugarValue], [randomBloodSugarGatherCode], [randomBloodSugarGatherName], [fastingBloodSugarOGTTCode], [fastingBloodSugarOGTTName], [fastingBloodSugarOGTTValue], [fastingBloodSugarOGTTGatherCode], [fastingBloodSugarOGTTGatherName], [twoHBloodSugarOGTTCode], [twoHBloodSugarOGTTName], [twoHBloodSugarOGTTValue], [twoHBloodSugarOGTTGatherCode], [twoHBloodSugarOGTTGatherName], [hbAlc], [hbAlcDate], [cholesterol], [triglycerides], [highCholesterol], [lowCholesterol], [acr], [urineProtein], [ghGaterWayCode], [ghGaterWayName], [drugComplianceCode], [drugComplianceName], [useDrug], [hasUseDrugSideEffects], [UseDrugSideEffects], [interveneCount], [beforeInterveneDate], [isIntervene], [syndrome], [interveneMeasures], [measuresContent], [otherInterveneMeasures], [otherMeasuresContent], [proposal], [otherProposal], [synStatus], [age], [empiGuid], [isGovernance]) VALUES ('101', '%s', '黄*珍', 'K0616970X', '%s', '2020-10-1 00:00:00.000', NULL, '家庭', NULL, '1015', '李*琳', '310118001', '上海市青浦区夏阳街道社区卫生服务中心', '1', '继续随访', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '4', '30', NULL, NULL, NULL, NULL, '2', NULL, NULL, NULL, NULL, '3', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, '', NULL, '1', NULL, '', NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '%s', '0')" % (sql[0][0],sql[0][1],sql[0][2]))

                    # 初始化数据，随访日期从早到晚依次排列
                    visitDate = self.execQuery("SELECT t4.visitDate FROM tb_empi_index_root t1 INNER JOIN tb_dc_chronic_info t2 ON t1.guid = t2.empiGuid INNER JOIN tb_dc_chronic_main t3 ON t2.manageNum = t3.manageNum AND t2.orgCode = t3.orgCode INNER JOIN tb_dc_dm_visit t4 ON t3.visitNum = t4.cardId AND t3.orgCode = t4.orgCode WHERE t1.idCardNo ='%s'" % idCardNo)
                    l_visitDate = []
                    for j in range(len(visitDate)):
                        l_visitDate.append(str(visitDate[j][0]).split(" ")[0])
                    l_visitDate.sort()
                    # print(l_visitDate)

                    # 初始化表
                    self.execQuery("DELETE FROM tb_lis_report")
                    self.execQuery("DELETE FROM tb_lis_report_indicator")
                    self.execQuery("insert into tb_lis_report(guid,visitStrNo,orgCode,orgName,visitType,reportNo,name,empiGuid,patientId,specimenTypeCodeSystem,specimenTypeCode,specimenTypeName,reportTypeCodeSystem,reportTypeCode,reportTypeName,reportName,applyDeptCode,applyDeptName,applyDoctorCode,applyDoctorName,reportDoctorCode,reportDoctorName,applyDate,reportDate,orderNo,status,createDate,isCurrent) values('1',null,'%s',null,null,'123456',null,'%s',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)" % (sql[0][1], sql[0][2]))
                    self.execQuery("insert into tb_lis_report_indicator(guid,visitStrNo,orgCode,orgName,visitType,reportNo,insItemCode,itemCodeSystem,itemCode,itemName,resultValue,resultUnit,resultFlagCodeSystem,resultFlagCode,resultFlagName,refQuality,refQuantifyLower,refQuantifyUpper,[order],status,createDate,isCurrent,empiGuid) values('1',null,'%s',null,null,'123456',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,'%s')" % (sql[0][1], sql[0][2]))


                    # # 2，检查点
                    # # 检查点1（正向）
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1 FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    self.execQuery("UPDATE tb_dc_dm_visit SET {varField} = null FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varField=varField) % idCardNo)
                    self.execQuery("update t_dic_hospital_info set HospitalLevel='%s' where Hospital_id='%s'" % (hospitalLevel, sql[0][1]))
                    self.execQuery("update tb_lis_report_indicator set itemName='%s'" % varValue)
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))  # # 第一条随访日期的后2天
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点1（正向），本次随访管理状态代码 = 1 ，" + str(varField) + " = Null，医院等级 = " + str(hospitalLevel) + "，项目名称 = " + str(varValue) + "，检验报告日期为第一次随访日期到第二次随访日期之间")
                    total = total + count

                    # # # 检查点2（正向）
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], -2))  # 最近一条随访日期的前2天
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点2（正向），将检查点1中的 检验报告日期为上一次与本次随访日期之间，其余条件不变")
                    total = total + count

                    # # # 检查点3（正向）
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点3（正向），将检查点1中的 本次随访管理状态代码 = Null，其余条件不变")
                    total = total + count

                    # # # 检查点4（正向）
                    self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[-1])
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点4（正向），将检查点1中的检验报告日期等于本次随访日期，其余条件不变")
                    total = total + count

                    # # # 检查点5（反向）
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 2 FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点5（反向），将检查点1中的 本次随访管理状态代码 = 2，其余条件不变")
                    total = total + count

                    # # 检查点6（反向）
                    self.execQuery("UPDATE tb_dc_dm_visit SET {varField} = '123' FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varField=varField) % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点6（反向），将检查点1中的 总胆固醇值 <> Null，其余条件不变")
                    total = total + count

                    # # 检查点7（反向）
                    errorHosptialLevel = int(hospitalLevel) + 1
                    self.execQuery("update t_dic_hospital_info set HospitalLevel='%s' where Hospital_id='%s'" % (errorHosptialLevel, sql[0][1]))
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点7（反向），将检查点1中的 医院级别 = " + str(errorHosptialLevel) + " ，其余条件不变")
                    self.execQuery("update t_dic_hospital_info set HospitalLevel='1' where Hospital_id='%s'" % (sql[0][1]))
                    total = total + count

                    # # 检查点8（反向）
                    self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[0])
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点8（反向），将检查点1中检验报告日期等于第一次随访日期，其余条件不变")
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
                    total = total + count

                    # # 检查点9（反向）
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], -2))
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点9（反向），将检查点1中检验报告日期早于第一次随访日期，其余条件不变")
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
                    total = total + count

                    # # 检查点10（反向）
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], 2))
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点10（反向），将检查点1中检验报告日期晚于本次随访日期，其余条件不变")
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
                    total = total + count

                    if total == 10:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()

                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 药品名称与药物类型不匹配
    def sql3995(self, ruleId, idCardNo):
        # 药品名称与药物类型不匹配

        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')

                try:
                    # 1，数据准备
                    ehrNum = self.execQuery("SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
                    orgCode = self.execQuery("SELECT  top 1 dm.orgCode FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
                    # 从tb_dc_dm_visit获取cardId和 orgCode值，更新到刚才新增的记录对应字段（visit Id，orgCode）中.
                    visitId = self.execQuery("select cardId from tb_dc_dm_visit   where  ehrNum='%s' order by visitDate desc" % ehrNum[0][0])
                    # print(visitId[0][0])
                    self.execQuery("DELETE FROM tb_dc_dm_usedrug")
                    self.execQuery("insert into tb_dc_dm_usedrug(guid,visitId,orgCode,drugTypeCodeSystem,drugTypeCode,drugTypeName,drugCode,drugName,eachDose,referenceDose,unit,totalDose,useWayCodeSystem,useWayCode,useWayName,frequency,cnDrugCodeSystem,cnDrugCode,cnDrugName) values('1','%s','%s',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)" % (visitId[0][0], orgCode[0][0]))

                    # 2，检查点

                    # # 检查点1（反向）
                    count = self.runRule("", self.l_ruleSql[0][i] , idCardNo, "检查点1（反向），药物名称 = Null，药物类型 = Null")
                    total = total + count

                    # 检查点2（反向）
                    self.execQuery("update  tb_dc_dm_usedrug set  drugName='%s'" % '二甲双胍')
                    self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName=Null")
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点2（反向），药物名称 != Null，药物类型 = Null")
                    total = total + count

                    # 检查点3（反向）
                    self.execQuery("update  tb_dc_dm_usedrug set  drugName=Null")
                    self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName='%s'" % '磺脲类')
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点3（反向），药物名称 = Null，药物类型 != Null")
                    total = total + count

                    # 抽样 糖尿病用药列表（只跑2条）
                    # 检查点4（正向）
                    self.execQuery("update  tb_dc_dm_usedrug set  drugName='%s'" % '二甲双胍')
                    self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName='%s'" % '中成药')
                    count = self.runRule("正向", self.l_ruleSql[0][i], idCardNo, "检查点4（正向），药品名称与药物类型匹配不一致")
                    total = total + count

                    # 检查点5（反向）
                    self.execQuery("update  tb_dc_dm_usedrug set  drugName='%s'" % '二甲双胍')
                    self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName='%s'" % '双胍类')
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点5（反向），药品名称与药物类型匹配一致")
                    total = total + count

                    # # 全遍历 糖尿病用药列表（跑 450 条）
                    # l_drugName = self.l_diabetes[0]
                    # l_drugTypeName = self.l_diabetes[1]
                    # dict1 = List_PO.lists2dict(l_drugName, l_drugTypeName)
                    # l_drugTypeNameDelRepeat = List_PO.listDelRepeat(l_drugTypeName)
                    # for i in range(len(l_drugName)):
                    #     for j in range(len(l_drugTypeNameDelRepeat)):
                    #         self.execQuery("update  tb_dc_dm_usedrug set  drugName='%s'" % l_drugName[i])
                    #         self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName='%s'" % l_drugTypeNameDelRepeat[j])
                    #         for k, v in dict1.items():
                    #             youxiao=0
                    #             if k == l_drugName[i] and v == l_drugTypeNameDelRepeat[j]:
                    #                 youxiao=1
                    #                 break
                    #         if youxiao == 1:
                    #             count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点（反向），药品名称【" + l_drugName[i] + "】与药物类型【" + l_drugTypeNameDelRepeat[j] + "】匹配一致")
                    #         else:
                    #             count = self.runRule("正向", self.l_ruleSql[0][i], idCardNo, "检查点（正向），药品名称【" + l_drugName[i] + "】与药物类型【" + l_drugTypeNameDelRepeat[j] + "】匹配不一致")

                    if total == 5:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 日饮酒量未填写
    def sql2168(self, ruleId, idCardNo):
        # 日饮酒量未填写

        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m',str(i + 2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i] + ", " + self.l_ruleSql[0][i], '\033[0m')

                try:
                    # 1，数据准备
                    ehrNum = self.execQuery(
                        "SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)

                    m = self.execQuery("select count(*) from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
                    # 随访记录必须2条以上，涉及到 当前检验报告日期与 上一期，本期日期比对。
                    if m[0][0] >1 :

                        # # 2，检查点

                        # # 检查点1（正向）
                        self.execQuery("update tb_dc_dm_visit set vistStatusCode=NULL where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingFrequencyCode=null where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingVolume=null where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点1（正向），本次随访管理状态代码 = Null ，饮酒频率 = Null，日饮酒量 = Null")
                        total = total + count

                        # # # 检查点2（正向）
                        self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingFrequencyCode=null where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingVolume=null where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点2（正向），本次随访管理状态代码 = 1，饮酒频率 = Null，日饮酒量 = Null")
                        total = total + count

                        # # # 检查点3（正向）
                        self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingFrequencyCode=2 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingVolume=null where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点3（正向），本次随访管理状态代码 = 1 ，饮酒频率 = 2，日饮酒量 = Null")
                        total = total + count

                        # # # 检查点4（反向）
                        self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingFrequencyCode=1 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingVolume=null where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点4（正向），本次随访管理状态代码 = 1 ，饮酒频率 = 1，日饮酒量 = Null")
                        total = total + count

                        # # # 检查点5（反向）
                        self.execQuery("update tb_dc_dm_visit set vistStatusCode=2 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingFrequencyCode=2 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingVolume=null where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点5（正向），本次随访管理状态代码 = 2 ，饮酒频率 = 2，日饮酒量 = Null")
                        total = total + count

                        # # 检查点6（反向）
                        self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingFrequencyCode=2 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingVolume='11111' where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点6（正向），本次随访管理状态代码 = 1 ，饮酒频率 = 2，日饮酒量 = 11111")
                        total = total + count

                        # # 检查点7（反向）
                        self.execQuery("update tb_dc_dm_visit set vistStatusCode=2 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingFrequencyCode=1 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update tb_dc_dm_visit set drinkingVolume='11111' where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点7（正向），本次随访管理状态代码 = 2 ，饮酒频率 = 1，日饮酒量 = 11111")
                        total = total + count

                        if total == 7:
                            Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                            Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                            Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                        else:
                            Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                            Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.save()
                    else:
                        Color_PO.consoleColor("31", "31", "[ERROR]" + self.l_ruleSql[0][i], ", 随访记录必须2条及以上！")
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 与遵医行为选项不匹配
    def sql2238(self, ruleId, idCardNo):
        # 与遵医行为选项不匹配

        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m',str(i + 2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i] + ", " + self.l_ruleSql[0][i], '\033[0m')

                try:
                    # 1，数据准备
                    ehrNum = self.execQuery(
                        "SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)

                    m = self.execQuery("select count(*) from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
                    # 随访记录必须2条以上，涉及到 当前检验报告日期与 上一期，本期日期比对。
                    if m[0][0] >1 :

                        # # 2，检查点

                        # # 检查点1（正向）
                        self.execQuery("update  tb_dc_dm_visit set  complianceStatusCode =3 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  drugComplianceCode=1 where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点1（正向），遵医行为 = 3 ，服药依从性 = 1")
                        total = total + count

                        # # # 检查点2（反向）
                        self.execQuery("update  tb_dc_dm_visit set  complianceStatusCode =1 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  drugComplianceCode=1 where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点2（反向），遵医行为 = 1 ，服药依从性 = 1")
                        total = total + count

                        # # # 检查点3（反向）
                        self.execQuery("update  tb_dc_dm_visit set  complianceStatusCode =2 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  drugComplianceCode=1 where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点3（反向），遵医行为 = 2 ，服药依从性 = 1")
                        total = total + count

                        # # # 检查点4（反向）
                        self.execQuery("update  tb_dc_dm_visit set  complianceStatusCode =3 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  drugComplianceCode=2 where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点4（反向），遵医行为 = 3 ，服药依从性 = 2")
                        total = total + count

                        # # # 检查点5（反向）
                        self.execQuery("update  tb_dc_dm_visit set  complianceStatusCode =3 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  drugComplianceCode=3 where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点5（反向），遵医行为 = 3 ，服药依从性 = 3")
                        total = total + count

                        # # 检查点6（反向）
                        self.execQuery("update  tb_dc_dm_visit set  complianceStatusCode =1 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  drugComplianceCode=2 where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点6（反向），遵医行为 = 1 ，服药依从性 = 2")
                        total = total + count

                        # # 检查点7（反向）
                        self.execQuery("update  tb_dc_dm_visit set  complianceStatusCode =1 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  drugComplianceCode=3 where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点7（反向），遵医行为 = 1 ，服药依从性 = 3")
                        total = total + count

                        # # 检查点8（反向）
                        self.execQuery("update  tb_dc_dm_visit set  complianceStatusCode =2 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  drugComplianceCode=2 where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点8（反向），遵医行为 = 2 ，服药依从性 = 2")
                        total = total + count

                        # # 检查点9（反向）
                        self.execQuery("update  tb_dc_dm_visit set  complianceStatusCode =2 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  drugComplianceCode=3 where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点9（反向），遵医行为 = 2 ，服药依从性 = 3")
                        total = total + count

                        if total == 9:
                            Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                            Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                            Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                        else:
                            Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                            Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.save()
                    else:
                        Color_PO.consoleColor("31", "31", "[ERROR]" + self.l_ruleSql[0][i], ", 随访记录必须2条及以上！")
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 接受过何种形式的健康教育未填写
    def sql2427(self, ruleId, idCardNo):

        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m',str(i + 2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i] + ", " + self.l_ruleSql[0][i], '\033[0m')

                try:
                    # 1，数据准备
                    ehrNum = self.execQuery(
                        "SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)

                    m = self.execQuery("select count(*) from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
                    # 随访记录必须2条以上，涉及到 当前检验报告日期与 上一期，本期日期比对。
                    if m[0][0] >1 :

                        # # 2，检查点

                        # # 检查点1（正向）
                        self.execQuery("update  tb_dc_dm_visit set  isAcceptHealthEdu =1 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  healthEduType =null where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点1（正向），是否接受过健康教育 = 1 ，接受健康教育形式 = Null")
                        total = total + count

                        # # # 检查点2（正向）
                        self.execQuery("update  tb_dc_dm_visit set  isAcceptHealthEdu =null where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  healthEduType =null where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点2（正向），是否接受过健康教育 = NuLL ，接受健康教育形式 = Null")
                        total = total + count

                        # 检查点3（反向）
                        self.execQuery("update  tb_dc_dm_visit set  isAcceptHealthEdu =2 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  healthEduType =null where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点3（反向），是否接受过健康教育 = 2 ，接受健康教育形式 = Null")
                        total = total + count
                        #  
                        # 检查点4（反向）
                        self.execQuery("update  tb_dc_dm_visit set  isAcceptHealthEdu =1 where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  healthEduType =1 where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点4（反向），是否接受过健康教育 = 1 ，接受健康教育形式 != Null")
                        total = total + count

                        # 检查点5（反向）
                        self.execQuery("update  tb_dc_dm_visit set  isAcceptHealthEdu = null where ehrNum='%s'" % ehrNum[0][0])
                        self.execQuery("update  tb_dc_dm_visit set  healthEduType =1 where ehrNum='%s'" % ehrNum[0][0])
                        count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点5（反向），是否接受过健康教育 = null ，接受健康教育形式 != Null")
                        total = total + count

                        if total == 5:
                            Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                            Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                            Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                        else:
                            Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                            Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.save()
                    else:
                        Color_PO.consoleColor("31", "31", "[ERROR]" + self.l_ruleSql[0][i], ", 随访记录必须2条及以上！")
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()



    # 高血压，本次随访管理状态代码 与 XXX未填写 （字符型或日期）
    def btn5(self, ruleId, idCardNo, varTable, varField):

        self.isTestData(idCardNo)
        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                try:
                    # 1，检查点
                    if varField == "nextVisiDate" or varField == "sportTime" or varField == "visitDate":
                        orig_fields = self.execQuery("SELECT htn.guid, htn.visitDate FROM tb_dc_htn_visit AS htn inner join tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'" % idCardNo)
                        # print(orig_fields[0][0])  # BFF11611-7FE7-45CE-B417-8CBD122C1743
                        # print(orig_fields[0][1])  # 1990-09-01 00:00:00
                        #
                        # print(orig_fields[1][0])  # dbf4fb1fe2ec4486b25ca0cf3c56dedd
                        # print(orig_fields[1][1])  # # 1990-09-14 00:00:00

                    # 检查点1（正向）
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    self.execQuery("UPDATE {varTable} SET {varField} = null FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, varField=varField) % idCardNo)
                    count = self.runRule("正向", self.l_ruleSql[0][i], idCardNo, "检查点1（正向），本次随访管理状态代码 = Null，" + self.l_comment[0][i].replace("未填写", "") + " = Null")
                    total = total + count

                    # # 检查点2（正向）
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    self.execQuery("UPDATE {varTable} SET {varField} = null FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, varField=varField) % idCardNo)
                    count = self.runRule("正向", self.l_ruleSql[0][i], idCardNo, "检查点2（正向），本次随访管理状态代码 = 1，" + self.l_comment[0][i].replace("未填写", "") + " = Null")
                    total = total + count

                    # 检查点3（反向）
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 2 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    self.execQuery("UPDATE {varTable} SET {varField} = null FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, varField=varField) % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点3（反向），本次随访管理状态代码 = 2，" + self.l_comment[0][i].replace("未填写", "") + " = Null")
                    total = total + count

                    # # 检查点4（反向）
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 1 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    if varField == "nextVisiDate" or varField == "sportTime" or varField == "visitDate":
                        for j in range(len(orig_fields)):
                            self.execQuery("update {varTable} set {varField} =CONVERT(varchar(100), '%s', 20) where guid='%s' and guid in (SELECT htn.guid FROM tb_dc_htn_visit AS htn inner join tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s')".format(varTable=varTable, varField=varField) %(orig_fields[j][1], orig_fields[j][0], idCardNo))
                    else:
                        self.execQuery("UPDATE {varTable} SET {varField} = '1' FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, varField=varField) % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点4（反向），本次随访管理状态代码 = 1，" + self.l_comment[0][i].replace("未填写", "") + " != Null")
                    total = total + count

                    # # 检查点5（反向）
                    self.execQuery("UPDATE tb_dc_htn_visit SET vistStatusCode = 2 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点5（反向），本次随访管理状态代码 = 2，" + self.l_comment[0][i].replace("未填写", "") + " != Null")
                    total = total + count

                    if total == 5:
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    # 接受过何种形式的健康教育未填写
    def sql1910(self, ruleId, idCardNo):

        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m',str(i + 2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i] + ", " + self.l_ruleSql[0][i], '\033[0m')

                try:

                    # # 1，检查点

                    # # 检查点1（正向）
                    self.execQuery("UPDATE tb_dc_htn_visit SET isAcceptHealthEdu = 1 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'" % idCardNo)
                    self.execQuery("UPDATE tb_dc_htn_visit SET healthEduType  = null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点1（正向），是否接受过健康教育 = 1 ，接受过何种形式的健康教育 = Null")
                    total = total + count

                    # # # 检查点2（正向）
                    self.execQuery("UPDATE tb_dc_htn_visit SET isAcceptHealthEdu = null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'" % idCardNo)
                    self.execQuery("UPDATE tb_dc_htn_visit SET healthEduType  = null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点2（正向），是否接受过健康教育 = null ，接受过何种形式的健康教育 = Null")
                    total = total + count

                    # 检查点3（反向）
                    self.execQuery("UPDATE tb_dc_htn_visit SET isAcceptHealthEdu = 2 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'" % idCardNo)
                    self.execQuery("UPDATE tb_dc_htn_visit SET healthEduType  = null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点3（反向），是否接受过健康教育 = 2 ，接受过何种形式的健康教育 = Null")
                    total = total + count
                    #  
                    # 检查点4（反向）
                    self.execQuery("UPDATE tb_dc_htn_visit SET isAcceptHealthEdu = 1 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'" % idCardNo)
                    self.execQuery("UPDATE tb_dc_htn_visit SET healthEduType  = 1 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点4（反向），是否接受过健康教育 = 1 ，接受过何种形式的健康教育 != Null")
                    total = total + count

                    # 检查点5（反向）
                    self.execQuery("UPDATE tb_dc_htn_visit SET isAcceptHealthEdu = null FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'" % idCardNo)
                    self.execQuery("UPDATE tb_dc_htn_visit SET healthEduType  = 1 FROM tb_dc_htn_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo = '%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点5（反向），是否接受过健康教育 = null ，接受过何种形式的健康教育 != Null")
                    total = total + count

                    if total == 5:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()

                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()


    def btn10(self, ruleId, idCardNo, hospitalLevel, varField, varValue):
        # 一级医院有检验结果（白细胞） 3629
        # 二级医院有检验结果（白细胞） 3628
        # 三级医院有检验结果（白细胞） 3627

        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;30m',str(i + 2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i] + ", " + self.l_ruleSql[0][i], '\033[0m')

                try:
                    # 1，数据准备

                    # 初始化数据（随访日期）
                    l_q = self.getValues("31011019371125044X", "tb_dc_htn_visit", ["empiGuid", "orgCode"])
                    # 测试至少需要2条记录
                    if len(l_q) == 0:
                        exit()
                    else:
                        # 获取 cardId,orgCode,empiGuid
                        sql = self.execQuery("SELECT top 1 t4.cardId,t4.orgCode,t4.empiGuid FROM tb_empi_index_root t1 INNER JOIN tb_dc_chronic_info t2 ON t1.guid = t2.empiGuid INNER JOIN tb_dc_chronic_main t3 ON t2.manageNum = t3.manageNum AND t2.orgCode = t3.orgCode INNER JOIN tb_dc_dm_visit t4 ON t3.visitNum = t4.cardId AND t3.orgCode = t4.orgCode WHERE t1.idCardNo ='%s'" % idCardNo)
                        if len(l_q) == 2:
                            # 将第一条随访日期修改为 2020-10-1
                            self.execQuery("update tb_dc_dm_visit set visitDate='2020-10-1' where guid='%s'" % sql[0][2])
                            # 新增1条记录，随访日期为 2019-01-16
                            self.execQuery("INSERT INTO tb_dc_dm_visit([guid], [cardId], [name], [ehrNum], [orgCode], [visitDate], [visitWayCode], [visitWayValue], [otherVisit], [visitDocNo], [visitDocName], [visitOrgCode], [visitOrgName], [vistStatusCode], [visitStatusValue], [nextVisiDate], [lostVisitCode], [lostVisitName], [lostVisitDate], [otherLostVIsitName], [deathReason], [targetDistrictCode], [targetDistrictName], [targetOrgCode], [targetOrgName], [moveProvinceCode], [moveProvinceValue], [moveCityCode], [moveCityValue], [moveDistrictCode], [moveDistrictValue], [moveStreetCode], [moveStreetValue], [moveNeighborhoodCode], [moveNeighborhoodValue], [moveVillageValue], [moveHouseNumber], [moveOrgCode], [moveOrgName], [hasPaperCard], [isAcceptHealthEdu], [healthEduType], [clinicalSymptomsCode], [clinicalSymptomsValue], [otherClinicalSymptoms], [symptomStatus], [clinicalInfo], [sbp], [dbp], [height], [weight], [waistline], [hipline], [targetWeight], [BMI], [targetBMI], [dorsalArteryOfFootLeftCode], [dorsalArteryOfFootLeftName], [dorsalArteryOfFootRightCode], [dorsalArteryOfFootRightName], [hypoglycemia], [familyHistory], [isLawSport], [sportTypeCode], [sportTypeName], [sportFrequence], [sportTimes], [dietCode], [dietName], [stapleFood], [targetStapleFood], [smokingVolume], [drinkingVolume], [targetSportFrequencyCode], [targetSportFrequencyName], [targetSportTimes], [smokingStatusCode], [smokingStatusName], [targetSmoke], [quitSmoking], [drinkingFrequencyCode], [drinkingFrequencyName], [targetDrink], [psychologyStatusCode], [psychologyStatusName], [complianceStatusCode], [complianceStatusName], [referralReason], [referralOrgDept], [visitType], [fastingBloodSugarCode], [fastingBloodSugarName], [fastingBloodSugarValue], [fastingBloodSugarGatherCode], [fastingBloodSugarGatherName], [randomBloodSugarCode], [randomBloodSugarName], [randomBloodSugarValue], [randomBloodSugarGatherCode], [randomBloodSugarGatherName], [fastingBloodSugarOGTTCode], [fastingBloodSugarOGTTName], [fastingBloodSugarOGTTValue], [fastingBloodSugarOGTTGatherCode], [fastingBloodSugarOGTTGatherName], [twoHBloodSugarOGTTCode], [twoHBloodSugarOGTTName], [twoHBloodSugarOGTTValue], [twoHBloodSugarOGTTGatherCode], [twoHBloodSugarOGTTGatherName], [hbAlc], [hbAlcDate], [cholesterol], [triglycerides], [highCholesterol], [lowCholesterol], [acr], [urineProtein], [ghGaterWayCode], [ghGaterWayName], [drugComplianceCode], [drugComplianceName], [useDrug], [hasUseDrugSideEffects], [UseDrugSideEffects], [interveneCount], [beforeInterveneDate], [isIntervene], [syndrome], [interveneMeasures], [measuresContent], [otherInterveneMeasures], [otherMeasuresContent], [proposal], [otherProposal], [synStatus], [age], [empiGuid], [isGovernance]) VALUES ('99', '%s', '黄*珍', 'K0616970X', '%s', '2019-01-16 00:00:00.000', NULL, '家庭', NULL, '1015', '李*琳', '310118001', '上海市青浦区夏阳街道社区卫生服务中心', '1', '继续随访', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '4', '30', NULL, NULL, NULL, NULL, '2', NULL, NULL, NULL, NULL, '3', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, '', NULL, '1', NULL, '', NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '%s', '0')" % (sql[0][0],sql[0][1],sql[0][2]))
                        elif len(l_q) == 1:
                            # 新增2条，随访日期分别为 2019-01-16 和 2020-10-1
                            self.execQuery("INSERT INTO tb_dc_dm_visit([guid], [cardId], [name], [ehrNum], [orgCode], [visitDate], [visitWayCode], [visitWayValue], [otherVisit], [visitDocNo], [visitDocName], [visitOrgCode], [visitOrgName], [vistStatusCode], [visitStatusValue], [nextVisiDate], [lostVisitCode], [lostVisitName], [lostVisitDate], [otherLostVIsitName], [deathReason], [targetDistrictCode], [targetDistrictName], [targetOrgCode], [targetOrgName], [moveProvinceCode], [moveProvinceValue], [moveCityCode], [moveCityValue], [moveDistrictCode], [moveDistrictValue], [moveStreetCode], [moveStreetValue], [moveNeighborhoodCode], [moveNeighborhoodValue], [moveVillageValue], [moveHouseNumber], [moveOrgCode], [moveOrgName], [hasPaperCard], [isAcceptHealthEdu], [healthEduType], [clinicalSymptomsCode], [clinicalSymptomsValue], [otherClinicalSymptoms], [symptomStatus], [clinicalInfo], [sbp], [dbp], [height], [weight], [waistline], [hipline], [targetWeight], [BMI], [targetBMI], [dorsalArteryOfFootLeftCode], [dorsalArteryOfFootLeftName], [dorsalArteryOfFootRightCode], [dorsalArteryOfFootRightName], [hypoglycemia], [familyHistory], [isLawSport], [sportTypeCode], [sportTypeName], [sportFrequence], [sportTimes], [dietCode], [dietName], [stapleFood], [targetStapleFood], [smokingVolume], [drinkingVolume], [targetSportFrequencyCode], [targetSportFrequencyName], [targetSportTimes], [smokingStatusCode], [smokingStatusName], [targetSmoke], [quitSmoking], [drinkingFrequencyCode], [drinkingFrequencyName], [targetDrink], [psychologyStatusCode], [psychologyStatusName], [complianceStatusCode], [complianceStatusName], [referralReason], [referralOrgDept], [visitType], [fastingBloodSugarCode], [fastingBloodSugarName], [fastingBloodSugarValue], [fastingBloodSugarGatherCode], [fastingBloodSugarGatherName], [randomBloodSugarCode], [randomBloodSugarName], [randomBloodSugarValue], [randomBloodSugarGatherCode], [randomBloodSugarGatherName], [fastingBloodSugarOGTTCode], [fastingBloodSugarOGTTName], [fastingBloodSugarOGTTValue], [fastingBloodSugarOGTTGatherCode], [fastingBloodSugarOGTTGatherName], [twoHBloodSugarOGTTCode], [twoHBloodSugarOGTTName], [twoHBloodSugarOGTTValue], [twoHBloodSugarOGTTGatherCode], [twoHBloodSugarOGTTGatherName], [hbAlc], [hbAlcDate], [cholesterol], [triglycerides], [highCholesterol], [lowCholesterol], [acr], [urineProtein], [ghGaterWayCode], [ghGaterWayName], [drugComplianceCode], [drugComplianceName], [useDrug], [hasUseDrugSideEffects], [UseDrugSideEffects], [interveneCount], [beforeInterveneDate], [isIntervene], [syndrome], [interveneMeasures], [measuresContent], [otherInterveneMeasures], [otherMeasuresContent], [proposal], [otherProposal], [synStatus], [age], [empiGuid], [isGovernance]) VALUES ('100', '%s', '黄*珍', 'K0616970X', '%s', '2019-01-16 00:00:00.000', NULL, '家庭', NULL, '1015', '李*琳', '310118001', '上海市青浦区夏阳街道社区卫生服务中心', '1', '继续随访', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '4', '30', NULL, NULL, NULL, NULL, '2', NULL, NULL, NULL, NULL, '3', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, '', NULL, '1', NULL, '', NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '%s', '0')" % (sql[0][0],sql[0][1],sql[0][2]))
                            self.execQuery("INSERT INTO tb_dc_dm_visit([guid], [cardId], [name], [ehrNum], [orgCode], [visitDate], [visitWayCode], [visitWayValue], [otherVisit], [visitDocNo], [visitDocName], [visitOrgCode], [visitOrgName], [vistStatusCode], [visitStatusValue], [nextVisiDate], [lostVisitCode], [lostVisitName], [lostVisitDate], [otherLostVIsitName], [deathReason], [targetDistrictCode], [targetDistrictName], [targetOrgCode], [targetOrgName], [moveProvinceCode], [moveProvinceValue], [moveCityCode], [moveCityValue], [moveDistrictCode], [moveDistrictValue], [moveStreetCode], [moveStreetValue], [moveNeighborhoodCode], [moveNeighborhoodValue], [moveVillageValue], [moveHouseNumber], [moveOrgCode], [moveOrgName], [hasPaperCard], [isAcceptHealthEdu], [healthEduType], [clinicalSymptomsCode], [clinicalSymptomsValue], [otherClinicalSymptoms], [symptomStatus], [clinicalInfo], [sbp], [dbp], [height], [weight], [waistline], [hipline], [targetWeight], [BMI], [targetBMI], [dorsalArteryOfFootLeftCode], [dorsalArteryOfFootLeftName], [dorsalArteryOfFootRightCode], [dorsalArteryOfFootRightName], [hypoglycemia], [familyHistory], [isLawSport], [sportTypeCode], [sportTypeName], [sportFrequence], [sportTimes], [dietCode], [dietName], [stapleFood], [targetStapleFood], [smokingVolume], [drinkingVolume], [targetSportFrequencyCode], [targetSportFrequencyName], [targetSportTimes], [smokingStatusCode], [smokingStatusName], [targetSmoke], [quitSmoking], [drinkingFrequencyCode], [drinkingFrequencyName], [targetDrink], [psychologyStatusCode], [psychologyStatusName], [complianceStatusCode], [complianceStatusName], [referralReason], [referralOrgDept], [visitType], [fastingBloodSugarCode], [fastingBloodSugarName], [fastingBloodSugarValue], [fastingBloodSugarGatherCode], [fastingBloodSugarGatherName], [randomBloodSugarCode], [randomBloodSugarName], [randomBloodSugarValue], [randomBloodSugarGatherCode], [randomBloodSugarGatherName], [fastingBloodSugarOGTTCode], [fastingBloodSugarOGTTName], [fastingBloodSugarOGTTValue], [fastingBloodSugarOGTTGatherCode], [fastingBloodSugarOGTTGatherName], [twoHBloodSugarOGTTCode], [twoHBloodSugarOGTTName], [twoHBloodSugarOGTTValue], [twoHBloodSugarOGTTGatherCode], [twoHBloodSugarOGTTGatherName], [hbAlc], [hbAlcDate], [cholesterol], [triglycerides], [highCholesterol], [lowCholesterol], [acr], [urineProtein], [ghGaterWayCode], [ghGaterWayName], [drugComplianceCode], [drugComplianceName], [useDrug], [hasUseDrugSideEffects], [UseDrugSideEffects], [interveneCount], [beforeInterveneDate], [isIntervene], [syndrome], [interveneMeasures], [measuresContent], [otherInterveneMeasures], [otherMeasuresContent], [proposal], [otherProposal], [synStatus], [age], [empiGuid], [isGovernance]) VALUES ('101', '%s', '黄*珍', 'K0616970X', '%s', '2020-10-1 00:00:00.000', NULL, '家庭', NULL, '1015', '李*琳', '310118001', '上海市青浦区夏阳街道社区卫生服务中心', '1', '继续随访', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '4', '30', NULL, NULL, NULL, NULL, '2', NULL, NULL, NULL, NULL, '3', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL, '', NULL, '1', NULL, '', NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '%s', '0')" % (sql[0][0],sql[0][1],sql[0][2]))

                    # 初始化数据，随访日期从早到晚依次排列
                    visitDate = self.execQuery("SELECT visitDate FROM tb_dc_htn_visit AS htn inner join tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    l_visitDate = []
                    for j in range(len(visitDate)):
                        l_visitDate.append(str(visitDate[j][0]).split(" ")[0])
                    l_visitDate.sort()
                    # print(l_visitDate)

                    # 初始化表
                    self.execQuery("DELETE FROM tb_lis_report")
                    self.execQuery("DELETE FROM tb_lis_report_indicator")
                    self.execQuery("insert into tb_lis_report(guid,visitStrNo,orgCode,orgName,visitType,reportNo,name,empiGuid,patientId,specimenTypeCodeSystem,specimenTypeCode,specimenTypeName,reportTypeCodeSystem,reportTypeCode,reportTypeName,reportName,applyDeptCode,applyDeptName,applyDoctorCode,applyDoctorName,reportDoctorCode,reportDoctorName,applyDate,reportDate,orderNo,status,createDate,isCurrent) values('1',null,'%s',null,null,'123456',null,'%s',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)" % (sql[0][1], sql[0][2]))
                    self.execQuery("insert into tb_lis_report_indicator(guid,visitStrNo,orgCode,orgName,visitType,reportNo,insItemCode,itemCodeSystem,itemCode,itemName,resultValue,resultUnit,resultFlagCodeSystem,resultFlagCode,resultFlagName,refQuality,refQuantifyLower,refQuantifyUpper,[order],status,createDate,isCurrent,empiGuid) values('1',null,'%s',null,null,'123456',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,'%s')" % (sql[0][1], sql[0][2]))


                    # # 2，检查点
                    # # 检查点1（正向）
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 1 FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    self.execQuery("UPDATE tb_dc_dm_visit SET {varField} = null FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varField=varField) % idCardNo)
                    self.execQuery("update t_dic_hospital_info set HospitalLevel='%s' where Hospital_id='%s'" % (hospitalLevel, sql[0][1]))
                    self.execQuery("update tb_lis_report_indicator set itemName='%s'" % varValue)
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))  # # 第一条随访日期的后2天
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点1（正向），本次随访管理状态代码 = 1 ，" + str(varField) + " = Null，医院等级 = " + str(hospitalLevel) + "，项目名称 = " + str(varValue) + "，检验报告日期为第一次随访日期到第二次随访日期之间")
                    total = total + count

                    # # # 检查点2（正向）
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], -2))  # 最近一条随访日期的前2天
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点2（正向），将检查点1中的 检验报告日期为上一次与本次随访日期之间，其余条件不变")
                    total = total + count

                    # # # 检查点3（正向）
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = null FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点3（正向），将检查点1中的 本次随访管理状态代码 = Null，其余条件不变")
                    total = total + count

                    # # # 检查点4（正向）
                    self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[-1])
                    count = self.runRule("正", self.l_ruleSql[0][i], idCardNo, "检查点4（正向），将检查点1中的检验报告日期等于本次随访日期，其余条件不变")
                    total = total + count

                    # # # 检查点5（反向）
                    self.execQuery("UPDATE tb_dc_dm_visit SET vistStatusCode = 2 FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'" % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点5（反向），将检查点1中的 本次随访管理状态代码 = 2，其余条件不变")
                    total = total + count

                    # # 检查点6（反向）
                    self.execQuery("UPDATE tb_dc_dm_visit SET {varField} = '123' FROM tb_dc_dm_visit AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode AND htn.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varField=varField) % idCardNo)
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点6（反向），将检查点1中的 总胆固醇值 <> Null，其余条件不变")
                    total = total + count

                    # # 检查点7（反向）
                    errorHosptialLevel = int(hospitalLevel) + 1
                    self.execQuery("update t_dic_hospital_info set HospitalLevel='%s' where Hospital_id='%s'" % (errorHosptialLevel, sql[0][1]))
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点7（反向），将检查点1中的 医院级别 = " + str(errorHosptialLevel) + " ，其余条件不变")
                    self.execQuery("update t_dic_hospital_info set HospitalLevel='1' where Hospital_id='%s'" % (sql[0][1]))
                    total = total + count

                    # # 检查点8（反向）
                    self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[0])
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点8（反向），将检查点1中检验报告日期等于第一次随访日期，其余条件不变")
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
                    total = total + count

                    # # 检查点9（反向）
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], -2))
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点9（反向），将检查点1中检验报告日期早于第一次随访日期，其余条件不变")
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
                    total = total + count

                    # # 检查点10（反向）
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], 2))
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点10（反向），将检查点1中检验报告日期晚于本次随访日期，其余条件不变")
                    self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
                    total = total + count

                    if total == 10:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()

                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()
