# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-1
# Description: 社区健康管理中心规则自动化脚本
#【腾讯文档】健康评估规则表自动化 https://docs.qq.com/sheet/DYkZUY0ZNaHRPdkRk?tab=sf3rdj
# 社区健康管理中心登录 http://192.168.0.243:8010/login#/login
# 健康档案接口文档 http://192.168.0.243:8014/doc.html
# Swagger http://192.168.0.243:8012/swagger-ui/index.html#/%E7%99%BB%E5%BD%95%E6%A8%A1%E5%9D%97/loginUsingPOST
# nacos  http://192.168.0.223:8848/nacos/#/serviceDetail?name=chc-auth&groupName=DEFAULT_GROUP
# open /Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CHC/rule/健康评估规则表自动化1.xlsx
#***************************************************************
from ChcRulePO import *
import threading


import time
# t = time.time()
# r = ChcRulePO("健康评估")
# r = ChcRulePO({"sheetName": "健康评估", "colTitle": ["测试结果", "测试规则", "评估规则编码"]})
# r.run(4, None)  # r1
# print(f'耗时:{time.time() - t:.4f}s')
# r.run(4, None)  # r6
# r.run(20, None)  # r4
# r.run(25, None)  # r3
# r.run("ERROR", None)

# r = ChcRulePO({"sheetName": "健康干预", "colTitle": ["测试结果", "测试规则", "疾病评估规则编码", "干预规则编码", "命中次数"]})
# r.run(2, None)  # r2
# r.run(20, None)  # r11, 命中2
# r.run(35, None)  # r5, 命中2
# r.run(44, None)  # r2, 命中2
# r.run(50, None)  # r8
# r.run(87, None)  # r7
# r.run("ERROR", "GW")
# r.run("ERROR", None)

# r = ChcRulePO({"sheetName": "健康干预中医体质辨识", "colTitle": ["测试结果", "测试规则", "干预规则编码", "干预规则"]})
# r.run(2, None)  # r12

# r = ChcRulePO({"sheetName": "儿童健康干预", "colTitle": ["测试结果", "测试规则", "干预规则编码"]})
# r.run(2, None)  # r1
# r.run("ERROR", None)

# r = ChcRulePO({"sheetName": "已患和高风险疾病评估", "colTitle": ["测试结果", "测试规则", "疾病评估规则编码", "健康评估规则库编码"]})
# r.run(2, None)  # r9
# r.run(3, None)  # r10
# r.run("ERROR", "GW")
# r.run(None, "GW")
# r.run("ERROR", None)

# r.open('儿童健康干预')
