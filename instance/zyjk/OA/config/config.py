# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-6-4
# Description: OA 配置文件
# *****************************************************************

import string, numpy
from string import digits
from PO.WebPO import *
from PO.ListPO import *
from PO.TimePO import *
from PO.ColorPO import *
from PO.LogPO import *
from PO.NetPO import *
from PO.DataPO import *
from PO.FilePO import *
from PO.StrPO import *
from PO.ExcelPO.ExcelPO import *
from PO.TimePO import *
Time_PO = TimePO()

from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bitest", 3306)  # 测试数据库

# 39 环境
varURL = "http://192.168.0.39"

# 日志文件
logFile = './log/oa_' + Time_PO.getDate() + '.log'
#
# # 邮件信息
# email_nickNameByFrom = u'令狐冲'
# email_sender = 'skducn@163.com'
# email_receiver = "h.jin@zy-healthtech.com"
# email_subject = "bi自动化测试结果"
# email_content = "你好！\n\n\n    这是本次bi集成平台自动化测试结果，请查看附件。\n\n\n\n\n\n\n\n这是一封自动产生的email，请勿回复 \n测试组 \nBest Regards"
# email_attachment = logFile


