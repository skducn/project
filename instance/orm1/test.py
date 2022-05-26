# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2022-5-25
# Description: # orm 对象关系映射
# https://blog.csdn.net/weixin_46220599/article/details/124470724
# python 制作一个简单的orm框架
# 支持insert, update, select, delete操作
# 支持全表查询，全表删除，删除表操作
# 如需更复杂的sql操作，框架支持直接运行sql
# User类名就是表名
# *****************************************************************

#!/usr/bin/env python3

from ormPO import *
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

if __name__ == '__main__':
        # import mysql.connector
        class StringField(Field):
                def __init__(self, name, *attrs):
                        super().__init__(name, 'varchar(50)', *attrs)

        class IntField(Field):
                def __init__(self, name, *attrs):
                        super().__init__(name, 'int', *attrs)

        class User(Model):
                def __init__(self, *, id = '', userName = '', password = ''):
                        self['id'] = id
                        self['userName'] = userName
                        self['password'] = password
                id = IntField('id', 'primary key', 'not null')
                userName = StringField('username', 'not null')
                password = StringField('password', 'not null')

        database = Database(MySQLdb.connect( host="192.168.0.238", user='root', password='ZAQ!2wsx', database = 'saashypertensiontest', port=3306))

        database.create(User())
        database.insert(
                User(id = 0, userName = 'aaa', password = 'aaa'),
                User(id = 1, userName = 'bbb', password = 'bbb')
        )
        users = database.selectAll(User())
        users.sort(key = lambda user: user['id'], reverse = True)
        print(users)
        for i in users:
                print(i)
        database.drop(User())
        database.commit()
        database.close()

