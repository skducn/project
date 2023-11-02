# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-8-1
# Description: CHC包
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"), "utf8")  # 测试环境

from PO.StrPO import *
Str_PO = StrPO()
from PO.ColorPO import *
Color_PO = ColorPO()
from PO.TimePO import *
Time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.DictPO import *
Dict_PO = DictPO()
from PO.DataPO import *
Data_PO = DataPO()
from PO.OpenpyxlPO import *
import random

class ChcRulePO2():

    def __init__(self, dbTableName):

        self.TOKEN = self.getToken(Configparser_PO.USER("user"), Configparser_PO.USER("password"))
        self.dbTableName = dbTableName

    def getToken(self, varUser, varPass):

        # 1,获取登录用户的token
        command = "curl -X POST \"" + Configparser_PO.HTTP("url") + ":8012/login\" -H \"accept: */*\" -H \"Content-Type: application/json\" -d \"{ \\\"password\\\": \\\"" + str(varPass) + "\\\", \\\"username\\\": \\\"" + str(varUser) + "\\\"}\""
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        if Configparser_PO.SWITCH("token") == "on":
            print(d_r['data']['access_token'])
        return d_r['data']['access_token']

    def getDiseaseIdcard(self):

        '''
        获取疾病身份证中对应疾病的身份证号码
        :param
        :return: 
        '''

        l_d_diseaseRuleCode_idcard = Sqlserver_PO.execQuery("select diseaseRuleCode, idcard from 疾病身份证")
        # print(l_d_diseaseRuleCode_idcard)  # [{'diseaseRuleCode': 'YH_JB001', 'idcard': 310101202308070001}, {'diseaseRuleCode': 'YH_JB002', 'idcard': 310101202308070002}, ...]
        return (l_d_diseaseRuleCode_idcard)

    def i_rerunExecuteRule(self, varId):

        '''
        重新评估 
        :param var:
        :param token:
        :return:
        '''

        command = "curl -X GET \"" + Configparser_PO.HTTP("url") + ":8011/server/tAssessInfo/rerunExecuteRule/" + str(varId) + "\" -H \"accept: */*\" -H \"Content-Type: application/json\" -H \"Authorization:" + str(self.TOKEN) + "\""
        if Configparser_PO.SWITCH("printInterface") == "on":
            print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        sleep(2)
        if Configparser_PO.SWITCH("printInterface") == "on":
            Color_PO.consoleColor("31", "33", str_r, "")

        if 'code' in d_r:
            if d_r['code'] != 200:
                if Configparser_PO.SWITCH("printsql") == "on":
                    Color_PO.consoleColor("31", "31", str_r, "")
                self.log = self.log + "\n" + str_r
                return ([{'name':'重新评估', 'value' : "[ERROR => i_rerunExecuteRule() => " + str(str_r) + "]"}])
            else:
                if Configparser_PO.SWITCH("printsql") == "on":
                    Color_PO.consoleColor("31", "36", "i_rerunExecuteRule => 重新评估 => " + str_r, "")
                # return ([{'name':'重新评估', 'value': 200}])
        else:
            if Configparser_PO.SWITCH("printsql") == "on":
                Color_PO.consoleColor("31", "31", str_r, "")
            self.log = self.log + "\n" + str_r
            # 如：{"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            return ([{'name':'重新评估', 'value': "[ERROR => i_rerunExecuteRule() => " + str(str_r) + "]"}])

    def i_startAssess(self, varIdcard):

        '''
        新增评估
        :param varIdcard:
        :param token:
        :return:
        '''

        self.verifyIdcard(varIdcard)
        command = "curl -X POST \"" + Configparser_PO.HTTP("url") + ":8014/tAssessInfo/startAssess\" -H \"token:" + \
                  self.TOKEN + "\" -H \"Request-Origion:SwaggerBootstrapUi\" -H \"accept:*/*\" -H \"Authorization:\" " \
                               "-H \"Content-Type:application/json\" -d \"{\\\"categoryCode\\\":\\\"\\\",\\\"idCard\\\":\\\"" + str(varIdcard) + "\\\",\\\"orgCode\\\":\\\"\\\"}\""
        if Configparser_PO.SWITCH("printInterface") == "on":
            print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        sleep(2)
        if Configparser_PO.SWITCH("printInterface") == "on":
            Color_PO.consoleColor("31", "33", str_r, "")

        if 'code' in d_r:
            if d_r['code'] != 200:
                # Color_PO.consoleColor("31", "31", str_r, "")
                if Configparser_PO.SWITCH("printsql") == "on":
                    Color_PO.consoleColor("31", "31", str_r, "")
                self.log = self.log + "\n" + str_r
                return ([{'name':'新增评估', 'value' : "[ERROR => i_startAssess() => " + str(str_r) + "]"}])
            else:
                if Configparser_PO.SWITCH("printsql") == "on":
                    Color_PO.consoleColor("31", "36", "self.i_startAssess => 新增评估 => " + str_r, "")
                # return ([{'name':'新增评估', 'value': 200}])
        else:
            if Configparser_PO.SWITCH("printsql") == "on":
                Color_PO.consoleColor("31", "31", str_r, "")
            self.log = self.log + "\n" + str_r
            # 如：{"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            return ([{'name':'新增评估', 'value': "[ERROR => i_startAssess() => " + str(str_r) + "]"}])

    def sql(self, varSql):

        '''
        执行sql
        :param varSql:
        :param TOKEN:
        :return:
        '''
        # print(varSql)
        if 'self.' in varSql:
            a = eval(varSql)
            return a
        else:
            varPrefix = varSql.split(" ")[0]
            varPrefix = varPrefix.lower()
            if varPrefix == 'select':
                command = 'Sqlserver_PO.execQuery("' + varSql + '")'
                a = eval(command)
                sleep(1)
                return a
            elif varPrefix == 'update' or varPrefix == 'insert' or varPrefix == 'delete' :
                command = 'Sqlserver_PO.execute("' + varSql + '")'
                a = eval(command)
                sleep(1)
                return a
            else:
                return None



    def outResult1(self, varQty):

        if varQty == 1:
            Color_PO.consoleColor("31", "36", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => OK]"), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, Time_PO.getDateTimeByDivide(), self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))
        else:
            print("step log".center(100, "-"))
            print(self.log)
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => ERROR]"), "")
            Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, self.log, self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))

    def outResult2(self, varQty):

        if varQty == 2:
            Color_PO.consoleColor("31", "36", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => OK]"), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, Time_PO.getDateTimeByDivide(), self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))
        else:
            print("step log".center(100, "-"))
            print(self.log)
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => ERROR]"), "")
            Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, self.log, self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))

    def outResultGW(self, diseaseRuleCode, l_ruleCode, d_expect):

        # print(l_ruleCode)   # ['GW_JB011', 'PG_JWS041', 'PG_JWS043']
        # print(d_expect)   # {'QTY0': 0, 'PG_JWS041': '1', 'PG_JWS043': '1'}
        l_ruleCode.remove(diseaseRuleCode) #  ['PG_JWS041', 'PG_JWS043']
        # print(l_ruleCode)  # ['QTY0', 'PG_JWS041', 'PG_JWS043']
        varSign = 0
        d_actual = {}
        for k, v in d_expect.items():
            if (k == "QTY0" and v == 0) or (k != "QTY0" and v == 1):
                varSign = varSign + 0
                d_actual[k] = v
            else:
                varSign = varSign + 1
                d_actual[k] = v

        # print(varSign)
        if Configparser_PO.SWITCH("printSql") == "on":
            print('预期 => ' + str(d_expect))
            print('实际 => ' + str(d_actual))

        if varSign == 0:
            Color_PO.consoleColor("31", "36", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => OK]"), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, Time_PO.getDateTimeByDivide(), self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))
        else:
            print("step log".center(100, "-"))
            print(self.log)
            print('预期 => ' + str(d_expect))
            print('实际 => ' + str(d_actual))
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => ERROR]"), "")
            Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, self.log, self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))

    def verifyIdcard(self, varIdcard):

        # 检查患者主索引表身份证是否存在!
        l_d_qty = Sqlserver_PO.execQuery("select count(*) as qty from TB_EMPI_INDEX_ROOT where IDCARDNO='%s'" % (varIdcard))
        # print(l_d_qty)  # [{'qty': 1}]
        if l_d_qty[0]['qty'] == 0:
            guid = Data_PO.getFigures(6)
            name = Data_PO.getChineseName()
            Sqlserver_PO.execute("INSERT INTO [TB_EMPI_INDEX_ROOT] ([GUID], [NAME], [SEXCODE], [SEXVALUE], [DATEOFBIRTH], [IDCARDNO]) VALUES ('" + str(guid) + "', N'" + str(name) + "', '2', '女', '1940-05-11', '" + str(varIdcard) + "')")

        # 检查基本信息表身份证是否存在!
        l_d_qty = Sqlserver_PO.execQuery("select count(*) as qty from HRPERSONBASICINFO where IDCARD='%s'" % (varIdcard))
        if l_d_qty[0]['qty'] == 0:
            Sqlserver_PO.execute("INSERT INTO [dbo].[HRPERSONBASICINFO] ([ARCHIVENUM], [NAME], [SEX], [DATEOFBIRTH], [IDCARD], [WORKUNIT], [PHONE], [CONTACTSNAME], [CONTACTSPHONE], [RESIDENCETYPE], [NATIONCODE], [BLOODTYPE], [RHBLOODTYPE], [DEGREE], [OCCUPATION], [MARITALSTATUS], [HEREDITYHISTORYFLAG], [HEREDITYHISTORYCODE], [ENVIRONMENTKITCHENAERATION], [ENVIRONMENTFUELTYPE], [ENVIRONMENTWATER], [ENVIRONMENTTOILET], [ENVIRONMENTCORRAL], [DATASOURCES], [CREATEID], [CREATENAME], [CREATETIME], [UPDATEID], [UPDATENAME], [UPDATETIME], [STATUS], [ISDELETED], [VERSION], [WORKSTATUS], [TELEPHONE], [OCCUPATIONALDISEASESFLAG], [OCCUPATIONALDISEASESWORKTYPE], [OCCUPATIONALDISEASESWORKINGYEARS], [DUSTNAME], [DUSTFLAG], [RADIOACTIVEMATERIALNAME], [RADIOACTIVEMATERIALFLAG], [CHEMICALMATERIALNAME], [CHEMICALMATERIALFLAG], [OTHERNAME], [OTHERFLAG], [PHYSICSMATERIALNAME], [PHYSICSMATERIALFLAG], [DOWNLOADSTATUS], [NONUMBERPROVIDED], [YLZFMC], [PERSONID], [MEDICAL_PAYMENTCODE], [KALEIDOSCOPE], [ISGOVERNANCE]) VALUES ('" + str(varIdcard) + "', '高血压已患', '2', '1959-03-28 00:00:00.000', '" + str(varIdcard) + "', NULL, '13585543856', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2022-11-14 16:49:32.357', NULL, NULL, '2020-02-19 00:00:00.000', NULL, NULL, NULL, NULL, '13585543856', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,'0')")

        # 检查签约信息表身份证是否存在!
        l_d_qty = Sqlserver_PO.execQuery("select count(*) as qty from QYYH where SFZH='%s'" % (varIdcard))
        if l_d_qty[0]['qty'] == 0:
            guid = Data_PO.getFigures(6)
            Sqlserver_PO.execute("INSERT INTO [dbo].[QYYH] ([CZRYBM], [CZRYXM], [JMXM], [SJHM], [SFZH], [JJDZ], [SFJD], [SIGNORGID], [ARCHIVEUNITCODE], [ARCHIVEUNITNAME], [DISTRICTORGCODE], [DISTRICTORGNAME], [TERTIARYORGCODE], [TERTIARYORGNAME], [PRESENTADDRDIVISIONCODE], [PRESENTADDRPROVCODE], [PRESENTADDRPROVVALUE], [PRESENTADDRCITYCODE], [PRESENTADDRCITYVALUE], [PRESENTADDRDISTCODE], [PRESENTADDDISTVALUE], [PRESENTADDRTOWNSHIPCODE], [PRESENTADDRTOWNSHIPVALUE], [PRESENTADDRNEIGHBORHOODCODE], [PRESENTADDRNEIGHBORHOODVALUE], [SIGNSTATUS], [SIGNDATE],[CATEGORY_CODE], [CATEGORY_NAME], [SEX_CODE], [SEX_NAME], [LAST_SERVICE_DATE], [ASSISTANT_DOC_ID], [ASSISTANT_DOC_NAME], [HEALTH_MANAGER_ID], [HEALTH_MANAGER_NAME], [ASSISTANT_DOC_PHONE], [HEALTH_MANAGER_PHONE]) VALUES ('" + str(guid) + "', N'姚皎情', N'高血压已患', NULL, '" + str(varIdcard) + "', N'平安街道16号', NULL, NULL, '0000001', '静安精神病院', '310118000000', '青浦区', '12345', '上海人民医院', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '2020-06-01', 166, '4', N'老年人',N'男', NULL, NULL, NULL, NULL, NULL, NULL, NULL)")


    def _getAutoIdcard(self, d):

        # 随机获取获取疾病身份证中身份证

        varIdcard = ""
        l_d_diseaseRuleCode_idcard = self.getDiseaseIdcard()
        # print(l_d_diseaseRuleCode_idcard)  # [{'diseaseRuleCode': 'YH_JB001', 'idcard': 310101202308070001}, ...]
        l_1 = []
        for i in range(len(l_d_diseaseRuleCode_idcard)):
            l_1.append(l_d_diseaseRuleCode_idcard[i]['idcard'])
        d["varIdcard"] = random.choice(l_1)
        # print(d["varIdcard"])
        self.verifyIdcard(varIdcard)
        if varIdcard != None:
            if 'hitQty' in d and d['hitQty'] == 2:
                self.outResult2(self.rule(d))
            else:
                self.outResult1(self.rule(d))
        else:
            Color_PO.consoleColor("31", "31", "[ERROR => _getDiseaseIdcard2() => 身份证不能为None!]", "")

    def _getDiseaseIdcard2(self, d):

        # 健康干预命中次数之获取身份证

        # print(d)
        varIdcard = ""
        l_d_diseaseRuleCode_idcard = self.getDiseaseIdcard()
        # print(l_d_diseaseRuleCode_idcard)
        for i in range(len(l_d_diseaseRuleCode_idcard)):
            for k, v in l_d_diseaseRuleCode_idcard[i].items():
                # print(l_d_diseaseRuleCode_idcard[i][k])
                if l_d_diseaseRuleCode_idcard[i][k] == d['diseaseRuleCode']:
                    varIdcard = l_d_diseaseRuleCode_idcard[i]['idcard']
                    break

        d["varIdcard"] = varIdcard
        self.verifyIdcard(varIdcard)

        if varIdcard != None:
            if 'hitQty' in d and d['hitQty'] == 2:
                self.outResult2(self.rule(d))
            else:
                self.outResult1(self.rule(d))
        else:
            Color_PO.consoleColor("31", "31", "[ERROR => _getDiseaseIdcard2() => 身份证不能为None!]", "")

    def _getDiseaseIdcardGW(self, d):

        # print(d)
        varIdcard = ""
        l_d_diseaseRuleCode_idcard = self.getDiseaseIdcard()
        # print(l_d_diseaseRuleCode_idcard)
        for i in range(len(l_d_diseaseRuleCode_idcard)):
            for k, v in l_d_diseaseRuleCode_idcard[i].items():
                # print(l_d_diseaseRuleCode_idcard[i][k])
                if l_d_diseaseRuleCode_idcard[i][k] == d['diseaseRuleCode']:
                    varIdcard = l_d_diseaseRuleCode_idcard[i]['idcard']
                    break
        d["varIdcard"] = varIdcard
        self.verifyIdcard(varIdcard)
        if varIdcard != None:
            l_ruleCode, d_all = self.gw(d)
            self.outResultGW(d['diseaseRuleCode'], l_ruleCode, d_all)
        else:
            Color_PO.consoleColor("31", "31", "[ERROR => _getDiseaseIdcard() => 身份证不能为None!]", "")



    def runResult(self, varResult):

        # r.runResult("")  # 执行result为空的规则
        # r.runResult("error")  # 执行result为error的规则
        # r.runResult("ok")  # 执行result为ok的规则
        # r.runResult("all")  # 执行所有的规则(谨慎)

        if varResult == "error" or varResult == "ok" or varResult == "":
            l_d_id = Sqlserver_PO.execQuery("select id from %s where result='%s'" % (self.dbTableName, varResult))
            # print(l_d_id)  # [{'id': 2}, {'id': 10}]
            for i in range(len(l_d_id)):
                self.run(l_d_id[i]['id'])
        elif varResult == "all":
            l_d_id = Sqlserver_PO.execQuery("select id from %s" % (self.dbTableName))
            for i in range(len(l_d_id)):
                self.run(l_d_id[i]['id'])


    def run(self, varId):

        '''
        筛选执行条件
        :param varA: 测试结果
        :param varC_rule: 测试规则名
        :return: none
        '''

        self.varId = varId

        try:
            l_d_rows = Sqlserver_PO.execQuery("select * from %s where id=%s" % (self.dbTableName, self.varId))
            # todo 1
            # print(l_d_rows[0]) # {'result': 'okay', 'memo': '2023/10/20 21:20:21', 'rule': 'r1', 'ruleParam': "AGE=55 .and. CATEGORY_CODE='2'", 'ruleCode': 'PG_Age001', 'tester': '刘斌龙', 'id': 1, 'var': ''}
            self.l_d_rows = l_d_rows[0]
        except:
            sys.exit(0)

        # 格式化参数
        rule = l_d_rows[0]['rule']
        ruleParam = l_d_rows[0]['ruleParam']
        ruleCode = l_d_rows[0]['ruleCode']
        if 'diseaseRuleCode' in l_d_rows[0].keys():
            diseaseRuleCode = l_d_rows[0]['diseaseRuleCode']

        # 传递参数
        l_d_param = Sqlserver_PO.execQuery("select param from 测试规则 where [rule]='%s'" % (rule))
        if l_d_param[0]['param'] == 'p1':
        # if (rule == "r1") or (rule == "r6") or (rule == "r12") or (rule == "r13") or (rule == "r14") or (rule == "r15") or (rule == "r16"):
            # 带参数1 1
            self.param1(rule, ruleParam, ruleCode)
        elif l_d_param[0]['param'] == 'p2':
        # elif (rule == "r3") or (rule == "r4") or (rule == "r8"):
            # 带参数2
            self.param2(rule, ruleParam, ruleCode)
        elif l_d_param[0]['param'] == 'p4':
        # elif rule == "r7":
            # 带参数4
            self.param4(rule, ruleParam, ruleCode)
        elif l_d_param[0]['param'] == 'p1_auto':
            # 带参数1,自动身份证
            self.param1_auto(rule, ruleParam, ruleCode)
        elif l_d_param[0]['param'] == 'p2_auto':
            # 带参数2,自动身份证
            self.param2_auto(rule, ruleParam, ruleCode)
        elif l_d_param[0]['param'] == 'p4_auto':
            # 带参数4,自动身份证
            self.param4_auto(rule, ruleParam, ruleCode)
        elif l_d_param[0]['param'] == 'p1_idcard':
        # elif (rule == "r9") or (rule == "r10"):
            # 带参数1（自动匹配身份证）1_idcard
            self.param1_idcard(rule, ruleParam, ruleCode, diseaseRuleCode)
        elif l_d_param[0]['param'] == 'p2_idcard':
        # elif rule == "r2":
            # 带参数2（自动匹配身份证）
            self.param2_idcard(rule, ruleParam, ruleCode, diseaseRuleCode)
        elif l_d_param[0]['param'] == 'p1_hit2':
        # elif rule == "r11":
            # 带参数1，健康干预两次命中（干预+疾病评估）1_hit2
            self.param1_idcard_hitQty2(rule, ruleParam, ruleCode, diseaseRuleCode, l_d_rows[0]['hitQty'])
        elif l_d_param[0]['param'] == 'p3_hit2':
        # elif rule == "r5":
            # 带参数3，健康干预两次命中（干预+疾病评估）
            self.param3_idcard_hitQty2(rule, ruleParam, ruleCode, diseaseRuleCode, l_d_rows[0]['hitQty'])
        elif l_d_param[0]['param'] == 'r_GW':
            self._getParamByGW(rule, ruleCode, diseaseRuleCode)  # r_GW


    def _getParamByGW(self, rule, ruleCode, diseaseRuleCode):
        l_sql = self.x(rule)
        d = {}
        d['rule'] = l_sql
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        self._getDiseaseIdcardGW(d)


    def x(self, rule):
        if Configparser_PO.SWITCH("printSql") == "on":
            Color_PO.consoleColor("31", "33", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + rule + ")]"), "")
        l_0 = Sqlserver_PO.execQuery("select sql from 测试规则 where [rule]='%s'" %(rule))
        l_sql = []
        for i in range(len(l_0)):
            l_sql.append(l_0[i]['sql'])
        return l_sql

    def param1(self, rule, ruleParam, ruleCode):
        l_sql = self.x(rule)
        d = {}
        d['rule'] = l_sql
        d['ruleParam'] = ruleParam.replace(".and.", ',')   # AGE=55 .and. CATEGORY_CODE='2'"
        d['ruleCode'] = ruleCode  # GY_GW001001
        self.outResult1(self.rule(d))

    def param2(self, rule, ruleParam, ruleCode):
        l_sql = self.x(rule)
        d = {}
        d['rule'] = l_sql
        l_ruleParam = Str_PO.str2list(ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        self.outResult1(self.rule(d))


    def param4(self, rule, ruleParam, ruleCode):
        l_sql = self.x(rule)
        d = {}
        d['rule'] = l_sql
        l_ruleParam = Str_PO.str2list(ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleParam4'] = l_ruleParam[3].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        self.outResult1(self.rule(d))

    def param4_auto(self, rule, ruleParam, ruleCode):
        l_sql = self.x(rule)
        d = {}
        d['rule'] = l_sql
        l_ruleParam = Str_PO.str2list(ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleParam4'] = l_ruleParam[3].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        self._getAutoIdcard(d)

    def param1_auto(self, rule, ruleParam, ruleCode):
        l_sql = self.x(rule)
        d = {}
        d['rule'] = l_sql
        d['ruleParam'] = ruleParam.replace(".and.", ',')
        d['ruleCode'] = ruleCode
        self._getAutoIdcard(d)

    def param1_idcard(self, rule, ruleParam, ruleCode, diseaseRuleCode):

        l_sql = self.x(rule)
        d = {}
        d['rule'] = l_sql
        d['ruleParam'] = ruleParam.replace(".and.", ',')
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        self._getDiseaseIdcard2(d)


    def param2_auto(self, rule, ruleParam, ruleCode):
        l_sql = self.x(rule)
        d = {}
        d['rule'] = l_sql
        l_ruleParam = Str_PO.str2list(ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        self._getAutoIdcard(d)

    def param2_idcard(self, rule, ruleParam, ruleCode, diseaseRuleCode):
        l_sql = self.x(rule)
        d = {}
        d['rule'] = l_sql
        l_ruleParam = Str_PO.str2list(ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        self._getDiseaseIdcard2(d)

    def param1_idcard_hitQty2(self, rule, ruleParam, ruleCode, diseaseRuleCode, hitQty):
        l_sql = self.x(rule)
        d = {}
        d['rule'] = l_sql
        d['ruleParam'] = ruleParam.replace(".and.", ',')
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        d['hitQty'] = hitQty
        self._getDiseaseIdcard2(d)

    def param3_idcard_hitQty2(self, rule, ruleParam, ruleCode, diseaseRuleCode, hitQty):
        l_sql = self.x(rule)
        d = {}
        d['rule'] = l_sql
        l_ruleParam = Str_PO.str2list(ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        d['hitQty'] = hitQty
        self._getDiseaseIdcard2(d)


    def rule(self, d):

        '''
        执行r规则
        :param d:
        :return:
        '''

        # print(d)  # {'rule': 'self.r1', 'ruleParam': "AGE=55 , CATEGORY_CODE='2'", 'ruleCode': 'PG_Age001'}
        # l_sql = eval(r)  # ['select top(1) ID,ID_CARD from T_ASSESS_INFO order by ID desc',...]
        l_sql = d['rule']
        # todo 2
        # print("[原始] => ", l_sql)

        self.log = ""
        varQTY = 0
        varQ2 = 0

        for i in range(len(l_sql)):

            # 格式转义
            if 'varIdcard' in d:
                l_sql[i] = str(l_sql[i]).replace("{身份证}", str(d['varIdcard']))
            if 'ruleParam1' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数1}", d['ruleParam1'])
            if 'ruleParam2' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数2}", d['ruleParam2'])
            if 'ruleParam3' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数3}", d['ruleParam3'])
            if 'ruleParam4' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数4}", d['ruleParam4'])
            if 'ruleParam' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数}", d['ruleParam'])
            if 'ruleCode' in d:
                l_sql[i] = str(l_sql[i]).replace("{规则编码}", d['ruleCode'])
            if "{随机数}" in l_sql[i]:
                l_sql[i] = str(l_sql[i]).replace("{随机数}", Data_PO.getPhone())
            if '{疾病评估规则编码}' in l_sql[i]:
                l_sql[i] = str(l_sql[i]).replace("{疾病评估规则编码}", d['diseaseRuleCode'])
        # todo 3
        # print("[第1次格式化sql] => ", l_sql)  #  ["delete from T_ASSESS_INFO where ID_CARD = '132222196702240429'", ...]

        for i in range(len(l_sql)):
            var = Sqlserver_PO.execQuery("select var from %s where id=%s" % (self.dbTableName, self.varId))
            # print("[] => ", var)
            # print(var[0]['var'])

            if var[0]['var'] != None:
                # print(var[0]['var'])
                if 'id=' in var[0]['var']:
                    varID = var[0]['var'].split("id=")[1].split(",")[0]
                    # print(varID)
                    l_sql[i] = str(l_sql[i]).replace("{varID}", varID)

            if var[0]['var'] != None:
                if 'idcard=' in var[0]['var']:
                    varIdcard = var[0]['var'].split("idcard=")[1].split(",")[0]
                    l_sql[i] = str(l_sql[i]).replace("{varIdcard}", varIdcard)

            if var[0]['var'] != None:
                if 'guid=' in var[0]['var']:
                    varGUID = var[0]['var'].split("guid=")[1].split(",")[0]
                    l_sql[i] = str(l_sql[i]).replace("{varGUID}", varGUID)

            # todo 4

            # # 输出sql语句
            if Configparser_PO.SWITCH("printSql") == "on":
                print(str(i + 1) + ", " + l_sql[i])  # 2, delete from T_ASSESS_INFO where ID_CARD = '310101202308070003'
            # 步骤日志
            if self.log == "":
                self.log = str(i + 1) + ", " + l_sql[i]
            else:
                self.log = self.log + "\n" + str(i + 1) + ", " + l_sql[i]

            a = self.sql(l_sql[i])

            if a != None:
                if isinstance(a, list) and a != []:
                    if isinstance(a[0], dict):
                        # print(a[0])  # {'ID': 5977}
                        if Configparser_PO.SWITCH("printSql") == "on":
                            Color_PO.consoleColor("31", "33", a[0], "")
                            # print(a[0])  # {'ID': 5977}
                        if "ID" in a[0]:
                            l_d_var = Sqlserver_PO.execQuery("select var from %s where id=%s" % (self.dbTableName, self.varId))
                            # print(l_d_var)  # [{'var': 'id=5977'}]

                            if l_d_var[0]['var'] == None or l_d_var[0]['var'] == "":
                                var2 = "id=" + str(a[0]['ID'])
                            else:
                                # 替换最新的变量值，如 原varID=123, 再次生成varID=444时，替换原来的123
                                if "," in l_d_var[0]['var']:
                                    var2 = l_d_var[0]['var'].replace(l_d_var[0]['var'].split("id=")[1].split(",")[0], str(a[0]['ID']))
                                else:
                                    var2 = l_d_var[0]['var'].replace(l_d_var[0]['var'].split("id=")[1], str(a[0]['ID']))
                            Sqlserver_PO.execute("update %s set var='%s' where id=%s" % (self.dbTableName, var2, self.varId))

                        if "ID_CARD" in a[0]:
                            varIdcard = a[0]['ID_CARD']
                            var2 = Sqlserver_PO.execQuery("select var from %s where id=%s" % (self.dbTableName, self.varId))
                            if var2[0]['var'] == None:
                                var2 = "idcard=" + str(varIdcard)
                            else:
                                var2 = var2[0]['var'] + ",idcard=" + str(varIdcard)
                            Sqlserver_PO.execute("update %s set var='%s' where id=%s" % (self.dbTableName, var2, self.varId))

                        if "GUID" in a[0]:
                            var2 = Sqlserver_PO.execQuery("select var from %s where id=%s" % (self.dbTableName, self.varId))
                            var2 = var2[0]['var'] + ",guid=" + str(a[0]['GUID'])
                            Sqlserver_PO.execute("update %s set var='%s' where id=%s" % (self.dbTableName, var2, self.varId))

                        if "QTY" in a[0]:
                            self.log = self.log + "\n" + str(a[0])  # 步骤日志
                            varQTY = a[0]['QTY']

                        if "hitQty" in d and d['hitQty'] == 2:
                            if "Q2" in a[0]:
                                self.log = self.log + "\n" + str(a[0])  # 步骤日志
                                varQ2 = a[0]['Q2']
                        else:
                            varQ2 = 0

        varQTY = int(varQTY) + int(varQ2)
        return varQTY

    def gw(self, d):

        '''
        执行gw规则
        :param d:
        :return:
        '''

        l_sql = d['rule']
        d_all = {}
        self.log = ""

        for i in range(len(l_sql)):

            # 格式转义
            if 'varIdcard' in d:
                l_sql[i] = str(l_sql[i]).replace("{身份证}", str(d['varIdcard']))
            if 'ruleParam1' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数1}", d['ruleParam1'])
            if 'ruleParam2' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数2}", d['ruleParam2'])
            if 'ruleParam3' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数3}", d['ruleParam3'])
            if 'ruleParam4' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数4}", d['ruleParam4'])
            if 'ruleParam' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数}", d['ruleParam'])
            if 'ruleCode' in d:
                l_sql[i] = str(l_sql[i]).replace("{规则编码}", d['ruleCode'])
            if "{随机数}" in l_sql[i]:
                l_sql[i] = str(l_sql[i]).replace("{随机数}", Data_PO.getPhone())
            if '{疾病评估规则编码}' in l_sql[i]:
                l_sql[i] = str(l_sql[i]).replace("{疾病评估规则编码}", d['diseaseRuleCode'])

        for i in range(len(l_sql)):
            var = Sqlserver_PO.execQuery("select var from %s where id=%s" % (self.dbTableName, self.varId))
            # print("[] => ", var)
            # print(var[0]['var'])

            if var[0]['var'] != None:
                # print(var[0]['var'])
                if 'id=' in var[0]['var']:
                    varID = var[0]['var'].split("id=")[1].split(",")[0]
                    # print(varID)
                    l_sql[i] = str(l_sql[i]).replace("{varID}", varID)

            if var[0]['var'] != None:
                if 'idcard=' in var[0]['var']:
                    varIdcard = var[0]['var'].split("idcard=")[1].split(",")[0]
                    l_sql[i] = str(l_sql[i]).replace("{varIdcard}", varIdcard)

            if var[0]['var'] != None:
                if 'guid=' in var[0]['var']:
                    varGUID = var[0]['var'].split("guid=")[1].split(",")[0]
                    l_sql[i] = str(l_sql[i]).replace("{varGUID}", varGUID)

            # 执行sql
            a = self.sql(l_sql[i])

            # 输出sql语句
            if Configparser_PO.SWITCH("printSql") == "on":
                print(str(i + 1) + ", " + l_sql[i])  # 2, delete from T_ASSESS_INFO where ID_CARD = '310101202308070003'

            # 步骤日志
            if self.log == "":
                self.log = str(i + 1) + ", " + l_sql[i]
            else:
                self.log = self.log + "\n" + str(i + 1) + ", " + l_sql[i]

            if a != None:
                if isinstance(a, list) and a != []:
                    if isinstance(a[0], dict):
                        d_all = Dict_PO.mergeDictReserveFirstKey(a[0], d_all)  # {'a': 1, 'b': 2, 'dev': 30, 'test': 3}
                        if Configparser_PO.SWITCH("printSql") == "on":
                            Color_PO.consoleColor("31", "33", a[0], "")
                            # print(a[0])  # {'ID': 5977}

                        self.log = self.log + "\n" + str(a[0])  # 步骤日志
                        if "ID" in a[0]:
                            l_d_var = Sqlserver_PO.execQuery("select var from %s where id=%s" % (self.dbTableName, self.varId))
                            # print(l_d_var)  # [{'var': 'id=5977'}]
                            if l_d_var[0]['var'] == None or l_d_var[0]['var'] == "":
                                var2 = "id=" + str(a[0]['ID'])
                            else:
                                # 替换最新的变量值，如 原varID=123, 再次生成varID=444时，替换原来的123
                                if "," in l_d_var[0]['var']:
                                    var2 = l_d_var[0]['var'].replace(
                                        l_d_var[0]['var'].split("id=")[1].split(",")[0], str(a[0]['ID']))
                                else:
                                    var2 = l_d_var[0]['var'].replace(l_d_var[0]['var'].split("id=")[1], str(a[0]['ID']))
                            Sqlserver_PO.execute(
                                "update %s set var='%s' where id=%s" % (self.dbTableName, var2, self.varId))

                        if "ID_CARD" in a[0]:
                            varIdcard = a[0]['ID_CARD']
                            var2 = Sqlserver_PO.execQuery(
                                "select var from %s where id=%s" % (self.dbTableName, self.varId))
                            if var2[0]['var'] == None:
                                var2 = "idcard=" + str(varIdcard)
                            else:
                                var2 = var2[0]['var'] + ",idcard=" + str(varIdcard)
                            Sqlserver_PO.execute(
                                "update %s set var='%s' where id=%s" % (self.dbTableName, var2, self.varId))

                        if "GUID" in a[0]:
                            var2 = Sqlserver_PO.execQuery("select var from %s where id=%s" % (self.dbTableName, self.varId))
                            var2 = var2[0]['var'] + ",guid=" + str(a[0]['GUID'])
                            Sqlserver_PO.execute(
                                "update %s set var='%s' where id=%s" % (self.dbTableName, var2, self.varId))

        ruleCode = d['ruleCode'].replace("(", '').replace(")", '').replace("'", '')
        # print(ruleCode)  # 'GW_JB011','PG_JWS041','PG_JWS043'
        l_ruleCode = Str_PO.str2list(ruleCode)
        if "ID" in d_all:
            del d_all['ID']
        if "ID_CARD" in d_all:
            del d_all['ID_CARD']
        if "GUID" in d_all:
            del d_all['GUID']
        # print(d_all)
        return l_ruleCode, d_all
