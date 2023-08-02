# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-1
# Description: 社区健康管理中心 - 规则自动化脚本
# http://192.168.0.243:8012/swagger-ui/index.html#/%E7%99%BB%E5%BD%95%E6%A8%A1%E5%9D%97/loginUsingPOST
# http://192.168.0.223:8848/nacos/#/serviceDetail?name=chc-auth&groupName=DEFAULT_GROUP
# http://192.168.0.243:8011/doc.html#/chc-auth/%E7%99%BB%E5%BD%95%E6%A8%A1%E5%9D%97/loginUsingPOST
# 1，获取规则内容 《健康评估规则表》
# 2，执行规则
# 3，更新结果
#***************************************************************

from PO.OpenpyxlPO import *
from ChcRulePO import *
ChcRule_PO = ChcRulePO()


# # # 1,获取登录用户的token
# token = ChcRule_PO.getToken("ww", "Zy@123456")
# print(token)

#
# # 2, 获取表格规则
# ChcRule_PO.clsApp("Microsoft Excel")
Openpyxl_PO = OpenpyxlPO("健康评估规则表.xlsx")
# print(Openpyxl_PO.getRowCol("健康评估规则库"))
rowCol = (Openpyxl_PO.getRowCol("健康评估规则库"))
# print(rowCol[0])
actualRow = rowCol[0] - 1
# print(Openpyxl_PO.getColValueByCol([2, 5], [1], "健康评估规则库"))  # 获取第二列（规则名称）和第五列（评估规则编码）的值，忽略第一行数据
l_ruleName_ruleCode = (Openpyxl_PO.getColValueByCol([2, 5], [1], "健康评估规则库"))  # 获取第二列（规则名称）和第五列（评估规则编码）的值，忽略第一行数据


for i in range(1, rowCol[0]):
    # print(l_ruleName_ruleCode[0][i+1], l_ruleName_ruleCode[1][i+1])

    # # 3， 跑规则
    # ChcRule_PO.runRule("24", token)


    # # 4, 校验评估规则结果表
    result = (ChcRule_PO.getResult(45, l_ruleName_ruleCode[1][i-1]))
    # print(l_ruleName_ruleCode[1][i-1])
    if result == 1:
        Openpyxl_PO.setCellValue(i+1, 7, "ok", "健康评估规则库")
    else:
        Openpyxl_PO.setCellValue(i+1, 7, "error", "健康评估规则库")
    Openpyxl_PO.setCellValue(1, 7, "自动化测试结果", "健康评估规则库")

    # break

Openpyxl_PO.open()

