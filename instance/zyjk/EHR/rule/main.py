# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-2-21
# Description: 电子健康档案质控规则自动化
#***************************************************************
# 警告如下：D:\dwp_backup\python study\GUI_wxpython\lib\site-packages\openpyxl\worksheet\_reader.py:312: UserWarning: Unknown extension is not supported and will be removed warn(msg)
# 解决方法：
import warnings
warnings.simplefilter("ignore")
# *****************************************************************
from PO.ColorPO import *
Color_PO = ColorPO()

import subprocess,json
from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "EHRDC")  # 测试环境
# a = Sqlserver_PO.select('select * from tb_dc_first_prenatal_visit')
# print(a)
# sys.exit(0)

def importDb(varFile, varTable, varSheet):
    Sqlserver_PO.xlsx2db(varFile, varTable, varSheet)
    Sqlserver_PO.execute("ALTER table %s alter column pResult varchar(111)" % (varTable))
    Sqlserver_PO.execute("ALTER table %s alter column nResult varchar(111)" % (varTable))

    Sqlserver_PO.execute("ALTER table %s alter column QC_type varchar(111)" % (varTable))
    Sqlserver_PO.execute("ALTER table %s alter column QC_tn varchar(111)" % (varTable))
    Sqlserver_PO.execute("ALTER table %s alter column QC_field varchar(111)" % (varTable))
    Sqlserver_PO.execute("ALTER table %s alter column QC_rule varchar(333)" % (varTable))
    Sqlserver_PO.execute("ALTER table %s alter column QC_desc varchar(111)" % (varTable))
    Sqlserver_PO.execute("ALTER table %s alter column QC_ruleID varchar(111)" % (varTable))

    Sqlserver_PO.execute("ALTER table %s alter column runQC varchar(111)" % (varTable))
    Sqlserver_PO.execute("ALTER table %s alter column pCase varchar(111)" % (varTable))
    Sqlserver_PO.execute("ALTER table %s alter column pCheck varchar(333)" % (varTable))
    Sqlserver_PO.execute("ALTER table %s alter column nCase varchar(111)" % (varTable))
    Sqlserver_PO.execute("ALTER table %s alter column nCheck varchar(333)" % (varTable))
    Sqlserver_PO.execute("ALTER table %s alter column tester varchar(20)" % (varTable))
    Sqlserver_PO.execute("EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % ('自动化质控规则表', varTable))  # sheetName=注释
def main(varTable, varRun='all'):

    if varRun != 'all':
        l_d_row = Sqlserver_PO.select("select * from %s where pResult != 'ok' or nResult != 'ok'" % (varTable))
        print("l_d_row => ", l_d_row)

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

        else:
            # print("[error], 执行档案编号对单个档案执行质控 失败！" + status)
            Color_PO.consoleColor("31", "31", str(i+1) + "[ERROR], ", "执行档案编号对单个档案执行质控 失败！" + status)



varTable ='A_testrule'

# # # # # todo 1, 初始化表（删除表）
# Sqlserver_PO.execute("drop table " + varTable)
#
# # todo 2, 导入数据
# importDb('rule.xlsx', varTable, 'rule')

main(varTable, 'error')









