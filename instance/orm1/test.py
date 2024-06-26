# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2022-5-25
# Description: # orm 对象-关系映射
# https://blog.csdn.net/weixin_46220599/article/details/124470724
# ORM全称“Object Relational Mapping”，即对象-关系映射，就是把关系数据库的一行映射为一个对象，也就是一个类对应一个表，这样，写代码更简单，不用直接操作SQL语句。

# python 制作一个简单的orm框架
# 支持insert, update, select, delete操作
# 支持全表查询，全表删除，删除表操作
# 如需更复杂的sql操作，框架支持直接运行sql
# 实例，自动创建Test123表，id,username,password字段和值
# *****************************************************************

from ormPO import *
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
database = Database(MySQLdb.connect( host="192.168.0.234", user='root', password='Zy_123456', database='crm', port=3306))

d = {"stringField": {'username':'not null', 'password':'not null', 'address':'shanghai'}, "intField": {'age':10}}

# todo 定义表结构
class StringField(Field):
    def __init__(self, name, *attrs):
        super().__init__(name, 'varchar(50)', *attrs)
class IntField(Field):
    def __init__(self, name, *attrs):
        super().__init__(name, 'int', *attrs)


class Test123(Model):
    def __init__(self, id = '', userName = '', password = ''):
        self['id'] = id
        self['userName'] = userName
        self['password'] = password
        # print(self['password'])
    id = IntField('id', 'primary key', 'not null')
    userName = StringField('username', 'not null')
    password = StringField('password', 'not null')


# ---------------------------------------------------------------------------------
# todo 将列表数据插入到数据库中
# 表：值
dd = {'Test123': [[0,'aaa','123'],[1,'bbb','666']]}

for k,v in dd.items():
        # 删除表(需要先判断表是否存在！
        database.dropIf(eval(k + '()'))  # database.drop(Test123())

        # 创建表
        database.create(eval(k + '()'))   # database.create(Test123())

        # 插入2条数据
        for i in range(len(v)):
            database.insert(eval(k + "(id = "+ str(v[i][0]) + ", userName = '" + str(v[i][1]) + "' , password = '" + str(v[i][2]) + "')"))

        # 插入3条数据
        # database.insert(
        #
        #         Test123(id = 0, userName = 'drd', password = '123456'),
        #         Test123(id = 1, userName = 'fef', password = '789098'),
        #         Test123(2,'aaaaaa', '11111')
        # )

        # todo 将数据库数据导出列表
        data = database.selectAll(eval(k + '()')) # data = database.selectAll(Test123())
        data.sort(key=lambda data: data['id'])
        # data.sort(key = lambda data: data['id'], reverse = True)  # 倒序
        print(data)  # [{'id': 0, 'userName': 'aaa', 'password': '123456'}, {'id': 1, 'userName': 'bbb', 'password': '789098'}]

database.commit()
database.close()


