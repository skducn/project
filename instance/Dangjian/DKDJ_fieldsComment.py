# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John   # coding: utf-8
# Date       : 2017-4-7
# Description: 党建数据库中所有的表,获取字段\类型\注释
# *******************************************************************************************************************************
from DKDJ_Param import *
# *******************************************************************************************************************************
import json

def getTblNameTypeDDL(varDatabase, varTable, varFields):
    # 获取数据库表字段、类型、DDL
    # 参数1 = 数据库
    # 参数2 = 表(如为空表示所有表，可遍历带指定前缀名的表)
    # 参数3 = 字段(多个字段用逗号分割，为空表示所有字段)
    list0 = []; list1 = []; list2 = []; x = y = tblFieldcount = 0
    if varTable != "":
        if "*" in varTable:
            varTable2 = varTable.split("*")[0] + "%"  # t_store_%
            m = cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (varDatabase,varTable2))
            if m != 0:
                t0=cur.fetchall()
                for p in range(len(t0)):  #  共有len(t0)张表
                    varTable = t0[p][0]
                    # 遍历指定的表
                    n = cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
                    if n != 0:
                        t1=cur.fetchone()
                        tblDDL = t1[0]
                        cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
                        t2=cur.fetchall()
                        print "\n[" + varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(len(t2)) + "]"
                        print "-" * 70
                        for i in t2:
                            if len(i[0]) > x: x = len(i[0])
                            if len(i[1]) > y: y = len(i[1])
                            tblFieldcount = tblFieldcount + 1
                        for i in t2:
                            list0.append(i[0] + " "*(x-len(i[0])+1))
                            list1.append(i[1] + " "*(y-len(i[1])+1))
                            ii=i[2].replace("\r\n", ",")
                            list2.append(ii.replace("  ", ""))
                        for i in range(tblFieldcount):
                            print list0[i], list1[i], list2[i]
                    list0 = []; list1 = []; list2 = []
                    tblFieldcount = 0
            else: print "[errorrrrrrr , 数据库("+varDatabase+")中没有找到 " + varTable.split("*")[0] + " 前缀的表!]"
        elif "*" not in varTable:
            # 遍历指定的表
            n = cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
            if n != 0:
                t1 = cur.fetchone()
                tblDDL = t1[0]
                cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
                t2 = cur.fetchall()
                if varFields == "":
                    print "\n[" + varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(len(t2)) + "]"
                    print "-" * 70
                    for i in t2:
                        if len(i[0]) > x: x = len(i[0])
                        if len(i[1]) > y: y = len(i[1])
                        tblFieldcount = tblFieldcount + 1
                    for i in t2:
                        list0.append(i[0] + " "*(x-len(i[0])+1))
                        list1.append(i[1] + " "*(y-len(i[1])+1))
                        ii=i[2].replace("\r\n", ",")
                        list2.append(ii.replace("  ", ""))
                    for i in range(tblFieldcount):
                        print list0[i], list1[i], list2[i]
                else:
                    print "\n[" + varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(len(varFields.split(","))) + "]"
                    print "-" * 70
                    for i in t2:
                        if len(i[0]) > x: x = len(i[0])
                        if len(i[1]) > y: y = len(i[1])
                    for i in t2:
                        for j in range(len(varFields.split(","))):
                            if i[0] == varFields.split(",")[j]:
                                list0.append(i[0] + " "*(x-len(i[0])+1))
                                list1.append(i[1] + " "*(y-len(i[1])+1))
                                ii=i[2].replace("\r\n", ",")
                                list2.append(ii.replace("  ", ""))
                    for i in range(len(varFields.split(","))):
                        try:
                            print list0[i], list1[i], list2[i]
                        except:
                            print "[??? Errorrrrrrr , 参数3中部分字段不存在!]"
            else:
                print "[errorrrrrrr , 数据库(" + varDatabase + ")中没有找到 " + varTable + "表!]"
    else:
        cur.execute('select TABLE_NAME,TABLE_COMMENT from information_schema.`TABLES` where table_schema="%s" ' % varDatabase)
        tblname=cur.fetchall()
        for k in range(len(tblname)):
            cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDatabase,tblname[k][0]))
            t2 = cur.fetchall()
            print "\n[" + varDatabase + " > " + tblname[k][0] + "(" + tblname[k][1] + ") > " + str(len(t2)) + "fields]"
            print "-" * 70
            for i in t2:
                if len(i[0]) > x: x = len(i[0])
                if len(i[1]) > y: y = len(i[1])
                tblFieldcount = tblFieldcount + 1
            for i in t2:
                list0.append(i[0] + " "*(x-len(i[0])+1))
                list1.append(i[1] + " "*(y-len(i[1])+1))
                list2.append(i[2])
            for i in range(tblFieldcount):
                print list0[i], list1[i], list2[i]
            list0 = []; list1 = []; list2 = []
            tblFieldcount = 0

# 用法1：获取 数据库中所有表的字段、类型、DDL
# getTblNameTypeDDL('dangjian', '', '')
# getTblNameTypeDDL('scenemsg', '', '')
# getTblNameTypeDDL('sysparam', '', '')
# getTblNameTypeDDL('upload', '', '')

# 用法2：获取 数据库某表中所有字段、类型、DDL
# getTblNameTypeDDL('dangjian', 'tt_user_login', '')
# getTblNameTypeDDL('personal', 't_share', '')
# getTblNameTypeDDL('personal', 't_user', '')
# getTblNameTypeDDL('personal', 't_user_complaint', '')
# getTblNameTypeDDL('personal', 't_user_friends', '')
# getTblNameTypeDDL('personal', 't_user_friends_apply', '')
# getTblNameTypeDDL('personal', 't_user_label', '')
# getTblNameTypeDDL('personal', 't_user_label_memberinfo', '')
# getTblNameTypeDDL('personal', 't_user_private_info', '')
# getTblNameTypeDDL('personal', 't_user_setting', '')
# getTblNameTypeDDL('scenemsg', 't_scene_msg', '')
# getTblNameTypeDDL('sysparam', 't_dict_circle', '')
# getTblNameTypeDDL('sysparam', 't_dict_industry', '')
# getTblNameTypeDDL('sysparam', 't_dict_region', '')
# getTblNameTypeDDL('upload', 'uploadfile', '')

# 用法3：获取 数据库某表中个部分字段、类型、DDL，如只需要获取2个字段 (字段名与数据库表中名字需大小写一致)
# getTblNameTypeDDL('personal', 't_user', 'id,sex,nickName')

# 用法4：获取 数据库带"t_user"前缀表的所有字段、类型、DDL （注意：前缀*）
# getTblNameTypeDDL('personal', 't_user_label*', '')


def getTblCreateTime(varDatabase, varTable, varStatus, varAfterTime):
    # 获取 表的创建时间
    # 参数1 = 数据库
    # 参数2 = 表
    # 参数3 = 指定日期前或后 （before表示指定日期之前创建、after表示指定日期之后创建）
    # 参数4 = 日期
    print "-" * 70
    if varDatabase != "":
        try:
            if varTable != "":
                cur.execute('select create_time from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDatabase, varTable))
                t3 = cur.fetchone()
                print "[" + varDatabase+"." + varTable + " 表的创建时间为 " + str(t3[0]) + "]"
            else:
                if varStatus == "after":
                    x = cur.execute('select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time>"%s"' % (varDatabase, varAfterTime))
                    t4 = cur.fetchall()
                    print "[共有 " + str(x) + " 张表在 "+ str(varAfterTime)+ " 之后被创建]"
                    for p in range(len(t4)):
                        print str(t4[p][1]) + " => " + t4[p][0]
                elif varStatus == "before":
                    x = cur.execute('select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time<"%s"' % (varDatabase, varAfterTime))
                    t4 = cur.fetchall()
                    print "[共有 " + str(x) + " 张表在 " + str(varAfterTime) + " 之前被创建]"
                    for p in range(len(t4)):
                        print str(t4[p][1]) + " => " + (t4[p][0])
                else: print "[errorrrrrrr , 参数3错误!]"
        except:
            print "[errorrrrrrr , 数据库(" + varDatabase + ")不存在!]"
    else:
        print "[warning , 数据库为空!]"

# # 获取 某表的创建时间
# getTblCreateTime("dangjian", "tt_task", "", "")
#
# # 获取 指定日期之后创建的表
# getTblCreateTime("personal", "", "after", "2016-11-24")
#
# # 获取 指定日期之前创建的表
# getTblCreateTime("personal", "", "before", "2016-12-08")


def getTblNameDDL(varDatabase, varTable):
    # 获取数据库表的字段、DDL （非列表排列）
    list0 = []; list2 = [] ; tblFieldcount = 0 ; sum1 = ""
    n = cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDatabase, varTable))
    if n != 0:
        t1 = cur.fetchone()  # t1[0] = 字段comment
        cur.execute('select column_name,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDatabase, varTable))
        t2 = cur.fetchall()
        print "\n[" + varDatabase + " > " + varTable + "(" + t1[0] + ") > " + str(len(t2)) + "fields]"
        print "-" * 150
        for i in t2:
            tblFieldcount = tblFieldcount + 1
            list0.append(i[0])
            ii = i[1].replace("\r\n", ",")
            list2.append(ii.replace("  ", ""))
        for i in range(tblFieldcount):
            sum1 = sum1 + " , " + list0[i] + "(" + list2[i] + ")"
        print sum1[2:]
    else:
        print "[errorrrrrrr,数据库("+varDatabase+")中没有找到 "+ varTable +"表!]"

# getTblNameDDL("dangjian", "tt_task")
# getTblNameDDL("upload", "uploadfile")
# getTblNameDDL("scenemsg", "t_scene_msg")


# getValueFromTBL('dangjian', 'tt_task','varchar', 'ceshi')


def getValueFromTBL(varDatabase, varTable, varType, varValue):
    # 功能：模糊搜索关键字，显示所在表及详细记录，遍历所有的表
    # 参数分别是 = 数据库，表*，数据类型，值

    list0 = []; list1 = []; x = y = tblFieldcount = 0
    if varType != "":
        if "*" in varTable:
            varTable2 = varTable.split("*")[0] + "%"  # t_store_%
            m = cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (varDatabase, varTable2))
            if m != 0:
                t0 = cur.fetchall()
                # print len(t0)   #  共有len(t0)张表
                for p in range(len(t0)):
                    varTable = t0[p][0]
                    # 遍历指定的表
                    n = cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s"' % (varDatabase, varTable))
                    if n != 0:
                        t1 = cur.fetchone()
                        tblDDL = t1[0]
                        cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s"' % (varDatabase,varTable))
                        t2 = cur.fetchall()
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
                            cur.execute('select * from %s where `%s` like "%s"' % (varTable,list0[i],varValue))
                            t4 = cur.fetchall()
                            if len(t4) <>0 :
                                print ">" * 70
                                print u"[RESULT: '" +varValue + u"' , found " + str(len(t4))  + " , " + varDatabase + "."+ varTable+"."+list0[i] + u"]\n"
                                for j in range(len(t4)):

                                    # print json.dumps(list(t4[j]), encoding="UTF-8", ensure_ascii=False)
                                    print list(t4[j])
                                print "\n"
                    list0 = []; list1 = [];tblFieldcount = 0
            else: print "[errorrrrrrr , 数据库(" + varDatabase + ")中没有找到 " + varTable.split("*")[0] + " 前缀的表!]"
        elif "*" not in varTable:
            print "erererer"
            # # 遍历指定的表
            # n = cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
            # if n != 0:
            #     t1 = cur.fetchone()
            #     tblDDL = t1[0]
            #     cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
            #     t2 = cur.fetchall()
            #     if varFields == "":
            #         print "\n[" + varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(len(t2)) + "]"
            #         print "-" * 70
            #         for i in t2:
            #             if len(i[0]) > x: x = len(i[0])
            #             if len(i[1]) > y: y = len(i[1])
            #             tblFieldcount = tblFieldcount + 1
            #         for i in t2:
            #             list0.append(i[0] + " "*(x-len(i[0])+1))
            #             list1.append(i[1] + " "*(y-len(i[1])+1))
            #             ii=i[2].replace("\r\n", ",")
            #             list2.append(ii.replace("  ", ""))
            #         for i in range(tblFieldcount):
            #             print list0[i], list1[i], list2[i]
            #     else:
            #         print "\n[" + varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(len(varFields.split(","))) + "]"
            #         print "-" * 70
            #         for i in t2:
            #             if len(i[0]) > x: x = len(i[0])
            #             if len(i[1]) > y: y = len(i[1])
            #         for i in t2:
            #             for j in range(len(varFields.split(","))):
            #                 if i[0] == varFields.split(",")[j]:
            #                     list0.append(i[0] + " "*(x-len(i[0])+1))
            #                     list1.append(i[1] + " "*(y-len(i[1])+1))
            #                     ii=i[2].replace("\r\n", ",")
            #                     list2.append(ii.replace("  ", ""))
            #         for i in range(len(varFields.split(","))):
            #             try:
            #                 print list0[i], list1[i], list2[i]
            #             except:
            #                 print "[??? Errorrrrrrr , 参数3中部分字段不存在!]"
            # else:
            #     print "[errorrrrrrr , 数据库(" + varDatabase + ")中没有找到 " + varTable + "表!]"
    # else:
    #     cur.execute('select TABLE_NAME,TABLE_COMMENT from information_schema.`TABLES` where table_schema="%s" ' % varDatabase)
    #     tblname=cur.fetchall()
    #     for k in range(len(tblname)):
    #         cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDatabase,tblname[k][0]))
    #         t2 = cur.fetchall()
    #         print "\n[" + varDatabase + " > " + tblname[k][0] + "(" + tblname[k][1] + ") > " + str(len(t2)) + "fields]"
    #         print "-" * 70
    #         for i in t2:
    #             if len(i[0]) > x: x = len(i[0])
    #             if len(i[1]) > y: y = len(i[1])
    #             tblFieldcount = tblFieldcount + 1
    #         for i in t2:
    #             list0.append(i[0] + " "*(x-len(i[0])+1))
    #             list1.append(i[1] + " "*(y-len(i[1])+1))
    #             list2.append(i[2])
    #         for i in range(tblFieldcount):
    #             print list0[i], list1[i], list2[i]
    #         list0 = []; list1 = []; list2 = []
    #         tblFieldcount = 0

# getValueFromTBL('dangjian', 'tt_task','varchar', u'任务简介')
getValueFromTBL('dangjian', '*','char', u'%我的子项目%')
# getValueFromTBL('yygdm', '*', 'char', u'%甲')


