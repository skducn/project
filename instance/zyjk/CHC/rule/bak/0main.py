# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-1
# Description: 社区健康管理中心 - 规则自动化脚本
# http://192.168.0.243:8012/swagger-ui/index.html#/%E7%99%BB%E5%BD%95%E6%A8%A1%E5%9D%97/loginUsingPOST
# http://192.168.0.243:8010/login#/login  登录页面
# 1，获取规则内容 《健康评估规则表》
# 2，执行规则
# 3，更新结果
#***************************************************************
import sys

from PO.OpenpyxlPO import *
from ChcRulePO_old import *
ChcRule_PO = ChcRulePO()


# 新增患者主索引
# ChcRule_PO.insertEMPI("INSERT INTO TB_EMPI_INDEX_ROOT(GUID, NAME, SEXCODE, SEXVALUE, DATEOFBIRTH, IDCARDNO, NATIONCODE, NATIONVALUE, PHONENUM) VALUES ('cs1005', N'测试干预1', '2', '女', '1992-12-01', '653101195005199966', NULL, NULL, '6567917733')")


# 1,获取登录用户的token
TOKEN = ChcRule_PO.getToken("jh", "12345678")  #
# TOKEN = ChcRule_PO.getToken("ww", "Zy@123456")  # 汪刚
# TOKEN = ChcRule_PO.getToken("www", "Ww123456")   # 刘斌龙

ChcRule_PO.clsApp("Microsoft Excel")
Openpyxl_PO = OpenpyxlPO("健康评估规则表自动化3.xlsx")


# todo 健康评估
# ChcRule_PO.run('健康评估', None, "r1", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康评估', "OK", "r6", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康评估', "ERROR", "r1", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康评估', None, None, Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康评估', "OK", None, Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康评估', "ERROR", None, Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康评估', "ALL", "r3", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康评估', "ALL", None, Openpyxl_PO, TOKEN)

# todo 健康干预
# ChcRule_PO.run('健康干预', None, "GW", Openpyxl_PO, TOKEN) # 执行测试结果为空的r8用例
# ChcRule_PO.run('健康干预', None, "r2", Openpyxl_PO, TOKEN)  # 执行测试结果为空的r8用例
# ChcRule_PO.run('健康干预', "ERROR", "r11", Openpyxl_PO, TOKEN)  # 执行测试结果为ERROR的r11用例
# ChcRule_PO.run('健康干预', "OK", "r11", Openpyxl_PO, TOKEN) # 执行测试结果为OK的r11用例
# ChcRule_PO.run('健康干预', None, None, Openpyxl_PO, TOKEN)  # 执行测试结果为空的所有用例
# ChcRule_PO.run('健康干预', "ERROR", None, Openpyxl_PO, TOKEN)  # 执行测试结果为ERROR的所有用例
# ChcRule_PO.run('健康干预', "OK", None, Openpyxl_PO, TOKEN)  # 执行测试结果为OK的所有用例
# ChcRule_PO.run('健康干预', "ALL", "r2", Openpyxl_PO, TOKEN)  # 执行测试结果为OK的所有用例
# ChcRule_PO.run('健康干预', "ALL", None, Openpyxl_PO, TOKEN)  # 执行测试结果为OK的所有用例


# todo 疾病评估规则（已患和高风险）
ChcRule_PO.run('疾病评估规则（已患和高风险）', None, "GW", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('疾病评估规则（已患和高风险）', "ERROR", "GW", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('疾病评估规则（已患和高风险）', "OK", "GW", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('疾病评估规则（已患和高风险）', None, "r9", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('疾病评估规则（已患和高风险）', 'ERROR', "r9", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('疾病评估规则（已患和高风险）', 'OK', "r9", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('疾病评估规则（已患和高风险）', 'ALL', "r9", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('疾病评估规则（已患和高风险）', 'ALL', None, Openpyxl_PO, TOKEN)


# todo 健康干预_中医体质辨识
# ChcRule_PO.run('健康干预_中医体质辨识', "OK", "r12", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康干预_中医体质辨识', "ERROR", "r12", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康干预_中医体质辨识', None, "r12", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康干预_中医体质辨识', "ALL", "r12", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康干预_中医体质辨识', "ALL", None, Openpyxl_PO, TOKEN)


Openpyxl_PO.open()

