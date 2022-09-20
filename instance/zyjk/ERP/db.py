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
# mysql_PO.dbDesc('fact*')  # 查看所有b开头的表结构（通配符*）
# mysql_PO.dbDesc('app_info')   # app_info表结构
# mysql_PO.dbDesc('fact*', 'Id,page')  # 查看所有b开头的表中id字段的结构（通配符*）
# mysql_PO.dbDesc('app_info', 'id,mid')   # 查看book表id,page字段的结构

# mysql_PO.dbDesc2xlsx("d:\\crmtest.xlsx")  # 另存表结构


# mysql_PO.dbRecord('*', 'char', '二二')
# mysql_PO.dbRecord('t_dinatibiogen_potential_info', 'int', 15060)
# mysql_PO.dbRecord('*', 'int', 15060)
# mysql_PO.dbRecord('*', 'timestamp', '2022-08-24 13:11%')
# mysql_PO.dbRecord('*', 'varchar', '16766667777')  # 模糊搜索所有表中带yoy的char类型。
# mysql_PO.dbRecord('*', 'float', u'%295.54%')

# mysql_PO.dbCreateDate()   # 查看所有表的创建时间
# mysql_PO.dbCreateDate('app_code')   # 查看book表创建时间
# mysql_PO.dbCreateDate('fact*')   # 查看所有b开头表的创建时间，通配符*
# mysql_PO.dbCreateDate('after', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
# mysql_PO.dbCreateDate('>', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
# mysql_PO.dbCreateDate('before', "2019-04-10")  # 显示所有在2019-12-08之前创建的表
# mysql_PO.dbCreateDate('<', "2019-02-18")  # 显示所有在2019-12-08之前创建的表