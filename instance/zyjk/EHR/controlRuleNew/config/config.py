# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-6-9
# Description: 电子健康档案 - 质控配置文件
# *****************************************************************

from PO.LogPO import *
from PO.NetPO import *
from PO.DataPO import *
from PO.ExcelPO.ExcelPO import *
from PO.TimePO import *
Time_PO = TimePO()

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.35", "test", "123456", "data_center_test1")  # 测试环境

varExcel = "cr1.2.xlsx"
varExcelSheet = "controlRule"
varCurl = 'curl http://localhost:8080/healthRecordRules/rulesApi/execute/31011310200312009116'
varJar = 'healthRecordRules.jar'

# 日志文件
logFile = './log/controlRul_' + Time_PO.getDate() + '.log'

# # 邮件信息
# email_nickNameByFrom = u'令狐冲'
# email_sender = 'skducn@163.com'
# email_receiver = "h.jin@zy-healthtech.com"
# email_subject = "bi自动化测试结果"
# email_content = "你好！\n\n\n    这是本次bi集成平台自动化测试结果，请查看附件。\n\n\n\n\n\n\n\n这是一封自动产生的email，请勿回复 \n测试组 \nBest Regards"
# email_attachment = logFile


