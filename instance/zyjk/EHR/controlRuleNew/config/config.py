# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-6-9
# Description: 电子健康档案 - 质控配置文件
# *****************************************************************

from PO.LogPO import *
from PO.NetPO import *
from PO.DataPO import *
from PO.ColorPO import *
from PO.ExcelPO.ExcelPO import *
from PO.TimePO import *
Time_PO = TimePO()

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.35", "test", "123456", "data_center_test1")  # 测试环境

varExcel = "cr1.2.xlsx"
varExcelSheet = "controlRule"
varCurl = 'curl http://localhost:8080/healthRecordRules/rulesApi/execute/31011310200312009116'
varJar = 'healthRecordRules.jar'
varRuleType = ""     # 默认为空，执行所有规则类型，其他可选：规范性，完整性，一致性，有效性，追溯性 ，表示执行某一规则类型 。
varIsRun = ""     # 默认为空，执行所有用例，其他可选：error，ok，表示只执行比对结果是error或ok的用例。

# 日志文件
logFile = './log/controlRul_' + Time_PO.getDate() + '.log'



