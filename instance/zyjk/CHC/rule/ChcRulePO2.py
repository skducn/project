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
from PO.DataPO import *
Data_PO = DataPO()
from PO.OpenpyxlPO import *


class ChcRulePO2():

    def __init__(self, dbTableName):

        self.TOKEN = self.getToken(Configparser_PO.USER("user"), Configparser_PO.USER("password"))
        self.dbTableName = dbTableName

        self.r1 = ["select top(1) ID,ID_CARD from T_ASSESS_INFO order by ID desc",
                   "UPDATE T_ASSESS_INFO set {测试规则参数} where ID_CARD = '{varIdcard}'",
                   "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'",
                   "self.i_rerunExecuteRule({varID})",
                   "select count(*) QTY from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE= '{规则编码}'"]

        self.r2 = ["delete from T_ASSESS_INFO where ID_CARD = '{身份证}'",
                    "DELETE FROM T_HIS_DIAGNOSIS where IDCARD = '{身份证}'",
                    "INSERT INTO T_HIS_DIAGNOSIS (IDCARD, DIAGNOSIS_CODE, DIAGNOSIS_TYPE,DIAGNOSIS_DATE, CREATE_DATE) VALUES ('{身份证}', {测试规则参数1},{测试规则参数2}, '2023-07-29 16:02:19.000', '2023-07-31 09:39:24.3700000')",
                    "self.i_startAssess({身份证})",
                    "select ID from T_ASSESS_INFO where ID_CARD = '{身份证}'",
                    "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'",
                    "self.i_rerunExecuteRule({varID})",
                    "select count(*) QTY from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'",
                    "select count(*) Q2 from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{疾病评估规则编码}'"]

        self.r3 = ["delete from T_ASSESS_INFO where ID_CARD = '110101196407281506'",
                    "delete from T_HIS_DIAGNOSIS where IDCARD = '110101196407281506'",
                    "INSERT INTO T_HIS_DIAGNOSIS (IDCARD, DIAGNOSIS_CODE, DIAGNOSIS_NAME, DIAGNOSIS_DATE, CREATE_DATE,DIAGNOSIS_TYPE) VALUES ('110101196407281506', {测试规则参数1}, '', '2023-07-29 16:02:19.000', '2023-07-31 09:39:24.3700000',{测试规则参数2})",
                    "self.i_startAssess(110101196407281506)",
                    "select ID from T_ASSESS_INFO where ID_CARD = '110101196407281506'",
                    "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'",
                    "self.i_rerunExecuteRule({varID})",
                    "select count(*) QTY from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'"]

        self.r4 = ["delete from T_ASSESS_INFO where ID_CARD = '110101196407281506'",
                    "self.i_startAssess(110101196407281506)",
                    "select ID from T_ASSESS_INFO where ID_CARD = '110101196407281506'",
                    "delete from T_ASSESS_PREVIOUS_HISTORY where IDCARD = '110101196407281506'",
                    "INSERT INTO T_ASSESS_PREVIOUS_HISTORY(IDCARD, ASSESS_ID, ASSOCIATION_TYPE, MSG_NAME, OCCUR_DATE, CREATE_DATE, MSG_CODE) VALUES ('110101196407281506', {varID}, {测试规则参数1}, '手术1', '2023-07-01', '2023-07-29 16:31:45.1600000', {测试规则参数2})",
                    "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'",
                    "self.i_rerunExecuteRule({varID})",
                    "select count(*) QTY from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'"]

        self.r5 = ["delete from T_ASSESS_INFO where ID_CARD = '{身份证}'",
                    "DELETE FROM T_HIS_DIAGNOSIS where IDCARD = '{身份证}'",
                    "INSERT INTO T_HIS_DIAGNOSIS (IDCARD, DIAGNOSIS_CODE, DIAGNOSIS_TYPE,DIAGNOSIS_DATE, CREATE_DATE) VALUES ('{身份证}', {测试规则参数1},{测试规则参数2}, '2023-07-29 16:02:19.000', '2023-07-31 09:39:24.3700000')",
                    "self.i_startAssess({身份证})",
                    "update T_ASSESS_INFO set {测试规则参数3} where ID_CARD = '{身份证}'",
                    "select ID from T_ASSESS_INFO where ID_CARD = '{身份证}'",
                    "self.i_rerunExecuteRule({varID})",
                    "select count(*) QTY from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'",
                    "select count(*) Q2 from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{疾病评估规则编码}'"]

        self.r6 = ["delete from T_ASSESS_INFO where ID_CARD = '110101196407281506'",
                    "self.i_startAssess(110101196407281506)",
                    "select ID from T_ASSESS_INFO where ID_CARD = '110101196407281506'",
                    "delete from T_ASSESS_FAMILY_HISTORY where IDCARD = '110101196407281506'",
                    "INSERT INTO T_ASSESS_FAMILY_HISTORY(IDCARD, ASSESS_ID, DISEASE_NAME, FAMILY_TIES, SERVER_DATE, CREATE_DATE) VALUES ('110101196407281506', {varID}, {测试规则参数}, '父亲', '1900-01-01', '2023-07-29 14:00:38.9466667')",
                    "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'",
                    "self.i_rerunExecuteRule({varID})",
                    "select count(*) QTY from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'"]

        self.r7 = ["delete from T_ASSESS_INFO where ID_CARD = '132222196702240429'",
                    "DELETE FROM T_HIS_DIAGNOSIS where IDCARD = '132222196702240429'",
                    "INSERT INTO T_HIS_DIAGNOSIS (IDCARD, DIAGNOSIS_CODE, DIAGNOSIS_TYPE,DIAGNOSIS_DATE, CREATE_DATE) VALUES ('132222196702240429', {测试规则参数1},{测试规则参数2}, '2023-07-29 16:02:19.000', '2023-07-31 09:39:24.3700000')",
                    "INSERT INTO T_HIS_DIAGNOSIS (IDCARD, DIAGNOSIS_CODE, DIAGNOSIS_TYPE,DIAGNOSIS_DATE, CREATE_DATE) VALUES ('132222196702240429', {测试规则参数3},{测试规则参数4}, '2023-07-29 16:02:19.000', '2023-07-31 09:39:24.3700000')",
                    "self.i_startAssess(132222196702240429)",
                    "select ID from T_ASSESS_INFO where ID_CARD = '132222196702240429'",
                    "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE= '{规则编码}'",
                    "self.i_rerunExecuteRule({varID})",
                    "select count(*) QTY from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'"]

        self.r8 = ["DELETE from TB_DC_HTN_VISIT where EMPIGUID = '5001'",
                    "INSERT INTO TB_DC_HTN_VISIT (GUID, CARDID, NAME, AGE , EHRNUM , ORGCODE , VISITDATE , VISITWAYCODE , VISITWAYVALUE , OTHERVISIT , VISITDOCNO , VISITDOCNAME , VISITORGCODE , VISITORGNAME , VISTSTATUSCODE , VISITSTATUSVALUE , NEXTVISIDATE , MANAGEGROUP , LOSTVISITCODE , LOSTVISITNAME , OTHERLOSTVISITNAME , LOSTVISITDATE , MOVEPROVINCECODE , MOVEPROVINCEVALUE , MOVECITYCODE , MOVECITYVALUE , MOVEDISTRICTCODE , MOVEDISTRICTVALUE , MOVESTREETCODE , MOVESTREETVALUE , MOVENEIGHBORHOODCODE , MOVENEIGHBORHOODVALUE , MOVEVILLAGEVALUE , MOVEHOUSENUMBER , MOVEORGCODE , MOVEORGNAME , DANGEROUSLEVELCODE , DANGEROUSLEVELNAME , DEATHREASON , SBP , DBP , ISMANUALINPUT , HEIGHT , WEIGHT , TARGETWEIGHT , BMI , WAISTLINE , TARGETBMI , FASTINGBLOODSUGARVALUE , FASTINGBLOODSUGARCODE , FASTINGBLOODSUGARNAME , FASTINGBLOODSUGARSIGN , CHOLESTEROL , HIGHCHOLESTEROL , LOWCHOLESTEROL , TRIGLYCERIDES , UACR , BCTV , BUATV , HOMOCYSTEINEDETECTION , BLOODPOTASSIUM , BLOODSODIUM , BLOODLIPIDS , URICACID , CREATININE , HEMOGLOBIN , HEMAMEBA , PLATELET , URINEPROTEIN , URINESUGAR , GLYCOSYLATEDHEMOGLOBIN , SERUMCPROTEIN , URINEPROTEINQUANTITY , ECG , ECHOCARDIOGRAM , CAROTIDULTRASOUND , CHESTXRAY , PULSEWAVE , REGULARACTIVITYSIGN , REGULARACTIVITIESTYPES , HASPAPERCARD , DRUGCOMPLIANCECODE , DRUGCOMPLIANCENAME , BPWAYCODE , BPWAYNAME , HEARTRATE , SMOKINGVOLUME , DRINKINGVOLUME , POSITIVESIGNS , SMOKINGSTATUSCODE , SMOKINGSTATUSNAME , TARGETSMOKE , QUITSMOKING , DRINKINGFREQUENCYCODE , DRINKINGFREQUENCYNAME , TARGETDRINK , TARGETSALTUPTAKESTATUS , REASONABLEDIETEVALUATION , PSYCHOLOGYEVALUATION , COMPLIANCEEVALUATION , SALTUPTAKESTATUS , SALTUPTAKESTATUSNAME , PSYCHOLOGYSTATUS , PSYCHOLOGYSTATUSNAME , COMPLIANCESTATUS , COMPLIANCESTATUSNAME , SPORTFREQUENCE , SPORTTIME , EXERCISEDESCRIPTION , EXERCISEFREQUENCYCODE , EXERCISEFREQUENCYNAME , TARGETSPORTFREQUENCYCODE , TARGETSPORTFREQUENCYNAME , TARGETSPORTTIMES , TARGETSTAPLEFOOD , SYMPTOMCODE , SYMPTOMVALUE , SYMPTOMOTHER , ISUSEDRUG , NOUSEDRUGREASONCODE , NOUSEDRUGREASONVALUE , NOUSEDRUGSIDEEFFECTS , OTHERNOUSEDRUGREASON , NOUSEDRUGLAW , NOUSEDRUGLAWREASON , LAWSIDEEFFECTSFLAG , LAWSIDEEFFECTS , OTHERLAWREASON , TREATMENTMEASURES , CLINICALINFO , AUXILIARYCHECK , INTERVENENUM , BEFOREINTERVENEDATE , ISINTERVENE , SYNDROME , INTERVENEMEASURES , MEASURESCONTENT , OTHERINTERVENEMEASURES , OTHERMEASURESCONTENT , PROPOSAL , ACCEPTABILITY , ISACCEPTHEALTHEDU , HEALTHEDUTYPE , VISITTYPE , REFERRALREASON , REFERRALORGDEPT , SYNSTATUS , EMPIGUID , ISGOVERNANCE ) VALUES (newid(), '001', NULL, NULL, NULL, '0000001', '2023-08-01 10:51:23.000', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '140', '90', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,{测试规则参数1}, '从不吸', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '5001', '0')",
                    "delete from T_ASSESS_INFO where ID_CARD = '120101199104058611'",
                    "self.i_startAssess(120101199104058611)",
                    "update T_ASSESS_INFO set {测试规则参数2}  where ID_CARD = '120101199104058611'",
                    "select ID from T_ASSESS_INFO where ID_CARD = '120101199104058611'",
                    "self.i_rerunExecuteRule({varID})",
                    "select count(*) QTY from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'"]

        self.r11 = ["DELETE FROM T_ASSESS_INFO where ID_CARD = '{身份证}'",
                    "DELETE FROM T_HIS_DIAGNOSIS where IDCARD = '{身份证}'",
                    "self.i_startAssess({身份证})",
                    "update T_ASSESS_INFO set {测试规则参数} where ID_CARD = '{身份证}'",
                    "select ID from T_ASSESS_INFO where ID_CARD = '{身份证}'",
                    "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID}",
                    "self.i_rerunExecuteRule({varID})",
                    "select count(*) QTY from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE= '{规则编码}'",
                    "select count(*) Q2 from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE= '{疾病评估规则编码}'"]

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

    def getIdcard(self):

        '''
        获取疾病身份证中对应疾病的身份证号码
        :param
        :return: 
        '''

        l_d_diseaseRuleCode_idcard = Sqlserver_PO.execQuery("select diseaseRuleCode, idcard from jh_idcard")
        # print(l_d_diseaseRuleCode_idcard)  # [{'diseaseRuleCode': 'YH_JB001', 'idcard': 310101202308070001}, {'diseaseRuleCode': 'YH_JB002', 'idcard': 310101202308070002}, ...]
        return (l_d_diseaseRuleCode_idcard)

    def i_rerunExecuteRule(self, var):

        '''
        重新评估 
        :param var:
        :param token:
        :return:
        '''

        command = "curl -X GET \"" + Configparser_PO.HTTP("url") + ":8011/server/tAssessInfo/rerunExecuteRule/" + str(var) + "\" -H \"accept: */*\" -H \"Content-Type: application/json\" -H \"Authorization:" + str(self.TOKEN) + "\""
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
                Color_PO.consoleColor("31", "31", str_r, "")
                return ([{'name':'重新评估', 'value' : "[ERROR => i_rerunExecuteRule() => " + str(str_r) + "]"}])
            else:
                return ([{'name':'重新评估', 'value': 200}])
        else:
            Color_PO.consoleColor("31", "31", str_r, "")
            # 如：{"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            return ([{'name':'重新评估', 'value': "[ERROR => i_rerunExecuteRule() => " + str(str_r) + "]"}])

    def i_startAssess(self, varIdcard):

        '''
        新增评估
        :param varIdcard:
        :param token:
        :return:
        '''

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
                Color_PO.consoleColor("31", "31", str_r, "")
                return ([{'name':'新增评估', 'value' : "[ERROR => i_startAssess() => " + str(str_r) + "]"}])
            else:
                return ([{'name':'新增评估', 'value': 200}])
        else:
            Color_PO.consoleColor("31", "31", str_r, "")
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



    def outResult1(self, varQty, varLog):

        if varQty == 1:
            Color_PO.consoleColor("31", "36", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => OK]"), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, Time_PO.getDateTimeByDivide(), self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))
        else:
            print("step log".center(100, "-"))
            print(self.log)
            Color_PO.consoleColor("31", "31", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(self.l_d_rows['rule']) + ") => ERROR]"), "")
            Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, self.log, self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))

    def outResult2(self, varQty, varLog):

        if varQty == 2:
            Color_PO.consoleColor("31", "36", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(
                self.l_d_rows['rule']) + ") => OK]"), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute(
                "update %s set memo='%s' where id=%s" % (self.dbTableName, Time_PO.getDateTimeByDivide(), self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))
        else:
            print("step log".center(100, "-"))
            print(self.log)
            Color_PO.consoleColor("31", "31", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(
                self.l_d_rows['rule']) + ") => ERROR]"), "")
            Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, self.log, self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))

    def outResultGW(self, varQty, varLog, v5):

        if varQty == 1:
            Color_PO.consoleColor("31", "36", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(v5) + ") => OK]"), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, Time_PO.getDateTimeByDivide(), self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))
        else:
            print("step log".center(100, "-"))
            print(self.log)
            Color_PO.consoleColor("31", "31", ("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + str(v5) + ") => ERROR]"), "")
            Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTableName, self.varId))
            Sqlserver_PO.execute("update %s set memo='%s' where id=%s" % (self.dbTableName, self.log, self.varId))
            Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTableName, self.varId))


    def _getIdcard(self, d):

        # 获取身份证

        # print(d)
        varIdcard = ""
        l_d_diseaseRuleCode_idcard = self.getIdcard()
        # print(l_d_diseaseRuleCode_idcard)
        for i in range(len(l_d_diseaseRuleCode_idcard)):
            for k, v in l_d_diseaseRuleCode_idcard[i].items():
                # print(l_d_diseaseRuleCode_idcard[i][k])
                if l_d_diseaseRuleCode_idcard[i][k] == d['diseaseRuleCode']:
                    varIdcard = l_d_diseaseRuleCode_idcard[i]['idcard']
                    break
        d["varIdcard"] = varIdcard
        # print(varIdcard)

        # 检查签约信息表（QYYH），患者主索引表（TB_EMPI_INDEX_ROOT），基本信息表（HRPERSONBASICINFO）
        l_d_qty = Sqlserver_PO.execQuery("select count(*) as qty from TB_EMPI_INDEX_ROOT where IDCARDNO='%s'" % (varIdcard))
        # print(l_d_qty)  # [{'qty': 1}]
        # print(l_d_qty[0]['qty'])
        if l_d_qty[0]['qty'] == 0:
            guid = Data_PO.getFigures(6)
            name = Data_PO.getChineseName()
            Sqlserver_PO.execute("INSERT INTO [TB_EMPI_INDEX_ROOT] ([GUID], [NAME], [SEXCODE], [SEXVALUE], [DATEOFBIRTH], [IDCARDNO]) VALUES ('" + str(guid) + "', N'" + str(name) + "', '2', '女', '1940-05-11', '" + str(varIdcard) + "')")

        if varIdcard != None:
            varQty, varLog = self.rule(d)
            self.outResult1(varQty, varLog)
        else:
            # print("[ERROR => _getIdcard() => 身份证不能为None!]")
            Color_PO.consoleColor("31", "31", "[ERROR => _getIdcard() => 身份证不能为None!]", "")

    def _getIdcard2(self, d):

        # 健康干预命中次数之获取身份证

        # print(d)
        varIdcard = ""
        l_d_diseaseRuleCode_idcard = self.getIdcard()
        # print(l_d_diseaseRuleCode_idcard)
        for i in range(len(l_d_diseaseRuleCode_idcard)):
            for k, v in l_d_diseaseRuleCode_idcard[i].items():
                # print(l_d_diseaseRuleCode_idcard[i][k])
                if l_d_diseaseRuleCode_idcard[i][k] == d['diseaseRuleCode']:
                    varIdcard = l_d_diseaseRuleCode_idcard[i]['idcard']
                    break
        d["varIdcard"] = varIdcard
        # print(varIdcard)
        # 检查签约信息表（QYYH），患者主索引表（TB_EMPI_INDEX_ROOT），基本信息表（HRPERSONBASICINFO）
        l_d_qty = Sqlserver_PO.execQuery("select count(*) as qty from TB_EMPI_INDEX_ROOT where IDCARDNO='%s'" % (varIdcard))
        # print(l_d_qty)  # [{'qty': 1}]
        # print(l_d_qty[0]['qty'])
        if l_d_qty[0]['qty'] == 0:
            guid = Data_PO.getFigures(6)
            name = Data_PO.getChineseName()
            Sqlserver_PO.execute("INSERT INTO [TB_EMPI_INDEX_ROOT] ([GUID], [NAME], [SEXCODE], [SEXVALUE], [DATEOFBIRTH], [IDCARDNO]) VALUES ('" + str(guid) + "', N'" + str(name) + "', '2', '女', '1940-05-11', '" + str(varIdcard) + "')")

        if varIdcard != None:
            varQty, varLog = self.rule(d)
            if d['hitQty'] == 2:
                self.outResult2(varQty, varLog)
            elif d['hitQty'] == None:
                self.outResult1(varQty, varLog)
        else:
            Color_PO.consoleColor("31", "31", "[ERROR => _getIdcard2() => 身份证不能为None!]", "")
            # print("[ERROR => _getIdcard2() => 身份证不能为None!]")


    def run(self, varId):

        '''
        筛选执行条件
        :param varA: 测试结果
        :param varC_rule: 测试规则名
        :return: none
        '''

        self.varId = varId

        l_d_rows = Sqlserver_PO.execQuery("select * from %s where id=%s" % (self.dbTableName, self.varId))
        # todo 1
        # print(l_d_rows[0]) # {'result': 'okay', 'memo': '2023/10/20 21:20:21', 'rule': 'self.r1', 'ruleParam': "AGE=55 .and. CATEGORY_CODE='2'", 'ruleCode': 'PG_Age001', 'tester': '刘斌龙', 'id': 1, 'var': ''}
        self.l_d_rows = l_d_rows[0]

        # 格式化参数
        rule = l_d_rows[0]['rule']
        ruleParam = l_d_rows[0]['ruleParam']
        ruleCode = l_d_rows[0]['ruleCode']
        if 'diseaseRuleCode' in l_d_rows[0].keys():
            diseaseRuleCode = l_d_rows[0]['diseaseRuleCode']

        # 传递参数
        if (rule == "r1") or (rule == "r6") or (rule == "r12"):
            # 带参数1
            self.param1(rule, ruleParam, ruleCode)
        elif (rule == "r3") or (rule == "r4") or (rule == "r8"):
            # 带参数2
            self.param2(rule, ruleParam, ruleCode)
        elif rule == "r7":
            # 带参数4
            self.param4(rule, ruleParam, ruleCode)
        elif (rule == "r9") or (rule == "r10"):
            # 带参数1（自动匹配身份证）
            self.param1_idcard(rule, ruleParam, ruleCode)
        elif rule == "r2":
            # 带参数2（自动匹配身份证）
            self.param2_idcard(rule, ruleParam, ruleCode, diseaseRuleCode)
        elif rule == "r11":
            # 带参数1，健康干预两次命中（干预+疾病评估）
            self.param1_idcard_hitQty2(rule, ruleParam, ruleCode, diseaseRuleCode, l_d_rows[0]['hitQty'])
        elif rule == "r5":
            # 带参数3，健康干预两次命中（干预+疾病评估）
            self.param3_idcard_hitQty2(rule, ruleParam, ruleCode, diseaseRuleCode, l_d_rows[0]['hitQty'])



    def param1(self, rule, ruleParam, ruleCode):
        if Configparser_PO.SWITCH("printSql") == "on":
            print("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + rule + ")]")
        d = {}
        d['rule'] = "self." + rule  # self.r1
        d['ruleParam'] = ruleParam.replace(".and.", ',')   # AGE=55 .and. CATEGORY_CODE='2'"
        d['ruleCode'] = ruleCode  # GY_GW001001
        varQty, varLog = self.rule(d)
        self.outResult1(varQty, varLog)


    def param2(self, rule, ruleParam, ruleCode):
        if Configparser_PO.SWITCH("printSql") == "on":
            print("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + rule + ")]")

        l_ruleParam = Str_PO.str2list(ruleParam)
        d = {}
        d['rule'] = "self." + rule
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        varQty, varLog = self.rule(d)
        self.outResult1(varQty, varLog)


    def param4(self, rule, ruleParam, ruleCode):

        if Configparser_PO.SWITCH("printSql") == "on":
            print("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + rule + ")]")
        l_ruleParam = Str_PO.str2list(ruleParam)
        d = {}
        d['rule'] = "self." + rule
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleParam4'] = l_ruleParam[3].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        varQty, varLog = self.rule(d)
        self.outResult1(varQty, varLog)


    def param1_idcard(self, rule, ruleParam, ruleCode, diseaseRuleCode):

        if Configparser_PO.SWITCH("printSql") == "on":
            print("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + rule + ")]")
        d = {}
        d['rule'] = "self." + rule
        d['ruleParam'] = ruleParam.replace(".and.", ',')
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        # varQty, varLog = self.rule(d)
        # self.outResult1(varQty, varLog)
        self._getIdcard(d)


    def param2_idcard(self, rule, ruleParam, ruleCode, diseaseRuleCode):

        if Configparser_PO.SWITCH("printSql") == "on":
            print("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + rule + ")]")
        l_ruleParam = Str_PO.str2list(ruleParam)
        d = {}
        d['rule'] = "self." + rule
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        # varQty, varLog = self.rule(d)
        # # self.outResult1(varQty, varLog)
        self._getIdcard(d)



    def param1_idcard_hitQty2(self, rule, ruleParam, ruleCode, diseaseRuleCode, hitQty):

        if Configparser_PO.SWITCH("printSql") == "on":
            print("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + rule + ")]")
        d = {}
        d['rule'] = "self." + rule
        d['ruleParam'] = ruleParam.replace(".and.", ',')
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        d['hitQty'] = hitQty
        self._getIdcard2(d)



    def param3_idcard_hitQty2(self, rule, ruleParam, ruleCode, diseaseRuleCode, hitQty):

        if Configparser_PO.SWITCH("printSql") == "on":
            print("[" + str(self.dbTableName) + " => " + str(self.varId) + "(" + rule + ")]")
        l_ruleParam = Str_PO.str2list(ruleParam)
        d = {}
        d['rule'] = "self." + rule
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleCode'] = ruleCode
        d['diseaseRuleCode'] = diseaseRuleCode
        d['hitQty'] = hitQty
        self._getIdcard2(d)


    def rule(self, d):

        '''
        执行r规则
        :param d:
        :return:
        '''

        # print(d)  # {'rule': 'self.r1', 'ruleParam': "AGE=55 , CATEGORY_CODE='2'", 'ruleCode': 'PG_Age001'}
        l_sql = eval(d['rule'])  # ['select top(1) ID,ID_CARD from T_ASSESS_INFO order by ID desc',...]
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

            if var[0]['var'] != None:
                if 'id=' in var[0]['var'] :
                    varID = var[0]['var'].split("id=")[1].split(",")[0]
                    l_sql[i] = str(l_sql[i]).replace("{varID}", varID)

            if var[0]['var'] != None:
                if 'idcard=' in var[0]['var'] :
                    varIdcard = var[0]['var'].split("idcard=")[1].split(",")[0]
                    l_sql[i] = str(l_sql[i]).replace("{varIdcard}", varIdcard)

            if var[0]['var'] != None:
                if 'guid=' in var[0]['var'] :
                    varGUID = var[0]['var'].split("guid=")[1].split(",")[0]
                    l_sql[i] = str(l_sql[i]).replace("{varGUID}", varGUID)

            # todo 4
            # print("[第" + str(i+2) + "次格式化sql] => ", l_sql[i])  #  delete from T_ASSESS_INFO where ID_CARD = '132222196702240429'

            # 健康干预 - 命中次数hitQty
            # Color_PO.consoleColor("31", "31", l_sql[i], "")
            if "hitQty" in d:
                if d['hitQty'] == 2:
                    a = self.sql(l_sql[i])
                    # print(a,5555555)
                    if "Q2" in a[0]:
                        self.log = self.log + "\n" + str(a[0])  # 步骤日志
                        varQ2 = a[0]['Q2']
                else:
                    a = self.sql(l_sql[i])
                    varQ2 = 0
            else:
                a = self.sql(l_sql[i])
                varQ2 = 0

            # # 输出sql语句
            if Configparser_PO.SWITCH("printSql") == "on":
                print(str(i + 1) + ", " + l_sql[i])  # 2, delete from T_ASSESS_INFO where ID_CARD = '310101202308070003'

            # 步骤日志
            self.log = self.log + "\n" + ", " + l_sql[i]

            if a != None:
                if isinstance(a, list) and a != []:
                    if isinstance(a[0], dict):
                        # print(a[0])
                        if "ID" in a[0]:
                            var2 = Sqlserver_PO.execQuery("select var from %s where id=%s" % (self.dbTableName, self.varId))
                            if var2[0]['var'] == None:
                                var2 = "id=" + str(a[0]['ID'])
                            else:
                                var2 = var2[0]['var'] + ",id=" + str(a[0]['ID'])
                            # print(var2)
                            Sqlserver_PO.execute("update %s set var='%s' where id=%s" % (self.dbTableName, var2, self.varId))

                        if "ID_CARD" in a[0]:
                            varIdcard = a[0]['ID_CARD']
                            var2 = Sqlserver_PO.execQuery("select var from %s where id=%s" % (self.dbTableName, self.varId))
                            if var2[0]['var'] == None:
                                var2 = "idcard=" + str(varIdcard)
                            else:
                                var2 = var2[0]['var'] + ",idcard=" + str(varIdcard)
                            Sqlserver_PO.execute("update %s set var='%s' where id=%s" % (self.dbTableName, var2, self.varId))

                        if "QTY" in a[0]:
                            self.log = self.log + "\n" + str(a[0])  # 步骤日志
                            varQTY = a[0]['QTY']

                        if "GUID" in a[0]:
                            var2 = Sqlserver_PO.execQuery("select var from %s where id=%s" % (self.dbTableName, self.varId))
                            var2 = var2[0]['var'] + ",guid=" + str(a[0]['GUID'])
                            Sqlserver_PO.execute("update %s set var='%s' where id=%s" % (self.dbTableName, var2, self.varId))

        varQTY = int(varQTY) + int(varQ2)
        return varQTY, self.log

    def gw(self, d):

        '''
        执行gw规则
        :param d:
        :return:
        '''
        # print(d)  # {'result': None, 'diseaseRuleCode': 'GW_JB009', 'ruleCode': "('GW_JB009','PG_JWS026','PG_JWS027','PG_JWS028','PG_JWS031','PG_JWS032')", 'varIdcard': '410101202308070009'}

        d_all = {}
        self.log = ""
        varQTY = ""
        i_startAssessStatus = 0

        # 1，遍历所有列获取值
        l_all = self.Openpyxl_PO.getCol("gwSql")
        for i in range(len(l_all)):
            if d['diseaseRuleCode'] == l_all[i][0]:
                for j in range(1, len(l_all[i])):
                    command = l_all[i][j]
                    if command != None:

                        # 调试
                        # if command == "exit":
                        #     Openpyxl_PO.setCell(21, 1, "", "testRule")
                        #     Openpyxl_PO.setCell(22, 1, "", "testRule")
                        #     Openpyxl_PO.setCell(23, 1, "", "testRule")
                        #     Openpyxl_PO.setCell(24, 1, "", "testRule")
                        #     Openpyxl_PO.setCell(25, 1, "", "testRule")
                        #     Openpyxl_PO.setCell(26, 1, "", "testRule")
                        #     Openpyxl_PO.setCell(27, 1, "", "testRule")
                        #     return d_all, log

                        if 'varIdcard' in d:
                            command = str(command).replace("{身份证}", d['varIdcard'])
                        if 'interventionRule' in d:
                            command = str(command).replace("{规则编码}", d['interventionRule'])
                        if "{随机数}" in command:
                            command = str(command).replace("{随机数}", Data_PO.getPhone())
                        if 'diseaseRuleCode' in d:
                            command = str(command).replace("{疾病评估规则编码}", d['diseaseRuleCode'])

                        varID = self.Openpyxl_PO.getCell(21, 1, "sql")
                        varIdcard = self.Openpyxl_PO.getCell(22, 1, "sql")
                        # varQTY = self.Openpyxl_PO.getCell(23, 1, "sql")
                        varRunRule = self.Openpyxl_PO.getCell(24, 1, "sql")
                        varNewAssess = self.Openpyxl_PO.getCell(25, 1, "sql")
                        varGUID = self.Openpyxl_PO.getCell(26, 1, "sql")
                        # varQTY0 = Openpyxl_PO.getCellValue(27, 1, "sql")

                        if varID != None:
                            if "varID=" in varID:
                                varID = varID.split("varID=")[1].split(")")[0]
                                command = str(command).replace("{varID}", varID)
                        if varIdcard != None:
                            if "varIdcard" in varIdcard:
                                varIdcard = varIdcard.split("varIdcard=")[1].split(")")[0]
                                command = str(command).replace("{varIdcard}", varIdcard)
                        # if varQTY != None:
                        #     if "varQTY" in varQTY:
                        #         varQTY = varQTY.split("varQTY=")[1].split(")")[0]
                        #         command = str(command).replace("{varQTY}", varQTY)
                        if varRunRule != None and varRunRule != "":
                            # print(type(varRunRule))
                            # varRunRule = varRunRule.split("varRunRule=")[1].split(")")[0]
                            self.log = self.log + "\n" + varRunRule
                        if varNewAssess != None and varNewAssess != "":
                            # print(type(varNewAssess))
                            # varNewAssess = varNewAssess.split("varNewAssess=")[1].split(")")[0]
                            self.log = self.log + "\n" + varNewAssess
                        if varGUID != None:
                            if "varGUID" in varGUID:
                                varGUID = varGUID.split("varGUID=")[1].split(")")[0]
                                command = str(command).replace("{varGUID}", varGUID)
                        # if varQTY0 != None:
                        #     if "varQTY0" in varQTY0:
                        #         varQTY0 = varQTY0.split("varQTY0=")[1].split(")")[0]
                        #         print(varQTY0)
                        #         command = str(command).replace("{varQTY0}", varQTY0)

                        Color_PO.consoleColor("31", "33", str(j+1) + ", " + command, "")
                        self.log = self.log + "\n" + str(j+1) + ", " + command  # 步骤日志
                        # a = eval(command)
                        a = self.sql(command)
                        sleep(1)

                        if a != None:
                            if isinstance(a, list):
                                if isinstance(a[0], dict):
                                    # print(a[0])

                                    if "ID" in a[0]:
                                        varID = a[0]['ID']
                                        self.Openpyxl_PO.setCell(21, 1, "varID=" + str(varID), "sql")
                                    if "ID_CARD" in a[0]:
                                        varIdcard = a[0]['ID_CARD']
                                        self.Openpyxl_PO.setCell(22, 1, "varIdcard=" + str(varIdcard), "sql")
                                    if "QTY" in a[0]:
                                        varQTY = a[0]['QTY']
                                        self.Openpyxl_PO.setCell(23, 1, "varQTY=" + str(varQTY), "sql")
                                    if "GUID" in a[0]:
                                        varGUID = a[0]['GUID']
                                        self.Openpyxl_PO.setCell(26, 1, "varGUID=" + str(varGUID), "sql")
                                    if "QTY0" in a[0]:
                                        varQTY0 = a[0]['QTY0']
                                        d_all['QTY0'] = str(a[0]['QTY0'])
                                        # print(varQTY0)
                                        # Openpyxl_PO.setCell(27, 1, "varQTY0=" + str(varQTY0), "sql")
                                    if "name" in a[0]:
                                        self.Openpyxl_PO.setCell(24, 1, "", "sql")
                                        self.Openpyxl_PO.setCell(25, 1, "", "sql")
                                        if "跑规则" == a[0]['name']:
                                            if a[0]['value'] != 200:
                                                self.Openpyxl_PO.setCell(24, 1, str(a[0]['value']), "sql")
                                        if "新增评估" == a[0]['name']:
                                            if a[0]['value'] != 200:
                                                self.Openpyxl_PO.setCell(25, 1, str(a[0]['value']), "sql")

                                    # JB001
                                    if d['diseaseRuleCode'] == 'GW_JB001':
                                        if "GW_JB001" in a[0]: d_all['GW_JB001'] = str(a[0]['GW_JB001'])
                                        if "PG_Age001" in a[0]: d_all['PG_Age001'] = str(a[0]['PG_Age001'])
                                        if "PG_SHXG001" in a[0]:d_all['PG_SHXG001'] = str(a[0]['PG_SHXG001'])
                                        if "PG_SHXG002" in a[0]:d_all['PG_SHXG002'] = str(a[0]['PG_SHXG002'])
                                        if "PG_STZB001" in a[0]:d_all['PG_STZB001'] = str(a[0]['PG_STZB001'])
                                        if "PG_STZB002" in a[0]:d_all['PG_STZB002'] = str(a[0]['PG_STZB002'])
                                        if "PG_SHXG004" in a[0]:d_all['PG_SHXG004'] = str(a[0]['PG_SHXG004'])
                                        if "PG_JYZB001" in a[0]:d_all['PG_JYZB001'] = str(a[0]['PG_JYZB001'])
                                        if "PG_JYZB002" in a[0]:d_all['PG_JYZB002'] = str(a[0]['PG_JYZB002'])
                                        if "PG_JZS001" in a[0]: d_all['PG_JZS001'] = str(a[0]['PG_JZS001'])
                                        if "PG_JWS001" in a[0]: d_all['PG_JWS001'] = str(a[0]['PG_JWS001'])
                                    elif d['diseaseRuleCode'] == 'GW_JB002':
                                        if "GW_JB002" in a[0]: d_all['GW_JB002'] = str(a[0]['GW_JB002'])
                                        if "PG_Age002" in a[0]: d_all['PG_Age002'] = str(a[0]['PG_Age002'])
                                        if "PG_JYZB003" in a[0]: d_all['PG_JYZB003'] = str(a[0]['PG_JYZB003'])
                                        if "PG_JWS002" in a[0]: d_all['PG_JWS002'] = str(a[0]['PG_JWS002'])
                                        if "PG_JWS003" in a[0]: d_all['PG_JWS003'] = str(a[0]['PG_JWS003'])
                                        if "PG_JWS004" in a[0]: d_all['PG_JWS004'] = str(a[0]['PG_JWS004'])
                                        if "PG_JWS005" in a[0]: d_all['PG_JWS005'] = str(a[0]['PG_JWS005'])
                                        if "PG_JWS006" in a[0]: d_all['PG_JWS006'] = str(a[0]['PG_JWS006'])
                                        if "PG_JWS007" in a[0]: d_all['PG_JWS007'] = str(a[0]['PG_JWS007'])
                                        if "PG_JZS002" in a[0]: d_all['PG_JZS002'] = str(a[0]['PG_JZS002'])
                                        if "PG_YWZL001" in a[0]: d_all['PG_YWZL001'] = str(a[0]['PG_YWZL001'])
                                        if "PG_SHXG004" in a[0]: d_all['PG_SHXG004'] = str(a[0]['PG_SHXG004'])
                                        if "PG_JYZB004" in a[0]: d_all['PG_JYZB004'] = str(a[0]['PG_JYZB004'])
                                        if "PG_JYZB005" in a[0]: d_all['PG_JYZB005'] = str(a[0]['PG_JYZB005'])
                                        if "PG_YWZL002" in a[0]: d_all['PG_YWZL002'] = str(a[0]['PG_YWZL002'])
                                        if "PG_STZB001" in a[0]: d_all['PG_STZB001'] = str(a[0]['PG_STZB001'])
                                        if "PG_STZB003" in a[0]: d_all['PG_STZB003'] = str(a[0]['PG_STZB003'])
                                    elif d['diseaseRuleCode'] == 'GW_JB003':
                                        if "GW_JB003" in a[0]: d_all['GW_JB003'] = str(a[0]['GW_JB003'])
                                        if "PG_JWS008" in a[0]: d_all['PG_JWS008'] = str(a[0]['PG_JWS008'])
                                        if "PG_JWS007" in a[0]: d_all['PG_JWS007'] = str(a[0]['PG_JWS007'])
                                        if "PG_JWS001" in a[0]: d_all['PG_JWS001'] = str(a[0]['PG_JWS001'])
                                        if "PG_JZS003" in a[0]: d_all['PG_JZS003'] = str(a[0]['PG_JZS003'])
                                        if "PG_SHXG004" in a[0]: d_all['PG_SHXG004'] = str(a[0]['PG_SHXG004'])
                                        if "PG_SHXG005" in a[0]: d_all['PG_SHXG005'] = str(a[0]['PG_SHXG005'])
                                        if "PG_JYZB001" in a[0]: d_all['PG_JYZB001'] = str(a[0]['PG_JYZB001'])
                                        if "PG_STZB004" in a[0]: d_all['PG_STZB004'] = str(a[0]['PG_STZB004'])
                                        if "PG_JWS009" in a[0]: d_all['PG_JWS009'] = str(a[0]['PG_JWS009'])
                                        if "PG_JWS010" in a[0]: d_all['PG_JWS010'] = str(a[0]['PG_JWS010'])
                                        if "PG_JWS011" in a[0]: d_all['PG_JWS011'] = str(a[0]['PG_JWS011'])
                                    elif d['diseaseRuleCode'] == 'GW_JB004':
                                        if "GW_JB004" in a[0]: d_all['GW_JB004'] = str(a[0]['GW_JB004'])
                                        if "PG_Age003" in a[0]: d_all['PG_Age003'] = str(a[0]['PG_Age003'])
                                        if "PG_JWS001" in a[0]: d_all['PG_JWS001'] = str(a[0]['PG_JWS001'])
                                        if "PG_JWS007" in a[0]: d_all['PG_JWS007'] = str(a[0]['PG_JWS007'])
                                        if "PG_JZS004" in a[0]: d_all['PG_JZS004'] = str(a[0]['PG_JZS004'])
                                        if "PG_JZS005" in a[0]: d_all['PG_JZS005'] = str(a[0]['PG_JZS005'])
                                        if "PG_JYZB006" in a[0]: d_all['PG_JYZB006'] = str(a[0]['PG_JYZB006'])
                                        if "PG_JYZB007" in a[0]: d_all['PG_JYZB007'] = str(a[0]['PG_JYZB007'])
                                        if "PG_JYZB008" in a[0]: d_all['PG_JYZB008'] = str(a[0]['PG_JYZB008'])
                                        if "PG_JYZB009" in a[0]: d_all['PG_JYZB009'] = str(a[0]['PG_JYZB009'])
                                        if "PG_JWS012" in a[0]: d_all['PG_JWS012'] = str(a[0]['PG_JWS012'])
                                    elif d['diseaseRuleCode'] == 'GW_JB005':
                                        if "GW_JB005" in a[0]: d_all['GW_JB005'] = str(a[0]['GW_JB005'])
                                        # if "PG_Age004" in a[0]: d_all['PG_Age004'] = str(a[0]['PG_Age004'])
                                        if "PG_SHXG005" in a[0]: d_all['PG_SHXG005'] = str(a[0]['PG_SHXG005'])
                                        if "PG_JWS013" in a[0]: d_all['PG_JWS013'] = str(a[0]['PG_JWS013'])
                                        if "PG_JZS006" in a[0]: d_all['PG_JZS006'] = str(a[0]['PG_JZS006'])
                                        if "PG_SHXG007" in a[0]: d_all['PG_SHXG007'] = str(a[0]['PG_SHXG007'])
                                        if "PG_JWS015" in a[0]: d_all['PG_JWS015'] = str(a[0]['PG_JWS015'])
                                        if "PG_STZB005" in a[0]: d_all['PG_STZB005'] = str(a[0]['PG_STZB005'])
                                    elif d['diseaseRuleCode'] == 'GW_JB006':
                                        if "GW_JB006" in a[0]: d_all['GW_JB006'] = str(a[0]['GW_JB006'])
                                        if "PG_Age005" in a[0]: d_all['PG_Age005'] = str(a[0]['PG_Age005'])
                                        if "PG_JWS016" in a[0]: d_all['PG_JWS016'] = str(a[0]['PG_JWS016'])
                                        if "PG_JWS017" in a[0]: d_all['PG_JWS017'] = str(a[0]['PG_JWS017'])
                                        if "PG_JWS018" in a[0]: d_all['PG_JWS018'] = str(a[0]['PG_JWS018'])
                                        if "PG_JZS007" in a[0]: d_all['PG_JZS007'] = str(a[0]['PG_JZS007'])
                                        if "PG_SHXG009" in a[0]: d_all['PG_SHXG009'] = str(a[0]['PG_SHXG009'])
                                        if "PG_SHXG005" in a[0]: d_all['PG_SHXG005'] = str(a[0]['PG_SHXG005'])
                                    elif d['diseaseRuleCode'] == 'GW_JB007':
                                        if "GW_JB007" in a[0]: d_all['GW_JB007'] = str(a[0]['GW_JB007'])
                                        if "PG_Age006" in a[0]: d_all['PG_Age006'] = str(a[0]['PG_Age006'])
                                        if "PG_JWS021" in a[0]: d_all['PG_JWS021'] = str(a[0]['PG_JWS021'])

                                    elif d['diseaseRuleCode'] == 'GW_JB009':
                                        if "GW_JB009" in a[0]: d_all['GW_JB009'] = str(a[0]['GW_JB009'])
                                        if "PG_Age007" in a[0]: d_all['PG_Age007'] = str(a[0]['PG_Age007'])
                                        if "PG_JWS026" in a[0]: d_all['PG_JWS026'] = str(a[0]['PG_JWS026'])
                                        if "PG_JWS027" in a[0]: d_all['PG_JWS027'] = str(a[0]['PG_JWS027'])
                                        if "PG_JWS028" in a[0]: d_all['PG_JWS028'] = str(a[0]['PG_JWS028'])
                                        if "PG_JWS031" in a[0]: d_all['PG_JWS031'] = str(a[0]['PG_JWS031'])
                                        if "PG_JWS032" in a[0]: d_all['PG_JWS032'] = str(a[0]['PG_JWS032'])
                                    elif d['diseaseRuleCode'] == 'GW_JB010':
                                        if "GW_JB010" in a[0]: d_all['GW_JB010'] = str(a[0]['GW_JB010'])
                                        if "PG_Age008" in a[0]: d_all['PG_Age008'] = str(a[0]['PG_Age008'])
                                        if "PG_JWS033" in a[0]: d_all['PG_JWS033'] = str(a[0]['PG_JWS033'])
                                        if "PG_JWS034" in a[0]: d_all['PG_JWS034'] = str(a[0]['PG_JWS034'])
                                        if "PG_JWS035" in a[0]: d_all['PG_JWS035'] = str(a[0]['PG_JWS035'])
                                        if "PG_JYZB010" in a[0]: d_all['PG_JYZB010'] = str(a[0]['PG_JYZB010'])
                                        if "PG_JWS037" in a[0]: d_all['PG_JWS037'] = str(a[0]['PG_JWS037'])
                                    elif d['diseaseRuleCode'] == 'GW_JB011':
                                        if "GW_JB011" in a[0]: d_all['GW_JB011'] = str(a[0]['GW_JB011'])
                                        if "PG_JWS041" in a[0]: d_all['PG_JWS041'] = str(a[0]['PG_JWS041'])
                                        if "PG_JWS043" in a[0]: d_all['PG_JWS043'] = str(a[0]['PG_JWS043'])

                            # if isinstance(a, tuple):
                            #     if "跑规则" in a[0]:
                            #         varRunRule = a[1]
                            #         Openpyxl_PO.setCell(24, 1, "varRunRule=" + str(varRunRule), "sql")
                            #     if "新增评估" in a[0]:
                            #         varNewAssess = a[1]
                            #         Openpyxl_PO.setCell(25, 1, "varNewAssess=" + str(varNewAssess), "sql")
                    else:
                        break
        self.Openpyxl_PO.setCell(21, 1, "", "sql")
        self.Openpyxl_PO.setCell(22, 1, "", "sql")
        self.Openpyxl_PO.setCell(23, 1, "", "sql")
        self.Openpyxl_PO.setCell(24, 1, "", "sql")
        self.Openpyxl_PO.setCell(25, 1, "", "sql")
        self.Openpyxl_PO.setCell(26, 1, "", "sql")
        self.Openpyxl_PO.setCell(27, 1, "", "sql")

        self.log = self.log + "\n" + str(d_all)
        return d_all, self.log
