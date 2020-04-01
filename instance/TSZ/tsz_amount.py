# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2016-7-11
# Description: android自动化测试平台(app金额用例.docx)
#****************************************************************
# 前置条件:
# 1, 先登录微信, 账户:happyjinhao , 秘密:jinhao123

# C1,（普通用户）账户余额发送推广红包
# C2,(代理商户）账户余额发送推广红包
# C3,（普通用户）账户余额发送图文
# C4,（大咖用户）账户余额发送推广红包
# C5,（大咖用户）账户余额发送图文(依赖于C1-3)

import os,sys,unittest,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis
from resource.web import *    #引入web模块中的函数
from resource.source import *
from appium import webdriver
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
import time,Image,ImageChops

#****************************************************************
# 参数化
varRandom4="".join(myfunc(4))

varPhone="13816107078"

varNickName = varPhone[0:3] + "****" + varPhone[7:] # 昵称

ProjectPath = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ"

ExcelFile = "/excel/tsz_amount.xls" #

ReportHtml = "/report/testreport_amount.html" # TestReport文件

ScreenshotFolder="/screenshot/"  #org\curr 截屏

ErrorScreenshotFolder = "/errscreenshot/"  # 错误截屏

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
#****************************************************************

class Tsz_amount(unittest.TestCase):

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
        self.conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
        self.cur = self.conn.cursor()
        self.conn.set_character_set('utf8')
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')
        self.cur.execute('show tables') # 获取数据库所有表名
        self.ukardwebTable=self.cur.fetchall()

        # 检查 t_user_thirdInfo 中belongName = john 的记录,并删除
        self.cur.execute('select count(id),userId from t_user_thirdInfo where belongName="John" order by id desc')
        tblTmp0 = self.cur.fetchone()
        if tblTmp0[0]==1:
            self.cur.execute('delete from  t_user_thirdInfo where userId=%s' %(tblTmp0[1]))
            self.conn.commit()
        sleep(10)

        # 检查 t_user 中是否存在此号码,没有则先登录
        self.cur.execute('select count(id) from t_user where username="%s" order by id desc' % (varPhone))
        tblTmp1 = self.cur.fetchone()
        if tblTmp1[0]<>1:    # 手机号表中不存在
             self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click() # 我
             sleep(3)
             flag = False
             try:
                self.driver.find_element_by_id("com.mowin.tsz:id/phone_number")
                flag = True
             except :
                flag = False
             if flag==False :
                 self.driver.find_element_by_id("com.mowin.tsz:id/settings").click() # 点击 设置
                 self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'退出登录')]").click()
                 self.driver.find_element_by_id("com.mowin.tsz:id/positive").click() # 退出登录
             self.driver.find_element_by_id("com.mowin.tsz:id/phone_number").send_keys(varPhone)
             self.driver.find_element_by_id("com.mowin.tsz:id/get_mobile_code").click()
             sleep(4)

             # 获取验证码
             self.conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
             self.cur = self.conn.cursor()
             self.cur.execute('select verify_code from ta_message where phone=%s order by id desc limit 1' % (varPhone))
             tblTmp9 = self.cur.fetchone()
             self.driver.find_element_by_id("com.mowin.tsz:id/mobile_code").send_keys(tblTmp9[0])
             self.driver.find_element_by_id("com.mowin.tsz:id/login").click()
             sleep(2)

             # 第三方账户绑定
             if self.driver.find_element_by_id("com.mowin.tsz:id/title").text=="第三方账号绑定" :
                 self.driver.swipe(100,200,100,200,500) # 点击 右上角X


        # 获取用户ID
        self.conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
        self.cur = self.conn.cursor()
        self.cur.execute('select id from t_user where username="%s" order by id desc' % (varPhone))
        tblTmp7 = self.cur.fetchone()
        self.myuserID=tblTmp7[0]

        # 获取群ID
        self.conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
        self.cur = self.conn.cursor()
        self.cur.execute('select id from t_redgroup_baseinfo where userId="%s" order by id desc ' % (tblTmp7[0]))
        tblTmp8 = self.cur.fetchone()
        self.mygroupID = tblTmp8[0]

        connGame= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='game', port=3306, use_unicode=True)
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

        self.fname=ExcelFile
        self.bk = xlrd.open_workbook(ExcelFile,formatting_info=True)
        self.newbk=copy(self.bk)
        styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
        styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')
        styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
        self.styleBlue=styleBlue
        self.styleGray25=styleGray25
        self.styleRed=styleRed

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

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
                   # page << p("<font color=red>[Error]</font> ",self.sheetTestCase.cell_value(l,3))  #输出测试用例

         # 是否生成VARHTMLFILE文档, 1=生成一个testreport.html; 2=生成多个带时间的html,如testreport20161205121210.html
         # if self.sheetMain.cell_value(1,6) == 1:
         #   page.printOut(VARHTMLFILE)
         #   sleep(4)
         #   # #send Email
         #   if self.sheetMain.cell_value(1,5)=="Y":
         #      self.sendemail(VARHTMLFILE)
         # elif self.sheetMain.cell_value(1,6) == 2:
         #   page.printOut(VARHTMLFILEtimestamp)
         #   # #send Email
         #   if self.sheetMain.cell_value(1,5)=="Y":
         #      self.sendemail(VARHTMLFILEtimestamp)


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
    def userLogin(self):
        # Common 用户第一次登录, 手机快速登录 页面,
        # ===== EXcel ID0 -ID9 参数用法 ====
        # for i in range(0,len(self.str_list)): # 遍历参数
        #     print self.str_list[i]
        # print self.str_list[0]  # 输出第一个参数
        # print type(self.str_list[1]) # 输出类型
        # [手机快速登录]
        # self.driver.find_element_by_id(self.str_list[1]).send_keys(varPhone)
        # self.driver.find_element_by_id(self.str_list[2]).click()
        # 等同于下面2句, 上面用了Excel中的参数1\2
        if self.isElement("com.mowin.tsz:id/phone_number")==True:
            sleep(2)
            self.driver.find_element_by_id("com.mowin.tsz:id/phone_number").send_keys(varPhone)
            self.driver.find_element_by_id("com.mowin.tsz:id/get_mobile_code").click()
            sleep(2)
            # 获取验证码
            self.cur.execute('select verify_code from ta_message where phone=%s order by id desc limit 1' % (varPhone))
            data9 = self.cur.fetchone()
            self.driver.find_element_by_id("com.mowin.tsz:id/mobile_code").send_keys(data9[0])
            self.driver.find_element_by_id("com.mowin.tsz:id/login").click()
            sleep(2)
    def myScreenshot(self,img,startX,startY,endX,endY,casenum):
        # org截屏
        # self.myScreenshot("weixinpay",160, 0, 1080, 1920,"C3-1")
        sleep(2)
        compareResult = self.comparePic(ScreenshotFolder + 'big_' + img + '.png',ScreenshotFolder + 'org_' + img + '.png',startX,startY,endX,endY)
        if compareResult > 1:
             print "Err," + casenum + "," + img + compareResult + ".png!"
             self.driver.save_screenshot(ErrorScreenshotFolder + img + compareResult + ".png")
        elif compareResult == 0:
             print "Created," + casenum + ",org_" + img + ".png"

    # =================== [app] ===================
    def drv_amount(self):
        print "\n"
        # self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click() # 我
        # self.userLogin()
        sleep(2)
        self.TestcaseModule()

    def accountRedbonusUser(self):
        #  C1,（普通用户）账户余额发送推广红包
        # 检查金额是否被正常扣除
        # 操作步骤：点击首页-设置广告内容-绑定红包炸弹-塞钱进红包-选择分享渠道(同一批次多个渠道)
        # 涉及数据库:
        # 1、t_user,commission_residue 字段减去发红包的金额
        # 2、t_extension_channel_redPool,redState=1【已分享】、redSumAmount 记录红包总金额
        # 3、t_extension_channel,redState=1【正常】，channelRedSumAmount字段记录该渠道的红包总金额，channelRedAmount字段记录渠道红包单个金额
        # 4、t_user_withdraw,w_state=1【提现成功】，check_state=1【审核成功】，is_valid=1【有效】，amount字段记录红包总金额，charge=0[手续费]
        # App变化：
        # 1、钱包-我的钱包-账户余额减去发红包的金额（取redis用户金额）
        # 2、立即提现-可提现金额减去发红包金额
        # Redis变化：
        # 1、t_user文件下该用户commission_residue减去发红包的金额
        # 2、t_extension_channel_redPool文件下redSumAmount红包总金额
        # 3、t_extension_channel文件下channelRedSumAmount红包总金额，channelRedAmount红包单个金额

        # 默认账户余额充值50元
        r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        r2.hset("t_user:id:" + str(self.myuserID),"Commission_residue","5000")
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('update t_user set Commission_residue = 5000 where id = %s ' %(self.myuserID))
        conn.commit()
        sleep(3)

        # APP业务逻辑,发红包发广告
        self.driver.find_element_by_id("com.mowin.tsz:id/send_red_packet_layout").click() # 点击 发红包
        self.driver.find_element_by_id("com.mowin.tsz:id/extension_title").send_keys(u"alibaba的广告品牌")
        sleep(2)
        self.driver.find_element_by_id("com.mowin.tsz:id/photo").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/gallery").click()
        varImages=self.driver.find_elements_by_id("com.mowin.tsz:id/image")
        for i in varImages:
            i.click()
            break
        sleep(2)
        self.driver.swipe(1000,200,1000,200,500) # 确定
        self.driver.find_element_by_id("com.mowin.tsz:id/extension_link").send_keys(u"www.163.com")
        self.driver.find_element_by_id("com.mowin.tsz:id/bind_red_packet").click()  # 设置完成,去绑红包炸弹
        self.driver.find_element_by_id("com.mowin.tsz:id/redpacket_et_count").send_keys("1") # 红包炸弹个数
        self.driver.find_element_by_id("com.mowin.tsz:id/redpacket_et_amount_hint").send_keys("1") #红包总金额
        varAccountPay = self.driver.find_element_by_id("com.mowin.tsz:id/account_balance").text # 检查选择支付方式栏下,余额支付右侧金额值
        if varAccountPay==u"¥50.00":print "OK,C1-1,发红包发广告,设置你的广告内容,绑红包炸弹,余额支付=50元"
        else:print "Error,C1-1,发红包发广告,设置你的广告内容,绑红包炸弹,余额支付<>50元"
        self.driver.find_element_by_id("com.mowin.tsz:id/account_balance_checkbox").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/send_red_packet").click() # 塞钱进红包
        sleep(2)
        self.driver.find_element_by_id("com.mowin.tsz:id/share_red_packet").click() # 红包炸弹已做好,发红包

        # 选择渠道
        # 1,朋友圈
        self.driver.find_element_by_id("com.mowin.tsz:id/wx_timeline").click() # 朋友圈
        self.driver.find_element_by_id("com.mowin.tsz:id/negative").click() # 温馨提示,系统可自动将此红包炸弹分享到你的红包群里. 点击不需要
        sleep(8)
        # 微信登录,登录后该应用将获得以下权限
        if self.driver.find_element_by_id("android:id/text1").text == "微信登录":
            self.driver.swipe(500,1000,500,1000,500) # 第三方授权 确认登录
            sleep(8)
        self.driver.find_element_by_id("com.tencent.mm:id/eg").click() # 第三方平台, 发送
        print "OK,分享至 - 朋友圈"

        # 2,微信(群)
        self.driver.find_element_by_id("com.mowin.tsz:id/wx_session").click() # 微信群
        # self.driver.find_element_by_id("com.mowin.tsz:id/negative").click() # 温馨提示,系统可自动将此红包炸弹分享到你的红包群里. 点击不需要
        sleep(8)
        # 如用户未登录微信,则登录
        if self.isElement("com.tencent.mm:id/ew")==True:
            self.driver.find_element_by_id("com.tencent.mm:id/ew").send_keys("happyjinhao")
            self.driver.find_element_by_id("com.tencent.mm:id/ew").send_keys("jinhao123")
            self.driver.find_element_by_id("com.tencent.mm:id/b4n").click()
            sleep(8)
            self.driver.swipe(500,1030,500,1030,500) # 微信登录,三藏红包登录后授权公开信息,点击确认登录.
        self.driver.swipe(500,700,500,700,500) # 选择 tsz测试群
        self.driver.find_element_by_id("com.tencent.mm:id/bhe").click() # 分享
        self.driver.find_element_by_id("com.tencent.mm:id/a7b").click() # 返回三藏红包
        print "OK,分享至 - 微信群"

        #  QQ=3525023378 ,会报存在安全问题,而无法登录.
        # # elif varChannel==3: #QQ好友
        # self.driver.find_element_by_id("com.mowin.tsz:id/qq").click() # QQ好友
        # # self.driver.find_element_by_id("com.mowin.tsz:id/negative").click() # 温馨提示,系统可自动将此红包炸弹分享到你的红包群里. 点击不需要
        # self.driver.swipe(500,900,500,900,500) # 选择令狐冲
        # sleep(3)
        # self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogRightBtn").click() # 分享
        # sleep(6)
        # self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogLeftBtn").click() # 返回三藏红包
        #
        #  # elif varChannel==4: #QQ空间
        # self.driver.find_element_by_id("com.mowin.tsz:id/qq_zone").click()
        # self.driver.find_element_by_id("com.tencent.mobileqq:id/ivTitleBtnRightText").click() # 发表
        # sleep(3)
        # if self.isElement("self.driver.find_element_by_id")==True:
        #     self.driver.find_element_by_id("com.tencent.mobileqq:id/name").click()

        # # elif varChannel==5: #微博
        # self.driver.find_element_by_id("com.mowin.tsz:id/weibo").click()
        # sleep(10)
        # if self.isElement("com.sina.weibo:id/bnLogin")==True:
        #     self.driver.find_element_by_id("com.sina.weibo:id/bnLogin").click()
        #     sleep(10)
        # self.driver.find_element_by_id("com.sina.weibo:id/titleSave").click()   # 第三方, 发送

        # 6,抢红包
        self.driver.find_element_by_id("com.mowin.tsz:id/app").click() # 抢红包
        self.driver.find_element_by_id("com.mowin.tsz:id/count").send_keys("1") # 输入红包炸弹数量
        self.driver.find_element_by_id("com.mowin.tsz:id/positive").click() # 发送
        print "OK,分享至 - 抢红包"

        # 7,红包群
        self.driver.find_element_by_id("com.mowin.tsz:id/red_packet_group").click() # 红包群
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 发给谁看,默认全部   点击 发送
        print "OK,分享至 - 红包群"

        # 8,二维码
        if self.isElement("com.mowin.tsz:id/qr_code")==True:
            self.driver.find_element_by_id("com.mowin.tsz:id/qr_code").click() # 二维码
            self.driver.find_element_by_id("com.mowin.tsz:id/positive").click() # 温馨提示,生成二维码后不可再分享至其他平台.是否生成二维码? ,点击确定
            if self.isElement("com.mowin.tsz:id/qr_code")<>True:
                 print "Error,C1-1,生成二维码页面错误"
                 sleep(3)
            self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回后到首页
            print "OK,分享至 - 二维码"
        else:
            sleep(3)
            self.driver.find_element_by_id("com.mowin.tsz:id/close").click()
            self.driver.find_element_by_id("com.mowin.tsz:id/negative").click() # 温馨提示,你确定不再继续向以下平台发红包炸弹了吗? 确定

        # 检查t_user,commission_residue字段减去发红包的金额
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select commission_residue from t_user where id=%s' %(self.myuserID))
        data1 = cur.fetchone()
        if data1[0]==4900:print "OK,C1-2,t_user,commission_residue=4900"
        else: print "Error,C1-2,t_user,commission_residue<>4900"

        # redis,检查 t_user,commission_residue 字段减去发红包的金额
        r3 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        varRedis1=r3.hget("t_user:id:" + str(self.myuserID),"Commission_residue")
        if varRedis1=="4900":print "OK,C1-3,redis,t_user,commission_residue=4900"
        else:print "Error,C1-3,redis,t_user,commission_residue<>4900"

        # 检查 t_extension_channel_redPool,redState=1【已分享】,redSumAmount=100 记录红包总金额
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select count(userId),id from t_extension_channel_redPool where userId=%s and redState=1 and redSumAmount=100' %(self.myuserID))
        data2 = cur.fetchone()
        if data2[0]>=1:print "OK,C1-4,t_extension_channel_redPool,红包总金额1元."
        else: print "Error,C1-4,t_extension_channel_redPool,红包总金额<>1元."

        # 检查 t_extension_channel,redState=1【正常】,channelRedSumAmount=100 该渠道的红包总金额,channelRedAmount=100 渠道红包单个金额
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select count(userId),id from t_extension_channel where userId=%s and extensionRedPoolId=%s and redState=1 and channelRedSumAmount=100 and channelRedAmount=100' %(self.myuserID,data2[1]))
        data3 = cur.fetchone()
        if data3[0]>=1:print "OK,C1-5,t_extension_channel,红包总金额1元."
        else: print "Error,C1-5,t_extension_channel,红包总金额<>1元."

        # 检查 t_user_withdraw,amount=100 红包总金额,charge=0 手续费,w_state=1 提现成功,check_state=1 审核成功,is_valid=1 有效
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select count(id) from t_user_withdraw where user_id=%s and amount=100 and charge=0 and w_state=1 and check_state=1' %(self.myuserID))
        data4 = cur.fetchone()
        if data4[0]>=1:print "OK,C1-6,t_user_withdraw,红包总金额1元."
        else: print "Error,C1-6,t_user_withdraw,红包总金额1元."

        # redis,检查 t_extension_channel_redPool,redSumAmount=100
        varRedis2=r3.hget("t_extension_channel_redPool:" + str(data2[1]),"redSumAmount")
        if varRedis2=="100":print "OK,C1-7,redis,t_extension_channel_redPool,redSumAmount=100"
        else:print "Error,C1-7,redis,t_extension_channel_redPool,redSumAmount<>100"

        # redis,检查 t_extension_channel,channelRedSumAmount=100
        varRedis3=r3.hget("t_extension_channel:" + str(data3[1]),"channelRedSumAmount")
        if varRedis3=="100":print "OK,C1-8,redis,t_extension_channel,channelRedSumAmount=100"
        else:print "Error,C1-8,redis,t_extension_channel,channelRedSumAmount<>100"

        # App变化：
        #  1、钱包-我的钱包-账户余额减去发红包的金额（取redis用户金额）,检查账户明细
        self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click()  # 我
        self.driver.find_element_by_id("com.mowin.tsz:id/my_wallet").click() # 钱包
        varAccountBalance = self.driver.find_element_by_id("com.mowin.tsz:id/mywalleny_allmoney").text
        if varAccountBalance=="49.00":print "OK,C1-9,我,钱包,账户余额=49.00"
        else:print "Error,C1-9,我,钱包,账户余额<>49.00"
        # 检查 账户明细 金额.
        self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'账户明细')]").click()
        varAccountDetailsCash =self.driver.find_elements_by_id("com.mowin.tsz:id/money")
        d_list=[]
        e_list=[]
        for var_AccountDetailsCash in varAccountDetailsCash:
            d_list.append(var_AccountDetailsCash.text)
        for var_AccountDetailsCash in varAccountDetailsCash:
             if var_AccountDetailsCash.text<>u"-1.00元":
                 print "Error,C1,账户明细 - 金额为" + str(var_AccountDetailsCash.text)
             break
        sleep(2)
        # 账户明细 - 明细类型
        varAccountDetailsType = self.driver.find_elements_by_id("com.mowin.tsz:id/item_accountdetail_hint")
        for var_AccountDetailsType in varAccountDetailsType:
            e_list.append(var_AccountDetailsType.text)
        for var_AccountDetailsType in varAccountDetailsType:
             if var_AccountDetailsType.text<>u"余额发送推广红包":
                 print "Error,C1,账户明细 - 类型为" + str(var_AccountDetailsType.text)
             break
        sleep(2)
        # print str(e_list[0]) +"," +str(d_list[0])
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回

        #  2、立即提现-可提现金额减去发红包金额
        self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_button").click()
        varGetCash = self.driver.find_element_by_id("com.mowin.tsz:id/with_drawal_balance").text # 可提现金额
        if varGetCash == u"¥49.00":print "OK,C1-10,我,钱包,立即提现=49.00"
        else:print "Error,C1-10,我,钱包,立即提现<>49.00"
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回
        self.driver.find_element_by_id("com.mowin.tsz:id/home_tab").click() # 返回到首页

        # 删除t_user_thirdInfo,删除与手机号关联的3条记录
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('delete from  t_user_thirdInfo where userId=%s' %(self.myuserID))
        conn.commit()
        print "============================================================="

    def accountRedbonusAgent(self):
        # C2,(代理商户）账户余额发送推广红包
        # 1、操作步骤：系统后台-代理商发展商户-新建合作商户-点击首页-设置广告内容-绑定
        #                   红包炸弹-塞钱进红包-选择分享渠道（二维码）
        #    前置条件,发红包金额1元,代理商:john代理商, 与公司分成比例2% , 代理商发展商户佣金6%
        # 2, 如果是大咖用户则不生产代理商与公司总收益,否则计算公式: 1元(10),100-100*0.06=94 ,0.06*0.02结果0.0012,所以等于0.
        #  t_extension_chaneel,channelRedSumAmount =94 , channelRedAmount=94 ,channel=4
        # 数据变化：
        #      1、t_user表commission_residue字段减去发红包的金额
        #      2、t_extension_channel_redPool表redState状态为1【已分享】、redSumAmount字段
        #         记录红包总金额（发送的红包金额减去公司分层的佣金）
        #      3、t_extension_channel表redState状态为1【正常】，channelRedSumAmount 字段记录
        #         该渠道的红包总金额，channelRedAmount字段记录渠道红包单个金额
        #      4、t_user_withdraw表w_state状态为1【提现成功】，check_state状态为1【审核
        #        成功】，is_valid状态为1【有效】，amount字段记录红包总金额，charge手续费为0
        #      5、t_extension_channel_fee表feeAmount字段（该表产生两条记录一条是记录公司分
        #         层佣金金额，一条是记录代理商佣金金额）
        # App变化：
        #      1、钱包-我的钱包-账户余额减去发红包的金额（取redis用户金额）
        #      2、立即提现-可提现金额减去发红包金额（取redis用户commission_residue金额）
        #
        # Redis变化：
        #      1、t_user文件下该用户commission_residue减去发红包的金额
        #      2、t_extension_channel_redPool文件下redSumAmount红包总金额
        #      3、t_extension_channel文件下channelRedSumAmount红包总金额，channelRedAmount
        #        红包单个金额

        # 只有登录过的用户才能在后台操作金额 , 当验证码错误时继续尝试再次登录,最多尝试5次
        # 设置 代理商户
        for a in range(5):
            from selenium import webdriver
            browser = webdriver.Firefox()
            browser.maximize_window()
            browser.get("http://sit2.88uka.com/admin/system/logout.do")
            x=b_login(browser)
            if x==1:
                b_BusinessCommission(browser,u"自动化商户名称1",varPhone,"6","6") # 代理商户,(商户名称,手机号,代理商,佣金) 其中代理商6 = john代理商1
                from appium import webdriver
                break

        sleep(5)
        # 默认充值50元 , 获取 t_agentbusi 与公司分配比例
        r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        r2.hset("t_user:id:" + str(self.myuserID),"Commission_residue","5000")
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select rate from t_agent_busi where userId=10001679')
        data100 = cur.fetchone()
        cur = conn.cursor()
        cur.execute('update t_user set Commission_residue = 5000 where id = %s ' %(self.myuserID))
        conn.commit()
        sleep(3)

        sleep(3)
        self.driver.find_element_by_id("com.mowin.tsz:id/send_red_packet_layout").click() # 点击 发红包
        self.driver.find_element_by_id("com.mowin.tsz:id/extension_title").send_keys(u"alibaba的广告品牌二维码")
        self.driver.find_element_by_id("com.mowin.tsz:id/photo").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/gallery").click()
        varImages=self.driver.find_elements_by_id("com.mowin.tsz:id/image")
        for i in varImages:
            i.click()
            break
        sleep(2)

        self.driver.swipe(1000,200,1000,200,500) # 确定
        self.driver.find_element_by_id("com.mowin.tsz:id/extension_link").send_keys(u"www.baidu.com")
        self.driver.find_element_by_id("com.mowin.tsz:id/bind_red_packet").click()  # 设置完成,去绑红包炸弹
        self.driver.find_element_by_id("com.mowin.tsz:id/redpacket_et_count").send_keys("1")
        self.driver.find_element_by_id("com.mowin.tsz:id/redpacket_et_amount_hint").send_keys("1")
        varAccountPay = self.driver.find_element_by_id("com.mowin.tsz:id/account_balance").text
        if varAccountPay==u"¥50.00":print "OK,C2-1,发红包发广告,设置你的广告内容,绑红包炸弹,余额支付=50元"
        else:print "Error,C2-1,发红包发广告,设置你的广告内容,绑红包炸弹,余额支付=50元"
        self.driver.find_element_by_id("com.mowin.tsz:id/account_balance_checkbox").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/send_red_packet").click() # 塞钱进红包
        sleep(6)
        self.driver.find_element_by_id("com.mowin.tsz:id/share_red_packet").click() # 红包炸弹已做好
        sleep(5)

        # 选择渠道 二维码
        if self.isElement("com.mowin.tsz:id/qr_code")==True:
            self.driver.find_element_by_id("com.mowin.tsz:id/qr_code").click() # 二维码
            self.driver.find_element_by_id("com.mowin.tsz:id/positive").click() # 温馨提示,生成二维码后不可再分享至其他平台.是否生成二维码? ,点击确定
            if self.isElement("com.mowin.tsz:id/qr_code")<>True:
                 print "Error,分享至 - 生成二维码页面错误"
                 sleep(3)
            self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回后到首页
            print "OK,分享至 - 二维码"

        sleep(5)
        # 检查t_user,commission_residue字段减去发红包的金额
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select commission_residue from t_user where id=%s' %(self.myuserID))
        data1 = cur.fetchone()
        if data1[0]==4900:print "OK,C2-2,t_user,commission_residue=4900"
        else: print "Error,C2-2,t_user,commission_residue<>4900"

        # redis,检查 t_user,commission_residue 字段减去发红包的金额
        r3 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        varRedis1=r3.hget("t_user:id:" + str(self.myuserID),"Commission_residue")
        if varRedis1=="4900":print "OK,C2-3,redis,t_user,commission_residue=4900"
        else:print "Error,C2-3,redis,t_user,commission_residue<>4900"

        # 检查 t_extension_channel_redPool,redState=1【已分享】,redSumAmount=100 记录红包总金额
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select count(userId),max(id) from t_extension_channel_redPool where userId=%s and redState=1 and redSumAmount=100 ' %(self.myuserID))
        data2 = cur.fetchone()
        if data2[0]>=1:print "OK,C2-4,t_extension_channel_redPool,redSumAmount=100"
        else: print "Error,C2-4,t_extension_channel_redPool,redSumAmount<>100"

        # print self.myuserID
        # print data2[1]
        # 检查 t_extension_channel,redState=1【正常】,channelRedSumAmount=100 该渠道的红包总金额,channelRedAmount=100 渠道红包单个金额
        # 100-100*0.06
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select count(userId),id,extensionRedPoolId from t_extension_channel where userId=%s and extensionRedPoolId=%s and redState=1 and channelRedSumAmount=94 and channelRedAmount=94' %(self.myuserID,data2[1]))
        data3 = cur.fetchone()
        if data3[0]>=1:print "OK,C2-5,t_extension_channel,channelRedSumAmount=94"
        else: print "Error,C2-5,t_extension_channel,channelRedSumAmount<>94"
        # print data3[1]
        # print data3[2]
        sleep(4)
        # 检查 t_extension_channel_free,isValid=1 , redPoolId , channelId= ,feeAmount, userId发红包人,agentBusiId代理商id,agentStoreId合作商户Id,
        # 100-100*0.06
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select feeAmount from t_extension_channel_fee where redPoolId=%s  and userId=10001679' %(data2[1]))
        data4 = cur.fetchone()
        if data4[0]==0:print "OK,C2-6,t_extension_channel_fee,10001679的佣金=0"   # 0.02 * 0.06 = 0.0012 ,结果四舍五入 0.00 =0
        else: print "Error,C2-6,t_extension_channel_fee,10001679的佣金<>0"

        cur.execute('select feeAmount from t_extension_channel_fee where redPoolId=%s  and userId=1' %(data2[1]))
        data4 = cur.fetchone()
        if data4[0]==6:print "OK,C2-6,t_extension_channel_fee,代理商的佣金=6"  # 1元 * 0.06
        else: print "Error,C2-6,t_extension_channel_fee,代理商的佣金<>6"

        # 检查 t_user_withdraw,amount=100 红包总金额,charge=0 手续费,w_state=1 提现成功,check_state=1 审核成功,is_valid=1 有效
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select count(id) from t_user_withdraw where user_id=%s and amount=100 and charge=0 and w_state=1 and check_state=1' %(self.myuserID))
        data5 = cur.fetchone()
        if data5[0]>=1:print "OK,C2-7,t_user_withdraw,红包总金额1元."
        else: print "Error,C2-7,t_user_withdraw,红包总金额1元."

        # redis,检查 t_extension_channel_redPool,redSumAmount=100
        varRedis2=r3.hget("t_extension_channel_redPool:" + str(data2[1]),"redSumAmount")
        if varRedis2=="100":print "OK,C2-8,redis,t_extension_channel_redPool,redSumAmount=100"
        else:print "Error,C2-8,redis,t_extension_channel_redPool,redSumAmount<>100"

        # redis,检查 t_extension_channel,channelRedSumAmount=100
        varRedis3=r3.hget("t_extension_channel:" + str(data3[1]),"channelRedSumAmount")
        if varRedis3=="94":print "OK,C2-9,redis,t_extension_channel,channelRedSumAmount=94"
        else:print "Error,C2-9,redis,t_extension_channel,channelRedSumAmount<>94"

        # App变化：
        #  1、钱包-我的钱包-账户余额减去发红包的金额（取redis用户金额）,检查账户明细
        self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click()  # 我
        self.driver.find_element_by_id("com.mowin.tsz:id/my_wallet").click() # 钱包
        varAccountBalance = self.driver.find_element_by_id("com.mowin.tsz:id/mywalleny_allmoney").text
        if varAccountBalance=="49.00":print "OK,C2-10,我,钱包,账户余额=49.00"
        else:print "Error,C2-10,我,钱包,账户余额<>49.00"
        # 检查 账户明细 金额.
        self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'账户明细')]").click()
        varAccountDetailsCash =self.driver.find_elements_by_id("com.mowin.tsz:id/money")
        d_list=[]
        e_list=[]
        for var_AccountDetailsCash in varAccountDetailsCash:
            d_list.append(var_AccountDetailsCash.text)
        for var_AccountDetailsCash in varAccountDetailsCash:
             if var_AccountDetailsCash.text<>u"-1.00元":
                 print "Error,C2,账户明细 - 金额为" + str(var_AccountDetailsCash.text)
             break
        sleep(2)
        # 账户明细 - 明细类型
        varAccountDetailsType = self.driver.find_elements_by_id("com.mowin.tsz:id/item_accountdetail_hint")
        for var_AccountDetailsType in varAccountDetailsType:
            e_list.append(var_AccountDetailsType.text)
        for var_AccountDetailsType in varAccountDetailsType:
             if var_AccountDetailsType.text<>u"余额发送推广红包":
                 print "Error,C2,账户明细 - 类型为" + str(var_AccountDetailsType.text)
             break
        sleep(2)
        # print str(e_list[0]) +"," +str(d_list[0])
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回

        #  2、立即提现-可提现金额减去发红包金额
        self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_button").click()
        varGetCash = self.driver.find_element_by_id("com.mowin.tsz:id/with_drawal_balance").text # 可提现金额
        if varGetCash == u"¥49.00":print "OK,C2-11,我,钱包,立即提现=49.00"
        else:print "Error,C2-11,我,钱包,立即提现<>49.00"
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回
        self.driver.find_element_by_id("com.mowin.tsz:id/home_tab").click() # 返回到首页

        # 删除t_user_thirdInfo,删除与手机号关联的3条记录
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('delete from  t_user_thirdInfo where userId=%s' %(self.myuserID))
        conn.commit()
        print "============================================================="

    def accountSendPicUser(self):
        # C3,（普通用户）账户余额发送图文
        #      1、操作步骤：红包群 － 点击我的红包群-输入图文-点击发送
        # 涉及数据库变化：
        #      1、t_user表commission_residue字段减去发红包的金额
        #      2、t_user_withdraw表w_state状态为1【提现成功】，check_state状态为0【提交审核】，
        #        is_valid状态为1【有效】，amount字段记录图文红包费用，charge手续费为0
        #      3、t_redgroup_message表messageState状态为0【正常】
        #      4、t_redgroup_messamge_auth表messageState状态为0【正常】
        #      5、t_redgroup_memberinfo表isMessage数量+1
        #      6、t_redgroup_baseinfo表lastLookUpMessageTime更新成当前发送红包时间
        # App变化：
        #      1、钱包-我的钱包-账户余额减去发红包的金额（取redis用户金额）
        #      2、立即提现-可提现金额减去发红包金额（取redis用户commission_residue金额）
        # Redis变化：
        #      1、t_user文件下该用户commission_residue减去发图文红包的金额

        # 默认账户余额充值0元
        r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        r2.hset("t_user:id:" + str(self.myuserID),"Commission_residue","0")
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('update t_user set Commission_residue = 0 where id = %s ' %(self.myuserID))
        conn.commit()

        sleep(3)
        self.driver.find_element_by_id("com.mowin.tsz:id/red_packet_group_tab").click() # 点击 红包群
        self.driver.find_element_by_id("com.mowin.tsz:id/my_send_red_packet_group").click() # 点击 我的红包群

        self.driver.find_element_by_id("com.mowin.tsz:id/content").send_keys(u"自动化信息1")
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 点击 发送
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 发给谁看 点击 发送
        sleep(3)
        self.driver.find_element_by_id("com.mowin.tsz:id/content").send_keys(u"自动化信息2")
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 点击 发送
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 发给谁看 点击 发送
        sleep(3)
        self.driver.find_element_by_id("com.mowin.tsz:id/content").send_keys(u"自动化信息3")
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 点击 发送
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 发给谁看 点击 发送
        sleep(3)
        self.driver.find_element_by_id("com.mowin.tsz:id/content").send_keys(u"自动化信息4")
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 点击 发送
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 发给谁看 点击 发送
        sleep(5)

        # 账户余额不足提示信息
        if self.isElement("com.mowin.tsz:id/title")==True:
            varAccountNoBalance = self.driver.find_element_by_id("com.mowin.tsz:id/title").text
            if varAccountNoBalance==u"账户余额不足, 请充值":
                print "OK,C3-1,红包群,我的红包群,提示账户余额不足请充值"
                self.driver.find_element_by_id("com.mowin.tsz:id/cancel").click()
            else:
                print "Error,C3-1,红包群,我的红包群,提示账户余额不足请充值信息错误"
        else:
            print "Error,C3-1,红包群,我的红包群,提示信息不存在"

        # 给账户余额充值40元
        r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        r2.hset("t_user:id:" + str(self.myuserID),"Commission_residue","4000")
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('update t_user set Commission_residue = 4000 where id = %s ' %(self.myuserID))
        conn.commit()
        sleep(2)

        self.driver.find_element_by_id("com.mowin.tsz:id/content").send_keys(u"自动化信息5")
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 点击 发送
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 发给谁看 点击 发送
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()

        # 点击 照片 ,发红包炸弹 未做

        # App变化：
        # 1、钱包-我的钱包-账户余额减去发红包的金额（取redis用户金额）,检查账户明细
        self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click()  # 我
        self.driver.find_element_by_id("com.mowin.tsz:id/my_wallet").click() # 钱包
        varAccountBalance = self.driver.find_element_by_id("com.mowin.tsz:id/mywalleny_allmoney").text
        if varAccountBalance=="39.00":print "OK,C3-2,我,钱包,账户余额=39.00"
        else:print "Error,C3-2,我,钱包,账户余额<>39.00"
        # 检查 账户明细 金额.
        self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'账户明细')]").click()
        varAccountDetailsCash =self.driver.find_elements_by_id("com.mowin.tsz:id/money")
        d_list=[]
        e_list=[]
        for var_AccountDetailsCash in varAccountDetailsCash:
            d_list.append(var_AccountDetailsCash.text)
        for var_AccountDetailsCash in varAccountDetailsCash:
             if var_AccountDetailsCash.text<>u"-1.00元":
                 print "Error,C3,账户明细 - 金额为" + str(var_AccountDetailsCash.text)
             break
        sleep(2)
        # 账户明细 - 明细类型
        varAccountDetailsType = self.driver.find_elements_by_id("com.mowin.tsz:id/item_accountdetail_hint")
        for var_AccountDetailsType in varAccountDetailsType:
            e_list.append(var_AccountDetailsType.text)
        for var_AccountDetailsType in varAccountDetailsType:
             if var_AccountDetailsType.text<>u"红包群发图文扣款":
                 print "Error,C3,账户明细 - 类型为" + str(var_AccountDetailsType.text)
             break
        sleep(2)
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回

        #  2、立即提现-可提现金额减去发红包金额
        self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_button").click()
        varGetCash = self.driver.find_element_by_id("com.mowin.tsz:id/with_drawal_balance").text # 可提现金额
        if varGetCash == u"¥39.00":print "OK,C3-3,我,钱包,立即提现=39.00"
        else:print "Error,C3-3,我,钱包,立即提现<>39.00"
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回
        self.driver.find_element_by_id("com.mowin.tsz:id/home_tab").click() # 返回到首页

        # redis,检查 t_user,commission_residue 字段减去发红包的金额
        r3 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        varRedis1=r3.hget("t_user:id:" + str(self.myuserID),"Commission_residue")
        if varRedis1=="3900":print "OK,C3-4,redis,t_user,commission_residue=3900"
        else:print "Error,C3-4,redis,t_user,commission_residue<>3900"

        # 检查t_user,commission_residue字段减去发红包的金额
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select commission_residue from t_user where id=%s' %(self.myuserID))
        data1 = cur.fetchone()
        if data1[0]==3900:print "OK,C3-5,t_user,commission_residue=3900"
        else: print "Error,C3-5,t_user,commission_residue<>3900"

        # 检查 t_user_withdraw,w_state=1 提现成功,check_state=0 提交审核,is_valid=1 有效,amount=100 红包总金额,charge=0 手续费
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select count(id) from t_user_withdraw where user_id=%s and amount=100 and charge=0 and w_state=1 and check_state=0' %(self.myuserID))
        data4 = cur.fetchone()
        if data4[0]>=1:print "OK,C3-6,t_user_withdraw,红包总金额1元."
        else: print "Error,C3-6,t_user_withdraw,红包总金额1元."

        # 检查 t_redgroup_message,messageState=0
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select sum(messageState) from t_redgroup_message where groupId=%s ' %(self.mygroupID))
        data2 = cur.fetchone()
        if data2[0]==0:print "OK,C3-7,t_redgroup_message,发送图文正常"
        else: print "Error,C3-7,t_redgroup_message,发送图文有异常"

        # 检查 t_redgroup_messamge_auth,messageState =0【正常】
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select sum(messageState) from t_redgroup_messamge_auth where groupId=%s ' %(self.mygroupID))
        data3 = cur.fetchone()
        if data3[0]==0:print "OK,C3-8,t_redgroup_messamge_auth,发送图文正常"
        else: print "Error,C3-8,t_redgroup_messamge_auth,发送图文有异常"

        # 检查 t_redgroup_baseinfo, lastLookUpMessageTime 更新成当前发送红包时间
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select lastLookUpMessageTime from t_redgroup_baseinfo where userId=%s ' %(self.myuserID))
        data4 = cur.fetchone()
        if data4[0]<>"":print "OK,C3-9,t_redgroup_baseinfo,更新成当前发送红包时间"
        else: print "Error,C3-9,t_redgroup_baseinfo,更新成当前发送红包时间"
        print "============================================================="

    def accountRedbonusMoneybags(self):
        #  C4,（大咖用户）账户余额发送推广红包
        #      1、操作步骤：系统后台-财务-充值-填写充值金额信息-点击首页-设置广告内容-绑定
        #                   红包炸弹-塞钱进红包-选择分享渠道
        # 数据库变化：
        #      1、t_user表rechargeAmount字段减去发红包的金额
        #      2、t_extension_channel_redPool表redState状态为1【已分享】、redSumAmount字段
        #         记录红包总金额
        #      3、t_extension_channel表redState状态为1【正常】，channelRedSumAmount字段记录
        #         该渠道的红包总金额，channelRedAmount字段记录渠道红包单个金额
        #      4、t_user_withdraw表w_state状态为1【提现成功】，check_state状态为1【审核
        #        成功】，is_valid状态为1【有效】，amount字段记录红包总金额，charge手续费为0
        # App变化：
        #      1、钱包-我的钱包-账户余额减去发红包的金额（取redis用户金额）
        #      2、立即提现-无变化（提现金额不记录大咖金额）
        # Redis变化：
        #      1、t_user文件下该用户commission_residue减去发红包的金额
        #      2、t_extension_channel_redPool文件下redSumAmount红包总金额
        #      3、t_extension_channel文件下channelRedSumAmount红包总金额，channelRedAmount
        #        红包单个金额


        # 只有登录过的用户才能在后台操作金额 , 当验证码错误时继续尝试再次登录,最多尝试5次
        # 设置 大咖用户
        for a in range(5):
            from selenium import webdriver
            browser = webdriver.Firefox()
            browser.maximize_window()
            browser.get("http://sit2.88uka.com/admin/system/logout.do")
            x=b_login(browser)
            if x==1:
                b_bigDogUser(browser,varPhone,"33","99") # 大咖用户,(手机号,金额,到期日期)
                from appium import webdriver
                break

        # 默认账户余额充值50元 ,给大咖用户充值33元
        r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        r2.hset("t_user:id:" + str(self.myuserID),"Commission_residue","5000")
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('update t_user set Commission_residue = 5000 where id = %s ' %(self.myuserID))
        conn.commit()

        sleep(3)
        self.driver.find_element_by_id("com.mowin.tsz:id/send_red_packet_layout").click() # 点击 发红包
        self.driver.find_element_by_id("com.mowin.tsz:id/extension_title").send_keys(u"alibaba的广告品牌大咖")
        self.driver.find_element_by_id("com.mowin.tsz:id/photo").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/gallery").click()
        varImages=self.driver.find_elements_by_id("com.mowin.tsz:id/image")
        for i in varImages:
            i.click()
            break
        sleep(2)
        self.driver.swipe(1000,200,1000,200,500) # 确定
        self.driver.find_element_by_id("com.mowin.tsz:id/extension_link").send_keys(u"www.163.com")
        self.driver.find_element_by_id("com.mowin.tsz:id/bind_red_packet").click()  # 设置完成,去绑红包炸弹
        self.driver.find_element_by_id("com.mowin.tsz:id/redpacket_et_count").send_keys("1")
        self.driver.find_element_by_id("com.mowin.tsz:id/redpacket_et_amount_hint").send_keys("1")
        varAccountPay = self.driver.find_element_by_id("com.mowin.tsz:id/account_balance").text
        if varAccountPay==u"¥83.00":print "OK,C4-1,发红包发广告,设置你的广告内容,绑红包炸弹,余额支付=83元"
        else:print "Error,C4-1,发红包发广告,设置你的广告内容,绑红包炸弹,余额支付<>83元"
        self.driver.find_element_by_id("com.mowin.tsz:id/account_balance_checkbox").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/send_red_packet").click() # 塞钱进红包
        sleep(2)
        self.driver.find_element_by_id("com.mowin.tsz:id/share_red_packet").click() # 红包炸弹已做好

        # # 检查 抢红包 和 红包群 icon为灰色
        # if self.isElement("com.mowin.tsz:id/app_disable")==True and self.isElement("com.mowin.tsz:id/red_packet_group_disable")==True:
        #     print "OK,C1-3,抢红包与红包群icon为灰色不可选."
        # else:
        #     print "Error,C1-3,抢红包与红包群icon为灰色不存在."

        # 选择渠道
        # if varChannel==1: # 朋友圈
        self.driver.find_element_by_id("com.mowin.tsz:id/wx_timeline").click() # 朋友圈
        sleep(4)
        self.driver.find_element_by_id("com.mowin.tsz:id/negative").click() # 温馨提示,系统可自动将此红包炸弹分享到你的红包群里. 点击不需要
        sleep(8)
        self.driver.find_element_by_id("com.tencent.mm:id/eg").click() # 第三方平台, 发送
        print "OK,分享至 - 朋友圈"

        sleep(3)
        self.driver.find_element_by_id("com.mowin.tsz:id/close").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/negative").click() # 温馨提示,你确定不再继续向以下平台发红包炸弹了吗? 确定


        # 检查t_user,commission_residue字段减去发红包的金额
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select rechargeAmount from t_user where id=%s' %(self.myuserID))
        data1 = cur.fetchone()
        if data1[0]==3200:print "OK,C4-2,t_user,rechargeAmount=3200"
        else: print "Error,C4-2,t_user,rechargeAmount<>3200"

        # redis,检查 t_user,commission_residue 字段减去发红包的金额
        r3 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        varRedis1=r3.hget("t_user:id:" + str(self.myuserID),"RechargeAmount")
        if varRedis1=="3200":print "OK,C4-3,redis,t_user,rechargeAmount=3200"
        else:print "Error,C4-3,redis,t_user,rechargeAmount<>3200"

        # 检查 t_extension_channel_redPool,redState=1【已分享】,redSumAmount=100 记录红包总金额
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select count(userId),id from t_extension_channel_redPool where userId=%s and redState=1 and redSumAmount=100' %(self.myuserID))
        data2 = cur.fetchone()
        if data2[0]>=1:print "OK,C4-4,t_extension_channel_redPool,红包总金额1元."
        else: print "Error,C4-4,t_extension_channel_redPool,红包总金额<>1元."

        # 检查 t_extension_channel,redState=1【正常】,channelRedSumAmount=100 该渠道的红包总金额,channelRedAmount=100 渠道红包单个金额
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select count(userId),id from t_extension_channel where userId=%s and extensionRedPoolId=%s and redState=1 and channelRedSumAmount=100 and channelRedAmount=100' %(self.myuserID,data2[1]))
        data3 = cur.fetchone()
        if data3[0]>=1:print "OK,C4-5,t_extension_channel,红包总金额1元."
        else: print "Error,C4-5,t_extension_channel,红包总金额<>1元."

        # 检查 t_user_withdraw,amount=100 红包总金额,charge=0 手续费,w_state=1 提现成功,check_state=1 审核成功,is_valid=1 有效
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select count(id) from t_user_withdraw where user_id=%s and amount=100 and charge=0 and w_state=1 and check_state=1' %(self.myuserID))
        data4 = cur.fetchone()
        if data4[0]>=1:print "OK,C4-6,t_user_withdraw,红包总金额1元."
        else: print "Error,C4-6,t_user_withdraw,红包总金额1元."

        # redis,检查 t_extension_channel_redPool,redSumAmount=100
        varRedis2=r3.hget("t_extension_channel_redPool:" + str(data2[1]),"redSumAmount")
        if varRedis2=="100":print "OK,C4-7,redis,t_extension_channel_redPool,redSumAmount=100"
        else:print "Error,C4-7,redis,t_extension_channel_redPool,redSumAmount<>100"

        # redis,检查 t_extension_channel,channelRedSumAmount=100
        varRedis3=r3.hget("t_extension_channel:" + str(data3[1]),"channelRedSumAmount")
        if varRedis3=="100":print "OK,C4-8,redis,t_extension_channel,channelRedSumAmount=100"
        else:print "Error,C4-8,redis,t_extension_channel,channelRedSumAmount<>100"

        # App变化：
        #  1、钱包-我的钱包-账户余额减去发红包的金额（取redis用户金额）,检查账户明细
        self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click()  # 我
        self.driver.find_element_by_id("com.mowin.tsz:id/my_wallet").click() # 钱包
        varAccountBalance = self.driver.find_element_by_id("com.mowin.tsz:id/mywalleny_allmoney").text
        if varAccountBalance=="82.00":print "OK,C4-9,钱包,账户余额=82.00"
        else:print "Error,C4-9,钱包,账户余额<>82.00"
        # 检查 账户明细 金额.
        self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'账户明细')]").click()
        varAccountDetailsCash =self.driver.find_elements_by_id("com.mowin.tsz:id/money")
        d_list=[]
        e_list=[]
        for var_AccountDetailsCash in varAccountDetailsCash:
            d_list.append(var_AccountDetailsCash.text)
        for var_AccountDetailsCash in varAccountDetailsCash:
             if var_AccountDetailsCash.text<>u"-1.00元":
                 print "Error,C4,账户明细 - 金额为" + str(var_AccountDetailsCash.text)
             break
        sleep(2)
        # 账户明细 - 明细类型
        varAccountDetailsType = self.driver.find_elements_by_id("com.mowin.tsz:id/item_accountdetail_hint")
        for var_AccountDetailsType in varAccountDetailsType:
            e_list.append(var_AccountDetailsType.text)
        for var_AccountDetailsType in varAccountDetailsType:
             if var_AccountDetailsType.text<>u"三藏红包充值金额 发推广红包":
                 print "Error,C4,账户明细 - 类型为" + str(var_AccountDetailsType.text)
             break
        sleep(2)
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回

        #  2、立即提现-可提现金额减去发红包金额
        self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_button").click()
        varGetCash = self.driver.find_element_by_id("com.mowin.tsz:id/with_drawal_balance").text # 可提现金额
        if varGetCash == u"¥50.00":print "OK,C4-10,我,钱包,立即提现=50.00"
        else:print "Error,C4-10,我,钱包,立即提现<>50.00"
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回
        self.driver.find_element_by_id("com.mowin.tsz:id/home_tab").click() # 返回到首页

        # 删除t_user_thirdInfo,删除与手机号关联的3条记录
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('delete from  t_user_thirdInfo where userId=%s' %(self.myuserID))
        conn.commit()
        print "============================================================="

    def accountSendPicMoneybags(self):
        # C5,（大咖用户）账户余额发送图文(依赖于C1-3)
        #      1、操作步骤：系统后台-财务-充值-填写充值金额信息-点击我的红包群-输入图文-点击
        #                  发送
        # 数据库变化：
        #      1、t_user表commission_residue字段减去发红包的金额
        #      2、t_user_withdraw表w_state状态为1【提现成功】，check_state状态为0【提交审核】，
        #        is_valid状态为1【有效】，amount字段记录图文红包费用，charge手续费为0
        #      3、t_redgroup_message表messageState状态为0【正常】
        #      4、t_redgroup_messamge_auth表messageState状态为0【正常】
        #      5、t_redgroup_memberinfo表isMessage数量+1
        #      6、t_redgroup_baseinfo表lastLookUpMessageTime更新成当前发送红包时间
        #
        # App变化：
        #      1、钱包-我的钱包-账户余额减去发红包的金额（取redis用户金额）
        #      2、立即提现-可提现金额减去发红包金额（取redis用户commission_residue金额）
        #
        # Redis变化：
        #      1、t_user文件下该用户commission_residue减去发图文红包的金额

        # # 默认账户余额充值0元 ,大咖账户=0
        # r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        # r2.hset("t_user:id:" + str(self.myuserID),"Commission_residue","0")
        # r2.hset("t_user:id:" + str(self.myuserID),"RechargeAmount","0")
        # conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        # cur = conn.cursor()
        # cur.execute('update t_user set Commission_residue = 0 where id = %s ' %(self.myuserID))
        # cur.execute('update t_user set rechargeAmount = 0 where id = %s ' %(self.myuserID))
        # conn.commit()

        sleep(3)
        self.driver.find_element_by_id("com.mowin.tsz:id/red_packet_group_tab").click() # 点击 红包群
        self.driver.find_element_by_id("com.mowin.tsz:id/my_send_red_packet_group").click() # 点击 我的红包群

        self.driver.find_element_by_id("com.mowin.tsz:id/content").send_keys(u"自动化信息11")
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 点击 发送
        self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 发给谁看 点击 发送

        # self.driver.find_element_by_id("com.mowin.tsz:id/content").send_keys(u"自动化信息12")
        # self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 点击 发送
        # self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 发给谁看 点击 发送
        #
        # self.driver.find_element_by_id("com.mowin.tsz:id/content").send_keys(u"自动化信息13")
        # self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 点击 发送
        # self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 发给谁看 点击 发送
        #
        # self.driver.find_element_by_id("com.mowin.tsz:id/content").send_keys(u"自动化信息14")
        # self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 点击 发送
        # self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 发给谁看 点击 发送

        # sleep(5)
        # # 账户余额不足提示信息
        # if self.isElement("com.mowin.tsz:id/title")==True:
        #     varAccountNoBalance = self.driver.find_element_by_id("com.mowin.tsz:id/title").text
        #     if varAccountNoBalance==u"账户余额不足, 请充值":
        #         print "OK,C1-5,我的红包群,发布第四次信息提示账户余额不足请充值"
        #         self.driver.find_element_by_id("com.mowin.tsz:id/cancel").click()
        #     else:
        #         print "Error,C1-5,我的红包群,发布第四次信息提示账户余额不足请充值"
        # else:
        #     print "Error,C1-5,我的红包群,发布第四次信息提示账户余额不足请充值"

        # # 给账户余额充值60元
        # r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        # r2.hset("t_user:id:" + str(self.myuserID),"Commission_residue","6000")
        # r2.hset("t_user:id:" + str(self.myuserID),"RechargeAmount","1000")
        # conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        # cur = conn.cursor()
        # cur.execute('update t_user set Commission_residue = 6000 where id = %s ' %(self.myuserID))
        # cur.execute('update t_user set rechargeAmount = 1000 where id = %s ' %(self.myuserID))
        # conn.commit()
        # sleep(2)

        # self.driver.find_element_by_id("com.mowin.tsz:id/content").send_keys(u"自动化信息15")
        # self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 点击 发送
        # self.driver.find_element_by_id("com.mowin.tsz:id/send").click() # 发给谁看 点击 发送
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()

        # 点击 照片 ,发红包炸弹 未做

        # App变化：
        #  1、钱包-我的钱包-账户余额减去发红包的金额（取redis用户金额）,检查账户明细
        self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click()  # 我
        self.driver.find_element_by_id("com.mowin.tsz:id/my_wallet").click() # 钱包
        varAccountBalance = self.driver.find_element_by_id("com.mowin.tsz:id/mywalleny_allmoney").text
        if varAccountBalance=="81.00":print "OK,C5-1,我,钱包,账户余额=81.00"
        else:print "Error,C5-1,我,钱包,账户余额<>81.00"
        # 检查 账户明细 金额.
        self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'账户明细')]").click()
        varAccountDetailsCash =self.driver.find_elements_by_id("com.mowin.tsz:id/money")
        d_list=[]
        e_list=[]
        for var_AccountDetailsCash in varAccountDetailsCash:
            d_list.append(var_AccountDetailsCash.text)
        for var_AccountDetailsCash in varAccountDetailsCash:
             if var_AccountDetailsCash.text<>u"-1.00元":
                 print "Error,C5,账户明细 - 金额为" + str(var_AccountDetailsCash.text)
             break
        sleep(2)
        # 账户明细 - 明细类型
        varAccountDetailsType = self.driver.find_elements_by_id("com.mowin.tsz:id/item_accountdetail_hint")
        for var_AccountDetailsType in varAccountDetailsType:
            e_list.append(var_AccountDetailsType.text)
        for var_AccountDetailsType in varAccountDetailsType:
             if var_AccountDetailsType.text<>u"红包群发图文扣款":
                 print "Error,C5,账户明细 - 类型为" + str(var_AccountDetailsType.text)
             break
        sleep(2)
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回

        #  2、立即提现-可提现金额减去发红包金额
        self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_button").click()
        varGetCash = self.driver.find_element_by_id("com.mowin.tsz:id/with_drawal_balance").text # 可提现金额
        if varGetCash == u"¥49.00":print "OK,C5-2,我,钱包,立即提现=49.00"
        else:print "Error,C5-2,我,钱包,立即提现<>49.00"
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回
        self.driver.find_element_by_id("com.mowin.tsz:id/home_tab").click() # 返回到首页

        # redis,检查 t_user,commission_residue 字段减去发红包的金额
        r3 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        varRedis1=r3.hget("t_user:id:" + str(self.myuserID),"Commission_residue")
        varRedis2=r3.hget("t_user:id:" + str(self.myuserID),"RechargeAmount")
        if varRedis1=="4900":print "OK,C5-3,redis,t_user,commission_residue=4900"
        else:print "Error,C5-3,redis,t_user,commission_residue<>4900"
        if varRedis2=="3200":print "OK,C5-4,redis,t_user,RechargeAmount=3200"
        else:print "Error,C5-4,redis,t_user,RechargeAmount<>3200"

        # C1-5-1,检查t_user,commission_residue字段减去发红包的金额
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select commission_residue from t_user where id=%s' %(self.myuserID))
        data1 = cur.fetchone()
        if data1[0]==4900:print "OK,C5-5,t_user,commission_residue=4900"
        else: print "Error,C5-5,t_user,commission_residue<>4900"

        # C1-5-2,检查 t_user_withdraw,w_state=1 提现成功,check_state=0 提交审核,is_valid=1 有效,amount=100 红包总金额,charge=0 手续费
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select count(id) from t_user_withdraw where user_id=%s and amount=100 and charge=0 and w_state=1 and check_state=0' %(self.myuserID))
        data4 = cur.fetchone()
        if data4[0]>=1:print "OK,C5-6,t_user_withdraw,红包总金额1元."
        else: print "Error,C5-6,t_user_withdraw,红包总金额1元."

        # C1-5-3,检查 t_redgroup_message,messageState=0
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select sum(messageState) from t_redgroup_message where groupId=%s ' %(self.mygroupID))
        data2 = cur.fetchone()
        if data2[0]==0:print "OK,C5-7,t_redgroup_message,发送图文正常"
        else: print "Error,C5-7,t_redgroup_message,发送图文有异常"

        # C1-5-4,检查 t_redgroup_messamge_auth,messageState =0【正常】
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select sum(messageState) from t_redgroup_messamge_auth where groupId=%s ' %(self.mygroupID))
        data3 = cur.fetchone()
        if data3[0]==0:print "OK,C5-8,t_redgroup_messamge_auth,发送图文正常"
        else: print "Error,C5-8,t_redgroup_messamge_auth,发送图文有异常"

        # C1-5-5,检查 t_redgroup_baseinfo, lastLookUpMessageTime 更新成当前发送红包时间
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select lastLookUpMessageTime from t_redgroup_baseinfo where userId=%s ' %(self.myuserID))
        data4 = cur.fetchone()
        if data4[0]<>"":print "OK,C5-9,t_redgroup_baseinfo,发送红包时间存在"
        else: print "Error,C5-9,t_redgroup_baseinfo,发送红包时间不存在"

        # C1-5-6,检查t_user,rechargeAmount=1000
        conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
        cur = conn.cursor()
        cur.execute('select rechargeAmount from t_user where id=%s' %(self.myuserID))
        data5 = cur.fetchone()
        if data5[0]==3200:print "OK,C5-10,t_user,rechargeAmount=3200"
        else: print "Error,C5-10,t_user,rechargeAmount<>3200"
        print "============================================================="


if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(Tsz_amount) # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1) # 执行测试

