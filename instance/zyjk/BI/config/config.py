﻿# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: 电子健康档案数据监控中心 配置文件
# *****************************************************************

import string, numpy
from string import digits
from PO.MysqlPO import *
from PO.TimePO import *
Time_PO = TimePO()

# 测试环境及账号
varURL = "https://192.168.0.183/admin/login?return=https%3A%2F%2F192.168.0.183%2Fportal_hosp%3Fcode%3D5749894d0d424f508d8139779150113b&system=portal&system=portal"
varUser = "0166"
varPass = "123456"


# 测试数据库
Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bitest", 3306)  # 测试数据库
# Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bidev", 3306)  # 开发数据库


logFile = './log/bi_' + Time_PO.getDate() + '.log'

email_nickNameByFrom = u'令狐冲'
email_sender = 'skducn@163.com'
email_receiver = "h.jin@zy-healthtech.com"
email_subject = "bi自动化测试结果"
email_content = "你好！\n\n\n    这是本次bi集成平台自动化测试结果，请查看附件。\n\n\n\n\n\n\n\n这是一封自动产生的email，请勿回复 \n测试组 \nBest Regards"
email_attachment = logFile


