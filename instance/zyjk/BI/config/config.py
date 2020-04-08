# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: 电子健康档案数据监控中心 配置文件
# *****************************************************************

import random

from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bidev", 3306)  # BI 开发数据库

# 测试环境
# varURL = "https://192.168.0.183/portal_hosp?code=5749894d0d424f508d8139779150113b&system=portal"
varURL = "https://192.168.0.183/admin/login?return=https%3A%2F%2F192.168.0.183%2Fportal_hosp%3Fcode%3D5749894d0d424f508d8139779150113b&system=portal&system=portal"
varUser = "016"
varPass = "123456"


# # 测试数据准备
# # 随机获得数据库中患者姓名
# l_patient = sqlserver_PO.ExecQuery('select name from t_system_patient_basic_info ')
# varPatient = random.choice(l_patient)
# varPatient = varPatient[0]
# # # or 指定患者，如
# # varPatient = '张2223'