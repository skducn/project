# -*- coding: gb2312 -*-
#****************************************************************
# Author     : John coding: utf-8

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

# ========== Param ==========
VARMYPHONE="13816101112"


# PyH文档 http://www.tuicool.com/articles/IRvEBr
from pyh import *
page =PyH('tszTable')
page.addCSS('myStylesheet1.css','myStylesheet2.css')
page << h2(u'tszTable', cl='center')
page << h4(u'GenerateTime : ',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'  , ' + VARMYPHONE + ' \'s result as below :')
# xy=u"用例执行情况："
# page << h4(xy.encode("utf-8"))
# decode的作用是将其他编码的字符串转换成unicode编码，如str1.decode('gb2312')，表示将gb2312编码的字符串str1转换成unicode编码。
# encode的作用是将unicode编码转换成其他编码的字符串，如str2.encode('gb2312')，表示将unicode编码的字符串str2转换成gb2312编码。

alist=[]
# 时间区域: 只操作当天日期的数据
ISOTIMEFORMAT="%Y-%m-%d"
myTime=time.strftime( ISOTIMEFORMAT, time.localtime() )
# myTime="2016-07-25"
myfrtTime = myTime + " 00:00:01"
myEndTime = myTime + " 23:59:59"
varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #当天日期时间

VARPERIODTIME =  myfrtTime + " ~ " + myEndTime
VAREXCELFILE = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/excel/tszTable.xls"
VARHTMLFILE = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/report/tszTable.html" # TestReport文件
VARHTMLFILEtimestamp = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/report/tszTable"+varTimeYMDHSM+".html" # TestReport文件
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

    def xx(self,tblName,tblAllFields,keyword,varTblName,tblChiName,*tblChiField):
        # 功能: 输出表名(中文),所有字段(中文)
        varList=[]
        varTmp=""
        if tblName == varTblName:
            reload(sys)
            sys.setdefaultencoding('utf-8')
            tblChiList = list(tblChiField)  # ['ID','代理商名称','创建时间','修改时间','有效性 1=有效 0=无效','审核标记 0=编辑 1=审核中 2=审核通过 3=审核退回','手机号','与公司分成比例']
            for i in range(len(tblChiList)):
                varList.append(str(tblAllFields[i]) +"("+ str(tblChiList[i])+")")
                varTmp =  varTmp + " , " + str(varList[i])
            x=str(tblName) + "(" + str(tblChiName) + ") => " + str(varTmp[2:])
            print x
            # print x.decode("gb2312").encode("utf-8")
            page << p("<font color=blue>"+ str(tblName) + ' </font> => ' + str(varTmp[2:]) + " {关键字: <font color=red>" + str(keyword) + "</font> }")
            del varList[:]
            varTmp=""


    def tableDDL(self,ATtable,allFields,keyword):
        # print list打印出数据存储的编码方式，中文是中文编码；
        # print list[1]打印出的是译转中文编码的中文。
        list3=[]
        xum=""
        self.xx(ATtable,allFields,keyword,'t_redgroup_baseinfo',u'红包群基本表',u'ID',u'用户ID',u'品牌名称',u'群头像',u'群背景图',u'总人数',u'创建时间',u'是否有红包',u'红包群状态',u'是否发过红包 0=未发过 1=已发过',u'是否修改过群头像 0=没 1=修改过',u'领红包人数',u'发到红包群个数',u'所属分类 0=其他 -1=全部',u'最近发红包时间',u'店铺链接',u'黑名单 0=不是 1=是',u'修改时间',u'新成员数量',u'被举报次数',u'最后查看消息时间')
        #
        # self.xx(ATtable,allFields,keyword,'t_agent_busi','代理商表','ID','代理商名称','创建时间','修改时间','有效性 1=有效 0=无效','审核标记 0=编辑 1=审核中 2=审核通过 3=审核退回','手机号','与公司分成比例')

        # if ATtable=='t_redgroup_baseinfo':
        #   list2 = ['ID','用户ID','品牌名称','群头像','群背景图','总人数','创建时间','是否有红包','红包群状态','是否发过红包 0=未发过 1=已发过','是否修改过群头像 0=没 1=修改过','领红包人数','发到红包群个数','所属分类 0=其他 -1=全部','最近发红包时间','店铺链接','黑名单 0=不是 1=是','修改时间','新成员数量','被举报次数','最后查看消息时间']
        #   for i in range(len(list2)):
        #      list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
        #      xum =  xum + " , " + list3[i]
        #   x=str(ATtable) + "(红包群基本表) => " + str(xum[2:])

        if ATtable=='t_agent_busi':
            list2 = ['ID','代理商名称','创建时间','修改时间','有效性 1=有效 0=无效','审核标记 0=编辑 1=审核中 2=审核通过 3=审核退回','手机号','与公司分成比例']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(代理商表) => " + str(xum[2:])


        if ATtable=='t_agent_store':
            list2 = ['ID','代理商合作商户名称','代理商ID','创建时间','修改时间','有效性 1=有效 0=无效','审核标记 0=编辑 1=审核中 2=审核通过 3=审核退回','商户手机号','佣金比例','城市编号','用户ID']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
                x=str(ATtable) + "(代理商合作商户表) => " + str(xum[2:])


        if ATtable=='t_experience_detail':
            list2 = ['ID','用户ID','体验金金额','创建时间','体验金类型 0=用户体验金 1=大咖充值体验金 2=体验金一级红包回收 3=体验金二级红包回收 4=审核退回 5=体验金过期回收 6=大咖充值过期回收','推广ID','过期时间','审核标记 0=编辑 1=审核中 2=审核通过 3=审核退回','有效性 1=有效 0=无效']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(体验金明细表) => " + str(xum[2:])

        if ATtable=='t_extension_channel':
            list2 = ['ID','用户ID','渠道推广红包池ID','渠道 1=外平台 2=抢红包 3=红包群 4=二维码','渠道红包总数量','渠道未领红包总数量','渠道红包总金额','渠道红包单个金额','推广来源 1=微信 2=支付宝 3=余额','城市ID','红包类型 21=推广红包 22=推广短信红包 26=推广体验金红包','创建时间','更新时间','红包状态 1=正常 2=回收 3=审核退回']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(渠道推广红包记录表) => " + str(xum[2:])

        if ATtable=='t_extension_channel_redDetail':
            list2 = ['ID','渠道推广红包池ID','发红包人','红包类型 21=推广红包 22=推广短信红包 26=推广体验金红包','红包状态 4=平台回收 5=正常生成 6=推广红包审核未通过','红包金额','创建时间','修改时间','推广来源 1=微信 2=支付宝 3=余额','城市ID','回收推广红包 0=不是 1=是']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(渠道推广红包明细表) => " + str(xum[2:])

        if ATtable=='t_extension_channel_redPool':
            list2 = ['ID','用户ID','红包总数量','已领红包总数量','未领红包总数量','已生成红包个数','红包类型 21=推广红包 22=推广短信红包 26=推广体验金红包','红包状态 0=未分享 1=已分享 2=已过期 4=新建记录 5=未成功充值','红包总金额','推广内容','创建时间','修改时间','城市ID','推广来源 1=微信 2=支付宝 3=余额','交易总费率','推广连接','审核状态 0=已通过 1=未通过','退款金额','品牌商户名称','未登录用户点击下载数','红包打开次数','图片链接打开次数','金额类型 0=正常充值 1=体验金 2=大咖','剩余金额','分享渠道']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(渠道推广红包主表) => " + str(xum[2:])

        if ATtable=='t_external_redDetail':
            list2 = ['ID','红包池ID','发红包人','红包类型','红包所属人','门店ID','商户ID','门店所属城市','红包状态 1=未领 2=占用 3=已领 4=平台回收 5=推广红包审核未通过','红包金额','创建时间','修改时间','领取人第三方名称','领取人第三方头像','推广红包ID','推广红包类型0=消费推广红包 1=用户推广红包','体验金','实际领到金额','渠道ID','批次ID','渠道类型 1=外平台 3=红包群 4=二维码','领取人第三方标识ID','领完状态 0=未领完 1=领完']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(外部红包池明细表) => " + str(xum[2:])




        if ATtable=='t_redgroup_countinfo':
            list2 = ['ID','群ID','总金额','总个数','发出批次数','浏览次数','创建时间','修改时间','广告图片(用户最近一批次的第一张图)','用户ID']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(红包群汇总表) => " + str(xum[2:])


        if ATtable=='t_redgroup_label':
            list2 = ['ID','群ID','标签名称','标签人数','创建时间']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(群分组表) => " + str(xum[2:])


        if ATtable=='t_redgroup_memberinfo':
            list2 = ['ID','群ID','用户ID','用户备注','批次ID','创建时间','群员状态 0=有效 1=无效','领取金额','是否有未领红包','群成员ID','领取红包数','静如店铺数','浏览广告数','分享次数','新成员数','群主查看 0=已查看 1=未查看','渠道类型 1=微信 2=QQ 3=新浪微博 4=三藏红包平台 5=主动加入','是否有未读图文消息','群名称备注','黑名单成员 0=不是 1=是']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(群成员表) => " + str(xum[2:])


        if ATtable=='t_redgroup_message':
            list2 = ['ID','群ID','群消息','类型 0=文字消息 1=红包炸弹消息 2=分享消息 3=抢到红包消息 4=分享奖励消息 5=红包抢完消息 6=第一次加入消息 7=图片消息','渠道ID','消息状态 0=正常 1=删除 2=撤回 3=举报','创建时间','批次ID','消息权限(多个逗号分隔)']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(群消息表) => " + str(xum[2:])


        if ATtable=='t_user':
            list2 = ['用户ID','用户名','性别 0=女 1=男 -1未定','密码','常住城市','昵称','城市','头像地址','头像像素','注册时间','邀请时间','最近一次登录时间','注册类型 1=appstore 2=官网 3=360市场 4=91市场 5=安卓市场 6=百度市场 7=豌豆荚 8=机锋市场 9=安智市场 10=应用汇 11=小米 12=优亿 13=木蚂蚁 14=应用宝','状态 0=已注销 1=已激活 2=已冻结 3=预注册 4=预登录','最近一次登录城市','是否有效 0=无效 1=有效 默认1','备注','备用字段1','备用字段2','备用字段3','注册省份','师傅类型 0=平台 1=门店 2=个人','师傅编号 0=平台','师傅名称','积分总额','积分余额','佣金总额','佣金余额','徒弟总数','上次提现时间','佣金提现金额','匿名用户 1=匿名 默认0','冻结金额','个性签名','出生日期','错过的返现金额','推广红包累计退款金额','审核未通过次数','黑名单用户 0=不是 1=是','体验金','充值金额','三藏号','三藏卡金额']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(用户表) => " + str(xum[2:])


        if ATtable=='t_user_friends':
            list2 = ['ID','用户ID','朋友ID','邀请状态 1=等待验证 2=同意 3=拒绝 4=单向删除','创建时间','修改时间','是否有效 1=有效 0=无效','邀请来源 1=请求发起 0=被邀请','备注名称']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(会员关系表) => " + str(xum[2:])


        if ATtable=='t_user_red_footprint':
            list2 = ['ID','发红包者','红包所属人','红包ID','红包类型','红包池ID','推广红包类型','创建时间','门店ID','门店名称','门店城市ID','描述','红包金额','批次ID']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(领红包足迹表) => " + str(xum[2:])



        if ATtable=='t_user_thirdInfo':
            list2 = ['ID','用户ID','第三方昵称','第三方头像','渠道 1=微信 2=QQ3=微博','绑定标记 0=未绑定 1=已绑定','openid','token','创建时间','合并前用户ID']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(第三方用户信息表) => " + str(xum[2:])


        if ATtable=='t_user_withdraw':
            list2 = ['ID','用户ID','提现金额','手续费','0=提现中 1=提现成功 2=提现失败 3=付款中','0=提交审核 1=审核成功 2=审核失败','银行卡号','默认银行卡ID','银行名称','银行账户名','是否有效','创建时间','审核备注','审核人姓名','审核时间','审核人ID','付款人名字','付款时间','付款人ID','付款失败原因','交易类型 9=提现 11=抢到红包 18=微信推广充值 23=微信推广发红包 24=充值费率 25=余额推广发红包 ...','交易类型 0=pos 1=微信 2=支付宝','app支付订单号','第三方支付ID','支付完成时间','业务主键']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(提现表) => " + str(xum[2:])


        if ATtable=='ta_message':
            list2 = ['ID','消息类型','0=等待执行 1=执行成功 2=执行失败 其他json错误','消息内容','操作时间','来源','版本','业务编号','回执结果','来源编号','信息标识','手机号','验证码']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(审核消息任务表) => " + str(xum[2:])


        if ATtable=='t_extension_redDetail':
            list2 = ['ID','推广红包池ID','发红包人','领红包人','领取人第三方名称','领取人第三方头像','红包类型 21=推广红包 22=推广短信红包 26=推广体验金红包','红包状态 0=未领 1=未分享 2=占用 3=已领未分享 4=平台回收 5=已领已分享 6=推广红包审核未通过','红包金额','创建时间','修改时间','交易费率','红包总数量','推广来源 1=微信 2=余额','城市ID','分享人ID','体验金','回收推广红包 0=不是 1=是']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(推广红包明细表) => " + str(xum[2:])

        if ATtable=='t_sys_message':
            list2 = ['ID','消息内容','创建时间','修改时间','有效性，1 有效，0 无效','审核标记，0 编辑，1 审核中，2审核通过，3 审核退回','消息标题','消息外部链接','系统标记，0 全部，1 安卓，2 ios','电话列表','用户id列表']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(系统消息表) => " + str(xum[2:])

        # ukardapp
        if ATtable=='t_share':
            list2 = ['分享ID','用户ID','批次ID','分享类型 15=分享收徒弟红包 16=分享红包招徒弟 20=分享app收徒弟 21=一级分享推广红包 22=二级分享推广红包 23=短信红包分享链接 24=体验金短信红包分享链接 25=新的渠道分享','分享优惠券或门店的名称','1=新浪微博 2=腾讯微博 3=微信好友 4=微信朋友圈 5=短信 6=qq好友 7=qq空间','用户评论','用户上传图片','分享时间','分享任务ID','城市ID','0=app 1=H5','分享人第三方标识ID','内容ID','渠道ID']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(分享表) => " + str(xum[2:])


        if ATtable=='t_share_relation':
            list2 = ['ID','批次ID','当前分享人用户ID','分享人第三方ID','父级ID','平台类型','创建时间']
            for i in range(len(list2)):
                list3.append(str(allFields[i]) +"("+ str(list2[i])+")")
                xum =  xum + " , " + list3[i]
            x=str(ATtable) + "(分享关系表) => " + str(xum[2:])

        # print x.decode("gb2312").encode("utf-8")
        # page << p("<font color=blue>"+ str(ATtable) + ' </font> => ' + str(xum[2:]) + " {关键字: <font color=red>" + str(keyword) + "</font> }")
        # del list3[:]
        # xum=""

    def output2(self,varFieldName,col_name_list,varCur,ATtable,varX):

         varFieldtime=""
         varTableCount=0

         if varFieldName in col_name_list:
             # 遍历列表定位字段 如: 获取所有 带time的字段 ,忽略大小写
             for m in range(len(col_name_list)):
                 m1=re.search("Time",col_name_list[m],re.IGNORECASE)
                 if m1:
                     # 输出有效期内的记录
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
                     if numrows>=1:  # 输出符合条件的字段及记录
                         # print ATtable + " => " + str(alist)
                         # print str(col_name_list)  # 所有字段名
                         self.tableDDL(ATtable,col_name_list,alist[0]) # 输出 表名 与 表结构 + DLL
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
                     break # 只获取当前表第一个带Time字段的值,忽略后面带Time的字段,如只获取 createTime , 忽略updateTime
         return varTableCount

    def t_userLogin(self,TabelName,varCur,varTable):
        print "=====[" + str(TabelName) + "," + str(VARPERIODTIME) + " , userID = " + str(myuserID) + " , groupID =" + str(mygroupID) + "]=====\n"
        page << p("<font color=purple>=====[" + str(TabelName) + " , " + str(VARPERIODTIME) + " , userID = " + str(myuserID) + " , groupID =" + str(mygroupID) + "]=====</font> ")

        varFieldtime=""  # 存放各表的时间
        varTableCount=0
        x=0 # 统计输出多少张符合要求的表

        for AT in varTable: # 遍历所有的表
            # 获取每个表中所有字段 ,存入col_name_list
            if AT[0] == "beijing_store":  # 跳过此视图
                pass
            else:
                varCur.execute("select count(*) from %s" % AT[0])
                t0 = varCur.fetchone()
                if t0[0]<>0: # 跳过空表
                    varCur.execute("select * from %s" % AT[0])
                    col_name_list = [tuple[0] for tuple in varCur.description]  # 获取表中所有字段
                    # 遍历表中是否包含以下字段的表,将记录内容保存到数组,并输出.

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
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TSZgameTable) # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1) # 执行测试

 # 失败,格式化元组中的数据,如 (619L, 2257L, 10001871L, u'', None, 1, datetime.datetime(2016, 7, 5, 13, 47, 58))
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