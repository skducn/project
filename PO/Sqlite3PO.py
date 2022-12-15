# -*- coding: utf-8 -*-
#***************************************************************
# Author     : John
# Data       : 2022-12-15
# Description: sqlite3 对象层
# http://www.51testing.com/html/22/n-7794322.html
#***************************************************************

import sqlite3


class Sqlite3PO():

    def __init__(self, db):

        self.db = db

    def __GetConnect(self):

        '''连接数据库'''

        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()
        if not self.cur:
            raise (NameError, "连接数据库失败")
        else:
            return self.cur


    def execQuery(self, sql):

        ''' 创建，单插入，查询语句
        返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        '''

        cur = self.__GetConnect()
        cur.execute(sql)

        try:
            result = cur.fetchall()
            self.conn.commit()
            return result
        except:
            self.conn.commit()
            return None

    def executemany(self, sql, varList):

        ''' 批量插入'''

        cur = self.__GetConnect()
        cur.executemany(sql, varList)
        self.conn.commit()



    def close(self):

        ''' 关闭'''

        self.conn.close()



if __name__ == '__main__':

    Sqlite3_PO = Sqlite3PO('students.db')

    # 1,建表
    # Sqlite3_PO.execQuery("""CREATE TABLE hh (
    # name TEXT,
    # age INTEGER,
    # height REAL
    # )""")


    # 2,插入单条数据
    # Sqlite3_PO.execQuery("INSERT INTO students VALUES ('mark', 20, 1.9)")

    # 3,插入多条数据
    all_students = [
        ('john', 21, 1.8),
        ('david', 35, 1.7),
        ('michael', 19, 1.83),
        ]
    Sqlite3_PO.executemany("INSERT INTO students VALUES (?, ?, ?)", all_students)


    # 4,查询
    x = Sqlite3_PO.execQuery("SELECT * FROM students")
    print(x)


    Sqlite3_PO.close()


