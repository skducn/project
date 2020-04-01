# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-3-5
# Description: sqlserver
# https://www.cnblogs.com/malcolmfeng/p/6909293.html
# pymssql托管在Github上：https://github.com/pymssql
# https://www.cnblogs.com/TF12138/p/4064752.html
# *****************************************************************
import pymssql
from time import sleep
server = "192.168.0.36"
user = "sa"
password = "@1qaz@WSX"
varDB = "healthrecord_test"
conn = pymssql.connect(server, user, password, varDB)  #获取连接
cur = conn.cursor() # 获取光标

# # 创建表
# cursor.execute("""
# IF OBJECT_ID('persons', 'U') IS NOT NULL
#     DROP TABLE persons
# CREATE TABLE persons (
#     id INT NOT NULL,
#     name VARCHAR(100),
#     salesrep VARCHAR(100),
#     PRIMARY KEY(id)
# )
# """)

# # 插入多行数据
# cursor.executemany(
#     "INSERT INTO persons VALUES (%d, %s, %s)",
#     [(1, 'John Smith', 'John Doe'),
#      (2, 'Jane Doe', 'Joe Dog'),
#      (3, 'Mike T.', 'Sarah H.')])
# # 你必须调用 commit() 来保持你数据的提交如果你没有将自动提交设置为true
# conn.commit()

# SELECT NAME FROM SYSOBJECTS WHERE TYPE='U'
# 'SELECT * FROM INFORMATION_SCHEMA.TABLES'

# 查询数据
# cur.execute('SELECT * FROM t_upms_user WHERE number=%s', '005')
# cur.execute("SELECT NAME FROM SYSOBJECTS WHERE TYPE='U'")
# cur.execute("select syscolumns.name,systypes.name from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('t_upms_user')")
# row = cur.fetchall()
# # print(len(row))
# for i in range(len(row)):
#     print(row[i][0],row[i][1])


# # 遍历数据（存放到元组中） 方式1
# row = cur.fetchone()
# while row:
#     # print("ID=%d, Name=%s" % (row[0], row[2]))
#     row = cur.fetchone()
#
# # 遍历数据（存放到元组中） 方式2
# for row in cur:
#     print('row = %r' % (row,))

def dbRecord(varTable, varType, varValue):

    '''
    # 搜索记录
    # 参数1：varTable = 表名（*表示所有的表）
    # 参数2：varType = 数据类型(char,int,double,timestamp)
    # 参数3：varValue = 值 (支持%模糊查询，如 %yy%)
    # dbRecord('myclass','char', 'yoyo')  # 报错？
    dbRecord('*','char', u'%yoy%')  # 模糊搜索所有表中带yoy的char类型。
    # dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
    # dbRecord('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。
    '''

    list0 = []
    list1 = []
    x = y = 0
    varKeyword = "remark,period"
    print()
    if varType in "int,char,double,timestamp,varchar":
        if "*" in varTable :
            # 遍历所有表
            cur.execute("SELECT NAME FROM SYSOBJECTS WHERE TYPE='U'")
            tbl = cur.fetchall()
            for b in range(len(tbl)):
                # 遍历所有的表 de 列名称、列类别、类注释
                varTable = tbl[b][0]
                # 获取表的注释
                # cur.execute('SELECT * FROM %s' % (varTable))
                # tblDDL = cur.fetchone()
                # 获取列名称、列类别、类注释
                cur.execute("select syscolumns.name,systypes.name from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')" % (varTable))
                tblFields = cur.fetchall()
                for i in tblFields:
                    if len(i[0]) > x: x = len(i[0])
                    if len(i[1]) > y: y = len(i[1])
                for j in tblFields:
                    if varType in j[1]:
                        list0.append(j[0])
                        list1.append(j[1])
                # print(varTable)
                for i in range(0, len(list0)):
                    cur.execute("select * from %s where %s like '%s'" % (varTable, list0[i], varValue))
                    t4 = cur.fetchall()
                    if len(t4) != 0:
                        # print("search: " + varValue + " > " + varDB + "." + varTable + "(" + str(tblDDL[0]) + ")." + list0[i] + " > [" + str(len(t4)) + " records]" + "\n" + "-"*60)
                        print("search: " + varValue + " > " + varDB + "." + varTable + "(" ")." + list0[i] + " > [" + str(len(t4)) + " records]" + "\n" + "-"*60)
                        for j in range(len(t4)):
                            print(list(t4[j]))
                        print()
                list0 = []; list1 = []
        elif "*" not in varTable:
            # 获取列名称、列类别、类注释
            cur.execute("select syscolumns.name,systypes.name from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')" % (varTable))
            tblFields = cur.fetchall()
            for i in tblFields:
                if len(i[0]) > x: x = len(i[0])
                if len(i[1]) > y: y = len(i[1])
            for j in tblFields:
                if varType in j[1]:
                    list0.append(j[0])
                    list1.append(j[1])
            for i in range(0, len(list0)):
                cur.execute("select * from %s where %s like '%s'" % (varTable, list0[i], varValue))
                t4 = cur.fetchall()
                if len(t4) != 0:
                    print("search: " + varValue + " > " + varDB + "." + varTable + "(" ")." + list0[
                        i] + " > [" + str(len(t4)) + " records]" + "\n" + "-" * 60)
                    for j in range(len(t4)):
                        print(list(t4[j]))
                    print()
            list0 = []
            list1 = []


# dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
dbRecord('*', 'varchar', '%admin%')  # 模糊搜索所有表中带yoy的char类型。
# dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# dbRecord('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。


# cursor.execute('select TABLE_NAME from information_schema.`TABLES` where table_schema="%s" ' % varDB)
# tblName = cursor.fetchall()
# print(len(row))

# 遍历数据（存放到字典中）
# cursor = conn.cursor(as_dict=True)
#
# cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
# for row in cursor:
#     print("ID=%d, Name=%s" % (row['id'], row['name']))
#
# conn.close()
# 关闭连接
conn.close()

