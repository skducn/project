# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-1
# Description: 社区健康管理中心 - 规则自动化脚本
# 健康档案接口文档 http://192.168.0.243:8014/doc.html
# Swagger http://192.168.0.243:8012/swagger-ui/index.html#/%E7%99%BB%E5%BD%95%E6%A8%A1%E5%9D%97/loginUsingPOST
# nacos  http://192.168.0.223:8848/nacos/#/serviceDetail?name=chc-auth&groupName=DEFAULT_GROUP
# http://192.168.0.243:8010/login#/login  登录页面
# 1，获取规则内容 《健康评估规则表》
# 2，执行规则
# 3，更新结果
# 【腾讯文档】健康评估规则表自动化
# https://docs.qq.com/sheet/DYkZUY0ZNaHRPdkRk?tab=sf3rdj
# open /Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CHC/rule/健康评估规则表自动化1.xlsx
#***************************************************************


from ChcRulePO import *
# ChcRule_PO = ChcRulePO()
# 新增患者主索引
# ChcRule_PO.insertEMPI("INSERT INTO TB_EMPI_INDEX_ROOT(GUID, NAME, SEXCODE, SEXVALUE, DATEOFBIRTH, IDCARDNO, NATIONCODE, NATIONVALUE, PHONENUM) VALUES ('cs1005', N'测试干预1', '2', '女', '1992-12-01', '653101195005199966', NULL, NULL, '6567917733')")



# todo 健康评估(testRule)
# healthValuation = ChcRulePO({"sheetName": "健康评估", "colTitle": ["测试结果", "测试规则", "评估规则编码"]})
# # # healthValuation.run(None, None)
# healthValuation.run("ERROR", None)
# healthValuation.run("OK", None)
# healthValuation.run("ALL", None)
# healthValuation.run(None, "r1")
# healthValuation.run("ERROR", "r1")
# healthValuation.run("OK", "r1")
# healthValuation.run("ALL", "r1")


# # todo 健康干预(testRule)
# healthInterposal = ChcRulePO({"sheetName": "健康干预", "colTitle": ["测试结果", "测试规则", "干预规则编码", "疾病评估规则编码", "命中次数"]})
# healthInterposal.run(None, None)
# healthInterposal.run("ERROR", None)
# healthInterposal.run("OK", None)
# healthInterposal.run("ALL", None)
# healthInterposal.run(None, "r1")
# healthInterposal.run("ERROR", "r1")
# healthInterposal.run("OK", "r1")
# healthInterposal.run("ALL", "r1")


# todo 健康干预中医体质辨识(testRule)
# zytzbs = ChcRulePO({"sheetName": "健康干预中医体质辨识", "colTitle": ["测试结果", "测试规则", "干预规则编码", "干预规则"]})
# zytzbs.run(None, None)
# zytzbs.run("ERROR", None)
# zytzbs.run("OK", None)
# zytzbs.run("ALL", None)
# zytzbs.run(None, "r12")
# zytzbs.run("ERROR", "r12")
# zytzbs.run("OK", "r12")
# zytzbs.run("ALL", "r12")


# # todo 儿童健康干预(testRule)
# ChildHealthInterposal = ChcRulePO({"sheetName": "儿童健康干预", "colTitle": ["测试结果", "测试规则", "干预规则编码"]})
# ChildHealthInterposal.run(None, None)
# ChildHealthInterposal.run("ERROR", None)
# ChildHealthInterposal.run("OK", None)
# ChildHealthInterposal.run("ALL", None)
# ChildHealthInterposal.run(None, "r1")
# ChildHealthInterposal.run("ERROR", "r1")
# ChildHealthInterposal.run("OK", "r1")
# ChildHealthInterposal.run("ALL", "r1")


# todo 已患和高风险疾病评估(GW)
gwDisease = ChcRulePO({"sheetName": "已患和高风险疾病评估", "colTitle": ["测试结果", "测试规则", "疾病评估规则编码", "健康评估规则库编码"]})
# gwDisease.run(None, "GW")
gwDisease.run("ERROR", "GW")
# # gwDisease.run("OK", None)
# gwDisease.run("ALL", "GW")
# gwDisease.run(None, "r9")
# gwDisease.run("ERROR", "r1")
# gwDisease.run("OK", "r1")
# gwDisease.run("ALL", "r1")

