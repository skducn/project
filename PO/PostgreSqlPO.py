# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Data       : 2022-12-06
# Description: PostgreSQL 对象层
# pip3.9 install psycopg2
# 参考：http://www.51testing.com/html/85/n-7794185.html
# python sqlalchemy中create_engine用法 https://blog.csdn.net/xc_zhou/article/details/118829588
# PostgreSQL  https://docs.sqlalchemy.org/en/14/dialects/postgresql.html
# ***************************************************************

import psycopg2
from sqlalchemy import create_engine


class PostgreSqlPO:
    def __init__(self, varHost, varUser, varPassword, varDB, varPort):

        self.host = varHost
        self.user = varUser
        self.password = varPassword
        self.db = varDB
        self.port = varPort
        self.conn = psycopg2.connect(
            host=varHost,
            user=varUser,
            password=varPassword,
            database=varDB,
            port=str(varPort),
            use_unicode=True,
        )
        self.cur = self.conn.cursor()
        if not self.cur:
            raise (NameError, "error，创建游标失败！")

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

    def getEngine_psycopg2(self):
        return create_engine(
            "postgresql+psycopg2://"
            + self.user
            + ":"
            + self.password
            + "@"
            + self.host
            + "/"
            + self.db
        )

    def getEngine(self):
        return create_engine(
            "postgresql://"
            + self.user
            + ":"
            + self.password
            + "@"
            + self.host
            + "/"
            + self.db
        )

    def getEngine_pg8000(self):
        return create_engine(
            "postgresql+pg8000://"
            + self.user
            + ":"
            + self.password
            + "@"
            + self.host
            + "/"
            + self.db
        )

    def close(self):
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":

    PostgreSql_PO = PostgreSqlPO("host", "user", "password", "db", "port")
    # t_userNo = PostgreSql_PO.execQuery('select id from sys_user_detail where userNo="%s"' % ("16766667777"))
