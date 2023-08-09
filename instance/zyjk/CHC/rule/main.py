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



# main
# ChcRule_PO.run('健康评估', "", "r6", Openpyxl_PO, TOKEN)  # OK
ChcRule_PO.run('健康评估', "OK", "r1", Openpyxl_PO, TOKEN)  # OK
# ChcRule_PO.run('健康评估', "ERROR", "r1", Openpyxl_PO, TOKEN)  # ok
# ChcRule_PO.run('健康评估', "ALL", "r1", Openpyxl_PO, TOKEN)  # ok

# ChcRule_PO.run('健康评估', "ALL", "", Openpyxl_PO, TOKEN)  # ok
# ChcRule_PO.run('健康评估', "OK", "", Openpyxl_PO, TOKEN)  # ok
# ChcRule_PO.run('健康评估', "ERROR", "", Openpyxl_PO, TOKEN)  # ok
# ChcRule_PO.run('健康评估', "", "", Openpyxl_PO, TOKEN)  # ok





# ChcRule_PO.run('健康干预', Openpyxl_PO, TOKEN)

# ChcRule_PO.run('疾病评估规则（已患和高风险）', Openpyxl_PO, TOKEN)   # 汪刚



