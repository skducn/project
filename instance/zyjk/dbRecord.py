# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-4-28
# Description: dbRecord()搜索表记录 from cmd
# *****************************************************************
import sys
sys.path.append("D:\\51\\python\\project")
from Public.PageObject.SqlServerPO import *
from Public.PageObject.MysqlPO import *

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
        if len(sys.argv) >= 2 and len(sys.argv) <= 3 :
            print(u"\n例子1：dbRecord.py EHR * varchar %jinhao% \n"
                  u"\n例子2：dbRecord.py EHR UpmsUser varchar e10adc3949ba59abbe56e057f20f883e \n"
                  u"\n例子3：dbRecord.py EHR CommonDictionaryType datetime 2018-10-15_18:21% \n"
                  u"\n例子4：dbRecord.py ehr * datetime 2018-10-15_18:21% \n"
                  )
        elif len(sys.argv) == 5:
            if sys.argv[2] == "*":
                if sys.argv[3] == 'datetime':
                    SqlServer_PO.dbRecord(sys.argv[2], sys.argv[3], str(sys.argv[4]).replace("_", " "))
                else:
                    SqlServer_PO.dbRecord(sys.argv[2], sys.argv[3], str(sys.argv[4]))
            else:
                if sys.argv[3] == "datetime":
                    SqlServer_PO.dbRecord(sys.argv[2], sys.argv[3], str(sys.argv[4]).replace("_", " "))
                else:
                    SqlServer_PO.dbRecord(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("错误，预期参数：5，实际参数：" + str(len(sys.argv)))

    # **********************************************************************************************************************************
    # PIM 基层健康管理平台
    elif sys.argv[1] == "PIM" or sys.argv[1] == "pim":
        SqlServer_PO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "pimtest")  # 测试环境
        if len(sys.argv) >= 2 and len(sys.argv) <= 3 :
            print(u"\n例子1：dbRecord.py PIM * varchar %海鹰居委会% \n"
                  u"\n例子2：dbRecord.py pim t_upms_user varchar e10adc3949ba59abbe56e057f20f883e \n"
                  u"\n例子3：dbRecord.py pim * money 34.5% \n"
                  )
        elif len(sys.argv) == 5:
            if sys.argv[2] == "*":
                if sys.argv[3] == 'datetime':
                    SqlServer_PO.dbRecord(sys.argv[2], sys.argv[3], str(sys.argv[4]).replace("_", " "))
                else:
                    SqlServer_PO.dbRecord(sys.argv[2], sys.argv[3], str(sys.argv[4]))
            else:
                if sys.argv[3] == "datetime":
                    SqlServer_PO.dbRecord(sys.argv[2], sys.argv[3], str(sys.argv[4]).replace("_", " "))
                else:
                    SqlServer_PO.dbRecord(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("错误，预期参数：5，实际参数：" + str(len(sys.argv)))

    # **********************************************************************************************************************************
    # fsms 家床
    elif sys.argv[1] == "FSMS" or sys.argv[1] == "fsms":
        SqlServer_PO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "fsms") # 测试环境
        if len(sys.argv) == 2:
            print(u"\n例子1：dbRecord.py fams * varchar %测试1%\n"
                  u"\n例子2：dbRecord.py fams t_upms_user varchar e10% \n"
                  u"\n例子3：dbRecord.py fams * double %35% \n"
                  u"\n例子4：dbRecord.py fams * timestamp %2019-01% \n"
                  )
        elif len(sys.argv) == 5:
            if sys.argv[2] == "*":
                if sys.argv[3] == 'datetime':
                    SqlServer_PO.dbRecord(sys.argv[2], sys.argv[3], str(sys.argv[4]).replace("_", " "))
                else:
                    SqlServer_PO.dbRecord(sys.argv[2], sys.argv[3], str(sys.argv[4]))
            else:
                if sys.argv[3] == "datetime":
                    SqlServer_PO.dbRecord(sys.argv[2], sys.argv[3], str(sys.argv[4]).replace("_", " "))
                else:
                    SqlServer_PO.dbRecord(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("错误，预期参数：5，实际参数：" + str(len(sys.argv)))

    # **********************************************************************************************************************************
    # crm 盛蕴CRM小程序
    elif sys.argv[1] == "CRM" or sys.argv[1] == "crm":
        Mysql_PO = MysqlPO("172.21.200.70", "jinhao", "123456", "TD_APP")  # 测试环境
        if len(sys.argv) == 2:
            print(u"\n例子1：dbRecord.py crm * varchar 金丽娜\n"
                  u"\n例子2：dbRecord.py crm * int 2250 \n"
                  u"\n例子3：dbRecord.py crm * datetime %2019-04-12_15:13:23% \n"
                  u"\n例子4：dbRecord.py crm user char 金丽娜 \n"
                  )
        elif len(sys.argv) == 5:
            if sys.argv[2] == "*":
                if sys.argv[3] == 'datetime':
                    Mysql_PO.dbRecord(sys.argv[2], sys.argv[3], str(sys.argv[4]).replace("_", " "))
                else:
                    Mysql_PO.dbRecord(sys.argv[2], sys.argv[3], str(sys.argv[4]))
            else:
                if sys.argv[3] == "datetime":
                    Mysql_PO.dbRecord(sys.argv[2], sys.argv[3], str(sys.argv[4]).replace("_", " "))
                else:
                    Mysql_PO.dbRecord(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("错误，预期参数：5，实际参数：" + str(len(sys.argv)))
    else:
        print("\n项目名<" + sys.argv[1] + ">不存在！")


# 盛孕 CRM小程序
# Mysql_PO.dbCreateDate()   # 查看所有表的创建时间
# Mysql_PO.dbCreateDate('app_code')   # 查看book表创建时间
# Mysql_PO.dbCreateDate('fact*')   # 查看所有b开头表的创建时间，通配符*
# Mysql_PO.dbCreateDate('after', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
# Mysql_PO.dbCreateDate('>', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
# Mysql_PO.dbCreateDate('before', "2019-04-10")  # 显示所有在2019-12-08之前创建的表
# Mysql_PO.dbCreateDate('<', "2019-02-18")  # 显示所有在2019-12-08之前创建的表




