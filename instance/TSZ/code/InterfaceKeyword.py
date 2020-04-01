# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: 接口驱动
#****************************************************************

import os,sys,unittest,requests,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis
reload(sys)
sys.setdefaultencoding('utf8')
from appium import webdriver
# from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import smtplib,pytesseract
from PIL import Image
from email.mime.text import MIMEText
from email.header import Header
from time import sleep
from xlwt.Style import *
from xlrd import open_workbook
from xlutils.copy import copy
from PIL import Image
from pyh import *
#from jhj_v1_5_setup import *
#win32api,win32con,HTMLTestRunner
# import HTMLTestRunner
import time,Image,ImageChops


# sleep(1212)
# a="121"
# xx="{""verifyUserId"":""10002084","redId":"' + a +'"}'
# print type(xx)
# sleep(112)

# x="100==500"
# print x.split("==",1)[0]
# print x.split("==",1)[1]
# sleep(1212)

# print sys.path
# from resource.source.comparePic import *
# from resource.source import test2
#****************************************************************
 # http://blog.csdn.net/wzwsj1986/article/details/1723658
        # character_set_client为客户端编码方式；
        # character_set_connection为建立连接使用的编码；
        # character_set_database数据库的编码；
        # character_set_results结果集的编码；
        # character_set_server数据库服务器的编码；
# 参数化
varPhone="13816109050"
ExcelFile = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/excel/tsz_v2_5test.xls"
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
bk = xlrd.open_workbook(ExcelFile,formatting_info=True)
newbk=copy(bk)
sheetConfigure= bk.sheet_by_name("configure")
sheetTestCase=bk.sheet_by_name("testcase")
styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')
styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')

def sendemail(varTitle,varContent):
    # 邮箱配置
    sender = '<jinhao@mo-win.com.cn>'
    receiver = 'jinhao@mo-win.com.cn'
    msg = MIMEText(varContent,'text','utf-8')
    msg['Subject'] = varTitle
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.exmail.qq.com')
        smtp.login('jinhao@mo-win.com.cn','Jinhao123')
        smtp.sendmail(sender,receiver,msg.as_string())
        smtp.quit()
    except Exception, e:
        print str(e)

def assertEqual(expected,actual,okmessage,errmessage):
    if expected == actual : print okmessage
    else: print errmessage


class InterfaceKeywork(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.connWeb= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306,charset="utf8",use_unicode=True)
        self.curWeb = self.connWeb.cursor()
        self.curWeb.execute('SET NAMES UTF8;')
        self.WebTables=self.curWeb.fetchall()
        self.connApp= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardapp', port=3306, charset="utf8",use_unicode=True)
        self.curApp = self.connApp.cursor()
        self.curApp.execute('SET NAMES UTF8;')
        self.AppTables=self.curApp.fetchall()
        self.connGame= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='game', port=3306,charset="utf8", use_unicode=True)
        self.curGame = self.connGame.cursor()
        self.curGame.execute('SET NAMES UTF8;')
        self.GameTables=self.curGame.fetchall()
        self.r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        self.r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")

    @classmethod
    def tearDownClass(self):
        pass

    def test_Main(self):
        for i in range(1,sheetConfigure.nrows):         #遍历 configure 执行函数模块
            if sheetConfigure.cell_value(i,0) == "Y":
                self.ConfigureCaseArea = sheetConfigure.cell_value(i,1)
                self.ConfigureConsoleOuput = sheetConfigure.cell_value(i,2)
                exec(sheetConfigure.cell_value(i,4))

    def TestcaseModule(self):
        case1=caseN=0
        for j in range(1,sheetTestCase.nrows):
            case1=case1+1
            if sheetTestCase.cell_value(j,1) == self.ConfigureCaseArea :
                for k in range(case1+1,100):
                    if k + 1 > sheetTestCase.nrows:
                        caseN=caseN+1
                        break
                    elif sheetTestCase.cell_value(k,1)=="":
                        caseN=caseN+1
                    elif sheetTestCase.cell_value(k,2)=="skip" :
                        caseN=caseN+1
                    else:
                        caseN=caseN+1
                        break
                break
        for l in range(case1,caseN+case1):
            try :
                if sheetTestCase.cell_value(l,2)=="skip":
                    newWs=newbk.get_sheet(1)
                    newWs.write(l,0,"skip",styleGray25)
                    newbk.save(ExcelFile)
                else:
                    self.CaseInfo = sheetTestCase.cell_value(l,3)
                    print "\n" + self.CaseInfo.split(";",1)[0] + "(" + str(sheetTestCase.cell_value(l,4).count("self")) + ") "
                    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                    # # 优先级1
                    # if sheetTestCase.cell_value(l,6).count("RtnOK")==1:
                    #     # print sheetTestCase.cell_value(l,6)
                    #     exec(sheetTestCase.cell_value(l,6))
                    # elif sheetTestCase.cell_value(l,6).count("RtnOK")>1:
                    #     y=0
                    #     for y in range(sheetTestCase.cell_value(l,6).count("RtnOK")):
                    #         exec(sheetTestCase.cell_value(l,6).split(";",sheetTestCase.cell_value(l,6).count('RtnOK'))[y])
                    #         # print sheetTestCase.cell_value(l,6).split(";",sheetTestCase.cell_value(l,6).count('RtnOK'))[y]
                    # 优先级1
                    if sheetTestCase.cell_value(l,6).count(";")==1:
                        # print sheetTestCase.cell_value(l,6)
                        exec(sheetTestCase.cell_value(l,6))
                    elif sheetTestCase.cell_value(l,6).count(";")>1:
                        y=0
                        for y in range(sheetTestCase.cell_value(l,6).count(";")+1):
                            exec(sheetTestCase.cell_value(l,6).split(";",sheetTestCase.cell_value(l,6).count(';'))[y])
                            # print sheetTestCase.cell_value(l,6).split(";",sheetTestCase.cell_value(l,6).count('RtnOK'))[y]

                    # 优先级2
                    if sheetTestCase.cell_value(l,5).count(";")>0:
                        y=0
                        for y in range(sheetTestCase.cell_value(l,5).count(";")+1):
                            exec(sheetTestCase.cell_value(l,5).split(";",sheetTestCase.cell_value(l,5).count(';'))[y])

                    # 优先级3
                    if sheetTestCase.cell_value(l,4).count(";")==0:
                        # print sheetTestCase.cell_value(l,4)
                        exec(sheetTestCase.cell_value(l,4))
                    else:
                        z=0
                        for z in range(sheetTestCase.cell_value(l,4).count(";")+1):
                            # print sheetTestCase.cell_value(l,4).split(";",sheetTestCase.cell_value(l,4).count(';'))[z]
                            exec(sheetTestCase.cell_value(l,4).split(";",sheetTestCase.cell_value(l,4).count(';'))[z])
                    newWs=newbk.get_sheet(1)
                    newWs.write(l,0,"OK",styleBlue)
                    newbk.save(ExcelFile)
            except:
                print u"Excel,Err,第"+str(l+1)+u"行,"+sheetTestCase.cell_value(l,3)
                newWs=newbk.get_sheet(1)
                newWs.write(l,0,"error",styleRed)
                newbk.save(ExcelFile)

    def Idefault(self,casePrefix,caseStatus,caseParam):
        # 通过字典获取参数 , 遍历字典,输出('key','value'),获取指定的value
        Params = eval(caseParam)
        print "================="
        print Params
        print "==============="
        # 如果有手机号则先获取
        for phone in Params.items():
            if "phone" in phone: varPhone = phone[1]
            if "mobileNum" in phone: varPhone = phone[1]
        for x in Params.items():
            if "userId" in x: varUserId = x[1]
            elif "verifyUserId" in x: varUserId = x[1]
            elif "mobileNum" in x:
                self.curWeb.execute('select id from t_user where username="%s" order by id desc limit 1' % x[1])
                tbl0 = self.curWeb.fetchone()
                varUserId = tbl0[0]
            elif "phone" in x:
                self.curWeb.execute('select id from t_user where username="%s" order by id desc limit 1' % x[1])
                tbl0 = self.curWeb.fetchone()
                varUserId = tbl0[0]
            if "mobileCode" in x:
                # 参数: type=1 获取登录验证码 , 2 提现验证码 , 4=设置提现密码
                varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.1/send_mobile_code.do"
                requests.request("GET", varUrl, headers={'cache-control': "no-cache"}, params={"type":str(x[1]),"mobileNum": str(varPhone)})
                r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
                Params['mobileCode']=r.get("app_withdrawCode_" + str(varPhone))
            elif "password" in x:
                # 参数: type=1 获取登录验证码 , 2 提现验证码 , 4=设置提现密码
                varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.1/send_mobile_code.do"
                requests.request("GET", varUrl, headers={'cache-control': "no-cache"}, params={"type":str(x[1]),"mobileNum": str(varPhone)})
                r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
                Params['password']=r.get("app_login_" + str(varPhone))
        # 通过字符串获取参数  # print caseParam.count(':') 参数个数 ,输出#C27-1,"userId","messageId","groupId","batchId","channelId"
        varParams=""
        for i in range(caseParam.count(':')):
            y=caseParam.split(",",caseParam.count(':'))[i]
            # print y.split(":",caseParam.count(':'))[0].replace("{","")
            varParams = varParams + "," + y.split(":",caseParam.count(':'))[0].replace("{","")
        caseParams = casePrefix + varParams
        varInterfaceName = self.CaseInfo.split(";",1)[0]
        varUrl = self.CaseInfo.split(";",1)[1]
        # 字典中加入用户id和用户code
        r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
        varCode = r.hget("app:verify:"+str(varUserId),"code")
        query1={}
        query1["verifyUserId"]= varUserId
        query1["verifyCode"]= varCode
        for x in Params:
            query1[x] = str(Params[x])
        # print query1
        headers = {'cache-control': "no-cache"}
        response = requests.request("GET", varUrl, headers=headers, params=query1)
        try:
            if caseStatus=="RtnNullOK" :  #如:{"data":null,"errorstr":"","errorcode":0,"success":true}
                if response.json()['success']==True:print "[OK,RtnNullOK] "  + caseParams + " => " + response.content
                else:
                    print "[errorrrrrrrrrr,RtnNullOK] "  + caseParams + " => " + response.content
                    sendemail(varInterfaceName,"[errorrrrrrrrrr,RtnOK] "  + caseParams + " => " + response.content)
            if caseStatus=="RtnOK" : #如:{"data":149,"errorstr":"","errorcode":0,"success":true}
                if response.json()['success']==True and len(str(response.json()['data']))>0:print "[OK,RtnOK] " + caseParams + " => " + response.content
                else:
                    print "[errorrrrrrrrrr,RtnOK] "  + caseParams + " => " + response.content
                    sendemail(varInterfaceName,"[errorrrrrrrrrr,RtnOK] "  + caseParams + " => " + response.content)
            if caseStatus=="RtnNoDATAOK" : # 如:{"data":[],"errorstr":"","errorcode":0,"success":true}
                if response.json()['success'] == True and response.json()['data'] == []:print "[OK,RtnNoDATAOK] "   + caseParams + " => " + response.content
                else:
                    print "[errorrrrrrrrrr,RtnNoDATAOK] "  + caseParams + " => " + response.content
                    sendemail(varInterfaceName,"[errorrrrrrrrrr,RtnOK] "  + caseParams + " => " + response.content)
            if caseStatus=="RtnSysErr" :
                if response.json()['errorcode']==100001 and response.json()['success']== False:print "[OK,RtnSysErr] "  + caseParams + " => " + response.content
                else: print "[errorrrrrrrrrr,RtnSysErr] "  + caseParams + " => " + response.content
            if caseStatus=="RtnParamErr" :
                if response.json()['errorcode']==100002 and response.json()['success']== False:print "[OK,RtnParamErr] "  + caseParams + " => " + response.content
                else:print "[errorrrrrrrrrr,RtnParamErr] "   + caseParams + " => " + response.content
            if caseStatus=="RtnDeviceErr" :
                if response.json()['errorcode']==100003 and response.json()['success']== False:print "[OK,RtnDeviceErr] "  + caseParams + " => " + response.content
                else:
                    print "[errorrrrrrrrrr,RtnDeviceErr] "  + caseParams + " => " + response.content
                    sendemail(varInterfaceName,"[errorrrrrrrrrr,RtnOK] "  + caseParams + " => " + response.content)
        except Exception,data:
            print Exception,":",data,"\n"

    def Idepend(self,caseName,caseUrl,caseStatus,caseParam):
        # 通过字典获取参数 , 遍历字典,输出('key','value'),获取指定的value
        Params = eval(caseParam)

        # 如果有手机号则先获取
        for phone in Params.items():
            if "phone" in phone: varPhone = phone[1]
            if "mobileNum" in phone: varPhone = phone[1]
        for x in Params.items():
            if "userId" in x: varUserId = x[1]
            elif "verifyUserId" in x: varUserId = x[1]
            elif "mobileNum" in x:
                self.curWeb.execute('select id from t_user where username="%s" order by id desc limit 1' % x[1])
                tbl0 = self.curWeb.fetchone()
                varUserId = tbl0[0]
            elif "phone" in x:
                self.curWeb.execute('select id from t_user where username="%s" order by id desc limit 1' % x[1])
                tbl0 = self.curWeb.fetchone()
                varUserId = tbl0[0]
            if "mobileCode" in x:
                # 参数: type=1 获取登录验证码 , 2 提现验证码 , 4=设置提现密码
                varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.1/send_mobile_code.do"
                requests.request("GET", varUrl, headers={'cache-control': "no-cache"}, params={"type":str(x[1]),"mobileNum": str(varPhone)})
                r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
                Params['mobileCode']=r.get("app_withdrawCode_" + str(varPhone))
            elif "password" in x:
                # 参数: type=1 获取登录验证码 , 2 提现验证码 , 4=设置提现密码
                varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.1/send_mobile_code.do"
                requests.request("GET", varUrl, headers={'cache-control': "no-cache"}, params={"type":str(x[1]),"mobileNum": str(varPhone)})
                r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
                Params['password']=r.get("app_login_" + str(varPhone))

        # 通过字符串获取参数  # print caseParam.count(':') 参数个数 ,输出#C27-1,"userId","messageId","groupId","batchId","channelId"
        varParams=""
        for i in range(caseParam.count(':')):
            y=caseParam.split(",",caseParam.count(':'))[i]
            # print y.split(":",caseParam.count(':'))[0].replace("{","")
            varParams = varParams + "," + y.split(":",caseParam.count(':'))[0].replace("{","")

        caseParams = caseName + varParams

        # 字典中加入用户id和用户code
        r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
        varCode = r.hget("app:verify:"+str(varUserId),"code")
        query1={}
        query1["verifyUserId"]= varUserId
        query1["verifyCode"]= varCode
        for x in Params:
            query1[x] = str(Params[x])
        headers = {'cache-control': "no-cache"}
        response = requests.request("GET", caseUrl, headers=headers, params=query1)
        try:
            if caseStatus=="RtnNullOK" :  #如:{"data":null,"errorstr":"","errorcode":0,"success":true}
                if response.json()['success']==True:print "<OK,RtnNullOK> "  + caseParams + " => " + response.content
                else:
                    print "<errorrrrrrrrrr,RtnNullOK> "  + caseParams + " => " + response.content
                    sendemail(caseName + "[errorrrrrrrrrr,RtnOK] "  + caseParams + " => " + response.content)
            if caseStatus=="RtnOK" : #如:{"data":149,"errorstr":"","errorcode":0,"success":true}
                if response.json()['success']==True and len(str(response.json()['data']))>0:print "<OK,RtnOK> " + caseParams + " => " + response.content
                else:
                    print "<errorrrrrrrrrr,RtnOK> "  + caseParams + " => " + response.content
                    sendemail(caseName,"[errorrrrrrrrrr,RtnOK] "  + caseParams + " => " + response.content)
            if caseStatus=="RtnNoDATAOK" : # 如:{"data":[],"errorstr":"","errorcode":0,"success":true}
                if response.json()['success'] == True and response.json()['data'] == []:print "<OK,RtnNoDATAOK> "   + caseParams + " => " + response.content
                else:
                    print "<errorrrrrrrrrr,RtnNoDATAOK> "  + caseParams + " => " + response.content
                    sendemail(caseName,"[errorrrrrrrrrr,RtnOK],"  + caseParams + " => " + response.content)
            if caseStatus=="RtnSysErr" :
                if response.json()['errorcode']==100001 and response.json()['success']== False:print "<OK,RtnSysErr> "  + caseParams + " => " + response.content
                else: print "<errorrrrrrrrrr,RtnSysErr>,"  + caseParams + " => " + response.content
            if caseStatus=="RtnParamErr" :
                if response.json()['errorcode']==100002 and response.json()['success']== False:print "<OK,RtnParamErr> "  + caseParams + " => " + response.content
                else:print "<errorrrrrrrrrr,RtnParamErr> "   + caseParams + " => " + response.content
            if caseStatus=="RtnDeviceErr" :
                if response.json()['errorcode']==100003 and response.json()['success']== False:print "<OK,RtnDeviceErr> "  + caseParams + " => " + response.content
                else:
                    print "<errorrrrrrrrrr,RtnDeviceErr> "  + caseParams + " => " + response.content
                    sendemail(caseName,"[errorrrrrrrrrr,RtnOK] "  + caseParams + " => " + response.content)
        except Exception,data:
            print Exception,":",data,"\n"

    def drv(self):
        self.TestcaseModule()

if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(InterfaceKeywork) # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1) # 执行测试

