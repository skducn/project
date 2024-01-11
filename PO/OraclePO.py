# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Data       : 2022-12-06
# Description: Oracle 对象层
# pip3.9 install cx_Oracle
# 参考：http://www.51testing.com/html/85/n-7794185.html
# ***************************************************************

import cx_Oracle


class OraclePO:
    def __init__(self, varUser, varPassword, varHost, varServerName):

        self.varUser = varUser
        self.varPassword = varPassword
        self.varHost = varHost
        self.varServerName = varServerName

    def __GetConnect(self):

        """连接数据库"""

        self.conn = cx_Oracle.connect(
            self.varUser
            + "/"
            + self.varPassword
            + "@"
            + self.varHost
            + "/"
            + self.varServerName
        )
        # print(self.conn.version.split()[0])  # 11.2.0.1.0
        self.cur = self.conn.cursor()
        if not self.cur:
            raise (NameError, "连接数据库失败")  # 将DBC信息赋值给cur
        else:
            return self.cur

    def execQuery(self, sql):

        """执行查询语句
        返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        """

        try:
            cur = self.__GetConnect()
            self.conn.commit()
            cur.execute(sql)
            self.conn.commit()
            result = self.cur.fetchall()
            cur.close()
            self.conn.close()
            return result
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')
    def execQueryParam(self, sql,params):

        """执行查询语句
        返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        """

        try:
            cur = self.__GetConnect()
            cur.execute(sql, params)
            # self.conn.commit()
            result = self.cur.fetchall()
            # cur.close()
            # self.conn.close()
            return result
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')



if __name__ == "__main__":

    Oracle_PO = OraclePO("SUNWENBO", "Sunwenbo1204", "192.168.0.235:1521", "ORCL")

    r = Oracle_PO.execQuery('SELECT * FROM DIP.EHR_DISABILITY_VISIT')
    print(r)
    for i in r:
        print(i)

