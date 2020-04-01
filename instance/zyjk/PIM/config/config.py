# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: 电子健康档案数据监控中心 配置文件
# *****************************************************************

from PO.sqlserverPO import *
sqlserver_PO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "bmlpimpro")  # PIM 测试环境
import random

# 开发环境
# varURL = "http://103.25.65.103:8884/login?pcid=wdw7e6daa448f69204f977475162ba"
# dimUsername = "53"
# dimPassword = "123456"

# 测试环境
varURL = "http://192.168.0.81:8324/login?pcid=c841cd37bc206a6c143df687be04986d"
user_drugstore = "y001"  # 测试药房1
user_nurse = "h001"  # 测试护士1
user_doctor = 'd001'  # 测试医生1
user_admin = 's001'  # 测试收费1
user_test123 = '0166'

# 测试数据准备
# 随机获得数据库中患者姓名
l_patient = sqlserver_PO.ExecQuery('select name from t_system_patient_basic_info ')
varPatient = random.choice(l_patient)
varPatient = varPatient[0]
# # or 指定患者，如
# varPatient = '张2223'