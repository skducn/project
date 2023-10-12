# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-8-1
# Description:
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from ConfigparserPO import *
Configparser_PO = ConfigparserPO()

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



class ChcRulePO():

    def __init__(self, d_sheetName_colTitle):

        self.clsApp("Microsoft Excel")
        # self.Openpyxl_PO = OpenpyxlPO("健康评估规则表自动化1.xlsx")
        self.Openpyxl_PO = OpenpyxlPO(Configparser_PO.EXCEL("name"))

        # 1,获取登录用户的token
        # self.TOKEN = self.getToken("jh", "12345678")  #
        self.TOKEN = self.getToken(Configparser_PO.USER("user"), Configparser_PO.USER("password"))

        self.sheetName = d_sheetName_colTitle['sheetName']
        # print(d_sheetName_colTitle['colTitle'])

        l_colSeq = self.Openpyxl_PO.title2colSeq(d_sheetName_colTitle['colTitle'], self.sheetName)
        # print(l_colSeq)

        self.l_l_row = self.Openpyxl_PO.getRowByPartialCol(l_colSeq, self.sheetName)
        self.l_l_row.pop(0)
        # print(self.l_l_row)  # [['OK', "r1,AGE=55 .and. CATEGORY_CODE='2'", 'PG_Age001'], ['OK', "r1,AGE=56 .and. CATEGORY_CODE='2'", 'PG_Age001'],...]]

        d_seq_row = {}
        for i in range(len(self.l_l_row)):
            d_seq_row[i+2] = self.l_l_row[i]
        # print(d_seq_row)  # {2: ['OK', "r1,AGE=55 .and. CATEGORY_CODE='2'", 'PG_Age001'], 3: ['OK', "r1,AGE=56 .and. CATEGORY_CODE='2'", 'PG_Age001'],...}
        self.d_seq_row = d_seq_row

    def open(self):
        self.Openpyxl_PO.open()

    def clsApp(self, varApp):

        '''
        关闭应用程序
        :param varApp:
        :return:
         # clsApp("chrome.exe")
        '''

        l_pid = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_pid.append(pid)
        for i in range(len(l_pid)):
            p = psutil.Process(l_pid[i])
            p.terminate()

    def getToken(self, varUser, varPass):

        # 1,获取登录用户的token
        command = "curl -X POST \"" + Configparser_PO.HTTP("url") + ":8012/login\" -H \"accept: */*\" -H \"Content-Type: application/json\" -d \"{ \\\"password\\\": \\\"" + str(varPass) + "\\\", \\\"username\\\": \\\"" + str(varUser) + "\\\"}\""
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        print(d_r['data']['access_token'])
        return d_r['data']['access_token']


    def getDiseaseIdcard(self):

        '''
        获取疾病身份证中对应疾病的身份证号码
        :param
        :return: {'YH_JB001': '310101202308070001', 'YH_JB002': '310101202308070002'}
        '''

        l_code_Idcard = self.Openpyxl_PO.getColByPartialColByUnwantedRow([1, 3], [1], "疾病身份证")
        d_code_Idcard = dict(zip(l_code_Idcard[0], l_code_Idcard[1]))
        return (d_code_Idcard)  # {'YH_JB001': '310101202308070001', 'YH_JB002': '310101202308070002'}

    def i_rerunExecuteRule(self, var):

        '''
        重新评估 
        :param var:
        :param token:
        :return:
        '''

        command = "curl -X GET \"" + Configparser_PO.HTTP("url") + ":8011/server/tAssessInfo/rerunExecuteRule/" + str(var) + "\" -H \"accept: */*\" -H \"Content-Type: application/json\" -H \"Authorization:" + str(self.TOKEN) + "\""
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # print(d_r)
        # print(command)
        # sleep(2)
        var = "[ERROR => i_rerunExecuteRule() => " + str(str_r) + "]"
        if 'code' in d_r:
            if d_r['code'] != 200:
                Color_PO.consoleColor("31", "31", command, "")
                Color_PO.consoleColor("31", "31", var, "")
                return ([{'name': '跑规则', 'value': var}])
            else:
                return ([{'name': '跑规则', 'value': 200}])
        else:
            Color_PO.consoleColor("31", "31", command, "")  # # {"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            Color_PO.consoleColor("31", "31", var, "")
            return ([{'name':'跑规则', 'value': var}])

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

        # print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        sleep(1)
        # print(d_r)

        var = "[ERROR => i_startAssess() => " + str(str_r) + "]"
        if 'code' in d_r:
            if d_r['code'] != 200:
                Color_PO.consoleColor("31", "31", var, "")
                # print(var)
                return ([{'name':'新增评估', 'value' : var}])
            else:
                return ([{'name':'新增评估', 'value': 200}])
        else:
            # {"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            return ([{'name':'新增评估', 'value': var}])

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
                return a
            elif varPrefix == 'update' or varPrefix == 'insert' or varPrefix == 'delete' :
                command = 'Sqlserver_PO.execute("' + varSql + '")'
                a = eval(command)
                return a
            else:
                return None



    def outResult1(self, varQty, varLog, k):

        if varQty == "1" or varQty == 1:
            self.Openpyxl_PO.setCellValue(k, 1, "OK", self.sheetName)
            Color_PO.consoleColor("31", "36", "[" + str(k) + " => OK]\n", "")
            self.Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), self.sheetName)
            self.Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=self.sheetName)
            self.Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=self.sheetName)
        else:
            self.Openpyxl_PO.setCellValue(k, 1, "ERROR", self.sheetName)
            Color_PO.consoleColor("31", "31", "[" + str(k) + " => ERROR]\n", "")
            self.Openpyxl_PO.setCellValue(k, 2, varLog, self.sheetName)
            self.Openpyxl_PO.setCellFont(k, "A", color="ff0000", varSheet=self.sheetName)
            self.Openpyxl_PO.setCellFont(k, "B", color="ff0000", varSheet=self.sheetName)


    def outResult2(self, varQty, varLog, k):

        if varQty == "2" or varQty == 2:
            Color_PO.consoleColor("31", "36", "[" + str(k) + " => OK]\n", "")
            self.Openpyxl_PO.setCellValue(k, 1, "OK", self.sheetName)
            self.Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), self.sheetName)
            self.Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=self.sheetName)
            self.Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=self.sheetName)
        else:
            self.Openpyxl_PO.setCellValue(k, 1, "ERROR", self.sheetName)
            Color_PO.consoleColor("31", "31", "[" + str(k) + " => ERROR]\n", "")
            self.Openpyxl_PO.setCellValue(k, 2, varLog, self.sheetName)
            self.Openpyxl_PO.setCellFont(k, "A", color="ff0000", varSheet=self.sheetName)
            self.Openpyxl_PO.setCellFont(k, "B", color="ff0000", varSheet=self.sheetName)


    def outResultGW(self, result, log, k, v5):

        if result == 1:
            Color_PO.consoleColor("31", "36", "[" + str(v5) + " => OK]\n", "")
            self.Openpyxl_PO.setCellValue(k, 1, "OK", self.sheetName)
            self.Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), self.sheetName)
            self.Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=self.sheetName)
            self.Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=self.sheetName)
        else:
            Color_PO.consoleColor("31", "31", "[" + str(v5) + " => ERROR]\n", "")
            self.Openpyxl_PO.setCellValue(k, 1, "ERROR", self.sheetName)
            self.Openpyxl_PO.setCellValue(k, 2, log, self.sheetName)
            self.Openpyxl_PO.setCellFont(k, "A", color="ff0000", varSheet=self.sheetName)
            self.Openpyxl_PO.setCellFont(k, "B", color="ff0000", varSheet=self.sheetName)


    def _getIdcard(self, d, k):

        # 获取身份证

        varIdcard = None
        d_code_idcard = self.getDiseaseIdcard()
        for k1, v1 in d_code_idcard.items():
            if k1 == d['diseaseRuleCode']:
                varIdcard = v1
                break
        d["varIdcard"] = varIdcard
        if varIdcard != None:
            varQty, varLog = self.rule(d)
            self.outResult1(varQty, varLog, k)
        else:
            print("[ERROR => _getIdcard() => 身份证为None!]")


    def _getIdcard2(self,d, k):

        # 健康干预命中次数之获取身份证

        varIdcard = None
        d_code_idcard = self.getDiseaseIdcard()
        for k1, v1 in d_code_idcard.items():
            if k1 == d['diseaseRuleCode']:
                varIdcard = v1
                break
        d["varIdcard"] = varIdcard
        if varIdcard != None:
            varQty, varLog = self.rule(d)
            if d['hitQty'] == 2:
                self.outResult2(varQty, varLog, k)
            elif d['hitQty'] == None:
                self.outResult1(varQty, varLog, k)
        else:
            print("[ERROR => _getIdcard2() => 身份证为None!]")





    def run(self, varA, varC_rule):

        '''
        筛选执行条件
        :param varA: 测试结果
        :param varC_rule: 测试规则名
        :return: none
        '''

        if varA == None:
            if varC_rule == None:
                self.runAll(varA)  # None, None
            else:
                self.runRule(varA, varC_rule)  # None, "r1"
        else:
            if varC_rule == None:
                self.runAll(varA)  # "ERROR", None
            else:
                self.runRule(varA, varC_rule)  # "OK", "r1"
        self.Openpyxl_PO.setAllCellDimensionsHeight(30, self.sheetName)

    def runAll(self, var1):
        for k, v in self.d_seq_row.items():
            if v[1] != None:
                if var1 == None and v[0] == None:
                    self.main(k, v)
                elif var1 == "OK" and v[0] == "OK":
                    self.main(k, v)
                elif var1 == "ERROR" and v[0] == "ERROR":
                    self.main(k, v)
                elif var1 == "ALL":
                    self.main(k, v)

    def runRule(self, var1, var3_rule):
        for k, v in self.d_seq_row.items():
            if v[1] != None:
                if var1 == None and v[0] == None:
                    self.main_rule(k, v, var3_rule)
                elif var1 == "OK" and v[0] == "OK":
                    self.main_rule(k, v, var3_rule)
                elif var1 == "ERROR" and v[0] == "ERROR":
                    self.main_rule(k, v, var3_rule)
                elif var1 == "ALL":
                    self.main_rule(k, v, var3_rule)

    def main(self, k, v):

        '''
        筛选测试规则参数
        :param k: 第几行
        :param v: 行数据（测试结果，测试规则，干预编码...）
        :return:
        '''

        # 格式化测试规则
        try:
            l_v1 = Str_PO.str2list(v[1])
            # print(l_v1)  # ['r11', "AGE='58'.and.DRINKING_FREQUENCY_CODE='3'"]
            varParam = l_v1[1] .replace(".and.", ',')
        except:
            Color_PO.consoleColor("31", "31", "[ERROR => main() => '" + self.sheetName + "', line " + str(k) + ", 测试规则 '" + str(v[1]) + "' 错误!]", "")


        if (l_v1[0] == "r1") or (l_v1[0] == "r6") or (l_v1[0] == "r12") :
            # 带参数1
            self.param1(v, l_v1, k)
            # self.param1(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif (l_v1[0] == "r3") or (l_v1[0] == "r4") or (l_v1[0] == "r8"):
            # 带参数2
            self.param2(v, l_v1, k)
        elif l_v1[0] == "r7":
            # 带参数4
            self.param4(v, l_v1, k)
        elif (l_v1[0] == "r9") or (l_v1[0] == "r10"):
            # 带参数1（自动匹配身份证）
            self.param1_idcard(v, l_v1, k)
        elif l_v1[0] == "r2":
            # 带参数2（自动匹配身份证）
            self.param2_idcard(v, l_v1, k)
        elif l_v1[0] == "r11":
            # 带参数1，健康干预两次命中（干预+疾病评估）
            self.param1_idcard_hitQty2(v, l_v1, k)
        elif l_v1[0] == "r5":
            # 带参数3，健康干预两次命中（干预+疾病评估）
            self.param3_idcard_hitQty2(v, l_v1, k)

    def main_rule(self, k, v, var3_rule):

        '''
        筛选测试规则参数（规则）
        :param k: 第几行
        :param v: 行数据（测试结果，测试规则，干预编码...）
        :return:
        '''

        try:
            l_v1 = Str_PO.str2list(v[1])
            # print(l_v1)  # ['r11', "AGE='58'.and.DRINKING_FREQUENCY_CODE='3'"]
            varParam = l_v1[1] .replace(".and.", ',')
        except:
            Color_PO.consoleColor("31", "31", "[ERROR => main_rule() => '" + self.sheetName + "', line " + str(k) + ", 测试规则 '" + str(v[1]) + "' 错误!]", "")

        if (l_v1[0] == "r1" and var3_rule == "r1") or (l_v1[0] == "r6" and var3_rule == "r6") or (l_v1[0] == "r12" and var3_rule == "r12"):
            # 带参数1
            self.param1(v, l_v1, k)
        elif (l_v1[0] == "r3" and var3_rule == "r3") or (l_v1[0] == "r4" and var3_rule == "r4") or (l_v1[0] == "r8" and var3_rule == "r8"):
            # 带参数2
            self.param2(v, l_v1, k)
        elif l_v1[0] == "r7" and var3_rule == "r7":
            # 带参数4
            self.param4(v, l_v1, k)
        elif (l_v1[0] == "r9" and var3_rule == "r9") or (l_v1[0] == "r10" and var3_rule == "r10") :
            # 带参数1（自动匹配身份证）
            self.param1_idcard(v, l_v1, k)
        elif l_v1[0] == "r2" and var3_rule == "r2":
            # 带参数2（自动匹配身份证）
            self.param2_idcard(v, l_v1, k)
        elif l_v1[0] == "r11" and var3_rule == "r11":
            # 带参数1，健康干预两次命中（干预+疾病评估）
            self.param1_idcard_hitQty2(v, l_v1, k)
        elif l_v1[0] == "r5" and var3_rule == "r5":
            # 带参数3，健康干预两次命中（干预+疾病评估）
            self.param3_idcard_hitQty2(v, l_v1, k)
        elif l_v1[0] == "GW" and var3_rule == "GW":

            d = {}
            d['result'] = v[0]
            d['diseaseRuleCode'] = v[2]
            d['interventionRule'] = v[3]
            Color_PO.consoleColor("31", "36", ("[" + str(self.sheetName) + " => " + str(k) + "(" + str(v[2]) + ")]"), "")
            # 格式化测试规则
            # print(l_v1) # ['GW', 'QTY0:0', 'PG_SHXG005:1', 'PG_SHXG007:1', 'PG_STZB005:1', 'PG_JZS006:1', 'PG_JWS015:1', 'PG_JWS013:1']
            l_v1.pop(0)
            d_v1 = List_PO.list2dictByKeyValue(l_v1)
            # 获取身份证（在"疾病身份证" sheet中获取对应的身份证）
            varIdcard = None
            d_code_idcard = self.getDiseaseIdcard()
            for k1, v1 in d_code_idcard.items():
                if k1 == d['diseaseRuleCode']:
                    varIdcard = v1
                    break
            d["varIdcard"] = varIdcard

            # 执行语句及输出
            print(d)
            d_all, log = self.gw(d)
            print("预期：", d_v1)
            print("实测：", d_all)
            if d_all == d_v1:
                self.outResultGW(1, log, k, v[2])
            else:
                self.outResultGW(0, log, k, v[2])

    def param1(self, v, l_v1, k):

        Color_PO.consoleColor("31", "36", ("[" + str(self.sheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        d = {}
        d['result'] = v[0]  # OK
        d['testRuleName'] = l_v1[0]  # r1
        d['testRuleParam'] = l_v1[1].replace(".and.", ',')  # AGE='58'.and.DRINKING_FREQUENCY_CODE='3'
        d['interventionRule'] = v[2]  # GY_GW001001  //干预规则编码
        varQty, varLog = self.rule(d)
        self.outResult1(varQty, varLog, k)


    def param2(self, v, l_v1, k):

        Color_PO.consoleColor("31", "36", ("[" + str(self.sheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        d = {}
        d['result'] = v[0]
        d['testRuleName'] = l_v1[0]
        d['testRuleParam1'] = l_v1[1]
        d['testRuleParam2'] = l_v1[2].replace(".and.", ',')
        d['interventionRule'] = v[2]
        varQty, varLog = self.rule(d)
        self.outResult1(varQty, varLog, k)


    def param4(self, v, l_v1, k):

        Color_PO.consoleColor("31", "36", ("[" + str(self.sheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        d = {}
        d['result'] = v[0]
        d['testRuleName'] = l_v1[0]
        d['testRuleParam1'] = l_v1[1]
        d['testRuleParam2'] = l_v1[2]
        d['testRuleParam3'] = l_v1[3]
        d['testRuleParam4'] = l_v1[4]
        d['interventionRule'] = v[2]
        varQty, varLog = self.rule(d)
        self.outResult1(varQty, varLog, k)


    def param1_idcard(self, v, l_v1, k):

        Color_PO.consoleColor("31", "36", ("[" + str(self.sheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        d = {}
        d['result'] = v[0]
        d['testRuleName'] = l_v1[0]
        d['testRuleParam'] = l_v1[1]
        d['interventionRule'] = v[2]
        d['diseaseRuleCode'] = v[3]
        self._getIdcard(d, k)


    def param2_idcard(self, v, l_v1, k):

        Color_PO.consoleColor("31", "36", ("[" + str(self.sheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        d = {}
        d['result'] = v[0]
        d['testRuleName'] = l_v1[0]
        d['testRuleParam1'] = l_v1[1]
        d['testRuleParam2'] = l_v1[2]
        d['diseaseRuleCode'] = v[2]
        d['interventionRule'] = v[3]

        self._getIdcard(d, k)


    def param1_idcard_hitQty2(self, v, l_v1, k):

        Color_PO.consoleColor("31", "36", ("[" + str(self.sheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        d = {}
        d['result'] = v[0]
        d['testRuleName'] = l_v1[0]
        d['testRuleParam'] = l_v1[1] .replace(".and.", ',')
        d['interventionRule'] = v[2]
        d['diseaseRuleCode'] = v[3]
        d['hitQty'] = v[4]
        self._getIdcard2(d, k)


    def param3_idcard_hitQty2(self, v, l_v1, k):

        Color_PO.consoleColor("31", "36", ("[" + str(self.sheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        d = {}
        d['result'] = v[0]
        d['testRuleName'] = l_v1[0]
        d['testRuleParam1'] = l_v1[1]
        d['testRuleParam2'] = l_v1[2]
        d['testRuleParam3'] = l_v1[3] .replace(".and.", ',')
        d['interventionRule'] = v[2]
        d['diseaseRuleCode'] = v[3]
        d['hitQty'] = v[4]
        self._getIdcard2(d, k)




    def rule(self, d):

        '''
        执行r规则
        :param d:
        :return:
        '''
        # print(d)  # {'result': None, 'testRuleName': 'r2', 'testRuleParam1': "'E11'", 'testRuleParam2': "'1'", 'ruleCode': 'GY_YH002001', 'diseaseRuleCode': 'YH_JB002', 'varIdcard': '310101202308070002'}

        log = ""
        varQTY = 0
        varQ2 = 0

        # 1，遍历所有列得到列值
        l_all = self.Openpyxl_PO.getAllCol("sql")
        i_startAssessStatus = 0
        for i in range(len(l_all)):
            if d['testRuleName'] == l_all[i][0]:
                for j in range(1, len(l_all[i])):
                    command = l_all[i][j]
                    if command != None:

                        if 'varIdcard' in d:
                            command = str(command).replace("{身份证}", d['varIdcard'])
                        if 'testRuleParam1' in d:
                            command = str(command).replace("{测试规则参数1}", d['testRuleParam1'])
                        if 'testRuleParam2' in d:
                            command = str(command).replace("{测试规则参数2}", d['testRuleParam2'])
                        if 'testRuleParam3' in d:
                            command = str(command).replace("{测试规则参数3}", d['testRuleParam3'])
                        if 'testRuleParam4' in d:
                            command = str(command).replace("{测试规则参数4}", d['testRuleParam4'])
                        if 'testRuleParam' in d:
                            command = str(command).replace("{测试规则参数}", d['testRuleParam'])
                        if 'interventionRule' in d:
                            command = str(command).replace("{规则编码}", d['interventionRule'])
                        if "{随机数}" in command:
                            command = str(command).replace("{随机数}", Data_PO.getPhone())

                        varID = self.Openpyxl_PO.getCell(21, 1, "sql")
                        # print("varID=" + str(varID))
                        varIdcard = self.Openpyxl_PO.getCell(22, 1, "sql")
                        varQTY = self.Openpyxl_PO.getCell(23, 1, "sql")
                        varRunRule = self.Openpyxl_PO.getCell(24, 1, "sql")
                        varNewAssess = self.Openpyxl_PO.getCell(25, 1, "sql")
                        varGUID = self.Openpyxl_PO.getCell(26, 1, "sql")
                        # print("varGUID=" + str(varGUID))
                        varQ2 = self.Openpyxl_PO.getCell(27, 1, "sql")

                        if varID != None:
                            if "varID=" in varID:
                                varID = varID.split("varID=")[1].split(")")[0]
                                command = str(command).replace("{varID}", varID)
                        if varIdcard != None:
                            if "varIdcard" in varIdcard:
                                varIdcard = varIdcard.split("varIdcard=")[1].split(")")[0]
                                command = str(command).replace("{varIdcard}", varIdcard)
                        if varQTY != None:
                            if "varQTY" in varQTY:
                                varQTY = varQTY.split("varQTY=")[1].split(")")[0]
                        if varGUID != None:
                            if "varGUID" in varGUID:
                                varGUID = varGUID.split("varGUID=")[1].split(")")[0]
                                command = str(command).replace("{varGUID}", varGUID)

                        if varRunRule != None and varRunRule != "":
                            # print(type(varRunRule))
                            # varRunRule = varRunRule.split("varRunRule=")[1].split(")")[0]
                            log = log + "\n" + varRunRule
                        if varNewAssess != None and varNewAssess != "":
                            # print(type(varNewAssess))
                            # varNewAssess = varNewAssess.split("varNewAssess=")[1].split(")")[0]
                            log = log + "\n" + varNewAssess

                        # 步骤日志
                        # log = log + "\n" + str(j + 1) + ", " + command

                        if "hitQty" in d:
                            if d['hitQty'] == 2:

                                if '{疾病评估规则编码}' in command:
                                    command = str(command).replace("{疾病评估规则编码}", d['diseaseRuleCode'])
                                    a = self.sql(command)
                                    sleep(1)

                                    if "Q2" in a[0]:
                                        varQ2 = a[0]['Q2']
                                        self.Openpyxl_PO.setCellValue(27, 1, "varQ2=" + str(varQ2), "sql")
                                    Color_PO.consoleColor("31", "33", str(j + 1) + ", " + command, "")
                                    log = log + "\n" + str(j + 1) + ", " + command  # 步骤日志
                                    print(a[0])
                                    log = log + "\n" + str(a[0])  # 步骤日志
                                else:
                                    a = self.sql(command)
                                    sleep(1)
                                    Color_PO.consoleColor("31", "33", str(j + 1) + ", " + command, "")
                                    log = log + "\n" + str(j + 1) + ", " + command  # 步骤日志
                            else:
                                if '{疾病评估规则编码}' not in command:
                                    Color_PO.consoleColor("31", "33", str(j + 1) + ", " + command, "")
                                    log = log + "\n" + str(j + 1) + ", " + command  # 步骤日志
                                varQ2 = 0
                                a = self.sql(command)
                                sleep(1)
                        else:
                            varQ2 = 0
                            # print(command)
                            if '{疾病评估规则编码}' not in command:
                                Color_PO.consoleColor("31", "33", str(j + 1) + ", " + command, "")
                                log = log + "\n" + str(j + 1) + ", " + command  # 步骤日志
                                if "{" in command and "}" in command :
                                    varName = command.split("{")[1].split("}")[0]
                                    Color_PO.consoleColor("31", "31", "[ERROR => rule() => sql中 {" + varName + "} 没有转义!]", "")
                                else:
                                    a = self.sql(command)
                                    sleep(1)
                            else:
                                break


                        if a != None:
                            if isinstance(a, list) and a != []:
                                if isinstance(a[0], dict):
                                    # print(a[0])

                                    if "ID" in a[0]:
                                        varID = a[0]['ID']
                                        self.Openpyxl_PO.setCellValue(21, 1, "varID=" + str(varID), "sql")
                                    if "ID_CARD" in a[0]:
                                        varIdcard = a[0]['ID_CARD']
                                        self.Openpyxl_PO.setCellValue(22, 1, "varIdcard=" + str(varIdcard), "sql")
                                    if "QTY" in a[0]:
                                        # print(a[0])
                                        log = log + "\n" + str(a[0])  # 步骤日志
                                        varQTY = a[0]['QTY']
                                        self.Openpyxl_PO.setCellValue(23, 1, "varQTY=" + str(varQTY), "sql")
                                    if "GUID" in a[0]:
                                        varGUID = a[0]['GUID']
                                        self.Openpyxl_PO.setCellValue(26, 1, "varGUID=" + str(varGUID), "sql")
                                    if "name" in a[0]:
                                        self.Openpyxl_PO.setCellValue(24, 1, "", "sql")
                                        self.Openpyxl_PO.setCellValue(25, 1, "", "sql")
                                        if "跑规则" == a[0]['name']:
                                            if a[0]['value'] != 200 :
                                                self.Openpyxl_PO.setCellValue(24, 1, str(a[0]['value']), "sql")
                                        if "新增评估" == a[0]['name']:
                                            if a[0]['value'] != 200 :
                                                self.Openpyxl_PO.setCellValue(25, 1, str(a[0]['value']), "sql")

                    else:
                        break
        self.Openpyxl_PO.setCellValue(21, 1, "", "sql")
        self.Openpyxl_PO.setCellValue(22, 1, "", "sql")
        self.Openpyxl_PO.setCellValue(23, 1, "", "sql")
        self.Openpyxl_PO.setCellValue(24, 1, "", "sql")
        self.Openpyxl_PO.setCellValue(25, 1, "", "sql")
        self.Openpyxl_PO.setCellValue(26, 1, "", "sql")
        self.Openpyxl_PO.setCellValue(27, 1, "", "sql")

        varQTY = int(varQTY) + int(varQ2)
        return varQTY, log

    def gw(self, d):

        '''
        执行gw规则
        :param d:
        :return:
        '''
        # print(d)  # {'result': None, 'diseaseRuleCode': 'GW_JB009', 'ruleCode': "('GW_JB009','PG_JWS026','PG_JWS027','PG_JWS028','PG_JWS031','PG_JWS032')", 'varIdcard': '410101202308070009'}

        d_all = {}
        log = ""
        varQTY = ""
        i_startAssessStatus = 0

        # 1，遍历所有列获取值
        l_all = self.Openpyxl_PO.getAllCol("gwSql")
        for i in range(len(l_all)):
            if d['diseaseRuleCode'] == l_all[i][0]:
                for j in range(1, len(l_all[i])):
                    command = l_all[i][j]
                    if command != None:

                        # 调试
                        # if command == "exit":
                        #     Openpyxl_PO.setCellValue(21, 1, "", "testRule")
                        #     Openpyxl_PO.setCellValue(22, 1, "", "testRule")
                        #     Openpyxl_PO.setCellValue(23, 1, "", "testRule")
                        #     Openpyxl_PO.setCellValue(24, 1, "", "testRule")
                        #     Openpyxl_PO.setCellValue(25, 1, "", "testRule")
                        #     Openpyxl_PO.setCellValue(26, 1, "", "testRule")
                        #     Openpyxl_PO.setCellValue(27, 1, "", "testRule")
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
                            log = log + "\n" + varRunRule
                        if varNewAssess != None and varNewAssess != "":
                            # print(type(varNewAssess))
                            # varNewAssess = varNewAssess.split("varNewAssess=")[1].split(")")[0]
                            log = log + "\n" + varNewAssess
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
                        log = log + "\n" + str(j+1) + ", " + command  # 步骤日志
                        # a = eval(command)
                        a = self.sql(command)
                        sleep(1)

                        if a != None:
                            if isinstance(a, list):
                                if isinstance(a[0], dict):
                                    print(a[0])

                                    if "ID" in a[0]:
                                        varID = a[0]['ID']
                                        self.Openpyxl_PO.setCellValue(21, 1, "varID=" + str(varID), "sql")
                                    if "ID_CARD" in a[0]:
                                        varIdcard = a[0]['ID_CARD']
                                        self.Openpyxl_PO.setCellValue(22, 1, "varIdcard=" + str(varIdcard), "sql")
                                    if "QTY" in a[0]:
                                        varQTY = a[0]['QTY']
                                        self.Openpyxl_PO.setCellValue(23, 1, "varQTY=" + str(varQTY), "sql")
                                    if "GUID" in a[0]:
                                        varGUID = a[0]['GUID']
                                        self.Openpyxl_PO.setCellValue(26, 1, "varGUID=" + str(varGUID), "sql")
                                    if "QTY0" in a[0]:
                                        varQTY0 = a[0]['QTY0']
                                        d_all['QTY0'] = str(a[0]['QTY0'])
                                        # print(varQTY0)
                                        # Openpyxl_PO.setCellValue(27, 1, "varQTY0=" + str(varQTY0), "sql")
                                    if "name" in a[0]:
                                        self.Openpyxl_PO.setCellValue(24, 1, "", "sql")
                                        self.Openpyxl_PO.setCellValue(25, 1, "", "sql")
                                        if "跑规则" == a[0]['name']:
                                            if a[0]['value'] != 200:
                                                self.Openpyxl_PO.setCellValue(24, 1, str(a[0]['value']), "sql")
                                        if "新增评估" == a[0]['name']:
                                            if a[0]['value'] != 200:
                                                self.Openpyxl_PO.setCellValue(25, 1, str(a[0]['value']), "sql")

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
                            #         Openpyxl_PO.setCellValue(24, 1, "varRunRule=" + str(varRunRule), "sql")
                            #     if "新增评估" in a[0]:
                            #         varNewAssess = a[1]
                            #         Openpyxl_PO.setCellValue(25, 1, "varNewAssess=" + str(varNewAssess), "sql")
                    else:
                        break
        self.Openpyxl_PO.setCellValue(21, 1, "", "sql")
        self.Openpyxl_PO.setCellValue(22, 1, "", "sql")
        self.Openpyxl_PO.setCellValue(23, 1, "", "sql")
        self.Openpyxl_PO.setCellValue(24, 1, "", "sql")
        self.Openpyxl_PO.setCellValue(25, 1, "", "sql")
        self.Openpyxl_PO.setCellValue(26, 1, "", "sql")
        self.Openpyxl_PO.setCellValue(27, 1, "", "sql")

        log = log + "\n" + str(d_all)
        return d_all, log
