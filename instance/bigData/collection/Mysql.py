# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Data       : 2024-3-4
# Description: MysqlPO对象层
# ***************************************************************


"""
pandas引擎（pymysql）  getEngine_pymysql()
pandas引擎（mysqldb）  getEngine_mysqldb()

1，查看表结构  dbDesc()
2，搜索记录  dbRecord('*', 'money', '%34.5%')
3，查询表创建时间  dbCreateDate()

4.1，将数据库表查询结果导出excel  sql2xlsx()
4.2，将数据库表查询结果导出csv  sql2csv()
4.3，将数据库表查询结果导出html  sql2html()
4.4，将数据库表结构导出excel  dbDesc2xlsx()
4.5，将数据库表导出html  Mysql_PO.db2html("erp_开发计划总揽_2022-11-12", "sys_area", "d://123.html",False)

5 获取单个表的所有字段 getTableField(self, varTable)

6 expain SQL语句的执行计划

7 获取mysql关键字列表 ？

"""

import sys, pymysql

pymysql.install_as_MySQLdb()
import MySQLdb
import pandas as pd
from PO.ExcelPO import *
from sqlalchemy import create_engine,text
from bs4 import BeautifulSoup


class Mysql:

    def __init__(self, varHost, varUser, varPassword, varDB, varPort=3336):

        self.host = varHost
        self.user = varUser
        self.password = varPassword
        self.db = varDB
        self.port = varPort
        self.conn = MySQLdb.connect(
            host=varHost,
            user=varUser,
            passwd=varPassword,
            db=varDB,
            port=int(varPort),
            use_unicode=True,
        )
        self.cur = self.conn.cursor()
        if not self.cur:
            raise (NameError, "error，创建游标失败！")


    def getEngine(self):
        # mysql 引擎
        return create_engine("mysql://" + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db)

    def getEngine_pymysql(self):
        # pymysql 引擎
        return create_engine("mysql+pymysql://" + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db)
        # return create_engine('mysql+pymysql://' + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db + "?charset=utf8")

    def getEngine_mysqlconnector(self):
        # mysqlconnector 引擎
        return create_engine("mysql+mysqlconnector://" + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db)

    def getEngine_mysqldb(self):
        # mysqldb 引擎
        return create_engine("mysql+mysqldb://" + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db)

    def getEngine_oursql(self):
        # oursql 引擎
        return create_engine("mysql+oursql://" + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db)


    def execQuery(self, sql):

        """查询sql"""

        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            self.conn.commit()
            return result
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')


    def execute(self, sql):

        '''
        执行sql （insert，update）
        :param sql:
        :return:
        '''

        try:
            self.cur.execute(sql)
            self.conn.commit()
            return "ok"
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            # print(repr(e))  # OperationalError('table hh already exists')
            return str(e)


    def execCall(self, varProcedure, varList = []):

        # 执行存储过程

        self.cur.callproc(varProcedure, varList)
        result = self.cur.fetchone()

        self.conn.commit()
        self.cur.close()
        self.conn.close()

        return result

    def close(self):
        self.cur.close()
        self.conn.close()


    def sql2xlsx(self, varSql, varXlsx, index=True):

        """
        4.1，将数据库表查询结果导出excel
        # Mysql_PO.db2xlsx("select * from sys_menu", "d:\\111.xlsx")
        """

        df = pd.read_sql(sql=varSql, con=self.getEngine_pymysql())
        df.to_excel(varXlsx, index=index)

    def sql2csv(self, varSql, varCSV, index=True):

        """
        4.1，将数据库表查询结果导出excel
        # Mysql_PO.db2csv("select * from sys_menu", "d:\\111.csv")
        """

        df = pd.read_sql(sql=varSql, con=self.getEngine_pymysql())
        df.to_csv(varCSV, encoding="gbk", index=index)

    def sql2html(self, sql, htmlFile, index=True):

        """
        4.3，将数据库表查询结果导出html
                # Mysql_PO.db2xlsx("select * from sys_menu", "d:\\index1.html")
                参考：https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_html.html
                css加载，https://blog.csdn.net/qq_38316655/article/details/104663077
                颜色，https://www.jianshu.com/p/946481cd288a
                https://www.jianshu.com/p/946481cd288a
        """

        df = pd.read_sql(sql=sql, con=self.getEngine_pymysql())
        df.to_html(htmlFile, col_space=100, na_rep="0", index=index)


    def db2html(self, varTitle, varTable, varFile, index=True):

        """
        4.5 将数据库表导出html
        # db2html("erp_开发计划总揽_","2022-11-12","12345")
        # db2html("erp_开发计划总揽_",str(Time_PO.getDateTime()),"12345")
        """

        df = pd.read_sql(
            sql="select * from `%s`" % varTable, con=self.getEngine_pymysql()
        )
        pd.set_option("colheader_justify", "center")  # 对其方式居中
        html = (
            """<html><head><title>"""
            + varTitle
            + """</title></head>
        <body><b><caption>"""
            + varTitle
            + """</caption></b><br><br>{table}</body></html>"""
        )
        style = """<style>.mystyle {font-size: 11pt; font-family: Arial;    border-collapse: collapse;     border: 1px solid silver;}.mystyle td, th {    padding: 5px;}.mystyle tr:nth-child(even) {    background: #E0E0E0;}.mystyle tr:hover {    background: silver;    cursor: pointer;}</style>"""

        # File_PO.createFolder("report")
        with open(varFile, "w") as f:
            f.write(
                style
                + html.format(
                    table=df.to_html(classes="mystyle", col_space=100, index=index)
                )
            )

        # # 优化report.html, 去掉None、修改颜色
        # html_text = BeautifulSoup(open(rptNameDate), features='html.parser')
        # tf = open(rptNameDate, 'w', encoding='utf-8')
        # tf.write(str(html_text))
        # tf.close()





if __name__ == "__main__":

    # todo OA
    Mysql_PO = Mysql("192.168.0.65", "ceshi", "123456", "TD_OA", 3336)
    engine = Mysql_PO.getEngine_mysqldb()
    df = pd.read_sql(text("select * from user"), con=engine.connect())
    print(df)



    # # 创建users表，没有设置id主键
    # Mysql_PO.execute("CREATE TABLE users(id int not null,name varchar(10),age int(4))")
    # # 在users表上，创建id主键
    # Mysql_PO.execute("alter table users add primary key(id)")
    #
    # # 创建teacher表，设置id主键
    # Mysql_PO.execute("CREATE TABLE teather(id int auto_increment primary key, name varchar(10),age int(4))")

    # # 删除teacher表的id主键(需要注意的是主键如果设置了自动递增，需要先将自动递增去掉，再删除主键。)
    # Mysql_PO.execute("alter table teather change id id int not null")  # 取消id的自动递增
    # Mysql_PO.execute("alter table teather DROP PRIMARY KEY")  # 取消所有主键


    # # 创建haha表，如果不存在的话。
    # Mysql_PO.execute("CREATE TABLE if not exists haha(id int auto_increment primary key, name varchar(10),age int(4))")





    # Mysql_PO.execute("INSERT INTO haha (name, age) VALUES ('john', 12)")


    # t_userNo = Mysql_PO.execQuery('select * from sys_user_detail where userNo="%s"' % ("16766667777"))
    # print(t_userNo)
    # print(t_userNo[0][0])  # 278
    #
    # t_userNo = Mysql_PO.execQuery('select * from sys_user_detail where id="%s"' % ("277"))
    # print(t_userNo)
    #
    # Mysql_PO.close()

    # # # 238 erp (测试) ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy123456", "crmtest", 3306)
    # # crm小程序清空账号权限
    # # Mysql_PO.execQuery("update user SET VX_MARK='', IMEI='', MODEL='',PLATFORM='', NOT_LOGIN=0, LIMIT_LOGIN=0 ")
    # l_result = Mysql_PO.execQuery('select USER_NAME from user where USER_PRIV_NO=%s ' % (999))
    # print(l_result)  # (('测试',), ('系统管理员',))
    # print(l_result[0][0])  # 测试

    # # 244 erp (预发布) ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # Mysql_PO = MysqlPO("192.168.0.244", "root", "ZAQ!2wsx", "crm", 3306)

    # 234 epd 招远防疫 (测试) ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # Mysql_PO = MysqlPO("192.168.0.231", "root", "Zy123456", "epidemic_center", 3306)  # 开发
    # Mysql_PO = MysqlPO("192.168.0.234", "root", "123456", "epd", 3306)   # 测试

    # # 211_zentao ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # Mysql_PO = MysqlPO("192.168.0.211", "readonly", "benetech123", "zentaoep", 3306) # 测试

    # # 195 ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bitest", 3306)  # 测试环境

    # *****************************************************************************************************************************
    # *****************************************************************************************************************************

    # print("1 查看数据库表结构（字段名、数据类型、主键、允许空值、字段说明）".center(100, "-"))
    # Mysql_PO.dbDesc()  # 1，所有表结构
    # Mysql_PO.dbDesc('sys_user_detail')  # 2，单表结构
    # Mysql_PO.dbDesc('sys_user_%')  # 3，带通配符表结构
    # Mysql_PO.dbDesc('sys_user_detail', ['id', 'sex', 'title'])  # 4,单表结构的可选字段
    # Mysql_PO.dbDesc('sys_user_%', ['id'])  # 5，带通配符表结构的可选字段(只输出找到字段的表)
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
    # Mysql_PO.dbCreateDate('task*')   # 查看所有b开头表的创建时间，通配符*
    # Mysql_PO.dbCreateDate('after', '2022-10-1')  # 查看所有在2019-02-18之后创建的表
    # Mysql_PO.dbCreateDate('>', '2021-11-14')  # 查看所有在2019-02-18之后创建的表
    # Mysql_PO.dbCreateDate('before', "2022-10-1")  # 显示所有在2019-12-08之前创建的表
    # Mysql_PO.dbCreateDate('<', "2021-11-14")  # 显示所有在2019-12-08之前创建的表

    # print("4.1，将数据库表查询结果导出excel".center(100, "-"))
    # Mysql_PO.sql2xlsx("select * from sys_area", "d:\\sys_area.xlsx")
    # Mysql_PO.sql2xlsx("select * from sys_area", "d:\\sys_area.xlsx", False)

    # print("4.2，将数据库表查询结果导出csv".center(100, "-"))
    # Mysql_PO.sql2csv("select * from sys_area", "d:\\sys_user_detail.csv")
    # Mysql_PO.sql2csv("select * from sys_area", "d:\\sys_user_detail.cav", False)

    # print("4.3，将数据库表查询结果导出html".center(100, "-"))
    # Mysql_PO.sql2html("select * from sys_area", "d:\\sys_user_detail.html")
    # Mysql_PO.sql2html("select * from sys_area", "d:\\sys_user_detail.html", False)

    # print("4.4 将数据库表查询结果导出htmll".center(100, "-"))
    # Mysql_PO.dbDesc2xlsx("d:\\crmtest.xlsx")
    # Mysql_PO.dbDesc2xlsx("/Users/linghuchong/Desktop/mac/sassDesc.xlsx")

    # print("4.5 将数据库表导出html".center(100, "-"))
    # Mysql_PO.db2html("erp_开发计划总揽_2022-11-12", "sys_area", "d://123.html")
    # Mysql_PO.db2html("erp_开发计划总揽_2022-11-12", "sys_area", "d://123.html",False)
    # Mysql_PO.db2html("erp_开发计划总揽_2022-11-12", "sys_area", "d://11/123.html", False)

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

    # print("5 将所有表结构导出到excel(覆盖)".center(100, "-"))
    # print(Mysql_PO.getTableField('test_interface'))

    # print("6 expain SQL语句的执行计划".center(100, "-"))
    # Mysql_PO.explainSingle("select sum(双A客户实际拜访人数) from(SELECT count(DISTINCT customer_id) 双A客户实际拜访人数 from t_visit WHERE user_id=84 and double_a_mark=1 and state=3 and valid_status=1 and created_at>='2022-06-01' and  created_at<='2022-06-30 23:59:59' GROUP BY  customer_id  HAVING(count(*)>=6))双A客户实际拜访人数")

    # print("6.2 expain SQL语句的执行计划文件".center(100, "-"))
    # Mysql_PO.explainMore("./data/i_erp_reportField_case.xlsx", "拜访分析报表", 4, 5, 2)


