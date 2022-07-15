# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-6-30
# Description: erp - 统计报表 - expain SQL语句的执行计划
#***************************************************************

from PO.StrPO import *
Str_PO = StrPO()
from PO.TimePO import *
Time_PO = TimePO()
from PO.DataPO import *
Data_PO = DataPO()

from PO.MysqlPO import *
iUrl = "http://192.168.0.245:8080"
db_ip = "192.168.0.244"
db_database = "crm"
db_username = "root"
db_password = "ZAQ!2wsx"
db_port = 3306
Mysql_PO = MysqlPO(db_ip, db_username, db_password, db_database, db_port)

from PO.OpenpyxlPO import *
Sys_PO.killPid('EXCEL.EXE')
Openpyxl_PO = OpenpyxlPO("i_erp_reportField_case.xlsx")

def explain(varSheet):
    tbl_sql = Openpyxl_PO.getColValueByCol([4], [], varSheet)
    Openpyxl_PO.setCellValue(1, 4, "sql(2022-06-01~2022-06-30 23:59:59)", varSheet)
    for i in range(len(tbl_sql[0])):
        if tbl_sql[0][i] != None and "select " in tbl_sql[0][i]:
            if Str_PO.getRepeatCount(tbl_sql[0][i], "%s") == 1:
                sql = tbl_sql[0][i] % (84)
            elif Str_PO.getRepeatCount(tbl_sql[0][i], "%s") == 3:
                sql = tbl_sql[0][i] % (84, "2022-06-01", "2022-06-30 23:59:59")
            execExplain = 'explain ' + sql
            # print(execExplain)
            db_result = Mysql_PO.execQuery(execExplain)
            # print("(id, selecrt_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra)")
            for j in range(len(db_result)):
                Openpyxl_PO.setCellValue(i + 1, j + 5, str(db_result[j]), varSheet)
                Openpyxl_PO.setCellValue(1, j + 5, "explain" + str(j+1), varSheet)


explain("拜访分析报表")
explain("协访分析")

Openpyxl_PO.open()