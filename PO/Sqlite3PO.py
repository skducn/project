# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Data       : 2022-12-15
# Description: sqlite3 对象层
# http://www.51testing.com/html/22/n-7794322.html
# SQLite Viewer  http://sqlite.zhangningning.com.cn/
# python sqlalchemy中create_engine用法 https://blog.csdn.net/xc_zhou/article/details/118829588
# ***************************************************************

"""

1 建表 execQuery(create)
2 插入单条数据  execQuery(insert)
3 插入多条数据  executemany(insert, list)
4 查询  execQuery(select)
5 将csv导入数据库表  csv2db(varCSV, varTable)

"""

import sqlite3
import pandas as pd
from sqlalchemy import create_engine


class Sqlite3PO:
    def __init__(self, db):

        self.db = db
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def execQuery(self, sql):

        """执行sql"""

        try:
            r = self.cur.execute(sql).fetchall()
            self.conn.commit()
            return r
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')
            return None

    def executemany(self, sql, varList):

        """批量插入"""

        try:
            self.cur.executemany(sql, varList)
            self.conn.commit()
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')

    def getEngine_sqlite(self):

        return create_engine("sqlite:///" + self.db)
        # return create_engine('sqlite:absolute/path/to/' + self.db)

    def csv2db(self, varCSV, varTable, if_exists="fail"):

        """将 csv 导入 数据库表"""
        # if_exists = 'fail', 'replace', 'append'
        # Sqlite3_PO.csv2db("./data/test12.csv", "population")

        try:
            df = pd.read_csv(varCSV)
            df.to_sql(varTable, con=self.getEngine_sqlite(), if_exists=if_exists)
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')

    def close(self):
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":

    varTable = "baidu"

    # 创建或打开 db
    Sqlite3_PO = Sqlite3PO("./data/student12s.db")

    # print("1 建表 school".center(100, "-"))
    # Sqlite3_PO.execQuery("""CREATE TABLE %s (
    # name TEXT,
    # age INTEGER,
    # height REAL
    # )""" % (varTable))
    #
    #
    # print("2 插入单条数据".center(100, "-"))
    # Sqlite3_PO.execQuery("INSERT INTO %s VALUES ('mark', 20, 1.44449)" % (varTable))
    #
    #
    # print("3 插入多条数据".center(100, "-"))
    # c = [
    #     ('john', 21, 1.8),
    #     ('david', 35, 1.7),
    #     ('michael', 19, 1.83),
    #     ]
    # Sqlite3_PO.executemany("INSERT INTO %s VALUES (?, ?, ?)" % (varTable), c)

    # print("4 查询".center(100, "-"))
    # r = Sqlite3_PO.execQuery("SELECT * FROM %s" % (varTable))
    # print(r)  # [('mark', 20, 1.44449)]
    # print(r[0][1])  # 20

    # print("5 将csv导入数据库表".center(100, "-"))
    # # Sqlite3_PO.csv2db("./data/test12.csv", varTable)  # 如果表已存在，则返回ValueError("Table 'baidu' already exists.")
    # Sqlite3_PO.csv2db("./data/test12.csv", varTable, 'replace')  # 替换 varTable
    # # Sqlite3_PO.csv2db("./data/test12.csv", varTable, 'append')  # 追加 varTable
    # x = Sqlite3_PO.execQuery("SELECT * FROM %s" % (varTable))
    # print(x)

    Sqlite3_PO.close()
