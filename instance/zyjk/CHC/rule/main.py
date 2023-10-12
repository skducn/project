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

# r.run(None, None)
# r.run("ERROR", None)
# r.run("OK", None)
# r.run("ALL", None)
# r.run(None, "r1")
# r.run("ERROR", "r1")
# r.run("OK", "r1")
# r.run("ALL", "r1")
#***************************************************************


from ChcRulePO import *
# ChcRule_PO = ChcRulePO()
# 新增患者主索引
# ChcRule_PO.insertEMPI("INSERT INTO TB_EMPI_INDEX_ROOT(GUID, NAME, SEXCODE, SEXVALUE, DATEOFBIRTH, IDCARDNO, NATIONCODE, NATIONVALUE, PHONENUM) VALUES ('cs1005', N'测试干预1', '2', '女', '1992-12-01', '653101195005199966', NULL, NULL, '6567917733')")



# r = ChcRulePO({"sheetName": "健康评估", "colTitle": ["测试结果", "测试规则", "评估规则编码"]})
# r.run("ERROR", None)

r = ChcRulePO({"sheetName": "健康干预", "colTitle": ["测试结果", "测试规则", "疾病评估规则编码", "干预规则编码", "命中次数"]})
r.run("ERROR", "GW")
# r.run(None, None)

# r = ChcRulePO({"sheetName": "健康干预中医体质辨识", "colTitle": ["测试结果", "测试规则", "干预规则编码", "干预规则"]})
# r.run("ERROR", None)

# r = ChcRulePO({"sheetName": "儿童健康干预", "colTitle": ["测试结果", "测试规则", "干预规则编码"]})
# r.run(None, None)

# r = ChcRulePO({"sheetName": "已患和高风险疾病评估", "colTitle": ["测试结果", "测试规则", "疾病评估规则编码", "健康评估规则库编码"]})
# r.run(None, "GW")
# r.run(None, None)
# # r.run("OK", None)

r.open()
