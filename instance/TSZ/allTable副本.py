# coding: utf-8
# s="中文"
# if isinstance(s, unicode):
#    #s=u"中文"
#    print s.encode('utf-8')
# else:
#    #s="中文"
#    print s.decode('utf-8').encode('utf-8')
#****************************************************************
# Author     : John
# Version    : 1.0.0
# Date       : 2016-5-27
# Description: TSZ alltable
#****************************************************************

import os,sys,unittest,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,re
import xlwt,xlrd,chardet,random,webbrowser
# import HTMLTestRunner,smtplib
from time import sleep
from xlwt.Style import *
from xlrd import open_workbook
from xlutils.copy import copy
from PIL import Image
import time
from datetime import datetime, timedelta

# ========== Test Area ==========
# DATETIME_FMT = "2016-12-06 12:23:11"
# xx=DATETIME_FMT.split(' ')
# yy=xx[0].split('-')
# print str(yy[0])+"-"+str(yy[1])+"-"+str(yy[2])+" 23:59:59"

# 日期 : http://www.open-open.com/lib/view/open1410416920211.html
# http://canlynet.iteye.com/blog/1543184
# ========== Test Area ==========


# ========== Param ==========
myPhone="13816101118"
File_ExcelName = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/excel/tszTable.xls"
Html_Testreport = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/report/testreport.html" # TestReport文件
Err_Screenshot = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/screenshot/"  # 错误截屏
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
# ISOTIMEFORMAT="%Y-%m-%d"
# # 返回当天日期 如 2016-06-12
# myfrtTime=time.strftime( ISOTIMEFORMAT, time.localtime() )
# myEndTime=myfrtTime+" 23:59:59"
# myfrtTime=myfrtTime+" 00:00:01"
# print "[有效时间段: " + myfrtTime+" ~ " +myEndTime +"]"

class TszTable(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.fname=File_ExcelName
        bk = xlrd.open_workbook(File_ExcelName,formatting_info=True)
        self.bk=bk
        newbk=copy(bk)
        self.newbk=newbk
        styleP = xlwt.easyxf('font: name Times New Roman, color-index blue')
        styleE = xlwt.easyxf('font: name Times New Roman, color-index red')
        self.styleP=styleP
        self.styleE=styleE
        #conn= MySQLdb.connect(host=myHost, user=myUserpasswd, passwd=myUserpasswd, db='ukardweb', port=myPort, use_unicode=True) #sit2 参数化失败
        #conn= MySQLdb.connect(host='192.168.2.144', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit
        #conn= MySQLdb.connect(host='192.168.2.100', user='lvjinyue', passwd='lvjinyue', db='ukardweb', port=3307, use_unicode=True) #uat

        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        curT = conn.cursor()
        conn.set_character_set('utf8')
        curT.execute('SET NAMES utf8;')
        curT.execute('SET CHARACTER SET utf8;')
        curT.execute('SET character_set_connection=utf8;')
        self.curT=curT
        self.curT.execute('show tables')
        ukardwebTables=self.curT.fetchall()
        self.ukardwebTables=ukardwebTables
        self.conn=conn

        conngame= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        curgame = conngame.cursor()
        conngame.set_character_set('utf8')
        curgame.execute('SET NAMES utf8;')
        curgame.execute('SET CHARACTER SET utf8;')
        curgame.execute('SET character_set_connection=utf8;')
        self.curgame=curgame
        self.curgame.execute('show tables')
        gameTables=self.curgame.fetchall()
        self.gameTables=gameTables
        self.conngame=conngame

        print "\n"
        print "============================= test start =============================="
        # [9,ta_message 运营-审核消息任务表]
        #   id,m_type= '消息类型',m_status= '0等待执行 1执行成功 2执行失败 其他json错误', m_content= '消息内容',oper_time = '操作时间',
        #   m_from= '来源',ver = '版本',busi_id= '业务编号',result = '回执结果',from_id = '来源编号', msg_id = '信息标识',
        #   phone = '用户手机号',verify_code = '动态验证码',
        #cur.execute('select verify_code from ta_message where phone="13816109050" order by id desc limit 1')
        self.curT.execute('select oper_time,verify_code,result,m_content from ta_message where phone=%s order by id desc limit 1' % (myPhone))
        data9 = self.curT.fetchone()
        if str(data9[1])=="":
           print u"ta_message => 最近一次充值 m_content:" + data9[3]
        else:
           print "ta_message => [" + myPhone + "," + str(data9[1]) + ", oper_time = " + str(data9[0]) + "]"

        # [0,t_user]
        self.curT.execute('select id,username,nickname,regist_time,login_time,first_login_time,commission_residue,last_withdraw_time,commission_withdraw,rechargeAmount from t_user where username="%s" order by id desc limit 0,1' % (myPhone))
        data0 = self.curT.fetchone()
        self.myuserID = data0[0]
        self.myfrtTime=str(data0[5])

        # 获取某个时间段的日期, 如只查找指定时间段内表中数据的变化.
        # tmpxx=self.myfrtTime.split(' ')
        # tmpyy=tmpxx[0].split('-')
        # self.myEndTime= str(tmpyy[0])+"-"+str(tmpyy[1])+"-"+str(tmpyy[2])+" 23:59:59"
        # print "[有效时间段: " + self.myfrtTime+" ~ " +self.myEndTime +"]"

        # 返回当天日期 如 2016-06-12
        ISOTIMEFORMAT="%Y-%m-%d"
        myfrtTime=time.strftime( ISOTIMEFORMAT, time.localtime() )
        self.myEndTime=myfrtTime+" 23:59:59"
        self.myfrtTime=myfrtTime+" 00:00:01"
        print "[有效时间段: " + self.myfrtTime+" ~ " + self.myEndTime +"]"

        print "t_user => [" + data0[1] +","+ str(data0[0])+","+ str(data0[2])+ u",可提现金:"+str(data0[6])+u",上次提现时间:"+str(data0[7])+u",提现金额:"+str(data0[8])\
              +u",充值金额:"+str(data0[9]) +u",注册时间:"+str(data0[3])+u",登录时间:"+str(data0[4])+u",首次登录时间:"+str(data0[5])
        # 账户余额 = 佣金余额 + 充值金额(大咖)
        print u"t_user => [账户余额:"+ str((data0[6]+data0[9])/100.00) +"]" +"\n"

        # DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
        # atime = timedelta(days=1)
        # now = datetime.strptime(self.myfrtTime,DATETIME_FMT)
        # self.hour24=now + atime
        # print self.hour24
        # sleep(3)
        # print self.hour24.split(':')
        # xx=self.hour24.split(':')
        # print xx[2]

        # today_zero_time = datetime.datetime.strftime(self.myfrtTime,DATETIME_FMT)
        # print today_zero_time
        # today_zero_time1 = datetime.datetime.strftime(self.hour24, '%Y-%m-%d %H:%M:%S')
        # print today_zero_time1

        # print 'hour: %s  minute: %s  second: %s' %(now.hour, now.minute, now.second)
        # print 'weekday: %s ' %(now.weekday()+1)  #一周是从0开始的

    @classmethod
    def tearDownClass(self):
        self.conn.commit()
        self.curT.close()
        self.conn.close()
        self.conngame.commit()
        self.curgame.close()
        self.conngame.close()
        # 遍历report目录中最新的文件
        # result_dir = 'C:\\Python27\\TMPappium\\report'
        # lists=os.listdir(result_dir)
        # lists.sort(key=lambda fn: os.path.getmtime(result_dir+"\\"+fn) if not
        # os.path.isdir(result_dir+"\\"+fn) else 0)
        # #print ('最新的文件为： '+lists[-1])
        # file_new = os.path.join(result_dir,lists[-1])
        # #print file_new
    def test_Main(self):
        u"""主程序"""
        sh1 = self.bk.sheet_by_name("Main")
        sh2 = self.bk.sheet_by_name("TestCase")
        self.sh1=sh1
        self.sh2=sh2
        #遍历Main执行函数模块
        for i in range(1,sh1.nrows):
            if sh1.cell_value(i,0) == "Y":
                tmpMain1=sh1.cell_value(i,1)
                tmpMain2=sh1.cell_value(i,2)
                tmpMain3=sh1.cell_value(i,3)
                self.tmpMain1=tmpMain1
                self.tmpMain2=tmpMain2
                self.tmpMain3=tmpMain3
                #执行函数模块
                exec(sh1.cell_value(i,4))
        #send Email
        if sh1.cell_value(1,5) == "Y":
            # self.sendemail()
            pass
    def TestcaseModule(self):
         #遍历TestCase及调用函数模块
         case1=caseN=0
         for j in range(1,self.sh2.nrows):
              case1=case1+1
              # 定位测试用例位置及数量
              if self.sh2.cell_value(j,1) == self.tmpMain1 and self.sh2.cell_value(j,2) == self.tmpMain2:
                  #假设有100个Case，实际不会有那么多Case
                  for k in range(case1+1,100):
                      if k + 1 > self.sh2.nrows:
                           #print "这是最后一行TestCase"
                           caseN=caseN+1
                           break
                      elif self.sh2.cell_value(k,1)=="" and self.sh2.cell_value(k,2)=="":
                           caseN=caseN+1
                      # elif  self.sh2.cell_value(k,1)=="skip" or self.sh2.cell_value(k,2)=="skip":
                      #      caseN=caseN+1
                      else:
                           caseN=caseN+1
                           break
                  break
         #遍历 Testcase1~TestCaseN
         for l in range(case1,caseN+case1):
               # 定位参数从第6列开始，遍历10列
               str_list=[]
               for m in range(6,15):  #id0 - id9
                     if self.sh2.cell(l,m).value <> "" :
                          N = self.sh2.cell_value(l,m)
                          str_list.append(str(N))
                     else:
                         break
               self.str_list=str_list
               try :
                   if self.sh2.cell_value(l,1)=="skip" or self.sh2.cell_value(l,2)=="skip":
                       newWs=self.newbk.get_sheet(1)
                       newWs.write(l,0,"skip",self.styleP)
                       self.newbk.save(self.fname)
                   else:
                       exec(self.sh2.cell_value(l,4))
                       newWs=self.newbk.get_sheet(1)
                       newWs.write(l,0,"pass",self.styleP)
                       self.newbk.save(self.fname)
                       # page << p("<font color=blue>[Pass]</font> ",self.sh2.cell_value(l,3))  #输出测试用例

               except:
                   print u"Excel,Err,第"+str(l+1)+u"行,"+self.sh2.cell_value(l,3)
                   newWs=self.newbk.get_sheet(1)
                   newWs.write(l,0,"error",self.styleE)
                   self.newbk.save(self.fname)
                   # page << p("<font color=red>[Error]</font> ",self.sh2.cell_value(l,3))  #输出测试用例
               # page.printOut(Html_Testreport)
               #open HTML
               # if self.sh1.cell_value(1,6) == "Y":
               #    webbrowser.open(Html_Testreport)



    ###################################################################################################
    def drv_ukardweb(self):
         # 用户第一次登录
         self.TestcaseModule()
    def drv_game(self):
        # game
        self.TestcaseModule()


    def t_userLogin(self,cur,tables):

        print "============================= Login ==============================遍历usernamme,phone,id,user_id,userId,userid"
        # C1-1, 用户第一次登录app,（t_user , ta_message , t_redgroup_baseinfo , t_redgroup_countinfo）
        # 生成

        for AT in tables:
            #print AT[0]  # 所有表
            # 获取表中所有字段
            self.cur.execute("select * from %s" % AT[0])
            col_name_list = [tuple[0] for tuple in self.cur.description]
            #print col_name_list

            # 判断如果表中id字段, 如果不存在则跳过此表, 否则遍历此表统计数量,忽略空表.
            if 'id' in col_name_list:
                self.cur.execute('select count(id) from %s' % (AT[0]))
                t1 = self.cur.fetchone()
                if t1[0] == 0:
                    pass
                    # print AT[0]
                else:
                    #print AT[0] + " => " + str(t1[0])
                    # 列表 phone = {myPhone}的表 ,检查字段 phone
                    if 'phone' in col_name_list:
                        self.cur.execute('select count(id) from %s where phone="%s" order by id desc ' % (AT[0],myPhone))
                        #cur.execute('select count(id) from t_agent_busi where phone="13816109050" order by id desc ')  //test
                        t2=self.cur.fetchone()
                        if t2[0]<>0:
                            print AT[0] + u" => [phone(" + str(myPhone) + ") = " +  str(t2[0]) + "]"

                    if 'username' in col_name_list:
                        #Truncated incorrect DOUBLE value解决办法, 将%s 改为 '%s'
                        self.cur.execute('select count(id) from %s where username="%s" order by id desc ' % (AT[0],myPhone))
                        t2=self.cur.fetchone()
                        if t2[0]<>0:
                            print AT[0] + u" => [username(" + str(myPhone) + ") = " + str(t2[0]) + "]"

                    if 'user_id' in col_name_list:
                        #Truncated incorrect DOUBLE value解决办法, 将%s 改为 '%s'
                        self.cur.execute('select count(id) from %s where user_id="%s" order by id desc ' % (AT[0],self.myuserID))
                        t2=self.cur.fetchone()
                        if t2[0]<>0:
                            print AT[0] + u" => [user_id(" + str(self.myuserID) + ") = "+  str(t2[0]) + "]"

                    if 'id' in col_name_list:
                        #Truncated incorrect DOUBLE value解决办法, 将%s 改为 '%s'
                        self.cur.execute('select count(id) from %s where id="%s" order by id desc ' % (AT[0],self.myuserID))
                        t2=self.cur.fetchone()
                        if t2[0]<>0:
                            print AT[0] + u" => [id(" + str(self.myuserID) + ") = "+  str(t2[0]) + "]"

                    if 'userid' in col_name_list:
                        #Truncated incorrect DOUBLE value解决办法, 将%s 改为 '%s'
                        self.cur.execute('select count(id) from %s where userid="%s" order by id desc ' % (AT[0],self.myuserID))
                        t2=self.cur.fetchone()
                        if t2[0]<>0:
                            print AT[0] + " => [userid(" + str(self.myuserID) + ") = "+  str(t2[0]) + "]"

                    if 'userId' in col_name_list:
                        #Truncated incorrect DOUBLE value解决办法, 将%s 改为 '%s'
                        self.cur.execute('select count(id) from %s where userId="%s" order by id desc ' % (AT[0],self.myuserID))
                        t2=self.cur.fetchone()
                        if t2[0]<>0:
                            print AT[0] + " => [userId(" + str(self.myuserID) + ") = "+  str(t2[0]) + "]"
                        # if t2[0]==3:  #t_user_thirdInfo
                        #     for i in range(3):
                        #         cur.execute('select * from t_user_thirdInfo where userId="%s" order by id desc limit %s,1' % (myuserID,i))
                        #         t3=cur.fetchone()
                        #         if t3[5] != "0":
                        #            print "Err,t_user_thirdInfo,channel = " + t3[4] + ",isValid = " + t3[5]

                    # 遍历列表定位字段 如: 获取所有 带time的字段 ,忽略大小写

                    for m in range(len(col_name_list)):
                         m1=re.search("Time",col_name_list[m],re.IGNORECASE)
                         if m1:
                             #print AT[0] + " => " + col_name_list[m]

                             if col_name_list[m]  in col_name_list:  #time
                             #Truncated incorrect DOUBLE value解决办法, 将%s 改为 '%s'
                                 # print col_name_list[m]
                                 #print self.myfrtTime
                                 #self.cur.execute('select count(id) from t_agent_busi where createTime="2016-04-12 18:55:51"')
                                 #self.cur.execute("select * from t_agent_busi where phone like '%%%s%%'" % x)
                                 #self.cur.execute("select * from t_agent_busi where CONVERT(createTime,120) like '%2016%'")
                                 #SELECT * FROM AT where CONVERT(varchar,DateTime) like '%2011-%' 转
                                 # 获取 时间为t_user登录时间的表  Where CheckDate Between '2013-01-01' And '2013-01-31'   Select DATEADD(DAY,1,'20130101')

                                 # self.cur.execute('select * from %s where %s="%s" ' % (AT[0],col_name_list[m],self.myfrtTime))
                                 if 'user_id' in col_name_list:
                                    #Truncated incorrect DOUBLE value解决办法, 将%s 改为 '%s'
                                    self.cur.execute('select count(id) from %s where user_id="%s" order by id desc ' % (AT[0],self.myuserID))
                                    t2=self.cur.fetchone()
                                    if t2[0]<>0:
                                         #print AT[0] + u" => [user_id,共有 = " +  str(t2[0]) + u"条]" # {myuserID}记录共有N条,无条件限制.
                                         # 符合有效期时间内 的 {myuserID}记录 ,如输出:  t_redgroup_baseinfo => [createTime = (2016-06-06 14:11:53) ]
                                         self.cur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and user_id=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],self.myfrtTime,self.myEndTime,self.myuserID,col_name_list[m]))
                                         numrows = int(self.cur.rowcount)    # 循环numrows次，每次取出一行数据
                                         x=""
                                         num=0
                                         for i in range(numrows):
                                            row = self.cur.fetchone()
                                            x="("+str(row[0])+") "+x
                                            num=num+1
                                         if x<>"":
                                             print AT[0] + " => [user_id("+ str(self.myuserID) +") = " + str(num)  + " , " + col_name_list[m]  +  x + "]"

                                 if 'userId' in col_name_list:
                                    #Truncated incorrect DOUBLE value解决办法, 将%s 改为 '%s'
                                    self.cur.execute('select count(id) from %s where userId="%s" order by id desc ' % (AT[0],self.myuserID))
                                    t2=self.cur.fetchone()
                                    if t2[0]<>0:
                                         # print AT[0] + u" => [userId,共有 = " +  str(t2[0]) + u"条]" # {myuserID}记录共有N条,无条件限制.
                                         # 符合有效期时间内 的 {myuserID}记录 ,如输出:  t_redgroup_baseinfo => [createTime = (2016-06-06 14:11:53) ]
                                         self.cur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and userId=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],self.myfrtTime,self.myEndTime,self.myuserID,col_name_list[m]))
                                         numrows = int(self.cur.rowcount)    # 循环numrows次，每次取出一行数据
                                         x=""
                                         num=0
                                         for i in range(numrows):
                                            row = self.cur.fetchone()
                                            x="("+str(row[0])+") "+x
                                            num=num+1
                                         if x<>"":
                                             print AT[0] + " => [userId("+ str(self.myuserID) +") = " + str(num) + " , " + col_name_list[m]  +  x + "]"

                                 if 'userid' in col_name_list:
                                    #Truncated incorrect DOUBLE value解决办法, 将%s 改为 '%s'
                                    self.cur.execute('select count(id) from %s where userid="%s" order by id desc ' % (AT[0],self.myuserID))
                                    t2=self.cur.fetchone()
                                    if t2[0]<>0:
                                         # print AT[0] + u" => [userId,共有 = " +  str(t2[0]) + u"条]" # {myuserID}记录共有N条,无条件限制.
                                         # 符合有效期时间内 的 {myuserID}记录 ,如输出:  t_redgroup_baseinfo => [createTime = (2016-06-06 14:11:53) ]
                                         self.cur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and userid=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],self.myfrtTime,self.myEndTime,self.myuserID,col_name_list[m]))
                                         numrows = int(self.cur.rowcount)    # 循环numrows次，每次取出一行数据
                                         x=""
                                         num=0
                                         for i in range(numrows):
                                            row = self.cur.fetchone()
                                            x="("+str(row[0])+") "+x
                                            num=num+1
                                         if x<>"":
                                             print AT[0] + " => [userid("+ str(self.myuserID) +") = " + str(num)  + " , " +  col_name_list[m]  +  x + "]"

                                 if 'id' in col_name_list:
                                     #Truncated incorrect DOUBLE value解决办法, 将%s 改为 '%s'
                                     self.cur.execute('select count(id) from %s where id="%s" order by id desc ' % (AT[0],self.myuserID))
                                     t2=self.cur.fetchone()
                                     if t2[0]<>0:
                                         # print AT[0] + u" => [id,共有 = " +  str(t2[0]) + u"条]" # {myuserID}记录共有N条,无条件限制.
                                         # 符合有效期时间内 的 {myuserID}记录 ,如输出:  t_redgroup_baseinfo => [createTime = (2016-06-06 14:11:53) ]
                                         self.cur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and id=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],self.myfrtTime,self.myEndTime,self.myuserID,col_name_list[m]))
                                         numrows = int(self.cur.rowcount)    # 循环numrows次，每次取出一行数据
                                         x=""
                                         num=0
                                         for i in range(numrows):
                                            row = self.cur.fetchone()
                                            x="("+str(row[0])+") "+x
                                            num=num+1
                                         if x<>"":
                                             print AT[0] + " => [id("+ str(self.myuserID) +") = " + str(num)  + " , " + col_name_list[m]  +  x + "]"

                                 if 'phone' in col_name_list:
                                    self.cur.execute('select count(id) from %s where phone="%s" order by id desc ' % (AT[0],myPhone))
                                    #cur.execute('select count(id) from t_agent_busi where phone="13816109050" order by id desc ')  //test
                                    t2=self.cur.fetchone()
                                    if t2[0]<>0:
                                         #print AT[0] + u" => [phone = "  +  str(t2[0]) + "]"
                                         # 符合有效期时间内 的 {myuserID}记录 ,如输出:  t_redgroup_baseinfo => [createTime = (2016-06-06 14:11:53) ]
                                         self.cur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and phone=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],self.myfrtTime,self.myEndTime,myPhone,col_name_list[m]))
                                         numrows = int(self.cur.rowcount)    # 循环numrows次，每次取出一行数据
                                         x=""
                                         num=0
                                         for i in range(numrows):
                                            row = self.cur.fetchone()
                                            x="("+str(row[0])+") "+x
                                            num=num+1
                                         if x<>"":
                                             print AT[0] + " => [phone("+ str(myPhone) +") = " + str(num)  + " , " +col_name_list[m]  +  x + "]"

                                 if 'username' in col_name_list:
                                    #Truncated incorrect DOUBLE value解决办法, 将%s 改为 '%s'
                                    self.cur.execute('select count(id) from %s where username="%s" order by id desc ' % (AT[0],myPhone))
                                    t2=self.cur.fetchone()
                                    if t2[0]<>0:
                                         # print AT[0] + u" => [username = " + str(t2[0]) + "]"
# 符合有效                                # 期时间内 的 {myuserID}记录 ,如输出:  t_redgroup_baseinfo => [createTime = (2016-06-06 14:11:53) ]
                                         self.cur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and username=%s order by "%s" desc' % (col_name_list[m],AT[0],col_name_list[m],self.myfrtTime,self.myEndTime,myPhone,col_name_list[m]))
                                         numrows = int(self.cur.rowcount)    # 循环numrows次，每次取出一行数据
                                         x=""
                                         num=0
                                         for i in range(numrows):
                                            row = self.cur.fetchone()
                                            x="("+str(row[0])+") "+x
                                            num=num+1
                                         if x<>"":
                                             print AT[0] + " => [username("+ str(myPhone) +") = " + str(num)  + " , " + col_name_list[m]  +  x + "]"

                                 # self.cur.execute('select count(id) from %s where user_id="%s" order by id desc ' % (AT[0],self.myuserID))
                                 # t2=self.cur.fetchone()
                                 # print t2

                                 #select createTime from t_agent_busi where createTime='2016-04-06 17:28:23'
                                 #self.cur.execute('select %s from %s where %s="%s" ' % (col_name_list[m],AT[0],col_name_list[m],pp))
                                 #self.cur.execute('select count(id) from %s where %s="%s" ' % (AT[0],col_name_list[m],self.myfrtTime))

                                 #t2=self.cur.fetchone()
                                 #rows = self.cur.fetchall()

                                 # #print rows[0]
                                 # for row in rows:
                                 #     for i in range(row[0]):
                                 #        print str(row[i])+"~~~~~"



                                 # if t2<>None :
                                 #      #print t2[0]
                                 #      if t2[0]>0:
                                 #          for row in rows[1]:
                                 #              print row
                                 #          print AT[0] + u" => "+ col_name_list[m] +" * "+str(t2[0]) + " [ "+str(t2[1]) +"]"
                                          #print t2[1]
                                          # for tt in t2[1]:
                                          #       print tt
                                          #print x
                                          #print AT[0] + " => ["+col_name_list[m] + " = " +  str(t2[0]) + "]"


    def t_playround(self):
        print "12121"
        # self.t_userLogin(self.curgame,self.gameTables)



    def bridingThird(self):
        print "============================= 第三方授权 =============================="
        # C1-2, 绑定第三方授权（t_user_thirdInfo , t_user , t_redgroup_baseinfo）
        # 操作: 绑定点击"QQ" ,头像 和 昵称 调用QQ
        # 相关表：t_user_thirdInfo, 用户头像和昵称修改表 t_user ,t_redgroup_baseinfo
        # 规则1:头像绑定优先级从高到低，"微信、QQ、微博" ，优先级高的覆盖优先级低的,譬如先绑定微博,头像和昵称调用微博的,然后绑定微信,头像和昵称调用微信,再绑定QQ,头像和昵称仍然是微信的.
        # 规则2:如果用户修改了头像或昵称，则再绑定时 不再调用 第三方的 头像或昵称

        for AT in self.ukardwebTables:
            #print AT[0]  # 所有表
            # 获取表中所有字段
            self.cur.execute("select * from %s" % AT[0])
            col_name_list = [tuple[0] for tuple in self.cur.description]
            #print col_name_list
            # 判断如果表中id字段, 如果不存在则跳过此表, 否则遍历此表统计数量,忽略空表.
            if 'id' in col_name_list:
                self.cur.execute('select count(id) from %s' % (AT[0]))
                t1 = self.cur.fetchone()
                if t1[0] == 0:
                    pass
                else:
                    if 'userId' in col_name_list:
                        self.cur.execute('select count(id) from %s where userId="%s" order by id desc ' % (AT[0],self.myuserID))
                        t2=self.cur.fetchone()
                        if t2[0]<>0:
                            print AT[0] + " => [userId = " +  str(t2[0]) + "]"
                        if AT[0]=="t_user_thirdInfo":
                            self.cur.execute('select nickname,head_pic from t_user where id="%s" order by id desc ' % (self.myuserID))
                            t3=self.cur.fetchone()
                            print AT[0] + " => " + t3[0] +" > " + t3[1]
                        if AT[0]=="t_redgroup_baseinfo":
                            self.cur.execute('select brandContent,LogoURL from t_redgroup_baseinfo where userId="%s" order by id desc ' % (self.myuserID))
                            t3=self.cur.fetchone()
                            print AT[0] + " => " + t3[0] +" > " + t3[1]

        print "========== ????  =========="

        # # [1,t_extension_channel 渠道推广红包渠道记录表]
        # # id,userId=10001679,extensionRedPoolId=渠道推广红包池Id,channel=1外平台2抢红包3红包群4二维码,
        # # channelRedNumber=红包总数,channelRedNoLeadNumber=未领红包总数，channelRedSumAmout=红包总金额,channelRedAmout=红包单个金额,
        # # source=推广来源（1微信2支付宝3余额），cityId，redType=红包类型（21推广红包22推广短信红包26推广体验金红包），createTime,updateTime,
        # # redState=红包状态（1正常2回收3审核退回）
        # cur.execute('select * from t_extension_channel order by id desc limit 1')
        # data1 = cur.fetchone()
        # if data1[1]<>myuserID:print "Err,Last1 = " + str(data1[1]) + " , not " + str(myuserID) + " ,[1,t_extension_channel]" + "\n"
        # else:print "Last1 = "+ str(myuserID) +u",渠道"+ data1[3] +u",红包总数"+ str(data1[4])+u",未领红包数"+str(data1[5])+u",总金额" + str(data1[6]) \
        #            + u",单金额" + str(data1[7]) + u",来源" + str(data1[8]) + u",类型" + str(data1[10]) + ",time"+str(data1[11]) + " [1,t_extension_channel]" + "\n"
        #
        #
        # # [2,t_extension_channel_redPool 渠道推广红包主表]
        # #   id,userId=10001679,redNumber=红包总数量',redLeadNumber=已领红包总数量',redNoLeadNumber=未领红包总数量',redGenerateNumber=已生成红包个数',
        # #   redType=红包类型(21:推广红包，22：推广短信红包，26：推广体验金红包)',
        # #   redState=红包状态 0:未分享,1:已分享,2:已过期,4:新建记录,5:未成功充值',
        # #   redSumAmount=红包总金额',extensionSub='推广内容',createTime,updateTime,cityId,source= '推广来源，1 微信，2 支付宝，3 余额',
        # #   transFee= '交易总费率',extensionUrl='渠道推广红包的推广链接',auditStatus='审核状态(0:审核通过,1:审核不过)',
        # #   refundAmount='退款金额',brandContent='品牌/商户名称',downloadCount='未登录用户点击下载数',openCount='红包打开次数',linkOpenCount= '图片链接打开次数',
        # #   type='0正常充值,1体验金,2大咖',surplusAmount= '剩余金额',
        # cur.execute('select * from t_extension_channel_redPool order by id desc limit 1')
        # data2 = cur.fetchone()
        # if data2[1]<>myuserID:print "Err,Last1 = "+str(data2[1])+" , not "+ str(myuserID) + " ,[2,t_extension_channel_redPool]"+ "\n"
        # else:print "Last1 = "+ str(myuserID) + u",红包总数" + str(data2[2]) + u",已领红包数" + str(data2[3]) + u",未领红包数" + str(data2[4]) \
        #            + u",生成红包个数" + str(data2[5]) + u",类型" + str(data2[6]) + u",红包总金额" + str(data2[8]) + u",来源" + str(data2[13]) + u",退款金额" + str(data2[17]) \
        #            + u",充值类型" + str(data2[22]) + u",剩余金额" + str(data2[23]) + " [2,t_extension_channel_redPool]" + "\n"
        #
        # # [3,t_external_redPool 红包池-外部红包池(主表)]
        #   # id,redAmount='红包金额',redType='红包类型  社交好友:16,体验金社交好友：27',
        #   # redNumber='红包总数量',redLeadNumber='已领红包总数量',redNoLeadNumber='未领红包总数量',
        #   # userid=10001679,tranid= '交易id',redState='红包状态 0.未激活1,已激活2.已过期3无效  4回收  5 :未分享  6: 未分享已过期',
        #   # payOutAmount='补贴金额 ', payInAmount='溢出金额 ',busiId='商户id',storeId='门店id',storeCityId='门店所属城市',createTime,updateTime,busiName='商户名称',storeName='门店名称',
        #   # tranAmount='交易金额',extensionId='推广红包ID',extensionType='推广红包类型(0:消费推广红包,1:用户推广红包)',
        #   # downloadCount='未登录用户点击下载数',openCount='红包打开次数',linkOpenCount='图片链接打开次数',
        #   # channelId ='渠道ID',batchId='批次ID',
        # cur.execute('select * from t_external_redPool order by id desc limit 1')
        # data3 = cur.fetchone()
        # if data3[6]<>myuserID:print "Err,Last1 = "+str(data3[6])+" , not "+ str(myuserID) + " ,[3,t_external_redPool]" + "\n"
        # else:print "Last1 = "+ str(myuserID) + u",红包金额" + str(data3[1]) + u",红包总数量" + str(data3[3]) + u",已领红包总数量" + str(data3[4]) \
        #            + u",未领红包总数量" + str(data3[5]) + u",推广红包ID=" + str(data3[19]) + u",渠道ID=" + str(data3[24]) + u",批次ID=" + str(data3[25]) + " [3,t_external_redPool]" + "\n"
        #
        #
        # # [4,t_external_redDetail 红包池-外部红包明细表]
        # #   id,redPoolId='红包池id',userId ='发红包者',redType='红包类型',belongId='红包所属人',storeId='门店id',busiId='商户id',storeCityId='门店所属城市',
        # #   redState='红包状态 1.未领2.占用3.已领4.平台回收,5.推广红包审核未通过',
        # #   amount='红包金额',createTime,updateTime
        # #   belongNam='领取人第三方名称',belongThumb='领取人第三方头像',
        # #   extensionId='推广红包ID',extensionType= '推广红包类型(0:消费推广红包,1:用户推广红包)',
        # #   experienceAmount='体验金',actualAmount='实际领到金额',channelId='渠道ID',batchId='批次ID',
        # #   channelType='渠道类型(1：外平台,3：红包群,4:二维码)',belongOpenId='领取人第三方标识ID',isLeadEnd'是否领完(0:未领完,1:领完)',
        # cur.execute('select * from t_external_redDetail  order by id desc limit 0,1')
        # data4 = cur.fetchone()
        # # 红包发包者 userID
        # if data4[2]<>myuserID:print "Err,Last1 = "+str(data4[2]) + " , not " + str(myuserID) + " ,[4,t_external_redDetail]" + "\n"
        # else:print "Last1 = "+ str(myuserID) + u",红包池id=" + str(data4[1]) + u",发红包者" + str(data4[2]) + u",红包所属人" + str(data4[4]) \
        #            + u",红包状态" + str(data4[8]) + u",红包金额" + str(data4[9]) + u",推广红包ID=" + str(data4[14]) + u",实际领到金额=" + str(data4[17]) + u",渠道ID=" + str(data4[18]) \
        #            + u",批次ID=" + str(data4[19]) + u",渠道类型=" + str(data4[20]) + u",是否领完=" + str(data4[22]) + " [4,t_external_redDetail]" + "\n"
        #
        # # [5,t_internal_redPool 红包池-内部红包池(主表)]
        # #   id,redAmount='红包金额',redType='红包类型  app好友:11  同城好友:14',
        # #   redNumber='红包总数量', redLeadNumber='已领红包总数量',redNoLeadNumber='未领红包总数量',
        # #   userid = '用户ID',tranid = '交易id',
        # #   redState ='红包状态 0.未激活1,已激活2.已过期3无效  4回收  5 :未分享  6: 未分享已过期',
        # #   payOutAmount ='补贴金额 ', payInAmount= '溢出金额 ', busiId='商户id',storeId = '门店id',storeCityId ='门店所属城市',createTime,updateTime
        # #   appRedPoolId ='APP好友红包池ID（只有同城红包池用到）',busiName= '商户名称',storeName= '门店名称',extensionId='推广红包ID',
        # #   extensionType= '推广红包类型(0:消费推广红包,1:用户推广红包)',channelId = '渠道ID',batchId = '批次ID',
        # cur.execute('select * from t_internal_redPool order by id desc limit 0,1')
        # data5 = cur.fetchone()
        # if data5[6]<>myuserID:print "Err,Last1 = " + str(data5[6]) + " , not " + str(myuserID) + " ,[5,t_internal_redPool]" + "\n"
        # else:print "Last1 = "+ str(myuserID) + u",红包金额=" + str(data5[1]) + u",红包总数量" + str(data5[3]) + u",已领红包总数量" + str(data5[4]) \
        #            + u",未领红包总数量" + str(data5[5]) + u",补贴金额" + str(data5[9]) + u",溢出金额=" + str(data5[10]) + u",推广红包ID=" + str(data5[19]) + u",渠道ID=" + str(data5[21]) \
        #            + u",批次ID=" + str(data5[22]) + " [5,t_internal_redPool]" + "\n"
        #
        # # [6,t_internal_redDetail 红包池-内部红包明细表]
        # #   id,redPoolId= '红包池id',userId = '发红包者',redType= '红包类型',belongId = '红包所属人',storeId =  '门店id',busiId = '商户id',storeCityId = '门店所属城市',
        # #   redState = '红包状态 1.未领2.占用3.已领4.平台回收,5.推广红包审核未通过',amount='红包金额',createTime,
        # #   appRedPoolId= 'APP好友红包池ID（只有同城红包池用到）',updateTime,extensionId= '推广红包ID',extensionType= '推广红包类型(0:消费推广红包,1:用户推广红包)',
        # #   channelId='渠道ID',batchId='批次ID',
        # cur.execute('select * from t_internal_redDetail order by id desc limit 0,1')
        # data6 = cur.fetchone()
        # if data6[2]<>myuserID:print "Err,Last1 = " + str(data6[2]) + " , not " + str(myuserID) + " ,[6,t_internal_redDetail]" + "\n"
        # else:print "Last1 = "+ str(myuserID) + u",红包池id=" + str(data6[1]) + u",发红包者" + str(data6[2]) + u",红包所属人" + str(data6[4]) + u",红包金额" + str(data6[9]) \
        #            + u",推广红包ID=" + str(data6[13]) +  u",渠道ID=" + str(data6[15])  + u",批次ID=" + str(data6[16]) + " [6,t_internal_redPool]" + "\n"
        #
        # # [7,t_extension_fallinto 推广分成表,分享奖励红包]
        # #   id,userId='发红包者',userOpenId='发送人第三方ID',belongId='红包所属人',batchId = '批次ID ',channelId = '渠道ID', redId = '红包ID',
        # #   redAmount ='红包金额', redType= '红包类型',redState= '红包状态(1:激活状态,3:已领状态,4:审核不通过)',
        # #   belongOpenId = '领取人第三方标识ID',channel ='渠道 1 微信，2 qq，3 微博',createTime ,updateTime,belongName = '领取人名称',belongThumb = '领取人头像',
        # cur.execute('select * from t_extension_fallinto order by id desc limit 0,1')
        # data7 = cur.fetchone()
        # if data7[1]<>myuserID:print "Err,Last1 = " + str(data7[1]) + " , not " + str(myuserID) + " ,[7,t_extension_fallinto]" + "\n"
        # else:print "Last1 = "+ str(myuserID) + u",发红包者=" + str(data7[1]) + u",红包所属人" + str(data7[3]) + u",批次ID=" + str(data7[4]) \
        #            + u",渠道ID=" + str(data7[5]) +  u",红包ID=" + str(data7[6])  + u",红包金额" + str(data7[7]) + " [7,t_extension_fallinto]" + "\n"
        #
        # # [8,t_user_thirdInfo 第三方用户信息表]
        # #   id,userId = '用户id',belongName='第三方昵称',belongThumb = '第三方头像',
        # #   channel = '渠道，1 微信，2 qq，3 微博',isValid= '绑定标记，0 未绑定，1 已绑定',openid,token ,createTime
        # for i in range(5):
        #     cur.execute('select * from t_user_thirdInfo order by id desc limit %d,1' % (i)) # 获取最后第二条的userId
        #     data8 = cur.fetchone()
        #     if data8[1]<>myuserID:print "Err,Last"+ str(i+1) +" = " + str(data8[1]) + " , not " + str(myuserID) + " ,[8,t_user_thirdInfo]"
        #     else:print "Last"+ str(i+1) +" = "+ str(myuserID) + " [8,t_user_thirdInfo]"
        # print "\n"
        #
        #
        #
        # # [10,t_user_withdraw 用户管理-提现表]
        # #   id,user_id = '用户id',amount =  '提现金额',
        # #   charge = '手续费',w_state = '0 提现中 1 提现成功 2  提现失败 3 付款中',check_state = '0 提交审核 1 审核成功 2  审核失败 ', bank_num = '银行卡号',
        # #   card_id = '我的默认银行卡id',bank_name = '银行名称',account_name = '银行卡账户名',is_valid = '是否有效',create_time= '创建时间',audit_remark= '审核备注',
        # #   audit_name= '审核人姓名',audit_time ='审核时间',audit = '审核人id',payer_name = '付款人名字',pay_time = '付款时间',payer = '付款人id',pay_remark = '付款失败原因',
        # #   moneyType = '交易类型  26推广审核退回 27体验金推广发红 28大咖推广发红包 29大咖充值  30体验金审核退回  31 新用户体验金充值 32新用户体验金过期 33大咖充值过期',
        # #   pay_type = '交易类型（0.pos 1.微信 2.支付宝）',pay_order_id = 'app支付订单号',pay_id = '第三方支付id',time_end = '支付完成时间',object_id = '业务主键',
        # cur.execute('select * from t_user_withdraw order by id desc limit 0,1')
        # data10 = cur.fetchone()
        # if data10[1]<>myuserID:print "Err,Last1 = " + str(data10[1]) + " , not " + str(myuserID) + " ,[10,t_user_withdraw]" + "\n"
        # else:print "Last1 = "+ str(myuserID) + u",提现金额=" + str(data10[2]) + u",手续费" + str(data10[3]) + u",提现状态=" + str(data10[4])+ u",审核状态" + str(data10[5]) \
        #            +  u",银行卡号" + str(data10[6])  + u",付款人名字" + str(data10[16]) + u",付款时间" + str(data10[17]) +  u",付款人id=" + str(data10[18])  + u",交易类型" + str(data10[20]) \
        #            + u",支付类型" + str(data10[21]) +  u",app支付订单号=" + str(data10[22])  + u",支付完成时间" + str(data10[24]) + u",业务主键" + str(data10[25]) + " [10,t_user_withdraw]" + "\n"




if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TszTable) # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1) # 执行测试
