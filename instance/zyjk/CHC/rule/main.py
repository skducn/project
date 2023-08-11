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
import sys

from PO.OpenpyxlPO import *
from ChcRulePO import *
ChcRule_PO = ChcRulePO()


# 新增患者主索引
# ChcRule_PO.insertEMPI("INSERT INTO TB_EMPI_INDEX_ROOT(GUID, NAME, SEXCODE, SEXVALUE, DATEOFBIRTH, IDCARDNO, NATIONCODE, NATIONVALUE, PHONENUM) VALUES ('cs1005', N'测试干预1', '2', '女', '1992-12-01', '653101195005199966', NULL, NULL, '6567917733')")


# 1,获取登录用户的token
TOKEN = ChcRule_PO.getToken("ww", "Zy@123456")  # 汪刚
# TOKEN = ChcRule_PO.getToken("www", "Ww123456")   # 刘斌龙

ChcRule_PO.clsApp("Microsoft Excel")
Openpyxl_PO = OpenpyxlPO("健康评估规则表自动化1.xlsx")


# todo 健康评估
# ChcRule_PO.run('健康评估', None, "r1", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康评估', "OK", "r6", Openpyxl_PO, TOKEN)
ChcRule_PO.run('健康评估', "ERROR", "r1", Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康评估', "ALL", "r1", Openpyxl_PO, TOKEN)

# ChcRule_PO.run('健康评估', None, None, Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康评估', "OK", None, Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康评估', "ERROR", None, Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康评估', "ALL", None, Openpyxl_PO, TOKEN)


# todo 健康干预
# ChcRule_PO.run('健康干预', "ERROR", None, Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康干预', "ALL", None, Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康干预', OK, None, Openpyxl_PO, TOKEN)
# ChcRule_PO.run('健康干预', None, None, Openpyxl_PO, TOKEN)


# todo 疾病评估规则（已患和高风险）
# ChcRule_PO.run('疾病评估规则（已患和高风险）', None, "GW_JB004", Openpyxl_PO, TOKEN)



