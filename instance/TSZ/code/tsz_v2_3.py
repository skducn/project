# coding: utf-8
#****************************************************************
# tsz_v2_3.py
# Author     : John
# Version    : 1.0.0
# Date       : 2016-6-1
# Description: 自动化测试平台
#****************************************************************


#http://tungwaiyip.info/software/HTMLTestRunner.html
import os,sys,unittest,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis
from appium import webdriver
#from selenium import webdriver
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
# print sys.path
# from resource.source.comparePic import *
# from resource.source import test2


################ test area ################
# pp = "t_user:id:10001789"
# r = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
# r.hset(pp,"Commission_residue",0)
# print "ok"
# sleep(1212)
# xx="(含6.0运费)"
# yy=xx[4:]
# print yy[:-7]
# a="12.6"
# b="3"
# c="6.0"
# print float(a)*int(b)+float(c)
# print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# sleep(123)
#os.path.abspath() 方法用于获取当前路径下的文件
#PATH = lambda p: os.path.abspath(p)
################################################

# 页面格式化 http://www.tuicool.com/articles/IRvEBr
# page =PyH('JHJ_TestReport')
# page.addCSS('myStylesheet1.css','myStylesheet2.css')
# page << h2(u'极好家V1.5自动化测试报告', cl='center')
# page << h4(u'Start Time:',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# page << h4(u'用例执行情况：')

# 环境变量
myPhone="13816101145"
partmyPhone = myPhone[0:3] + "****" + myPhone[7:]

File_ExcelName = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/excel/tsz_v2_3.xls" #
Html_Testreport = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/report/testreport_v2_3.html" # TestReport文件
Folder_Screenshot="/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/screenshot/"  #org\curr 截屏
Folder_Errscreenshot = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/errscreenshot/"  # 错误截屏
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class Tsz_2_3(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = '6c9cb8bf'
        desired_caps['appPackage'] = 'com.mowin.tsz'
        desired_caps['appActivity'] = 'com.mowin.tsz.SplashActivity'
        desired_caps['unicodeKeyboard'] ='True'
        desired_caps['resetKeyboard'] = 'True'
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        # app=os.path.join(os.path.dirname(__file__),
        #       '../../../../ForMac/iOS/JHJ.app')
        # app=os.path.abspath(app)
        # self.driver=webdriver.Remote(
        # command_executor='http://127.0.0.1:4723/wd/hub',
        # desired_capabilities={
        # 'browserName':'iOS',
        # 'platform':'Mac',
        # 'version':'6.0',
        # 'app': app
        # })

        # app=os.path.join(os.path.dirname(__file__),'JHJ.app')
        # app=os.path.abspath(app)
        # self.driver=webdriver.Remote(
        #   command_executor='http://127.0.0.1:4723/wd/hub',
        #   desired_capabilities={
        #     'browserName':'iOS',
        #     'platform':'Mac',
        #     'version':'6.0',
        #     'app': app
        #   })
        # self._values=[]

        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit
        #conn= MySQLdb.connect(host='192.168.2.144', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        #conn= MySQLdb.connect(host='192.168.2.100', user='lvjinyue', passwd='lvjinyue', db='ukardweb', port=3307, use_unicode=True) #uat
        cur = conn.cursor()
        conn.set_character_set('utf8')
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        self.cur=cur
        # 获取数据库所有表名
        self.cur.execute('show tables')
        AllTables=self.cur.fetchall()
        self.AllTables=AllTables
        self.conn=conn

        self.fname=File_ExcelName
        self.bk = xlrd.open_workbook(File_ExcelName,formatting_info=True)
        #self.bk=bk
        self.newbk=copy(self.bk)
        #self.newbk=newbk
        self.styleP = xlwt.easyxf('font: name Times New Roman, color-index blue')
        self.styleE = xlwt.easyxf('font: name Times New Roman, color-index red')
        # self.styleP=styleP
        # self.styleE=styleE
        #self.browser = webdriver.Firefox()
    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        # 遍历report目录中最新的文件
        # result_dir = 'C:\\Python27\\TMPappium\\report'
        # lists=os.listdir(result_dir)
        # lists.sort(key=lambda fn: os.path.getmtime(result_dir+"\\"+fn) if not
        # os.path.isdir(result_dir+"\\"+fn) else 0)
        # #print ('最新的文件为： '+lists[-1])
        # file_new = os.path.join(result_dir,lists[-1])
        # #print file_new
    def sendemail(self):
        # 邮箱配置
        sender = 'john.jin@jihaojia.com.cn'
        receiver = 'john.jin@jihaojia.com.cn'
        f = open(Html_Testreport,'rb')
        mail_body = f.read()
        f.close()
        msg=MIMEText(mail_body,_subtype='html',_charset='utf-8')
        #msg = MIMEText('<html><h1>你好！</h1></html>','html','utf-8')
        # msg = MIMEText('你好','text','utf-8')
        # msg['Subject'] = Header(subject,'utf-8')
        msg['Subject'] = u'极好家V1.5自动化测试报告'
        smtpserver = 'smtp.mxhichina.com'
        smtp = smtplib.SMTP()
        smtp.connect('smtp.mxhichina.com')
        smtp.login('john.jin@jihaojia.com.cn','Tester411')
        smtp.sendmail(sender,receiver,msg.as_string())
        smtp.quit()

    def test_Main(self):
        # 初始化驱动
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
                exec(sh1.cell_value(i,4))
        #send Email
        if sh1.cell_value(1,5) == "Y":
            self.sendemail()
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
                   print "Excel,Err,第"+str(l+1)+"行,"+self.sh2.cell_value(l,3)
                   newWs=self.newbk.get_sheet(1)
                   newWs.write(l,0,"error",self.styleE)
                   self.newbk.save(self.fname)
                   # page << p("<font color=red>[Error]</font> ",self.sh2.cell_value(l,3))  #输出测试用例
               # page.printOut(Html_Testreport)
               #open HTML
               # if self.sh1.cell_value(1,6) == "Y":
               #    webbrowser.open(Html_Testreport)


    # =================== [web] ===================
    def b_login(self):
        # 登录失败后继续登录,最多尝试5次
        for b in range(5):
            # WEB端登录
            self.browser.maximize_window()  #将浏览器最大化
            self.browser.get("http://sit2.88uka.com/admin/finance/userExperienceList.do")
            self.browser.find_element_by_id("userName").clear() #清空输入框默认内容
            self.browser.find_element_by_id("userName").send_keys("test")
            self.browser.find_element_by_id("passWord").send_keys("111111")
            self.browser.save_screenshot('/Users/linghuchong/Downloads/51/aa.png')  #截取当前网页，该网页有我们需要的验证码
            imgelement = self.browser.find_element_by_id("authCode")  #定位验证码
            location = imgelement.location  #获取验证码x,y轴坐标
            size=imgelement.size  #获取验证码的长宽
            rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
            i=Image.open("/Users/linghuchong/Downloads/51/aa.png") #打开截图
            frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
            frame4.save('/Users/linghuchong/Downloads/51/aaframe4.png')
            qq=Image.open('/Users/linghuchong/Downloads/51/aaframe4.png')
            #text=pytesseract.image_to_string(qq) #使用image_to_string识别验证码
            os.system('tesseract /Users/linghuchong/Downloads/51/aaframe4.png out -l eng')
            text = os.popen('more out.txt').readline()
            self.browser.find_element_by_id("randomCode").send_keys(text)
            #self.browser.find_element_by_class_name("btn-c").click()
            sleep(5)
            if self.b_isElement("edit_password")<>True:
                 print "Err,WEb三藏红包系统平台验证码错误!"
                 self.browser.close()
                 self.browser = webdriver.Firefox()
                 sleep(3)
            else:
                break
    def b_close(self):
        self.browser.close()
    def b_chongzhi(self,varAmount,varExpire):
        # Web后台充值并审核通过,如对手机13816101118充值70元,有效期99天,则 b_chongzhi(self,"70","99") ,默认手机号是当前myPhone
        self.browser.find_element_by_xpath('//div[@class="nav"]/ul/li[3]').click()    # 点击主菜单 财务
        sleep(3)
        self.browser.find_element_by_xpath('//div[@id="container"]/div/dl/dd[14]').click()  # 点击侧边菜单 充值
        sleep(2)
        self.browser.find_element_by_name("btnUserExperience").click()  # 点击 充值按钮
        self.browser.find_element_by_name("userName").send_keys(myPhone) # 手机号
        self.browser.find_element_by_name("experienceAmount").send_keys(varAmount) # 充值金额 70
        self.browser.find_element_by_name("day").send_keys(varExpire) # 金额过期 99 days
        self.browser.find_element_by_id("submitButton").click()
        a=self.browser.switch_to_alert()
        a.accept()
        sleep(2)
        # 运营
        self.browser.find_element_by_xpath('//div[@class="nav"]/ul/li[4]').click()    # 运营
        sleep(3)
        self.browser.find_element_by_xpath('//div[@id="container"]/div/dl/dd[4]').click()  # 信息审核(1425)
        sleep(2)
        self.browser.find_element_by_xpath('//tbody/tr/td[7]/a').click()  # 审核
        self.browser.find_element_by_name("auditPass").click() # 通过
        a=self.browser.switch_to_alert()
        a.accept()
        sleep(2)
        a=self.browser.switch_to_alert()
        a.accept()
        return varAmount


    # =================== [common] ===================
    def customPic(self,img,startX, startY, endX, endY):
        # 自定义截取范围
        # img=u"%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        # self.get_screenshot_by_custom_size(self,u"%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3],0, 76, 1080, 1769)
        self.driver.save_screenshot(img)
        box=(startX, startY, endX, endY)
        i = Image.open(img)
        newImage = i.crop(box)
        newImage.save(img)

    def comparePic(self,img1,img2,startX,startY,endX,endY):
         # 两图比较,如无原始图则截屏后退出(不比较),否则两图比较,不一致则返回时间戳
         # img1='big_redgame.png' , img2= 'org_redgame.png'
         # self.comparePic(self,img1,img2,0, 76, 1080, 1769)
         self.driver.save_screenshot(img1)
         box=(startX,startY,endX,endY)
         i = Image.open(img1)
         newImage = i.crop(box)
         newImage.save(img1)
         sleep(2)
         if os.path.exists(img2):
             tmpimg1 = open(img1, "r")
             tmpimg2 = open(img2, "r")
             if tmpimg1.read() <> tmpimg2.read():
                 now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
                 return now
             else:
                 return 1
         else:
             os.renames(img1,img2)
             return 0

   #判断app元素是否存在,不存在则返回时间戳
    def isElement(self,locate):
        # 判断app元素是否存在,不存在则返回时间戳
        flag = False
        try:
            self.driver.find_element_by_id(locate)
            flag = True
        except :
            flag = False
        return flag
    def b_isElement(self,locate):
        # 判断browser元素是否存在,不存在则返回时间戳
        flag = False
        try:
            self.browser.find_element_by_id(locate)
            flag = True
        except :
            flag = False
            flagfile=u"%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        return flag,flagfile
    def userLogin(self):
        # Common 用户第一次登录, 手机快速登录 页面,
        # ===== EXcel ID0 -ID9 参数用法 ====
        # for i in range(0,len(self.str_list)): # 遍历参数
        #     print self.str_list[i]
        # print self.str_list[0]  # 输出第一个参数
        # print type(self.str_list[1]) # 输出类型
        # [手机快速登录]
        # self.driver.find_element_by_id(self.str_list[1]).send_keys(myPhone)
        # self.driver.find_element_by_id(self.str_list[2]).click()
        # 等同于下面2句, 上面用了Excel中的参数1\2
        if self.isElement("com.mowin.tsz:id/phone_number")==True:
            sleep(2)
            self.driver.find_element_by_id("com.mowin.tsz:id/phone_number").send_keys(myPhone)
            self.driver.find_element_by_id("com.mowin.tsz:id/get_mobile_code").click()
            sleep(2)
            # 获取验证码
            self.cur.execute('select verify_code from ta_message where phone=%s order by id desc limit 1' % (myPhone))
            data9 = self.cur.fetchone()
            self.driver.find_element_by_id("com.mowin.tsz:id/mobile_code").send_keys(data9[0])
            self.driver.find_element_by_id("com.mowin.tsz:id/login").click()
            sleep(2)
    def myScreenshot(self,img,startX,startY,endX,endY,casenum):
        # org截屏
        # self.myScreenshot("weixinpay",160, 0, 1080, 1920,"C3-1")
        sleep(2)
        compareResult = self.comparePic(Folder_Screenshot + 'big_' + img + '.png',Folder_Screenshot + 'org_' + img + '.png',startX,startY,endX,endY)
        if compareResult > 1:
             print "Err," + casenum + "," + img + compareResult + ".png!"
             self.driver.save_screenshot(Folder_Errscreenshot + img + compareResult + ".png")
        elif compareResult == 0:
             print "Created," + casenum + ",org_" + img + ".png"


    # =================== [app] ===================


    # 首页
    def drv_home(self):
        self.TestcaseModule()
    def homepage(self):
        # C1-1，首页元素检查
        pass
        self.driver.switch_to.context("WEBVIEW")
        self.driver.switch_to_default_content()

    def bridingThird(self):
        # C1-2，初次登录，检查第三方账号绑定
        # 清理第三方账号
        self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click()
        self.userLogin()
        self.cur.execute('delete from t_user_thirdInfo where belongName="%s" or belongName="%s" or belongName="%s"' % ("John","令狐冲","用户5590858666"))
        self.conn.commit()
        sleep(8)

        # 第三方账号绑定
        self.driver.find_element_by_id("com.mowin.tsz:id/settings").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/bind_other_account").click()
        sleep(2)
        img = "third"
        compareResult = self.comparePic(Folder_Screenshot + 'big_' + img + '.png',Folder_Screenshot + 'org_' + img + '.png',0, 76, 1080, 1769)
        if compareResult>1:
             print "Err,third 截屏文件:"+ img + compareResult + ".png!"
             self.driver.save_screenshot(Folder_Errscreenshot + compareResult + ".png")
        elif compareResult==0:
             print "Info,获取原始 "+img+" 的截屏."


        # 点击微信 授权  测试微信号 = John
        self.driver.find_element_by_id("com.mowin.tsz:id/bind_wx_status").click()
        sleep(4)
        img = "thirdweixinLogin"
        compareResult = self.comparePic(Folder_Screenshot + 'big_' + img + '.png',Folder_Screenshot + 'org_' + img + '.png',0, 76, 1080, 1769)
        if compareResult>1:
             print "Err,微信授权登录页:"+ img + compareResult + ".png!"
             self.driver.save_screenshot(Folder_Errscreenshot + img + compareResult + ".png")
        elif compareResult==0:
             print "Info,获取原始 "+img+" 的截屏."
        # 微信页面确认登录
        self.driver.swipe(500, 1065, 500, 1065, 500); # 点击 登录
        sleep(3)
        if self.driver.find_element_by_id("com.mowin.tsz:id/bind_wx_status").text<>"已授权":
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
            print "Err,C1-2,微信授权失败:"+Folder_Errscreenshot + img + timestamp + ".png"
            self.driver.save_screenshot(Folder_Errscreenshot + img + timestamp + ".png")
        sleep(2)


        # # 点击QQ 授权  测试QQ号 = 令狐冲
        self.driver.find_element_by_id("com.mowin.tsz:id/bind_qq_status").click()
        sleep(4)
        img = "thirdqqLogin"
        compareResult = self.comparePic(Folder_Screenshot + 'big_' + img + '.png',Folder_Screenshot + 'org_' + img + '.png',0, 76, 1080, 1769)
        if compareResult>1:
             print "Err,QQ授权登录页:"+ img + compareResult + ".png!"
             self.driver.save_screenshot(Folder_Errscreenshot + img + compareResult + ".png")
        elif compareResult==0:
             print "Info,获取原始 "+img+" 的截屏."
        # QQ页面确认登录
        self.driver.swipe(500, 1500, 500, 1500, 500); # 点击 登录
        sleep(3)
        if self.driver.find_element_by_id("com.mowin.tsz:id/bind_qq_status").text<>"已授权":
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
            print "Err,C1-2,qq授权失败:"+Folder_Errscreenshot + img + timestamp + ".png"
            self.driver.save_screenshot(Folder_Errscreenshot + img + timestamp + ".png")


        # # 点击微博 授权
        self.driver.find_element_by_id("com.mowin.tsz:id/bind_weibo_status").click()
        sleep(4)
        img = "thirdweiboLogin"
        compareResult = self.comparePic(Folder_Screenshot + 'big_' + img + '.png',Folder_Screenshot + 'org_' + img + '.png',0, 76, 1080, 1769)
        if compareResult>1:
             print "Err,weibo授权登录页:"+ img + compareResult + ".png!"
             self.driver.save_screenshot(Folder_Errscreenshot + img + compareResult + ".png")
        elif compareResult==0:
             print "Info,获取原始 "+img+" 的截屏."
        # weibo页面确认登录
        self.driver.swipe(500, 900, 500, 900, 500); # 点击 登录
        sleep(3)
        if self.driver.find_element_by_id("com.mowin.tsz:id/bind_weibo_status").text<>"已授权":
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
            print "Err,C1-2,weibo授权失败:"+Folder_Errscreenshot + img + timestamp + ".png"
            self.driver.save_screenshot(Folder_Errscreenshot + img + timestamp + ".png")

        # 第三方账号绑定 微信\QQ\微博 已授权截图
        img = "thirdweixinqqAuthorized"
        compareResult = self.comparePic(Folder_Screenshot + 'big_' + img + '.png',Folder_Screenshot + 'org_' + img + '.png',0, 76, 1080, 1769)
        if compareResult>1:
             print "Err,第三方账号全部已授权:"+ img + compareResult + ".png!"
             self.driver.save_screenshot(Folder_Errscreenshot + img + compareResult + ".png")
        elif compareResult==0:
             print "Info,获取原始 "+img+" 的截屏."
        sleep(4)
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
        if self.driver.find_element_by_id("com.mowin.tsz:id/name").text<>"John":print "Err,C1-2,微信授权后,我页面中昵称未更换!"

        # # t_user_thirdINfo表验证数据 , 获取userId  ?有问题
        # self.cur.execute('select id from t_user where username="%s" order by id desc limit 1' % (myPhone))
        # data1 = self.cur.fetchone()
        # print "12121212"
        # print data1[0]
        # self.cur.execute('select belongName,belongThumb,isValid,openid,token from t_user_thirdInfo where userId=%s and channel=1 order by id desc ' % (data1[0]))
        # data2 = self.cur.fetchone()
        # if data2[0] == "John" and data2[1]<>"" and data2[2]=="1" and data2[3]<>"" and data2[4]<>"":
        #     pass
        # else:
        #     print u"Err,微信授权数据库:belongName="+ data2[0]+" , belongThumb="+ data2[1]+" , isValid="+ data2[2]+" , openid="+ data2[3]+" , token="+ data2[4]
        #
        # self.cur.execute('select belongName,belongThumb,isValid,openid,token from t_user_thirdInfo where userId=%s and channel=2 order by id desc ' % (data1[0]))
        # data2 = self.cur.fetchone()
        # if data2[0] == u"令狐冲" and data2[1]<>"" and data2[2]=="1" and data2[3]<>"" and data2[4]<>"":
        #     pass
        # else:
        #     print u"Err,QQ授权数据库:belongName="+ data2[0]+" , belongThumb="+ data2[1]+" , isValid="+ data2[2]+" , openid="+ data2[3]+" , token="+ data2[4]


    # 红包群
    def drv_redgroup(self):
        self.TestcaseModule()

    # 红包游戏
    def drv_redgame(self):
        print "\n"
        self.driver.find_element_by_id("com.mowin.tsz:id/game_tab").click() # 红包游戏
        self.userLogin()
        sleep(2)
        # 红包游戏列表页截屏,红包游戏列表页
        self.myScreenshot("HBBDX_list",0, 76, 1080, 1769,"C3-1")
        # 进入游戏
        self.driver.find_element_by_id("com.mowin.tsz:id/button").click()  # 点击 进入游戏
        self.TestcaseModule()


    def HBBDXweixinRecharge(self):
        # C3-1,用户首次进入游戏(体验游戏)
        # 检查点1,红包比大小页面元素截屏(不包括在线人数)
        self.myScreenshot("HBBDX_mainPageWithWidth",160, 0, 1080, 1920,"C3-1")
        self.myScreenshot("HBBDX_mainPageWithHeight",0, 0, 1080, 1500,"C3-1")

        # 检查点2,游戏余额 + 现金余额 = 0.00
        gameAmount = self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").text
        gameAmount = gameAmount.split("￥")
        if gameAmount[1] == "0.00":
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").click()   # 点击 游戏余额:$0.00
            # 点击游戏余额后, 弹出 充值游戏余额(高亮) 和 余额退回我的钱包 浮层,
            self.myScreenshot("HBBDX_clickGameBalanceRechargeLight",0, 0, 1080, 1500,"C3-1")
            sleep(2)
            self.driver.swipe(300, 750, 300, 750, 500); # 点击 充值游戏余额
            # 充值游戏余额
            self.myScreenshot("HBBDX_rechargeGameBalanceWeixinLight",160, 0, 1080, 1920,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/weixin_pay_icon").click()
            # 充值游戏余额浮层中 , 点击 微信支付
            self.myScreenshot("HBBDX_weixinPay",160, 0, 1080, 1920,"C3-1")
            # 微信支付
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount").send_keys("1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            sleep(10)
            # 页面跳转到 微信安全支付 确认交易 ,点击立即支付
            self.myScreenshot("HBBDX_weixinPagePayConfirm",0, 350, 1080, 1769,"C3-1")
            print self.driver.find_element_by_id("com.tencent.mm:id/cnp").text  # 游戏充值 190899
            self.driver.swipe(500, 800, 500, 800, 500); # 点击 立即支付
            # 820124
            sleep(4)
            self.driver.swipe(540, 1600, 540, 1600, 500); # 点击 8
            sleep(1)
            self.driver.swipe(540, 1300, 540, 1300, 500); # 点击 2
            sleep(1)
            self.driver.swipe(540, 1800, 540, 1800, 500); # 点击 0
            sleep(1)
            self.driver.swipe(200, 1300, 200, 1300, 500); # 点击 1
            sleep(1)
            self.driver.swipe(540, 1300, 540, 1300, 500); # 点击 2
            sleep(1)
            self.driver.swipe(200, 1400, 200, 1400, 500); # 点击 4
            sleep(4)
            # 交易详情 , 微信安全支付 ,完成
            self.myScreenshot("HBBDX_weixinPagePayFinish",0, 220, 1080, 600,"C3-1")
            sleep(3)
            self.driver.find_element_by_id("com.tencent.mm:id/ed").click() # 点击完成
            sleep(5)
            # 红包比大小页面 ,浮层 已成功充值1.00元游戏余额,快进入游戏试试手气吧.
            self.myScreenshot("HBBDX_infoWeixinPay1yuanOK",0, 0, 1080, 1500,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click() # 点击 知道了
            # 红包比大小页面 检查游戏余额:$ 1.00
            self.myScreenshot("HBBDX_gameBalance1yuanFromWeixin",0, 0, 1080, 1500,"C3-1")

            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").click()   # 点击 游戏余额:$1.00
            # 点击游戏余额后, 弹出 充值游戏余额(高亮) 和 余额退回我的钱包(高亮) 浮层,
            self.myScreenshot("HBBDX_clickGameBalanceRechargeAndBackLight",0, 0, 1080, 1500,"C3-1")
            sleep(2)
            self.driver.swipe(300, 840, 300, 840, 500); # 点击 余额退回我的钱包
            self.myScreenshot("HBBDX_balanceOut",160, 0, 1080, 1920,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount_hint").send_keys("1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            # 浮层 , 1.00元游戏余额已成功退回到你的钱包余额账户内.
            self.myScreenshot("HBBDX_info1yuantoAccount",160, 0, 1080, 1920,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click() # 点击 知道了
            # 红包比大小页面 检查游戏余额:$ 0.00
            gameAmount = self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").text
            gameAmount = gameAmount.split("￥")
            if gameAmount[1] <> "0.00":print "Err,C3-1,经过了微信充值及余额退回操作后,游戏余额应是0.00!,实测结果:" + str(gameAmount[1])

            # 点击 游戏余额
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").click()   # 点击 游戏余额:$0.00
            self.driver.swipe(300, 750, 300, 750, 500); # 点击 充值游戏余额
            # 点击 充值游戏余额
            self.myScreenshot("HBBDX_rechargeGameBalanceAllLight",160, 0, 1080, 1920,"C3-1")
            # 充值游戏余额浮层中 , 点击 余额支付
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/account_balance_icon").click() # 点击 余额支付
            # 余额支付 浮层, 充值 1元
            self.myScreenshot("HBBDX_balancePay",160, 0, 1080, 1920,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount_hint").send_keys("1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            sleep(2)
            # 浮层, 已成功充值1.00元游戏余额,快进入游戏试试手气吧.
            self.myScreenshot("HBBDX_infoBalancePay1yuanOK",0, 0, 1080, 1500,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click() # 点击 知道了

            # 开始 体验游戏 ,游戏中点击退出游戏
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click() # 点击 体验游戏
            sleep(8)
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/exit_game").click() # 点击 退出游戏
            var1=self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/message").text
            print var1
            if var1 <> u"现在离开, 本轮游戏将由笨笨的机器人代玩哟, 输了可不要怪它喔~":print u"Err,C3-1,提示:现在离开, 本轮游戏将由笨笨的机器人代玩哟, 输了可不要怪它喔~ 实测:" + str(var1)
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/negative").click() # 点击 知道 返回游戏主界面
            # redis中清除isExperience =0
            self.cur.execute('select id from t_user where username="%s" order by id desc' % (myPhone))
            data1 = self.cur.fetchone()
            ppz = "t_game_user:"+str(data1[0])
            r = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
            r.hset(ppz,"isExperience",0)
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/exit_game").click() # 点击 退出游戏
            # 退出游戏 浮层截屏 ,
            self.myScreenshot("HBBDX_exitGame",180, 0, 1080, 1500,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/negative").click() # 点击 确定
            sleep(2)

            self.driver.find_element_by_id("com.mowin.tsz:id/button").click()  # 点击 进入游戏

            # 检查点3,开始 体验游戏 ,体验游戏结束后自动弹出浮层 ,点击知道返回游戏主界面
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click() # 点击 体验游戏
            sleep(80)
            if self.isElement("com.mowin.tsz.thanthesize:id/positive"):
                var1=self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/message").text
                if var1 <> u"游戏体验已结束, 进入正式游戏试试身手吧~":print u"Err,C3-1,提示:游戏体验已结束, 进入正式游戏试试身手吧~ 实测:" + str(var1)
                self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click() # 点击知道了
            else:
                self.driver.save_screenshot(Folder_Errscreenshot + u"体验游戏结束后无弹出浮层.png")
                print "Err,C3-1,体验游戏结束后无弹出浮层!"


            # 检查点4,体验游戏 变为 开始游戏 ,截屏
            self.myScreenshot("HBBDX_startGame",0, 0, 1080, 1500,"C3-1")

            # 检查点5,游戏说明及规则
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/game_help").click() # 点击 游戏说明及规则
            sleep(3)
            # 游戏说明及规则 截图
            self.myScreenshot("HBBDX_gameRule1",0, 0, 1080, 1730,"C3-1")
            self.driver.swipe(1500,600,50,600,2000)
            sleep(2)
            self.myScreenshot("HBBDX_gameRule2",0, 0, 1080, 1730,"C3-1")
            self.driver.swipe(1500,600,50,600,2000)
            sleep(2)
            self.myScreenshot("HBBDX_gameRule3",0, 0, 1080, 1730,"C3-1")
            self.driver.swipe(1500,600,50,600,2000)
            sleep(2)
            self.myScreenshot("HBBDX_gameRule4",0, 0, 1080, 1730,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/close").click()  # 点击 右上角关闭

            # 检查点5,游戏分享
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/share_game").click() # 点击 游戏分享
            # 游戏分享至 截图
            self.myScreenshot("HBBDX_gameShareTo",0, 0, 1080, 1500,"C3-1")
            # # 朋友圈
            # print "1,朋友圈"
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_timeline_icon").click() # 点击 朋友圈
            # sleep(5)
            # self.myScreenshot("HBBDX_gameShareToFriendCircle",0, 491, 1080, 755,"C3-1") # 朋友圈 截屏
            # self.driver.find_element_by_id("com.tencent.mm:id/ez").click() # 朋友圈, 点击 返回
            # self.driver.find_element_by_id("com.tencent.mm:id/bgp").click() # 朋友圈, 点击 退出
            # sleep(8)
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_timeline_icon").click() # 点击 朋友圈
            # self.driver.find_element_by_id("com.tencent.mm:id/ee").click() # 点击 发送
            # print "分享已完成, 请前往朋友圈检查..."
            # sleep(8)
            #
            # # 微信 群
            # print "2,微信群"
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_session_icon").click() # 点击 微信 群
            # sleep(5)
            # self.driver.find_element_by_id("com.tencent.mm:id/ez").click() # 点击 返回
            # sleep(8)
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_session_icon").click() # 点击 微信 群
            # tmpWeixin = self.driver.find_elements_by_id("com.tencent.mm:id/hw")
            # for i in tmpWeixin:
            #     if i.text=="tsz测试群":
            #         i.click()
            #         break
            # self.myScreenshot("HBBDX_gameShareToWeixin",125, 620, 955, 1370,"C3-1") # 微信 截屏
            # self.driver.find_element_by_id("com.tencent.mm:id/bgp").click() # 点击 分享
            # self.driver.find_element_by_id("com.tencent.mm:id/a6x").click() # 点击 返回三藏红包
            # sleep(8)
            # print "分享已完成, 请前往微信群检查..."


            # QQ好友 ? 程序有问题
            print "3,QQ好友"
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_qq_icon").click() # 点击 QQ好友
            sleep(5)
            self.driver.find_element_by_id("com.tencent.mobileqq:id/ivTitleBtnRightText").click() # 点击取消
            sleep(8)
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_qq_icon").click() # 点击 QQ好友
            tmpQQ = self.driver.find_elements_by_id("com.tencent.mobileqq:id/name")
            for i in tmpQQ:
                if i.text=="选择群聊":
                    i.click()
                    break
            self.driver.swipe(800,800,800,800,500) # 选中 TSZtest
            self.myScreenshot("HBBDX_gameShareToQQ",75, 600, 1005, 1395,"C3-1") # QQ 截屏
            self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogRightBtn").click() # 点击 发送
            self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogLeftBtn").click() # 点击 返回三藏红包
            sleep(8)
            print "分享已完成, 请前往QQ好友检查..."


            # # QQ空间 ?程序有问题
            # print "4,QQ空间"
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_qq_zone_icon").click() # 点击 QQ空间
            # sleep(5)
            # self.myScreenshot("HBBDX_gameShareToQQarea",0, 76, 1080, 686,"C3-1") # QQ空间 截屏
            # self.driver.swipe(100,150,100,150,500) # QQ,点击取消
            # sleep(8)
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_qq_zone_icon").click() # 点击 QQ空间
            # sleep(3)
            # self.driver.find_element_by_id("com.tencent.mobileqq:id/ivTitleBtnRightText").click() # QQ空间,点击发表
            # sleep(5)
            # print "分享已完成, 请前往QQ空间检查..."

            # 新浪微博
            print "5,新浪微博"
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_weibo_icon").click() # 点击 新浪微博
            sleep(5)
            self.myScreenshot("HBBDX_gameShareToSinaweibo",0, 76, 1080, 735,"C3-1") # 新浪微博页面 截屏
            self.driver.find_element_by_id("com.sina.weibo:id/titleBack").click() # 新浪微博,点击取消
            self.driver.swipe(300,1200,300,1200,500) # 新浪微博,点击不保存
            sleep(8)
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_weibo_icon").click() # 点击 新浪微博
            sleep(3)
            self.driver.find_element_by_id("com.sina.weibo:id/titleSave").click() # 新浪微博,点击发送
            sleep(5)
            print "分享已完成, 请前往新浪微博检查..."

            # 关闭 游戏分享至
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/close").click() # 点击 右上角关闭
            # 开始游戏
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click() # 点击 开始游戏
            # 游戏余额不足 请充值,截屏
            self.myScreenshot("HBBDX_gameBalanceLackingPlsRecharge",180, 0, 1080, 1500,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/close").click()
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/exit_game").click()
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/negative").click()

    def HBBDXstartGame(self):
        # C3-2，红包比大小开始游戏后，检查余额及数据库余额
        # 后台数据库重置 50元
        # 修改redis中修改commission_residue, t_user中commission_residue
        varCommission_residue = 5000
        self.cur.execute('select id from t_user where username="%s" order by id desc' % (myPhone))
        data0 = self.cur.fetchone()
        self.cur.execute('update t_user set commission_residue=%s where id=%s' % (varCommission_residue,data0[0]))
        self.conn.commit()
        pp = "t_user:id:"+str(data0[0])
        r = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        r.hset(pp,"Commission_residue",varCommission_residue)

        # 进入游戏
        self.driver.find_element_by_id("com.mowin.tsz:id/button").click()  # 点击 进入游戏
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click() # 点击 开始游戏
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/account_balance_icon").click() # 点击 余额支付
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount_hint").send_keys("30")
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click() # 点击 确定
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click() # 点击 知道了
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click() # 点击 开始游戏


        sleep(121212)
          # # 点击 充值游戏余额 并截屏  ,注:截屏中现金余额 = 100.00
            # self.driver.swipe(300, 750, 300, 750, 500); # 点击 充值游戏余额
            # sleep(2)
            # img = "rechargegameamount"
            # compareResult = self.comparePic(Folder_Screenshot + 'big_' + img + '.png',Folder_Screenshot + 'org_' + img + '.png',160, 0, 1080, 1920)
            # if compareResult > 1:
            #      print "Err,C3-2," + img + compareResult + ".png!"
            #      self.driver.save_screenshot(Folder_Errscreenshot + compareResult + ".png")
            # elif compareResult == 0:
            #      print "Created,C3-2,org_" + img + ".png"
            #
            # # 充值游戏余额浮层中 , 点击 余额支付 并截屏
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/account_balance_icon").click()
            # sleep(2)
            # img = "balancepay"
            # compareResult = self.comparePic(Folder_Screenshot + 'big_' + img + '.png',Folder_Screenshot + 'org_' + img + '.png',160, 0, 1080, 1920)
            # if compareResult > 1:
            #      print "Err,C3-2," + img + compareResult + ".png!"
            #      self.driver.save_screenshot(Folder_Errscreenshot + compareResult + ".png")
            # elif compareResult == 0:
            #      print "Created,C3-2,org_" + img + ".png"
            #
            # sleep(2)
            # cashAmount = self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/account_balance").text
            # cashAmount = cashAmount.split("￥")
            # print cashAmount[1]
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/close").click() # 关闭 充值游戏余额浮层
            # myAcount = gameAmount + cashAmount
            # if myAcount == "0.00" or myAcount < "10.00":
            #     # 修改redis中修改commission_residue, t_user中commission_residue
            #     varCommission_residue = 10000
            #     self.cur.execute('select id from t_user where username="%s" order by id desc' % (myPhone))
            #     data0 = self.cur.fetchone()
            #     self.cur.execute('update t_user set commission_residue=%s where id=%s' % (varCommission_residue,data0[0]))
            #     self.conn.commit()
            #     pp = "t_user:id:"+str(data0[0])
            #     r = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
            #     r.hset(pp,"Commission_residue",varCommission_residue)

        # 点击 充值游戏余额 并截屏  ,注:截屏中现金余额 = 100.00
        self.driver.swipe(300, 750, 300, 750, 500); # 点击 充值游戏余额
        sleep(2)
        img = "rechargegameamount"
        compareResult = self.comparePic(Folder_Screenshot + 'big_' + img + '.png',Folder_Screenshot + 'org_' + img + '.png',160, 0, 1080, 1920)
        if compareResult > 1:
             print "Err,C3-2," + img + compareResult + ".png!"
             self.driver.save_screenshot(Folder_Errscreenshot + compareResult + ".png")
        elif compareResult == 0:
             print "Created,C3-2,org_" + img + ".png"

        # 充值游戏余额浮层中 , 点击 余额支付 并截屏
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/account_balance_icon").click()
        sleep(2)
        img = "balancepay"
        compareResult = self.comparePic(Folder_Screenshot + 'big_' + img + '.png',Folder_Screenshot + 'org_' + img + '.png',160, 0, 1080, 1920)
        if compareResult > 1:
             print "Err,C3-2," + img + compareResult + ".png!"
             self.driver.save_screenshot(Folder_Errscreenshot + compareResult + ".png")
        elif compareResult == 0:
             print "Created,C3-2,org_" + img + ".png"



        xx=gamebalance.split("￥") #游戏余额: ￥50.00
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").click()
        sleep(1)
        # x = self.driver.get_window_size()['width']
        # y = self.driver.get_window_size()['height']
        # print x
        # print y
        if float(xx[1])>= 40.00:
            # 余额退回我的钱包
            sleep(2)
            self.driver.swipe(300, 850, 300, 850, 500); # 点击 余额退回我的钱包
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount_hint").send_keys("20")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            chongzhitishi=self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/message").text
            if chongzhitishi<>"20.00元游戏余额已成功退回到你的钱包余额账户内。": print "Err,余额退回我的钱包!"
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            sleep(3)
            # 检查 游戏余额是否减掉20元
            gamebalance = self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").text # 获取游戏余额
            yy=gamebalance.split("￥")
            if float(yy[1])<>(float(xx[1])-20.00):print "Err,余额退回后计算错误!"
        elif float(xx[1])>= 10.00:
            print "Info, 游戏金额超过10元,可玩游戏"

            # # 检查是否是体验游戏
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click()
            # # 游戏体验已结束, 进入正式游戏试试身手吧~
            # # com.mowin.tsz.thanthesize:id/message

        elif float(xx[1])>5.00 and float(xx[1])<10.00:
            print "Warning, 游戏金额不足10元,正在充值!"
            # 点击 开始游戏 进行充值
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click()
            sleep(2)
            self.driver.swipe(300, 750, 300, 750, 500); # 点击 充值游戏余额
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance_recharge").click() # 余额支付
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount_hint").send_keys("1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            chongzhitishi=self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/message").text
            if chongzhitishi<>"已成功充值1.00元游戏余额, 快进入游戏试试手气吧。": print "Err,充值游戏余额!"
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            sleep(3)
            # 检查 游戏余额是否加1元
            gamebalance = self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").text # 获取游戏余额
            zz=gamebalance.split("￥")
            if float(zz[1])<>(float(xx[1])+1.00):print "Err,充值游戏余额后后计算错误!"
        elif float(xx[1])<5.00 :
            self.driver.swipe(300, 750, 300, 750, 500); # 点击 充值游戏余额
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance_recharge").click() # 余额支付
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount_hint").send_keys("1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            chongzhitishi=self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/message").text
            if chongzhitishi<>"已成功充值1.00元游戏余额, 快进入游戏试试手气吧。": print "Err,充值游戏余额!"
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            sleep(3)
            # 检查 游戏余额是否加1元
            gamebalance = self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").text # 获取游戏余额
            zz=gamebalance.split("￥")
            if float(zz[1])<>(float(xx[1])+1.00):print "Err,充值游戏余额后后计算错误!"

    # 我
    def dev_me(self):
    # 我
        self.TestcaseModule()
    def me2(self):
        # 我 打开app,点击我,跳到登录页面,登录后跳到 我 页面,检查我 页面上标题
        # 检查 我 标题
        self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click()
        self.userLogin()
        if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"我":print "Err,C1-1,我标题文字!"
        # 检查私信及连接
        if self.driver.find_element_by_id("com.mowin.tsz:id/private_msg").text<>u"私信":print "Err,C1-1,私信标题!"
        if self.isElement("com.mowin.tsz:id/private_msg")==True:
            self.driver.find_element_by_id("com.mowin.tsz:id/private_msg").click()
            # 私信页面, 检查标题\内容
            if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"私信":print "Err,C1-1,私信文字!"

            # 私信 - 检查头像
            if self.isElement("com.mowin.tsz:id/thumb_private")<>True:print "Err，C1-1,私信-头像 不存在!"
            # 私信 - 检查 138****1115的红包群 页面返回按钮,标题
            # 返回按钮
            if self.isElement("com.mowin.tsz:id/back")<>True:print "Err，C1-1,私信-红包群信息-返回按钮 不存在!"
            # 标题
            if self.isElement("com.mowin.tsz:id/nick_name")==True:
                text_actual= partmyPhone + "的红包群"
                if self.driver.find_element_by_id("com.mowin.tsz:id/nick_name").text<>text_actual:print "Err,C1-1,私信-'" + partmyPhone + "的红包群'文字!"
                self.driver.find_element_by_id("com.mowin.tsz:id/private_layout").click()
            else:
                 print "Err，C1-1,私信-"+ partmyPhone +"的红包群 不存在!"

            # 私信 - 138****1115的红包群页面,检查返回按钮\标题\群成员Icon连接\内容=点击右上角，选择群成员进行私信
            # 检查返回按钮
            if self.isElement("com.mowin.tsz:id/back")<>True:print "Err，C1-1,私信-"+partmyPhone+"的红包群-返回按钮 不存在!"
            # 检查标题
            text_title = partmyPhone+"的红包群"
            if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>text_title:print "Err,C1-1,'" +partmyPhone + "的红包群'标题!"
            # 检查 内容 = 点击右上角，选择群成员进行私信
            if self.driver.find_element_by_id("com.mowin.tsz:id/no_data_layout").text<>u"点击右上角，选择群成员进行私信":print "Err,C1-1,私信-'"+partmyPhone+"红包群'内 文字!"
            # 检查 右上角 群成员icon,并点击.
            self.driver.find_element_by_xpath("//android.widget.ImageView[contains(@index,2)]").click()

            # 私信 - 红包群信息页面 ,检查 返回按钮\标题\头像\电话号码\群主\所有组成员 = 全部群成员(1)
            if self.isElement("com.mowin.tsz:id/back")<>True:print "Err，C1-1,私信-红包群信息-返回按钮 不存在!"
            # 检查标题
            if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"红包群信息":print "Err,C1-1,私信-红包群信息 标题文字错误!"

            # 检查头像
            if self.isElement("com.mowin.tsz:id/head_thumb")<>True:print "Err，C1-1,私信-红包群信息-头像 不存在!"
            # 检查电话号码
            if self.driver.find_element_by_id("com.mowin.tsz:id/name").text<>partmyPhone:print "Err,C1-1,私信-红包群信息-"+partmyPhone+"文字错误!"
            # 检查群主
            if self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'群主')]").text<>u"群主":print "Err,C1-1,私信-红包群信息-群主 文字错误!"
            # 检查 全部群成员(1)
            if self.isElement("com.mowin.tsz:id/all_group_member")==True:
                 if self.driver.find_element_by_id("com.mowin.tsz:id/all_group_member").text<>u"全部群成员(1)":print "Err,C1-1,私信-红包群信息-全部群成员(1) 文字错误!"
                 # 私信 - 群成员(1) ,检查 返回按钮\标题\搜索框\头像\昵称
                 self.driver.find_element_by_id("com.mowin.tsz:id/all_group_member").click()
                 if self.isElement("com.mowin.tsz:id/back")<>True:print "Err，C1-1,私信-群成员(1)-返回按钮 不存在!"
                 # 检查标题
                 if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"群成员(1)":print "Err,C1-1,私信-红包群信息 标题文字错误!"
                 # 检查 搜索框
                 if self.isElement("com.mowin.tsz:id/search_edit")==True:
                      if self.driver.find_element_by_id("com.mowin.tsz:id/search_edit").text<>u"搜索":print "Err,C1-1,私信-红包群信息-搜索 文字错误!"
                 else:
                      print "Err，C1-1,私信-群成员(1)-搜索框 不存在!"
                 # 检查 头像
                 if self.isElement("com.mowin.tsz:id/thumb")<>True:print "Err，C1-1,私信-群成员(1)-头像 不存在!"
                 # 检查 昵称
                 if self.isElement("com.mowin.tsz:id/nick_name")==True:
                       if self.driver.find_element_by_id("com.mowin.tsz:id/nick_name").text<>partmyPhone:print "Err,C1-1,私信-红包群信息-昵称 文字错误!"
                 else:
                    print "Err，C1-1,私信-群成员(1)-昵称 不存在!"
                 self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
            else:
                 print "Err，C1-1,私信-红包群信息-全部群成员(1) 文字不存在!"

            self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
            self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
            self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
        else:
            print "Err,C1-1 私信icon!"
    def personInfo(self,varNickname,varSign,varArea):
         #C1-2,我的页面头部个人信息，检查头像、昵称、签名、二维码
         sleep(3)
         # 检查 头像
         if self.isElement("com.mowin.tsz:id/thmub")<>True:print "Err，C1-2,我-头像 不存在!"
         # 检查 昵称
         if self.isElement("com.mowin.tsz:id/name")==True:
              text_Search=self.driver.find_element_by_id("com.mowin.tsz:id/name").text
              if partmyPhone<>text_Search:
                  print "Err,C1-2,我-昵称 错误!"
         else:
             print "Err，C1-2,我-昵称 不存在!"
         # 检查 签名
         if self.isElement("com.mowin.tsz:id/sign")==True:
              text_Sign=self.driver.find_element_by_id("com.mowin.tsz:id/sign").text
              if text_Sign<>"编辑个性签名" :
                  print "Err,C1-2,我-签名 错误!"
         else:
             print "Err，C1-2,我-签名 不存在!"
         # 检查 二维码
         if self.isElement("com.mowin.tsz:id/qr_code")==True:
             pass
              # self.driver.find_element_by_id("com.mowin.tsz:id/qr_code").click()
              # sleep(2)
              # self.driver.tap([(200,200),(200,200)],500)
         else:
             print "Err，C1-2,我-个人信息-二维码 不存在!"

         # 编辑个人信息,检查返回按钮\标题\昵称\个性签名\性别\常住地\手机号
         self.driver.find_element_by_id("com.mowin.tsz:id/user_name_and_gender_layout").click()
         # 检查 返回按钮
         if self.isElement("com.mowin.tsz:id/back")<>True:print "Err，C1-2,个人信息-返回按钮 不存在!"
         # 检查 标题文字
         if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"个人信息":print "Err,C1-2,个人信息-标题文字!"
         # 检查 昵称文字 和 昵称 ,修改昵称
         if self.driver.find_element_by_id("com.mowin.tsz:id/nick_title").text<>u"昵称":print "Err，C1-2,个人信息-昵称文字!"
         if self.driver.find_element_by_id("com.mowin.tsz:id/nick_name").text<>partmyPhone:print "Err，C1-2,个人信息-昵称!"
         self.driver.find_element_by_id("com.mowin.tsz:id/nick_name").click()
         # 修改昵称
         if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"昵称":print "Err，C1-2,个人信息-昵称-标题文字!"
         self.driver.find_element_by_class_name("android.widget.EditText").clear()
         self.driver.find_element_by_class_name("android.widget.EditText").send_keys(varNickname)
         self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'保存')]").click()
         if self.driver.find_element_by_id("com.mowin.tsz:id/nick_name").text<>varNickname:print "Err，C1-2,个人信息-昵称修改后!"

         # 检查 个人签名文字 和 个人签名
         if self.driver.find_element_by_id("com.mowin.tsz:id/sign_title").text<>u"个性签名":print "Err，C1-2,个人信息-个性签名文字!"
         if self.driver.find_element_by_id("com.mowin.tsz:id/sign").text<>u"编辑个性签名":print "Err，C1-2,个人信息-个性签名!"
         self.driver.find_element_by_id("com.mowin.tsz:id/sign").click()
         # 修改个性签名
         if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"个性签名":print "Err，C1-2,个人信息-个人签名-标题文字!"
         self.driver.find_element_by_xpath("//android.widget.EditText[contains(@index,0)]").send_keys(varSign)
         self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'保存')]").click()
         if self.driver.find_element_by_id("com.mowin.tsz:id/sign").text<>varSign:print "Err，C1-2,个人信息-个性签名修改后!"

         # 检查 性别文字 和 性别
         if self.driver.find_element_by_id("com.mowin.tsz:id/gender_title").text<>u"性别":print "Err，C1-2,个人信息-性别文字!"
         text_sex=self.driver.find_element_by_id("com.mowin.tsz:id/gender").text
         if text_sex<>u"男":print "Err，C1-2,个人信息-性别!"
         self.driver.find_element_by_id("com.mowin.tsz:id/gender").click()
         # 修改性别
         if text_sex=="男":
             self.driver.find_element_by_id("com.mowin.tsz:id/famale").click()
         else:
             self.driver.find_element_by_id("com.mowin.tsz:id/male").click()
         text_sex=self.driver.find_element_by_id("com.mowin.tsz:id/gender").text
         if text_sex<>"女":print "Err，C1-2,个人信息-性别修改后!"

         # 检查 常住地文字 和 手机号
         if self.driver.find_element_by_id("com.mowin.tsz:id/always_place_title").text<>u"常驻地":print "Err，C1-2,个人信息-常驻地文字!"
         if self.driver.find_element_by_id("com.mowin.tsz:id/always_place").text<>u"上海":print "Err，C1-2,个人信息-常住地!"
         self.driver.find_element_by_id("com.mowin.tsz:id/always_place").click()
         # 修改地区
         text_area=self.driver.find_elements_by_id("com.mowin.tsz:id/city_name")
         for t_area in text_area:
             if t_area.get_attribute("text")==varArea:
                 t_area.click()
                 break
         sleep(3)
         if self.driver.find_element_by_id("com.mowin.tsz:id/always_place").text<>varArea:print "Err，C1-2,个人信息-常住地修改后!"
         # 检查 手机号文字 和 手机号
         if self.driver.find_element_by_id("com.mowin.tsz:id/phone_title").text<>u"手机号":print "Err，C1-2,个人信息-手机号文字!"
         if self.driver.find_element_by_id("com.mowin.tsz:id/phone").text<>partmyPhone:print "Err，C1-2,个人信息-手机号!"

         self.driver.find_element_by_id("com.mowin.tsz:id/back").click()

         # 检查 我 页面中个人信息修改后的结果 ,检查 昵称\个性签名
         # 检查 昵称修改后
         if self.driver.find_element_by_id("com.mowin.tsz:id/name").text<> varNickname:print "Err,C1-2,我-个人信息-昵称修改后!"
         # 检查 个性签名修改后
         if self.driver.find_element_by_id("com.mowin.tsz:id/sign").text<> u"个性签名: "+varSign :print "Err,C1-2,我-个人信息-个性签名修改后!"

         # 编辑个人信息,检查返回按钮\标题\昵称\个性签名\性别\常住地\手机号
         self.driver.find_element_by_id("com.mowin.tsz:id/user_name_and_gender_layout").click()
         # 恢复 默认昵称\个性签名\性别\常驻地
         # 恢复昵称
         self.driver.find_element_by_id("com.mowin.tsz:id/nick_name").click()
         self.driver.find_element_by_class_name("android.widget.EditText").clear()
         self.driver.find_element_by_class_name("android.widget.EditText").send_keys(partmyPhone)
         self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'保存')]").click()
         # 恢复个性签名
         self.driver.find_element_by_id("com.mowin.tsz:id/sign").click()
         self.driver.find_element_by_xpath("//android.widget.EditText[contains(@index,0)]").clear()
         self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'保存')]").click()
         # 恢复性别
         self.driver.find_element_by_id("com.mowin.tsz:id/gender").click()
         self.driver.find_element_by_id("com.mowin.tsz:id/male").click()
         # 恢复常驻地
         self.driver.find_element_by_id("com.mowin.tsz:id/always_place").click()
         for t_area in text_area:
             if t_area.get_attribute("text")=="上海":
                 t_area.click()
                 break
         self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
    def account(self):
         # 临时 登录
         sleep(3)
         self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click()
         # 截屏 图片对比
         self.driver.save_screenshot('/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/my.png')
         sleep(2)
         img1 = open("/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/my.png", "r")
         img2 = open("/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/mytest.png", "r")
         if img1.read() == img2.read():
            print "ok"
         else:
            print "err"


         self.driver.find_element_by_id("com.mowin.tsz:id/phone_number").send_keys(myPhone)
         self.driver.find_element_by_id("com.mowin.tsz:id/get_mobile_code").click()
         sleep(1)
         self.cur.execute('select verify_code from ta_message where phone=%s order by id desc limit 1' % (myPhone))
         data9 = self.cur.fetchone()
         self.driver.find_element_by_id("com.mowin.tsz:id/mobile_code").send_keys(data9[0])
         self.driver.find_element_by_id("com.mowin.tsz:id/login").click()
         sleep(2)




         #C1-3，钱包－账户余额
         self.driver.find_element_by_id("com.mowin.tsz:id/my_wallet").click()
         # 钱包 - 检查 返回按钮\标题\账户明细\账户余额
         # 检查返回按钮
         if self.isElement("com.mowin.tsz:id/back")<>True:print "Err，C1-3,钱包-返回按钮 不存在!"
         # 检查标题
         if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"我的钱包":print "Err,C1-3,钱包-我的钱包标题!"
         if self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'账户明细')]").text<>u"账户明细":print "Err,C1-3,钱包-账户明细文字!"

         # 检查账户明细 并点击.
         self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'账户明细')]").click()
         # 账户明细, 检查返回\标题
         # 检查返回按钮
         if self.isElement("com.mowin.tsz:id/back")<>True:print "Err，C1-3,钱包-账户明细-返回按钮 不存在!"
         # 检查标题
         if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"账户明细":print "Err,C1-3,钱包-账户明细标题!"
         # # 默认第一次时,显示 唐僧icon\脚icon
         # if self.isElement("com.mowin.tsz:id/progress")<>True:print "Err，C1-3,钱包-账户明细-唐僧icon 不存在!"
         # if self.isElement("com.mowin.tsz:id/image")<>True:print "Err，C1-3,钱包-账户明细-脚icon 不存在!"
         # if self.driver.find_element_by_id("com.mowin.tsz:id/text_hint").text<>u"暂无账户明细":print "Err,C1-3,钱包-账户明细内容!"
         self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
         sleep(3)
         # 检查 账户余额文字 和 金额
         if self.driver.find_element_by_id("com.mowin.tsz:id/mywallet_text").text<>u"账户余额":print "Err,C1-3,钱包-账户余额文字!"
         if self.driver.find_element_by_id("com.mowin.tsz:id/mywalleny_allmoney").text<>"0.00":print "Err,C1-3,钱包-账户余额!"
         if self.driver.find_element_by_id("com.mowin.tsz:id/accumulated_earnings_text").text<>u"红包累计收益 ¥":print "Err,C1-3,钱包-红包累计收益 ¥文字!"
         if self.driver.find_element_by_id("com.mowin.tsz:id/accumulated_earnings").text<>"0.00":print "Err,C1-3,钱包-红包累计收益 ¥!"

         # WEB平台充值并审核, 检查 app端账户余额是否更新.
         # 步骤,1先获取app端账户余额,2其次WEB端充值审核,3最后app端检查账户余额.
         # 步骤1,
         app_account = self.driver.find_element_by_id("com.mowin.tsz:id/mywalleny_allmoney").text
         # 步骤2,
         self.b_login()
         varAmount=self.b_chongzhi("10","99")  # 默认当前myPhone手机号
         sleep(2)
         self.b_close()
         # 步骤3,
         self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
         self.driver.find_element_by_id("com.mowin.tsz:id/my_wallet").click()
         app_account_revised = self.driver.find_element_by_id("com.mowin.tsz:id/mywalleny_allmoney").text
         if (float(app_account)+float(varAmount))<>float(app_account_revised):print "Err,C1-3,钱包-系统充值后账户余额![原账户余额:"+app_account +",充值金额:"+varAmount+",最新账户余额:"+app_account_revised+"]"

         # 立即提现
         if self.isElement("com.mowin.tsz:id/withdrawal_button")<>True:
             print "Err，C1-3,钱包-立即提现 不存在!"
         else:
         #  self.isElement("com.mowin.tsz:id/withdrawal_button").click()
            pass
            # 立即提现
            # 在Sit2进行充值


         self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
    def web_chongzhi(self):
           # 打开sit2,进行充值操作
           self.browser.get("http://sit2.88uka.com/admin/finance/userExperienceList.do")
           self.browser.find_element_by_id("phoneValue").send_keys("13816101118")
           self.browser.find_elements_by_class_name("savebtn").click()



           allhandles=self.browser.window_handles
           for handle in allhandles:
               if handle != self.nowhandle:
                   self.browser.switch_to_window(handle)
           sleep(3)
           self.browser.maximize_window()
           # 商品标题
           self.browser.find_element_by_id("itemTitle").send_keys(GoodsName)
           # 商品副标题
           self.browser.find_element_by_id("phoneValue").send_keys("13816101118")
           # 参考价格
           self.browser.find_element_by_id("refPrice").send_keys(u"12.44")
           self.browser.find_element_by_id("goods_c_a").click()
           xx=self.browser.find_elements_by_class_name("select_cat")
           for x1 in xx:
               if x1.text==u"好货优先":
                   x1.click()
           # 保存
           self.browser.find_element_by_id("categorSelect").click()




    # 安装
    def install(self):
        self.TestcaseModule()
    def UninstallAPK(self):
        sleep(3)
        xx=self.driver.is_app_installed("cn.jihaojia")
        if xx==True:
           os.system('adb uninstall cn.jihaojia')
        else:
           pass
    def InstallAPK(self,ApkName):
        sleep(6)
        os.system('adb install ./apk/'+ApkName)
        sleep(3)
        self.driver.start_activity("cn.jihaojia",'cn.jihaojia.activity.GuidanceActivity')
        sleep(3)
        if self.isElement("cn.jihaojia:id/fuck")<>True:
            print "Err,安装,引导页未显示!"
        self.driver.swipe(1000, 600, 100, 600,500)
        sleep(2)
        self.driver.swipe(1000, 600, 100, 600,500)
        sleep(2)
        self.driver.swipe(1000, 600, 100, 600,500)
        sleep(2)
        self.driver.swipe(1000, 600, 100, 600,500)
        sleep(3)
        if self.isElement("cn.jihaojia:id/item_image")<>True:
            print "Err,安装,引导页未滑到最后Skip按钮不存在!"
        else:
            self.driver.find_element_by_id("cn.jihaojia:id/item_image").click()
    ##########################################################################################


if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(Tsz_2_3) # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1) # 执行测试

