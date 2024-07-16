# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2024-3-8
# Description: CHC规则包
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import subprocess
import pyperclip as pc
# 1、复制内容到剪贴板
# 2、粘贴剪贴板里的内容

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB_SQL("host"), Configparser_PO.DB_SQL("user"), Configparser_PO.DB_SQL("password"), Configparser_PO.DB_SQL("database"))  # 测试环境
# SqlServerPO = SqlServerPO(Configparser_PO.DB_DM("host"), Configparser_PO.DB_DM("user"), Configparser_PO.DB_DM("password"), Configparser_PO.DB_DM("port"))  # 测试环境

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

from PO.CharPO import *
Char_PO = CharPO()



class ChcrulePO():

    def __init__(self, sheetName=''):

        self.TOKEN = self.getToken(Configparser_PO.USER("user"), Configparser_PO.USER("password"))
        self.dbTable = Char_PO.chinese2pinyin(sheetName)
        self.dbTable = "a_" + self.dbTable
        self.sheetName = sheetName
        # print(self.sheetName)

        # 读取疾病身份证对应的表(a_jibingshenfenzheng)
        self.jbsfz = "a_" + Char_PO.chinese2pinyin(Configparser_PO.FILE("jbsfz"))
        # print(self.jbsfz)
        # 读取测试规则对应的表(a_ceshiguize)
        self.csgz = "a_" + Char_PO.chinese2pinyin(Configparser_PO.FILE("csgz"))
        # print(self.csgz)

    def createTable(self, sheetName):

        dbTable = Char_PO.chinese2pinyin(sheetName)
        dbTable = "a_" + dbTable
        # print(dbTable)

        Sqlserver_PO.execute("drop table if exists " + dbTable)
        # excel导入db
        Sqlserver_PO.xlsx2db(Configparser_PO.FILE("case"), dbTable, sheetName)

        if sheetName != "测试规则" and sheetName != "疾病身份证":
            Sqlserver_PO.execute("ALTER table %s alter column result varchar(999)" % (dbTable))  # 此列没数据，创建后是float，需转换成char
            Sqlserver_PO.execute("ALTER TABLE %s alter column id int not null" % (dbTable))  # 设置主id不能为Null
            Sqlserver_PO.execute("ALTER TABLE %s add PRIMARY KEY (id)" % (dbTable))  # 设置主键（条件是id不能为Null）
            Sqlserver_PO.execute("ALTER table %s alter column updateDate char(11)" % (dbTable))  # 将float改为char类型
            Sqlserver_PO.execute("ALTER table %s alter column updateDate DATE" % (dbTable))  # 注意sqlserver无法将float改为date，先将float改为char，再将char改为data，
        # Sqlserver_PO.execute("ALTER TABLE %s ADD id1 INT NOT NULL IDENTITY(1,1) primary key (id1) " % ('健康评估'))  # 新增id自增主键
        # Sqlserver_PO.execute("ALTER TABLE %s ADD var varchar(111)" % (tableName))  # 临时变量
        # 添加表注释
        Sqlserver_PO.execute("EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % ('(测试用例)' + sheetName, dbTable))  # sheetName=注释，dbTable=表名
        print("[ok] 表'%s(%s)'创建成功!" % (dbTable, sheetName))

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

        l_d_diseaseRuleCode_idcard = Sqlserver_PO.select("select diseaseRuleCode, idcard from %s" % (self.jbsfz))
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
        if Configparser_PO.SWITCH("interface") == "on":
            print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        sleep(2)
        if Configparser_PO.SWITCH("interface") == "on":
            Color_PO.consoleColor("31", "33", str_r, "")

        if 'code' in d_r:
            if d_r['code'] != 200:
                if Configparser_PO.SWITCH("SQL") == "on":
                    Color_PO.consoleColor("31", "31", str_r, "")
                self.log = self.log + "\n" + str_r
                return ([{'name':'重新评估', 'value' : "[ERROR => 重新评估(i_rerunExecuteRule) => " + str(str_r) + "]"}])
            else:
                return None
                # if Configparser_PO.SWITCH("SQL") == "on":
                #     Color_PO.consoleColor("31", "33", "重新评估(i_rerunExecuteRule) => " + str_r, "")
                # return ([{'name':'重新评估', 'value': 200}])
        else:
            if Configparser_PO.SWITCH("SQL") == "on":
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
        if Configparser_PO.SWITCH("interface") == "on":
            print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        sleep(2)

        if Configparser_PO.SWITCH("interface") == "on":
            Color_PO.consoleColor("31", "33", str_r, "")

        if 'code' in d_r:
            if d_r['code'] != 200:
                if Configparser_PO.SWITCH("SQL") == "on":
                    Color_PO.consoleColor("31", "31", str_r, "")
                self.log = self.log + "\n" + str_r
                return ([{'name':'新增评估', 'value' : "[ERROR => 新增评估(i_startAssess) => " + str(str_r) + "]"}])
            else:
                return None
                # if Configparser_PO.SWITCH("SQL") == "on":
                #     Color_PO.consoleColor("31", "33", "新增评估(i_startAssess) =>  => " + str_r, "")
                # return ([{'name':'新增评估', 'value': 200}])
        else:
            if Configparser_PO.SWITCH("SQL") == "on":
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
                command = 'Sqlserver_PO.select("' + varSql + '")'
                a = eval(command)
                sleep(1)
                return a
            elif varPrefix == 'update' or varPrefix == 'insert' or varPrefix == 'delete' :
                command = 'Sqlserver_PO.execute("' + varSql + '")'
                # todo 输出sql语句（调试）
                # print(command)
                a = eval(command)
                sleep(2)
                return a
            else:
                return None

    def verifyIdcard(self, varIdcard):

        # 检查患者主索引表身份证是否存在!
        l_d_qty = Sqlserver_PO.select("select count(*) as qty from TB_EMPI_INDEX_ROOT where IDCARDNO='%s'" % (varIdcard))
        # print(l_d_qty)  # [{'qty': 1}]
        if l_d_qty[0]['qty'] == 0:
            guid = Data_PO.getFigures(6)
            name = Data_PO.getChineseName()
            Sqlserver_PO.execute("INSERT INTO [TB_EMPI_INDEX_ROOT] ([GUID], [NAME], [SEXCODE], [SEXVALUE], [DATEOFBIRTH], [IDCARDNO]) VALUES ('" + str(guid) + "', N'" + str(name) + "', '2', '女', '1940-05-11', '" + str(varIdcard) + "')")

        # 检查基本信息表身份证是否存在!
        l_d_qty = Sqlserver_PO.select("select count(*) as qty from HRPERSONBASICINFO where IDCARD='%s'" % (varIdcard))
        if l_d_qty[0]['qty'] == 0:
            Sqlserver_PO.execute("INSERT INTO [dbo].[HRPERSONBASICINFO] ([ARCHIVENUM], [NAME], [SEX], [DATEOFBIRTH], [IDCARD], [WORKUNIT], [PHONE], [CONTACTSNAME], [CONTACTSPHONE], [RESIDENCETYPE], [NATIONCODE], [BLOODTYPE], [RHBLOODTYPE], [DEGREE], [OCCUPATION], [MARITALSTATUS], [HEREDITYHISTORYFLAG], [HEREDITYHISTORYCODE], [ENVIRONMENTKITCHENAERATION], [ENVIRONMENTFUELTYPE], [ENVIRONMENTWATER], [ENVIRONMENTTOILET], [ENVIRONMENTCORRAL], [DATASOURCES], [CREATEID], [CREATENAME], [CREATETIME], [UPDATEID], [UPDATENAME], [UPDATETIME], [STATUS], [ISDELETED], [VERSION], [WORKSTATUS], [TELEPHONE], [OCCUPATIONALDISEASESFLAG], [OCCUPATIONALDISEASESWORKTYPE], [OCCUPATIONALDISEASESWORKINGYEARS], [DUSTNAME], [DUSTFLAG], [RADIOACTIVEMATERIALNAME], [RADIOACTIVEMATERIALFLAG], [CHEMICALMATERIALNAME], [CHEMICALMATERIALFLAG], [OTHERNAME], [OTHERFLAG], [PHYSICSMATERIALNAME], [PHYSICSMATERIALFLAG], [DOWNLOADSTATUS], [NONUMBERPROVIDED], [YLZFMC], [PERSONID], [MEDICAL_PAYMENTCODE], [KALEIDOSCOPE], [ISGOVERNANCE]) VALUES ('" + str(varIdcard) + "', '高血压已患', '2', '1959-03-28 00:00:00.000', '" + str(varIdcard) + "', NULL, '13585543856', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2022-11-14 16:49:32.357', NULL, NULL, '2020-02-19 00:00:00.000', NULL, NULL, NULL, NULL, '13585543856', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,'0')")

        # 检查签约信息表身份证是否存在!
        l_d_qty = Sqlserver_PO.select("select count(*) as qty from QYYH where SFZH='%s'" % (varIdcard))
        if l_d_qty[0]['qty'] == 0:
            guid = Data_PO.getFigures(6)
            Sqlserver_PO.execute("INSERT INTO [dbo].[QYYH] ([CZRYBM], [CZRYXM], [JMXM], [SJHM], [SFZH], [JJDZ], [SFJD], [SIGNORGID], [ARCHIVEUNITCODE], [ARCHIVEUNITNAME], [DISTRICTORGCODE], [DISTRICTORGNAME], [TERTIARYORGCODE], [TERTIARYORGNAME], [PRESENTADDRDIVISIONCODE], [PRESENTADDRPROVCODE], [PRESENTADDRPROVVALUE], [PRESENTADDRCITYCODE], [PRESENTADDRCITYVALUE], [PRESENTADDRDISTCODE], [PRESENTADDDISTVALUE], [PRESENTADDRTOWNSHIPCODE], [PRESENTADDRTOWNSHIPVALUE], [PRESENTADDRNEIGHBORHOODCODE], [PRESENTADDRNEIGHBORHOODVALUE], [SIGNSTATUS], [SIGNDATE],[CATEGORY_CODE], [CATEGORY_NAME], [SEX_CODE], [SEX_NAME], [LAST_SERVICE_DATE], [ASSISTANT_DOC_ID], [ASSISTANT_DOC_NAME], [HEALTH_MANAGER_ID], [HEALTH_MANAGER_NAME], [ASSISTANT_DOC_PHONE], [HEALTH_MANAGER_PHONE]) VALUES ('" + str(guid) + "', N'姚皎情', N'肝癌高危', NULL, '" + str(varIdcard) + "', N'平安街道16号', NULL, NULL, '0000001', '静安精神病院', '310118000000', '青浦区', '12345', '上海人民医院', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '2020-06-01', 166, '4', N'1',N'男', NULL, NULL, NULL, NULL, NULL, NULL, NULL)")


    def runRow(self, dbId):

        # 按id执行

        self.dbId = dbId

        # todo 获取指定记录
        l_d_rows = Sqlserver_PO.select("select * from %s where id=%s" % (self.dbTable, self.dbId))

        # print(l_d_rows[0]) # {'id': 1, 'result': 'ok', 'updateDate': datetime.datetime(2023, 11, 7, 10, 4, 15), 'rule': 'r1', 'ruleParam': "AGE=55 .and. CATEGORY_CODE='2'", 'ruleCode': 'PG_Age001', '分类': '年龄', '规则名称': '年龄≥55岁', '评估规则详细描述': '年龄≥55岁', '评估因素判断规则': '年龄>=55', 'tester': '刘斌龙', 'var': ''}
        self.rule = l_d_rows[0]['rule']
        self.ruleParam = l_d_rows[0]['ruleParam']
        self.ruleCode = l_d_rows[0]['ruleCode']
        if 'diseaseRuleCode' in l_d_rows[0].keys():
            self.diseaseRuleCode = l_d_rows[0]['diseaseRuleCode']
        else:
            self.diseaseRuleCode = ""
        if 'hitQty' in l_d_rows[0].keys():
            self.hitQty = l_d_rows[0]['hitQty']
        else:
            self.hitQty= ""

        self._matchRule()

    def runRule(self, t_dbRule):

        # 按rule规则执行

        l_d_id = Sqlserver_PO.select("select id from %s where [rule] in %s" % (self.dbTable, t_dbRule))
        print(l_d_id)  # [{'id': 2}, {'id': 3}]
        for i in range(len(l_d_id)):
            self.runRow(l_d_id[i]['id'])

    def runResult(self, varResult):

        # 按result执行
        # r.runResult("error")  # 执行result为error的规则
        # r.runResult("all")  # 执行所有的规则(谨慎)

        if varResult == "all":
            l_d_id = Sqlserver_PO.select("select id from %s" % (self.dbTable))
            for i in range(len(l_d_id)):
                self.runRow(l_d_id[i]['id'])
        elif varResult != "ok":
            l_d_id = Sqlserver_PO.select("select id from %s where result <> 'ok'" % (self.dbTable))
            for i in range(len(l_d_id)):
                self.runRow(l_d_id[i]['id'])


    def _matchRule(self):
        # todo 适配相应的测试规则
        l_d_param = Sqlserver_PO.select("select param from %s where [rule]='%s'" % (self.csgz, self.rule))
        if l_d_param[0]['param'] == 'p1':
            # 带参数1
            self.param1()
        elif l_d_param[0]['param'] == 'p2':
            # 带参数2
            self.param2()
        elif l_d_param[0]['param'] == 'p4':
            # 带参数4
            self.param4()
        elif l_d_param[0]['param'] == 'p1_auto':
            # 带参数1且获取自动身份证
            self.param1_auto()
        elif l_d_param[0]['param'] == 'p2_auto':
            # 带参数2且获取自动身份证
            self.param2_auto()
        elif l_d_param[0]['param'] == 'p4_auto':
            # 带参数4且获取自动身份证
            self.param4_auto()
        elif l_d_param[0]['param'] == 'p1_idcard':
            # 带参数1且自动匹配疾病身份证
            self.param1_idcard()
        elif l_d_param[0]['param'] == 'p2_idcard':
            # 带参数2且自动匹配疾病身份证
            self.param2_idcard()
        elif l_d_param[0]['param'] == 'p1_hit2':
            # 带参数1，健康干预两次命中（干预+疾病评估）
            self.param1_idcard_hitQty2()
        elif l_d_param[0]['param'] == 'p3_hit2':
            # 带参数3，健康干预两次命中（干预+疾病评估）
            self.param3_idcard_hitQty2()
        elif l_d_param[0]['param'] == 'r_GW':
            self._getParamByGW()


    def getSql(self):
        
        # 获取sql语句

        # todo 输出第一行
        print("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + self.rule + ")]")

        # Color_PO.consoleColor("31", "33", (("[" + str(self.dbTable) + " => " + str(self.dbId) + "(" + rule + ")]").center(100, '-')), "")
        l_0 = Sqlserver_PO.select("select sql from %s where [rule]='%s'" %(self.csgz, self.rule))
        l_sql = []
        for i in range(len(l_0)):
            if os.name == "posix":
                l_sql.append(l_0[i]['sql'])
            else:
                l_sql.append(l_0[i]['sql'].encode('latin1').decode('GB2312'))
        return l_sql


    def param1(self):
        d = {}
        d['l_sql'] = self.getSql()
        d['ruleParam'] = self.ruleParam.replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        self.outResult1(self.testRule(d))

    def param2(self):
        d = {}
        d['l_sql'] = self.getSql()
        l_ruleParam = Str_PO.str2list(self.ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        self.outResult1(self.testRule(d))

    def param4(self):
        d = {}
        d['l_sql'] = self.getSql()
        l_ruleParam = Str_PO.str2list(self.ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleParam4'] = l_ruleParam[3].replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        self.outResult1(self.testRule(d))

    def param4_auto(self):
        d = {}
        d['l_sql'] = self.getSql()
        l_ruleParam = Str_PO.str2list(self.ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleParam4'] = l_ruleParam[3].replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        self._getAutoIdcard(d)

    def param1_auto(self):
        d = {}
        d['l_sql'] = self.getSql()
        d['ruleParam'] = self.ruleParam.replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        self._getAutoIdcard(d)

    def param1_idcard(self):
        d = {}
        d['l_sql'] = self.getSql()
        d['ruleParam'] = self.ruleParam.replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        d['diseaseRuleCode'] = self.diseaseRuleCode
        self._getDiseaseIdcard2(d)

    def param2_auto(self):
        d = {}
        d['l_sql'] = self.getSql()
        l_ruleParam = Str_PO.str2list(self.ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        self._getAutoIdcard(d)

    def param2_idcard(self):
        d = {}
        d['l_sql'] = self.getSql()
        l_ruleParam = Str_PO.str2list(self.ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        d['diseaseRuleCode'] = self.diseaseRuleCode
        self._getDiseaseIdcard2(d)

    def param1_idcard_hitQty2(self):
        d = {}
        d['l_sql'] = self.getSql()
        d['ruleParam'] = self.ruleParam.replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        d['diseaseRuleCode'] = self.diseaseRuleCode
        d['hitQty'] = self.hitQty
        self._getDiseaseIdcard2(d)

    def param3_idcard_hitQty2(self):
        d = {}
        d['l_sql'] = self.getSql()
        l_ruleParam = Str_PO.str2list(self.ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        d['diseaseRuleCode'] = self.diseaseRuleCode
        d['hitQty'] = self.hitQty
        self._getDiseaseIdcard2(d)

    def _getParamByGW(self):
        d = {}
        d['l_sql'] = self.getSql()
        d['ruleCode'] = self.ruleCode
        d['diseaseRuleCode'] = self.diseaseRuleCode
        self._getDiseaseIdcardGW(d)


    def outResult1(self, varQty):

        if varQty == 1:
            Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
        else:
            # Color_PO.consoleColor("31", "31", (("[" + str(self.dbTable) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
            # self.log = "[error]\n" + self.log
            print(self.log)
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
        Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))

    def outResult2(self, varQty):

        if varQty == 2:
            Color_PO.consoleColor("31", "36", (("[" + str(self.dbTable) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
        else:
            # print("step log".center(100, "-"))
            # self.log = "error," + self.log
            print(self.log)
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", (("[" + str(self.dbTable) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
        Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))

    def outResultGW(self, d_actual):

        varSign = 0
        d_error = {}
        for k, v in d_actual.items():
            if (k == "QTY0" and v == 0) or (k != "QTY0" and v == 1):
                varSign = varSign + 0
            else:
                varSign = varSign + 1
                d_error[k] = v

        if Configparser_PO.SWITCH("SQL") == "on":
            print('值 => ' + str(d_actual))

        if varSign == 0:
            Color_PO.consoleColor("31", "36", (("[" + str(self.dbTable) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
            Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
            # Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTable, self.dbId))
        else:
            print("step log".center(100, "-"))
            self.log = "error," + self.log
            print(self.log)
            Color_PO.consoleColor("31", "31", '错误值 => ' + str(d_error), "")
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", (("[" + str(self.dbTable) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
            Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
            # Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTable, self.dbId))

    def _getAutoIdcard(self, d):

        # 随机获取疾病身份证中身份证

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
                self.outResult2(self.testRule(d))
            else:
                self.outResult1(self.testRule(d))
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
                self.outResult2(self.testRule(d))
            else:
                self.outResult1(self.testRule(d))
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



    def testRule(self, d):

        # 执行r规则

        # print(d)  # {'rule': ['select top(1) ID,ID_CARD from T_ASSESS_INFO order by ID desc', "UPDATE T_ASSESS_INFO set {测试规则参数} where ID_CARD = '{varIdcard}'", "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'", 'self.i_rerunExecuteRule({varID})', "select count(*) QTY from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE= '{规则编码}'"], 'ruleParam': "AGE=55 , CATEGORY_CODE='2'", 'ruleCode': 'PG_Age001'}
        l_sql = d['l_sql']

        self.log = ""
        varQTY = 0
        varQ2 = 0

        for i in range(len(l_sql)):

            # 格式化sql
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

        # 获取临时变量
        d_update = {}  # 更新数据
        d_clipboard = {}  # 新数据
        for i in range(len(l_sql)):
            clipboard = pc.paste()  # 从剪贴板获取数据

            if "{" in clipboard:
                d_clipboard = Str_PO.str2dict(clipboard)
                d_update.update(d_clipboard)  # 新数据合并到更新数据中
                if 'ID' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{ID}", str(d_update['ID']))
                if 'IDCARD' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{IDCARD}", str(d_update['IDCARD']))
                if 'ID_CARD' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{ID_CARD}", str(d_update['ID_CARD']))
                if 'GUID' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{GUID}", str(d_update['GUID']))

            # todo 输出sql语句
            if Configparser_PO.SWITCH("SQL") == "on":
                print(str(i + 1) + ", " + l_sql[i])  # 1, delete from T_ASSESS_INFO where ID_CARD = '310101202308070003'

            # 记录步骤日志
            if self.log == "":
                self.log = str(i + 1) + ", " + l_sql[i]
            else:
                self.log = self.log + "\n" + str(i + 1) + ", " + l_sql[i]

            # todo 执行sql
            a = self.runSql(l_sql[i])


            if a != None:
                if isinstance(a, list) and a != []:
                    if isinstance(a[0], dict):
                        pc.copy(str(a[0]))  # 复制到剪贴板
                        if Configparser_PO.SWITCH("SQL") == "on":
                            Color_PO.consoleColor("31", "33", a[0], "")  # 橙色显示参数值 {'ID': 498228, 'ID_CARD': '110101193001191103'}

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
                    l_sql[i] = str(l_sql[i]).replace("{ID}", str(d_update['ID']))
                if 'IDCARD' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{IDCARD}", str(d_update['IDCARD']))
                if 'GUID' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{GUID}", str(d_update['GUID']))

            # todo 输出sql语句 - gw
            if Configparser_PO.SWITCH("SQL") == "on":
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
                        if Configparser_PO.SWITCH("SQL") == "on":
                            for k, v in a[0].items():
                                if k == "QTY0" or k == "ID":
                                    Color_PO.consoleColor("31", "33", a[0], "")
                                else:
                                    if v != 1 :
                                        Color_PO.consoleColor("31", "31", a[0], "")
                                    else:
                                        Color_PO.consoleColor("31", "33", a[0], "")
                        # print(a[0])
                        # print(d_actual)
                        from collections import ChainMap
                        d_actual = dict(ChainMap(a[0], d_actual))
                        # d_actual = Dict_PO.mergeDictReserveFirstKey(a[0], d_actual)  # {'a': 1, 'b': 2, 'dev': 30, 'test': 3}

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
