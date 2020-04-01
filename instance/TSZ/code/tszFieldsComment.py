# -*- coding: utf-8 -*-
#****************************************************************
# Author     : John   # coding: utf-8
# Date       : 2016-8-25
# Description: 遍历数据库中所有的表,输出字段\类型\注释
#****************************************************************

import os,sys,xlwt,xlrd,MySQLdb,string,datetime
import xlwt,xlrd,chardet,random,webbrowser
from time import sleep
from xlwt.Style import *
from xlrd import open_workbook
from xlutils.copy import copy
from datetime import datetime
from datetime import timedelta

# 数据库
connWeb= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curWeb = connWeb.cursor()
curWeb.execute('SET NAMES utf8;')
connWeb.set_character_set('utf8')
curWeb.execute('show tables')
ukardwebTable=curWeb.fetchall()

def assertEqual(expected,actual,okmessage,errmessage):
    # 功能:用于检查表数据
    # 参数1=预期值 ,参数2=实测值 ,参数3= 输出正确提示,参数4=输出错误提示
    if expected == actual : print okmessage
    else: print errmessage
def tblChiStructure(self,tblName,tblAllFields,keyword,varTblName,tblChiName,*tblChiField):
    # 功能: 输出表名(中文),所有字段(中文)
    # print list打印出数据存储的编码方式，中文是中文编码；
    # print list[1]打印出的是译转中文编码的中文。
    varList=[]
    varTmp=""
    if tblName == varTblName:
        reload(sys)
        sys.setdefaultencoding('utf-8')
        tblChiList = list(tblChiField)  # ['ID','代理商名称','创建时间','修改时间','有效性 1=有效 0=无效','审核标记 0=编辑 1=审核中 2=审核通过 3=审核退回','手机号','与公司分成比例']
        for i in range(len(tblChiList)):
            varList.append(str(tblAllFields[i]) +"("+ str(tblChiList[i])+")")
            varTmp =  varTmp + " , " + str(varList[i])
        print str(tblName) + "(" + str(tblChiName) + ") => \n"
        print str(varTmp[2:])
        # print x
        # print x.decode("gb2312").encode("utf-8")
        page << p("<font color=blue>"+ str(tblName) + ' </font> => ' + str(varTmp[2:]) + " {关键字: <font color=red>" + str(keyword) + "</font> }")
        del varList[:]
        varTmp=""


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def showTblNameAndDDL(varDatabase,varTable):
    # 功能:获取数据库表字段+DDL    # showDDL(数据库名,表名)
    list0=[]
    list2=[]
    tblFieldcount=0
    sum1=""

    # 遍历指定的表
    n = curWeb.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
    if n <> 0 :
        t1 = curWeb.fetchone()  # t1[0] = 字段comment
        curWeb.execute('select column_name,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
        t2 = curWeb.fetchall()
        print "\n[" + varDatabase + " > " + varTable + "(" + t1[0] + ") > " + str(len(t2)) + "fields]"
        print "-" * 150
        for i in t2:
            tblFieldcount=tblFieldcount+1
            list0.append(i[0])
            ii=i[1].replace("\r\n",",")
            list2.append(ii.replace("  ",""))
        for i in range(tblFieldcount):
            sum1= sum1 + " , " + list0[i] + "(" + list2[i] +")"
        print sum1[2:]
    else:
        print "errorrrrrrr,数据库("+varDatabase+")中没有找到 "+ varTable +"表!"
# 显示数据库,表,所有字段,DDL
# showTblNameAndDDL("ukardweb","t_user")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def showDDL(varDatabase,varTable,varFields):
    # 功能:获取数据库表字段DDL
    # showDDL(参数1,参数2,参数3)
    # 参数1 = 数据库 , 参数2 = 表(为空表示所有表;可遍历带指定前缀名的表) , 参数3 = 字段(多个字段用逗号分割;为空表示所有字段)

    conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db=varDatabase, port=3306, use_unicode=True)
    conn.set_character_set('utf8')
    cur = conn.cursor()
    cur.execute('SET NAMES utf8;')
    list0=[]
    list1=[]
    list2=[]
    x=y=tblFieldcount=0
    if varTable <> "":
        if "*" in varTable:
            varTable2=varTable.split("*")[0] + "%"  # t_store_%
            m = cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (varDatabase,varTable2))
            if m <> 0 :
                t0=cur.fetchall()
                for p in range(len(t0)):  #  共有len(t0)张表
                    varTable = t0[p][0]
                    # 遍历指定的表
                    n = cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
                    if n <> 0 :
                        t1=cur.fetchone()
                        tblDDL = t1[0]
                        cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
                        t2=cur.fetchall()
                        print "\n[" + varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(len(t2)) + "]"
                        print "-" * 70
                        for i in t2:
                            if len(i[0])>x: x=len(i[0])
                            if len(i[1])>y: y=len(i[1])
                            tblFieldcount=tblFieldcount+1
                        for i in t2:
                            list0.append(i[0] + " "*(x-len(i[0])+1))
                            list1.append(i[1]+ " "*(y-len(i[1])+1))
                            ii=i[2].replace("\r\n",",")
                            list2.append(ii.replace("  ",""))
                        for i in range(tblFieldcount):
                            print list0[i],list1[i],list2[i]
                    list0=[]
                    list1=[]
                    list2=[]
                    tblFieldcount=0
            else: print "errorrrrrrr,数据库("+varDatabase+")中没有找到 " + varTable.split("*")[0] + " 前缀的表!"

        elif "*" not in varTable:

            # 遍历指定的表
            n = cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
            if n <> 0 :
                t1=cur.fetchone()
                tblDDL = t1[0]
                cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
                t2=cur.fetchall()

                if varFields=="":
                    print "\n[" + varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(len(t2)) + "]"
                    print "-" * 70
                    for i in t2:
                        if len(i[0])>x: x=len(i[0])
                        if len(i[1])>y: y=len(i[1])
                        tblFieldcount=tblFieldcount+1

                    for i in t2:
                        list0.append(i[0] + " "*(x-len(i[0])+1))
                        list1.append(i[1]+ " "*(y-len(i[1])+1))
                        ii=i[2].replace("\r\n",",")
                        list2.append(ii.replace("  ",""))
                    for i in range(tblFieldcount):
                        print list0[i],list1[i],list2[i]
                else:
                    print "\n[" + varDatabase + " > " + varTable + "(" + tblDDL + ") > " + str(len(varFields.split(","))) + "]"
                    print "-" * 70
                    for i in t2:
                        if len(i[0])>x: x=len(i[0])
                        if len(i[1])>y: y=len(i[1])
                    for i in t2:
                        for j in range(len(varFields.split(","))):
                            if i[0] == varFields.split(",")[j]:
                                list0.append(i[0] + " "*(x-len(i[0])+1))
                                list1.append(i[1]+ " "*(y-len(i[1])+1))
                                ii=i[2].replace("\r\n",",")
                                list2.append(ii.replace("  ",""))
                    for i in range(len(varFields.split(","))):
                        try:
                            print list0[i],list1[i],list2[i]
                        except:
                            print "??? Errorrrrrrr, 参数3中部分字段不存在!"

            else:

                print "errorrrrrrr,数据库("+varDatabase+")中没有找到 "+ varTable +"表!"

    else:
        cur.execute('select TABLE_NAME,TABLE_COMMENT from information_schema.`TABLES` where table_schema="%s" ' % varDatabase)
        tblname=cur.fetchall()
        # 遍历某数据库中所有的表
        for k in range(len(tblname)):
            # print tblname[k][0]
            cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDatabase,tblname[k][0]))
            t2=cur.fetchall()
            print "\n[" + varDatabase + " > " + tblname[k][0] + "(" + tblname[k][1] + ") > " + str(len(t2)) + "]"
            print "-" * 70
            for i in t2:
                if len(i[0])>x: x=len(i[0])
                if len(i[1])>y: y=len(i[1])
                tblFieldcount=tblFieldcount+1
            for i in t2:
                list0.append(i[0] + " "*(x-len(i[0])+1))
                list1.append(i[1]+ " "*(y-len(i[1])+1))
                # ii=i[2].replace("\r\n",",")
                # list2.append(ii.replace("  ",""))
                list2.append(i[2])
            for i in range(tblFieldcount):
                print list0[i],list1[i],list2[i]
            list0=[]
            list1=[]
            list2=[]
            tblFieldcount=0

# 显示表t_user中3个字段(id,ref2,remard)的DDL
# showDDL('ukardweb','t_redgroup_baseinfo','')

# 显示表t_redgroup_baseinfo中所有字段的DDL
# showDDL('ukardweb','t_redgroup_baseinfo','')

# 显示表t_game_user中多个字段用逗号分割,如下用例第三个参数逗号后字段为空,则提示报错
# showDDL('game','t_game_user','userId,')

# 显示game数据库中所有表的字段及DDL
# showDDL('game','','')

# 显示"t_store_"前缀表的所有字段DDL
# showDDL('ukardweb','t_store_*','remark')

# showDDL('game','t_game_explain','sort')
# showDDL('game','t_game_explain','sort,id')
# showDDL('game','t_game_explain','sort,id,123')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def showTblTime(varDatabase,varTable,varStatus,varAfterTime):
    # 功能:显示表的创建时间
    # varStatus =1 表示 varAfterTime 之后创建 ; =0 表示 varAfterTime 之前创建
    conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db=varDatabase, port=3306, use_unicode=True)
    conn.set_character_set('utf8')
    cur = conn.cursor()
    cur.execute('SET NAMES utf8;')
    # n1 = cur.execute('select distinct table_schema from information_schema.`TABLES`')
    print "-" * 70
    if varDatabase<>"":
        try:
            if varTable <>"":
                cur.execute('select create_time from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
                t3=cur.fetchone()
                print "[表("+varDatabase+"."+varTable +")的创建时间为 " + str(t3[0]) + "]"
            else:
                if varStatus == "0":
                    x=cur.execute('select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time>"%s"' % (varDatabase,varAfterTime))
                    t4=cur.fetchall()
                    print "[共有 " + str(x) + " 张表在 "+ str(varAfterTime)+ " 之后被创建]"
                    for p in range(len(t4)):
                        print str(t4[p][1]) + " => " + t4[p][0]
                elif varStatus == "1":
                    x=cur.execute('select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time<"%s"' % (varDatabase,varAfterTime))
                    t4=cur.fetchall()
                    print "[共有 " + str(x) + " 张表在 " + str(varAfterTime)+ " 之前被创建]"
                    for p in range(len(t4)):
                        print t4[p][0] +" => " + str(t4[p][1])
                else: print "errorrrrrrr,参数3错误!"

            print ">" *70
        except:
            print "errorrrrrrr,数据库(" + varDatabase + ")不存在!"
    else:
        print "warning,数据库为空!"
# 表(ukardweb.t_user)的创建时间为 2016-09-02 15:49:00
# showTblTime("ukardweb","t_user","","")

# # 参数3 = 0 时,显示指定日期之后创建的表
# showTblTime("ukardweb","","0","2016-08-17")

# # 参数3 = 1 时,显示指定日期之前创建的表
# showTblTime("ukardweb","","1","2016-02-17")

# 参数3 非0,1 时,报错
# showTblTime("ukardweb","","19","2015-08-17")

