# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-2-21
# Description: EHR 质控规则自动化
# 【腾讯文档】EHR质控规则自动化
# https://docs.qq.com/sheet/DYm93RkZ3bENGSHd4?tab=BB08J2
#***************************************************************
# 警告如下：D:\dwp_backup\python study\GUI_wxpython\lib\site-packages\openpyxl\worksheet\_reader.py:312: UserWarning: Unknown extension is not supported and will be removed warn(msg)
# 解决方法：
import sys
import warnings
warnings.simplefilter("ignore")
# *****************************************************************
# 要切换到 $ cd /Users/linghuchong/Downloads/51/Python/project/instance/zyjk/EHR/rule 下执行 python main.py
sys.path.append("../../../../")
# sys.path.append("/Users/linghuchong/Downloads/51/Python/project")


import subprocess, json

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB_SQL("host"), Configparser_PO.DB_SQL("user"), Configparser_PO.DB_SQL("password"), Configparser_PO.DB_SQL("database"))  # 测试环境

class Ehr_rule_PO():


    def excel2db(self, varFile, varTable, varSheet=0):

        # 文件导入db
        # 1, db中删除表
        Sqlserver_PO.execute("drop table if exists " + varTable)

        # 2, excel导入db
        Sqlserver_PO.xlsx2db(varFile, varTable, varSheet)

        # 3, 设置表注释
        Sqlserver_PO.setTableComment(varTable, '(测试用例)erh质控规则表')

        # 4, 设置字段类型与描述
        Sqlserver_PO.setFieldTypeComment(varTable, 'updateDate', 'varchar(999)', '正向测试结果')
        Sqlserver_PO.setFieldTypeComment(varTable, 'pResult', 'varchar(100)', '正向测试结果')
        Sqlserver_PO.setFieldTypeComment(varTable, 'nResult', 'varchar(100)', '反向测试结果')
        Sqlserver_PO.setFieldTypeComment(varTable, 'QC_type', 'varchar(100)', '质控类型')
        Sqlserver_PO.setFieldTypeComment(varTable, 'QC_tn', 'varchar(100)', '质控表')
        Sqlserver_PO.setFieldTypeComment(varTable, 'QC_field', 'varchar(100)', '质控字段')
        Sqlserver_PO.setFieldTypeComment(varTable, 'QC_rule', 'varchar(300)', '质控规则')
        Sqlserver_PO.setFieldTypeComment(varTable, 'QC_desc', 'varchar(100)', '质控错误描述')
        Sqlserver_PO.setFieldTypeComment(varTable, 'QC_ruleID', 'varchar(100)', '质控规则ID')
        Sqlserver_PO.setFieldTypeComment(varTable, 'runQC', 'varchar(100)', '执行质控')
        Sqlserver_PO.setFieldTypeComment(varTable, 'pCase', 'varchar(300)', '正向用例')
        Sqlserver_PO.setFieldTypeComment(varTable, 'pCheck', 'varchar(300)', '正向检查')
        Sqlserver_PO.setFieldTypeComment(varTable, 'nCase', 'varchar(300)', '正向用例')
        Sqlserver_PO.setFieldTypeComment(varTable, 'nCheck', 'varchar(300)', '反向检查')
        Sqlserver_PO.setFieldTypeComment(varTable, 'tester', 'varchar(100)', '测试者')

        # 5, 设置自增主键
        Sqlserver_PO.setIdentityPrimaryKey(varTable, "ID")

    def main(self, varTable, varRun='all'):

        if varRun != 'all':
            l_d_row = Sqlserver_PO.select("select * from %s where pResult != 'ok' or nResult != 'ok'" % (varTable))
            # print("l_d_row => ", l_d_row)

        else:
            l_d_row = Sqlserver_PO.select("select * from %s" % (varTable))
            # print("l_d_row => ", l_d_row)  # [{'s_value': None, 'o_value': None, 's_field': None, 'o_field': None, 's_comment': None, 'o_comment': None, 's_type': None, 'o_type': None, 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'y', 'tester': '郭斐', 's_sql': "SELECT * FROM T_CHILD_INFO where id='1189'", 'o_sql': "SELECT * FROM DIP.TB_EB_ETJBQK where ETBSFID='1189'"}, {'s_value': '1189', 'o_value': '1189', 's_field': 'ID', 'o_field': 'ETBSFID', 's_comment': '主键', 'o_comment': 'None', 's_type': 'int', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '111', 'o_value': '111', 's_field': 'CREATE_ORG_CODE', 'o_field': 'YLJGDM', 's_comment': '创建机构代码', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '马德勇', 'o_value': '马德勇', 's_field': 'NAME', 'o_field': 'XM', 's_comment': '姓名', 'o_comment': 'None', 's_type': 'nvarchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '1', 'o_value': '1', 's_field': 'SEX_CODE', 'o_field': 'XBDM', 's_comment': '性别代码', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'CHAR', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '220621199012163357', 'o_value': '220621199012163357', 's_field': 'IDCARD', 'o_field': 'ZJHM', 's_comment': '身份证', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '测试', 'o_value': '测试', 's_field': 'MOTHER_NAME', 'o_field': 'MQXM', 's_comment': '母亲姓名', 'o_comment': 'None', 's_type': 'nvarchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '222222222222222222', 'o_value': '222222222222222222', 's_field': 'MOTHER_IDCARD', 'o_field': 'MQSFZ_HM', 's_comment': '母亲身份证号', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '370685001001', 'o_value': '370685001001', 's_field': 'PRESENT_VILLAGE_CODE', 'o_field': 'XZDZ_JWBM', 's_comment': '现住址-居委编码', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '文化区社区居民委员会', 'o_value': '文化区社区居民委员会', 's_field': 'PRESENT_VILLAGE_NAME', 'o_field': 'XZDZ_JW', 's_comment': '现住址-居委', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '2024-01-06 00:00:00', 'o_value': '2024-01-06 00:00:00', 's_field': 'BIRTH', 'o_field': 'CSRQSJ', 's_comment': '出生日期', 'o_comment': 'None', 's_type': 'datetime', 'o_type': 'DATE', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}]

        for i, index in enumerate(l_d_row):

            QC_type = l_d_row[i]['QC_type']
            QC_rule = l_d_row[i]['QC_rule']
            QC_desc = l_d_row[i]['QC_desc']
            QC_ruleID = l_d_row[i]['QC_ruleID']

            idcard = l_d_row[i]['runQC']
            pCase = l_d_row[i]['pCase']
            pCheck = l_d_row[i]['pCheck']
            nCase = l_d_row[i]['nCase']
            nCheck = l_d_row[i]['nCheck']

            def runQC(idcard):

                # 步骤2：根据档案编号对单个档案执行质控
                command = 'curl -X GET "http://192.168.0.243:8090/healthRecordRules/rulesEngine/execute/' + str(idcard) + '" -H "accept: */*"'
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()
                str_r = bytes.decode(out)
                d_r = json.loads(str_r)
                # print(d_r)   # {'code': 200, 'msg': '成功', 'data': None}
                if d_r['code'] == 200:
                    return 1
                return str_r


            # todo 正向
            # 步骤1: 执行用例
            Sqlserver_PO.execute(pCase)

            # 步骤2：根据档案编号对单个档案执行质控
            status = runQC(idcard)  # {'code': 200, 'msg': '成功', 'data': None}

            if status == 1:
                # 步骤3：查询结果
                l_d_r = Sqlserver_PO.select(pCheck)
                # print(l_d_r)

                # 步骤4: 验证结果
                if l_d_r == [] :
                    Sqlserver_PO.execute("update %s set pResult='error' where QC_rule='%s' and QC_ruleID='%s'" % (varTable, QC_rule, QC_ruleID))
                    Color_PO.consoleColor("31", "31", str(i+1) + " [ERROR] => ", "[正向] " + QC_type + ", " + QC_rule + ", " + QC_ruleID + ", 预期值：" + QC_desc + "，返回值：空, 请检查pCase语句！")
                elif l_d_r[0]['Comment'] == QC_desc:
                    Sqlserver_PO.execute("update %s set pResult='ok' where QC_rule='%s' and QC_ruleID='%s'" % (varTable, QC_rule, QC_ruleID))
                    # print("[正向 ok], " + QC_rule + ", " + QC_ruleID)
                    print(str(i+1))
                else:
                    Sqlserver_PO.execute("update %s set pResult='error' where QC_rule='%s' and QC_ruleID='%s'" % (varTable, QC_rule, QC_ruleID))
                    Color_PO.consoleColor("31", "31", str(i + 1) + " [ERROR] => ", "[正向] " + QC_type + ", " + QC_rule + ", " + QC_ruleID + ", 预期值：" + QC_desc + "，返回值：空, 请检查pCase语句！")
                    print(str(i + 1))
                Sqlserver_PO.execute("update %s set updateDate='%s' where QC_ruleID='%s'" % (varTable, Time_PO.getDateTimeByDivide(), QC_ruleID))

            else:
                # print("[error], 执行档案编号对单个档案执行质控 失败！" + status)
                Color_PO.consoleColor("31", "31", str(i+1) + "[ERROR], ", "执行档案编号对单个档案执行质控 失败！" + status)

            # todo 反向
            # 步骤1: 执行用例
            Sqlserver_PO.execute(nCase)

            # 步骤2：根据档案编号对单个档案执行质控
            runQC(idcard)

            if status == 1:
                # 步骤3：查询结果
                l_d_r = Sqlserver_PO.select(nCheck)

                # 步骤4: 验证结果
                if l_d_r == []:
                    Sqlserver_PO.execute("update %s set nResult='ok' where QC_desc='%s' and QC_ruleID='%s'" % (varTable, QC_desc, QC_ruleID))
                    # print("[反向 ok], " + QC_rule + ", " + QC_ruleID)
                    # print(str(i + 1))
                else:
                    Sqlserver_PO.execute("update %s set nResult='error' where QC_desc='%s' and QC_ruleID='%s'" % (varTable, QC_desc, QC_ruleID))
                    Color_PO.consoleColor("31", "31", str(i+1) + " [ERROR] => ", "[反向] " + QC_type + ", " + QC_rule + ", " + QC_ruleID + ", 预期值：" + QC_desc + "，返回值：空, 请检查nCase语句！")
                    # Color_PO.consoleColor("31", "31", "[ERROR], ", "[反向], " + QC_rule + ", " + QC_ruleID)
                Sqlserver_PO.execute("update %s set updateDate='%s' where QC_ruleID='%s'" % (varTable, Time_PO.getDateTimeByDivide(), QC_ruleID))

            else:
                # print("[error], 执行档案编号对单个档案执行质控 失败！" + status)
                Color_PO.consoleColor("31", "31", str(i+1) + "[ERROR], ", "执行档案编号对单个档案执行质控 失败！" + status)


    def db2html(self):

        # db导出html

        # 导出所有值
        Sqlserver_PO.db2html("select ID, updateDate as 更新时间, pResult as 正向结果, nResult as 反向结果, QC_type as 类型, QC_field as 质控字段, QC_rule as 质控规则, QC_desc as 错我描述, pCase as 正向用例, nCase as 反向用例, pCheck as 正向校验 from %s" % (Configparser_PO.DB_SQL("table")), Configparser_PO.FILE("html"))

        # 导出错误记录
        # Sqlserver_PO.db2html("select ID, updateDate as 更新时间, pResult as 正向结果, nResult as 反向结果, QC_type as 类型, QC_field as 质控字段, QC_rule as 质控规则, QC_desc as 错我描述, pCase as 正向用例, nCase as 反向用例, pCheck as 正向校验 from %s where pResult='error' or nResult='error'" % (Configparser_PO.DB_SQL("table")), Configparser_PO.FILE("html"))






