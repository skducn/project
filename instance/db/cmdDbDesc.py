# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-4-16
# Description: dbDesc()搜索表结构 from cmd
# *****************************************************************
import sys
# sys.path.append("D:\\51\\python\\project")
sys.path.append("../../")
from PO.SqlserverPO import *
from PO.MysqlPO import *

if len(sys.argv) == 1 :
    print(u"\n功能：搜索表结构或记录\n"      
           u"\n参数1：项目名，如 EHR，PIM，fsms，crm\n"  
           u"\n参数2：表名，如单表UpmsUser 或 多表mon* 及所有的表\n"
           u"\n参数3：字段名\n"
           u"\n例子1：dbDesc.py EHR * \n"
           u"\n例子2：dbDesc.py EHR UpmsUser \n"
           u"\n例子3：dbDesc.py EHR mon* \n"
           u"\n例子4：dbDesc.py ehr UpmsUser Birthday \n"
           u"\n例子5：dbDesc.py ehr UpmsUser Id,Birthday,Sex \n"
          )
else:
    # EHR 电子健康档案
    if sys.argv[1] == "EHR" or sys.argv[1] == "ehr":
        SqlServer_PO = SqlServerPO("192.168.0.35", "test", "123456", "healthrecord_test")  # 测试环境
        if len(sys.argv) == 2:
            print(u"\n例子1：dbDesc.py EHR * \n"
                  u"\n例子2：dbDesc.py EHR UpmsUser \n"
                  u"\n例子3：dbDesc.py EHR mon* \n"
                  u"\n例子4：dbDesc.py ehr UpmsUser Birthday \n"
                  u"\n例子5：dbDesc.py ehr UpmsUser Id,Birthday,Sex \n"
                  )
        if len(sys.argv) == 3:
            if sys.argv[2] == "*":
                SqlServer_PO.dbDesc()
            elif sys.argv[2] != "*":
                SqlServer_PO.dbDesc(sys.argv[2])
        if len(sys.argv) == 4:
            SqlServer_PO.dbDesc(sys.argv[2], sys.argv[3])

    # PIM 基层健康管理平台
    elif sys.argv[1] == "PIM" or sys.argv[1] == "pim":
        SqlServer_PO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "pimtest")  # 测试环境
        if len(sys.argv) == 2:
            print(u"\n例子1：dbDesc.py PIM * \n"
                  u"\n例子2：dbDesc.py pim t_upms_user \n"
                  u"\n例子3：dbDesc.py pim b* \n"
                  u"\n例子4：dbDesc.py pim t_ph_outin_batch subNo,orgNo \n"
                  u"\n例子5：dbDesc.py pim b* subNo,orgNo \n"
                  )
        if len(sys.argv) == 3:
            if sys.argv[2] == "*":
                SqlServer_PO.dbDesc()
            elif sys.argv[2] != "*":
                SqlServer_PO.dbDesc(sys.argv[2])
        if len(sys.argv) == 4:
            SqlServer_PO.dbDesc(sys.argv[2], sys.argv[3])

    # fsms 家床
    elif sys.argv[1] == "FSMS" or sys.argv[1] == "fsms":
        SqlServer_PO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "fsms") # 测试环境
        if len(sys.argv) == 2:
            print(u"\n例子1：dbDesc.py fams * \n"
                  u"\n例子2：dbDesc.py fams t_upms_user \n"
                  u"\n例子3：dbDesc.py fams b* \n"
                  u"\n例子4：dbDesc.py fams t_ph_outin_batch subNo,orgNo \n"
                  u"\n例子5：dbDesc.py fams b* subNo,orgNo \n"
                  )
        if len(sys.argv) == 3:
            if sys.argv[2] == "*":
                SqlServer_PO.dbDesc()
            elif sys.argv[2] != "*":
                SqlServer_PO.dbDesc(sys.argv[2])
        if len(sys.argv) == 4:
            SqlServer_PO.dbDesc(sys.argv[2], sys.argv[3])

    # crm 盛蕴CRM小程序
    elif sys.argv[1] == "CRM" or sys.argv[1] == "crm":
        Mysql_PO = MysqlPO("172.21.200.70", "jinhao", "123456", "TD_APP")  # 测试环境
        if len(sys.argv) == 2:
            print(u"\n例子1：dbDesc.py crm * \n"
                  u"\n例子2：dbDesc.py crm app_info \n"
                  u"\n例子3：dbDesc.py crm fact* \n"
                  u"\n例子4：dbDesc.py crm fact* Id,page \n"
                  u"\n例子5：dbDesc.py crm app_info id,mid \n"
                  )
        if len(sys.argv) == 3:
            if sys.argv[2] == "*":
                Mysql_PO.dbDesc()
            elif sys.argv[2] != "*":
                Mysql_PO.dbDesc(sys.argv[2])
        if len(sys.argv) == 4:
            Mysql_PO.dbDesc(sys.argv[2], sys.argv[3])
    else:
        print("\n项目名<" + sys.argv[1] + ">不存在！")





