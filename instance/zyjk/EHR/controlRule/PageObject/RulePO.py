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
        self.Log_PO = LogPO(logFile, fmt='%(levelname)s - %(message)s - %(asctime)s')  # 输出日志


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
    def runRule(self, varWay, ruleId, ruleSql, idCard, varMsg):

        # 1） 执行质控
        os.system('curl -X  GET "http://192.168.0.243:8090/healthRecordRules/rulesEngine/execute/' + str(idCard) + '" -H  "accept: */*" -o /dev/null -s')
        # 2） 检查结果
        result = self.execQuery("select * from HrRule r1 inner join HrRuleRecord r2 on r1.RuleId=r2.RuleId where r2.ArchiveNum='%s' AND r1.RuleSql='%s'" % (idCard, ruleSql))
        if varWay == "p":
            # 正向测试
            if len(result) > 0:
                Color_PO.consoleColor("31", "36", "[OK]" + ruleId, varMsg)
            else:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleId, varMsg)
        else:
            # 反向测试
            if len(result) > 0:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleId, varMsg)
            else:
                Color_PO.consoleColor("31", "33", "[OK]" + ruleId, varMsg)

    # 规则2
    def test2(self, ruleId, ruleSql, *var):

        try:
            # 1，获取测试数据(判断记录是否存在)
            n = self.execQuery("select count(*) from tb_empi_index_root where idCardNo='%s'" % var[0])  # # 用户身份证
            m = self.execQuery("select count(*) from tb_dc_dm_visit where ehrNum='%s'" % var[1])  # 档案编号
            if n[0][0] == 1 and m[0][0] > 0 :
                vistStatusCode = self.execQuery("select vistStatusCode from (select top 1 * from tb_dc_dm_visit where ehrNum='%s' order by visitDate desc) as a" % var[1])
                drugName = self.execQuery("select drugName from tb_dc_dm_usedrug")
                # print(vistStatusCode)
                # print(drugName)

                # 检查点1（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=Null where ehrNum='%s'" % var[1])
                self.execQuery("update tb_dc_dm_usedrug set drugName=Null")
                self.runRule("p", ruleId, ruleSql, var[0], "检查点1（正向），将 vistStatusCode 值改为 Null 且药物名称为空值")

                # 检查点2（正向）
                self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % var[1])
                self.execQuery("update tb_dc_dm_usedrug set drugName=Null")
                self.runRule("p", ruleId, ruleSql, var[0], "检查点2（正向），将 vistStatusCode 值改为 1")

                # 检查点3（正向）
                if vistStatusCode[0][0] != None and vistStatusCode[0][0] !='1':
                    self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % var[1])
                    self.execQuery("update tb_dc_dm_usedrug set drugName=Null")
                    self.runRule("p", ruleId, ruleSql, var[0], "检查点3（正向），将 vistStatusCode 值改为 1")

                # 检查点4（正向）
                if drugName[0][0] != None:
                    self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % var[1])
                    self.execQuery("update tb_dc_dm_usedrug set drugName=Null")
                    self.runRule("p", ruleId, var[0], "检查点4（正向），将drugName 值改为 Null")

                # 检查点5（反向）
                if vistStatusCode[0][0] != None and vistStatusCode[0][0] != '1':
                    self.execQuery("update tb_dc_dm_visit set vistStatusCode='%s' where ehrNum='%s'" % (vistStatusCode[0][0], var[1]))
                    self.execQuery("update tb_dc_dm_usedrug set drugName=Null")
                    self.runRule("n", ruleId, ruleSql, var[0], "检查点5（反向），将 vistStatusCode 值改为 非1非Null ")

                # 检查点6（反向）
                if drugName[0][0] != None:
                    self.execQuery("update tb_dc_dm_visit set vistStatusCode=1 where ehrNum='%s'" % var[1])
                    self.execQuery("update tb_dc_dm_usedrug set drugName='%s'" % drugName[0][0])
                    self.runRule("n", ruleId, ruleSql, var[0], "检查点6（反向），将drugName 值改为 非Null")

                # 3，恢复测试数据
                if vistStatusCode[0][0] == None:
                    self.execQuery("update tb_dc_dm_visit set vistStatusCode=Null where ehrNum='%s'" % (var[1]))
                else:
                    self.execQuery("update tb_dc_dm_visit set vistStatusCode='%s' where ehrNum='%s'" % (vistStatusCode[0][0], var[1]))
                if drugName[0][0] == None :
                    self.execQuery("update  tb_dc_dm_usedrug  set  drugName=Null")
                else:
                    self.execQuery("update  tb_dc_dm_usedrug  set  drugName='%s'" % str(drugName[0][0]))
            else:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleId, "测试数据不存在!")
        except:
            Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
            exit()

    # 规则3
    def test3(self, ruleId, ruleSql, *var):

        try:
            # 1，获取测试数据(判断记录是否存在)
            n = self.execQuery("select count(*) from tb_empi_index_root where idCardNo='%s'" % var[0])
            if n[0][0] == 1 :
                self.execQuery("DELETE FROM tb_dc_dm_usedrug")
                self.execQuery("insert into tb_dc_dm_usedrug(guid,visitId,orgCode,drugTypeCodeSystem,drugTypeCode,drugTypeName,drugCode,drugName,eachDose,referenceDose,unit,totalDose,useWayCodeSystem,useWayCode,useWayName,frequency,cnDrugCodeSystem,cnDrugCode,cnDrugName) values('1',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)")
                visitId, orgCode = self.execQuery("select cardId,orgCode from tb_dc_dm_visit   where  ehrNum='%s' order by visitDate desc" % var[1])
                # print(visitId[0])
                # print(orgCode[1])

                # 2，检查点
                # # 检查点1（反向）
                self.runRule("n", ruleId, ruleSql, var[0], "检查点1（反向），药物名称与药物类型都为 Null")

                # 检查点2（正向）
                self.execQuery("update  tb_dc_dm_usedrug set  visitId='%s'" % str(visitId[0]))
                self.execQuery("update  tb_dc_dm_usedrug set  orgCode='%s'" % str(orgCode[1]))
                self.execQuery("update  tb_dc_dm_usedrug set  drugName='%s'" % '二甲双胍')
                self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName='%s'" % '中成药')
                self.runRule("p", ruleId, ruleSql, var[0], "检查点2（正向），药品名称与药物类型匹配不一致")

                # 检查点3（反向）
                self.execQuery("update  tb_dc_dm_usedrug set  visitId='%s'" % str(visitId[0]))
                self.execQuery("update  tb_dc_dm_usedrug set  orgCode='%s'" % str(orgCode[1]))
                self.execQuery("update  tb_dc_dm_usedrug set  drugName='%s'" % '二甲双胍')
                self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName='%s'" % '双胍类')
                self.runRule("", ruleId, ruleSql, var[0], "检查点3（反向），药品名称与药物类型匹配一致")

                # 检查点4（反向）
                self.execQuery("update  tb_dc_dm_usedrug set  visitId='%s'" % str(visitId[0]))
                self.execQuery("update  tb_dc_dm_usedrug set  orgCode='%s'" % str(orgCode[1]))
                self.execQuery("update  tb_dc_dm_usedrug set  drugName='%s'" % '二甲双胍')
                self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName=Null")
                self.runRule("", ruleId, ruleSql, var[0], "检查点4（反向），药物名称不为空，药物类型为空")

                # 检查点5（反向）
                self.execQuery("update  tb_dc_dm_usedrug set  visitId='%s'" % str(visitId[0]))
                self.execQuery("update  tb_dc_dm_usedrug set  orgCode='%s'" % str(orgCode[1]))
                self.execQuery("update  tb_dc_dm_usedrug set  drugName=Null")
                self.execQuery("update  tb_dc_dm_usedrug set  drugTypeName='%s'" % '磺脲类')
                self.runRule("", ruleId, ruleSql, var[0], "检查点5（反向），药物名称为空，药物类型不为空")


            else:
                Color_PO.consoleColor("31", "31", "[ERROR]" + ruleId, "测试数据不存在!")
        except:
            Color_PO.consoleColor("31", "33", "[WARNING]", "数据库执行时报错!")
            exit()


