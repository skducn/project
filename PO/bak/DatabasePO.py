# coding=utf-8
#***************************************************************
# Author     : John
# Revise on : 2017-11-16
# Description: DatabasePO对象层
# Database_PO = DatabasePO('10.111.3.4', 3306, 'cetc', '20121221', 'hjk')
# 查询后中文正确显示，但在数据库中却显示乱码 ， 解决方法如下 ，添加 charset='utf8 ，  charset是要跟你数据库的编码一样，如果是数据库是gb2312 ,则写charset='gb2312'。
# conn = MySQLdb.Connect(host='localhost', user='root', passwd='root', db='python',charset='utf8')
#***************************************************************

import MySQLdb, platform
from PO.BasePO import *
# from selenium.webdriver.common.by import By

# if platform.system() == 'Darwin':
#     sys.setdefaultencoding('utf-8')  # for win 比如windows的cmd下的默认字符编码为GBK或ASCII
# if platform.system() == 'Windows':
#     from Public.cmdColor import *
#     sys.setdefaultencoding('GBK')  # for win 比如windows的cmd下的默认字符编码为GBK或ASCII

def printColor(macColor, winColor, varContent):
    if platform.system() == 'Darwin':
        print(macColor) + varContent + '\033[0m'
    if platform.system() == 'Windows':
        (eval(winColor))(varContent.encode('gb2312') + "\n")

class DatabasePO(BasePO):

    def __init__(self, dimHost, dimPort, dimUser, dimPasswd, dimDatabase):
        self.varHost = dimHost
        self.varPort = dimPort
        self.varUser = dimUser
        self.varPasswd = dimPasswd
        self.varDatabase = dimDatabase
        self.conn = MySQLdb.connect(host=self.varHost, user=self.varUser, passwd=self.varPasswd, db=self.varDatabase, port=self.varPort, use_unicode=True, charset='utf8', autocommit=True)
        self.cur = self.conn.cursor()
        self.cur.execute('SET NAMES utf8;')
        self.conn.set_character_set('utf8')
        # self.cur.execute('show tables')
        self.BasePage = BasePO(self)

    def showCreateTime(self, dimTable, dimStatus, dimAfterTime):
        # 功能: 获取表的创建时间
        # 参数1 = 表(默认为空，搜索所有的表）
        # 参数2 = 指定日期前或后 （before表示指定日期之前创建、after表示指定日期之后创建）
        # 参数3 = 日期(不能为空)
        # Database_PO.showCreateTime("", "after", "2017-10-10")    如：2017-10-15 23:26:15 => tt_manage_user
        # Database_PO.showCreateTime("", "before", "2017-10-10")
        # Database_PO.showCreateTime("", "", "")  显示所有表创建时间
        print("-" * 100)
        if self.varDatabase != "":
            try:
                if dimTable == "" and dimStatus == "":
                    self.cur.execute(
                        'select count(create_time) from information_schema.`TABLES` where table_schema="%s" ' % (
                            self.varDatabase))
                    t1 = self.cur.fetchall()
                    # print t1[0][0]  # 统计表数量
                    print("[" + self.varDatabase + " 中共有 " + str(t1[0][0]) + " 张表，各表的创建时间（升序）如下]")
                    self.cur.execute(
                        'select table_name,create_time from information_schema.`TABLES` where table_schema="%s" order by create_time' % (
                            self.varDatabase))
                    t3 = self.cur.fetchall()
                    for i in range(t1[0][0]):
                        print(str(t3[i][1]) + " => " + t3[i][0])
                elif dimTable != "":
                    self.cur.execute(
                        'select create_time from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                            self.varDatabase, dimTable))
                    t3 = self.cur.fetchone()
                    print("[" + self.varDatabase + "." + dimTable + " 表的创建时间为 " + str(t3[0]) + "]")
                else:
                    if dimStatus == "after":
                        x = self.cur.execute(
                            'select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time>"%s"' % (
                                self.varDatabase, dimAfterTime))
                        t4 = self.cur.fetchall()
                        print("[" + self.varDatabase + " 中共有 " + str(x) + " 张表在 " + str(dimAfterTime) + " 之后被创建]")

                        for p in range(len(t4)):
                            print(str(t4[p][1]) + " => " + t4[p][0])
                    elif dimStatus == "before":
                        x = self.cur.execute(
                            'select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time<"%s"' % (
                                self.varDatabase, dimAfterTime))
                        t4 = self.cur.fetchall()
                        print("[" + self.varDatabase + " 中共有 " + str(x) + " 张表在 " + str(dimAfterTime) + " 之前被创建]")

                        for p in range(len(t4)):
                            print(str(t4[p][1]) + " => " + (t4[p][0]))
                    else:
                        print("errorrrrrrrrrr, 表名不能为空！")
            except:
                print("errorrrrrrrrrr, 表名(" + self.varDatabase + "." + dimTable + ")不存在！")
        else:
            print("warning , 数据库不能为空！")
    def selectKeyword(self, varTable, varType, varValue):
        # 功能：模糊搜索关键字，遍历所有的表获取关键字的详细记录
        # 参数以此为表（*表示所有表）、数据类型、值
        # 参1 = 表(*表示搜索所有的表）, 参2 = 字段类型 （如：char、int、tinyint、double、timestamp）, 参3 = 关键字(不能为空,*通配符)
        # Database_PO.searchKeyword("*", "char", "a123456")
        # Database_PO.searchKeyword("tt_store", "timestamp", "2017-10-15 23:29:47")
        # Database_PO.searchKeyword("tt_st%", "datetime", "2017-10-15 19:45:54")
        # Database_PO.searchKeyword('#tt_qa', u'char', u'%814子项目2%')
        list0 = []
        list1 = []
        x = y = tblFieldcount = 0
        isMoreTables = 0  # 是否是针对多表查询
        noResult = 0
        # varType = 'char'  # 默认搜索字符型
        if varType in 'int,json,char,tinyint,smallint,timestamp,varchar,double,datetime':
            # python sql.py -sk testsy.* timestamp 2018-07-02_11:%    更新日期
            if varType =="timestamp":
                # pass 2018-06-14_15:12:12
                varValue0 = str(varValue).split("_")[0]
                varValue1 = str(varValue).split("_")[1]
                varValue = varValue0 + " " + varValue1
            m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
            allTablesName = self.cur.fetchall()
            if varTable == '*':  # 遍历所有表
                isMoreTables = 1
                m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
                t0 = self.cur.fetchall()
                printColor('\033[1;32;40m', 'printGreen', u"All of the " + str(len(t0)) + u" tables is traversed.")
            elif u'#' in varTable:  # 忽略表，如 '#rcd_order_detail_2'
                isMoreTables = 1
                if u"," in varTable:
                    # 忽略2个指定的表(表之间用逗号分隔)
                    # Database_PO.searchKeyword(u"#rcd_order_detail_2|rcd_orderinfo", u"char", u"张三")  如 #rcd_order_info|tt_user_login
                    varTable2 = varTable.split(u"#")[1]  # rcd_order_detail_2|rcd_orderinfo_2'
                    varTable3 = varTable2.split(u",")
                    m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not regexp "%s|%s" ' % (self.varDatabase, varTable3[0], varTable3[1]))
                    # m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not like "%s" and table_name not like "%s"' % (self.varDatabase, varTable3[0], varTable3[1]))
                    t0 = self.cur.fetchall()
                    printColor('\033[1;32;40m', 'printGreen', str(len(t0)) + u" of the " + str(len(allTablesName)) + u" tables is traversed. ignore (" + varTable3[0] + u" , " + varTable3[1] + u")")
                else:
                    # 忽略1个表或多个模糊的表
                    # Database_PO.searchKeyword(u"#rcd_order_detail_2", u"char", u"张三")  如 #rcd_order_detail_2 表示遍历时忽略 rcd_order_detail_2 表.
                    # Database_PO.searchKeyword(u"#rcd_%", u"char", u"wang")  # 忽略 rcd_开头的所有表
                    varTable2 = varTable.split(u"#")[1]
                    m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not like "%s"' % (self.varDatabase, varTable2))
                    t0 = self.cur.fetchall()
                    printColor('\033[1;32;40m', 'printGreen', str(len(t0)) + u" of the " + str(len(allTablesName)) + u" tables is traversed. ignore(" + varTable2 + u")")
            elif u'%' in varTable:  # 遍历部分表，如 tt_store% 遍历tt_store开头的表
                isMoreTables = 1
                m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (self.varDatabase, varTable))
                t0 = self.cur.fetchall()
                printColor('\033[1;32;40m', 'printGreen', str(len(t0)) + u" of the " + str(len(allTablesName)) + u" tables is traversed.")

            if isMoreTables == 1:
                if m != 0:
                    for p in range(len(t0)):
                        varTable = t0[p][0]  # 遍历指定的表
                        n = self.cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s"' % (self.varDatabase, varTable))
                        if n != 0:
                            t1 = self.cur.fetchone()
                            tblDDL = t1[0]
                            self.cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (self.varDatabase, varTable))
                            t2 = self.cur.fetchall()
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
                                # print list0[i]
                                # print varTable   unicode( varValue , errors='ignore')
                                l_fieldLen = []
                                l_maxLen = []
                                l_valueLen = []
                                self.cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (self.varDatabase, varTable))
                                allField = self.cur.fetchall()  # 所有字段
                                # self.cur.execute("select * from %s where `%s` like '%s'" % (varTable, list0[i], unicode(varValue, 'gbk')))
                                self.cur.execute("select * from %s where `%s` like '%s'" % (varTable, list0[i], varValue.encode('utf-8').decode('unicode_escape')))

                                allRecord = self.cur.fetchall()  # 所有值

                                if len(allRecord) != 0:
                                    printColor('\033[1;36;40m', 'printSkyBlue', varTable + u"." + list0[i] + u"(" + str(len(allRecord)) + u")  " + tblDDL)
                                    # 遍历每个字段的长度,生成列表l_fieldLen
                                    for i in range(len(allField)):
                                        l_fieldLen.append(len(allField[i][0]))
                                        l_maxLen.append(len(allField[i][0]))
                                    # print u"l_fieldLen = " + str(l_fieldLen)

                                    # 遍历每个值的长度并与字段长度比较，生成列表l_maxLen
                                    for j in range(len(allRecord)):
                                        for k in range(len(list(allRecord[j]))):
                                            # 格式化中文字符统计，以下4行
                                            # value = unicode(str(list(allRecord[j])[k]), 'utf-8')
                                            value = str(list(allRecord[j])[k]).encode('utf-8').decode('unicode_escape')
                                            length = len(value)
                                            utf8_length = len(value.encode('utf-8'))
                                            length = (utf8_length - length) / 2 + length
                                            l_valueLen.append(length)
                                            if l_maxLen[k] < l_valueLen[k]: l_maxLen[k] = l_valueLen[k]
                                            if l_maxLen[k] < l_fieldLen[k]: l_maxLen[k] = l_fieldLen[k]
                                        l_valueLen = []
                                    # print u"l_maxLen = " + str(l_maxLen)

                                    # 输出字段的列表（顶部）
                                    l_field = []
                                    varFields = ""
                                    for i in range(len(allField)):
                                        l_field.append(str(allField[i][0]))
                                        varFields = varFields + str(list(allField[i])[0]) + u" " * (int(l_maxLen[i]) - int(l_fieldLen[i])) + u" "

                                    # 字段列表（顶部）
                                    printColor('\033[1;32;40m', 'printGreen', varFields)

                                    for j in range(len(allRecord)):
                                        varStr = ""
                                        for k in range(len(list(allRecord[j]))):
                                            # value = unicode(str(list(allRecord[j])[k]), 'utf-8')
                                            value = str(list(allRecord[j])[k]).encode('utf-8').decode('unicode_escape')
                                            length = len(value)
                                            utf8_length = len(value.encode('utf-8'))
                                            length = (utf8_length - length) / 2 + length
                                            varStr = varStr + str(list(allRecord[j])[k]) + u" " * (int(l_maxLen[k]) - length) + u" "
                                        printColor('', 'printDarkWhite', varStr)
                                    noResult = 1

                                    # 字段列表（底部）
                                    printColor('\033[1;32;40m', 'printGreen', varFields)
                                    print("\n")

                        list0 = []
                        list1 = []
                        tblFieldcount = 0
                    if noResult == 0:
                        printColor('\033[1;36;40m', 'printSkyBlue', u"Result = 0")
                else:
                    printColor('\033[1;31;47m', 'printRed', u"errorrrrrrrrrr, 数据库（" + self.varDatabase + u"）中没有找到 " + varTable.split("%")[0] + u" 前缀的表!!!")

            # 单个表查询 ===============================================================================================
            else:

                self.cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (self.varDatabase, varTable))
                t1 = self.cur.fetchone()
                tblDDL = t1[0]
                l_fieldLen = []
                l_maxLen = []
                l_valueLen = []

                self.cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (self.varDatabase, varTable))
                allField = self.cur.fetchall()  # 所有字段
                self.cur.execute('select * from %s ' % (varTable))
                allRecord = self.cur.fetchall()  # 所有值

                # 遍历每个字段的长度,生成列表l_fieldLen
                for i in range(len(allField)):
                    l_fieldLen.append(len(allField[i][0]))
                    l_maxLen.append(len(allField[i][0]))
                # print u"l_fieldLen = " + str(l_fieldLen)

                # 遍历每个值的长度并与字段长度比较，生成列表l_maxLen
                for j in range(len(allRecord)):
                    for k in range(len(list(allRecord[j]))):
                        # 格式化中文字符统计，以下4行
                        # value = unicode(str(list(allRecord[j])[k]), 'utf-8')
                        value = str(list(allRecord[j])[k]).encode('utf-8').decode('unicode_escape')
                        length = len(value)
                        utf8_length = len(value.encode('utf-8'))
                        length = (utf8_length - length) / 2 + length
                        l_valueLen.append(length)
                        if l_maxLen[k] < l_valueLen[k]: l_maxLen[k] = l_valueLen[k]
                        if l_maxLen[k] < l_fieldLen[k]: l_maxLen[k] = l_fieldLen[k]
                    l_valueLen = []
                # print u"l_maxLen = " + str(l_maxLen)

                # 输出字段的列表（顶部）
                l_field = []
                varFields = ""
                for i in range(len(allField)):
                    l_field.append(str(allField[i][0]))
                    varFields = varFields + str(list(allField[i])[0]) + u" " * (int(l_maxLen[i]) - int(l_fieldLen[i])) + u" "


                # 遍历所有记录 =========================================================================================
                if varValue == "*":

                    printColor('\033[1;36;40m', 'printSkyBlue', tblDDL + u" , Records = " + str(len(allRecord)))
                    # 字段列表（顶部显示）
                    printColor('\033[1;32;40m', 'printGreen', varFields)

                    # 输出值列表
                    self.cur.execute('select * from %s ' % (varTable))
                    allRecord = self.cur.fetchall()
                    for j in range(len(allRecord)):
                        varValues = ""

                        for k in range(len(list(allRecord[j]))):
                            # 格式化中文字符统计
                            # value = unicode(str(list(allRecord[j])[k]), 'utf-8')
                            value = str(list(allRecord[j])[k]).encode('utf-8').decode('unicode_escape')
                            length = len(value)
                            utf8_length = len(value.encode('utf-8'))
                            length = (utf8_length - length) / 2 + length

                            varValues = varValues + str(list(allRecord[j])[k]) + u" " * (int(l_maxLen[k])-length) + u" "

                        printColor('', 'printDarkWhite', varValues)
                        noResult = 1

                    # 字段列表（底部显示）
                    printColor('\033[1;32;40m', 'printGreen', varFields)


                # 单表，模糊遍历记录 =========================================================================================
                elif "%" in varValue or "*" not in varValue:
                    # 模糊遍历字段
                    for i in allField:
                        if len(i[0]) > x: x = len(i[0])
                        if len(i[1]) > y: y = len(i[1])
                        tblFieldcount = tblFieldcount + 1
                    for j in allField:
                        if varType in j[1]:
                            list0.append(j[0])
                            list1.append(j[1])

                    # 输出值列表
                    l_value =[]
                    for i in range(0, len(list0)):
                        # list0[i]  字段名,如果字段名是关键字必须添加`
                        # self.cur.execute("select * from %s where `%s` like '%s'" % (varTable, list0[i], unicode(varValue, 'gbk')))
                        self.cur.execute("select * from %s where `%s` like '%s'" % (varTable, list0[i], varValue.encode('utf-8').decode('unicode_escape')))


                        t4 = self.cur.fetchall()
                        if len(t4) != 0:
                            printColor('\033[1;36;40m', 'printSkyBlue', tblDDL + u" , Result = " + list0[i] + u" , Records = " + str(len(t4)))
                            # 字段列表（顶部显示）
                            printColor('\033[1;32;40m', 'printGreen', varFields)
                            varAllValueCount = 0 # 统计所有值的数量，如1条记录10个值，那3条记录30个值
                            varFindRecordNumber = len(t4)  # 找到两条记录
                            for j in range(len(t4)):
                                varValues = ""
                                for k in range(len(list(t4[j]))):
                                    l_value.append(str(t4[j][k]))
                                    varAllValueCount = varAllValueCount + 1

                                    # 格式化中文字符统计
                                    # value = unicode(str(list(t4[j])[k]), 'utf-8')
                                    value = str(list(t4[j])[k]).encode('utf-8').decode('unicode_escape')
                                    length = len(value)
                                    utf8_length = len(value.encode('utf-8'))
                                    length = (utf8_length - length) / 2 + length

                                    varValues = varValues + str(list(t4[j])[k]) + u" " * (int(l_maxLen[k]) - length) + u" "

                                printColor('', 'printDarkWhite', varValues.lstrip(' ,'))
                                noResult = 1

                            # 输出字段的列表(底部)
                            printColor('\033[1;32;40m', 'printGreen', varFields)

                    # 搜索无结果
                    if noResult == 0:
                        printColor('\033[1;36;40m', 'printSkyBlue', u"no Result")
        else:
            printColor('\033[1;31;47m', 'printRed', u"errorrrrrrrrrr, 对象类型错误或不符合要求，如int,char,tinyint,smallint,timestamp,varchar,double,datetime 或搜索*缺少引号，应该为'*'！")
    def selectField(self, varTable, varType, varValue):
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
        x = y = tblFieldcount  = 0
        isMoreTables = 0  # 是否是针对多表查询
        noResult = 0
        # varType = 'char'  # 默认搜索字符型
        if varType in 'int,char,tinyint,smallint,timestamp,varchar,double,datetime':
            m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
            allTablesName = self.cur.fetchall()
            if varTable == u'*':  # 遍历所有表
                isMoreTables = 1
                m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
                t0 = self.cur.fetchall()
                printColor('\033[1;32;40m', 'printGreen', u"All of the " + str(len(t0)) + u" tables is traversed.")
            elif u"#" in varTable:  # 忽略表
                isMoreTables = 1
                if u"," in varTable:
                    # 忽略2个指定的表（表之间用逗号分隔）
                    varTable2 = varTable.split(u"#")[1]
                    varTable3 = varTable2.split(u",")
                    m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not regexp "%s|%s"' % (self.varDatabase, varTable3[0], varTable3[1]))
                    t0 = self.cur.fetchall()
                    printColor('\033[1;32;40m', 'printGreen', str(len(t0)) + u" of the " + str(len(allTablesName)) + u" tables is traversed. ignore(" + varTable3[0] + u" , " + varTable3[1] + u")")
                else:
                    # 不包含1个表或多个模糊的表，#rcd_order_info 遍历不包含rcd_order_info的所有表.
                    # Database_PO.searchKeyword(u"#rcd_%", u"char", u"wang")
                    # Database_PO.searchKeyword(u"#rcd_order_detail_2", u"char", u"张三")
                    varTable2 = varTable.split(u"#")[1]
                    m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not like "%s"' % (self.varDatabase, varTable2))
                    t0 = self.cur.fetchall()
                    printColor('\033[1;32;40m', 'printGreen', str(len(t0)) + u" of the " + str(len(allTablesName)) + u" tables is traversed. ignore(" + varTable2 + u")")
            elif u"%" in varTable:
                isMoreTables = 1
                m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (self.varDatabase, varTable))
                t0 = self.cur.fetchall()
                printColor('\033[1;32;40m', 'printGreen', str(len(t0)) + u" of the " + str(len(allTablesName)) + u" tables is traversed.")

            if isMoreTables == 1:
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
                            self.cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (self.varDatabase, varTable))
                            t2 = self.cur.fetchall()
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
                                self.cur.execute('select * from %s where `%s` like "%s"' % (varTable, list0[i], varValue))
                                t4 = self.cur.fetchall()
                                if len(t4) != 0:

                                    printColor('\033[1;36;40m', 'printSkyBlue', varTable + u"." + list0[i] + u"(" + str(len(t4)) + u")  " + tblDDL)

                                    # 获取字段名
                                    list33 = []
                                    for x in t2:
                                        list33.append(x[0])
                                    for j in range(len(t4)):
                                        varStr = ""
                                        for k in range(len(list(t4[j]))):
                                            varStr = varStr + u" , " + u"(" + list33[k] + u")" + str(list(t4[j])[k])

                                        printColor('', 'printDarkWhite', varStr.lstrip(' ,'))
                                        print(" ")
                                    noResult = 1
                        list0 = []
                        list1 = []
                        tblFieldcount = 0
                    if noResult == 0:
                        printColor('\033[1;36;40m', 'printSkyBlue', u"Result = 0")
                else:
                    printColor('\033[1;31;47m', 'printRed', u"errorrrrrrrrrr, 数据库（" + self.varDatabase + u"）中没有找到 " + varTable.split("%")[0] + u" 前缀的表!!!")

            # 单个表查询
            else:


                n = self.cur.execute(
                    'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                        self.varDatabase, varTable))
                if n != 0:
                    t1 = self.cur.fetchone()
                    printColor('\033[1;32;40m', 'printGreen', str(len(t1)) + u" of the " + str(len(allTablesName)) + u" tables is traversed.")

                    tblDDL = t1[0]
                    self.cur.execute(
                        'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (
                            self.varDatabase, varTable))
                    t2 = self.cur.fetchall()

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
                        self.cur.execute('select * from %s where `%s` like "%s"' % (varTable, list0[i], varValue))
                        t4 = self.cur.fetchall()
                        if len(t4) != 0:

                            printColor('\033[1;36;40m', 'printSkyBlue', varTable + u"." + list0[i] + u"(" + str(len(t4)) + u")  " + tblDDL)

                            # 获取字段名
                            list33 = []
                            for x in t2:
                                list33.append(x[0])

                            for j in range(len(t4)):
                                varStr = ""
                                for k in range(len(list(t4[j]))):
                                    varStr = varStr + u" , " + u"(" + list33[k] + u")" + str(list(t4[j])[k])

                                printColor('', 'printDarkWhite', varStr.lstrip(' ,'))
                                print(" ")
                            noResult = 1
                    if noResult == 0:
                        printColor('\033[1;36;40m', 'printSkyBlue', u"Result = 0")
                else:
                    printColor('\033[1;31;47m', 'printRed', u"errorrrrrrrrrr, 数据库（" + self.varDatabase + u"）中没有找到此表(" + varTable + u")!")
        else:
            printColor('\033[1;31;47m', 'printRed', u"errorrrrrrrrrr, 搜索对象错误或不符合要求，如搜索*缺少双引号，应该为'*'!!!")
    def selectDDL(self, varTable, varType, varValue):
        # 功能：模糊搜索关键字，遍历获取关键字的详细记录
        # 参数1 = 表(*表示搜索所有的表）
        # 参数2 = 数据类型 （如：char、int、tinyint、double、timestamp）
        # 参数3 = 关键字(不能为空,*通配符)
        # Database_PO.searchKeywordAll("*", "char", "a123456")
        # Database_PO.searchKeywordAll("*", "timestamp", "2017-10-15 23:29:47")
        # Database_PO.searchKeywordAll("*", "datetime", "2017-10-15 19:45:54")
        # Database_PO.searchKeywordAll('#rcd_order%', u'char', u'%814子项目2%')
        # 美化排列显示的变量
        listName = []
        listType = []
        listMemo = []
        varNameSize = varTypeSize = varMemoSize = 0
        list33 = []
        list44 = []
        list55 = []
        tblFieldCount = tblFieldCount2 = 0
        # varMoreTable = 1  # 多表
        isMoreTables = 0
        noResult = 0
        # varType = 'char'  # 默认搜索字符型

        if varType in 'int,char,tinyint,smallint,timestamp,varchar,double,datetime':
            # 获取数据库中表的数量
            m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
            allTablesName = self.cur.fetchall()
            if varTable == u'*':  # 遍历所有表
                isMoreTables = 1
                m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
                t0 = self.cur.fetchall()
                printColor('\033[1;32;40m', 'printGreen', u"All of the " + str(len(t0)) + u" tables is traversed.")
            elif u"#" in varTable:
                isMoreTables = 1
                if u"," in varTable:
                    # 忽略2个指定的表（表之间用逗号分隔）
                    varTable2 = varTable.split(u"#")[1]
                    varTable3 = varTable2.split(u",")
                    m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not regexp "%s|%s"' % (self.varDatabase, varTable3[0], varTable3[1]))
                    t0 = self.cur.fetchall()
                    printColor('\033[1;32;40m', 'printGreen', str(len(t0)) + u" of the " + str(len(allTablesName)) + u" tables is traversed. ignore(" + varTable3[0] + u" , " + varTable3[1] + u")")
                else:
                    # 忽略1个表或多个模糊的表， 如：#rcd_order_info 或 #rcd_order%
                    varTable2 = varTable.split(u"#")[1]
                    m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name not like "%s"' % (self.varDatabase, varTable2))
                    t0 = self.cur.fetchall()
                    printColor('\033[1;32;40m', 'printGreen', str(len(t0)) + u" of the " + str(len(allTablesName)) + u" tables is traversed. ignore(" + varTable2 + u")")
            elif u"%" in varTable: # 遍历部分表，如 *tt_% 表示tt_开头的表
                isMoreTables = 1
                m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (self.varDatabase, varTable))
                t0 = self.cur.fetchall()
                # if t0 == 0:
                printColor('\033[1;32;40m', 'printGreen', str(len(t0)) + u" of the " + str(len(allTablesName)) + u" tables is traversed.")

            if isMoreTables == 1:
                if m != 0:
                    # 遍历符合要求的表
                    for p in range(len(t0)):
                        varTable = t0[p][0]

                        # 获取表的comment， 如 用户表
                        self.cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s"' % (self.varDatabase, varTable))
                        t1 = self.cur.fetchone()
                        tblDDL = t1[0]
                        # print tblDDL

                        # 获取字段名、字段类型、字段备注
                        self.cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (
                                self.varDatabase, varTable))
                        t2 = self.cur.fetchall()
                        # print t2
                        for i in t2:
                            if len(i[0]) > varNameSize: varNameSize = len(i[0])
                            if len(i[1]) > varTypeSize: varTypeSize = len(i[1])
                            if len(i[2]) > varMemoSize: varMemoSize = len(i[2])
                            tblFieldCount = tblFieldCount + 1
                        for j in t2:
                            if varType in j[1]:
                                listName.append(j[0])
                                listType.append(j[1])
                                listMemo.append(j[2])
                        # 遍历符合关键字字段类型
                        for i in range(len(listName)):
                            self.cur.execute('select * from %s where `%s` like "%s"' % (varTable, listName[i], varValue))
                            t4 = self.cur.fetchall()
                            if len(t4) != 0:

                                # printColor('\033[1;36;40m', 'printSkyBlue', u"Result = " + str(len(
                                #     t4)) + u" , SearchWord = " + varValue + u" , DB = " + self.varDatabase + u" , Table = " + varTable + u" " + tblDDL + u" , Fields = " + str(
                                #     len(t2)) + u" , Position = " + listName[i])
                                printColor('\033[1;36;40m', 'printSkyBlue', varTable + u"." + listName[i] + u"(" + str(len(t4)) + u")  " + tblDDL)

                                for i in t2:
                                    list33.append(i[0] + u" " * (varNameSize - len(i[0])))
                                    list44.append(i[1] + u" " * (varTypeSize - len(i[1])))
                                    list55.append(str(i[2]).replace(u"\r", u"").replace(u" ", u"").replace(u"，", u"") + u"_" * (varMemoSize - len(i[2])+3))

                                # 遍历所有字段，输出结果
                                for j in range(len(t4)):
                                    for i in range(tblFieldCount):
                                        print(list33[i], list44[i], list55[i], list(t4[j])[i])
                                    print("\n")
                                noResult =1

                        listName = []; listType = []; listMemo = []; list33 = []; list44 = []; list55 = []

                        tblFieldCount = 0
                        varNameSize = varTypeSize = varMemoSize = 0
                    if noResult == 0:
                        printColor('\033[1;36;40m', 'printSkyBlue', u"Result = 0")
                else:
                    printColor('\033[1;31;47m', 'printRed', u"errorrrrrrrrrr, 数据库(" + self.varDatabase + u")中没有找到 " + varTable.split("*")[0] + u" 前缀的表!!!")

            # 单个表查询
            else:

                n = self.cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (self.varDatabase, varTable))
                if n != 0:
                    t1 = self.cur.fetchone()
                    printColor('\033[1;32;40m', 'printGreen', str(len(t1)) + u" of the " + str(len(allTablesName)) + u" tables is traversed.")
                    tblDDL = t1[0]
                    self.cur.execute(
                        'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (
                            self.varDatabase, varTable))
                    t2 = self.cur.fetchall()

                    for i in t2:
                        if len(i[0]) > varNameSize: varNameSize = len(i[0])
                        if len(i[1]) > varTypeSize: varTypeSize = len(i[1])
                        if len(i[2]) > varMemoSize: varMemoSize = len(i[2])
                        tblFieldCount = tblFieldCount + 1

                    for j in t2:
                        if varType in j[1]:
                            listName.append(j[0])
                            listType.append(j[1])
                            listMemo.append(j[2])
                    # print len(list0)   # 搜索的字段类型有多少个
                    for i in range(0, len(listName)):
                        # list0[i]  字段名,如果字段名是关键字必须添加`
                        self.cur.execute('select * from %s where `%s` like "%s"' % (varTable, listName[i], varValue))
                        t4 = self.cur.fetchall()
                        if len(t4) != 0:

                            # printColor('\033[1;36;40m', 'printSkyBlue', u"Result = " + str(len(
                            #     t4)) + u" , SearchWord = " + varValue + u" , DB = " + self.varDatabase + u" , Table = " + varTable + u" " + tblDDL + u" , Fields = " + str(
                            #     len(t2)) + u" , Position = " + listName[i])
                            printColor('\033[1;36;40m', 'printSkyBlue',
                                            varTable + u"." + listName[i] + u"(" + str(len(t4)) + u")  " + tblDDL)

                            for i in t2:
                                list33.append(i[0] + u" " * (varNameSize - len(i[0])))
                                list44.append(i[1] + u" " * (varTypeSize - len(i[1])))
                                list55.append(str(i[2]).replace(u"\r", u"").replace(u" ", u"").replace(u"，", u"") + u"_" * (varMemoSize - len(i[2]) + 3))

                                # 遍历所有字段，输出结果
                            for j in range(len(t4)):
                                for i in range(tblFieldCount):
                                    print(list33[i], list44[i], list55[i], list(t4[j])[i])
                                print("\n")
                            noResult = 1
                    if noResult == 0:
                        printColor('\033[1;36;40m', 'printSkyBlue', u"Result = 0")
                else:
                    printColor('\033[1;31;47m', 'printRed', u"errorrrrrrrrrr,  数据库(" + self.varDatabase + u")中没有找到此表(" + varTable + u")!!!")
        else:
            printColor('\033[1;31;47m', 'printRed', u"errorrrrrrrrrr, 搜索对象错误或不符合要求，如搜索*缺少双引号，应该为'*'!!!")

    def selectStructure(self, varTable, dimFields):
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
        isMoreTables = 0

        m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
        allTablesName = self.cur.fetchall()
        if varTable == u'*':  # 遍历所有表
            isMoreTables = 1
            m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s"' % (self.varDatabase))
            t0 = self.cur.fetchall()
            printColor('\033[1;32;40m', 'printGreen', u"All of the " + str(len(t0)) + u" tables is traversed.")
        elif u'%' in varTable:  # 遍历部分表，如 tt_store% 遍历tt_store开头的表
            isMoreTables = 1
            m = self.cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (self.varDatabase, varTable))
            t0 = self.cur.fetchall()
            printColor('\033[1;32;40m', 'printSkyBlue', str(len(t0)) + u" of the " + str(len(allTablesName)) + u" tables is traversed.")

        if isMoreTables == 1 :
            if m != 0:
                for p in range(len(t0)):  # 共有len(t0)张表
                    varTable = t0[p][0]
                    # 遍历指定的表
                    n = self.cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (self.varDatabase, varTable))
                    if n != 0:
                        t1 = self.cur.fetchone()
                        tblDDL = t1[0]
                        self.cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (self.varDatabase, varTable))
                        t2 = self.cur.fetchall()
                        self.cur.execute('select count(*) from %s' % (varTable))
                        t3 = self.cur.fetchall()
                        # '显示所有字段'
                        if dimFields == u"*":

                            printColor('\033[1;32;40m', 'printSkyBlue', tblDDL + u" , Fields = " + str(len(t2)))
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
                                printColor('\033[1;32;40m', 'printGreen', list0[i] + list1[i] + list2[i])

                            print("\n")
                        # '显示指定字段'
                        else:

                            for i in t2:
                                if len(i[0]) > x: x = len(i[0])
                                if len(i[1]) > y: y = len(i[1])
                            for i in t2:
                                for j in range(len(dimFields.split(","))):
                                    if i[0] == dimFields.split(",")[j]:
                                        list0.append(i[0] + ",")
                                        list1.append(i[1] + ",")
                                        ii = i[2].replace("\r\n", ",")
                                        list2.append(ii.replace("  ", ""))

                            var1 = 0
                            for i in range(len(dimFields.split(","))):
                                try:
                                    if list0[len(dimFields.split(","))-1] != "" :
                                        if var1 == 0:
                                            printColor('\033[1;32;40m', 'printSkyBlue', u"\n" + tblDDL + u" , Fields = " + str(t3[0][0]))
                                            var1 = 1
                                        printColor('\033[1;32;40m', 'printGreen', list0[i] + list1[i] + list2[i])

                                except:
                                    # printColor('\033[1;31;47m', 'printYellow', u"warning, 字段参数不存在。")
                                    pass
                    list0 = []
                    list1 = []
                    list2 = []
                    tblFieldcount = 0
            else:
                printColor('\033[1;31;47m', 'printRed', u"errorrrrrrrrrr , 数据库(" + self.varDatabase + u")中没有找到 " + varTable.split("%")[0] + u" 前缀的表!")

        # 单个表查询
        else:

            n = self.cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (self.varDatabase, varTable))
            if n != 0:
                t1 = self.cur.fetchone()
                tblDDL = t1[0]
                self.cur.execute(
                    'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (
                        self.varDatabase, varTable))
                t2 = self.cur.fetchall()
                self.cur.execute('select count(*) from %s' % (varTable))
                t3 = self.cur.fetchall()

                printColor('\033[1;32;40m', 'printSkyBlue', tblDDL + u" , Fields = " + str(t3[0][0]))

                if dimFields == u"*":
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
                        printColor('\033[1;32;40m', 'printGreen', list0[i] + list1[i] + list2[i])

                else:

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
                            printColor('\033[1;32;40m', 'printGreen', list0[i] + list1[i] + list2[i])
                        except:
                            printColor('\033[1;31;47m', 'printYellow', u"warning, 字段参数不存在。")
            else:
                printColor('\033[1;31;47m', 'printRed', u"errorrrrrrrrrr , 数据库（" + self.varDatabase + u"）中没有找到此表（" + varTable + u"）!!!")
    def selectW(self, varTable, rtnField, varWhere):
        # 功能：搜索带条件的结果
        # 输出 表备注、记录数、字段列表
        self.cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (self.varDatabase, varTable))
        t1 = self.cur.fetchone()
        tblDDL = t1[0]

        # 1个条件=======================================================================================================
        if "!" not in varWhere and "," not in varWhere:

            # 1个条件输出2个或多个字段 (最多5个字段) ===================================================================
            whereField = varWhere.split("=")[0]
            whereValue = str(varWhere.split("=")[1]).encode("utf-8")
            # 输出值列表
            self.cur.execute('select * from %s where %s="%s" ' % (varTable, whereField, whereValue))
            allRecord = self.cur.fetchall()
            printColor('\033[1;36;40m', 'printSkyBlue', tblDDL + u" , Records = " + str(len(allRecord)))

            if "," in rtnField:

                if len(str(rtnField).split(",")) == 2:
                    rtnField1 = str(rtnField).split(",")[0];rtnField2 = str(rtnField).split(",")[1]
                    varN = self.cur.execute('select %s,%s from %s where %s="%s" ' % (rtnField1, rtnField2, varTable, whereField, whereValue))
                elif len(str(rtnField).split(",")) == 3:
                    rtnField1 = str(rtnField).split(",")[0];rtnField2 = str(rtnField).split(",")[1];rtnField3 = str(rtnField).split(",")[2]
                    varN = self.cur.execute('select %s,%s,%s from %s where %s="%s" ' % (rtnField1, rtnField2, rtnField3, varTable, whereField, whereValue))
                elif len(str(rtnField).split(",")) == 4:
                    rtnField1 = str(rtnField).split(",")[0];rtnField2 = str(rtnField).split(",")[1];
                    rtnField3 = str(rtnField).split(",")[2];rtnField4 = str(rtnField).split(",")[3]
                    varN = self.cur.execute('select %s,%s,%s,%s from %s where %s="%s" ' % (rtnField1, rtnField2, rtnField3, rtnField4, varTable, whereField, whereValue))
                elif len(str(rtnField).split(",")) == 5:
                    rtnField1 = str(rtnField).split(",")[0];rtnField2 = str(rtnField).split(",")[1];
                    rtnField3 = str(rtnField).split(",")[2];rtnField4 = str(rtnField).split(",")[3];rtnField5 = str(rtnField).split(",")[4]
                    varN = self.cur.execute('select %s,%s,%s,%s,%s from %s where %s="%s" ' % (rtnField1, rtnField2, rtnField3, rtnField4, rtnField5, varTable, whereField, whereValue))

                if varN == 0:
                    printColor('\033[1;31;47m', 'printYellow',u"warning，表（" + varTable + u"）中未找到符合条件（" + whereField + u" = " + whereValue + u"）的 " + rtnField1 + u"," + rtnField2 + u"值!!!")
                else:
                    n = self.cur.fetchall()
                    # 输出2个字段
                    if len(str(rtnField).split(",")) == 2:
                        varMax1 = len(rtnField1)
                        for k in range(len(n)):
                            if len(str(n[k][0])) > varMax1: varMax1 = len(str(n[k][0]))
                        printColor('\033[1;31;47m', 'printGreen', rtnField1 + " " * (varMax1 - len(rtnField1)) + u"  " + rtnField2)
                        for i in range(len(n)):
                            print(str(n[i][0]) + " " * (varMax1 - len(str(n[i][0]))) + u" ", str(n[i][1]))
                    # 输出3个字段
                    elif len(str(rtnField).split(",")) == 3:
                        varMax1 = len(rtnField1)
                        varMax2 = len(rtnField2)
                        for k in range(len(n)):
                            if len(str(n[k][0])) > varMax1: varMax1 = len(str(n[k][0]))
                            if len(str(n[k][1])) > varMax2: varMax2 = len(str(n[k][1]))
                        printColor('\033[1;31;47m', 'printGreen', rtnField1 + " " * (varMax1 - len(rtnField1)+1) + u" " + rtnField2 + " " * (varMax2 - len(rtnField2)) + u"  " + rtnField3)
                        for i in range(len(n)):
                            print(str(n[i][0]) + " " * (varMax1 - len(str(n[i][0]))) + u" ", str(n[i][1]) + " " * (varMax2 - len(str(n[i][1])))+ u" ", n[i][2])
                    # 输出4个字段
                    elif len(str(rtnField).split(",")) == 4:
                        varMax1 = len(rtnField1)
                        varMax2 = len(rtnField2)
                        varMax3 = len(rtnField3)
                        for k in range(len(n)):
                            if len(str(n[k][0])) > varMax1: varMax1 = len(str(n[k][0]))
                            if len(str(n[k][1])) > varMax2: varMax2 = len(str(n[k][1]))
                            if len(str(n[k][2])) > varMax3: varMax3 = len(str(n[k][2]))
                        printColor('\033[1;31;47m', 'printGreen', rtnField1 + " " * (varMax1 - len(rtnField1)+1)
                        + u" " + rtnField2 + " " * (varMax2 - len(rtnField2))
                        + u"  " + rtnField3 + " " * (varMax3 - len(rtnField3)) + u"  " + rtnField4)
                        for i in range(len(n)):
                            print(str(n[i][0]) + " " * (varMax1 - len(str(n[i][0]))) + u" ", str(n[i][1]) + " " * (varMax2 - len(str(n[i][1]))) + u" ", str(n[i][2]) + " " * (varMax3 - len(str(n[i][2])))+ u" ", str(n[i][3]))
                    # 输出5个字段
                    elif len(str(rtnField).split(",")) == 5:
                        varMax1 = len(rtnField1);varMax2 = len(rtnField2)
                        varMax3 = len(rtnField3);varMax4 = len(rtnField4)
                        for k in range(len(n)):
                            if len(str(n[k][0])) > varMax1: varMax1 = len(str(n[k][0]))
                            if len(str(n[k][1])) > varMax2: varMax2 = len(str(n[k][1]))
                            if len(str(n[k][2])) > varMax3: varMax3 = len(str(n[k][2]))
                            if len(str(n[k][3])) > varMax4: varMax4 = len(str(n[k][3]))
                        printColor('\033[1;31;47m', 'printGreen', rtnField1 + " " * (varMax1 - len(rtnField1)+1) +u" "
                                        + rtnField2 + " " * (varMax2 - len(rtnField2)) + u"  "
                                        + rtnField3 + " " * (varMax3 - len(rtnField3)) + u"  "
                                        + rtnField4 + " " * (varMax4 - len(rtnField4)) + u"  "
                                        + rtnField5)
                        for i in range(len(n)):
                            print(str(n[i][0]) + " " * (varMax1 - len(str(n[i][0]))) + u" ", str(n[i][1]) + " " * (varMax2 - len(str(n[i][1]))) + u" ", str(n[i][2]) + " " * (varMax3 - len(str(n[i][2]))) + u" ", str(n[i][3]) + " " * (varMax4 - len(str(n[i][3]))) + u" ", str(n[i][4]))

            # 1个条件输出所有字段 ======================================================================================
            elif "*" in rtnField :

                # 遍历字段
                self.cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (self.varDatabase, varTable))
                allField = self.cur.fetchall()
                # 遍历值
                self.cur.execute('select * from %s where %s="%s" ' % (varTable, whereField, whereValue))
                allRecord = self.cur.fetchall()
                l_fieldLen =[]
                l_maxLen=[]
                l_valueLen=[]

                # 遍历每个字段的长度,生成列表l_fieldLen
                for i in range(len(allField)):
                    l_fieldLen.append(len(allField[i][0]))
                    l_maxLen.append(len(allField[i][0]))
                # print u"l_fieldLen = " + str(l_fieldLen)

                # 遍历每个值的长度并与字段长度比较，生成列表l_maxLen
                for j in range(len(allRecord)):
                    for k in range(len(list(allRecord[j]))):
                        l_valueLen.append(len(str(list(allRecord[j])[k])))
                        if l_maxLen[k] < l_valueLen[k]: l_maxLen[k] = l_valueLen[k]
                        if l_maxLen[k] < l_fieldLen[k]: l_maxLen[k] = l_fieldLen[k]
                    l_valueLen = []
                # print u"l_maxLen = " + str(l_maxLen)

                # 输出字段的列表
                varFields = ""
                for i in range(len(allField)):
                    # 如果列表中最大字段数大于19，则宽度固定20
                    # if l_maxLen[i] > 19:
                    #     varFields = varFields + str(list(allField[i])[0]) + u" " * (20 - int(l_fieldLen[i])) + u"  "
                    # else:
                    varFields = varFields + str(list(allField[i])[0]) + u" " * (int(l_maxLen[i]) - int(l_fieldLen[i])) + u"  "

                # 字段列表（顶部显示）
                printColor('\033[1;32;40m', 'printGreen', varFields)

                for j in range(len(allRecord)):
                    varValues = ""
                    for k in range(len(list(allRecord[j]))):
                        # if len(str(list(allRecord[j])[k])) > 19:
                        #     # 判断变量中是否包含中文
                        #     if self.BasePage.check_contain_chinese(str(list(allRecord[j])[k]).encode("utf-8")) == True:
                        #         varValues = varValues + str(list(allRecord[j])[k][:9]) + u"... "
                        #     else:
                        #         varValues = varValues + str(list(allRecord[j])[k][:17]) + u"...  "
                        # elif int(l_maxLen[k]) > 20:
                        #     varValues = varValues + str(list(allRecord[j])[k]) + u" " * (20 - len(str(list(allRecord[j])[k]))) + u"  "
                        # else:
                        varValues = varValues + str(list(allRecord[j])[k]) + u" " * (int(l_maxLen[k]) - len(str(list(allRecord[j])[k]))) + u"  "
                    printColor('', 'printDarkWhite', varValues)

                # 字段列表（底部显示）
                printColor('\033[1;32;40m', 'printGreen', varFields)

            # 1个条件输出1个字段 =======================================================================================
            else:

                varN = self.cur.execute('select %s from %s where %s="%s" ' % (rtnField, varTable, whereField, whereValue))
                if varN == 0:
                    printColor('\033[1;31;47m', 'printYellow',
                                    u"warning, 表（" + varTable + u"）中未找到符合条件（" + whereField + u" = " + whereValue + u"）的 " + rtnField + u"值!!!")
                elif varN == 1:
                    printColor('\033[1;31;47m', 'printGreen', rtnField)
                    print(str(self.cur.fetchone()[0]))
                else:
                    n = self.cur.fetchall()
                    printColor('\033[1;31;47m', 'printGreen', rtnField)
                    for i in range(len(n)):
                        print(n[i][0])


        # 2个条件 ======================================================================================================
        else:

            # 2个条件输出2个或多个字段（最多5个字段）
            if "," in rtnField:

                if "!" in varWhere and "," not in varWhere:
                    tmpwhereField1 = str(varWhere).split("!")[0]
                    whereField1 = tmpwhereField1.split("=")[0]
                    whereValue1 = str(tmpwhereField1.split("=")[1]).encode("utf-8")
                    tmpwhereField2 = str(varWhere).split("!")[1]
                    whereField2 = tmpwhereField2.split("=")[0]
                    whereValue2 = str(tmpwhereField2.split("=")[1]).encode("utf-8")

                    if len(str(rtnField).split(",")) == 2:
                        rtnField1 = str(rtnField).split(",")[0];
                        rtnField2 = str(rtnField).split(",")[1]
                        varN = self.cur.execute('select %s,%s from %s where %s="%s" or %s="%s" ' % (rtnField1, rtnField2, varTable, whereField1, whereValue1, whereField2, whereValue2))

                    if len(str(rtnField).split(",")) == 3:
                        rtnField1 = str(rtnField).split(",")[0];rtnField2 = str(rtnField).split(",")[1]
                        rtnField3 = str(rtnField).split(",")[2]
                        varN = self.cur.execute('select %s,%s,%s from %s where %s="%s" or %s="%s" ' % (rtnField1, rtnField2, rtnField3, varTable, whereField1, whereValue1, whereField2, whereValue2))
                    if len(str(rtnField).split(",")) == 4:
                        rtnField1 = str(rtnField).split(",")[0];rtnField2 = str(rtnField).split(",")[1]
                        rtnField3 = str(rtnField).split(",")[2];rtnField4 = str(rtnField).split(",")[3]
                        varN = self.cur.execute('select %s,%s,%s,%s from %s where %s="%s" or %s="%s" ' % (rtnField1, rtnField2, rtnField3, rtnField4, varTable, whereField1, whereValue1, whereField2, whereValue2))
                    if len(str(rtnField).split(",")) == 5:
                        rtnField1 = str(rtnField).split(",")[0];rtnField2 = str(rtnField).split(",")[1]
                        rtnField3 = str(rtnField).split(",")[2];rtnField4 = str(rtnField).split(",")[3];rtnField5 = str(rtnField).split(",")[4]
                        varN = self.cur.execute('select %s,%s,%s,%s,%s from %s where %s="%s" or %s="%s" ' % (rtnField1, rtnField2, rtnField3, rtnField4, rtnField5, varTable, whereField1, whereValue1, whereField2, whereValue2))
                if "," in varWhere and "!" not in varWhere:
                    tmpwhereField1 = str(varWhere).split(",")[0]
                    whereField1 = tmpwhereField1.split("=")[0]
                    whereValue1 = str(tmpwhereField1.split("=")[1]).encode("utf-8")
                    tmpwhereField2 = str(varWhere).split(",")[1]
                    whereField2 = tmpwhereField2.split("=")[0]
                    whereValue2 = str(tmpwhereField2.split("=")[1]).encode("utf-8")
                    if len(str(rtnField).split(",")) == 2:
                        rtnField1 = str(rtnField).split(",")[0];
                        rtnField2 = str(rtnField).split(",")[1]
                        varN = self.cur.execute('select %s,%s from %s where %s="%s" and %s="%s" ' % (
                        rtnField1, rtnField2, varTable, whereField1, whereValue1, whereField2, whereValue2))
                    if len(str(rtnField).split(",")) == 3:
                        rtnField1 = str(rtnField).split(",")[0];
                        rtnField2 = str(rtnField).split(",")[1]
                        rtnField3 = str(rtnField).split(",")[2]
                        varN = self.cur.execute('select %s,%s,%s from %s where %s="%s" and %s="%s" ' % (
                        rtnField1, rtnField2, rtnField3, varTable, whereField1, whereValue1, whereField2, whereValue2))
                    if len(str(rtnField).split(",")) == 4:
                        rtnField1 = str(rtnField).split(",")[0];
                        rtnField2 = str(rtnField).split(",")[1]
                        rtnField3 = str(rtnField).split(",")[2];
                        rtnField4 = str(rtnField).split(",")[3]
                        varN = self.cur.execute('select %s,%s,%s,%s from %s where %s="%s" and %s="%s" ' % (
                        rtnField1, rtnField2, rtnField3, rtnField4, varTable, whereField1, whereValue1, whereField2,
                        whereValue2))
                    if len(str(rtnField).split(",")) == 5:
                        rtnField1 = str(rtnField).split(",")[0];
                        rtnField2 = str(rtnField).split(",")[1]
                        rtnField3 = str(rtnField).split(",")[2];
                        rtnField4 = str(rtnField).split(",")[3];
                        rtnField5 = str(rtnField).split(",")[4]
                        varN = self.cur.execute('select %s,%s,%s,%s,%s from %s where %s="%s" and %s="%s" ' % (
                        rtnField1, rtnField2, rtnField3, rtnField4, rtnField5, varTable, whereField1, whereValue1,
                        whereField2, whereValue2))

                if varN == 0:
                    printColor('\033[1;31;47m', 'printYellow',u"warning，表（" + varTable + u"）中未找到符合条件（" + whereField1 + u" = " + whereValue1 + u" 且 " + whereField2 + u" = " + whereValue2 + u"）的 " + rtnField1 + u"," + rtnField2 + u"值!!!")
                else:
                    n = self.cur.fetchall()
                    # 输出2个字段
                    if len(str(rtnField).split(",")) == 2:
                        varMax1 = len(rtnField1)
                        for k in range(len(n)):
                            if len(str(n[k][0])) > varMax1: varMax1 = len(str(n[k][0]))
                        printColor('\033[1;31;47m', 'printGreen', rtnField1 + " " * (varMax1 - len(rtnField1)) + u" " + rtnField2)
                        for i in range(len(n)):
                            print(str(n[i][0]) + " " * (varMax1 - len(str(n[i][0]))), str(n[i][1]))
                    # 输出3个字段
                    elif len(str(rtnField).split(",")) == 3:
                        varMax1 = len(rtnField1)
                        varMax2 = len(rtnField2)
                        for k in range(len(n)):
                            if len(str(n[k][0])) > varMax1: varMax1 = len(str(n[k][0]))
                            if len(str(n[k][1])) > varMax2: varMax2 = len(str(n[k][1]))
                        printColor('\033[1;31;47m', 'printGreen',
                                        rtnField1 + " " * (varMax1 - len(rtnField1)) + u" " +
                                        rtnField2 + " " * (varMax2 - len(rtnField2)) + u" " +
                                        rtnField3)
                        for i in range(len(n)):
                            print(str(n[i][0]) + " " * (varMax1 - len(str(n[i][0]))) , str(n[i][1])+ " " * (varMax2 - len(str(n[i][1]))) , str(n[i][2]))
                    # 输出4个字段
                    elif len(str(rtnField).split(",")) == 4:
                        varMax1 = len(rtnField1);varMax2 = len(rtnField2)
                        varMax3 = len(rtnField3)
                        for k in range(len(n)):
                            if len(str(n[k][0])) > varMax1: varMax1 = len(str(n[k][0]))
                            if len(str(n[k][1])) > varMax2: varMax2 = len(str(n[k][1]))
                            if len(str(n[k][2])) > varMax3: varMax3 = len(str(n[k][2]))
                        printColor('\033[1;31;47m', 'printGreen',
                                        rtnField1 + " " * (varMax1 - len(rtnField1)) + u" " +
                                        rtnField2 + " " * (varMax2 - len(rtnField2)) + u" " +
                                        rtnField3 + " " * (varMax3 - len(rtnField3)) + u" " +
                                        rtnField4)
                        for i in range(len(n)):
                            print(str(n[i][0]) + " " * (varMax1 - len(str(n[i][0]))), \
                                str(n[i][1]) + " " * (varMax2 - len(str(n[i][1]))), \
                                str(n[i][2]) + " " * (varMax3 - len(str(n[i][2]))), str(n[i][3]))
                    # 输出5个字段
                    elif len(str(rtnField).split(",")) == 5:
                        varMax1 = len(rtnField1)
                        varMax2 = len(rtnField2)
                        varMax3 = len(rtnField3)
                        varMax4 = len(rtnField4)
                        for k in range(len(n)):
                            if len(str(n[k][0])) > varMax1: varMax1 = len(str(n[k][0]))
                            if len(str(n[k][1])) > varMax2: varMax2 = len(str(n[k][1]))
                            if len(str(n[k][2])) > varMax3: varMax3 = len(str(n[k][2]))
                            if len(str(n[k][3])) > varMax4: varMax4 = len(str(n[k][3]))
                        printColor('\033[1;31;47m', 'printGreen',
                                        rtnField1 + " " * (varMax1 - len(rtnField1)) + u" " +
                                        rtnField2 + " " * (varMax2 - len(rtnField2)) + u" " +
                                        rtnField3 + " " * (varMax3 - len(rtnField3)) + u" " +
                                        rtnField4 + " " * (varMax4 - len(rtnField4)) + u" " +
                                        rtnField5)
                        for i in range(len(n)):
                            print(str(n[i][0]) + " " * (varMax1 - len(str(n[i][0]))), \
                                str(n[i][1]) + " " * (varMax2 - len(str(n[i][1]))), \
                                str(n[i][2]) + " " * (varMax3 - len(str(n[i][2]))), \
                                str(n[i][3]) + " " * (varMax4 - len(str(n[i][3]))), \
                                str(n[i][4]))

            # 2个条件输出所有字段 ======================================================================================
            elif "*" in rtnField:

                # 遍历字段
                self.cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (self.varDatabase, varTable))
                allField = self.cur.fetchall()

                l_fieldLen = []
                l_maxLen = []
                l_valueLen = []

                # 遍历每个字段的长度,生成列表l_fieldLen
                for i in range(len(allField)):
                    l_fieldLen.append(len(allField[i][0]))
                    l_maxLen.append(len(allField[i][0]))
                # print u"l_fieldLen = " + str(l_fieldLen)

                # 遍历 or
                if "!" in varWhere and "," not in varWhere:
                    tmpwhereField1 = str(varWhere).split("!")[0]
                    whereField1 = tmpwhereField1.split("=")[0]
                    whereValue1 = str(tmpwhereField1.split("=")[1]).encode("utf-8")
                    tmpwhereField2 = str(varWhere).split("!")[1]
                    whereField2 = tmpwhereField2.split("=")[0]
                    whereValue2 = str(tmpwhereField2.split("=")[1]).encode("utf-8")
                    self.cur.execute('select * from %s where %s="%s" or %s="%s" ' % (varTable, whereField1, whereValue1, whereField2, whereValue2))

                # 遍历 and
                if "," in varWhere and "!" not in varWhere:
                    tmpwhereField1 = str(varWhere).split(",")[0]
                    whereField1 = tmpwhereField1.split("=")[0]
                    whereValue1 = str(tmpwhereField1.split("=")[1]).encode("utf-8")
                    tmpwhereField2 = str(varWhere).split(",")[1]
                    whereField2 = tmpwhereField2.split("=")[0]
                    whereValue2 = str(tmpwhereField2.split("=")[1]).encode("utf-8")
                    self.cur.execute('select * from %s where %s="%s" and %s="%s" ' % (varTable, whereField1, whereValue1, whereField2, whereValue2))

                allRecord = self.cur.fetchall()
                printColor('\033[1;36;40m', 'printSkyBlue', tblDDL + u" , Records = " + str(len(allRecord)))

                # 遍历每个值的长度并与字段长度比较，生成列表l_maxLen
                for j in range(len(allRecord)):
                    for k in range(len(list(allRecord[j]))):
                        l_valueLen.append(len(str(list(allRecord[j])[k])))
                        if l_maxLen[k] < l_valueLen[k]: l_maxLen[k] = l_valueLen[k]
                        if l_maxLen[k] < l_fieldLen[k]: l_maxLen[k] = l_fieldLen[k]
                    l_valueLen = []
                # print u"l_maxLen = " + str(l_maxLen)

                # 输出字段的列表（顶部）
                varFields = ""
                for i in range(len(allField)):
                    # 如果列表中最大字段数大于19，则宽度固定20
                    if l_maxLen[i] > 19:
                        varFields = varFields + str(list(allField[i])[0]) + u" " * (20 - int(l_fieldLen[i])) + u"  "
                    else:
                        varFields = varFields + str(list(allField[i])[0]) + u" " * (
                        int(l_maxLen[i]) - int(l_fieldLen[i])) + u"  "

                printColor('\033[1;32;40m', 'printGreen', varFields)

                for j in range(len(allRecord)):
                    varValues = ""
                    for k in range(len(list(allRecord[j]))):
                        if len(str(list(allRecord[j])[k])) > 19:
                            # 判断变量中是否包含中文
                            if self.BasePage.check_contain_chinese(
                                    str(list(allRecord[j])[k]).encode("utf-8")) == True:
                                varValues = varValues + str(list(allRecord[j])[k][:9]) + u"... "
                            else:
                                varValues = varValues + str(list(allRecord[j])[k][:17]) + u"...  "
                        elif int(l_maxLen[k]) > 20:
                            varValues = varValues + str(list(allRecord[j])[k]) + u" " * (
                                20 - len(str(list(allRecord[j])[k]))) + u"  "
                        else:
                            varValues = varValues + str(list(allRecord[j])[k]) + u" " * (
                                int(l_maxLen[k]) - len(str(list(allRecord[j])[k]))) + u"  "
                    printColor('', 'printDarkWhite', varValues)


            # 2个条件输出1个字段 =======================================================================================
            else:

                if "!" in varWhere and "," not in varWhere:
                    tmpwhereField1 = str(varWhere).split("!")[0]
                    whereField1 = tmpwhereField1.split("=")[0]
                    whereValue1 = str(tmpwhereField1.split("=")[1]).encode("utf-8")
                    tmpwhereField2 = str(varWhere).split("!")[1]
                    whereField2 = tmpwhereField2.split("=")[0]
                    whereValue2 = str(tmpwhereField2.split("=")[1]).encode("utf-8")
                    self.cur.execute('select * from %s where %s="%s" or %s="%s" ' % (varTable, whereField1, whereValue1, whereField2, whereValue2))
                    allRecord = self.cur.fetchall()
                    printColor('\033[1;36;40m', 'printSkyBlue', tblDDL + u" , Records = " + str(len(allRecord)))
                    varN = self.cur.execute('select %s from %s where %s="%s" or %s="%s" ' % (rtnField, varTable, whereField1, whereValue1, whereField2, whereValue2))

                if "," in varWhere and "!" not in varWhere:
                    tmpwhereField1 = str(varWhere).split(",")[0]
                    whereField1 = str(tmpwhereField1.split("=")[0]).encode("utf-8")
                    whereValue1 = tmpwhereField1.split("=")[1]
                    tmpwhereField2 = str(varWhere).split(",")[1]
                    whereField2 = tmpwhereField2.split("=")[0]
                    whereValue2 = str(tmpwhereField2.split("=")[1]).encode("utf-8")
                    self.cur.execute('select * from %s where %s="%s" and %s="%s" ' % (varTable, whereField1, whereValue1, whereField2, whereValue2))
                    allRecord = self.cur.fetchall()
                    printColor('\033[1;36;40m', 'printSkyBlue', tblDDL + u" , Records = " + str(len(allRecord)))
                    varN = self.cur.execute('select %s from %s where %s="%s" and %s="%s" ' % (rtnField, varTable, whereField1, whereValue1, whereField2, whereValue2))

                if varN == 0:
                    printColor('\033[1;31;47m', 'printYellow', u"warning, 表（" + varTable + u"）中未找到符合条件（" + whereField1 + u" = " + whereValue1 + u" 且 " + whereField2 + u" = " + whereValue2 + u"）的 " + rtnField + u"值!!!")
                elif varN == 1:
                    printColor('\033[1;31;47m', 'printGreen', rtnField)
                    print(str(self.cur.fetchone()[0]))
                else:
                    n = self.cur.fetchall()
                    printColor('\033[1;31;47m', 'printGreen', rtnField)
                    for i in range(len(n)):
                        print(n[i][0])
    def rtnCount(self, varTable):
        # 功能：select，1个条件并返回rtnField值
        # 参数1 = 表(不能为空）
        # x = Database_PO.tblCountAll("tt_user_login")
        varN = ""
        varN = self.cur.execute('select count(*) from %s ' % (varTable))
        if varN == 0:
            printColor('\033[1;31;47m', 'printYellow', u"warning，表（" + varTable + u"）中未找到符合条件的值!")
            return None
        else:
            return str(self.cur.fetchone()[0])
    def rtnCountW(self, varTable, varWhere):
        # 功能：搜索1个条件返回统计数量
        # x = Database_PO.rtnCountW("tt_store", "store_id", "1")
        varN = ""
        if "=" in varWhere:
            whereField = varWhere.split("=")[0]
            whereValue = varWhere.split("=")[1]
            varN = self.cur.execute('select count(%s) from %s where %s="%s" ' % (whereField, varTable, whereField, whereValue))
            if varN == 0:
                printColor('\033[1;31;47m', 'printYellow', u"warning，表（" + varTable + u"）中未找到符合条件（" + whereField + u" = " + whereValue + u"）的值!!!")
                return None
            else:
                return str(self.cur.fetchone()[0])
        else:
            printColor('\033[1;31;47m', 'printRed', u"错误，条件中缺少等于号")
    def updateW(self, varTable, varUpdate, varWhere):
        # 功能：update，依据1个条件更新某个字段值，更新前先select查询显示记录（-sf方式显示），更新前二次确认。
        # x = Database_PO.tblWhere1Update1("tt_store", "is_need_approve", "0", "user_name", "666001")
        list0 =[];list1 =[];list33 = []
        varMoreWhere = ""

        if "=" in varUpdate:
            updateField = str(varUpdate).split("=")[0]
            updateValue = str(varUpdate).split("=")[1]
            updateValue = updateValue.encode("utf-8")
        if "=" in varWhere:
            whereField = str(varWhere).split("=")[0]
            whereValue = str(varWhere).split("=")[1]
            whereValue = whereValue.encode("utf-8")

        if "!" in varWhere and "," not in varWhere:
            tmpwhereField1 = str(varWhere).split("!")[0]
            whereField1 = tmpwhereField1.split("=")[0]
            whereValue1 = tmpwhereField1.split("=")[1]
            whereValue1 = whereValue1.encode("utf-8")
            tmpwhereField2 = str(varWhere).split("!")[1]
            whereField2 = tmpwhereField2.split("=")[0]
            whereValue2 = tmpwhereField2.split("=")[1]
            whereValue2 = whereValue2.encode("utf-8")
            varMoreWhere = "or"
        if "," in varWhere and "!" not in varWhere:
            tmpwhereField1 = str(varWhere).split(",")[0]
            whereField1 = tmpwhereField1.split("=")[0]
            whereValue1 = tmpwhereField1.split("=")[1]
            whereValue1 = whereValue1.encode("utf-8")
            tmpwhereField2 = str(varWhere).split(",")[1]
            whereField2 = tmpwhereField2.split("=")[0]
            whereValue2 = tmpwhereField2.split("=")[1]
            whereValue2 = whereValue2.encode("utf-8")
            varMoreWhere = "and"

        n = self.cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (self.varDatabase, varTable))
        if n != 0:
            t1 = self.cur.fetchone()
            self.cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (self.varDatabase, varTable))
            t2 = self.cur.fetchall()
            for j in t2:
                list0.append(j[0])
                list1.append(j[1])

            if varMoreWhere == "":
                # 1个条件
                self.cur.execute('select * from %s where `%s` = "%s"' % (varTable, whereField, whereValue))
            else:
                # 2个条件
                if varMoreWhere == "and" :
                    self.cur.execute('select * from %s where %s="%s" and %s="%s"' % (varTable, whereField1, whereValue1, whereField2, whereValue2))
                if varMoreWhere == "or":
                    self.cur.execute('select * from %s where %s="%s" or %s="%s"' % (varTable, whereField1, whereValue1, whereField2, whereValue2))

            t4 = self.cur.fetchall()
            if len(t4) != 0:
                # 获取字段名
                for x in t2:
                    list33.append(x[0])
                printColor('\033[1;31;47m', 'printGreen', "[select * from " + varTable + " where " + whereField + "=" + whereValue + "]")
                for j in range(len(t4)):
                    varStr = ""
                    for k in range(len(list(t4[j]))):
                        varStr = varStr + u" , " + u"(" + list33[k] + u")" + str(list(t4[j])[k])
                    printColor('', 'printDarkWhite', varStr.lstrip(' ,'))
                    print(" ")
                # x = input(unicode("搜索到 " + str(len(t4)) + " 条记录，是否立即更新 Y/N ?  ", 'utf-8').encode('gbk')).decode(sys.stdin.encoding)
                x = input("搜索到 " + str(len(t4)) + " 条记录，是否立即更新 Y/N ?  ".encode('utf-8')).decode('unicode_escape')
                if x == "y" or x == "Y":
                    printColor('\033[1;31;47m', 'printGreen', "\n[update " + varTable + " set " + updateField + "=" +updateValue + " where " + whereField + "=" + whereValue + "]")
                    if varMoreWhere == "":
                        varN = self.cur.execute('update %s set %s=%s where %s=%s ' % (varTable, updateField, updateValue, whereField, whereValue))
                    else:
                        if varMoreWhere == "and" :
                            varN = self.cur.execute('update %s set %s=%s where %s=%s and %s=%s' % (varTable, updateField, updateValue, whereField1, whereValue1, whereField2, whereValue2))
                        if varMoreWhere == "or" :
                            varN = self.cur.execute('update %s set %s=%s where %s=%s or %s=%s' % (varTable, updateField, updateValue, whereField1, whereValue1, whereField2, whereValue2))
                    self.conn.commit()
                    if varN == 0:
                        printColor('\033[1;31;47m', 'printYellow', u"warning，更新的字段值与原值一样！\n")
                    else:
                        printColor('\033[1;31;47m', 'printGreen', u"已更新 " + str(varN) + u" 条记录。")
            else:
                if varMoreWhere == "":
                    printColor('\033[1;31;47m', 'printYellow',u"warning，表（" + varTable + u"）中未找到此条件（" + whereField + u" = " + whereValue + u"）\n")
                else:
                    # 2个条件
                    if varMoreWhere == "and":
                        printColor('\033[1;31;47m', 'printYellow',u"warning，表（" + varTable + u"）中未找到此条件（" + whereField1 + u" = " + whereValue1  + u" 与 " + whereField2 + u" = " + whereValue2 + u"）\n")
                    if varMoreWhere == "or":
                        printColor('\033[1;31;47m', 'printYellow',u"warning，表（" + varTable + u"）中未找到此条件（" + whereField1 + u" = " + whereValue1  + u" 或 " + whereField2 + u" = " + whereValue2 + u"）\n")
