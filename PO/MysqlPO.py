# -*- coding: utf-8 -*-
#***************************************************************
# Author     : John
# Data       : 2019-04-16
# Description: MysqlPO对象层
#***************************************************************
# pip3 install mysqlclient  (MySQLdb)
# pip3 install pymysql
# 问1：数据库中乱码显示问题，查询后却显示中文？
# 答1：设置 charset 编码，如 self.conn = MySQLdb.connect(host=self.varHost, user=self.varUser, passwd=self.varPassword, db=self.varDB, port=self.varPort, use_unicode=True, charset='utf8') ，注意：charset 应该与数据库编码一致，如数据库是gb2312 ,则 charset='gb2312'。
# None是一个对象，而NULL是一个类型。
# Python中没有NULL，只有None，None有自己的特殊类型NoneType
# None不等于0、任何空字符串、False等。
# 在Python中，None、False、0、""(空字符串)、[](空列表)、()(空元组)、{}(空字典)都相当于False
#***************************************************************

'''
pandas引擎（pymysql）  getPymysqlEngine()
pandas引擎（mysqldb）  getMysqldbEngine()

1，查看数据库表结构（字段、类型、大小、可空、注释），注意，表名区分大小写 dbDesc()
2，搜索表记录 dbRecord('*', 'money', '%34.5%')
3，查询创建时间 dbCreateDate()

4.1，数据库表导出excel db2xlsx()
4.2，数据库表导出html db2html()
4.3，数据库表导出csv db2csv()
4.4 excel导入数据库表 xlsx2db()
4.5 所有表结构导出excel dbDesc2xlsx()

5 获取单个表的所有字段


'''
import sys
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from PO.ExcelPO import *
import pandas as pd
from sqlalchemy import create_engine
from PO.OpenpyxlPO import *
from PO.NewexcelPO import *
from PO.ColorPO import *
Color_PO = ColorPO()

class MysqlPO():

    def __init__(self, varHost, varUser, varPassword, varDB, varPort=3336):
        self.varHost = varHost
        self.varUser = varUser
        self.varPassword = varPassword
        self.varDB = varDB
        self.varPort = int(varPort)

    def __GetConnect(self):

        '''连接数据库'''

        if not self.varDB:
            raise (NameError, "没有设置数据库信息")
        self.conn = MySQLdb.connect(host=self.varHost, user=self.varUser, passwd=self.varPassword, db=self.varDB, port=int(self.varPort), use_unicode=True)
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

    def getPymysqlEngine(self):
        # pandas引擎（pymysql）
        return create_engine('mysql+pymysql://' + self.varUser + ":" + self.varPassword + "@" + self.varHost + ":" + str(self.varPort) + "/" + self.varDB)

    def getMysqldbEngine(self):
        # pandas引擎（mysqldb）
        return create_engine('mysql+mysqldb://' + self.varUser + ":" + self.varPassword + "@" + self.varHost + ":" + str(self.varPort) + "/" + self.varDB)

    def _dbDesc_search(self, varTable, var_l_field=0):

        '''dbDesc函数中子查询'''

        l_field = []
        l_type = []
        l_isnull = []
        l_isKey = []
        l_comment = []

        t_table_comment = self.execQuery('select table_name,table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (self.varDB, varTable))
        if t_table_comment[0][0] == varTable:
            t_field_type_isnull_key_comment = self.execQuery('select column_name,column_type,is_nullable,column_key,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (self.varDB, varTable))
            # print(t_field_type_isnull_key_comment)  # (('id', 'int(11)', 'PRI', 'NO', '主键'),

            # 字段与类型对齐
            a = b = c = d = e = 0
            for i in t_field_type_isnull_key_comment:
                if len(i[0]) > a: a = len(i[0])
                if len(i[1]) > b: b = len(i[1])
                if len(i[2]) > c: c = len(i[2])
                if len(i[3]) > d: d = len(i[3])
                if len(i[4]) > e: e = len(i[4])

            if var_l_field != 0:
                # 可选字段
                for l in range(len(var_l_field)):
                    for m in range(len(t_field_type_isnull_key_comment)):
                        # print(t_field_type_key_isnull_comment[m][0])
                        if var_l_field[l] == t_field_type_isnull_key_comment[m][0]:
                            l_field.append(t_field_type_isnull_key_comment[m][0] + " " * (a - len(t_field_type_isnull_key_comment[m][0]) + 1))
                            l_type.append(t_field_type_isnull_key_comment[m][1] + " " * (b - len(t_field_type_isnull_key_comment[m][1]) + 1))
                            l_isnull.append(t_field_type_isnull_key_comment[m][2] + " " * (c - len(t_field_type_isnull_key_comment[m][2]) + 8))
                            l_isKey.append(t_field_type_isnull_key_comment[m][3] + " " * (d - len(t_field_type_isnull_key_comment[m][3]) + 1))
                            l_comment.append(t_field_type_isnull_key_comment[m][4] + " " * (e - len(t_field_type_isnull_key_comment[m][4]) + 1))
            else:
                # 所有字段
                for i in t_field_type_isnull_key_comment:
                    l_field.append(i[0] + " " * (a - len(i[0]) + 1))
                    l_type.append(i[1] + " " * (b - len(i[1]) + 1))
                    l_isnull.append(i[2] + " " * (c - len(i[2]) + 8))
                    l_isKey.append(i[3] + " " * (d - len(i[3]) + 1))
                    l_comment.append(i[4] + " " * (e - len(i[4])))

            # 只输出找到字段的表
            if len(l_field) != 0:
                print("- - " * 50)
                Color_PO.consoleColor("31", "36",
                                      "[" + t_table_comment[0][0] + " (" + t_table_comment[0][1] + ") - " + str(
                                          len(t_field_type_isnull_key_comment)) + "个字段]", "")
                print("字段名" + " " * (a - 4), "数据类型" + " " * (b - 6), "允许空值" + " " * (c + 1), "主键" + " " * (d - 2), "字段说明")
                for i in range(len(l_field)):
                    print(l_field[i], l_type[i], l_isnull[i], l_isKey[i], l_comment[i])

            l_field = []
            l_type = []
            l_isKey = []
            l_isnull = []
            l_comment = []
        else:
            Color_PO.consoleColor("31", "31", "[ERROR], 没有找到'" + varTable + "'表!]", "")
    def dbDesc(self, *args):
        ''' 查看数据库表结构（字段、类型、DDL）
        第1个参数：表名或表头*（通配符*）
        第2个参数：字段名（区分大小写），指定查看的字段名，多个字段名用逗号分隔，不支持通配符*
        '''

        if len(args) == 0:
            # 1, 所有表结构(ok)
            t_tables = self.execQuery('SELECT TABLE_NAME FROM information_schema.`TABLES` WHERE table_type = "BASE TABLE" AND table_schema = "%s"' % self.varDB)
            for t in range(len(t_tables)):
                self._dbDesc_search(t_tables[t][0])
            Color_PO.consoleColor("31", "31", "\n[已完成], 当前数据库 " + self.varDB + " 共有 " + str(len(t_tables)) + " 张表。 ", "")

        elif len(args) == 1:
            varTable = args[0]
            if "%" not in varTable:
                # 2, 单表结构（ok）
                self._dbDesc_search(varTable)
            elif "%" in varTable:
                # 3, 带通配符表结构（ok）
                t_tables = self.execQuery('select table_name from information_schema.`TABLES` where table_type = "BASE TABLE" AND table_schema="%s" and table_name like "%s"' % (self.varDB, varTable))
                if len(t_tables) != 0:
                    for t in range(len(t_tables)):
                        self._dbDesc_search(t_tables[t][0])
                else:
                    Color_PO.consoleColor("31", "31", "[ERROR], 没有找到'" + str(varTable) + "'前缀的表!", "")

        elif len(args) == 2:
            varTable = args[0]
            var_l_field = args[1]
            if varTable == "*":
                # 6, 所有表结构的可选字段(只输出找到字段的表)
                t_tables = self.execQuery('SELECT TABLE_NAME FROM information_schema.`TABLES` WHERE table_type = "BASE TABLE" AND table_schema = "%s"' % self.varDB)
                for t in range(len(t_tables)):
                    self._dbDesc_search(t_tables[t][0], var_l_field)
            elif "%" not in varTable:
                # 4, 单表结构可选字段（ok）
                self._dbDesc_search(varTable, var_l_field)
            elif "%" in varTable:
                # 5, 带通配符表结构可选字段（ok）
                t_tables = self.execQuery('select table_name from information_schema.`TABLES` where table_type = "BASE TABLE" AND table_schema="%s" and table_name like "%s"' % (self.varDB, varTable))
                if len(t_tables) != 0:
                    for t in range(len(t_tables)):
                        self._dbDesc_search(t_tables[t][0], var_l_field)
                else:
                    Color_PO.consoleColor("31", "31", "[ERROR], 没有找到'" + str(varTable) + "'前缀的表!", "")


    def _dbRecord_search(self, varDB, varTable, varType, varValue):

        '''dbRecord函数中子查询'''

        # mysql关键字和保留字，涉及的关键字将不处理（谨慎！）
        l_keyword = ['desc', 'limit', 'key', 'group', 'usage']

        l_field = []
        l_fieldComment = []

        # 表注释
        t_comment = self.execQuery(
            'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
            varDB, varTable))
        # print(t_comment)  # (('系统用户详情信息表 ',),)

        # 字段，类型，字段注释
        t_field_type = self.execQuery(
            'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (
            varDB, varTable))
        # print(t_field_type)  # (('userNo', 'varchar(50)'))

        # 过滤掉不符合类型的字段
        for j in t_field_type:
            if varType in j[1]:
                l_field.append(j[0])
                l_fieldComment.append(j[2])
        # print(l_field)  # ['userNo', 'userName', 'cardNo', 'email', 'mobile', 'shortName']
        # print(l_fieldComment)  # ['用户工号', '用户姓名', '证件号码', '邮箱', '手机号', '姓名首字母缩写（如张三：zs）']

        varSign = 0
        for i in range(len(l_field)):
            # 过滤mysql关键字
            for j in range(len(l_keyword)):
                if l_field[i] == l_keyword[j]:
                    varSign = 1

            if varSign == 0 :
                t_record = self.execQuery('select * from `%s` where %s LIKE "%s" ' % (varTable, l_field[i], varValue))
                if len(t_record) != 0:
                    print("- - " * 50)
                    Color_PO.consoleColor("31", "36",
                                          "[" + self.varDB + "." + varTable + "(" + str(t_comment[0][0]) + ")." +
                                          l_field[i] + "(" + str(l_fieldComment[i]) + ")]", "")
                    for j in range(len(t_record)):
                        print(str(t_record[j]).encode('gbk', 'ignore').decode('gbk'))
            else:
                Color_PO.consoleColor("31", "33", "[warning]，字段'" + str(l_field[i]) + "'是关键字, 不处理！", "")
                varSign = 0
        l_fields = []
        l_fieldComment = []
    def dbRecord(self, varTable, varType, varValue):
        '''
        # 2, 搜索表记录
        # 参数1：varTable = 表名（*表示所有的表）
        # 参数2：varType = 数据类型(char,int,double,timestamp)
        # 参数3：varValue = 值 (支持%模糊查询，如 %yy%)
        '''
        # dbRecord('*','char', u'%yoy%')  # 模糊搜索所有表中带yoy的char类型。
        # dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
        # dbRecord('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。
        # dbRecord('myclass','char', 'yoyo')

        if varType in "float,money,int,nchar,nvarchar,datetime,timestamp":
            if "*" in varTable:
                t_tables = self.execQuery('SELECT TABLE_NAME FROM information_schema. TABLES WHERE table_type = "BASE TABLE" AND table_schema ="%s" ' % (self.varDB))
                # print(t_table)  # (('af_preoperative_counseling_detail',), ('af_preoperative_counseling_info',))

                if len(t_tables) != 0:
                    for t in range(len(t_tables)):
                        self._dbRecord_search(self.varDB, t_tables[t][0], varType, varValue)
                else:
                    Color_PO.consoleColor("31", "31", "[ERROR], 没有找到 " + varTable.split("*")[0] + " 前缀的表!", "")
            elif "*" not in varTable:
                self._dbRecord_search(self.varDB, varTable, varType, varValue)

    def dbCreateDate(self, *args):

        '''
        3，查表的创建时间及时间区间
        无参：查看所有表的创建时间
        一个参数：表名
        二个参数：第一个是时间前后，如 before指定日期之前创建、after指定日期之后创建，第二个是日期
        '''
        # Mysql_PO.dbCreateDate()   # 查看所有表的创建时间
        # Mysql_PO.dbCreateDate('app_code')   # 查看book表创建时间
        # Mysql_PO.dbCreateDate('fact*')   # 查看所有b开头表的创建时间，通配符*
        # Mysql_PO.dbCreateDate('after', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
        # Mysql_PO.dbCreateDate('>', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
        # Mysql_PO.dbCreateDate('before', "2019-04-10")  # 显示所有在2019-12-08之前创建的表
        # Mysql_PO.dbCreateDate('<', "2019-02-18")  # 显示所有在2019-12-08之前创建的表
        if len(args) == 0:
            try:
                tbl = self.execQuery('select table_name,create_time from information_schema.`TABLES` where table_schema="%s"' % (self.varDB))
                print("\n" + self.varDB + "下 " + str(len(tbl)) + " 张表的创建时间" + "\n" + "-" * 60)
                for r in range(len(tbl)):
                    print(str(tbl[r][1]) + " => " + tbl[r][0])
            except:
                print("[warning , 数据库为空!]")
        elif len(args) == 1:
            if "*" in args[0]:
                varTable = args[0].split("*")[0] + "%"  # t_store_%
                tbl = self.execQuery('select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and table_name like "%s" ' % (self.varDB, varTable))
                print("\n" + self.varDB + "." + args[0] + " 表的创建时间" + "\n" + "-" * 60)
                for r in range(len(tbl)):
                    print(str(tbl[r][1]) + " => " + tbl[r][0])
            else:
                try:
                    tbl = self.execQuery('select create_time from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (self.varDB, args[0]))
                    print("\n" + self.varDB + "." + args[0] + " 表的创建时间" + "\n" + "-" * 60)
                    print(str(tbl[0]) + " => " + args[0])
                except:
                    print("[errorrrrrrr , " + args[0] + "表不存在!]")
        elif len(args) == 2:
            if args[0] == "after" or args[0] == ">":
                tbl = self.execQuery('select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time>"%s"' % (self.varDB, args[1]))
                print("\n" + self.varDB + "下 " + str(len(tbl)) + " 张表在 " + str(args[1]) + " 之后被创建" + "\n" + "-" * 60)
                for r in range(len(tbl)):
                    print(str(tbl[r][1]) + " => " + tbl[r][0])
            elif args[0] == "before" or args[0] == "<":
                tbl = self.execQuery('select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time<"%s"' % (self.varDB, args[1]))
                print("\n" + self.varDB + "下 " + str(len(tbl)) + " 张表在 " + str(args[1]) + " 之前被创建" + "\n" + "-" * 60)
                for r in range(len(tbl)):
                    print(str(tbl[r][1]) + " => " + (tbl[r][0]))
            else:
                print("[errorrrrrrr , 参数1必须是 after 或 before ]")
        else:
            print("[errorrrrrrr , 参数溢出！]")


    def db2xlsx(self, sql, xlsxFile):

        '''
        4.1 使用pandas将数据库表导出excel
        :param sql:
        :param xlsxFile:
        :return:
                # Mysql_PO.db2xlsx("select * from sys_menu", "d:\\111.xlsx")
        '''

        try:
            df = pd.read_sql(sql=sql, con=self.getPymysqlEngine())
            df.to_excel(xlsxFile)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) +" row" )

    def db2html(self, sql, htmlFile):

        '''
        4.2 使用pandas将数据库表导出html
        :param sql:
        :param toHtml:
        :return:
                # Mysql_PO.db2xlsx("select * from sys_menu", "d:\\index1.html")
                参考：https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_html.html
                css加载，https://blog.csdn.net/qq_38316655/article/details/104663077
                颜色，https://www.jianshu.com/p/946481cd288a
                https://www.jianshu.com/p/946481cd288a
        '''

        try:
            df = pd.read_sql(sql=sql, con=self.getPymysqlEngine())
            df.to_html(htmlFile, col_space=100, na_rep="0")
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def xlsx2db(self, varExcelFile, varTable, usecols=None, nrows=None, skiprows=None, dtype=None, parse_dates=None, date_parser=None, converters=None, sheet_name=None, index=False):

        '''
        4.4 excel导入数据库表(覆盖)
        :return:

        参数参考：https://zhuanlan.zhihu.com/p/96203752
        '''

        try:
            df = pd.read_excel(varExcelFile, usecols=usecols, nrows=usecols, skiprows=skiprows, dtype=dtype, parse_dates=parse_dates, date_parser=date_parser, converters=converters, sheet_name=sheet_name)
            df.to_sql(varTable, con=self.getMysqldbEngine(), if_exists='replace', index=index)
        except Exception as e:
            print(e)

    def dbDesc2xlsx(self, varFileName):

        '''
        4.5 所有表结构导出excel(覆盖)
        :param varFileName:
        :return:
        '''

        listSub = []
        listMain = []
        dict1 = {}

        try:
            tblName = self.execQuery('select TABLE_NAME,TABLE_COMMENT from information_schema.`TABLES` where table_schema="%s" ' % self.varDB)
            # print(tblName)
            listSub.append("表名")
            listSub.append("表说明")
            listSub.append("名称")
            listSub.append("数据类型(长度)")
            listSub.append("允许空值")
            listSub.append("主键")
            listSub.append("默认值")
            listSub.append("说明")
            dict1[1] = listSub
            for k in range(len(tblName)):
                tblFields = self.execQuery('select column_name,column_type,is_nullable,column_key,column_default,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (self.varDB, tblName[k][0]))
                for i in range(len(tblFields)):
                    list3 = list(tblName[k]) + list(tblFields[i])
                    listMain.append(list3)
            for i in range(len(listMain)):
                dict1[i+2] = listMain[i]
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")
        NewexcelPO(varFileName)
        Openpyxl_PO = OpenpyxlPO(varFileName)
        Openpyxl_PO.setRowValue(dict1)
        Openpyxl_PO.save()


    def getTableField(self, varTable):

        ''' 5, 获取单个表的所有字段 '''
        # Mysql_PO.getTableField('HrCover')

        l_field = []
        try:
            t_table = self.execQuery('select column_name from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (self.varDB, varTable))

            for i in range(len(t_table)):
                l_field.append(t_table[i][0])
            return l_field

        except Exception as e:
            print(e, ",很抱歉，出现异常您搜索的<" + varTable + ">不存在！")


if __name__ == '__main__':


    # 238 sass高血压（测试） ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    Mysql_PO = MysqlPO("192.168.0.238", "root", "ZAQ!2wsx", "saasusertest", 3306)
    # t_userNo = Mysql_PO.execQuery('select id from sys_user_detail where userNo="%s"' % ("16766667777"))
    # print(t_userNo[0][0])  # 278


    # # 238 erp (测试) ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # Mysql_PO = MysqlPO("192.168.0.238", "root", "ZAQ!2wsx", "crmtest", 3306)
    # crm小程序清空账号权限
    # Mysql_PO.execQuery("update user SET VX_MARK='', IMEI='', MODEL='',PLATFORM='', NOT_LOGIN=0, LIMIT_LOGIN=0 ")
    # l_result = Mysql_PO.execQuery('select USER_NAME from user where USER_PRIV_NO=%s ' % (999))
    # print(l_result)
    # print(l_result[0][0])

    # 234 epd 招远防疫 (测试) ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # Mysql_PO = MysqlPO("192.168.0.231", "root", "Zy123456", "epidemic_center", 3306)  # 开发
    # Mysql_PO = MysqlPO("192.168.0.234", "root", "123456", "epd", 3306)   # 测试

    # # 211_zentao ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # Mysql_PO = MysqlPO("192.168.0.211", "readonly", "benetech123", "zentaoep", 3306) # 测试

    # # 195 ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bitest", 3306)  # 测试环境

    # # 64 ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bitest", 3306)  # 测试环境



    # *****************************************************************************************************************************
    # *****************************************************************************************************************************

    # print("1 查看数据库表结构（字段名、数据类型、主键、允许空值、字段说明）".center(100, "-"))
    # Mysql_PO.dbDesc()  # 1，所有表结构
    # Mysql_PO.dbDesc('sys_user_detail')  # 2，单表结构
    # Mysql_PO.dbDesc('sys_user_%')  # 3，带通配符表结构
    # Mysql_PO.dbDesc('sys_user_detail', ['id', 'sex', 'title'])  # 4,单表结构的可选字段
    # Mysql_PO.dbDesc('sys_user_%', [ 'sex'])  # 5，带通配符表结构的可选字段(只输出找到字段的表)
    # Mysql_PO.dbDesc("*", ['sex', 'title', 'org_name'])  # 6，所有表结构的可选字段(只输出找到字段的表)

    # print("2，搜索表记录".center(100, "-"))
    # Mysql_PO.dbRecord('sys_user_detail', 'varchar', '16766667777')
    # Mysql_PO.dbRecord('sys_user_detail', 'varchar', '1676666%')
    # Mysql_PO.dbRecord('*', 'varchar', '16766667%')
    # Mysql_PO.dbRecord('sys_user', 'char', '%金%')  # 搜索user表中内容包含金丽娜的char类型记录。
    # Mysql_PO.dbRecord('*', 'varchar', u'%招远疫情防控公告123456%')   # 搜索所有表中带金丽娜的char类型记录。
    # Mysql_PO.dbRecord('*', 'datetime', '2010%')  # 模糊搜索所有表中日期类型为datetime的2019-04-12 15:13:23记录。
    # Mysql_PO.dbRecord('sys_user_detail', 'datetime', '2015-04-13%')  # 模糊搜索所有表中日期类型为datetime的2019-04-12 15:13:23记录。

    # print("3，查表的创建时间及时间区间".center(100, "-"))
    # Mysql_PO.dbCreateDate()   # 查看所有表的创建时间
    # Mysql_PO.dbCreateDate('test1')   # 查看book表创建时间
    # Mysql_PO.dbCreateDate('test*')   # 查看所有b开头表的创建时间，通配符*
    # Mysql_PO.dbCreateDate('after', '2021-11-14')  # 查看所有在2019-02-18之后创建的表
    # Mysql_PO.dbCreateDate('>', '2021-11-14')  # 查看所有在2019-02-18之后创建的表
    # Mysql_PO.dbCreateDate('before', "2021-11-14")  # 显示所有在2019-12-08之前创建的表
    # Mysql_PO.dbCreateDate('<', "2021-11-14")  # 显示所有在2019-12-08之前创建的表

    # print("4.1，数据库表导出excel".center(100, "-"))
    # Mysql_PO.db2xlsx("select * from ba_area", "data/ba_area.xlsx")

    # print("4.2，数据库表导出html".center(100, "-"))
    # Mysql_PO.db2html("select * from sys_user_detail", "d:\\sys_user_detail.html")
    # Mysql_PO.db2html("select * from sys_user_detail where userName='dc'", "/Users/linghuchong/Desktop/mac/sys_user_detail.html")

    # print("4.4 excel导入数据库表".center(100, "-"))
    # Mysql_PO.xlsx2db("data/testcase2.xlsx", "testcase2", sheet_name="case")
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", usecols=eval("range(4)"), nrows=6, dtype={'No.': str, '金额': float},parse_dates=['isRun'], date_parser=lambda x: pd.to_datetime(x, format='%Y%m'))  # 读取表格中前3列、前6行数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", usecols=eval("range(4)"), nrows=6, converters={'isRun': lambda x: pd.to_datetime(x, format='%Y%m')})  # 读取表格中前3列、前6行数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", eval("range(3)"), 6, skiprows=range(1, 100, 2), sheet_name="case")  # 读取表格中前3列、前6行数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", eval("range(3)"), 6, range(1, 100, 2))  # 读取表格中前3列、前6行数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", "A,C,E", None)  # 读取表格中A,C,E3列数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", "A:F", None)  # 读取表格中A-F 列数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", [0,3,4,5], None)  # 读取表格中4列数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", ['interURL','一级属性'], None)  # 读取表格中['interURL','一级属性']列数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", lambda x: x in ['班级', 'interURL', '语文'], None)  # 读取表格中符合（存在）['班级', 'interURL', '语文']列数据，并写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", lambda x: x in ['班级', 'interURL', '语文'], None, sheet_name="case")  # 读取表格中符合（存在）['班级', 'interURL', '语文']列数据，并写入数据库表


    # print("4.5 将所有表结构导出到excel(覆盖)".center(100, "-"))
    # Mysql_PO.dbDesc2xlsx("d:\\sassDesc.xlsx")
    # Mysql_PO.dbDesc2xlsx("/Users/linghuchong/Desktop/mac/sassDesc.xlsx")


    # print("5 将所有表结构导出到excel(覆盖)".center(100, "-"))
    print(Mysql_PO.getTableField('test_interface'))
