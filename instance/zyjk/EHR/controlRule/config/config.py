# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-5-12
# Description: 电子健康档案 - 质控配置文件
# *****************************************************************


from PO.LogPO import *
from PO.NetPO import *
from PO.DataPO import *
# from PO.ExcelPO.ExcelPO import *
from PO.FilePO import *
File_PO = FilePO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.ColorPO import *
Color_PO = ColorPO()

from PO import SqlserverPO
Sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHRDC")  # 测试环境

# 日志文件
logFile = './log/controlRul_' + Time_PO.getDate() + '.log'

# # 邮件信息
# email_nickNameByFrom = u'令狐冲'
# email_sender = 'skducn@163.com'
# email_receiver = "h.jin@zy-healthtech.com"
# email_subject = "bi自动化测试结果"
# email_content = "你好！\n\n\n    这是本次bi集成平台自动化测试结果，请查看附件。\n\n\n\n\n\n\n\n这是一封自动产生的email，请勿回复 \n测试组 \nBest Regards"
# email_attachment = logFile


