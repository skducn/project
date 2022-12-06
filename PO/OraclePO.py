# -*- coding: utf-8 -*-
#***************************************************************
# Author     : John
# Data       : 2022-12-06
# Description: Oracle 对象层
# pip3.9 install cx_Oracle
# 参考：http://www.51testing.com/html/85/n-7794185.html
#***************************************************************

import cx_Oracle


class OraclePO():

    def __init__(self, varUser, varPassword, varHost, varDB):

        self.varUser = varUser
        self.varPassword = varPassword
        self.varHost = varHost
        self.varDB = varDB


    def __GetConnect(self):

        '''连接数据库'''

        if not self.varDB:
            raise (NameError, "没有设置数据库信息")
        self.conn = cx_Oracle.connect(self.varUser + "/" + self.varPassword + "@" + self.varHost + "/" + self.varDB)
        self.cur = self.conn.cursor()
        if not self.cur:
            raise (NameError, "连接数据库失败")  # 将DBC信息赋值给cur
        else:
            return self.cur

    def execQuery(self, sql):

        ''' 执行查询语句
        返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        '''

        cur = self.__GetConnect()
        self.conn.commit()  # 用于新增后立即查询
        cur.execute(sql)

        try:
            result = cur.fetchall()
        except:
            self.conn.commit()
            cur.close()
            self.conn.close()
            return
        self.conn.commit()
        cur.close()
        self.conn.close()
        return result



if __name__ == '__main__':


    Oracle_PO = OraclePO("user","password","host","db")
    # t_userNo = Oracle_PO.execQuery('select id from sys_user_detail where userNo="%s"' % ("16766667777"))
