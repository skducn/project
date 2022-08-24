# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2022-8-24
# Description: erp(测试238) , dbDesc()搜索表结构，dbRecord()搜索表记录
# *****************************************************************

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from PO import MysqlPO
mysql_PO = MysqlPO.MysqlPO("192.168.0.238", "root", "ZAQ!2wsx", "crmtest", 3306)


# mysql_PO.dbDesc()  # 输出表结构
# mysql_PO.dbDesc2xlsx("d:\\crmtest.xlsx")  # 另存表结构

# mysql_PO.dbRecord('*', 'char', '二二')
# mysql_PO.dbRecord('t_dinatibiogen_potential_info', 'int', 15060)
# mysql_PO.dbRecord('*', 'int', 15060)
# mysql_PO.dbRecord('*', 'timestamp', u'%2022-08-24 13:11%')
# mysql_PO.dbRecord('*', 'varchar', '16766667777')  # 模糊搜索所有表中带yoy的char类型。

