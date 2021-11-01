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
        Sqlserver_PO.ExecQueryBySQL(File_PO.getLayerPath("./config") + "\\" + varSqlFile)

    # 2，执行SQL命令
    def execQuery(self, varSQL):
        x = Sqlserver_PO.ExecQuery(varSQL)
        return x

    # 3，执行存储过程
    def execProcedure(self, varProcedureName):
        Sqlserver_PO.ExecProcedure(varProcedureName)

    # 4，执行sql文件
    def execSqlFile1(self, varSqlFile):
        Sqlserver_PO.ExecQueryBySQL1(File_PO.getLayerPath("./config") + "\\" + varSqlFile)

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
                Color_PO.consoleColor("31", "31", "[ERROR]", varMsg)
            else:
                Color_PO.consoleColor("31", "33", "[OK]", varMsg)
                count +=1
        else:
            # 正向测试
            if len(result) > 0:
                Color_PO.consoleColor("31", "36", "[OK]", varMsg)
                count += 1
            else:
                Color_PO.consoleColor("31", "31", "[ERROR]", varMsg)

        return count

    # 6, # 判断测试数据（身份证）是否存在？
    def isTestData(self, idCardNo):

        n = self.execQuery("select count(*) from tb_empi_index_root where idCardNo='%s'" % idCardNo)
        if n[0][0] != 1:
            Color_PO.consoleColor("31", "31", "[ERROR]" + " select * from tb_empi_index_root where idCardNo='" + str(idCardNo) +"'", ", 此身份证不存在或重复！")
            exit()
        return idCardNo

    # ***************************************************************************************************************************************************************************************************

    def c5(self, ruleId, idCardNo, varTable, varField):
        # 模板陈

        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;38m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')
                # print("\n" + str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i])
                try:
                    # 1，数据准备
                    ehrNum = self.execQuery(
                        "SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)

                    # 2，检查点

                    # 检查点1（正向）
                    self.execQuery("update tb_dc_dm_visit set vistStatusCode=Null where ehrNum='%s'" % ehrNum[0][0])
                    self.execQuery("update  {varTable} set  {varField} =Null".format(varTable=varTable, varField=varField))
                    count = self.runRule("正向", self.l_ruleSql[0][i], idCardNo, "检查点1（正向），本次随访管理状态代码 = Null，" + self.l_comment[0][i] + " = Null")
                    total = total + count

                    # 检查点2（正向）
                    self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                    self.execQuery("update  {varTable} set  {varField} =Null".format(varTable=varTable, varField=varField))
                    count = self.runRule("正向", self.l_ruleSql[0][i], idCardNo, "检查点2（正向），本次随访管理状态代码 = 1，" + self.l_comment[0][i] + " = Null")
                    total = total + count

                    # 检查点3（反向）
                    self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                    self.execQuery("update  {varTable} set  {varField} ='11111'".format(varTable=varTable, varField=varField))
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点3（正向），本次随访管理状态代码 = 1，" + self.l_comment[0][i] + " != Null")
                    total = total + count

                    # 检查点4（反向）
                    self.execQuery("update tb_dc_dm_visit set vistStatusCode=2 where ehrNum='%s'" % ehrNum[0][0])
                    self.execQuery("update  {varTable} set  {varField} =Null".format(varTable=varTable, varField=varField))
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点4（正向），本次随访管理状态代码 = 2，" + self.l_comment[0][i] + " = Null")
                    total = total + count

                    # 检查点5（反向）
                    self.execQuery("update tb_dc_dm_visit set vistStatusCode=2 where ehrNum='%s'" % (ehrNum[0][0]))
                    self.execQuery("update  {varTable} set  {varField} ='11111'".format(varTable=varTable, varField=varField))
                    count = self.runRule("", self.l_ruleSql[0][i], idCardNo, "检查点5（反向），本次随访管理状态代码 = 2，" + self.l_comment[0][i] + " != Null")
                    total = total + count

                    if total == 5:
                        return "ok"
                    else:
                        return "error"
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

    def sql3995(self, ruleId, idCardNo):
        # 药品名称与药物类型不匹配

        count = 0
        total = 0
        for i in range(len(self.l_ruleId[0])):
            if ruleId == self.l_ruleId[0][i]:
                print('\n\033[1;31;38m', str(i+2) + ", " + self.l_comment[0][i] + ", " + self.l_ruleId[0][i]  + ", " +  self.l_ruleSql[0][i], '\033[0m')

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
                        return "ok"
                    else:
                        return "error"
                except:
                    Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
                    exit()

               
    def ruleId_66f1d27307164209b95f51fe8576a2cd_4(self, comment, ruleSql, idCardNo):
        # 一级医院有检验结果（ACR）
        print("\n" + comment + ruleSql.center(100, "-"))
        try:
            # 1，数据准备
            ehrNum = self.execQuery(
                "SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
            orgCode = self.execQuery(
                "SELECT  top 1 dm.orgCode FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
            empiGuid = self.execQuery("select guid from tb_empi_index_root where idCardNo='%s'" % idCardNo)
            visitDate = self.execQuery("select visitDate from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
            l_visitDate = []
            for i in range(len(visitDate)):
                l_visitDate.append(str(visitDate[i][0]).split(" ")[0])
            l_visitDate.sort()  # 随访日期从早到晚依次排列
            # print(l_visitDate)
            # print(Time_PO.getBeforeAfterDate(l_visitDate[0], 2))  # 第一条随访日期的后2天
            # print(Time_PO.getBeforeAfterDate(l_visitDate[-1], -2))  # 最近一条随访日期的前2天

            m = self.execQuery("select count(*) from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
            # 随访记录必须2条以上，涉及到 当前检验报告日期与 上一期，本期日期比对。
            if m[0][0] >1 :
                # 初始化表
                self.execQuery("DELETE FROM tb_lis_report")
                self.execQuery("DELETE FROM tb_lis_report_indicator")
                self.execQuery("insert into tb_lis_report(guid,visitStrNo,orgCode,orgName,visitType,reportNo,name,empiGuid,patientId,specimenTypeCodeSystem,specimenTypeCode,specimenTypeName,reportTypeCodeSystem,reportTypeCode,reportTypeName,reportName,applyDeptCode,applyDeptName,applyDoctorCode,applyDoctorName,reportDoctorCode,reportDoctorName,applyDate,reportDate,orderNo,status,createDate,isCurrent) values('1',null,'%s',null,null,'123456',null,'%s',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)" % (orgCode[0][0], empiGuid[0][0]))
                self.execQuery("insert into tb_lis_report_indicator(guid,visitStrNo,orgCode,orgName,visitType,reportNo,insItemCode,itemCodeSystem,itemCode,itemName,resultValue,resultUnit,resultFlagCodeSystem,resultFlagCode,resultFlagName,refQuality,refQuantifyLower,refQuantifyUpper,[order],status,createDate,isCurrent,empiGuid) values('1',null,'%s',null,null,'123456',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,'%s')" % (orgCode[0][0], empiGuid[0][0]))

                # # 2，检查点

                # # 检查点1.1（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update tb_dc_dm_visit set acr=null where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update t_dic_hospital_info set HospitalLevel='1' where Hospital_id='%s'" % (orgCode[0][0]))
                self.execQuery("update tb_lis_report_indicator set itemName='%s'" % ('ACR'))
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))  # # 第一条随访日期的后2天
                self.runRule("正", ruleSql, idCardNo, "检查点1.1（正向），本次随访管理状态代码 = 1 ，尿微量白蛋白/尿肌酐 = Null，医院等级 = 1，项目名称 = ACR，检验报告日期为第一次随访日期到第二次随访日期之间")

                # # 检查点1.2（正向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], -2))  # 最近一条随访日期的前2天
                self.runRule("正", ruleSql, idCardNo,"检查点1.2（正向），本次随访管理状态代码 = 1 ，尿微量白蛋白/尿肌酐 = Null，医院等级 = 1，项目名称 = ACR，检验报告日期为上一次与本次随访日期之间")

                # # 检查点2（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=Null where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("正", ruleSql, idCardNo, "检查点2（正向），将检查点1中的 本次随访管理状态代码 = Null，其余条件不变")

                # # 检查点3（正向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[-1])
                self.runRule("正", ruleSql, idCardNo, "检查点3（正向），将检查点1中的检验报告日期等于本次随访日期，其余条件不变")

                # # 检查点4（正向）
                self.execQuery("update tb_lis_report_indicator set itemName='尿微量白蛋白肌酐比值'")
                self.runRule("正", ruleSql, idCardNo, "检查点4（正向），将检查点1中的 项目名称 = 尿微量白蛋白肌酐比值，其余条件不变")

                # 检查点5（反向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=2 where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("", ruleSql, idCardNo, "检查点5（反向），将检查点1中的 本次随访管理状态代码 = 2，其余条件不变")
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])

                # 检查点6（反向）
                self.execQuery("update tb_dc_dm_visit set acr='1111' where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("", ruleSql, idCardNo, "检查点6（反向），将检查点1中的 尿微量白蛋白/尿肌酐 = 非Null，其余条件不变")
                self.execQuery("update tb_dc_dm_visit set acr=null where ehrNum='%s'" % ehrNum[0][0])

                # 检查点7（反向）
                self.execQuery("update t_dic_hospital_info set HospitalLevel='2' where Hospital_id='%s'" % (orgCode[0][0]))
                self.runRule("", ruleSql, idCardNo, "检查点7（反向），将检查点1中的 医院等级 = 2，其余条件不变")
                self.execQuery("update t_dic_hospital_info set HospitalLevel='1' where Hospital_id='%s'" % (orgCode[0][0]))

                # 检查点8（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[0])
                self.runRule("", ruleSql, idCardNo, "检查点8（反向），将检查点1中检验报告日期等于第一次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))

                # 检查点9（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], -2))
                self.runRule("", ruleSql, idCardNo, "检查点9（反向），将检查点1中检验报告日期早于第一次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))

                # 检查点10（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], 2))
                self.runRule("", ruleSql, idCardNo, "检查点10（反向），将检查点1中检验报告日期晚于本次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
            else:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleSql, ", 随访记录必须2条及以上！")
        except:
            Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
            exit()
    def ruleId_97384e2480e14d4db9a6f70d33b8d4ff_5(self, comment, ruleSql, idCardNo):
        # 三级医院有检验结果（ACR）
        print("\n" + comment + ruleSql.center(100, "-"))
        try:
            # 1，数据准备
            ehrNum = self.execQuery(
                "SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
            orgCode = self.execQuery(
                "SELECT  top 1 dm.orgCode FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
            empiGuid = self.execQuery("select guid from tb_empi_index_root where idCardNo='%s'" % idCardNo)
            visitDate = self.execQuery("select visitDate from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
            l_visitDate = []
            for i in range(len(visitDate)):
                l_visitDate.append(str(visitDate[i][0]).split(" ")[0])
            l_visitDate.sort()  # 随访日期从早到晚依次排列

            m = self.execQuery("select count(*) from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
            # 随访记录必须2条以上，涉及到 当前检验报告日期与 上一期，本期日期比对。
            if m[0][0] >1 :
                self.execQuery("DELETE FROM tb_lis_report")
                self.execQuery("DELETE FROM tb_lis_report_indicator")
                self.execQuery("insert into tb_lis_report(guid,visitStrNo,orgCode,orgName,visitType,reportNo,name,empiGuid,patientId,specimenTypeCodeSystem,specimenTypeCode,specimenTypeName,reportTypeCodeSystem,reportTypeCode,reportTypeName,reportName,applyDeptCode,applyDeptName,applyDoctorCode,applyDoctorName,reportDoctorCode,reportDoctorName,applyDate,reportDate,orderNo,status,createDate,isCurrent) values('1',null,'%s',null,null,'123456',null,'%s',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)" % (orgCode[0][0], empiGuid[0][0]))
                self.execQuery("insert into tb_lis_report_indicator(guid,visitStrNo,orgCode,orgName,visitType,reportNo,insItemCode,itemCodeSystem,itemCode,itemName,resultValue,resultUnit,resultFlagCodeSystem,resultFlagCode,resultFlagName,refQuality,refQuantifyLower,refQuantifyUpper,[order],status,createDate,isCurrent,empiGuid) values('1',null,'%s',null,null,'123456',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,'%s')" % (orgCode[0][0], empiGuid[0][0]))

                # 2，检查点

                # # 检查点1.1（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update tb_dc_dm_visit set acr=null where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update t_dic_hospital_info set HospitalLevel='3' where Hospital_id='%s'" % (orgCode[0][0]))
                self.execQuery("update tb_lis_report_indicator set itemName='%s'" % ('ACR'))
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))  # # 第一条随访日期的后2天
                self.runRule("正", ruleSql, idCardNo, "检查点1.1（正向），本次随访管理状态代码 = 1 ，尿微量白蛋白/尿肌酐 = Null，医院等级 = 3，项目名称 = ACR，检验报告日期为第一次随访日期到第二次随访日期之间")

                # # 检查点1.2（正向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], -2))  # 最近一条随访日期的前2天
                self.runRule("正", ruleSql, idCardNo, "检查点1.2（正向），本次随访管理状态代码 = 1 ，尿微量白蛋白/尿肌酐 = Null，医院等级 = 3，项目名称 = ACR，检验报告日期为上一次与本次随访日期之间")

                # # 检查点2（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=Null where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("正", ruleSql, idCardNo, "检查点2（正向），将检查点1中的 本次随访管理状态代码 = Null，其余条件不变")

                # # 检查点3（正向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[-1])
                self.runRule("正", ruleSql, idCardNo, "检查点3（正向），将检查点1中的检验报告日期等于本次随访日期，其余条件不变")

                # # 检查点4（正向）
                self.execQuery("update tb_lis_report_indicator set itemName='尿微量白蛋白肌酐比值'")
                self.runRule("正", ruleSql, idCardNo, "检查点4（正向），将检查点1中的 项目名称 = 尿微量白蛋白肌酐比值，其余条件不变")

                # 检查点5（反向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=2 where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("", ruleSql, idCardNo, "检查点5（反向），将检查点1中的 本次随访管理状态代码 = 2，其余条件不变")
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])

                # 检查点6（反向）
                self.execQuery("update tb_dc_dm_visit set acr='1111' where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("", ruleSql, idCardNo, "检查点6（反向），将检查点1中的 尿微量白蛋白/尿肌酐 = 非Null，其余条件不变")
                self.execQuery("update tb_dc_dm_visit set acr=null where ehrNum='%s'" % ehrNum[0][0])

                # 检查点7（反向）
                self.execQuery("update t_dic_hospital_info set HospitalLevel='2' where Hospital_id='%s'" % (orgCode[0][0]))
                self.runRule("", ruleSql, idCardNo, "检查点7（反向），将检查点1中的 医院等级 = 2，其余条件不变")
                self.execQuery("update t_dic_hospital_info set HospitalLevel='1' where Hospital_id='%s'" % (orgCode[0][0]))

                # 检查点8（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[0])
                self.runRule("", ruleSql, idCardNo, "检查点8（反向），将检查点1中检验报告日期等于第一次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))

                # 检查点9（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], -2))
                self.runRule("", ruleSql, idCardNo, "检查点9（反向），将检查点1中检验报告日期早于第一次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))

                # 检查点10（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], 2))
                self.runRule("", ruleSql, idCardNo, "检查点10（反向），将检查点1中检验报告日期晚于本次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
            else:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleSql, ", 随访记录必须2条及以上！")
        except:
            Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
            exit()
    def ruleId_e730a482345e4976bb792be43c75788a_6(self, comment, ruleSql, idCardNo):
        # 二级医院有检验结果（ACR）
        print("\n" + comment + ruleSql.center(100, "-"))
        try:
            # 1，数据准备
            ehrNum = self.execQuery(
                "SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
            orgCode = self.execQuery(
                "SELECT  top 1 dm.orgCode FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
            empiGuid = self.execQuery("select guid from tb_empi_index_root where idCardNo='%s'" % idCardNo)
            visitDate = self.execQuery("select visitDate from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
            l_visitDate = []
            for i in range(len(visitDate)):
                l_visitDate.append(str(visitDate[i][0]).split(" ")[0])
            l_visitDate.sort()  # 随访日期从早到晚依次排列

            m = self.execQuery("select count(*) from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
            # 随访记录必须2条以上，涉及到 当前检验报告日期与 上一期，本期日期比对。
            if m[0][0] >1 :
                # 初始化表
                self.execQuery("DELETE FROM tb_lis_report")
                self.execQuery("DELETE FROM tb_lis_report_indicator")
                self.execQuery("insert into tb_lis_report(guid,visitStrNo,orgCode,orgName,visitType,reportNo,name,empiGuid,patientId,specimenTypeCodeSystem,specimenTypeCode,specimenTypeName,reportTypeCodeSystem,reportTypeCode,reportTypeName,reportName,applyDeptCode,applyDeptName,applyDoctorCode,applyDoctorName,reportDoctorCode,reportDoctorName,applyDate,reportDate,orderNo,status,createDate,isCurrent) values('1',null,'%s',null,null,'123456',null,'%s',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)" % (orgCode[0][0], empiGuid[0][0]))
                self.execQuery("insert into tb_lis_report_indicator(guid,visitStrNo,orgCode,orgName,visitType,reportNo,insItemCode,itemCodeSystem,itemCode,itemName,resultValue,resultUnit,resultFlagCodeSystem,resultFlagCode,resultFlagName,refQuality,refQuantifyLower,refQuantifyUpper,[order],status,createDate,isCurrent,empiGuid) values('1',null,'%s',null,null,'123456',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,'%s')" % (orgCode[0][0], empiGuid[0][0]))

                # # 2，检查点

                # # 检查点1.1（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update tb_dc_dm_visit set acr=null where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update t_dic_hospital_info set HospitalLevel='2' where Hospital_id='%s'" % (orgCode[0][0]))
                self.execQuery("update tb_lis_report_indicator set itemName='%s'" % ('ACR'))
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))  # # 第一条随访日期的后2天
                self.runRule("正", ruleSql, idCardNo, "检查点1.1（正向），本次随访管理状态代码 = 1 ，尿微量白蛋白/尿肌酐 = Null，医院等级 = 2，项目名称 = ACR，检验报告日期为第一次随访日期到第二次随访日期之间")

                # # 检查点1.2（正向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], -2))  # 最近一条随访日期的前2天
                self.runRule("正", ruleSql, idCardNo, "检查点1.2（正向），本次随访管理状态代码 = 1 ，尿微量白蛋白/尿肌酐 = Null，医院等级 = 2，项目名称 = ACR，检验报告日期为上一次与本次随访日期之间")

                # # 检查点2（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=Null where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("正", ruleSql, idCardNo, "检查点2（正向），将检查点1中的 本次随访管理状态代码 = Null，其余条件不变")

                # # 检查点3（正向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[-1])
                self.runRule("正", ruleSql, idCardNo, "检查点3（正向），将检查点1中的检验报告日期等于本次随访日期，其余条件不变")

                # # 检查点4（正向）
                self.execQuery("update tb_lis_report_indicator set itemName='尿微量白蛋白肌酐比值'")
                self.runRule("正", ruleSql, idCardNo, "检查点4（正向），将检查点1中的 项目名称 = 尿微量白蛋白肌酐比值，其余条件不变")

                # 检查点5（反向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=2 where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("", ruleSql, idCardNo, "检查点5（反向），将检查点1中的 本次随访管理状态代码 =2，其余条件不变")
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])

                # 检查点6（反向）
                self.execQuery("update tb_dc_dm_visit set acr='1111' where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("", ruleSql, idCardNo, "检查点6（反向），将检查点1中的 尿微量白蛋白/尿肌酐 = 非Null，其余条件不变")
                self.execQuery("update tb_dc_dm_visit set acr=null where ehrNum='%s'" % ehrNum[0][0])

                # 检查点7（反向）
                self.execQuery("update t_dic_hospital_info set HospitalLevel='3' where Hospital_id='%s'" % (orgCode[0][0]))
                self.runRule("", ruleSql, idCardNo, "检查点7（反向），将检查点1中的 医院等级 = 3，其余条件不变")
                self.execQuery("update t_dic_hospital_info set HospitalLevel='1' where Hospital_id='%s'" % (orgCode[0][0]))

                # 检查点8（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[0])
                self.runRule("", ruleSql, idCardNo, "检查点8（反向），将检查点1中检验报告日期等于第一次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))

                # 检查点9（反向）
                self.execQuery(
                    "update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], -2))
                self.runRule("", ruleSql, idCardNo, "检查点9（反向），将检查点1中检验报告日期早于第一次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))

                # 检查点10（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], 2))
                self.runRule("", ruleSql, idCardNo, "检查点10（反向），将检查点1中检验报告日期晚于本次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
            else:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleSql, ", 随访记录必须2条及以上！")
        except:
            Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
            exit()

    def ruleId_17ff3dd2fe5c4b41a766b130d1333e73_8(self, comment, ruleSql, idCardNo):
        # 与二级医院实验室检验结果逻辑不符合（总胆固醇）
        print("\n" + comment + ruleSql.center(100, "-"))
        try:
            # 1，数据准备
            ehrNum = self.execQuery(
                "SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
            orgCode = self.execQuery(
                "SELECT  top 1 dm.orgCode FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
            empiGuid = self.execQuery("select guid from tb_empi_index_root where idCardNo='%s'" % idCardNo)

            visitDate = self.execQuery("select visitDate from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
            l_visitDate = []
            for i in range(len(visitDate)):
                l_visitDate.append(str(visitDate[i][0]).split(" ")[0])
            l_visitDate.sort()  # 随访日期从早到晚依次排列

            m = self.execQuery("select count(*) from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
            # 随访记录必须2条以上，涉及到 当前检验报告日期与 上一期，本期日期比对。
            if m[0][0] >1 :
                # 初始化表
                self.execQuery("DELETE FROM tb_lis_report")
                self.execQuery("DELETE FROM tb_lis_report_indicator")
                self.execQuery(
                    "insert into tb_lis_report(guid,visitStrNo,orgCode,orgName,visitType,reportNo,name,empiGuid,patientId,specimenTypeCodeSystem,specimenTypeCode,specimenTypeName,reportTypeCodeSystem,reportTypeCode,reportTypeName,reportName,applyDeptCode,applyDeptName,applyDoctorCode,applyDoctorName,reportDoctorCode,reportDoctorName,applyDate,reportDate,orderNo,status,createDate,isCurrent) values('1',null,'%s',null,null,'123456',null,'%s',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)" % (
                    orgCode[0][0], empiGuid[0][0]))
                self.execQuery(
                    "insert into tb_lis_report_indicator(guid,visitStrNo,orgCode,orgName,visitType,reportNo,insItemCode,itemCodeSystem,itemCode,itemName,resultValue,resultUnit,resultFlagCodeSystem,resultFlagCode,resultFlagName,refQuality,refQuantifyLower,refQuantifyUpper,[order],status,createDate,isCurrent,empiGuid) values('1',null,'%s',null,null,'123456',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,'%s')" % (
                    orgCode[0][0], empiGuid[0][0]))

                # # 2，检查点

                # # 检查点1（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update tb_dc_dm_visit set cholesterol=null where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update t_dic_hospital_info set HospitalLevel='2' where Hospital_id='%s'" % (orgCode[0][0]))
                self.execQuery("update tb_lis_report_indicator set itemName='总胆固醇'")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))  # # 第一条随访日期的后2天
                self.runRule("正", ruleSql, idCardNo, "检查点1（正向），本次随访管理状态代码 = 1 ，总胆固醇值 = Null，医院等级 = 2，项目名称 = 总胆固醇，检验报告日期为第一次随访日期到第二次随访日期之间")

                # # # 检查点2（正向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], -2))  # 最近一条随访日期的前2天
                self.runRule("正", ruleSql, idCardNo, "检查点2（正向），将检查点1中的 检验报告日期为上一次与本次随访日期之间，其余条件不变")
                #
                # # # 检查点3（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=Null where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("正", ruleSql, idCardNo, "检查点3（正向），将检查点1中的 本次随访管理状态代码 = Null，其余条件不变")
                #
                # # # 检查点4（正向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[-1])
                self.runRule("正", ruleSql, idCardNo, "检查点4（正向），将检查点1中的检验报告日期等于本次随访日期，其余条件不变")
                #
                # # # 检查点5（反向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=2 where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("", ruleSql, idCardNo, "检查点5（正向），将检查点1中的 本次随访管理状态代码 = 2，其余条件不变")
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                #
                # # 检查点6（反向）
                self.execQuery("update tb_dc_dm_visit set cholesterol ='11111' where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("", ruleSql, idCardNo, "检查点6（反向），将检查点1中的 总胆固醇值 <> Null，其余条件不变")
                #
                # # 检查点7（反向）
                self.execQuery("update t_dic_hospital_info set HospitalLevel='1' where Hospital_id='%s'" % (orgCode[0][0]))
                self.runRule("", ruleSql, idCardNo, "检查点7（反向），将检查点1中的 医院级别 = 1 ，其余条件不变")
                self.execQuery("update t_dic_hospital_info set HospitalLevel='1' where Hospital_id='%s'" % (orgCode[0][0]))
                #
                # # 检查点8（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[0])
                self.runRule("", ruleSql, idCardNo, "检查点8（反向），将检查点1中检验报告日期等于第一次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
                #
                # # 检查点9（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], -2))
                self.runRule("", ruleSql, idCardNo, "检查点9（反向），将检查点1中检验报告日期早于第一次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
                #
                # # 检查点10（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], 2))
                self.runRule("", ruleSql, idCardNo, "检查点10（反向），将检查点1中检验报告日期晚于本次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
            else:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleSql, ", 随访记录必须2条及以上！")
        except:
            Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
            exit()
    def ruleId_27b9cb4fc53d48baac87fc22ad4414be_9(self, comment, ruleSql, idCardNo):
        # 与三级医院实验室检验结果逻辑不符合（总胆固醇）
        print("\n" + comment + ruleSql.center(100, "-"))
        try:
            # 1，数据准备
            ehrNum = self.execQuery(
                "SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
            orgCode = self.execQuery(
                "SELECT  top 1 dm.orgCode FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
            empiGuid = self.execQuery("select guid from tb_empi_index_root where idCardNo='%s'" % idCardNo)

            visitDate = self.execQuery("select visitDate from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
            l_visitDate = []
            for i in range(len(visitDate)):
                l_visitDate.append(str(visitDate[i][0]).split(" ")[0])
            l_visitDate.sort()  # 随访日期从早到晚依次排列

            m = self.execQuery("select count(*) from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
            # 随访记录必须2条以上，涉及到 当前检验报告日期与 上一期，本期日期比对。
            if m[0][0] >1 :
                # 初始化表
                self.execQuery("DELETE FROM tb_lis_report")
                self.execQuery("DELETE FROM tb_lis_report_indicator")
                self.execQuery(
                    "insert into tb_lis_report(guid,visitStrNo,orgCode,orgName,visitType,reportNo,name,empiGuid,patientId,specimenTypeCodeSystem,specimenTypeCode,specimenTypeName,reportTypeCodeSystem,reportTypeCode,reportTypeName,reportName,applyDeptCode,applyDeptName,applyDoctorCode,applyDoctorName,reportDoctorCode,reportDoctorName,applyDate,reportDate,orderNo,status,createDate,isCurrent) values('1',null,'%s',null,null,'123456',null,'%s',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)" % (
                    orgCode[0][0], empiGuid[0][0]))
                self.execQuery(
                    "insert into tb_lis_report_indicator(guid,visitStrNo,orgCode,orgName,visitType,reportNo,insItemCode,itemCodeSystem,itemCode,itemName,resultValue,resultUnit,resultFlagCodeSystem,resultFlagCode,resultFlagName,refQuality,refQuantifyLower,refQuantifyUpper,[order],status,createDate,isCurrent,empiGuid) values('1',null,'%s',null,null,'123456',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,'%s')" % (
                    orgCode[0][0], empiGuid[0][0]))

                # # 2，检查点

                # # 检查点1（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update tb_dc_dm_visit set cholesterol=null where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update t_dic_hospital_info set HospitalLevel='3' where Hospital_id='%s'" % (orgCode[0][0]))
                self.execQuery("update tb_lis_report_indicator set itemName='总胆固醇'")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))  # # 第一条随访日期的后2天
                self.runRule("正", ruleSql, idCardNo, "检查点1（正向），本次随访管理状态代码 = 1 ，总胆固醇值 = Null，医院等级 = 3，项目名称 = 总胆固醇，检验报告日期为第一次随访日期到第二次随访日期之间")

                # # # 检查点2（正向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], -2))  # 最近一条随访日期的前2天
                self.runRule("正", ruleSql, idCardNo, "检查点2（正向），将检查点1中的 检验报告日期为上一次与本次随访日期之间，其余条件不变")
                #
                # # # 检查点3（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=Null where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("正", ruleSql, idCardNo, "检查点3（正向），将检查点1中的 本次随访管理状态代码 = Null，其余条件不变")
                #
                # # # 检查点4（正向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[-1])
                self.runRule("正", ruleSql, idCardNo, "检查点4（正向），将检查点1中的检验报告日期等于本次随访日期，其余条件不变")
                #
                # # # 检查点5（反向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=2 where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("", ruleSql, idCardNo, "检查点5（正向），将检查点1中的 本次随访管理状态代码 = 2，其余条件不变")
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                #
                # # 检查点6（反向）
                self.execQuery("update tb_dc_dm_visit set cholesterol ='11111' where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("", ruleSql, idCardNo, "检查点6（反向），将检查点1中的 总胆固醇值 <> Null，其余条件不变")
                #
                # # 检查点7（反向）
                self.execQuery("update t_dic_hospital_info set HospitalLevel='2' where Hospital_id='%s'" % (orgCode[0][0]))
                self.runRule("", ruleSql, idCardNo, "检查点7（反向），将检查点1中的 医院级别 = 2 ，其余条件不变")
                self.execQuery("update t_dic_hospital_info set HospitalLevel='1' where Hospital_id='%s'" % (orgCode[0][0]))
                #
                # # 检查点8（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[0])
                self.runRule("", ruleSql, idCardNo, "检查点8（反向），将检查点1中检验报告日期等于第一次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
                #
                # # 检查点9（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], -2))
                self.runRule("", ruleSql, idCardNo, "检查点9（反向），将检查点1中检验报告日期早于第一次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
                #
                # # 检查点10（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], 2))
                self.runRule("", ruleSql, idCardNo, "检查点10（反向），将检查点1中检验报告日期晚于本次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
            else:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleSql, ", 随访记录必须2条及以上！")
        except:
            Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
            exit()
    def ruleId_711d9d2122884c74992c8c6c30da738f_10(self, comment, ruleSql, idCardNo):
        # 与一级医院实验室检验结果逻辑不符合（总胆固醇）
        print("\n" + comment + ruleSql.center(100, "-"))
        try:
            # 1，数据准备
            ehrNum = self.execQuery(
                "SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
            orgCode = self.execQuery(
                "SELECT  top 1 dm.orgCode FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)
            empiGuid = self.execQuery("select guid from tb_empi_index_root where idCardNo='%s'" % idCardNo)

            visitDate = self.execQuery("select visitDate from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
            l_visitDate = []
            for i in range(len(visitDate)):
                l_visitDate.append(str(visitDate[i][0]).split(" ")[0])
            l_visitDate.sort()  # 随访日期从早到晚依次排列

            m = self.execQuery("select count(*) from  tb_dc_dm_visit where ehrNum = '%s'" % ehrNum[0][0])
            # 随访记录必须2条以上，涉及到 当前检验报告日期与 上一期，本期日期比对。
            if m[0][0] >1 :
                # 初始化表
                self.execQuery("DELETE FROM tb_lis_report")
                self.execQuery("DELETE FROM tb_lis_report_indicator")
                self.execQuery(
                    "insert into tb_lis_report(guid,visitStrNo,orgCode,orgName,visitType,reportNo,name,empiGuid,patientId,specimenTypeCodeSystem,specimenTypeCode,specimenTypeName,reportTypeCodeSystem,reportTypeCode,reportTypeName,reportName,applyDeptCode,applyDeptName,applyDoctorCode,applyDoctorName,reportDoctorCode,reportDoctorName,applyDate,reportDate,orderNo,status,createDate,isCurrent) values('1',null,'%s',null,null,'123456',null,'%s',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)" % (
                    orgCode[0][0], empiGuid[0][0]))
                self.execQuery(
                    "insert into tb_lis_report_indicator(guid,visitStrNo,orgCode,orgName,visitType,reportNo,insItemCode,itemCodeSystem,itemCode,itemName,resultValue,resultUnit,resultFlagCodeSystem,resultFlagCode,resultFlagName,refQuality,refQuantifyLower,refQuantifyUpper,[order],status,createDate,isCurrent,empiGuid) values('1',null,'%s',null,null,'123456',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,'%s')" % (
                    orgCode[0][0], empiGuid[0][0]))

                # # 2，检查点

                # # 检查点1（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update tb_dc_dm_visit set cholesterol=null where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update t_dic_hospital_info set HospitalLevel='1' where Hospital_id='%s'" % (orgCode[0][0]))
                self.execQuery("update tb_lis_report_indicator set itemName='总胆固醇'")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))  # # 第一条随访日期的后2天
                self.runRule("正", ruleSql, idCardNo, "检查点1（正向），本次随访管理状态代码 = 1 ，总胆固醇值 = Null，医院等级 = 1，项目名称 = 总胆固醇，检验报告日期为第一次随访日期到第二次随访日期之间")

                # # # 检查点2（正向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], -2))  # 最近一条随访日期的前2天
                self.runRule("正", ruleSql, idCardNo, "检查点2（正向），将检查点1中的 检验报告日期为上一次与本次随访日期之间，其余条件不变")
                #
                # # # 检查点3（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=Null where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("正", ruleSql, idCardNo, "检查点3（正向），将检查点1中的 本次随访管理状态代码 = Null，其余条件不变")
                #
                # # # 检查点4（正向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[-1])
                self.runRule("正", ruleSql, idCardNo, "检查点4（正向），将检查点1中的检验报告日期等于本次随访日期，其余条件不变")
                #
                # # # 检查点5（反向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=2 where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("", ruleSql, idCardNo, "检查点5（正向），将检查点1中的 本次随访管理状态代码 = 2，其余条件不变")
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                #
                # # 检查点6（反向）
                self.execQuery("update tb_dc_dm_visit set cholesterol ='11111' where ehrNum='%s'" % ehrNum[0][0])
                self.runRule("", ruleSql, idCardNo, "检查点6（反向），将检查点1中的 总胆固醇值 <> Null，其余条件不变")
                #
                # # 检查点7（反向）
                self.execQuery("update t_dic_hospital_info set HospitalLevel='2' where Hospital_id='%s'" % (orgCode[0][0]))
                self.runRule("", ruleSql, idCardNo, "检查点7（反向），将检查点1中的 医院级别 = 2 ，其余条件不变")
                self.execQuery("update t_dic_hospital_info set HospitalLevel='1' where Hospital_id='%s'" % (orgCode[0][0]))
                #
                # # 检查点8（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % l_visitDate[0])
                self.runRule("", ruleSql, idCardNo, "检查点8（反向），将检查点1中检验报告日期等于第一次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
                #
                # # 检查点9（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], -2))
                self.runRule("", ruleSql, idCardNo, "检查点9（反向），将检查点1中检验报告日期早于第一次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
                #
                # # 检查点10（反向）
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[-1], 2))
                self.runRule("", ruleSql, idCardNo, "检查点10（反向），将检查点1中检验报告日期晚于本次随访日期，其余条件不变")
                self.execQuery("update tb_lis_report set reportDate='%s'" % Time_PO.getBeforeAfterDate(l_visitDate[0], 2))
            else:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleSql, ", 随访记录必须2条及以上！")
        except:
            Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
            exit()

