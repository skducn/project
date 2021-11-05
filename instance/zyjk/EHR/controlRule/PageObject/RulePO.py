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
        self.id = id
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

        sign = 0
        # 1） 执行质控
        os.system('curl -X  GET "http://192.168.0.243:8090/healthRecordRules/rulesEngine/execute/' + str(idCardNo) + '" -H  "accept: */*" -o /dev/null -s')
        # 2） 检查结果
        result = self.execQuery("select * from HrRule r1 inner join HrRuleRecord r2 on r1.RuleId=r2.RuleId where r2.ArchiveNum='%s' AND r1.RuleSql='%s'" % (idCardNo, ruleSql))
        if  "反" in varWay :
            # 反向测试
            if len(result) > 0:
                Color_PO.consoleColor("31", "31", "[ERRORRRRRRRRRR]" + varMsg, "")
                sign += 1
            else:
                Color_PO.consoleColor("31", "33", "[OK]", varMsg)

        else:
            # 正向测试
            if len(result) > 0:
                Color_PO.consoleColor("31", "36", "[OK]", varMsg)
            else:
                Color_PO.consoleColor("31", "31", "[ERRORRRRRRRRRR]" + varMsg, "")
                sign += 1

        return sign

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

    def integrity7(self, ruleId, idCardNo, d_tableField, *p):

        # 完整性多表

        # R.integrity123(R.id[0][i], "310110193902060067", {"tb_dc_dm_visit":["vistStatusCode", "hbAlc"]}, ["正1", 1, "NULL"],["正2", "NULL", "NULL"], ["反3", 1, "123"], ["反4", 2, "NULL"],["反5",2,"123"])

        # d = {"tb_dc_dm_visit": ["vistStatusCode", "hbAlc"], "name": ["111", "222", "333"]}
        for k, v in d_tableField.items():
            print(k) # tb_dc_dm_visit
            print(v)  #  ["vistStatusCode", "hbAlc"]


        try:
            count = 0
            total = 0
            for i in range(len(self.id[0])):
                if ruleId == self.id[0][i]:
                    print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.id[0][i] + ", " + self.l_ruleSql[0][i], '\033[0m')

                    cType =0
                    l_checkpoint = []

                    # 获取检查点
                    for j in range(1, len(p)):
                        l_checkpoint.append(p[j])

                    # 遍历字段，判断类型
                    l_fieldType = []
                    for a in range(len(p[0])):
                        if Sqlserver_PO.getFieldType(varTable, p[0][a]) == "datetime":
                            l_fieldType.append(1)
                            cType = 1
                        else:
                            l_fieldType.append(0)
                    # print(l_fieldType)

                    # 2个字段
                    if len(p[0]) == 2 :
                        if cType == 0:
                            # 不是datetime字段
                            for j in range(len(l_checkpoint)):
                                self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1]) % (l_checkpoint[j][1], l_checkpoint[j][2], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]))
                                total = total + sign
                        else:
                            # 有部分字段是datatime类型
                            for j in range(len(l_checkpoint)):
                                if l_fieldType[0] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = CONVERT(varchar(100), '%s', 20), {field2}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1]) % (l_checkpoint[j][1], l_checkpoint[j][2], idCardNo))
                                if l_fieldType[1] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= CONVERT(varchar(100), %s, 20) FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1]) % (l_checkpoint[j][1], l_checkpoint[j][2], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo,  "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]))
                                total = total + sign
                    # 3个字段
                    elif len(p[0]) == 3:
                         if cType == 0:
                            # 不是datetime字段
                            for j in range(len(l_checkpoint)):
                                self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]) + "，" + str(p[0][2]) + " = " + str(l_checkpoint[j][3]))
                                total = total + sign
                         else:
                            # 有部分字段是datatime类型
                            for j in range(len(l_checkpoint)):
                                if l_fieldType[0] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = CONVERT(varchar(100), '%s', 20), {field2}= %s, {field3}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], idCardNo))
                                if l_fieldType[1] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= CONVERT(varchar(100), %s, 20), {field3}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], idCardNo))
                                if l_fieldType[2] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= CONVERT(varchar(100), %s, 20) FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]) + "，" + str(p[0][2]) + " = " + str(l_checkpoint[j][3]))
                                total = total + sign
                    # 4个字段
                    elif len(p[0]) == 4:
                         if cType == 0:
                            # 不是datetime字段
                            for j in range(len(l_checkpoint)):
                                self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= %s, {field4}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]) + "，" + str(p[0][2]) + " = " + str(l_checkpoint[j][3]) + "，" + str(p[0][3]) + " = " + str(l_checkpoint[j][4]))
                                total = total + sign
                         else:
                            # 有部分字段是datatime类型
                            for j in range(len(l_checkpoint)):
                                if l_fieldType[0] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = CONVERT(varchar(100), '%s', 20), {field2}= %s, {field3}= %s, {field4}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], idCardNo))
                                if l_fieldType[1] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= CONVERT(varchar(100), %s, 20), {field3}= %s, {field4}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], idCardNo))
                                if l_fieldType[2] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= CONVERT(varchar(100), %s, 20), {field4}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], idCardNo))
                                if l_fieldType[3] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= %s, {field4}= CONVERT(varchar(100), %s, 20) FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]) + "，" + str(p[0][2]) + " = " + str(l_checkpoint[j][3])+ "，" + str(p[0][3]) + " = " + str(l_checkpoint[j][4]))
                                total = total + sign
                    # 5个字段
                    elif len(p[0]) == 5:
                         if cType == 0:
                            # 不是datetime字段
                            for j in range(len(l_checkpoint)):
                                self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= %s, {field4}= %s, {field5}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3], field5=p[0][4]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], l_checkpoint[j][5], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]) + "，" + str(p[0][2]) + " = " + str(l_checkpoint[j][3]) + "，" + str(p[0][3]) + " = " + str(l_checkpoint[j][4]) + "，" + str(p[0][4]) + " = " + str(l_checkpoint[j][5]))
                                total = total + sign
                         else:
                            # 有部分字段是datatime类型
                            for j in range(len(l_checkpoint)):
                                if l_fieldType[0] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = CONVERT(varchar(100), '%s', 20), {field2}= %s, {field3}= %s, {field4}= %s, {field5}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3], field5=p[0][4]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], l_checkpoint[j][5], idCardNo))
                                if l_fieldType[1] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= CONVERT(varchar(100), %s, 20), {field3}= %s, {field4}= %s, {field5}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3], field5=p[0][4]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], l_checkpoint[j][5], idCardNo))
                                if l_fieldType[2] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= CONVERT(varchar(100), %s, 20), {field4}= %s, {field5}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3], field5=p[0][4]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], l_checkpoint[j][5], idCardNo))
                                if l_fieldType[3] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= %s, {field4}= CONVERT(varchar(100), %s, 20), {field5}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3], field5=p[0][4]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], l_checkpoint[j][5], idCardNo))
                                if l_fieldType[4] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= %s, {field4}= %s, {field5}= CONVERT(varchar(100), %s, 20) FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3], field5=p[0][4]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], l_checkpoint[j][5], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]) + "，" + str(p[0][2]) + " = " + str(l_checkpoint[j][3])+ "，" + str(p[0][3]) + " = " + str(l_checkpoint[j][4]) + "，" + str(p[0][4]) + " = " + str(l_checkpoint[j][5]))
                                total = total + sign

                    if total == 0:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
        except Exception as e:
            print("errorrrrrrrrrr, 未知异常 => ", e)


    def integrity123(self, ruleId, idCardNo, varTable, *p):

        # 完整性单表
        # R.integrity123(R.id[0][i], "310110193902060067", "tb_dc_dm_visit",["vistStatusCode", "hbAlc"], ["正1", 1, "NULL"],["正2", "NULL", "NULL"], ["反3", 1, "123"], ["反4", 2, "NULL"],["反5",2,"123"])

        try:
            count = 0
            total = 0
            for i in range(len(self.id[0])):
                if ruleId == self.id[0][i]:
                    print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.id[0][i] + ", " + self.l_ruleSql[0][i], '\033[0m')

                    cType =0
                    l_checkpoint = []

                    # 获取检查点
                    for j in range(1, len(p)):
                        l_checkpoint.append(p[j])

                    # 遍历字段，判断类型
                    l_fieldType = []
                    for a in range(len(p[0])):
                        if Sqlserver_PO.getFieldType(varTable, p[0][a]) == "datetime":
                            l_fieldType.append(1)
                            cType = 1
                        else:
                            l_fieldType.append(0)
                    # print(l_fieldType)

                    # 2个字段
                    if len(p[0]) == 2 :
                        if cType == 0:
                            # 不是datetime字段
                            for j in range(len(l_checkpoint)):
                                self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1]) % (l_checkpoint[j][1], l_checkpoint[j][2], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]))
                                total = total + sign
                        else:
                            # 有部分字段是datatime类型
                            for j in range(len(l_checkpoint)):
                                if l_fieldType[0] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = CONVERT(varchar(100), '%s', 20), {field2}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1]) % (l_checkpoint[j][1], l_checkpoint[j][2], idCardNo))
                                if l_fieldType[1] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= CONVERT(varchar(100), %s, 20) FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1]) % (l_checkpoint[j][1], l_checkpoint[j][2], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo,  "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]))
                                total = total + sign
                    # 3个字段
                    elif len(p[0]) == 3:
                         if cType == 0:
                            # 不是datetime字段
                            for j in range(len(l_checkpoint)):
                                self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]) + "，" + str(p[0][2]) + " = " + str(l_checkpoint[j][3]))
                                total = total + sign
                         else:
                            # 有部分字段是datatime类型
                            for j in range(len(l_checkpoint)):
                                if l_fieldType[0] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = CONVERT(varchar(100), '%s', 20), {field2}= %s, {field3}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], idCardNo))
                                if l_fieldType[1] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= CONVERT(varchar(100), %s, 20), {field3}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], idCardNo))
                                if l_fieldType[2] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= CONVERT(varchar(100), %s, 20) FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]) + "，" + str(p[0][2]) + " = " + str(l_checkpoint[j][3]))
                                total = total + sign
                    # 4个字段
                    elif len(p[0]) == 4:
                         if cType == 0:
                            # 不是datetime字段
                            for j in range(len(l_checkpoint)):
                                self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= %s, {field4}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]) + "，" + str(p[0][2]) + " = " + str(l_checkpoint[j][3]) + "，" + str(p[0][3]) + " = " + str(l_checkpoint[j][4]))
                                total = total + sign
                         else:
                            # 有部分字段是datatime类型
                            for j in range(len(l_checkpoint)):
                                if l_fieldType[0] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = CONVERT(varchar(100), '%s', 20), {field2}= %s, {field3}= %s, {field4}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], idCardNo))
                                if l_fieldType[1] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= CONVERT(varchar(100), %s, 20), {field3}= %s, {field4}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], idCardNo))
                                if l_fieldType[2] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= CONVERT(varchar(100), %s, 20), {field4}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], idCardNo))
                                if l_fieldType[3] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= %s, {field4}= CONVERT(varchar(100), %s, 20) FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]) + "，" + str(p[0][2]) + " = " + str(l_checkpoint[j][3])+ "，" + str(p[0][3]) + " = " + str(l_checkpoint[j][4]))
                                total = total + sign
                    # 5个字段
                    elif len(p[0]) == 5:
                         if cType == 0:
                            # 不是datetime字段
                            for j in range(len(l_checkpoint)):
                                self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= %s, {field4}= %s, {field5}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3], field5=p[0][4]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], l_checkpoint[j][5], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]) + "，" + str(p[0][2]) + " = " + str(l_checkpoint[j][3]) + "，" + str(p[0][3]) + " = " + str(l_checkpoint[j][4]) + "，" + str(p[0][4]) + " = " + str(l_checkpoint[j][5]))
                                total = total + sign
                         else:
                            # 有部分字段是datatime类型
                            for j in range(len(l_checkpoint)):
                                if l_fieldType[0] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = CONVERT(varchar(100), '%s', 20), {field2}= %s, {field3}= %s, {field4}= %s, {field5}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3], field5=p[0][4]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], l_checkpoint[j][5], idCardNo))
                                if l_fieldType[1] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= CONVERT(varchar(100), %s, 20), {field3}= %s, {field4}= %s, {field5}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3], field5=p[0][4]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], l_checkpoint[j][5], idCardNo))
                                if l_fieldType[2] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= CONVERT(varchar(100), %s, 20), {field4}= %s, {field5}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3], field5=p[0][4]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], l_checkpoint[j][5], idCardNo))
                                if l_fieldType[3] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= %s, {field4}= CONVERT(varchar(100), %s, 20), {field5}= %s FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3], field5=p[0][4]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], l_checkpoint[j][5], idCardNo))
                                if l_fieldType[4] == 1:
                                    self.execQuery("UPDATE {varTable} SET {field1} = %s, {field2}= %s, {field3}= %s, {field4}= %s, {field5}= CONVERT(varchar(100), %s, 20) FROM {varTable} AS htn INNER JOIN tb_dc_chronic_main AS cMain ON htn.OrgCode = cMain.orgCode INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo ='%s'".format(varTable=varTable, field1=p[0][0], field2=p[0][1], field3=p[0][2], field4=p[0][3], field5=p[0][4]) % (l_checkpoint[j][1], l_checkpoint[j][2], l_checkpoint[j][3], l_checkpoint[j][4], l_checkpoint[j][5], idCardNo))
                                sign = self.runRule(l_checkpoint[j][0], self.l_ruleSql[0][i], idCardNo, "（" + l_checkpoint[j][0] + "）， " + str(p[0][0]) + " = " + str(l_checkpoint[j][1]) + "，" + str(p[0][1]) + " = " + str(l_checkpoint[j][2]) + "，" + str(p[0][2]) + " = " + str(l_checkpoint[j][3])+ "，" + str(p[0][3]) + " = " + str(l_checkpoint[j][4]) + "，" + str(p[0][4]) + " = " + str(l_checkpoint[j][5]))
                                total = total + sign

                    if total == 0:
                        Openpyxl_PO.setCellValue(i + 2, 22, "ok", ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce', '006100'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 20, "N", "", "rule")
                    else:
                        Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                        Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
                    Openpyxl_PO.save()
        except Exception as e:
            print("errorrrrrrrrrr, 未知异常 => ", e)



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
        for i in range(len(self.id[0])):
            if ruleId == self.id[0][i]:
                print('\n\033[1;31;30m',str(i + 2) + ", " + self.l_comment[0][i] + ", " + self.id[0][i] + ", " + self.l_ruleSql[0][i], '\033[0m')

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
        for i in range(len(self.id[0])):
            if ruleId == self.id[0][i]:
                print('\n\033[1;31;30m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.id[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')

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



    def btn10(self, ruleId, idCardNo, hospitalLevel, varField, varValue):
        # 一级医院有检验结果（白细胞） 3629
        # 二级医院有检验结果（白细胞） 3628
        # 三级医院有检验结果（白细胞） 3627

        count = 0
        total = 0
        for i in range(len(self.id[0])):
            if ruleId == self.id[0][i]:
                print('\n\033[1;31;30m',str(i + 2) + ", " + self.l_comment[0][i] + ", " + self.id[0][i] + ", " + self.l_ruleSql[0][i], '\033[0m')

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
