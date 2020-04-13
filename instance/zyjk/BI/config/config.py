# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: 电子健康档案数据监控中心 配置文件
# *****************************************************************

import string, numpy
from string import digits
from PO.MysqlPO import *


# 测试环境及账号
varURL = "https://192.168.0.183/admin/login?return=https%3A%2F%2F192.168.0.183%2Fportal_hosp%3Fcode%3D5749894d0d424f508d8139779150113b&system=portal&system=portal"
varUser = "016"
varPass = "123456"


# 测试数据库
Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bitest", 3306)  # 测试数据库
# Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bidev", 3306)  # 开发数据库


# bi_outpatient_yard  //全院门诊就诊统计