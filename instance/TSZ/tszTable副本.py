# -*- coding: gb2312 -*-
#****************************************************************
# Author     : John coding: utf-8

# Version    : 1.0.0
# Date       : 2016-6-13
# Description: gameTable.py
# Function   : �������ݿ������еı�,��ѯ����� ĳʱ��� �����еļ�¼ ,�˽ű��ɲ�ѯ ukardweb \game \ ukardapp ���ݿ����еı�
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
# ���ʼ�������� smtplib �� MIMEText
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

# reload(sys)
# sys.setdefaultencoding('utf-8')
# xx=[1,2,u'����']
# xum=""
# for i in xx:
#     print i
#     xum=xum + "," + str(i)
#     print xum
# arrow100=">"
# print arrow100 * 130
# sleep(12121)

# ========== Param ==========
VARMYPHONE="13816101112"


# PyH�ĵ� http://www.tuicool.com/articles/IRvEBr
from pyh import *
page =PyH('tszTable')
page.addCSS('myStylesheet1.css','myStylesheet2.css')
page << h2(u'tszTable', cl='center')
page << h4(u'GenerateTime : ',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'  , ' + VARMYPHONE + ' \'s result as below :')
# xy=u"����ִ�������"
# page << h4(xy.encode("utf-8"))
# decode�������ǽ�����������ַ���ת����unicode���룬��str1.decode('gb2312')����ʾ��gb2312������ַ���str1ת����unicode���롣
# encode�������ǽ�unicode����ת��������������ַ�������str2.encode('gb2312')����ʾ��unicode������ַ���str2ת����gb2312���롣

alist=[]
# ʱ������: ֻ�����������ڵ�����
ISOTIMEFORMAT="%Y-%m-%d"
myTime=time.strftime( ISOTIMEFORMAT, time.localtime() )
# myTime="2016-07-25"
myfrtTime = myTime + " 00:00:01"
myEndTime = myTime + " 23:59:59"
varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #��������ʱ��

VARPERIODTIME =  myfrtTime + " ~ " + myEndTime
VAREXCELFILE = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/excel/tszTable.xls"
VARHTMLFILE = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/report/tszTable.html" # TestReport�ļ�
VARHTMLFILEtimestamp = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/report/tszTable"+varTimeYMDHSM+".html" # TestReport�ļ�
VARERRSCREENSHOT = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/screenshot/"  # �������
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
cur = conn.cursor()
conn.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
cur.execute('show tables') # ��ȡ���ݿ����б���
ukardwebTable=cur.fetchall()
# ��ȡ�û�ID
cur.execute('select id from t_user where username="%s" order by id desc' % (VARMYPHONE))
data0 = cur.fetchone()
myuserID = data0[0]
# ��ȡȺID
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
curapp.execute('show tables') # ��ȡ���ݿ����б���
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
        # ��������
        sender = '<jinhao@mo-win.com.cn>'
        receiver = 'jinhao@mo-win.com.cn'
        f = open(varFile,'rb')
        mail_body = f.read()
        f.close()
        msg=MIMEText(mail_body,_subtype='html',_charset='utf-8')
        # msg = MIMEText('<html><h1>��ã�</h1></html>','html','utf-8')
        # msg = MIMEText('���','text','utf-8')
        # msg['Subject'] = Header(subject,'utf-8')
        msg['Subject'] = u'���غ��gameTAble'
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
        #����Mainִ�к���ģ��
        for i in range(1,sheetMain.nrows):
            if sheetMain.cell_value(i,0) == "Y":
                Maincol1=sheetMain.cell_value(i,1)
                Maincol2=sheetMain.cell_value(i,2)
                self.Maincol1=Maincol1
                self.Maincol2=Maincol2
                exec(sheetMain.cell_value(i,4))

    def TestcaseModule(self):
         #����TestCase�����ú���ģ��
         case1=caseN=0
         for j in range(1,self.sheetTestCase.nrows):
              case1=case1+1
              # ��λ��������λ�ü�����
              if self.sheetTestCase.cell_value(j,1) == self.Maincol1 and self.sheetTestCase.cell_value(j,2) == self.Maincol2:
                  for k in range(case1+1,100): # ������100��Case
                      if k + 1 > self.sheetTestCase.nrows:  # ���һ��
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
         #���� Testcase1~TestCaseN
         for l in range(case1,caseN+case1):
               # ��λ�����ӵ�6�п�ʼ������10��
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
                       # page << p("<font color=blue>[Pass]</font> ",self.sheetTestCase.cell_value(l,3))  #�����������
               except:
                   print u"Excel,Err,��"+str(l+1)+u"��,"+self.sheetTestCase.cell_value(l,3)
                   newWs=self.newbk.get_sheet(1)
                   newWs.write(l,0,"error",self.styleRed)
                   self.newbk.save(self.fname)
                   page << p("<font color=red>[Error]</font> ",self.sheetTestCase.cell_value(l,3))  #�����������
               
         # �Ƿ�����VARHTMLFILE�ĵ�, 1=����һ��testreport.html; 2=���ɶ����ʱ���html,��testreport20161205121210.html
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

    def xx(self,tblName,tblAllFields,keyword,varTblName,tblChiName,*tblChiField):
        # ����: �������(����),�����ֶ�(����)
        varList=[]
        varTmp=""
        if tblName == varTblName:
            reload(sys)
            sys.setdefaultencoding('utf-8')
            tblChiList = list(tblChiField)  # ['ID','����������','����ʱ��','�޸�ʱ��','��Ч�� 1=��Ч 0=��Ч','��˱�� 0=�༭ 1=����� 2=���ͨ�� 3=����˻�','�ֻ���','�빫˾�ֳɱ���']
            for i in range(len(tblChiList)):
                varList.append(str(tblAllFields[i]) +"("+ str(tblChiList[i])+")")
                varTmp =  varTmp + " , " + str(varList[i])
            x=str(tblName) + "(" + str(tblChiName) + ") => " + str(varTmp[2:])
            print x
            # print x.decode("gb2312").encode("utf-8")
            page << p("<font color=blue>"+ str(tblName) + ' </font> => ' + str(varTmp[2:]) + " {�ؼ���: <font color=red>" + str(keyword) + "</font> }")
            del varList[:]
            varTmp=""


    def tableDDL(self,ATtable,allFields,keyword):
        # print list��ӡ�����ݴ洢�ı��뷽ʽ�����������ı��룻
        # print list[1]��ӡ��������ת���ı�������ġ�
        list3=[]
        xum=""
        self.xx(ATtable,allFields,keyword,'t_redgroup_baseinfo',u'���Ⱥ������',u'ID',u'�û�ID',u'Ʒ������',u'Ⱥͷ��',u'Ⱥ����ͼ',u'������',u'����ʱ��',u'�Ƿ��к��',u'���Ⱥ״̬',u'�Ƿ񷢹���� 0=δ���� 1=�ѷ���',u'�Ƿ��޸Ĺ�Ⱥͷ�� 0=û 1=�޸Ĺ�',u'��������',u'�������Ⱥ����',u'�������� 0=���� -1=ȫ��',u'��������ʱ��',u'��������',u'������ 0=���� 1=��',u'�޸�ʱ��',u'�³�Ա����',u'���ٱ�����',u'���鿴��Ϣʱ��')
        #
        # self.xx(ATtable,allFields,keyword,'t_agent_busi','�����̱�','ID','����������','����ʱ��','�޸�ʱ��','��Ч�� 1=��Ч 0=��Ч','��˱�� 0=�༭ 1=����� 2=���ͨ�� 3=����˻�','�ֻ���','�빫˾�ֳɱ���')

        # if ATtable=='t_redgroup_baseinfo':
        #   list2 = ['ID','�û�ID','Ʒ������','Ⱥͷ��','Ⱥ����ͼ','������','����ʱ��','�Ƿ��к��','���Ⱥ״̬','�Ƿ񷢹���� 0=δ���� 1=�ѷ���','�Ƿ��޸Ĺ�Ⱥͷ�� 0=û 1=�޸Ĺ�','��������','�������Ⱥ����','�������� 0=���� -1=ȫ��','��������ʱ��','��������','������ 0=���� 1=��','�޸�ʱ��','�³�Ա����','���ٱ�����','���鿴��Ϣʱ��']
        #   for i in range(len(list2)):
        #      list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
        #      xum =  xum + " , " + list3[i]
        #   x=str(ATtable) + "(���Ⱥ������) => " + str(xum[2:])

        if ATtable=='t_agent_busi':
            list2 = ['ID','����������','����ʱ��','�޸�ʱ��','��Ч�� 1=��Ч 0=��Ч','��˱�� 0=�༭ 1=����� 2=���ͨ�� 3=����˻�','�ֻ���','�빫˾�ֳɱ���']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�����̱�) => " + str(xum[2:])


        if ATtable=='t_agent_store':
            list2 = ['ID','�����̺����̻�����','������ID','����ʱ��','�޸�ʱ��','��Ч�� 1=��Ч 0=��Ч','��˱�� 0=�༭ 1=����� 2=���ͨ�� 3=����˻�','�̻��ֻ���','Ӷ�����','���б��','�û�ID']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
                x=str(ATtable) + "(�����̺����̻���) => " + str(xum[2:])


        if ATtable=='t_experience_detail':
            list2 = ['ID','�û�ID','�������','����ʱ��','��������� 0=�û������ 1=�󿧳�ֵ����� 2=�����һ��������� 3=��������������� 4=����˻� 5=�������ڻ��� 6=�󿧳�ֵ���ڻ���','�ƹ�ID','����ʱ��','��˱�� 0=�༭ 1=����� 2=���ͨ�� 3=����˻�','��Ч�� 1=��Ч 0=��Ч']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�������ϸ��) => " + str(xum[2:])

        if ATtable=='t_extension_channel':
            list2 = ['ID','�û�ID','�����ƹ�����ID','���� 1=��ƽ̨ 2=����� 3=���Ⱥ 4=��ά��','�������������','����δ����������','��������ܽ��','��������������','�ƹ���Դ 1=΢�� 2=֧���� 3=���','����ID','������� 21=�ƹ��� 22=�ƹ���ź�� 26=�ƹ��������','����ʱ��','����ʱ��','���״̬ 1=���� 2=���� 3=����˻�']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�����ƹ�����¼��) => " + str(xum[2:])

        if ATtable=='t_extension_channel_redDetail':
            list2 = ['ID','�����ƹ�����ID','�������','������� 21=�ƹ��� 22=�ƹ���ź�� 26=�ƹ��������','���״̬ 4=ƽ̨���� 5=�������� 6=�ƹ������δͨ��','������','����ʱ��','�޸�ʱ��','�ƹ���Դ 1=΢�� 2=֧���� 3=���','����ID','�����ƹ��� 0=���� 1=��']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�����ƹ�����ϸ��) => " + str(xum[2:])

        if ATtable=='t_extension_channel_redPool':
            list2 = ['ID','�û�ID','���������','������������','δ����������','�����ɺ������','������� 21=�ƹ��� 22=�ƹ���ź�� 26=�ƹ��������','���״̬ 0=δ���� 1=�ѷ��� 2=�ѹ��� 4=�½���¼ 5=δ�ɹ���ֵ','����ܽ��','�ƹ�����','����ʱ��','�޸�ʱ��','����ID','�ƹ���Դ 1=΢�� 2=֧���� 3=���','�����ܷ���','�ƹ�����','���״̬ 0=��ͨ�� 1=δͨ��','�˿���','Ʒ���̻�����','δ��¼�û����������','����򿪴���','ͼƬ���Ӵ򿪴���','������� 0=������ֵ 1=����� 2=��','ʣ����','��������']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�����ƹ�������) => " + str(xum[2:])

        if ATtable=='t_external_redDetail':
            list2 = ['ID','�����ID','�������','�������','���������','�ŵ�ID','�̻�ID','�ŵ���������','���״̬ 1=δ�� 2=ռ�� 3=���� 4=ƽ̨���� 5=�ƹ������δͨ��','������','����ʱ��','�޸�ʱ��','��ȡ�˵���������','��ȡ�˵�����ͷ��','�ƹ���ID','�ƹ�������0=�����ƹ��� 1=�û��ƹ���','�����','ʵ���쵽���','����ID','����ID','�������� 1=��ƽ̨ 3=���Ⱥ 4=��ά��','��ȡ�˵�������ʶID','����״̬ 0=δ���� 1=����']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�ⲿ�������ϸ��) => " + str(xum[2:])




        if ATtable=='t_redgroup_countinfo':
            list2 = ['ID','ȺID','�ܽ��','�ܸ���','����������','�������','����ʱ��','�޸�ʱ��','���ͼƬ(�û����һ���εĵ�һ��ͼ)','�û�ID']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(���Ⱥ���ܱ�) => " + str(xum[2:])


        if ATtable=='t_redgroup_label':
            list2 = ['ID','ȺID','��ǩ����','��ǩ����','����ʱ��']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(Ⱥ�����) => " + str(xum[2:])


        if ATtable=='t_redgroup_memberinfo':
            list2 = ['ID','ȺID','�û�ID','�û���ע','����ID','����ʱ��','ȺԱ״̬ 0=��Ч 1=��Ч','��ȡ���','�Ƿ���δ����','Ⱥ��ԱID','��ȡ�����','���������','��������','�������','�³�Ա��','Ⱥ���鿴 0=�Ѳ鿴 1=δ�鿴','�������� 1=΢�� 2=QQ 3=����΢�� 4=���غ��ƽ̨ 5=��������','�Ƿ���δ��ͼ����Ϣ','Ⱥ���Ʊ�ע','��������Ա 0=���� 1=��']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(Ⱥ��Ա��) => " + str(xum[2:])


        if ATtable=='t_redgroup_message':
            list2 = ['ID','ȺID','Ⱥ��Ϣ','���� 0=������Ϣ 1=���ը����Ϣ 2=������Ϣ 3=���������Ϣ 4=��������Ϣ 5=���������Ϣ 6=��һ�μ�����Ϣ 7=ͼƬ��Ϣ','����ID','��Ϣ״̬ 0=���� 1=ɾ�� 2=���� 3=�ٱ�','����ʱ��','����ID','��ϢȨ��(������ŷָ�)']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(Ⱥ��Ϣ��) => " + str(xum[2:])


        if ATtable=='t_user':
            list2 = ['�û�ID','�û���','�Ա� 0=Ů 1=�� -1δ��','����','��ס����','�ǳ�','����','ͷ���ַ','ͷ������','ע��ʱ��','����ʱ��','���һ�ε�¼ʱ��','ע������ 1=appstore 2=���� 3=360�г� 4=91�г� 5=��׿�г� 6=�ٶ��г� 7=�㶹�� 8=�����г� 9=�����г� 10=Ӧ�û� 11=С�� 12=���� 13=ľ���� 14=Ӧ�ñ�','״̬ 0=��ע�� 1=�Ѽ��� 2=�Ѷ��� 3=Ԥע�� 4=Ԥ��¼','���һ�ε�¼����','�Ƿ���Ч 0=��Ч 1=��Ч Ĭ��1','��ע','�����ֶ�1','�����ֶ�2','�����ֶ�3','ע��ʡ��','ʦ������ 0=ƽ̨ 1=�ŵ� 2=����','ʦ����� 0=ƽ̨','ʦ������','�����ܶ�','�������','Ӷ���ܶ�','Ӷ�����','ͽ������','�ϴ�����ʱ��','Ӷ�����ֽ��','�����û� 1=���� Ĭ��0','������','����ǩ��','��������','����ķ��ֽ��','�ƹ����ۼ��˿���','���δͨ������','�������û� 0=���� 1=��','�����','��ֵ���','���غ�','���ؿ����']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�û���) => " + str(xum[2:])


        if ATtable=='t_user_friends':
            list2 = ['ID','�û�ID','����ID','����״̬ 1=�ȴ���֤ 2=ͬ�� 3=�ܾ� 4=����ɾ��','����ʱ��','�޸�ʱ��','�Ƿ���Ч 1=��Ч 0=��Ч','������Դ 1=������ 0=������','��ע����']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(��Ա��ϵ��) => " + str(xum[2:])


        if ATtable=='t_user_red_footprint':
            list2 = ['ID','�������','���������','���ID','�������','�����ID','�ƹ�������','����ʱ��','�ŵ�ID','�ŵ�����','�ŵ����ID','����','������','����ID']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�����㼣��) => " + str(xum[2:])



        if ATtable=='t_user_thirdInfo':
            list2 = ['ID','�û�ID','�������ǳ�','������ͷ��','���� 1=΢�� 2=QQ3=΢��','�󶨱�� 0=δ�� 1=�Ѱ�','openid','token','����ʱ��','�ϲ�ǰ�û�ID']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�������û���Ϣ��) => " + str(xum[2:])


        if ATtable=='t_user_withdraw':
            list2 = ['ID','�û�ID','���ֽ��','������','0=������ 1=���ֳɹ� 2=����ʧ�� 3=������','0=�ύ��� 1=��˳ɹ� 2=���ʧ��','���п���','Ĭ�����п�ID','��������','�����˻���','�Ƿ���Ч','����ʱ��','��˱�ע','���������','���ʱ��','�����ID','����������','����ʱ��','������ID','����ʧ��ԭ��','�������� 9=���� 11=������� 18=΢���ƹ��ֵ 23=΢���ƹ㷢��� 24=��ֵ���� 25=����ƹ㷢��� ...','�������� 0=pos 1=΢�� 2=֧����','app֧��������','������֧��ID','֧�����ʱ��','ҵ������']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(���ֱ�) => " + str(xum[2:])


        if ATtable=='ta_message':
            list2 = ['ID','��Ϣ����','0=�ȴ�ִ�� 1=ִ�гɹ� 2=ִ��ʧ�� ����json����','��Ϣ����','����ʱ��','��Դ','�汾','ҵ����','��ִ���','��Դ���','��Ϣ��ʶ','�ֻ���','��֤��']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�����Ϣ�����) => " + str(xum[2:])


        if ATtable=='t_extension_redDetail':
            list2 = ['ID','�ƹ�����ID','�������','������','��ȡ�˵���������','��ȡ�˵�����ͷ��','������� 21=�ƹ��� 22=�ƹ���ź�� 26=�ƹ��������','���״̬ 0=δ�� 1=δ���� 2=ռ�� 3=����δ���� 4=ƽ̨���� 5=�����ѷ��� 6=�ƹ������δͨ��','������','����ʱ��','�޸�ʱ��','���׷���','���������','�ƹ���Դ 1=΢�� 2=���','����ID','������ID','�����','�����ƹ��� 0=���� 1=��']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�ƹ�����ϸ��) => " + str(xum[2:])

        if ATtable=='t_sys_message':
            list2 = ['ID','��Ϣ����','����ʱ��','�޸�ʱ��','��Ч�ԣ�1 ��Ч��0 ��Ч','��˱�ǣ�0 �༭��1 ����У�2���ͨ����3 ����˻�','��Ϣ����','��Ϣ�ⲿ����','ϵͳ��ǣ�0 ȫ����1 ��׿��2 ios','�绰�б�','�û�id�б�']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(ϵͳ��Ϣ��) => " + str(xum[2:])

        # ukardapp
        if ATtable=='t_share':
            list2 = ['����ID','�û�ID','����ID','�������� 15=������ͽ�ܺ�� 16=��������ͽ�� 20=����app��ͽ�� 21=һ�������ƹ��� 22=���������ƹ��� 23=���ź���������� 24=�������ź���������� 25=�µ���������','�����Ż�ȯ���ŵ������','1=����΢�� 2=��Ѷ΢�� 3=΢�ź��� 4=΢������Ȧ 5=���� 6=qq���� 7=qq�ռ�','�û�����','�û��ϴ�ͼƬ','����ʱ��','��������ID','����ID','0=app 1=H5','�����˵�������ʶID','����ID','����ID']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�����) => " + str(xum[2:])


        if ATtable=='t_share_relation':
            list2 = ['ID','����ID','��ǰ�������û�ID','�����˵�����ID','����ID','ƽ̨����','����ʱ��']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(�����ϵ��) => " + str(xum[2:])

        # print x.decode("gb2312").encode("utf-8")
        # page << p("<font color=blue>"+ str(ATtable) + ' </font> => ' + str(xum[2:]) + " {�ؼ���: <font color=red>" + str(keyword) + "</font> }")
        # del list3[:]
        # xum=""

    def output2(self,varFieldName,col_name_list,varCur,ATtable,varX):

         varFieldtime=""
         varTableCount=0

         if varFieldName in col_name_list:
             # �����б�λ�ֶ� ��: ��ȡ���� ��time���ֶ� ,���Դ�Сд
             for m in range(len(col_name_list)):
                 m1=re.search("Time",col_name_list[m],re.IGNORECASE)
                 if m1:
                     # �����Ч���ڵļ�¼
                     varCur.execute('select %s from %s where %s BETWEEN "%s" And "%s" and %s=%s order by %s desc' % (col_name_list[m],ATtable,col_name_list[m],myfrtTime,myEndTime,varFieldName,varX,col_name_list[m]))
                     numrows = int(varCur.rowcount)
                     for i in range(numrows):
                         row = varCur.fetchone()
                         varFieldtime="("+str(row[0])+") "+varFieldtime
                     if varFieldtime<>"":
                         alist.append(varFieldName)
                         alist.append(col_name_list[m])
                         alist.append(numrows)
                         alist.append(varFieldtime)
                     if numrows>=1:  # ��������������ֶμ���¼
                         # print ATtable + " => " + str(alist)
                         # print str(col_name_list)  # �����ֶ���
                         self.tableDDL(ATtable,col_name_list,alist[0]) # ��� ���� �� ��ṹ + DLL
                         # page << p("<font color=blue>" + str(ATtable) + "</font> => " + "<font color=red>" + str(alist[0]) + "</font>")  # + " <font color=purple>" + str(col_name_list) + "</font>"
                         # page << p("&nbsp;&nbsp;&nbsp;&nbsp;<font color=purple>" + str(col_name_list) + "</font>")
                         varCur.execute('select * from %s where %s BETWEEN "%s" And "%s" and %s="%s" order by %s desc' % (ATtable,col_name_list[m],myfrtTime,myEndTime,varFieldName,varX,col_name_list[m]))
                         t2=varCur.fetchall()
                         reload(sys)
                         sys.setdefaultencoding('utf-8')
                         sum=""
                         for j in range(numrows):
                             l=0
                             for k in t2[j]:
                                 sum =  sum + ", (" + str(col_name_list[l]) +")" + str(k)
                                 l=l+1
                             print str(j+1) +") "+ str(sum[2:])
                             page << p("<font color=green>" + str(j+1) +") "+ str(sum[2:]).decode("utf-8").encode("gb2312") + "</font>")  #.decode("gb2312").encode("utf-8")  #decode('unicode_escape')
                             sum=""
                         del alist[:]
                         varFieldtime=""
                         varTableCount=1
                     break # ֻ��ȡ��ǰ���һ����Time�ֶε�ֵ,���Ժ����Time���ֶ�,��ֻ��ȡ createTime , ����updateTime
         return varTableCount

    def t_userLogin(self,TabelName,varCur,varTable):
        print "=====[" + str(TabelName) + "," + str(VARPERIODTIME) + " , userID = " + str(myuserID) + " , groupID =" + str(mygroupID) + "]=====\n"
        page << p("<font color=purple>=====[" + str(TabelName) + " , " + str(VARPERIODTIME) + " , userID = " + str(myuserID) + " , groupID =" + str(mygroupID) + "]=====</font> ")

        varFieldtime=""  # ��Ÿ����ʱ��
        varTableCount=0
        x=0 # ͳ����������ŷ���Ҫ��ı�

        for AT in varTable: # �������еı�
            # ��ȡÿ�����������ֶ� ,����col_name_list
            if AT[0] == "beijing_store":  # ��������ͼ
                pass
            else:
                varCur.execute("select count(*) from %s" % AT[0])
                t0 = varCur.fetchone()
                if t0[0]<>0: # �����ձ�
                    varCur.execute("select * from %s" % AT[0])
                    col_name_list = [tuple[0] for tuple in varCur.description]  # ��ȡ���������ֶ�
                    # ���������Ƿ���������ֶεı�,����¼���ݱ��浽����,�����.

                    tmp1=self.output2('userId',col_name_list,varCur,AT[0],myuserID)
                    tmp2=self.output2('user_id',col_name_list,varCur,AT[0],myuserID)
                    tmp3=self.output2('id',col_name_list,varCur,AT[0],myuserID)
                    tmp4=self.output2('id1',col_name_list,varCur,AT[0],myuserID)
                    tmp5=self.output2('id2',col_name_list,varCur,AT[0],myuserID)
                    tmp6=self.output2('belongId',col_name_list,varCur,AT[0],myuserID)
                    tmp7=self.output2('accept_id',col_name_list,varCur,AT[0],myuserID)
                    tmp8=self.output2('friendid',col_name_list,varCur,AT[0],myuserID)
                    tmp9=self.output2('th_id',col_name_list,varCur,AT[0],myuserID)
                    tmp10=self.output2('sd_id',col_name_list,varCur,AT[0],myuserID)
                    tmp11=self.output2('groupUserId',col_name_list,varCur,AT[0],myuserID)
                    tmp12=self.output2('submit_user_id',col_name_list,varCur,AT[0],myuserID)
                    tmp13=self.output2('shareUserId',col_name_list,varCur,AT[0],myuserID)
                    tmp14=self.output2('userId1',col_name_list,varCur,AT[0],myuserID)
                    tmp15=self.output2('userId2',col_name_list,varCur,AT[0],VARMYPHONE)
                    tmp16=self.output2('phone',col_name_list,varCur,AT[0],VARMYPHONE)
                    tmp17=self.output2('username',col_name_list,varCur,AT[0],VARMYPHONE)
                    tmp18=self.output2('contacts',col_name_list,varCur,AT[0],VARMYPHONE)
                    tmp19=self.output2('groupId',col_name_list,varCur,AT[0],mygroupID)
                    tmp20=self.output2('oldUserId',col_name_list,varCur,AT[0],myuserID)
                    tmp21=self.output2('userIdArray',col_name_list,varCur,AT[0],myuserID)
                    tmp22=self.output2('userArray',col_name_list,varCur,AT[0],VARMYPHONE)
                    tmpall= tmp1+tmp2+tmp3+tmp4+tmp5+tmp6+tmp7+tmp8+tmp9+tmp10+tmp11+tmp12+tmp13+tmp14+tmp15+tmp16+tmp17+tmp18+tmp19+tmp20+tmp21+tmp22
                    if tmpall >= 1:
                        varTableCount=varTableCount+1
                        arrowSymbol=">"
                        print arrowSymbol * 130
                        page << p(arrowSymbol * 130)

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
        self.t_userLogin("ukardapp",curapp,ukardappTable)
        self.t_userLogin("game",curGame,gameTable)



    def drv_game(self):
        # game
        self.TestcaseModule()
    def t_game(self):
        self.t_userLogin(self.curGame,self.gameTable)


if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TSZgameTable) # ������Լ�
    unittest.TextTestRunner(verbosity=2).run(suite1) # ִ�в���

 # ʧ��,��ʽ��Ԫ���е�����,�� (619L, 2257L, 10001871L, u'', None, 1, datetime.datetime(2016, 7, 5, 13, 47, 58))
                                                         # c_list=[]
                                                         # xx=t2[j]
                                                         # for k in range(len(xx)):
                                                         #     print xx[k]
                                                         #     # print type(xx[k])
                                                         #     if isinstance(xx[k], long):
                                                         #         print "ok"
                                                         #         c_list.append(xx)
                                                         #     elif isinstance(xx[k], int):
                                                         #         print "err"
                                                         #     elif isinstance(xx[k], unicode):
                                                         #         print "hahah"
                                                         #     elif isinstance(xx[k], datetime.datetime):
                                                         #         print "xixix"
                                                         #     c_list.append(xx[k])
                                                         # print c_list