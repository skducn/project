# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-1
# Description: 社区健康管理中心 - 规则自动化脚本
# http://192.168.0.243:8012/swagger-ui/index.html#/%E7%99%BB%E5%BD%95%E6%A8%A1%E5%9D%97/loginUsingPOST
# http://192.168.0.223:8848/nacos/#/serviceDetail?name=chc-auth&groupName=DEFAULT_GROUP
# 1，获取规则内容 《健康评估规则表》
# 2，执行规则
# 3，更新结果
#***************************************************************

import subprocess, json
from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "utf8")  # 测试环境

from PO.OpenpyxlPO import *

from ChcRulePO import *
ChcRule_PO = ChcRulePO()

# # # 1,获取登录用户的token
# token = ChcRule_PO.getToken("ww", "Zy@123456")
# print(token)

#
# # 2, 获取表格规则
# # Sys_PO.closeApp("EXCEL.EXE")
# Openpyxl_PO = OpenpyxlPO("test.xlsx")
Openpyxl_PO = OpenpyxlPO("健康评估规则表.xlsx")
# Openpyxl_PO.openSheet(Sheet="hello")
print(Openpyxl_PO.getRowCol("健康评估规则库"))

# # 3， 跑规则
# ChcRule_PO.runRule("24", token)
#
#
# # 4, 校验评估规则结果表
# result = (ChcRule_PO.getResult(45, "PG_AGE002"))
# # 如果1，成功，更新表格规则结果位成功。否则失败。
