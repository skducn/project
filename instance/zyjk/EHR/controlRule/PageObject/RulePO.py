# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-5-12
# Description: 质控对象库
# 依据：D:\1zy\6 研发二部\1 电子健康档案\2.3.1\V2.3.1开发测试任务.xlsx
# *****************************************************************

from instance.zyjk.EHR.controlRule.config.config import *


class RulePO(object):

    def __init__(self):
        self.Time_PO = TimePO()
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
    def runRule(self, varWay, ruleSql, idCard, varMsg):

        # 1） 执行质控
        os.system('curl -X  GET "http://192.168.0.243:8090/healthRecordRules/rulesEngine/execute/' + str(idCard) + '" -H  "accept: */*" -o /dev/null -s')
        # 2） 检查结果
        result = self.execQuery("select * from HrRule r1 inner join HrRuleRecord r2 on r1.RuleId=r2.RuleId where r2.ArchiveNum='%s' AND r1.RuleSql='%s'" % (idCard, ruleSql))
        if varWay == "":
            # 反向测试
            if len(result) > 0:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleSql, varMsg)
            else:
                Color_PO.consoleColor("31", "33", "[OK]" + ruleSql, varMsg)
        else:
            # 正向测试
            if len(result) > 0:
                Color_PO.consoleColor("31", "36", "[OK]" + ruleSql, varMsg)
            else:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleSql, varMsg)

    # 规则2
    def test2(self, ruleSql, idCardNo):

        try:
            # 1，获取测试数据(判断记录是否存在)
            n = self.execQuery("select count(*) from tb_empi_index_root where idCardNo='%s'" % idCardNo)  # # 用户身份证
            ehrNum = self.execQuery(
                "SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)

            if n[0][0] == 1 :
                vistStatusCode = self.execQuery("select vistStatusCode from (select top 1 * from tb_dc_dm_visit where ehrNum='%s' order by visitDate desc) as a" % ehrNum[0][0])
                drugName = self.execQuery("select drugName from tb_dc_dm_usedrug")
                # print(vistStatusCode)
                # print(drugName)

                # 检查点1（正向）,随访管理状态vistStatusCode值为Null 且 药物名称为Null
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=Null where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update tb_dc_dm_usedrug set drugName=Null")
                self.runRule("正向", ruleSql, idCardNo, "检查点1（正向），随访管理状态vistStatusCode值为Null 且 药物名称为Null")

                # 检查点2（正向）,随访管理状态vistStatusCode值为1 且 药物名称为Null
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update tb_dc_dm_usedrug set drugName=Null")
                self.runRule("正向", ruleSql, idCardNo, "检查点2（正向），随访管理状态vistStatusCode值为1 且 药物名称为Null")

                # 检查点3（反向）,随访管理状态vistStatusCode值为1 且 药物名称不为Null
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update tb_dc_dm_usedrug set drugName = '111111'")
                self.runRule("", ruleSql, idCardNo, "检查点3（正向），随访管理状态vistStatusCode值为1 且 药物名称不为Null")

                # 检查点4（反向），随访管理状态vistStatusCode值为2 且 药物名称为Null
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=2 where ehrNum='%s'" % ehrNum[0][0])
                self.execQuery("update tb_dc_dm_usedrug set drugName=Null")
                self.runRule("", ruleSql, idCardNo, "检查点4（正向），随访管理状态vistStatusCode值为2 且 药物名称为Null")

                # 检查点5（反向），随访管理状态vistStatusCode值为2 且 药物名称不为Null
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=2 where ehrNum='%s'" % (ehrNum[0][0]))
                self.execQuery("update tb_dc_dm_usedrug set drugName = '111111'")
                self.runRule("", ruleSql, idCardNo, "检查点5（反向），随访管理状态vistStatusCode值为2 且 药物名称不为Null")

            else:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleSql, ", " + str(idCardNo) + " 不存在！")
        except:
            Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
            exit()

    # 规则3
    def test3(self, ruleSql, idCardNo):

        try:
            # 1，获取测试数据(判断记录是否存在)
            n = self.execQuery("select count(*) from tb_empi_index_root where idCardNo='%s'" % idCardNo)
            ehrNum = self.execQuery(
                "SELECT  top 1 dm.ehrNum FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % idCardNo)

            if n[0][0] == 1 :
                self.execQuery("DELETE FROM tb_dc_dm_usedrug")  # 初始化此表，删除里面所有的记录。
                self.execQuery("insert into tb_dc_dm_usedrug(guid,visitId,orgCode,drugTypeCodeSystem,drugTypeCode,drugTypeName,drugCode,drugName,eachDose,referenceDose,unit,totalDose,useWayCodeSystem,useWayCode,useWayName,frequency,cnDrugCodeSystem,cnDrugCode,cnDrugName) values('1',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)")
                # 从tb_dc_dm_visit获取cardId和 orgCode值，更新到刚才新增的记录对应字段（visit Id，orgCode）中.
                visitId, orgCode = self.execQuery("select cardId,orgCode from tb_dc_dm_visit   where  ehrNum='%s' order by visitDate desc" % ehrNum[0][0])
                # print(visitId[0])
                # print(orgCode[1])
                self.execQuery("update  tb_dc_dm_usedrug set  visitId='%s'" % str(visitId[0]))
                self.execQuery("update  tb_dc_dm_usedrug set  orgCode='%s'" % str(orgCode[1]))

                # 2，检查点
                # # 检查点1（反向）,药物名称与药物类型都为 Null
                self.runRule("", ruleSql, idCardNo, "检查点1（反向），药物名称与药物类型都为 Null")

                # 检查点2（反向）,药物名称不为Null，药物类型为Null
                self.execQuery("update  tb_dc_dm_usedrug set  drugName='%s'" % '二甲双胍')
                self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName=Null")
                self.runRule("", ruleSql, idCardNo, "检查点2（反向），药物名称不为Null，药物类型为Null")

                # 检查点3（反向）,药物名称为Null，药物类型不为Null
                self.execQuery("update  tb_dc_dm_usedrug set  drugName=Null")
                self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName='%s'" % '磺脲类')
                self.runRule("", ruleSql, idCardNo, "检查点3（反向），药物名称为Null，药物类型不为Null")

                # 抽样 糖尿病用药列表（跑 2 条）
                # # 检查点4（正向）,药品名称与药物类型匹配不一致（抽样）
                # self.execQuery("update  tb_dc_dm_usedrug set  drugName='%s'" % '二甲双胍')
                # self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName='%s'" % '中成药')
                # self.runRule("正向", ruleSql, idCardNo, "检查点4（正向），药品名称与药物类型匹配不一致")
                #
                # # 检查点5（反向）,药品名称与药物类型匹配一致（抽样）
                # self.execQuery("update  tb_dc_dm_usedrug set  drugName='%s'" % '二甲双胍')
                # self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName='%s'" % '双胍类')
                # self.runRule("", ruleSql, idCardNo, "检查点5（反向），药品名称与药物类型匹配一致")

                # 全遍历 糖尿病用药列表（跑 450 条）
                l_drugName = self.l_diabetes[0]
                l_drugTypeName = self.l_diabetes[1]
                dict1 = List_PO.lists2dict(l_drugName, l_drugTypeName)
                l_drugTypeNameDelRepeat = List_PO.listDelRepeat(l_drugTypeName)
                for i in range(len(l_drugName)):
                    for j in range(len(l_drugTypeNameDelRepeat)):
                        self.execQuery("update  tb_dc_dm_usedrug set  drugName='%s'" % l_drugName[i])
                        self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName='%s'" % l_drugTypeNameDelRepeat[j])
                        for k, v in dict1.items():
                            youxiao=0
                            if k == l_drugName[i] and v == l_drugTypeNameDelRepeat[j]:
                                youxiao=1
                                break
                        if youxiao == 1:
                            self.runRule("", ruleSql, idCardNo, "检查点（反向），药品名称【" + l_drugName[i] + "】与药物类型【" + l_drugTypeNameDelRepeat[j] + "】匹配一致")
                        else:
                            self.runRule("正向", ruleSql, idCardNo, "检查点（正向），药品名称【" + l_drugName[i] + "】与药物类型【" + l_drugTypeNameDelRepeat[j] + "】匹配不一致")

            else:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleSql, ", " + str(idCardNo) + " 不存在！")
        except:
            Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
            exit()


