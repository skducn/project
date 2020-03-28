# coding=utf-8
#***************************************************************
# Author     : John
# Revise on : 2017-11-16
# Description: DatabasePO对象层，定义数据库封装对象
#***************************************************************

from selenium.webdriver.common.by import By
import json, MySQLdb

# 继承BasePage类,操作登录页面元素

class DatabasePO(object):

    def __init__(self, dimHost, dimUser, dimPasswd, dimDatabase):
        self.varHost = dimHost
        self.varUser = dimUser
        self.varPasswd = dimPasswd
        self.varDatabase = dimDatabase
        self.conn = MySQLdb.connect(host=self.varHost, user=self.varUser, passwd=self.varPasswd, db=self.varDatabase, port=3306, use_unicode=True)
        self.cur = self.conn.cursor()
        self.cur.execute('SET NAMES utf8;')
        self.conn.set_character_set('utf8')
        self.cur.execute('show tables')

    def showStructureList(self, dimTable, dimFields):
        # 功能：显示数据库表结构 ， // 数据库 > 表名（表comment）> 字段数 > 记录数 > 字段列表（字段名、类型、DDL） ,注意：字段名区分大小写
        # 参数1 = 表 (可选1、留空表示遍历所有的表；可选2、指定具体的表或指定前缀名的表，如tt_*)
        # 参数2 = 字段 (可选1、留空表示遍历所有的字段；可选2、指定1个或多个字段用逗号分割)
        # Database_PO.showStructureList("", "")
        # Database_PO.showStructureList("tt_user*", "")
        # Database_PO.showStructureList("tt_user_login", "")
        # Database_PO.showStructureList("tt_user_login", "name")
        # Database_PO.showStructureList("tt_user_login", "name,user_id")
        list0 = []
        list1 = []
        list2 = []
        x = y = tblFieldcount = 0
        if dimTable != "":
            if "*" in dimTable:
                varTable2 = dimTable.split("*")[0] + "%"  # t_store_%
                m = self.cur.execute(
                    'select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (
                    self.varDatabase, varTable2))
                if m != 0:
                    t0 = self.cur.fetchall()
                    print u' 本次影响' + str(len(t0)) + '张表'
                    for p in range(len(t0)):  # 共有len(t0)张表
                        varTable = t0[p][0]
                        # 遍历指定的表
                        n = self.cur.execute(
                            'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                                self.varDatabase, varTable))
                        if n != 0:
                            t1 = self.cur.fetchone()
                            tblDDL = t1[0]
                            self.cur.execute(
                                'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (
                                    self.varDatabase, varTable))
                            t2 = self.cur.fetchall()
                            self.cur.execute('select count(*) from %s' % (varTable))
                            t3 = self.cur.fetchall()
                            if dimFields == "":
                                print "\n[" + self.varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(
                                    len(t2)) + u"字段 > " + str(t3[0][0]) + u"记录]"
                                print "-" * 100
                                for i in t2:
                                    if len(i[0]) > x: x = len(i[0])
                                    if len(i[1]) > y: y = len(i[1])
                                    tblFieldcount = tblFieldcount + 1
                                for i in t2:
                                    list0.append(i[0] + " " * (x - len(i[0]) + 10))
                                    list1.append(i[1] + " " * (y - len(i[1]) + 10))
                                    ii = i[2].replace("\r\n", ",")
                                    list2.append(ii.replace("  ", ""))
                                for i in range(tblFieldcount):
                                    print list0[i], list1[i], list2[i]
                            else:
                                print "\n[" + self.varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(
                                    len(dimFields.split(","))) + u"字段 > " + str(t3[0][0]) + u"记录]"
                                print "-" * 100
                                for i in t2:
                                    if len(i[0]) > x: x = len(i[0])
                                    if len(i[1]) > y: y = len(i[1])
                                for i in t2:
                                    for j in range(len(dimFields.split(","))):
                                        if i[0] == dimFields.split(",")[j]:
                                            list0.append(i[0] + " " * (x - len(i[0]) + 10))
                                            list1.append(i[1] + " " * (y - len(i[1]) + 10))
                                            ii = i[2].replace("\r\n", ",")
                                            list2.append(ii.replace("  ", ""))
                                for i in range(len(dimFields.split(","))):
                                    try:
                                        print list0[i], list1[i], list2[i]
                                    except:
                                        print "errorrrrrrrrrr , 参数2的部分字段不存在哦！"
                        list0 = []
                        list1 = []
                        list2 = []
                        tblFieldcount = 0
                else:
                    print "errorrrrrrrrrr , 数据库(" + self.varDatabase + ")中没有找到 " + dimTable.split("*")[0] + " 前缀的表!"
            elif "*" not in dimTable:
                # 遍历指定的表
                n = self.cur.execute(
                    'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                        self.varDatabase, dimTable))
                if n != 0:
                    t1 = self.cur.fetchone()
                    tblDDL = t1[0]
                    self.cur.execute(
                        'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (
                            self.varDatabase, dimTable))
                    t2 = self.cur.fetchall()
                    # print u'[本次影响' + str(len(t2)) + u'个字段]'
                    self.cur.execute('select count(*) from %s' % (dimTable))
                    t3 = self.cur.fetchall()
                    if dimFields == "":
                        print "\n[" + self.varDatabase + " > " + dimTable + "(" + tblDDL + ") > " + str(
                            len(t2)) + u"(字段) > " + str(t3[0][0]) + u"(记录)]"
                        print "-" * 100
                        for i in t2:
                            if len(i[0]) > x: x = len(i[0])
                            if len(i[1]) > y: y = len(i[1])
                            tblFieldcount = tblFieldcount + 1
                        for i in t2:
                            list0.append(i[0] + " " * (x - len(i[0]) + 1))
                            list1.append(i[1] + " " * (y - len(i[1]) + 1))
                            ii = i[2].replace("\r\n", ",")
                            list2.append(ii.replace("  ", ""))
                        for i in range(tblFieldcount):
                            # 字段 类型 DDL说明
                            print list0[i], list1[i], list2[i]
                    else:
                        print "\n[" + self.varDatabase + " > " + dimTable + "(" + tblDDL + ") > " + str(
                            len(dimFields.split(","))) + u"字段 > " + str(t3[0][0]) + u"记录]"
                        print "-" * 100
                        for i in t2:
                            if len(i[0]) > x: x = len(i[0])
                            if len(i[1]) > y: y = len(i[1])
                        for i in t2:
                            for j in range(len(dimFields.split(","))):
                                if i[0] == dimFields.split(",")[j]:
                                    list0.append(i[0] + " " * (x - len(i[0]) + 1))
                                    list1.append(i[1] + " " * (y - len(i[1]) + 1))
                                    ii = i[2].replace("\r\n", ",")
                                    list2.append(ii.replace("  ", ""))
                        for i in range(len(dimFields.split(","))):
                            try:
                                print list0[i], list1[i], list2[i]
                            except:
                                print "errorrrrrrrrrr , 参数2的部分字段不存在哦！！！"
                else:
                    print "errorrrrrrrrrr , 数据库(" + self.varDatabase + ")中没有找到 " + dimTable + "表!"
        else:
            self.cur.execute(
                'select TABLE_NAME,TABLE_COMMENT from information_schema.`TABLES` where table_schema="%s" ' % self.varDatabase)
            tblname = self.cur.fetchall()
            for k in range(len(tblname)):
                self.cur.execute(
                    'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (
                        self.varDatabase, tblname[k][0]))
                t2 = self.cur.fetchall()
                self.cur.execute('select count(*) from %s' % (tblname[k][0]))
                t3 = self.cur.fetchall()
                print "\n[" + self.varDatabase + " > " + tblname[k][0] + "(" + tblname[k][1] + ") > " + str(
                    len(t2)) + u"字段 > " + str(t3[0][0]) + u"记录]"
                print "-" * 100
                for i in t2:
                    if len(i[0]) > x: x = len(i[0])
                    if len(i[1]) > y: y = len(i[1])
                    tblFieldcount = tblFieldcount + 1
                for i in t2:
                    list0.append(i[0] + " " * (x - len(i[0]) + 1))
                    list1.append(i[1] + " " * (y - len(i[1]) + 1))
                    list2.append(i[2])
                for i in range(tblFieldcount):
                    print list0[i], list1[i], list2[i]
                list0 = []
                list1 = []
                list2 = []
                tblFieldcount = 0

    def showCreateTime(self, dimTable, dimStatus, dimAfterTime):
        # 功能: 获取表的创建时间
        # 参数1 = 表(默认为空，搜索所有的表）
        # 参数2 = 指定日期前或后 （before表示指定日期之前创建、after表示指定日期之后创建）
        # 参数3 = 日期(不能为空)
        # Database_PO.showCreateTime("", "after", "2017-10-10")    如：2017-10-15 23:26:15 => tt_manage_user
        # Database_PO.showCreateTime("", "before", "2017-10-10")
        # Database_PO.showCreateTime("", "", "")  显示所有表创建时间
        print "-" * 100
        if self.varDatabase != "":
            try:
                if dimTable == "" and dimStatus == "":
                    self.cur.execute(
                        'select count(create_time) from information_schema.`TABLES` where table_schema="%s" ' % (
                            self.varDatabase))
                    t1 = self.cur.fetchall()
                    # print t1[0][0]  # 统计表数量
                    print "[" + self.varDatabase + " 中共有 " + str(t1[0][0]) + " 张表，各表的创建时间（升序）如下]"
                    self.cur.execute(
                        'select table_name,create_time from information_schema.`TABLES` where table_schema="%s" order by create_time' % (
                            self.varDatabase))
                    t3 = self.cur.fetchall()
                    for i in range(t1[0][0]):
                        print str(t3[i][1]) + " => " + t3[i][0]
                elif dimTable != "":
                    self.cur.execute(
                        'select create_time from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                            self.varDatabase, dimTable))
                    t3 = self.cur.fetchone()
                    print "[" + self.varDatabase + "." + dimTable + " 表的创建时间为 " + str(t3[0]) + "]"
                else:
                    if dimStatus == "after":
                        x = self.cur.execute(
                            'select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time>"%s"' % (
                                self.varDatabase, dimAfterTime))
                        t4 = self.cur.fetchall()
                        print "[" + self.varDatabase + " 中共有 " + str(x) + " 张表在 " + str(dimAfterTime) + " 之后被创建]"

                        for p in range(len(t4)):
                            print str(t4[p][1]) + " => " + t4[p][0]
                    elif dimStatus == "before":
                        x = self.cur.execute(
                            'select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time<"%s"' % (
                                self.varDatabase, dimAfterTime))
                        t4 = self.cur.fetchall()
                        print "[" + self.varDatabase + " 中共有 " + str(x) + " 张表在 " + str(dimAfterTime) + " 之前被创建]"

                        for p in range(len(t4)):
                            print str(t4[p][1]) + " => " + (t4[p][0])
                    else:
                        print "errorrrrrrrrrr, 表名不能为空！"
            except:
                print "errorrrrrrrrrr, 表名(" + self.varDatabase + "." + dimTable + ")不存在！"
        else:
            print "warning , 数据库不能为空！"

    def searchKeyword(self, varTable, varType, varValue):
        # 功能：模糊搜索关键字，遍历所有的表获取关键字的详细记录
        # 参数以此为表（*表示所有表）、数据类型、值
        # 参数1 = 表(*表示搜索所有的表）
        # 参数2 = 字段类型 （如：char、int、tinyint、double、timestamp）
        # 参数3 = 关键字(不能为空,*通配符)
        # Database_PO.searchKeyword("*", "char", "a123456")
        # Database_PO.searchKeyword("*", "timestamp", "2017-10-15 23:29:47")
        # Database_PO.searchKeyword("*", "datetime", "2017-10-15 19:45:54")
        # Database_PO.searchKeyword('*', u'char', u'%814子项目2%')
        list0 = []
        list1 = []
        x = y = tblFieldcount = varbat = 0
        if varType in 'int,char,tinyint,smallint,timestamp,varchar,double,datetime':

            m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
            t123 = self.cur.fetchall()

            if varTable == u'*':
                # 遍历所有表
                varbat = 1
                m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
                t0 = self.cur.fetchall()
                print u"共有 " + str(len(t0)) + u" 张表 ，全部遍历"

            elif u"*" in varTable:
                # 遍历部分表，如 *tt_% 遍历tt_开头的表 , Database_PO.searchKeyword(u"*tt_%", u"char", u"wang")
                varTable2 = varTable.split(u"*")[1]  # *t_store_%
                varbat = 1
                m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (self.varDatabase, varTable2))
                t0 = self.cur.fetchall()
                print u"共有 " + str(len(t123)) + u" 张表 ，遍历 " + str(len(t0)) + u" 张表 "

            elif u'#' in varTable:
                # 忽略表，如 '#rcd_order_detail_2'
                if u"|" in varTable:
                    # 忽略2个指定的表(表用|分隔) ，如 #rcd_order_info|tt_user_login ， Database_PO.searchKeyword(u"#rcd_order_detail_2|rcd_orderinfo", u"char", u"张三")
                    varTable2 = varTable.split(u"#")[1]  #   rcd_order_detail_2|rcd_orderinfo_2'
                    varTable3 = varTable2.split(u"|")
                    # for i in range(len(varTable2.split(u"|"))):
                    #     print "ignore => " + varTable3[i]
                    # not regexp 方法
                    m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not regexp "%s|%s" ' % (self.varDatabase, varTable3[0], varTable3[1]))
                    # m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not like "%s" and table_name not like "%s"' % (self.varDatabase, varTable3[0], varTable3[1]))
                    t0 = self.cur.fetchall()
                    print u"共有 " + str(len(t123)) + u" 张表 ，遍历 " + str(len(t0)) + u" 张表 ，已忽略 " + str(varTable3[0]) + u"、" + str(varTable3[0]) + u"表"
                else:
                    # 不包含1个表或多个模糊的表，#rcd_order_info 遍历不包含rcd_order_info的所有表.
                    # Database_PO.searchKeyword(u"#rcd_%", u"char", u"wang")
                    # Database_PO.searchKeyword(u"#rcd_order_detail_2", u"char", u"张三")
                    varTable2 = varTable.split(u"#")[1]

                    m = self.cur.execute(
                        'select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not like "%s"' % (self.varDatabase, varTable2))
                    t0 = self.cur.fetchall()
                    print u"共有 " + str(len(t123)) + u" 张表 ，遍历 " + str(len(t0)) + u" 张表!!! "
                varbat = 1

            if varbat == 1:
                if m != 0:
                    for p in range(len(t0)):
                        varTable = t0[p][0]
                        # 遍历指定的表
                        n = self.cur.execute(
                            'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s"' % (
                                self.varDatabase, varTable))
                        if n != 0:
                            t1 = self.cur.fetchone()
                            tblDDL = t1[0]
                            self.cur.execute(
                                'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (
                                    self.varDatabase, varTable))
                            t2 = self.cur.fetchall()
                            # print "\n[" + varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(len(t2)) + "fields]"
                            for i in t2:
                                if len(i[0]) > x: x = len(i[0])
                                if len(i[1]) > y: y = len(i[1])
                                tblFieldcount = tblFieldcount + 1
                            for j in t2:
                                if varType in j[1]:
                                    list0.append(j[0])
                                    list1.append(j[1])
                            # print len(list0)   # 搜索的字段类型有多少个
                            # print varTable
                            for i in range(0, len(list0)):
                                # list0[i]  字段名,如果字段名是关键字必须添加`
                                # print list0[i]
                                # print varValue
                                # print varTable
                                self.cur.execute('select * from %s where `%s` like "%s"' % (varTable, list0[i], varValue))
                                t4 = self.cur.fetchall()
                                if len(t4) != 0:
                                    print ">" * 70
                                    print u"[Result = " + str(len(
                                        t4)) + u" , Keyword = '" + varValue + u"' , " + self.varDatabase + "." + varTable + "." + \
                                          list0[i] + u"]\n"
                                    for j in range(len(t4)):
                                        varStr = ""
                                        for k in range(len(list(t4[j]))):
                                            varStr = varStr + u" , " + str(list(t4[j])[k])
                                        print varStr.lstrip(' ,')
                                        print ">" * 70


                                    print "\n"
                        list0 = []
                        list1 = []
                        tblFieldcount = 0
                else:
                    print u"errorrrrrrrrrr, 数据库(" + self.varDatabase + u")中没有找到 " + varTable.split("*")[0] + u" 前缀的表!"



            # 单个表查询

            else:

                n = self.cur.execute(
                    'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                        self.varDatabase, varTable))
                if n != 0:
                    t1 = self.cur.fetchone()
                    print u"共有 " + str(len(t123)) + u" 张表 ，遍历 " + str(len(t1)) + u" 张表 "
                    tblDDL = t1[0]
                    self.cur.execute(
                        'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (
                            self.varDatabase, varTable))
                    t2 = self.cur.fetchall()
                    # print "\n[" + varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(len(t2)) + "fields]"
                    for i in t2:
                        if len(i[0]) > x: x = len(i[0])
                        if len(i[1]) > y: y = len(i[1])
                        tblFieldcount = tblFieldcount + 1
                    for j in t2:
                        if varType in j[1]:
                            list0.append(j[0])
                            list1.append(j[1])
                    # print len(list0)   # 搜索的字段类型有多少个
                    for i in range(0, len(list0)):
                        # list0[i]  字段名,如果字段名是关键字必须添加`
                        self.cur.execute(
                            'select * from %s where `%s` like "%s"' % (varTable, list0[i], varValue))
                        t4 = self.cur.fetchall()
                        if len(t4) != 0:
                            print ">" * 150
                            print u"[Result = " + str(
                                len(
                                    t4)) + u" , Keyword = '" + varValue + u"' , " + self.varDatabase + u"." + varTable + u"." + \
                                  list0[i] + u"]\n"

                            for j in range(len(t4)):
                                # print json.dumps(list(t4[j]), encoding="UTF-8", ensure_ascii=False)
                                # print list(t4[j])
                                # print type(list(t4[j]))
                                # print len(list(t4[j]))
                                varStr = ""
                                for k in range(len(list(t4[j]))):
                                    varStr = varStr + u" , " + str(list(t4[j])[k])
                                print varStr.lstrip(' ,')


                            print "\n"
                else:
                    print u"errorrrrrrrrrr, 数据库(" + self.varDatabase + u")中没有找到此表(" + varTable + u")!"
        else:
            print u"errorrrrrrrrrr, 数据类型错误或为空！"

    def searchKeywordStru(self, varTable, varType, varValue):
        # 功能：模糊搜索关键字，遍历所有的表获取关键字的详细记录及字段名，如 (userid)12,(phone)13816109040
        # 参数以此为表（*表示所有表）、数据类型、值
        # 参数1 = 表(*表示搜索所有的表）
        # 参数2 = 字段类型 （如：char、int、tinyint、double、timestamp）
        # 参数3 = 关键字(不能为空,*通配符)
        # Database_PO.searchKeyword("*", "char", "a123456")
        # Database_PO.searchKeyword("*", "timestamp", "2017-10-15 23:29:47")
        # Database_PO.searchKeyword("*", "datetime", "2017-10-15 19:45:54")
        # Database_PO.searchKeyword('*', u'char', u'%814子项目2%')
        list0 = []
        list1 = []
        x = y = tblFieldcount = varbat = 0
        if varType in 'int,char,tinyint,smallint,timestamp,varchar,double,datetime':

            m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
            t123 = self.cur.fetchall()

            if varTable == u'*':
                # * 遍历所有表 , Database_PO.searchKeyword(u"*, u"char", u"wang")
                m = self.cur.execute(
                    'select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
                t0 = self.cur.fetchall()
                print u"共有 " + str(len(t0)) + u" 张表 ，全部遍历"
                varbat = 1

            elif u"*" in varTable:
                # *tt_% 遍历tt_开头的表 , Database_PO.searchKeyword(u"*tt_%", u"char", u"wang")
                varTable2 = varTable.split(u"*")[1]  # *t_store_%
                varbat = 1
                m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (self.varDatabase, varTable2))
                t0 = self.cur.fetchall()
                print u"共有 " + str(len(t123)) + u" 张表 ，遍历 " + str(len(t0)) + u" 张表 "

            elif u"#" in varTable:
                if u"|" in varTable:
                    # 不包含多个明确的表 ， #rcd_order_info|tt_user_login 遍历不包含这2个的所有表，多表之间用|分割。Database_PO.searchKeyword(u"#rcd_order_detail_2|rcd_orderinfo", u"char", u"张三")
                    varTable2 = varTable.split(u"#")[1]  # #t_store_
                    m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not regexp "%s"' % (self.varDatabase, varTable2))
                    t0 = self.cur.fetchall()
                    print u"共有 " + str(len(t123)) + u" 张表 ，遍历 " + str(len(t0)) + u" 张表 "
                else:
                    # 不包含1个表或多个模糊的表，#rcd_order_info 遍历不包含rcd_order_info的所有表.
                    # Database_PO.searchKeyword(u"#rcd_%", u"char", u"wang")
                    # Database_PO.searchKeyword(u"#rcd_order_detail_2", u"char", u"张三")
                    varTable2 = varTable.split(u"#")[1]
                    m = self.cur.execute(
                        'select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not like "%s"' % (
                            self.varDatabase, varTable2))
                    t0 = self.cur.fetchall()
                    print u"共有 " + str(len(t123)) + u" 张表 ，遍历 " + str(len(t0)) + u" 张表 "
                varbat = 1

            if varbat == 1:
                if m != 0:
                    for p in range(len(t0)):
                        varTable = t0[p][0]
                        # 遍历指定的表
                        n = self.cur.execute(
                            'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s"' % (
                                self.varDatabase, varTable))
                        if n != 0:
                            t1 = self.cur.fetchone()
                            tblDDL = t1[0]
                            self.cur.execute(
                                'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (
                                    self.varDatabase, varTable))
                            t2 = self.cur.fetchall()
                            # print "\n["  + " > " + varTable + "(" + tblDDL + ") > " + str(len(t2)) + "fields]"
                            for i in t2:
                                if len(i[0]) > x: x = len(i[0])
                                if len(i[1]) > y: y = len(i[1])
                                tblFieldcount = tblFieldcount + 1
                            for j in t2:
                                if varType in j[1]:
                                    list0.append(j[0])
                                    list1.append(j[1])
                            # print len(list0)   # 搜索的字段类型有多少个
                            # print varTable
                            for i in range(0, len(list0)):
                                # list0[i]  字段名,如果字段名是关键字必须添加`
                                # print list0[i]
                                # print varValue
                                self.cur.execute('select * from %s where `%s` like "%s"' % (varTable, list0[i], varValue))
                                t4 = self.cur.fetchall()
                                if len(t4) != 0:
                                    print ">" * 70
                                    print u"[Result = " + str(len(
                                        t4)) + u" , Keyword = '" + varValue + u"' , " + self.varDatabase + " -> " + varTable + " -> " + \
                                          list0[i] + u"]\n"

                                    # 获取字段名
                                    list33 = []
                                    for x in t2:
                                        list33.append(x[0])

                                    for j in range(len(t4)):
                                        varStr = ""
                                        for k in range(len(list(t4[j]))):
                                            varStr = varStr + u" , " + u"(" + list33[k] + u")" + str(list(t4[j])[k])
                                        print varStr.lstrip(' ,')
                                        print ">" * 70
                                    print "\n"
                        list0 = []
                        list1 = []
                        tblFieldcount = 0
                else:
                    print u"errorrrrrrrrrr, 数据库(" + self.varDatabase + u")中没有找到 " + varTable.split("*")[0] + u" 前缀的表!"

            # 单个表查询

            else:

                n = self.cur.execute(
                    'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                        self.varDatabase, varTable))
                if n != 0:
                    t1 = self.cur.fetchone()
                    print u"共有 " + str(len(t123)) + u" 张表 ，遍历 " + str(len(t1)) + u" 张表 "
                    tblDDL = t1[0]
                    self.cur.execute(
                        'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (
                            self.varDatabase, varTable))
                    t2 = self.cur.fetchall()
                    # print "\n[" + varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(len(t2)) + "fields]"
                    for i in t2:
                        if len(i[0]) > x: x = len(i[0])
                        if len(i[1]) > y: y = len(i[1])
                        tblFieldcount = tblFieldcount + 1
                    for j in t2:
                        if varType in j[1]:
                            list0.append(j[0])
                            list1.append(j[1])
                    # print len(list0)   # 搜索的字段类型有多少个
                    for i in range(0, len(list0)):
                        # list0[i]  字段名,如果字段名是关键字必须添加`
                        self.cur.execute(
                            'select * from %s where `%s` like "%s"' % (varTable, list0[i], varValue))
                        t4 = self.cur.fetchall()
                        if len(t4) != 0:
                            print ">" * 150
                            print u"[Result = " + str(
                                len(
                                    t4)) + u" , Keyword = '" + varValue + u"' , " + self.varDatabase + u"." + varTable + u"." + \
                                  list0[i] + u"]\n"

                            for j in range(len(t4)):
                                # print json.dumps(list(t4[j]), encoding="UTF-8", ensure_ascii=False)
                                # print list(t4[j])
                                # print type(list(t4[j]))
                                # print len(list(t4[j]))
                                varStr = ""
                                for k in range(len(list(t4[j]))):
                                    varStr = varStr + u" , " + str(list(t4[j])[k])
                                print varStr.lstrip(' ,')
                            print "\n"
                else:
                    print u"errorrrrrrrrrr, 数据库(" + self.varDatabase + u")中没有找到此表(" + varTable + u")!"
        else:
            print u"errorrrrrrrrrr, 数据类型错误或为空！"

    def searchKeywordAll(self, varTable, varType, varValue):
        # 功能：模糊搜索关键字，遍历所有的表获取关键字的详细记录及字段名，如 (userid)12,(phone)13816109040
        # 参数以此为表（*表示所有表）、数据类型、值
        # 参数1 = 表(*表示搜索所有的表）
        # 参数2 = 字段类型 （如：char、int、tinyint、double、timestamp）
        # 参数3 = 关键字(不能为空,*通配符)
        # Database_PO.searchKeywordAll("*", "char", "a123456")
        # Database_PO.searchKeywordAll("*", "timestamp", "2017-10-15 23:29:47")
        # Database_PO.searchKeywordAll("*", "datetime", "2017-10-15 19:45:54")
        # Database_PO.searchKeywordAll('*', u'char', u'%814子项目2%')
        list0 = []
        list1 = []
        x = y = tblFieldcount = varbat = tblFieldcount2 = 0
        if varType in 'int,char,tinyint,smallint,timestamp,varchar,double,datetime':

            m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
            t123 = self.cur.fetchall()

            if varTable == u'*':
                # * 遍历所有表 , Database_PO.searchKeyword(u"*, u"char", u"wang")
                m = self.cur.execute(
                    'select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
                t0 = self.cur.fetchall()
                print u"共有 " + str(len(t0)) + u" 张表 ，全部遍历"
                varbat = 1

            elif u"*" in varTable:
                # *tt_% 遍历tt_开头的表 , Database_PO.searchKeyword(u"*tt_%", u"char", u"wang")
                varTable2 = varTable.split(u"*")[1]  # *t_store_%
                varbat = 1
                m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (self.varDatabase, varTable2))
                t0 = self.cur.fetchall()
                print u"共有 " + str(len(t123)) + u" 张表 ，遍历 " + str(len(t0)) + u" 张表 "

            elif u"#" in varTable:
                if u"|" in varTable:
                    # 不包含多个明确的表 ， #rcd_order_info|tt_user_login 遍历不包含这2个的所有表，多表之间用|分割。Database_PO.searchKeyword(u"#rcd_order_detail_2|rcd_orderinfo", u"char", u"张三")
                    varTable2 = varTable.split(u"#")[1]  # #t_store_
                    m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not regexp "%s"' % (self.varDatabase, varTable2))
                    t0 = self.cur.fetchall()
                    print u"共有 " + str(len(t123)) + u" 张表 ，遍历 " + str(len(t0)) + u" 张表 "
                else:
                    # 不包含1个表或多个模糊的表，#rcd_order_info 遍历不包含rcd_order_info的所有表.
                    # Database_PO.searchKeyword(u"#rcd_%", u"char", u"wang")
                    # Database_PO.searchKeyword(u"#rcd_order_detail_2", u"char", u"张三")
                    varTable2 = varTable.split(u"#")[1]
                    m = self.cur.execute(
                        'select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not like "%s"' % (
                            self.varDatabase, varTable2))
                    t0 = self.cur.fetchall()
                    print u"共有 " + str(len(t123)) + u" 张表 ，遍历 " + str(len(t0)) + u" 张表 "
                varbat = 1

            if varbat == 1:
                if m != 0:
                    for p in range(len(t0)):
                        varTable = t0[p][0]
                        # 遍历指定的表
                        n = self.cur.execute(
                            'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s"' % (
                                self.varDatabase, varTable))
                        if n != 0:
                            t1 = self.cur.fetchone()
                            tblDDL = t1[0]
                            self.cur.execute(
                                'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (
                                    self.varDatabase, varTable))
                            t2 = self.cur.fetchall()
                            # print "\n["  + " > " + varTable + "(" + tblDDL + ") > " + str(len(t2)) + "fields]"
                            for i in t2:
                                if len(i[0]) > x: x = len(i[0])
                                if len(i[1]) > y: y = len(i[1])
                                tblFieldcount = tblFieldcount + 1
                            for j in t2:
                                if varType in j[1]:
                                    list0.append(j[0])
                                    list1.append(j[1])
                            # print len(list0)   # 搜索的字段类型有多少个
                            # print varTable
                            for i in range(0, len(list0)):

                                # list0[i]  字段名,如果字段名是关键字必须添加`
                                # print list0[i]
                                # print varValue
                                self.cur.execute('select * from %s where `%s` like "%s"' % (varTable, list0[i], varValue))
                                t4 = self.cur.fetchall()
                                if len(t4) != 0:
                                    print ">" * 70
                                    print u"[Result = " + str(len(
                                        t4)) + u" , Keyword = '" + varValue + u"' , " + self.varDatabase + " -> " + varTable + " -> " + \
                                          list0[i] + u"]\n"

                                    # 获取字段名
                                    list33 = []
                                    list44 = []
                                    list55 = []

                                    z=0
                                    for i in t2:
                                        if len(i[0]) > x: x = len(i[0])
                                        if len(i[1]) > y: y = len(i[1])
                                        if len(i[2]) > z: z = len(i[2])
                                        tblFieldcount2 = tblFieldcount2 + 1

                                    for i in t2:
                                        list33.append(i[0] + " " * (x - len(i[0]) + 1))
                                        list44.append(i[1] + " " * (y - len(i[1]) + 1))
                                        list55.append(i[2].replace("\r\n", ",").replace("  ", "") + " " * (z - len(i[2]) + 1))
                                    varStr = ""

                                    for i in range(tblFieldcount2):
                                        print list33[i], list44[i], list55[i], str(list(t4[0])[i])
                                    print varStr.lstrip(' ,')
                                    print "\n"
                        list0 = []
                        list1 = []
                        tblFieldcount = 0
                        tblFieldcount2 = 0

                else:
                    print u"errorrrrrrrrrr, 数据库(" + self.varDatabase + u")中没有找到 " + varTable.split("*")[0] + u" 前缀的表!"

            # 单个表查询

            else:
                n = self.cur.execute(
                    'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                        self.varDatabase, varTable))
                if n != 0:
                    t1 = self.cur.fetchone()
                    print u"共有 " + str(len(t123)) + u" 张表 ，遍历 " + str(len(t1)) + u" 张表 "
                    tblDDL = t1[0]
                    self.cur.execute(
                        'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (
                            self.varDatabase, varTable))
                    t2 = self.cur.fetchall()
                    # print "\n[" + varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(len(t2)) + "fields]"
                    for i in t2:
                        if len(i[0]) > x: x = len(i[0])
                        if len(i[1]) > y: y = len(i[1])
                        tblFieldcount = tblFieldcount + 1
                    for j in t2:
                        if varType in j[1]:
                            list0.append(j[0])
                            list1.append(j[1])
                    # print len(list0)   # 搜索的字段类型有多少个
                    for i in range(0, len(list0)):
                        # list0[i]  字段名,如果字段名是关键字必须添加`
                        self.cur.execute(
                            'select * from %s where `%s` like "%s"' % (varTable, list0[i], varValue))
                        t4 = self.cur.fetchall()
                        if len(t4) != 0:
                            print ">" * 150
                            print u"[Result = " + str(
                                len(
                                    t4)) + u" , Keyword = '" + varValue + u"' , " + self.varDatabase + u"." + varTable + u"." + \
                                  list0[i] + u"]\n"

                            for j in range(len(t4)):
                                # print json.dumps(list(t4[j]), encoding="UTF-8", ensure_ascii=False)
                                # print list(t4[j])
                                # print type(list(t4[j]))
                                # print len(list(t4[j]))
                                varStr = ""
                                for k in range(len(list(t4[j]))):
                                    varStr = varStr + u" , " + str(list(t4[j])[k])
                                print varStr.lstrip(' ,')

                            print "\n"
                else:
                    print u"errorrrrrrrrrr, 数据库(" + self.varDatabase + u")中没有找到此表(" + varTable + u")!"
        else:
            print u"errorrrrrrrrrr, 数据类型错误或为空！"

    def getSearch1get1(self, varTable, varField, varValue, rtnField):
        # 功能：搜索1个条件并返回rtnField值
        # 参数1 = 表(不能为空）
        # 参数2 = 搜索字段
        # 参数3 = 参数2对应的值
        # 参数4 = 返回字段（字符串）
        # x = Database_PO.getSearch1get1("tt_user_login", "user_id", "2", "phone_number")， ／／如返回phone_number的值
        varN = self.cur.execute('select %s from %s where %s="%s" ' % (rtnField, varTable, varField, varValue))
        if varN == 0:
            print u"[warning] 表" + varTable + u" 中未找到符合条件（ " + varField + u" = " + varValue + u" ）的 "+ rtnField +  u"值！"
            return -1
        elif varN == 1:
            print "return: 1"
            return str(self.cur.fetchone()[0])
        elif varN > 1:
            print "return: " + str(varN)
            return str(self.cur.fetchall())

    def getSearch2get1(self, varTable, varField1, varValue1, varField2, varValue2, rtnField):
        # 功能：搜索2个条件并返回rtnField值
        # 参数1 = 表(不能为空）
        # 参数2\3\4\5 = 搜索字段1 和 字段2
        # 参数6 = 返回字段（字符串）
        # x = Database_PO.getSearch2get1("tt_user_login", "user_id", "2", "password", "123456", "phone_number")， ／／如返回phone_number的值
        varN = self.cur.execute('select %s from %s where %s="%s" and %s="%s" ' % (rtnField, varTable, varField1, varValue1, varField2, varValue2))
        if varN == 0:
            print u"[warning] 表" + varTable + u" 中未找到符合条件（ " + varField1 + u" = " + varValue1 + u" 且 " + varField2 + u" = " + varValue2 + u"）的 " + rtnField + u"值！"
            return None
        elif varN == 1:
            return str(self.cur.fetchone()[0])

    def getSearch1get2(self, varTable, varField, varValue, rtnField1, rtnField2):
        # 功能：搜索1个条件并返回2个rtnField值
        # 参数1 = 表(不能为空）
        # 参数2\3 = 搜索字段及对应的值
        # 参数4\5 = 返回字段1、2
        # xy = Database_PO.getSearch1get2("tt_user_login", "user_id", "2", "password", "phone_number")   //(u'123456', u'13564951111')
        # print xy[0],xy[1]  类型是unicode
        varN = self.cur.execute('select %s,%s from %s where %s="%s" ' % (rtnField1,rtnField2, varTable, varField, varValue))
        if varN == 0:
            print u"[warning] 表" + varTable + u" 中未找到符合条件（ " + varField + u" = " + varValue + u"）的 " + rtnField1 + u"," + rtnField2 + u"值！"
            return None
        elif varN == 1:
            return self.cur.fetchall()[0]

    def getSearch2get2(self, varTable, varField1, varValue1, varField2, varValue2, rtnField1, rtnField2):
        # 功能：搜索2个条件并返回2个rtnField值
        # 参数1 = 表(不能为空）
        # 参数2\3\4\5 = 搜索字段1 和 字段2
        # 参数6\7 = 返回字段1、2
        # xy = Database_PO.getSearch2get2("tt_user_login", "user_id", "2", "password", "123456", "phone_number","is_send_message")  //(u'123456', u'13564951111')
        # print xy[0],xy[1]  类型是unicode
        varN = self.cur.execute('select %s,%s from %s where %s="%s" and %s="%s" ' % (rtnField1,rtnField2, varTable, varField1, varValue1, varField2, varValue2))
        if varN == 0:
            print u"[warning] 表" + varTable + u" 中未找到符合条件（ " + varField1 + u" = " + varValue1 + u" 且 " + varField2 + u" = " + varValue2 + u"）的 " + rtnField1 + u"," + rtnField2 +  u"值！"
            return None
        elif varN == 1:
            return self.cur.fetchall()[0]

    def getSearch1getCount(self, varTable, varField, varValue):
        # 功能：搜索1个条件并返回rtnField值
        # 参数1 = 表(不能为空）
        # 参数2 = 搜索字段
        # 参数3 = 参数2对应的值
        # 参数4 = 返回字段（字符串）
        # x = Database_PO.getSearch1getCount("tt_user_login", "user_id", "2")
        varN = ""
        varN = self.cur.execute('select count(%s) from %s where %s="%s" ' % (varField, varTable, varField, varValue))
        if varN == 0:
            print u"[warning] 表" + varTable + u" 中未找到符合条件（ " + varField + u" = " + varValue + u" ）的值！"
            return None
        else:
            return str(self.cur.fetchone()[0])



