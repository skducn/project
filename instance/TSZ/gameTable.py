# coding: utf-8

#****************************************************************
# Author     : John
# Version    : 1.0.0
# Date       : 2016-6-13
# Description: gameTable.py
# Function   : 遍历数据库中所有的表,查询并输出 某时间段 内所有的记录 ,此脚本可查询 ukardweb \game \ ukardapp 数据库所有的表
#****************************************************************

import os,sys,unittest,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,re
import xlwt,xlrd,chardet,random,webbrowser
from time import sleep
from xlwt.Style import *
from xlrd import open_workbook
from xlutils.copy import copy
from PIL import Image
import time,requests,pyh
# import HTMLTestRunner
# 发邮件所需组件 smtplib 和 MIMEText
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header

# bblist=['phone', '13816109050', 1L, 'userId', 10001679L, 1L]
# print bblist
# if 'userId' in bblist:
#     print "ok"
#
#
# str2='\u91d1\u91d1 \u7ed9\u60a8\u53d1\u73b0\u91d1\u7ea2\u5305\u5566\uff010.20\u5143\u7ea2\u5305\u7b49\u5927\u5bb6\u6765\u62a2\uff0c\u62a2\u5230\u5c31\u80fd\u63d0\u73b0\u54e6~'
# str1 = '\u4f60\u597d'
# print str2.decode('unicode_escape')

# print len((3232L, 10001871L, 2257L, u'1', 0L, 0L, 0L, 20L, 3L, u'3101000000', 21, datetime.datetime(2016, 7, 5, 13, 47, 27), datetime.datetime(2016, 7, 5, 13, 47, 27), 1))
# x=123
# y='abc'
# c=44L
# dlist=[]
# dlist.append(x)
# dlist.append(y)
# dlist.append(c)
# print dlist
#
# sleep(1212121)


# ========== Param ==========
VARMYPHONE="13816109050"


# PyH文档 http://www.tuicool.com/articles/IRvEBr
from pyh import *
page =PyH('gameTable')
page.addCSS('myStylesheet1.css','myStylesheet2.css')
page << h2(u'gameTable', cl='center')
page << h4(u'GenerateTime : ',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'  , ' + VARMYPHONE + ' \'s result as below :')
# xy=u"用例执行情况："
# page << h4(xy.encode("utf-8"))
# decode的作用是将其他编码的字符串转换成unicode编码，如str1.decode('gb2312')，表示将gb2312编码的字符串str1转换成unicode编码。
# encode的作用是将unicode编码转换成其他编码的字符串，如str2.encode('gb2312')，表示将unicode编码的字符串str2转换成gb2312编码。


alist=[]
# 时间区域: 只操作当天日期的数据
ISOTIMEFORMAT="%Y-%m-%d"
myTime=time.strftime( ISOTIMEFORMAT, time.localtime() )
myfrtTime=myTime+" 00:00:01"
myEndTime=myTime+" 23:59:59"
varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #当天日期时间

VARPERIODTIME = "period of validity is from " + myfrtTime+" to " + myEndTime +""
VAREXCELFILE = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/excel/tszTable.xls"
VARHTMLFILE = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/report/gameTable.html" # TestReport文件
VARHTMLFILEtimestamp = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/report/gameTable"+varTimeYMDHSM+".html" # TestReport文件
VARERRSCREENSHOT = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/screenshot/"  # 错误截屏
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
cur = conn.cursor()
conn.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
cur.execute('show tables') # 获取数据库所有表名
ukardwebTable=cur.fetchall()
# 获取用户ID
cur.execute('select id from t_user where username="%s" order by id desc' % (VARMYPHONE))
data0 = cur.fetchone()
myuserID = data0[0]
# 获取群ID
cur.execute('select id from t_redgroup_baseinfo where userId="%s" order by id desc ' % (myuserID))
data0 = cur.fetchone()
mygroupID = data0[0]


connGame= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='game', port=3306, use_unicode=True) #sit2
curGame = connGame.cursor()
connGame.set_character_set('utf8')
curGame.execute('SET NAMES utf8;')
curGame.execute('SET CHARACTER SET utf8;')
curGame.execute('SET character_set_connection=utf8;')
curGame.execute('show tables')
gameTable=curGame.fetchall()

connapp= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardapp', port=3306, use_unicode=True)
curapp = connapp.cursor()
connapp.set_character_set('utf8')
curapp.execute('SET NAMES utf8;')
curapp.execute('SET CHARACTER SET utf8;')
curapp.execute('SET character_set_connection=utf8;')
curapp.execute('show tables') # 获取数据库所有表名
ukardappTable=curapp.fetchall()


class TSZgameTable(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.fname=VAREXCELFILE
        bk = xlrd.open_workbook(VAREXCELFILE,formatting_info=True)
        self.bk=bk
        newbk=copy(bk)
        self.newbk=newbk
        styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
        styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')
        styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
        self.styleBlue=styleBlue
        self.styleGray25=styleGray25
        self.styleRed=styleRed
    @classmethod
    def tearDownClass(self):
        cur.close()
        conn.close()
        curGame.close()
        connGame.close()
        curapp.close()
        connapp.close()

    def sendemail(self,varFile):
        # 邮箱配置
        sender = '<jinhao@mo-win.com.cn>'
        receiver = 'jinhao@mo-win.com.cn'
        f = open(varFile,'rb')
        mail_body = f.read()
        f.close()
        msg=MIMEText(mail_body,_subtype='html',_charset='utf-8')
        # msg = MIMEText('<html><h1>你好！</h1></html>','html','utf-8')
        # msg = MIMEText('你好','text','utf-8')
        # msg['Subject'] = Header(subject,'utf-8')
        msg['Subject'] = u'三藏红包gameTAble'
        try:
            smtp = smtplib.SMTP()
            smtp.connect('smtp.exmail.qq.com')
            smtp.login('jinhao@mo-win.com.cn','Jinhao80')
            smtp.sendmail(sender,receiver,msg.as_string())
            smtp.quit()
        except Exception, e:
            print str(e)

    def test_Main(self):
        sheetMain= self.bk.sheet_by_name("Main")
        sheetTestCase = self.bk.sheet_by_name("TestCase")
        self.sheetMain=sheetMain
        self.sheetTestCase=sheetTestCase
        #遍历Main执行函数模块
        for i in range(1,sheetMain.nrows):
            if sheetMain.cell_value(i,0) == "Y":
                Maincol1=sheetMain.cell_value(i,1)
                Maincol2=sheetMain.cell_value(i,2)
                self.Maincol1=Maincol1
                self.Maincol2=Maincol2
                exec(sheetMain.cell_value(i,4))


    def TestcaseModule(self):
         #遍历TestCase及调用函数模块
         case1=caseN=0
         for j in range(1,self.sheetTestCase.nrows):
              case1=case1+1
              # 定位测试用例位置及数量
              if self.sheetTestCase.cell_value(j,1) == self.Maincol1 and self.sheetTestCase.cell_value(j,2) == self.Maincol2:
                  for k in range(case1+1,100): # 假设有100个Case
                      if k + 1 > self.sheetTestCase.nrows:  # 最后一行
                           caseN=caseN+1
                           break
                      elif self.sheetTestCase.cell_value(k,1)=="" and self.sheetTestCase.cell_value(k,2)=="":
                           caseN=caseN+1
                      elif self.sheetTestCase.cell_value(k,2)=="skip" :
                           caseN=caseN+1
                      else:
                           caseN=caseN+1
                           break
                  break
         #遍历 Testcase1~TestCaseN
         for l in range(case1,caseN+case1):
               # 定位参数从第6列开始，遍历10列
               str_list=[]
               for m in range(6,15):  #id0 - id9
                     if self.sheetTestCase.cell(l,m).value <> "" :
                          N = self.sheetTestCase.cell_value(l,m)
                          str_list.append(str(N))
                     else:
                         break
               self.str_list=str_list
               try :
                   if self.sheetTestCase.cell_value(l,1)=="skip" or self.sheetTestCase.cell_value(l,2)=="skip":
                       newWs=self.newbk.get_sheet(1)
                       newWs.write(l,0,"skip",self.styleGray25)
                       self.newbk.save(self.fname)
                   else:
                       exec(self.sheetTestCase.cell_value(l,4))
                       newWs=self.newbk.get_sheet(1)
                       newWs.write(l,0,"OK",self.styleBlue)
                       self.newbk.save(self.fname)
                       # page << p("<font color=blue>[Pass]</font> ",self.sheetTestCase.cell_value(l,3))  #输出测试用例
               except:
                   print u"Excel,Err,第"+str(l+1)+u"行,"+self.sheetTestCase.cell_value(l,3)
                   newWs=self.newbk.get_sheet(1)
                   newWs.write(l,0,"error",self.styleRed)
                   self.newbk.save(self.fname)
                   page << p("<font color=red>[Error]</font> ",self.sheetTestCase.cell_value(l,3))  #输出测试用例
               
         # 是否生成VARHTMLFILE文档, 1=生成一个testreport.html; 2=生成多个带时间的html,如testreport20161205121210.html
         if self.sheetMain.cell_value(1,6) == 1:
           page.printOut(VARHTMLFILE)
           sleep(4)
           # #send Email
           if self.sheetMain.cell_value(1,5)=="Y":
              self.sendemail(VARHTMLFILE)
         elif self.sheetMain.cell_value(1,6) == 2:
           page.printOut(VARHTMLFILEtimestamp)
           # #send Email
           if self.sheetMain.cell_value(1,5)=="Y":
              self.sendemail(VARHTMLFILEtimestamp)


    def output(self,col_name_list,varName,varCur,ATtable,varX):
        if varName in col_name_list:
            varCur.execute('select count(%s) from %s where %s="%s"' % (varName,ATtable,varName,varX))
            t2=varCur.fetchone()
            if t2[0]>0:
                alist.append(varName)
                alist.append(varX)
                alist.append(t2[0])


    def t_userLogin(self,TabelName,varCur,varTable):
        print "[" + str(TabelName) + "," + str(VARPERIODTIME) +"] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
        page << p("<font color=green>[" + str(TabelName) + "] , " + str(VARPERIODTIME) +" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>></font> ")

        # print "[" + str(TabelName) + "," + str(len(varTable)) + u"张表]"
        varFieldtime=""  # 存放各表的时间
        varTableCount=0 # 统计输出多少张符合要求的表
        for AT in varTable:
            # 遍历所有的表
            # 获取每个表中所有字段 ,存入col_name_list
            if AT[0] == "beijing_store" : # or AT[0] == "t_redgroup_user_label" :
                pass
            else:
                varCur.execute("select * from %s" % AT[0])
                col_name_list = [tuple[0] for tuple in varCur.description]
                # 判断表中id字段, 如果不存在则跳过此表, 否则遍历此表统计数量,忽略空表.
                if 'id' in col_name_list:
                    varCur.execute('select count(id) from %s' % (AT[0]))
                    t1 = varCur.fetchone()
                    if t1[0] > 0:
                        # 遍历表中的字段是否包含 phone,username,user_id,userid,userId,userId1,userId2 及 各类时间字段,如createTime,updateTime etc.
                        self.output(col_name_list,'userId',varCur,AT[0],myuserID)
                        self.output(col_name_list,'user_id',varCur,AT[0],myuserID)
                        self.output(col_name_list,'userid',varCur,AT[0],myuserID)
                        self.output(col_name_list,'id',varCur,AT[0],myuserID)
                        self.output(col_name_list,'id1',varCur,AT[0],myuserID)
                        self.output(col_name_list,'id2',varCur,AT[0],myuserID)
                        self.output(col_name_list,'belongId',varCur,AT[0],myuserID)
                        self.output(col_name_list,'accept_id',varCur,AT[0],myuserID)
                        self.output(col_name_list,'friendid',varCur,AT[0],myuserID)
                        self.output(col_name_list,'th_id',varCur,AT[0],myuserID)
                        self.output(col_name_list,'sd_id',varCur,AT[0],myuserID)
                        self.output(col_name_list,'groupUserId',varCur,AT[0],myuserID)
                        self.output(col_name_list,'submit_user_id',varCur,AT[0],myuserID)
                        self.output(col_name_list,'shareUserId',varCur,AT[0],myuserID)
                        self.output(col_name_list,'userId1',varCur,AT[0],myuserID)
                        self.output(col_name_list,'userId2',varCur,AT[0],myuserID)

                        self.output(col_name_list,'phone',varCur,AT[0],VARMYPHONE)
                        self.output(col_name_list,'username',varCur,AT[0],VARMYPHONE)
                        self.output(col_name_list,'contacts',varCur,AT[0],VARMYPHONE)

                        self.output(col_name_list,'groupId',varCur,AT[0],mygroupID)

                        if alist:  #不为空时
                            # 遍历列表定位字段 如: 获取所有 带time的字段 ,忽略大小写
                            for m in range(len(col_name_list)):
                                m1=re.search("Time",col_name_list[m],re.IGNORECASE)
                                if m1:
                                    if col_name_list[m]  in col_name_list:  # 遍历字段中带Time字符的字段
                                         # print col_name_list[m]
                                         # if 'userId' in alist:
                                         #     # 输出有效期内的 {myuserID}条记录
                                         #     varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and userId=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                         #     numrows = int(varCur.rowcount)
                                         #     for i in range(numrows):
                                         #         row = varCur.fetchone()
                                         #         varFieldtime="("+str(row[0])+") "+varFieldtime
                                         #         # print t2[i]
                                         #     if varFieldtime<>"":
                                         #         alist.append(col_name_list[m])
                                         #         alist.append(numrows)
                                         #         alist.append(varFieldtime)
                                         #     if numrows>=1:  # 输出符合条件的字段及记录
                                         #         print AT[0] + " => " + str(alist)
                                         #         print "     >>>>>>" + str(col_name_list)
                                         #         page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                         #         page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                         #         varTableCount=varTableCount+1
                                         #         varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and userId=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                         #         t2=varCur.fetchall()
                                         #         for j in range(numrows):
                                         #             print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                         #             # 失败,格式化元组中的数据,如 (619L, 2257L, 10001871L, u'', None, 1, datetime.datetime(2016, 7, 5, 13, 47, 58))
                                         #             # c_list=[]
                                         #             # xx=t2[j]
                                         #             # for k in range(len(xx)):
                                         #             #     print xx[k]
                                         #             #     # print type(xx[k])
                                         #             #     if isinstance(xx[k], long):
                                         #             #         print "ok"
                                         #             #         c_list.append(xx)
                                         #             #     elif isinstance(xx[k], int):
                                         #             #         print "err"
                                         #             #     elif isinstance(xx[k], unicode):
                                         #             #         print "hahah"
                                         #             #     elif isinstance(xx[k], datetime.datetime):
                                         #             #         print "xixix"
                                         #             #     c_list.append(xx[k])
                                         #             # print c_list
                                         #             page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                         #         print "\n"
                                         #     del alist[:]
                                         #     varFieldtime=""
                                         # print col_name_list[m]
                                         # print alist
                                         if 'userId' in alist:
                                             # print AT[0]
                                             # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and userId=%s ' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and userId=%s ' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'user_id' in alist:
                                             # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and user_id=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and user_id=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'userid' in alist:
                                            # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and userid=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and userid=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'id' in alist:
                                            # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and id=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and id=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'id1' in alist:
                                            # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and id1=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and id1=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'id2' in alist:
                                            # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and id2=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and id2=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'belongId' in alist:
                                            # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and belongId=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and belongId=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'accept_id' in alist:
                                             # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and accept_id=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and accept_id=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'friendid' in alist:
                                             # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and friendid=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and friendid=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'th_id' in alist:
                                             # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and th_id=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and th_id=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'sd_id' in alist:
                                             # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and sd_id=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and sd_id=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'groupUserId' in alist:
                                             # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and groupUserId=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and groupUserId=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'submit_user_id' in alist:
                                             # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and submit_user_id=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and submit_user_id=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'shareUserId' in alist:
                                             # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and shareUserId=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and shareUserId=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'userId1' in alist:
                                             # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and userId1=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and userId1=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'userId2' in alist:
                                             # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and userId2=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and userId2=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,myuserID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""


                                         elif 'phone' in alist:
                                            # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and phone=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,VARMYPHONE,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and phone=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,VARMYPHONE,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'username' in alist:
                                            # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and username=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,VARMYPHONE,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and username=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,VARMYPHONE,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'contacts' in alist:
                                            # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and contacts=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,VARMYPHONE,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and contacts=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,VARMYPHONE,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

                                         elif 'groupId' in alist:
                                             # 输出有效期内的 {myuserID}条记录
                                             varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and groupId=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],myfrtTime,myEndTime,mygroupID,col_name_list[m]))
                                             numrows = int(varCur.rowcount)
                                             for i in range(numrows):
                                                 row = varCur.fetchone()
                                                 varFieldtime="("+str(row[0])+") "+varFieldtime
                                             if varFieldtime<>"":
                                                 alist.append(col_name_list[m])
                                                 alist.append(numrows)
                                                 alist.append(varFieldtime)
                                             if numrows>=1:
                                                 print AT[0] + " => " + str(alist)
                                                 print "     >>>>>>" + str(col_name_list)
                                                 page << p("<font color=blue>"+ str(AT[0]) + " => " + str(alist)) + " </font> "
                                                 page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                                                 varTableCount=varTableCount+1
                                                 varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and groupId=%s order by "%s" desc' % (AT[0],col_name_list[m],myfrtTime,myEndTime,mygroupID,col_name_list[m]))
                                                 t2=varCur.fetchall()
                                                 for j in range(numrows):
                                                     print "     >>>>>>" + str(j+1) +", "+ str(t2[j]).decode('unicode_escape')
                                                     page << p("&nbsp;&nbsp;&nbsp;&nbsp;" + str(j+1) + " , " + str(t2[j]))
                                                 print "\n"
                                             del alist[:]
                                             varFieldtime=""

        print u"[affected " + str(varTableCount) + " tables]\n"
        page << p("<font color=red> [affected " + str(varTableCount) + " tables]</font> ")


    def drv_ukardweb(self):
        self.TestcaseModule()
    def t_ukardweb(self):
        print "1111"
        # self.t_userLogin(self.cur,self.ukardwebTable)
    def t_sendRed(self):
        print "2222"
    def t_responseTables(self):
        print "3333"
        self.t_userLogin("ukardweb",cur,ukardwebTable)
        # self.t_userLogin("ukardapp",curapp,ukardappTable)
        # self.t_userLogin("game",curGame,gameTable)
        print "121212"





    def drv_game(self):
        # game
        self.TestcaseModule()
    def t_game(self):
        self.t_userLogin(self.curGame,self.gameTable)


if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TSZgameTable) # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1) # 执行测试