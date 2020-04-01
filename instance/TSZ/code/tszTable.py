# coding: utf-8
#****************************************************************
# Author     : John # -*- coding: utf-8 -*-
# Version    : 1.0.0
# Date       : 2016-6-13
# Description: tszTable.py
# Function   : 依据当前手机号遍历数据库中所有的表,查询并输出此手机号某时间段内所有更改过的的记录 ,数据库包括 ukardweb,game,ukardapp所有的表
#****************************************************************

import os,sys,unittest,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,re,smtplib,time,requests,pyh,webbrowser
import xlwt,xlrd,chardet,random,webbrowser
from time import sleep
from xlwt.Style import *
from xlrd import open_workbook
from xlutils.copy import copy
from PIL import Image
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
# import HTMLTestRunner
# PyH文档 http://www.tuicool.com/articles/IRvEBr
from pyh import *


# VARHTMLFILEtimestamp = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/report/tszTable20160920151652.html" # TestReport文件
#
# webbrowser.open_new_tab("file://" + VARHTMLFILEtimestamp)
#
# # webbrowser.open_new_tab("file:///Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/report/tszTable20160920151652.html")
# sleep(1212)

# 去重复
# ids = [1,4,3,3,4,2,3,4,5,6,1]
# ids = list(set(ids))
# print ids
# sleep(1212)
# str2='\u91d1\u91d1 \u7ed9\u60a8\u53d1\u73b0\u91d1\u7ea2\u5305\u5566\uff010.20\u5143\u7ea2\u5305\u7b49\u5927\u5bb6\u6765\u62a2\uff0c\u62a2\u5230\u5c31\u80fd\u63d0\u73b0\u54e6~'
# str1 = '\u4f60\u597d'
# print str2.decode('unicode_escape')

# print len((3232L, 10001871L, 2257L, u'1', 0L, 0L, 0L, 20L, 3L, u'3101000000', 21, datetime.datetime(2016, 7, 5, 13, 47, 27), datetime.datetime(2016, 7, 5, 13, 47, 27), 1))

# reload(sys)
# sys.setdefaultencoding('utf-8')
# xx=[1,2,u'中文']
# xum=""
# for i in xx:
#     print i
#     xum=xum + "," + str(i)
#     print xum
# arrow100=">"
# print arrow100 * 130
# sleep(12121)

# 手机号
# varPhone = "18918814232"
varPhone = "13816100001"

# # 字符串转变量
# var = "This is a string"
# varName = 'var'
# s= locals()[varName]
# s2=vars()[varName]
# print s
# print s2
# print eval('var')
# sleep(1212)

page = PyH('tszTable')
page.addCSS('myStylesheet1.css','myStylesheet2.css')
page << h2(u'tszTable (',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +')', cl='center')
# page << h4(u'GenerateTime : ',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'  , ' + varPhone + ' \'s result as below :')
# xy=u"用例执行情况："
# page << h4(xy.encode("utf-8"))
# decode的作用是将其他编码的字符串转换成unicode编码，如str1.decode('gb2312')，表示将gb2312编码的字符串str1转换成unicode编码。
# encode的作用是将unicode编码转换成其他编码的字符串，如str2.encode('gb2312')，表示将unicode编码的字符串str2转换成gb2312编码。

alist=[]
l_tablescount=[]
list5=[]
l_keyword=[]
l_value=[]

# 时间参数
ISOTIMEFORMAT = "%Y-%m-%d"
myTime = time.strftime( ISOTIMEFORMAT, time.localtime())
# myTime="2016-07-25"  # 指定一个日期
myfrtTime = myTime + " 00:00:01"
myEndTime = myTime + " 23:59:59"
varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #当天日期时间
VARPERIODTIME =  myfrtTime + " ~ " + myEndTime

# 文档路径
VAREXCELFILE = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/excel/tszTable.xls"
VARHTMLFILE = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/report/tszTable.html" # TestReport文件
VARHTMLFILEtimestamp = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/report/tszTable"+varTimeYMDHSM+".html" # TestReport文件
VARERRSCREENSHOT = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/screenshot/"  # 错误截屏
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

# 数据库
connWeb= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curWeb = connWeb.cursor()
curWeb.execute('SET NAMES utf8;')
connWeb.set_character_set('utf8')
curWeb.execute('show tables')
ukardwebTable=curWeb.fetchall()
# 获取用户ID,三藏号
curWeb.execute('select id,tszNumber from t_user where username="%s" order by id desc' % (varPhone))
data0 = curWeb.fetchone()
myuserID = data0[0]
mytszNumber = data0[1]
# 获取群ID
curWeb.execute('select id from t_redgroup_baseinfo where userId="%s" order by id desc ' % (myuserID))
data0 = curWeb.fetchone()
mygroupID = data0[0]
# 是否个人认证
curWeb.execute('select isAuth,authType,cityName,city from t_redgroup_baseinfo where userId="%s" order by id desc ' % (myuserID))
data0 = curWeb.fetchone()
if data0[0]==1 and data0[1]==2 and data0[2]<>"" and data0[3]<>"" : varAuth = "已认证"
else:
    varAuth = "还未认证哦!"
    # 数据库修改为认证
    curWeb.execute('update t_redgroup_baseinfo set isAuth=1,authType=2 where userId="%s" order by id desc ' % (myuserID))
    connWeb.commit()
    varAuth = "操作数据库个人认证通过"

connApp= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardapp', port=3306, use_unicode=True)
curApp = connApp.cursor()
curApp.execute('SET NAMES utf8;')
curApp.execute('show tables')
ukardappTable=curApp.fetchall()

connGame= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='game', port=3306, use_unicode=True)
curGame = connGame.cursor()
curGame.execute('SET NAMES utf8;')
curGame.execute('show tables')
gameTable=curGame.fetchall()

class TszTable(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.fname = VAREXCELFILE
        self.bk = xlrd.open_workbook(VAREXCELFILE, formatting_info=True)
        self.newbk = copy(self.bk)
        self.styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
        self.styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')
        self.styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')


    @classmethod
    def tearDownClass(self):
        curWeb.close()
        connWeb.close()
        curGame.close()
        connGame.close()
        curApp.close()
        connApp.close()

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
        sheetKeyword = self.bk.sheet_by_name("Keyword1")
        for j in range(1, sheetKeyword.nrows):

            l_keyword.append(sheetKeyword.cell_value(j, 0).encode('raw_unicode_escape'))
            l_value.append(sheetKeyword.cell_value(j, 1).encode('raw_unicode_escape'))
        # 关键字,列表转字典

        self.d_keywords = dict(zip(l_keyword,l_value))
        self.sheetMain=sheetMain
        self.sheetTestCase=sheetTestCase
        self.sheetKeyword = sheetKeyword
        #遍历Main执行函数模块
        for i in range(1, sheetMain.nrows):
            if sheetMain.cell_value(i, 0) == "Y":
                Maincol1=sheetMain.cell_value(i, 1)
                Maincol2=sheetMain.cell_value(i, 2)
                self.Maincol1=Maincol1
                self.Maincol2=Maincol2
                exec(sheetMain.cell_value(i,4))



    def TestcaseModule(self):
         #遍历TestCase及调用函数模块
         case1 = caseN = 0
         for j in range(1, self.sheetTestCase.nrows):
              case1 = case1 + 1
              # 定位测试用例位置及数量
              if self.sheetTestCase.cell_value(j, 1) == self.Maincol1 and self.sheetTestCase.cell_value(j, 2) == self.Maincol2:
                  for k in range(case1+1, 100): # 假设有100个Case
                      if k + 1 > self.sheetTestCase.nrows:  # 最后一行
                           caseN=caseN+1
                           break
                      elif self.sheetTestCase.cell_value(k,1)=="" and self.sheetTestCase.cell_value(k, 2)=="":
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
               except Exception as e:
                   print e
                   print u"Excel,Err,第"+str(l+1)+u"行,"+self.sheetTestCase.cell_value(l,3)
                   newWs=self.newbk.get_sheet(1)
                   newWs.write(l,0,"error",self.styleRed)
                   self.newbk.save(self.fname)
                   page << p("<font color=red>[Error]</font> ",self.sheetTestCase.cell_value(l,3))  #输出测试用例
               
         # 是否生成VARHTMLFILE文档, 1=生成一个testreport.html; 2=生成多个带时间的html,如testreport20161205121210.html
         if self.sheetMain.cell_value(1,6) == 1:
           page.printOut(VARHTMLFILE)
           sleep(4)
           # send Email
           if self.sheetMain.cell_value(1,5)=="Y":
              self.sendemail(VARHTMLFILE)
         elif self.sheetMain.cell_value(1,6) == 2:
           page.printOut(VARHTMLFILEtimestamp)
           webbrowser.open_new_tab("file://" + VARHTMLFILEtimestamp)
           # send Email
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

    def showTblNameAndDDL(self,varDatabase,varTable,varKeyword):
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
            # 表中相同记录,去重处理
            if varTable not in list5:
                print "\n"
                print "-" * 70
                print "[" + varDatabase + " > " + varTable + "(" + t1[0] + ") > " + varKeyword + "]"
                print "-" * 70
                l_tablescount.append(varTable)
                reload(sys)
                sys.setdefaultencoding('utf8')
                page << p("<font color=blue>" + str(varDatabase) + " > " + str(varTable) + "(" + str(t1[0]) + ") > " + str(varKeyword) + "</font>")  # + " <font color=purple>" + str(col_name_list) + "</font>"

                for i in t2:
                    tblFieldcount=tblFieldcount+1
                    list0.append(i[0])
                    ii=i[1].replace("\r\n",",")
                    list2.append(ii.replace("  ",""))
                for i in range(tblFieldcount):
                    sum1 = sum1 + " , " + list0[i] + "(" + list2[i] +")"

                print sum1[2:]
                page << p("<font color=purple>" + str(sum1[2:]) + "</font>")
                list5.append(varTable)


        else:
            print "errorrrrrrr,数据库("+varDatabase+")中没有找到 "+ varTable +"表!"

    def output3(self,varDatabaseName,varSglTblName,varAllFields,varCur,d_keywords):

         for k in self.d_keywords:  # 遍历关键字
             if k in varAllFields:
                 varFieldtime=""
                 for m in range(len(varAllFields)):
                     m1 = re.search("Time",varAllFields[m],re.IGNORECASE)
                     if m1:
                         varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and %s=%s order by %s desc' % (varAllFields[m],varSglTblName,varAllFields[m],myfrtTime,myEndTime,k,eval(self.d_keywords[k]),varAllFields[m]))
                         numrows = int(varCur.rowcount)
                         for i in range(numrows):
                             row = varCur.fetchone()
                             varFieldtime="("+str(row[0])+") "+varFieldtime
                         if varFieldtime<>"":
                             alist.append(k)
                             alist.append(varAllFields[m])
                             alist.append(numrows)
                             alist.append(varFieldtime)
                         if numrows >= 1:  # 输出符合条件的字段及记录
                             self.showTblNameAndDDL(varDatabaseName,varSglTblName,alist[0])
                             # page << p("<font color=blue>" + str(varDatabaseName) + "</font> => " + "<font color=red>" + str(alist[0]) + "</font>")  # + " <font color=purple>" + str(col_name_list) + "</font>"
                             # page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(varAllFields) + "</font>")
                             varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and %s="%s" order by %s desc' % (varSglTblName,varAllFields[m],myfrtTime,myEndTime,k,eval(self.d_keywords[k]),varAllFields[m]))
                             t2=varCur.fetchall()
                             reload(sys)
                             sys.setdefaultencoding('utf-8')
                             sum=""
                             for j in range(numrows):
                                 l=0
                                 for k in t2[j]:
                                     sum =  sum + ", (" + str(varAllFields[l]) +")" + str(k)
                                     l=l+1
                                 print "~~~~~~~~"
                                 print str(j+1) +"), "+ str(sum[2:])
                                 page << p("<font color=green>" + str(j+1) +"), "+ str(sum[2:]).decode("utf-8").encode("utf-8") + "</font>")   # decode('unicode_escape')
                                 sum=""
                             del alist[:]
                         break  # 只获取当前表第一个带Time字段的值,忽略后面带Time的字段,如只获取 createTime , 忽略updateTime

    def t_userLogin(self,varDatabaseName,varTableName,varCur):
        print ">>>>>>> [" + str(varDatabaseName) + " , phone = " + str(varPhone) + "(" + varAuth + ") , tszNumber = " + str(mytszNumber) + " , userID = " + str(myuserID) + " , groupID = " + str(mygroupID) + " , " + str(VARPERIODTIME) + "]"
        page << p(">>>>>>> [" + str(varDatabaseName) + " , phone = " + str(varPhone) + " , userId = " + str(myuserID) + " , groupID = " + str(mygroupID) + " , " + str(VARPERIODTIME) + "]")
        varFieldtime=""  # 存放各表的时间

        x=0 # 统计输出多少张符合要求的表
        # d_keywords = {"userId" : myuserID, "user_id" : myuserID, "id" : myuserID, "id1" : myuserID,
        #                      "id2" : myuserID, "belongId" : myuserID, "accept_id" : myuserID, "friendid" : myuserID,
        #                      "th_id" : myuserID, "sd_id" : myuserID, "groupUserId" : myuserID, "submit_user_id" : myuserID,
        #                      "shareUserId" : myuserID, "userId1" : myuserID, "userId2" : myuserID, "oldUserId" : myuserID,
        #                      "userIdArray" : myuserID, "phone" : varPhone, "username" : varPhone,"contacts" : varPhone,
        #                      "userArray" : varPhone,"groupId" : mygroupID}

        for varSglTblName in varTableName: # 遍历所有的表, 获取每个表中所有字段 ,存入col_name_list
            if varSglTblName[0] == "beijing_store":  # 跳过此视图
                pass
            else:
                varCur.execute("select count(*) from %s" % varSglTblName[0])
                t0 = varCur.fetchone()
                if t0[0] <> 0: # 跳过空表
                    varCur.execute("select * from %s" % varSglTblName[0])
                    varAllFields = [tuple[0] for tuple in varCur.description]  # 获取表中所有字段
                    # 遍历表中包含以下字段de记录并保存到数组
                    self.output3(varDatabaseName,varSglTblName[0],varAllFields,varCur,self.d_keywords)

                    # arrowSymbol=">"
                    # print arrowSymbol * 150
                    # page << p(arrowSymbol * 150)
        # 获取影响的表数量,去重统计
        l_tablescount2 = {}.fromkeys(l_tablescount).keys()
        print u"[affected " + str(len(l_tablescount2)) + " tables]\n"
        page << p("<font color=red> [affected " + str(len(l_tablescount2)) + " tables]</font> ")
        del l_tablescount[:]

    def drv_ukardweb(self):
        self.TestcaseModule()

    def t_ukardweb(self):
        print "1111"
        # self.t_userLogin(self.curWeb,self.ukardwebTable)

    def t_sendRed(self):
        print "2222"

    def t_responseTables(self):
        print "3333"
        self.t_userLogin("ukardweb",ukardwebTable,curWeb)
        self.t_userLogin("ukardapp",ukardappTable,curApp)
        self.t_userLogin("game",gameTable,curGame)



    def drv_game(self):
        # game
        self.TestcaseModule()
    def t_game(self):
        self.t_userLogin(self.curGame,self.gameTable)


if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TszTable) 
    unittest.TextTestRunner(verbosity=2).run(suite1)

