# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-8-1
# Description: CHC包 for Sqlserver
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"))  # 测试环境

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

# from PO.OpenpyxlPO import *
import random, subprocess
import pyperclip as pc

class Sql_chcPO():

    def __init__(self, dbTableName):

        self.TOKEN = self.getToken(Configparser_PO.USER("user"), Configparser_PO.USER("password"))
        self.dbTableName = dbTableName

    def insertTbl(self, sheetName, tableName):
        Sqlserver_PO.execute("drop table " + tableName)
        Sqlserver_PO.xlsx2db('规则db.xlsx', sheetName, tableName)
        # Sqlserver_PO.execute("ALTER TABLE %s ADD id1 INT NOT NULL IDENTITY(1,1) primary key (id1) " % ('健康评估'))  # 新增id自增主键
        Sqlserver_PO.execute("ALTER TABLE %s alter column id int not null" % (tableName))  # 设置主id不能为Null
        Sqlserver_PO.execute("ALTER TABLE %s add PRIMARY KEY (id)" % (tableName))  # 设置主键（条件是id不能为Null）
        # Sqlserver_PO.execute("ALTER TABLE %s ADD var varchar(111)" % (tableName))  # 临时变量

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
                return ([{'name':'重新评估', 'value' : "[ERROR => 重新评估(i_rerunExecuteRule) => " + str(str_r) + "]"}])
            else:
                return None
                # if Configparser_PO.SWITCH("printsql") == "on":
                #     Color_PO.consoleColor("31", "33", "重新评估(i_rerunExecuteRule) => " + str_r, "")
                # return ([{'name':'重新评估', 'value': 200}])
        else:
            if Configparser_PO.SWITCH("printsql") == "on":
                Color_PO.consoleColor("31", "31", str_r, "")
            self.log = self.log + "\n" + str_r
            # 如：{"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            return ([{'name':'重新评估', 'value': "[ERROR => 重新评估(i_rerunExecuteRule) => " + str(str_r) + "]"}])

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
                if Configparser_PO.SWITCH("printsql") == "on":
                    Color_PO.consoleColor("31", "31", str_r, "")
                self.log = self.log + "\n" + str_r
                return ([{'name':'新增评估', 'value' : "[ERROR => 新增评估(i_startAssess) => " + str(str_r) + "]"}])
            else:
                return None
                # if Configparser_PO.SWITCH("printsql") == "on":
                #     Color_PO.consoleColor("31", "33", "新增评估(i_startAssess) =>  => " + str_r, "")
                # return ([{'name':'新增评估', 'value': 200}])
        else:
            if Configparser_PO.SWITCH("printsql") == "on":
                Color_PO.consoleColor("31", "31", str_r, "")
            self.log = self.log + "\n" + str_r
            # 如：{"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            return ([{'name':'新增评估', 'value': "[ERROR => 新增评估(i_startAssess) => " + str(str_r) + "]"}])

    def runSql(self, varSql):

        # 执行sql

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
            Sqlserver_PO.execute("INSERT INTO [dbo].[QYYH] ([CZRYBM], [CZRYXM], [JMXM], [SJHM], [SFZH], [JJDZ], [SFJD], [SIGNORGID], [ARCHIVEUNITCODE], [ARCHIVEUNITNAME], [DISTRICTORGCODE], [DISTRICTORGNAME], [TERTIARYORGCODE], [TERTIARYORGNAME], [PRESENTADDRDIVISIONCODE], [PRESENTADDRPROVCODE], [PRESENTADDRPROVVALUE], [PRESENTADDRCITYCODE], [PRESENTADDRCITYVALUE], [PRESENTADDRDISTCODE], [PRESENTADDDISTVALUE], [PRESENTADDRTOWNSHIPCODE], [PRESENTADDRTOWNSHIPVALUE], [PRESENTADDRNEIGHBORHOODCODE], [PRESENTADDRNEIGHBORHOODVALUE], [SIGNSTATUS], [SIGNDATE],[CATEGORY_CODE], [CATEGORY_NAME], [SEX_CODE], [SEX_NAME], [LAST_SERVICE_DATE], [ASSISTANT_DOC_ID], [ASSISTANT_DOC_NAME], [HEALTH_MANAGER_ID], [HEALTH_MANAGER_NAME], [ASSISTANT_DOC_PHONE], [HEALTH_MANAGER_PHONE]) VALUES ('" + str(guid) + "', N'姚皎情', N'肝癌高危', NULL, '" + str(varIdcard) + "', N'平安街道16号', NULL, NULL, '0000001', '静安精神病院', '310118000000', '青浦区', '12345', '上海人民医院', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '2020-06-01', 166, '4', N'1',N'男', NULL, NULL, NULL, NULL, NULL, NULL, NULL)")



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

        # todo 获取数据库数据
        l_d_rows = Sqlserver_PO.execQuery("select * from %s where id=%s" % (self.dbTableName, self.varId))
        self.l_d_rows = l_d_rows[0]
        # print(l_d_rows[0]) # {'id': 1, 'result': 'ok', 'memo': datetime.datetime(2023, 11, 7, 10, 4, 15), 'rule': 'r1', 'ruleParam': "AGE=55 .and. CATEGORY_CODE='2'", 'ruleCode': 'PG_Age001', '分类': '年龄', '规则名称': '年龄≥55岁', '评估规则详细描述': '年龄≥55岁', '评估因素判断规则': '年龄>=55', 'tester': '刘斌龙', 'var': ''}
        rule = l_d_rows[0]['rule']
        ruleParam = l_d_rows[0]['ruleParam']
        ruleCode = l_d_rows[0]['ruleCode']
        if 'diseaseRuleCode' in l_d_rows[0].keys():
            diseaseRuleCode = l_d_rows[0]['diseaseRuleCode']

        # todo 适配相应的测试规则
        l_d_param = Sqlserver_PO.execQuery("select param from 测试规则 where [rule]='%s'" % (rule))
        if l_d_param[0]['param'] == 'p1':
            # 带参数1
            self.param1(rule, ruleParam, ruleCode)
        elif l_d_param[0]['param'] == 'p2':
            # 带参数2
            self.param2(rule, ruleParam, ruleCode)
        elif l_d_param[0]['param'] == 'p4':
            # 带参数4
            self.param4(rule, ruleParam, ruleCode)
        elif l_d_param[0]['param'] == 'p1_auto':
            # 带参数1且获取自动身份证
            self.param1_auto(rule, ruleParam, ruleCode)
        elif l_d_param[0]['param'] == 'p2_auto':
            # 带参数2且获取自动身份证
            self.param2_auto(rule, ruleParam, ruleCode)
        elif l_d_param[0]['param'] == 'p4_auto':
            # 带参数4且获取自动身份证
            self.param4_auto(rule, ruleParam, ruleCode)
        elif l_d_param[0]['param'] == 'p1_idcard':
            # 带参数1且自动匹配疾病身份证
            self.param1_idcard(rule, ruleParam, ruleCode, diseaseRuleCode)
        elif l_d_param[0]['param'] == 'p2_idcard':
            # 带参数2且自动匹配疾病身份证
            self.param2_idcard(rule, ruleParam, ruleCode, diseaseRuleCode)
        elif l_d_param[0]['param'] == 'p1_hit2':
            # 带参数1，健康干预两次命中（干预+疾病评估）
            self.param1_idcard_hitQty2(rule, ruleParam, ruleCode, diseaseRuleCode, l_d_rows[0]['hitQty'])
        elif l_d_param[0]['param'] == 'p3_hit2':
            # 带参数3，健康干预两次命中（干预+疾病评估）
            self.param3_idcard_hitQty2(rule, ruleParam, ruleCode, diseaseRuleCode, l_d_rows[0]['hitQty'])
        elif l_d_param[0]['param'] == 'r_GW':
            self._getParamByGW(rule, ruleCode, diseaseRuleCode)


    def getSql(self, rule):
        
        # todo 获取sql语句
        
        if Configparser_PO.SWITCH("printSql") == "on":
            # [健康评估 => 1(r1)]
            Color_PO.consoleColor("31", "33", (("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + rule + ")]").center(100, '-')), "")
        l_0 = Sqlserver_PO.execQuery("select sql from 测试规则 where [rule]='%s'" %(rule))
        l_sql = []
        for i in range(len(l_0)):
            if os.name == "posix":
                l_sql.append(l_0[i]['sql'])
            else:
                l_sql.append(l_0[i]['sql'].encode('latin1').decode('GB2312'))
        return l_sql


    def param1(self, rule, ruleParam, ruleCode):
        d = {}
        d['l_sql'] = self.getSql(rule)
        d['ruleParam'] = ruleParam.replace(".and.", ',')
        d['ruleCode'] = ruleCode
        self.outResult1(self.rule(d))

    def param2(self, rule, ruleParam, ruleCode):
        d = {}
        d['l_sql'] = self.getSql(rule)
        l_ruleParam = Str_PO.str2list(ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        self.outResult1(self.rule(d))


    def param4(self, rule, ruleParam, ruleCode):
        d = {}
        d['l_sql'] = self.getSql(rule)
        l_ruleParam = Str_PO.str2list(ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleParam4'] = l_ruleParam[3].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        self.outResult1(self.rule(d))

    def param4_auto(self, rule, ruleParam, ruleCode):
        d = {}
        d['l_sql'] = self.getSql(rule)
        l_ruleParam = Str_PO.str2list(ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleParam4'] = l_ruleParam[3].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        self._getAutoIdcard(d)

    def param1_auto(self, rule, ruleParam, ruleCode):
        d = {}
        d['l_sql'] = self.getSql(rule)
        d['ruleParam'] = ruleParam.replace(".and.", ',')
        d['ruleCode'] = ruleCode
        self._getAutoIdcard(d)

    def param1_idcard(self, rule, ruleParam, ruleCode, diseaseRuleCode):
        d = {}
        d['l_sql'] = self.getSql(rule)
        d['ruleParam'] = ruleParam.replace(".and.", ',')
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        self._getDiseaseIdcard2(d)

    def param2_auto(self, rule, ruleParam, ruleCode):
        d = {}
        d['l_sql'] = self.getSql(rule)
        l_ruleParam = Str_PO.str2list(ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        self._getAutoIdcard(d)

    def param2_idcard(self, rule, ruleParam, ruleCode, diseaseRuleCode):
        d = {}
        d['l_sql'] = self.getSql(rule)
        l_ruleParam = Str_PO.str2list(ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        self._getDiseaseIdcard2(d)

    def param1_idcard_hitQty2(self, rule, ruleParam, ruleCode, diseaseRuleCode, hitQty):
        d = {}
        d['l_sql'] = self.getSql(rule)
        d['ruleParam'] = ruleParam.replace(".and.", ',')
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        d['hitQty'] = hitQty
        self._getDiseaseIdcard2(d)

    def param3_idcard_hitQty2(self, rule, ruleParam, ruleCode, diseaseRuleCode, hitQty):
        d = {}
        d['l_sql'] = self.getSql(rule)
        l_ruleParam = Str_PO.str2list(ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        d['hitQty'] = hitQty
        self._getDiseaseIdcard2(d)

    def _getParamByGW(self, rule, ruleCode, diseaseRuleCode):
        d = {}
        d['l_sql'] = self.getSql(rule)
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        self._getDiseaseIdcardGW(d)


    def outResult1(self, varQty):

        if varQty == 1:
            Color_PO.consoleColor("31", "36", (("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => OK]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, Time_PO.getDateTimeByDivide(), self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))
        else:
            print("step log".center(100, "-"))
            self.log = "error," + self.log
            print(self.log)
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", (("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => ERROR]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='%s' where id=%s" % (self.dbTableName, self.log, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, Time_PO.getDateTimeByDivide(), self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))

    def outResult2(self, varQty):

        if varQty == 2:
            Color_PO.consoleColor("31", "36", (("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => OK]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, Time_PO.getDateTimeByDivide(), self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))
        else:
            print("step log".center(100, "-"))
            self.log = "error," + self.log
            print(self.log)
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", (("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => ERROR]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='%s' where id=%s" % (self.dbTableName, self.log, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, Time_PO.getDateTimeByDivide(), self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))

    def outResultGW(self, d_actual):

        varSign = 0
        d_error = {}
        for k, v in d_actual.items():
            if (k == "QTY0" and v == 0) or (k != "QTY0" and v == 1):
                varSign = varSign + 0
            else:
                varSign = varSign + 1
                d_error[k] = v

        if Configparser_PO.SWITCH("printSql") == "on":
            print('值 => ' + str(d_actual))

        if varSign == 0:
            Color_PO.consoleColor("31", "36", (("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => OK]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, Time_PO.getDateTimeByDivide(), self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))
        else:
            print("step log".center(100, "-"))
            self.log = "error," + self.log
            print(self.log)
            Color_PO.consoleColor("31", "31", '错误值 => ' + str(d_error), "")
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", (("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => ERROR]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='%s' where id=%s" % (self.dbTableName, self.log, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, Time_PO.getDateTimeByDivide(), self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))

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
            # d_actual = self.gw(d)
            # l_ruleCode, d_actual = self.gw(d)
            # l_ruleCode.remove(d['diseaseRuleCode'])  # ['PG_JWS041', 'PG_JWS043']
            # print(d_actual)
            # self.outResultGW(l_ruleCode, d_all)
            # print(d_actual)
            self.outResultGW(self.gw(d))
        else:
            Color_PO.consoleColor("31", "31", "[ERROR => _getDiseaseIdcard() => 身份证不能为None!]", "")



    def rule(self, d):

        # todo 执行r规则

        # print(d)  # {'rule': ['select top(1) ID,ID_CARD from T_ASSESS_INFO order by ID desc', "UPDATE T_ASSESS_INFO set {测试规则参数} where ID_CARD = '{varIdcard}'", "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'", 'self.i_rerunExecuteRule({varID})', "select count(*) QTY from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE= '{规则编码}'"], 'ruleParam': "AGE=55 , CATEGORY_CODE='2'", 'ruleCode': 'PG_Age001'}
        l_sql = d['l_sql']

        self.log = ""
        varQTY = 0
        varQ2 = 0

        for i in range(len(l_sql)):

            # todo 格式化sql
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

        pc.copy('')  # 清空剪贴板

        # todo 获取临时变量
        d_update = {}  # 更新数据
        d_new = {}  # 新数据
        for i in range(len(l_sql)):
            s = pc.paste()
            if "{" in s:
                d_new = Str_PO.str2dict(s)
                d_update.update(d_new)  # 新数据合并到更新数据中
                if 'ID' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{varID}", str(d_update['ID']))
                if 'IDCARD' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{varIdcard}", str(d_update['IDCARD']))
                if 'GUID' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{varGUID}", str(d_update['GUID']))

            # todo 输出sql语句
            if Configparser_PO.SWITCH("printSql") == "on":
                print(str(i + 1) + ", " + l_sql[i])  # 1, delete from T_ASSESS_INFO where ID_CARD = '310101202308070003'

            # todo 记录步骤日志
            if self.log == "":
                self.log = str(i + 1) + ", " + l_sql[i]
            else:
                self.log = self.log + "\n" + str(i + 1) + ", " + l_sql[i]

            # todo 执行sql
            a = self.runSql(l_sql[i])

            if a != None:
                if isinstance(a, list) and a != []:
                    if isinstance(a[0], dict):
                        # print(a[0])  # {'ID': 5977}
                        pc.copy(str(a[0]))
                        if Configparser_PO.SWITCH("printSql") == "on":
                            Color_PO.consoleColor("31", "33", a[0], "")
                            # print(a[0])  # {'ID': 5977}

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

        # todo 执行gw规则

        l_sql = d['l_sql']
        d_actual = {}
        self.log = ""

        for i in range(len(l_sql)):
            # todo 格式化sql - gw
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

        pc.copy('')  # 清空剪贴板

        # todo 获取临时变量 - gw
        d_update = {}  # 更新数据
        d_new = {}  # 新数据
        for i in range(len(l_sql)):
            s = pc.paste()
            if "{" in s:
                d_new = Str_PO.str2dict(s)
                d_update.update(d_new)  # 新数据合并到更新数据中
                if 'ID' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{varID}", str(d_update['ID']))
                if 'IDCARD' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{varIdcard}", str(d_update['IDCARD']))
                if 'GUID' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{varGUID}", str(d_update['GUID']))

            # todo 输出sql语句 - gw
            if Configparser_PO.SWITCH("printSql") == "on":
                print(str(i + 1) + ", " + l_sql[i])  # 2, delete from T_ASSESS_INFO where ID_CARD = '310101202308070003'

            # todo 记录步骤日志 - gw
            if self.log == "":
                self.log = str(i + 1) + ", " + l_sql[i]
            else:
                self.log = self.log + "\n" + str(i + 1) + ", " + l_sql[i]

            # todo 执行sql - gw
            a = self.runSql(l_sql[i])

            if a != None:
                if isinstance(a, list) and a != []:
                    if isinstance(a[0], dict):
                        pc.copy(str(a[0]))
                        self.log = self.log + "\n" + str(a[0])
                        if Configparser_PO.SWITCH("printSql") == "on":
                            for k, v in a[0].items():
                                if k == "QTY0" or k == "ID":
                                    Color_PO.consoleColor("31", "33", a[0], "")
                                else:
                                    if v != 1 :
                                        Color_PO.consoleColor("31", "31", a[0], "")
                                    else:
                                        Color_PO.consoleColor("31", "33", a[0], "")
                        d_actual = Dict_PO.mergeDictReserveFirstKey(a[0], d_actual)  # {'a': 1, 'b': 2, 'dev': 30, 'test': 3}

        # ruleCode = d['ruleCode'].replace("(", '').replace(")", '').replace("'", '')
        # # print(ruleCode)  # 'GW_JB011','PG_JWS041','PG_JWS043'
        # l_ruleCode = Str_PO.str2list(ruleCode)
        if "ID" in d_actual:
            del d_actual['ID']
        if "ID_CARD" in d_actual:
            del d_actual['ID_CARD']
        if "GUID" in d_actual:
            del d_actual['GUID']
        return d_actual
