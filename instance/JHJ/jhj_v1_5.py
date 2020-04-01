# coding: utf-8
#****************************************************************
# jhj_v1_5.py
# Author     : John
# Version    : 1.0.0
# Date       : 2016-4-1
# Description: 自动化测试平台
#****************************************************************


#http://tungwaiyip.info/software/HTMLTestRunner.html
import os,sys,unittest,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,platform,string,datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from appium import webdriver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from xlwt.Style import *
from xlrd import open_workbook
from xlutils.copy import copy
from PIL import Image
from pyh import *
#from jhj_v1_5_setup import *
#win32api,win32con,HTMLTestRunner
import HTMLTestRunner

print sys.path

################ test area ################
# xx="(含6.0运费)"
# yy=xx[4:]
# print yy[:-7]
# a="12.6"
# b="3"
# c="6.0"
# print float(a)*int(b)+float(c)
# print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# sleep(123)
################################################

# 页面格式化 http://www.tuicool.com/articles/IRvEBr
# page =PyH('JHJ_TestReport')
# page.addCSS('myStylesheet1.css','myStylesheet2.css')
# page << h2(u'极好家V1.5自动化测试报告', cl='center')
# page << h4(u'Start Time:',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# page << h4(u'用例执行情况：')

# 环境变量
File_ExcelName = "/Users/linghuchong/Downloads/51/ForWin/Python/02_code/excel/jhj_1_5.xls"
Html_Testreport = "/Users/linghuchong/Downloads/51/ForWin/Python/02_code/report/testreport.html" # TestReport文件
Err_Screenshot = "/Users/linghuchong/Downloads/51/ForWin/Python/02_code/screenshot/"  # 错误截屏
#os.path.abspath() 方法用于获取当前路径下的文件
#PATH = lambda p: os.path.abspath(p)
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

class Jhj1_5(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.3'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appPackage'] = 'cn.jihaojia'
        #for 1.5 and before
        desired_caps['appActivity'] = 'cn.jihaojia.activity.GuidanceActivity'
        #for 1.5.1
        #desired_caps['appActivity'] = 'cn.jihaojia.ui.guide.GuidanceActivity'
        desired_caps['unicodeKeyboard'] ='True'
        desired_caps['resetKeyboard'] = 'True'
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        self.fname=File_ExcelName
        bk = xlrd.open_workbook(File_ExcelName,formatting_info=True)
        self.bk=bk
        newbk=copy(bk)
        self.newbk=newbk
        styleP = xlwt.easyxf('font: name Times New Roman, color-index blue')
        styleE = xlwt.easyxf('font: name Times New Roman, color-index red')
        self.styleP=styleP
        self.styleE=styleE

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
                      else:
                           caseN=caseN+1
                           break
                 break
         #遍历 Testcase1~TestCaseN
         for l in range(case1,caseN+case1):
                   #遍历100列，参数从第五列开始，一般不会有100个参数
                   str_list=[]
                   for m in range(6,15):  #id0 - id9
                         if self.sh2.cell(l,m).value<>"" :
                              N=self.sh2.cell_value(l,m)
                              str_list.append(str(N))
                         else:
                             break
                   self.str_list=str_list
                   try :
                       exec(self.sh2.cell_value(l,4))
                       newWs=self.newbk.get_sheet(1)
                       newWs.write(l,0,"pass",self.styleP)
                       self.newbk.save(self.fname)
                       # page << p("<font color=blue>[Pass]</font> ",self.sh2.cell_value(l,3))  #输出测试用例
                   except:
                       print "Err,第"+str(l+1)+"行,"+self.sh2.cell_value(l,3)
                       newWs=self.newbk.get_sheet(1)
                       newWs.write(l,0,"error",self.styleE)
                       self.newbk.save(self.fname)
                       # page << p("<font color=red>[Error]</font> ",self.sh2.cell_value(l,3))  #输出测试用例
                   # page.printOut(Html_Testreport)
                   #open HTML
                   if self.sh1.cell_value(1,6) == "Y":
                      webbrowser.open(Html_Testreport)
    def NullModule(self):
        pass

    ##############################################################################################
#首页
def homepage(self):
     #首页
     self.TestcaseModule()

    def Hometop3(self):
        sleep(5)
        Coordinate=self.driver.find_element_by_id("cn.jihaojia:id/home_qrcode_img").location
        print Coordinate.get('x') #72
        print Coordinate.get('y') #60
        ElementSize=self.driver.find_element_by_id("cn.jihaojia:id/home_qrcode_img").size
        print ElementSize['width'] #68
        print ElementSize['height'] #150


        sleep(1)
        #C1-1顶部按钮验证，福利按钮、搜索框、购物车
        #C1-1，验证顶部福利按钮是否存在，并跳转到优惠券页面
        if self.isElement("cn.jihaojia:id/home_qrcode_img")==True:
            self.driver.find_element_by_id("cn.jihaojia:id/home_qrcode_img").click()
            sleep(2)
            if self.isElement("cn.jihaojia:id/t1")==True:
                self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click() #返回
            else:
                print "Err,C1-1 优惠券文字不存在！！！"
        else:
              print "Err,C1-1顶部福利按钮不存在！！！"
        #C1-1，验证顶部搜索框内文字及搜索跳转
        if self.isElement("cn.jihaojia:id/home_search_edt")==True:
            #验证搜索框内 极好家 文字是否显示
            c1tmptext1=self.driver.find_element_by_id("cn.jihaojia:id/home_search_edt").text
            if c1tmptext1=="极好家":
                pass
            else :
                print "Err，C1-1极好家文字无显示！！！"
                self.assertEqual(1,0,"Err，C1-1极好家文字无显示！！！")
            #点击输入框跳转搜索页面并进行搜索功能（没有完成，无法回车？？？）
            # self.driver.find_element_by_id("cn.jihaojia:id/home_search_edt").click()
            # self.driver.find_element_by_id("cn.jihaojia:id/action_search_edt").send_keys("123")
            # sleep(2)
            # self.driver.find_element_by_id("cn.jihaojia:id/action_search_edt").send_keys(Keys.ENTER)
            # searchresult=self.driver.find_elements_by_id("cn.jihaojia:id/recommend_page_day_image")
            # for searchresult1 in searchresult:
            #     searchresult1.click()
            #     break
        else:
            print "C1-1，顶部搜索框不存在！！！"
        #C1-1，验证 顶部购物车按钮是否存在及跳转
        if self.isElement("cn.jihaojia:id/trolley")==True:
            #跳转到购物车页面
            self.driver.find_element_by_id("cn.jihaojia:id/trolley").click()
            #没有登录
            if self.isElement("cn.jihaojia:id/gaga_login_account_edit")==True:
                self.Login("13816109050")
                sleep(2)
                if self.driver.find_element_by_id("cn.jihaojia:id/t1").text=="购物车" :
                    self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click() #返回
                else:
                    print "Err,C1-1购物车文字不存在！！！"
            else:
                if self.driver.find_element_by_id("cn.jihaojia:id/t1").text=="购物车" :
                    self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click() #返回
                else:
                    print "Err,C1-1购物车文字不存在！！！"
        else:
            print "Err,C1-1顶部购物车按钮不存在！！！"
        sleep(2)
    def HomeS1(self):
         #C1-2,顶部banner正常显示3张图
         x=0
         if self.isElement("cn.jihaojia:id/cbLoopViewPager")==True:
             pass
         else:
             print "Err，C1-2 顶部banner图不显示！！！"
             self.assertEqual(1,0,"Err，C1-2顶部banner图不显示！！！")
    def HomeS2(self):
         #C1-3,首页顶部活动广告位 是否显示
         if self.isElement("cn.jihaojia:id/home_item_meplace_img1")==True:
             pass
         else:
             print "Err，C1-3,首页顶部活动广告位 没有显示！！！"
             self.assertEqual(1,0,"Err，C1-3,首页顶部活动广告位 没有显示！！！")
    def HomeS3(self):
         #C1-4,首页热推区 是否显示
         if self.isElement("cn.jihaojia:id/grid_view")==True:
             pass
         else:
             print "Err，C1-4,首页热推区 没有显示！！！"
             self.assertEqual(1,0,"Err，C1-4,首页热推区 没有显示！！！")
    def HomeS4(self):
         #C1-5新用户登录显示新人专享,老用户登录则不显示
         #新用户登录
         # self.MySetupExitLogin()
         # self.driver.find_element_by_id("cn.jihaojia:id/setting").click()
         # self.Login("13816102222")#自动化登录，调用
         # self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
         # sleep(2)
         # self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[0].click()
         self.driver.swipe(800, 1600, 800, 800, 0);
         sleep(10)
         #C1-5,首页新人专享 心Icon 是否显示
         if self.isElement("cn.jihaojia:id/saveworry_icon_1")==True:
             pass
         else:
             print "Err,C1-5,首页新人专享,时间Icon无显示!"
             self.assertEqual(1,0,"Err,C1-5,首页新人专享,时间Icon无显示!")
         #C1-5,首页新人专享 尝鲜诚惠 是否显示
         if self.isElement("cn.jihaojia:id/saveworry_icon_2")==True:
             pass
         else:
             print "Err,C1-5,首页新人专享,尝鲜诚惠无显示!"
             self.assertEqual(1,0,"Err,C1-5,首页新人专享,尝鲜诚惠无显示!")
         #C1-5,首页新人专享 文字 是否显示
         if self.isElement("cn.jihaojia:id/saveworry_title_txt")==True:
             pass
         else:
             print "Err,C1-5,首页新人专享,新人专享文字无显示!"
             self.assertEqual(1,0,"Err,C1-5,首页新人专享,新人专享文字无显示!")
         #C1-5,首页新人专享 更多> 文字 是否显示
         if self.isElement("cn.jihaojia:id/saveworry_more_layout")==True:
             #点击更多
             self.driver.find_element_by_id("cn.jihaojia:id/saveworry_more_layout").click()
             self.Unionpage("C1-5","新人专享")
         else:
             print "Err,C1-5,首页新人专享,更多> 文字无显示!"
             self.assertEqual(1,0,"Err,C1-5,首页新人专享,更多> 文字无显示!")
         #C1-5,首页新人专享 无显示
         sleep(3)
         if self.isElement("cn.jihaojia:id/home_item_grid_img1")==True:
             pass
         else:
             print "Err,C1-5,首页新人专享,推荐项无显示!"
             self.assertEqual(1,0,"Err,C1-5,首页新人专享,推荐项无显示!")

        #老用户登录
    def HomeS5(self):
         #C1-6,首页值得买 时间Icon 是否显示
         if self.isElement("cn.jihaojia:id/sekking_icon_1")==True:
             pass
         else:
             print "Err，C1-6,首页值得买 时间Icon 没有显示！！！"
             self.assertEqual(1,0,"Err，C1-6,首页值得买 时间Icon 没有显示！！！")

         #C1-5,首页值得买 文字 是否显示
         if self.isElement("cn.jihaojia:id/sekking_title_txt")==True:
             pass
         else:
             print "Err，C1-6,首页值得买文字 没有显示！！！"
             self.assertEqual(1,0,"Err，C1-5,首页值得买文字 没有显示！！！")
         #C1-6,首页值得买 更多> 文字 是否显示
         if self.isElement("cn.jihaojia:id/cassic_more_layout")==True:
             #点击更多
             self.driver.find_element_by_id("cn.jihaojia:id/cassic_more_layout").click()
             if self.driver.find_element_by_id("cn.jihaojia:id/home_title_txt").text=="值得买" :
                  sleep(2)
                  self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[0].click()
             else:
                 print "Err，C1-6,首页值得买点击 更多后跳转错误！！！"
                 self.assertEqual(1,0,"Err，C1-6,首页值得买点击 更多后跳转错误！！！")
         else:
             print "Err，C1-6,首页值得买 更多> 文字 没有显示！！！"
             self.assertEqual(1,0,"Err，C1-6,首页值得买 更多> 文字 没有显示！！！")
         self.driver.swipe(800, 1600, 800, 700, 0);
         #C1-6,首页值得买 区域是否显示
         if self.isElement("cn.jihaojia:id/classic_grid_view")==True:
             pass
         else:
             print "Err，C1-6,首页值得买 区域没有显示！！！"
             self.assertEqual(1,0,"Err，C1-6,首页值得买 区域没有显示！！！")
    def HomeS6(self):
         self.driver.swipe(800, 1600, 800, 800, 0);
         #C1-7首页横幅A 是否显示
         if self.isElement("cn.jihaojia:id/home_item_banners_img")==True:
             pass
         else:
             print "Err,C1-7,首页横幅A广告不存在!"
             self.assertEqual(1,0,"Err,C1-7,首页横幅B广告不存在!")
    def HomeS7(self):
         #C1-8首页新品速递 时间Icon\新品速递\取悦自己\更多
         if self.isElement("cn.jihaojia:id/newest_icon_1")==True:
             pass
         else:
             print "Err,C1-8,首页新品速递,时间Icon无显示!"
             self.assertEqual(1,0,"Err,C1-8,首页新品速递,时间Icon无显示!")
         #C1-8首页新品速递 新品速递文字
         if self.isElement("cn.jihaojia:id/taent_talent_txt")==True:
             pass
         else:
             print "Err,C1-8,首页新品速递,新品速递文字无显示!"
             self.assertEqual(1,0,"Err,C1-8,首页新品速递,新品速递文字无显示!")
         #C1-8首页新品速递 取悦自己文字
         if self.isElement("cn.jihaojia:id/newest_icon_2")==True:
             pass
         else:
             print "Err,C1-8,首页新品速递,取悦自己文字无显示!"
             self.assertEqual(1,0,"Err,C1-8,首页新品速递,取悦自己文字无显示!")
         #C1-8,首页新品速递 更多> 文字 是否显示
         if self.isElement("cn.jihaojia:id/taent_newest_layout")==True:
             #点击更多
             self.driver.find_element_by_id("cn.jihaojia:id/taent_newest_layout").click()
             self.Unionpage("C1-8","新品速递")     #  #C1-8首页新品速递 更多
         else:
             print "Err,C1-8,首页新人专享,更多>文字无显示!"
             self.assertEqual(1,0,"Err,C1-8,首页新人专享,更多>文字无显示!")
         #C1-8,首页,新品速递,推荐项无显示
         sleep(3)
         if self.isElement("cn.jihaojia:id/home_item_newest_img1")==True:
             pass
         else:
             print "Err,C1-8,首页新品速递,推荐项无显示!"
             self.assertEqual(1,0,"Err,C1-8,首页新品速递,推荐项无显示!")

        #  ############################################## 写一个类
        #  #更多（推荐项合集页）的 3个检查点，标题、购物车、返回
        #  #C1-8首页新品速递 更多
        #  if self.isElement("cn.jihaojia:id/taent_newest_layout")==True:
        #      self.driver.find_element_by_id("cn.jihaojia:id/taent_newest_layout").click()
        #      #检查 标题、购物车、返回
        #      if self.driver.find_element_by_id("cn.jihaojia:id/home_title_txt").text=="新品速递":
        #          pass
        #      else:
        #          print "Err，C1-8首页新品速递 页面标题错误！！！"
        #          self.assertEqual(1,0,"Err，C1-8首页新品速递 页面标题错误！！！")
        #      #检查 购物车Icon是否存在，并点击检查（登录状态）
        #      if self.isElement("cn.jihaojia:id/trolley")==True:
        #          self.driver.find_element_by_id("cn.jihaojia:id/trolley").click()
        #          if self.driver.find_element_by_id("cn.jihaojia:id/t1").text=="购物车":
        #              self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
        #          else:
        #              print "Err，C1-8首页新品速递 购物车页面 登录界面错误！！！"
        #              #self.assertEqual(1,0,"Err，C1-8首页新品速递 购物车页面 标题错误！！！")
        #              self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
        #      else:
        #          print "Err，C1-8首页新品速递 购物车Iocn不存在！！！"
        #          self.assertEqual(1,0,"Err，C1-8首页新品速递 购物车Iocn不存在！！！")
        #      #检查 返回
        #      if self.isElement("cn.jihaojia:id/home_qrcode_img")==True:
        #           self.driver.find_element_by_id("cn.jihaojia:id/home_qrcode_img").click()
        #      else:
        #          print "Err，C1-8首页新品速递 返回按钮不存在！！！"
        #          #self.assertEqual(1,0,"Err，C1-8首页新品速递 返回按钮不存在！！！")
        #  else:
        #      print "Err，C1-8首页新品速递 更多！！！"
        #      self.assertEqual(1,0,"Err，C1-8首页新品速递 更多！！！")
        # ###################################
    def HomeS8(self):
         self.driver.swipe(800, 1600, 800, 800, 0);
         #C1-9首页达人推荐 人头Icon\达人推荐\更多
         #C1-9首页达人推荐 达人推荐文字
         if self.isElement("cn.jihaojia:id/taent_title_txt")==True:
             pass
         else:
             print "Err,C1-9,首页达人推荐,达人推荐文字无显示!"
             self.assertEqual(1,0,"Err,C1-9,首页达人推荐,达人推荐文字无显示!")

         #C1-9,首页达人推荐 更多> 文字 是否显示
         if self.isElement("cn.jihaojia:id/taent_talent_layout")==True:
             #点击更多
             self.driver.find_element_by_id("cn.jihaojia:id/taent_talent_layout").click()
             self.Unionpage("C1-9","达人推荐")     #  #C1-8首页新品速递 更多
         else:
             print "Err,C1-9,首页达人推荐,更多>文字无显示!"
             self.assertEqual(1,0,"Err,C1-8,首页达人推荐,更多>文字无显示!")
         #C1-9,首页,达人推荐,推荐项无显示
         sleep(3)
         if self.isElement("cn.jihaojia:id/home_item_talent_img2")==True:
             pass
         else:
             print "Err,C1-9,首页达人推荐,推荐项无显示!"
             self.assertEqual(1,0,"Err,C1-9,首页达人推荐,推荐项无显示!")
    def HomeS9(self):
         #C1-10首页横幅B 是否显示
         if self.isElement("cn.jihaojia:id/home_item_banners_img")==True:
             pass
         else:
             print "Err,C1-10,首页横幅B广告不存在!"
             self.assertEqual(1,0,"Err,C1-10,首页横幅B广告不存在!")
    def HomeS10(self):
         self.driver.swipe(800, 1600, 800, 800, 0);
         #C1-10首页过家家\过家家\更多
         #C1-9过家家文字
         if self.isElement("cn.jihaojia:id/life_title_txt")==True:
             pass
         else:
             print "Err,C1-10,首页过家家,过家家文字无显示!"
             self.assertEqual(1,0,"Err,C1-10,首页过家家,过家家文字无显示!")

         #C1-10,首页达人推荐 更多> 文字 是否显示
         if self.isElement("cn.jihaojia:id/life_more_layout")==True:
             #点击更多
             self.driver.find_element_by_id("cn.jihaojia:id/life_more_layout").click()
             #？self.Unionpage("C1-10","过家家")     #  #C1-8首页新品速递 更多
         else:
             print "Err,C1-9,首页达人推荐,更多>文字无显示!"
             self.assertEqual(1,0,"Err,C1-8,首页达人推荐,更多>文字无显示!")
         #C1-10,首页,过家家,推荐项无显示
         sleep(3)
         if self.isElement("cn.jihaojia:id/life_shome_image1")==True:
             pass
         else:
             print "Err,C1-10,首页过家家,推荐项无显示!"
             self.assertEqual(1,0,"Err,C1-10,首页过家家,推荐项无显示!")
    def HomeS11(self):
         self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[0].click()
         self.driver.swipe(800, 1600, 800, 800, 0);
         self.driver.swipe(800, 1600, 800, 800, 0);
         self.driver.swipe(800, 1600, 800, 800, 0);
         self.driver.swipe(800, 1600, 800, 800, 0);
         self.driver.swipe(800, 1600, 800, 800, 0);
         self.driver.swipe(800, 1600, 800, 800, 0);
         #C1-12首页横幅C广告是否显示
         if self.isElement("cn.jihaojia:id/home_item_banners_img")==True:
             pass
         else:
             print "Err,C1-12,首页横幅C广告不存在!"
             self.assertEqual(1,0,"Err,C1-12,首页横幅C广告不存在!")
         if self.driver.find_element_by_id("cn.jihaojia:id/recinnebd_title_txt").text=="猜你喜欢":
             pass
         else:
             print "Err,C1-12,首页猜你喜欢文字不存在!"
             self.assertEqual(1,0,"Err,C1-12,首页猜你喜欢文字不存在!")

    # 值得买
    def zdm(self):
         #值得买
         sleep(2)
         self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[1].click()
         self.TestcaseModule()
    def ZDMchooseGoods(self,idvalue):
         self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
         self.driver.find_element_by_id("cn.jihaojia:id/setting").click()
         sleep(4)

         #C2-1，点击商品到商品详情页
         sleep(3)
         self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[1].click()
         sleep(2)
         #self.ZDMchooseGoods_list=self.str_list[:]
         # for i in range(0,len(self.str_list)):
         #       print self.str_list[i]
         # print self.str_list[0]
         #print type(self.str_list[1])
         try:
             self.driver.find_element_by_id(idvalue).click()
             sleep(4)
         except:
             print "ZDMchooseGoods参数"+idvalue +"不存在!"
             status=0
             return status
    def ZDMgoodsToShopcar(self,GoodsQty):
         #【商品详情页】
         # C2-2，添加N个商品到购物车(参数1=件数)
         sleep(4)
         # 右上角购物车数字 ， 获取这个数字
         if self.isElement("cn.jihaojia:id/goshopnum")==True:
             tmpShopnums=self.driver.find_element_by_id("cn.jihaojia:id/goshopnum").text
         else:
             tmpShopnums=0
         # 点击“加入购物车”
         self.driver.find_element_by_id("cn.jihaojia:id/add_shoppingcart").click()
         # 点击“立即支付” self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_pay").click()
         # 购买数量 = GoodsQty
         for a in range(GoodsQty-1):
              self.driver.find_element_by_id("cn.jihaojia:id/addquantity").click()
         #确认（默认数量为1）
         self.driver.find_element_by_id("cn.jihaojia:id/confrim").click()
         sleep(3)
         if tmpShopnums==0:
             tmpShopnums=self.driver.find_element_by_id("cn.jihaojia:id/goshopnum").text
             self.assertEqual(1,int(tmpShopnums),"Err,C2-2,商品详情页,购物车数不存在!")
         else:
              sleep(3)
              tmpShopnums2=self.driver.find_element_by_id("cn.jihaojia:id/goshopnum").text
              tmpShopnums3=int(tmpShopnums)+1
              #self.assertEqual(int(tmpShopnums2),tmpShopnums3,"Err,C2-2,商品详情页,购物车商品数没刷新!")
    def ZDMcollect(self):
          #C2-3,添加商品收藏，检查是否添加成功，反选商品收藏
          self.driver.find_element_by_id("cn.jihaojia:id/collectadd").click()
          sleep(5)
          bb=0
          pw=self.driver.find_elements_by_class_name("android.view.View")
          for p1 in pw:
              if bb==8:
                  #print p1.get_attribute("name")  # =="欧式浮雕纸巾收纳盒"
                  sourcetitle=p1.get_attribute("name")
                  break
              bb=bb+1
          self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
          sleep(2)
          self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
          #Excel中直接写id
          ZDMchooseGoods_list=self.str_list[:]
          # for i in range(0,len(self.str_list)):
          #     print self.str_list[i]
          #     print type(self.str_list[i])
          self.driver.find_element_by_id(str(ZDMchooseGoods_list[0])).click()
          sleep(6)
          i=0
          if self.isElement("cn.jihaojia:id/productname")==True:
              myCollects=self.driver.find_elements_by_id("cn.jihaojia:id/productname")
              for my1 in myCollects:
                 if my1.text==sourcetitle:
                     c1=1
                     self.driver.find_elements_by_id("cn.jihaojia:id/mainLayout")[i].click() #点击收藏的商品跳转到商品详情页
                     self.driver.find_element_by_id("cn.jihaojia:id/collectadd").click() #取消收藏
                     self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
                     self.driver.swipe(600, 500, 600, 1400, 0); #下拉刷屏
                     if self.isElement("cn.jihaojia:id/productname")==True:
                       myCollects=self.driver.find_elements_by_id("cn.jihaojia:id/productname")
                       for my2 in myCollects:
                           if my2.text==sourcetitle:
                               print "Err,C2-3,商品仍在收藏夹内，未删除!"
                     else:
                         pass
                         #print "OK,收藏夹中商品已取消!"
                     break
                 else:
                   c1=0
                 i=i+1
                 sleep(3)
          else:
              print "Err,C2-3,我的收藏内无记录!"
          if c1==0:
              print "Err,C2-3,添加收藏夹失败!"
          self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
    def ZDMpay(self):
        self.ZDMchooseGoods("cn.jihaojia:id/worth_item_worry_img1")
        self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click #点击购物车
    def ZDM1(self):
        if self.ZDMchooseGoods("cn.jihaojia:id/worth_item_worry_img3")==0:
            self.assertEqual(1,0,"Err123")
        if self.ZDMchooseGoods("cn.jihaojia:id/worth_item_worry_img6")==0:
            self.assertEqual(1,0,"Err123")

    # 生活家
    def live(self):
         #生活家
         sleep(2)
         self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[2].click()
         self.TestcaseModule()

    # 搜索
    def search(self):
        #搜索
        sleep(2)
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[3].click()
        self.TestcaseModule()
    def SearchZero(self,iRow,Goodsname):
        #C4-1, 搜索商品后检查价格是否为0
        self.driver.find_element_by_id("cn.jihaojia:id/home_search_edt").click()
        self.driver.find_element_by_id("cn.jihaojia:id/action_search_edt").send_keys(Goodsname)
        self.driver.find_element_by_id("action_search_but").click()
        sleep(4)
        #验证搜索后商品的价格不能为0.0（遍历）
        s_price=self.driver.find_elements_by_id("cn.jihaojia:id/recommend_price_txt")
        for s_price1 in s_price:
            if s_price1.text=="打新价：0.0元 " or s_price1.text=="极好价：0.0元 ":
                print "Err,C4-1,搜索"+Goodsname+"后发现打新价为0元的商品"
                #break
        self.driver.find_element_by_id("cn.jihaojia:id/action_search_txt").click() #取消
        sleep(4)

    def Search1(self):
        #C4-2,【探享】，检查 抵用券抵用券Icon、购物车Icon及跳转、值得买主标签栏中T1广告位
        #检查 抵用券icon
        if self.isElement("cn.jihaojia:id/home_qrcode_img")==True:
            self.driver.find_element_by_id("cn.jihaojia:id/home_qrcode_img").click()
            if self.driver.find_element_by_id("cn.jihaojia:id/t1").text=="抵用券":
                 self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
            else:
                print "Err,C4-2,搜索页,抵用券页面不存在!"
                self.assertEqual(1,0,"Err,C4-2,搜索页,抵用券页面不存在!")
        else:
            print "Err,C4-2,搜索页抵用券icon不存在!"
            self.assertEqual(1,0,"Err,C4-2,搜索页抵用券icon不存在!")
        #检查购物车icon
        if self.isElement("cn.jihaojia:id/trolley")==True:
            self.driver.find_element_by_id("cn.jihaojia:id/trolley").click()
            if self.driver.find_element_by_id("cn.jihaojia:id/t1").text=="购物车":
                 self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
            else:
                print "Err,C4-2,搜索页,购物车页面不存在!"
                self.assertEqual(1,0,"Err,C4-2,搜索页,购物车页面不存在!")
        else:
            print "Err,C4-2,搜索页购物车icon不存在!"
            self.assertEqual(1,0,"Err,C4-2,搜索页,购物车icon不存在!")
        #检查4个主标签栏
        fourcount=0
        fourlabel=self.driver.find_elements_by_id("cn.jihaojia:id/text")
        for fourlabel1 in fourlabel:
            #print fourlabel1.text
            if fourlabel1.text=="值得买" :
                fourcount=fourcount+1
            if fourlabel1.text=="省心汇":
                fourcount=fourcount+1
            if fourlabel1.text=="过家家":
                fourcount=fourcount+1
            if fourlabel1.text=="百宝箱":
                fourcount=fourcount+1
        if fourcount<>4:
            print "Err,C4-2,搜索页,4个主标签栏显示有误!"

        # 检查值得买T1广告位是否存在?
        tmpad2=0
        tmpad=self.driver.find_elements_by_class_name("android.widget.ImageView")
        for tmpad1 in tmpad:
             Coordinate=tmpad1.location
             if Coordinate.get('x')==310 and Coordinate.get('y')==255:
                 tmpad2="True"
                 break
        if tmpad2<>"True":
            print "Err,C4-2,搜索页,值得买主标签中T1广告不存在!"
            # boss后台上线T1广告
            browser = webdriver.Firefox()
            browser.get("http://192.168.0.100:8180/login")
            nowhandle=browser.current_window_handle
            browser.find_element_by_name("account").clear() #清空输入框默认内容
            browser.find_element_by_name("account").send_keys("admin")
            browser.find_element_by_name("password").send_keys("123456")
            browser.find_element_by_class_name("login_btn").click()
            browser.get("http://192.168.0.100:8180/cms/recommend/detail/list.htm?positionCode=T1")
            allhandles=browser.window_handles
            for handle in allhandles:
                if handle != nowhandle:
                    browser.switch_to_window(handle)
            sleep(3)
            xx=browser.find_elements_by_class_name("change_href")
            pp=0
            oo=0
            for x1 in xx:
                if x1.text==u"下线":
                    pp=1
            for x2 in xx:
                if pp==0 and oo==3:
                    x2.click()
                    break
                else:
                    oo=oo+1
        # ElementSize=self.driver.find_element_by_id("cn.jihaojia:id/home_qrcode_img").size
        # print ElementSize['width'] #68
        # print ElementSize['height'] #150


##############################################################################################

    # 我的 - 我的订单
    def myOrder(self):
         #设置
         sleep(2)
         self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
         #【我的订单】
         sleep(3)
         myorders=self.driver.find_elements_by_class_name("android.widget.TextView")
         for tmpmyorder in myorders :
             try :
                  if tmpmyorder.text=="我的订单":
                      tmpmyorder.click()
             except :
                 print "第一行第四列参数错误"
         self.TestcaseModule()
    def Myorder1(self):
        #C5-A-1，验证“代付款、待发货、待收货、评价”
        self.ZDMgoodsToShopcar(2) #进入值得买页面，给购物车添加商品
        #代付款???



        #待发货 - 提交到 待收货，评价，返回评价成功页面
        myorderstatus=self.driver.find_elements_by_class_name("android.widget.TextView")
        for myorderstatus1 in myorderstatus :
            if myorderstatus1.text=="待发货" :
               myorderstatus1.click()
               break
        sleep(3)
        self.driver.find_element_by_id("cn.jihaojia:id/ordersingleimg").click() #点击商品图片
        ordercode=self.driver.find_element_by_id("cn.jihaojia:id/orderCode").text #获取订单编号
        #数据库里更新为 待收货
        try:
            conn=MySQLdb.connect(host='192.168.0.100',user='root',passwd='',db='jtx001',port=3306)
            cur=conn.cursor()
            cur.execute('update ord_order_info set order_status=4 where order_code='+ordercode)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
             print "Myorder1,Mysql Error %d: %s" % (e.args[0], e.args[1])

        self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click() #返回到我的订单

        # 待收货 - 点击确认收货，点击确定
        myorderstatus=self.driver.find_elements_by_class_name("android.widget.TextView")
        for myorderstatus2 in myorderstatus :
            if myorderstatus2.text=="待收货" :
               myorderstatus2.click()
               break
        self.driver.swipe(600, 500, 600, 1400, 0); #下拉刷屏
        sleep(3)
        #点击确认收货
        self.driver.find_elements_by_id("cn.jihaojia:id/btnstatus")[0].click()
        self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()

        #评价 - 点击评价菜单，点击评价
        myorderstatus=self.driver.find_elements_by_class_name("android.widget.TextView")
        for myorderstatus1 in myorderstatus :
            if myorderstatus1.text=="评价" :
               myorderstatus1.click()
               break
        #？刷一下页面后点击第一个评价按钮
        self.driver.swipe(600, 500, 600, 1400, 0); #下拉刷屏
        self.driver.find_elements_by_id("cn.jihaojia:id/btnstatus")[0].click() #点击评价按钮
        #【评价】
        #点击商品 跳转到商品详情页 及检测件数
        #获取件数
        tmppj1=self.driver.find_element_by_id("cn.jihaojia:id/item").text
        print tmppj1[:-1]
        #点击商品
        self.driver.find_element_by_id("cn.jihaojia:id/number_layout").click()
        #【查看商品】
        if self.driver.find_element_by_id("cn.jihaojia:id/t1").text=="查看商品":
            # 获取商品件数
            tmppj2=self.driver.find_element_by_id("cn.jihaojia:id/list_count").text
            print tmppj2[1:]
            if tmppj1[:-1]==tmppj2[1:]:
                pass
            else:
                print "Err,#C5-A-1,评价中商品件数与查看商品中件数不一致!"
            self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click() #返回到评价页面
            tmpseegoods1=self.driver.find_element_by_id("cn.jihaojia:id/list_name").text
            print tmpseegoods1
        #总体评价
        self.driver.find_element_by_id("cn.jihaojia:id/radio2").click() #中评
        self.driver.find_element_by_id("cn.jihaojia:id/evaluaterating1").click() #描述相符
        self.driver.find_element_by_id("cn.jihaojia:id/evaluaterating2").click() #产品质量
        self.driver.find_element_by_id("cn.jihaojia:id/evaluaterating3").click() #物流速度
        self.driver.find_element_by_id("cn.jihaojia:id/command").send_keys(u"这个商品确实不错，使用非常方便") #评价
        self.driver.find_element_by_id("cn.jihaojia:id/uploadpic").click() #上传凭证最多3张
        self.driver.tap([(600, 300)], 50)
        self.driver.tap([(900, 300)], 50)
        self.driver.tap([(600, 500)], 50)
        self.driver.find_element_by_id("cn.jihaojia:id/id_ok").click()
        sleep(3)
        #删除2张图
        self.driver.find_elements_by_id("cn.jihaojia:id/id_item_close")[2].click()
        self.driver.find_elements_by_id("cn.jihaojia:id/id_item_close")[1].click()
        self.driver.find_element_by_id("cn.jihaojia:id/submit").click() #提交
        #【评价成功】
        if self.driver.find_element_by_id("cn.jihaojia:id/t1").text=="评价成功":
            #验证购物车icon和跳转
            if self.isElement("cn.jihaojia:id/my_btn")==True:
                 self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click()
                 if self.driver.find_element_by_id("cn.jihaojia:id/t1").text=="购物车":
                     self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click() #返回
                     self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click() #返回
                 else:
                     print "Err,#C5-A-1,购物车页面不存在!"
                     self.assertEqual(1,0,"Err,#C5-A-1,购物车页面不存在!")
            else:
                 print "Err,#C5-A-1,评价成功,购物车icon不存在!"
        else:
            print "Err,#C5-A-1,评价成功页面不存在!"
            self.assertEqual(1,0,"Err,#C5-A-1,评价成功页面不存在!")

        if self.driver.find_element_by_id("cn.jihaojia:id/goontobuy").text=="再逛逛" and self.driver.find_element_by_id("cn.jihaojia:id/seeorder").text=="查看订单" :
            pass
        else:
            print "Err,#C5-A-1,评价成功,再逛逛和查看订单按钮不存在!"
            self.assertEqual(1,0,"Err,#C5-A-1,评价成功,再逛逛和查看订单按钮不存在!")
        self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click() #返回 我的订单
        #刷屏，检查评价记录是否还存在，应不存在。
        self.driver.swipe(600, 500, 600, 1400, 0); #下拉刷屏
        #免胶半透明立体窗花
        print self.driver.find_element_by_id("cn.jihaojia:id/productname").text
        if self.driver.find_element_by_id("cn.jihaojia:id/productname").text==tmpseegoods1 :
            pass
        else:
            print "Err,#C5-A-1,我的订单,商品评价信息仍然存在!"
            self.assertEqual(1,0,"Err,#C5-A-1,我的订单,商品评价信息仍然存在!")
    def Myorder2(self):
         #C5-A-2，验证购物车里商品数量与购物车右上角数字是否一致
         #如果无商品则去值得买添加商品
         if self.isElement("cn.jihaojia:id/goshopnum")==False:
              self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click() #返回
              sleep(2)
              if self.isElement("cn.jihaojia:id/backbtncomm")==True:
                  self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click() #返回
                  #点击值得买
                  sleep(2)
                  self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[1].click()
                  self.ZDMgoodsToShopcar(4,2)  #跳转到值得买页面添加5个商品到购物车
                  self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
                  myorders=self.driver.find_elements_by_class_name("android.widget.TextView")
                  for myorder1 in myorders :
                      if myorder1.text=="我的订单":
                           myorder1.click()
                           break
         sleep(2)
         MyOrderShopCarRightIconQTY= self.driver.find_element_by_id("cn.jihaojia:id/goshopnum").text #获取购物车右上角数字
         #self.assertEqual(int(MyOrderShopCarRightIconQTY.encode("utf-8")),4)  #将字符串转整数
         self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click() #点击购物车
         #【购物车】 （缺陷，购物车里商品不能超过一屏，否则无法统计数量，在红米手机上默认5个）
         sleep(2)
         qtys=0
         MyOrderShopCarRightIconQTY=int(MyOrderShopCarRightIconQTY.encode("utf-8"))
         if MyOrderShopCarRightIconQTY > 5 :
             tmp1=MyOrderShopCarRightIconQTY-5
             for i in range(tmp1):
                 self.Myorder3(8)
                 sleep(2)
             self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
             self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
             #进入我的订单
             myorders=self.driver.find_elements_by_class_name("android.widget.TextView")
             for myorder1 in myorders :
                 if myorder1.text=="我的订单":
                    myorder1.click()
                    break
             MyOrderShopCarRightIconQTY = self.driver.find_element_by_id("cn.jihaojia:id/goshopnum").text #获取购物车右上角数字
             MyOrderShopCarRightIconQTY = int(MyOrderShopCarRightIconQTY.encode("utf-8"))
             self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click() #点击购物车
         #购物车商品数量
         sleep(4)
         ShopCarQTYs=self.driver.find_elements_by_id("cn.jihaojia:id/shopping_checkbox")
         for ShopCarQTY in ShopCarQTYs:
              qtys=qtys+1
         self.assertEqual(MyOrderShopCarRightIconQTY,qtys)
    def Myorder3(self):
        #C5-A-3,验证是否正确删除了商品
        self.driver.swipe(800, 300, 300, 300, 0); #删除第1个商品
        self.driver.tap([(900, 300)], 50)
        self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/txt_title").text,u"确定要删除这个宝贝吗？")
        self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()
        ShopCarQTYs=self.driver.find_elements_by_id("cn.jihaojia:id/shopping_checkbox")
    def Myorder4(self,GoodsQTYs):
        self.ShopCar(GoodsQTYs)
        self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()

    # 我的 - 抵用券
    def myVoucher(self):
        #我的抵用券
        #我的
        sleep(3)
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
        sleep(2)
        #【抵用券】
        self.driver.find_element_by_id("cn.jihaojia:id/coupon_layout").click()
        sleep(4)
        self.TestcaseModule()
    def Voucher1(self):
        pass
        # #C5-B-1,输入错误抵用券，提示错误信息（暂时关闭，因为程序有bug）
        # self.driver.find_element_by_id("cn.jihaojia:id/input_recommendcode").send_keys("12345678")
        # self.driver.find_element_by_id("cn.jihaojia:id/dialog_button_ok").click()
        # if "兑换码错误" not in self.driver.find_element_by_id("cn.jihaojia:id/txt_title").text :
        #     print "Err，#C5-B-1,输入错误抵用券，提示错误信息!"
        #     self.assertEqual(1,0,"Err")
        # sleep(2)
        # self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()
    def Voucher2(self,vouchernum):
        #C5-B-2,输入正确抵用券 (数据库自动生成抵用券)
        ###############优惠券商品
        # select * from mmp_coupon_info;
        # insert into mmp_coupon_info(coupon_title,coupon_describe,item_code,coupon_status,coupon_type,member_type,begin_time,end_time,coupon_condition,quantity,price,not_free,limit_num,coupon_count,disabled,create_time,create_user,update_time,update_user) values("自动化测试1","说明文字2",1151112198658006,1,1,0,now(),"2016-12-10 19:00:04",1,1,12.30,1,1,23,0,now(),"[运营]5",now(),"[运营]5");
        #Mysql 建立数据库,数据库使用UTF-8
        # 自此问题应该能全部解决 , 如还出现编码错误,
        #修改/usr/lib/python2.4/site-packages/MySQLdb/cursors.py
        #原来是:
        #charset = db.character_set_name()
        #query = query.encode(charset)
        #修改为:
        #query = query.encode('utf-8')
        sleep(3)
        try:
            #vouchernum="123456789"
            conn=MySQLdb.connect(host='192.168.0.100',user='root',passwd='',db='jtx001',port=3306, use_unicode=True)
            cur=conn.cursor()
            conn.set_character_set('utf8')
            cur.execute('SET NAMES utf8;')
            cur.execute('SET CHARACTER SET utf8;')
            cur.execute('SET character_set_connection=utf8;')
            user1=u"[运营]5"
            title1=u"自动化抵用券"
            titledesc1=u"用于自动化测试"
            # 清除 数据库中测试抵用券
            cur.execute('delete from mmp_coupon_item_sku where coupon_id=22')
            cur.execute('delete from mmp_coupon_info where coupon_id=22')
            cur.execute('delete from mmp_coupon_info_detail where coupon_id=22')
            # 生成 数据库中测试抵用券
            cur.execute('insert into mmp_coupon_info_detail(coupon_no,disable,coupon_id,create_user,update_time,update_user,create_time) values("%s",0,22,"%s",now(),"%s",now())' % (vouchernum ,user1 ,user1))
            cur.execute('insert into mmp_coupon_info(coupon_id,coupon_title,coupon_describe,item_code,coupon_status,coupon_type,member_type,begin_time,end_time,coupon_condition,quantity,price,not_free,limit_num,coupon_count,disabled,create_time,create_user,update_time,update_user) values(22,"%s","%s",1151124176072657,1,1,0,now(),"2016-12-10 19:00:04",0,1,12.30,1,1,23,0,now(),"%s",now(),"%s")' % (title1,titledesc1,user1 ,user1))
            cur.execute(' insert into mmp_coupon_item_sku(coupon_id,item_code,sku_code,quantity,create_time,update_time) values(22,1151124176072657,2151124176072663,13,now(),now())')
            cur.execute(' insert into mmp_coupon_item_sku(coupon_id,item_code,sku_code,quantity,create_time,update_time) values(22,1151124176072657,2151124176072664,7,now(),now())')
            cur.execute(' insert into mmp_coupon_item_sku(coupon_id,item_code,sku_code,quantity,create_time,update_time) values(22,1151124176072657,2151124176072665,9,now(),now())')
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
             print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        sleep(2)
        self.driver.find_element_by_id("cn.jihaojia:id/input_recommendcode").send_keys(vouchernum)
        self.driver.find_element_by_id("cn.jihaojia:id/dialog_button_ok").click()

        if "添加至我的抵用券" not in self.driver.find_element_by_id("cn.jihaojia:id/pay").text :
             print "Err，C5-B-2,添加至我的抵用券显示错误!"
             self.assertEqual(1,0,"Err")
        sleep(3)
        title2=self.driver.find_element_by_id("cn.jihaojia:id/text").text
        titledesc2=self.driver.find_element_by_id("cn.jihaojia:id/time").text
        #print titledesc2
        self.driver.find_element_by_id("cn.jihaojia:id/pay").click()  #添加至我的抵用券
        sleep(3)
        # #使用抵用券 ，先验证抵用券title2和titledesc2
        tmpVoucher=self.driver.find_elements_by_id("cn.jihaojia:id/coupon_name")
        tmp1=0
        for tmpVoucher1 in tmpVoucher:
            if tmpVoucher1.text==title2:
                 tmp1=1
        if tmp1<>1:
             print "Err，C5-B-2,抵用券,名称显示错误!"
        tmpVoucher=self.driver.find_elements_by_id("cn.jihaojia:id/coupon_time")
        tmp1=0
        for tmpVoucher2 in tmpVoucher:
            if tmpVoucher2.text==titledesc2:
                tmp1=2
            #print tmpVoucher2.text
        if tmp1<>2:
             print "Err，C5-B-2,抵用券,有效期显示错误!"
        #写死定位到坐标，点击 自动化抵用券
        self.driver.tap([(800, 1200)], 50)
        sleep(3)
        if "立即使用" not in self.driver.find_element_by_id("cn.jihaojia:id/pay").text :
             print "Err，C5-B-2,礼品券,立即使用按钮文字显示错误!"
             self.assertEqual(1,0,"Err")
        sleep(6)
        self.driver.find_element_by_id("cn.jihaojia:id/pay").click() #立即使用
        sleep(3)
        self.driver.find_element_by_id("cn.jihaojia:id/confrim").click()
        self.driver.find_element_by_id("cn.jihaojia:id/shopping_checkbox").click() #单选 抵用券商品
        #验证抵用券商品价格 与 总计价格是否一致，同时去结算为1
        diyongquanjiage=self.driver.find_element_by_id("cn.jihaojia:id/couponDes").text #此商品仅需付款12.3元
        #截取获取价格 12.3
        y=diyongquanjiage[7:]
        diyongquanjiage1=self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_money").text
        if y[:-1]<>diyongquanjiage1[1:]:
            print "Err,抵用券价格与总计价格不相等!"
        self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_pay").click() #去结算
        sleep(3)
        self.driver.find_element_by_id("cn.jihaojia:id/pay").click() #立即支付
        sleep(4)
        self.PayWayPing("1")
        sleep(3)
        self.driver.find_element_by_id("cn.jihaojia:id/backimage").click()
        sleep(3)
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
        sleep(2)
        #【抵用券】
        self.driver.find_element_by_id("cn.jihaojia:id/coupon_layout").click()
        if self.isElement("cn.jihaojia:id/past_start")==False:
              print "Err,C5-B-2,抵用券,未显示已使用!"
              self.assertEqual(1,0,"Err")
        self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()

    # 我的 - 常用联系人/地址
    def myAddress(self):
         #常用联系人地址
         sleep(3)
         self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
         sleep(2)
         self.driver.find_element_by_id("cn.jihaojia:id/address").click()
         sleep(4)
         self.TestcaseModule()
         #self.ContactAddress()
    def Myaddress1(self):
         #C5-C-1,新增地址，若地址个数小4个则新增直到等于4个。
         AddressNums=self.driver.find_elements_by_id("cn.jihaojia:id/addres_name")
         AddressCounts=0
         for AddressNum in AddressNums:  #遍历常用地址个数
              AddressCounts=AddressCounts+1
         #新增1个地址
         #添加地址，点击+
         self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click()
         #随机生成1个四位数
         b_list = range(1000,5000)
         b_list_int = random.sample(b_list,1)
         for jj in range(0,b_list_int.__len__()):
              b_list_int[jj] = str(b_list_int[jj])
              self.driver.find_element_by_id("cn.jihaojia:id/reciver").send_keys(u"令狐冲"+"".join(b_list_int))
              self.driver.find_element_by_id("cn.jihaojia:id/mobile").send_keys("1381610"+"".join(b_list_int))
              self.driver.find_element_by_id("android:id/text1").click()
              Revtimes=self.driver.find_elements_by_id("android:id/text1")
              for Revtime in Revtimes:  #周一至周五收货、周六日节假日收货
                  if Revtime.text=="收货时间不限":
                      Revtime.click()
                      break
              self.driver.find_element_by_id("cn.jihaojia:id/region_layout").click()
              sleep(2)
              # #红米5.0.2
              self.driver.swipe(300, 1150, 300, 680, 0); #省 上海
              self.driver.swipe(500, 1000, 500, 900, 0); #市 上海市内
              self.driver.swipe(800, 1000, 800, 800, 0); #区 徐汇区
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()
              self.driver.find_element_by_id("cn.jihaojia:id/detail_addres").send_keys(u"上海浦东南路100号")
              self.driver.find_element_by_id("cn.jihaojia:id/savebtn").click()

         #如果地址数量小于4个，则继续新增，直到4个为止。
         for i in range(5):
             if AddressCounts < 4:
                  #添加地址，点击+
                  self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click()
                  #随机生成1个四位数
                  b_list = range(1000,5000)
                  b_list_int = random.sample(b_list,1)
                  for jj in range(0,b_list_int.__len__()):
                       b_list_int[jj] = str(b_list_int[jj])
                  self.driver.find_element_by_id("cn.jihaojia:id/reciver").send_keys(u"令狐冲"+"".join(b_list_int))
                  self.driver.find_element_by_id("cn.jihaojia:id/mobile").send_keys("1381610"+"".join(b_list_int))
                  self.driver.find_element_by_id("android:id/text1").click()
                  Revtimes=self.driver.find_elements_by_id("android:id/text1")
                  for Revtime in Revtimes:  #周一至周五收货、周六日节假日收货
                      if Revtime.text=="收货时间不限":
                         Revtime.click()
                         break
                  self.driver.find_element_by_id("cn.jihaojia:id/region_layout").click()
                  sleep(2)
                  #yeshen
                  # self.driver.swipe(150, 700, 150, 600, 0); #省 山西
                  # self.driver.swipe(300, 700, 300, 600, 0); #市 大同
                  # self.driver.swipe(500, 720, 500, 590, 0); #区 南郊
                  # #红米5.0.2
                  self.driver.swipe(300, 1150, 300, 680, 0); #省 上海
                  self.driver.swipe(500, 1000, 500, 900, 0); #市 上海市内
                  self.driver.swipe(800, 1000, 800, 800, 0); #区 徐汇区
                  sleep(2)
                  self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()
                  self.driver.find_element_by_id("cn.jihaojia:id/detail_addres").send_keys(u"上海浦东南路100号")
                  self.driver.find_element_by_id("cn.jihaojia:id/savebtn").click()
                  AddressCounts=AddressCounts+1
             else:
                 break
    def Myaddress2(self):
         #C5-C-2,删除第4个地址 （默认删除从左到右，从上到下）
         sleep(2)
         self.driver.tap([(800, 800)], 3000)
         #确定要删除这个地址吗？
         if "确定要删除这个地址吗" not in self.driver.find_element_by_id("cn.jihaojia:id/txt_title").text :
             print "err,确定要删除这个地址吗提示信息错误!"
             self.assertEqual(1,0,"Err，提示信息显示错误！！！")
         self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()
    def Myaddress3(self):
         #C5-C-3,设置默认地址，默认在第一二个之间切换
         sleep(3)
         XYdict=self.driver.find_element_by_id("cn.jihaojia:id/addres_start").location
         if XYdict.get('x') == 448 :
              self.driver.tap([(800, 500)], 50) #点击第二个地址
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click() #设为默认
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
              sleep(3)
              XYdict=self.driver.find_element_by_id("cn.jihaojia:id/addres_start").location
              if XYdict.get('x') == 448 :
                  print "Err,C5-C-3,第二个地址右上角没有默认字样!"
                  self.assertEqual(1,0,"Err")
         else:
              self.driver.tap([(200, 500)], 50) #点击第一个地址
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click() #设为默认
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
              sleep(3)
              XYdict=self.driver.find_element_by_id("cn.jihaojia:id/addres_start").location
              if XYdict.get('x') == 980 :
                  print "Err,C5-C-3,第一个地址右上角没有默认字样!"
                  self.assertEqual(1,0,"Err")
         self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()

    # 我的 - 我的购物车
    def myShopcar(self):
         sleep(2)
         self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
         sleep(2)
         myshopcars=self.driver.find_elements_by_class_name("android.widget.TextView")
         for myshopcar1 in myshopcars :
            if myshopcar1.text=="我的购物车" :
               myshopcar1.click()
               break
         sleep(3)
         self.TestcaseModule()
    def ShopCarToPay(self,goodsqty):
        #C5-D-1,To account and pay at my shopcar  测试流程是我的购物车、去结算、支付方式、支付成功
        #【购物车】
        #默认检查标题
        self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/t1").text,"购物车")
        # 1、当购物车为空，默认检查提示信息（空）、去逛逛按钮 ，点击去逛逛跳转值得买页面添加商品到购物车。
        if self.isElement("cn.jihaojia:id/shoping_cart_pay")==False:
            self.assertEqual(self.driver.find_elements_by_class_name("android.widget.TextView")[1].text,"您的购物车还是空荡荡的")
            self.assertEqual(self.driver.find_element_by_class_name("android.widget.Button").text,"去逛逛")
            if self.driver.find_element_by_class_name("android.widget.Button").text=="去逛逛":
                #点击去逛逛 ，跳转到值得买
                self.driver.find_element_by_class_name("android.widget.Button").click()
                sleep(3)
                self.driver.find_element_by_id("cn.jihaojia:id/worth_item_advertis1").click()
                self.GoodsDetails("5",goodsqty)  #值得买，添加1个商品goodsqty数量件，并立即支付
                sleep(5)
                #【支付】 - 选择支付方式 跳转到第三方Ping++
                self.driver.find_element_by_id("cn.jihaojia:id/pay").click()
                self.PayWayPing("1") # 支付
                self.PaySuccess("1") # 支付成功
            else:
                print "Err,购物车,去逛逛按钮不存在!"

    def ShopCarToElements(self,goodsqty):
        #【支付】
        #C5-D-2,检查支付页面各元素，如 个人信息、商品名、价格、数量、选择数量、订单总计、运费、金额、选择支付方式
        sleep(3)
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[1].click()
        self.driver.find_element_by_id("cn.jihaojia:id/worth_item_advertis1").click()
        self.GoodsDetails("5",goodsqty)  #商品详情页，添加1个商品N数量件，点击立即支付，跳转到支付页面
        #【支付】- 获取地址 - 管理地址
        # 1,获取当前地址信息（名字、电话、地址、收货时间），核对变更后地址信息刷新情况
        tmp1=self.driver.find_element_by_id("cn.jihaojia:id/Verify_name").text #我的拉力
        tmp2=self.driver.find_element_by_id("cn.jihaojia:id/Verify_phone").text #13816109050
        tmp3=self.driver.find_element_by_id("cn.jihaojia:id/Verify_add").text  #河北唐山路南区
        tmp4=self.driver.find_element_by_id("cn.jihaojia:id/Verify_adddetail").text #浦东东方路100
        tmp5=self.driver.find_element_by_id("cn.jihaojia:id/Verify_takeTime").text #收货时间不限
        self.driver.find_element_by_id("cn.jihaojia:id/addressadd").click()
        # 调用 常用地址（管理）
        (a,b,c,d,e) = self.AddressManager("2",tmp1) #切换地址
        sleep(3)
        tmp1=self.driver.find_element_by_id("cn.jihaojia:id/Verify_name").text #我的拉力
        tmp2=self.driver.find_element_by_id("cn.jihaojia:id/Verify_phone").text #13816109050
        tmp3=self.driver.find_element_by_id("cn.jihaojia:id/Verify_add").text  #河北唐山路南区
        tmp4=self.driver.find_element_by_id("cn.jihaojia:id/Verify_adddetail").text #浦东东方路100
        tmp5=self.driver.find_element_by_id("cn.jihaojia:id/Verify_takeTime").text #收货时间不限
        if a==tmp1 and b==tmp2 and c==tmp3 and d==tmp4 and e==tmp5:
            pass
        else:
            print "Err,支付,个人信息有误!"
        # 2,商品名、价格、数量、选择数量、订单总计、运费、金额、选择支付方式
        self.driver.find_element_by_id("cn.jihaojia:id/pay_name").text
        sgnPrice=self.driver.find_element_by_id("cn.jihaojia:id/money").text  #¥ 12.6
        #print sgnPrice[2:]
        defaultQty=self.driver.find_element_by_id("cn.jihaojia:id/number").text   #X 2
        #print defaultQty[2:]
        # 选择数量
        chooseQty=self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_number").text
        if defaultQty[2:]<>chooseQty:
            print "Err,支付，默认商品数量与选择数量不一致!"
        # 选择数量 点击+号
        self.driver.find_element_by_id("cn.jihaojia:id/cart_texts").click()
        defaultQty1=self.driver.find_element_by_id("cn.jihaojia:id/number").text   #X 3
        #print defaultQty1[2:]
        chooseQty1=self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_number").text #X 3
        if defaultQty1[2:]<>chooseQty1:
            print "Err,支付,选择数量新增1后数量与商品数量不一致!"
        # 订单总计
        orderTotal=self.driver.find_element_by_id("cn.jihaojia:id/pay_money").text   #¥43.8
        #print orderTotal[1:]

        # 验证 运费规则:
        # 1、地区是上海安徽浙江苏州，订单金额大于等于69元包邮，否则运费6元。
        # 2、除以上地区，订单金额额大于等于129元包邮，否则运费9元。
        info2=self.driver.find_element_by_id("cn.jihaojia:id/Verify_add").text
        if "上海" in info2 or "安徽" in info2 or "浙江" in info2 or "苏州" in info2:
            if round(orderTotal[1:],2) >= 69 :
                if "0.0" not in self.driver.find_element_by_id("cn.jihaojia:id/freightSubtatal").text:
                    print "Err,支付,江浙沪地区金额超过69元没包邮!"
            else :
                if "6.0" not in self.driver.find_element_by_id("cn.jihaojia:id/freightSubtatal").text:
                    print "Err,支付,江浙沪地区金额低于69元运费显示不是6元!"
        else :
            if round(orderTotal[1:],2) >= 129 :
                if "0.0" not in self.driver.find_element_by_id("cn.jihaojia:id/freightSubtatal").text:
                    print "Err,支付,其他地区金额超过129元没包邮!"
            else :
                if "9.0" not in self.driver.find_element_by_id("cn.jihaojia:id/freightSubtatal").text:
                    print "Err,支付,其他地区金额低于129元运费显示不是9元!"

        # 获取运费
        includeFare=self.driver.find_element_by_id("cn.jihaojia:id/freightSubtatal").text   #(含6.0运费)
        #print includeFare
        tmpincludeFare=includeFare[2:]
        #print tmpincludeFare[:-3] #6.0
        # 计算 单价*选择数量+运费
        calCash=float(sgnPrice[2:]) * int(chooseQty1)+ float(tmpincludeFare[:-3])
        #print calCash
        if  calCash <> float(orderTotal[1:]) :
            print tmpincludeFare[:-3]
            print sgnPrice[3:]
            print defaultQty[2:]
            print orderTotal[1:]
            print "Err,支付，单价*数量+运费不等于订单总计!"
        #金额
        money=self.driver.find_element_by_id("cn.jihaojia:id/money_number").text   #¥43.8
        #print money[1:]
        if float(money[1:]) <> float(orderTotal[1:]) :
            print money[2:]
            print orderTotal[1:]
            print "Err,支付,订单总计与金额不一致!"

        tmpPaySuccess=self.driver.find_elements_by_class_name("android.widget.TextView")
        tmp=0
        for tmpPaySuccess1 in tmpPaySuccess:
            if tmpPaySuccess1.text=="选择支付方式":
                tmp=tmp+1
            if  tmpPaySuccess1.text=="支付宝客户端支付":
                tmp=tmp+1
            if tmpPaySuccess1.text=="推荐安装支付宝客户端的用户使用":
                tmp=tmp+1
            if tmpPaySuccess1.text=="微信支付":
                tmp=tmp+1
            if tmpPaySuccess1.text=="推荐安装微信5.0以上版本的使用":
                tmp=tmp+1
            #print tmpPaySuccess1.text
        if tmp<>5:
            print "Err,支付,选择支付方式、支付宝客户端支付、微信支付文字显示有误!"

    def AddressManager(self,operate,name):
        #【常用地址】，参数name = 用户名
        # 默认检查标题
        # operate 1=返回（原路径） 、2=切换、3=新增并管理
        sleep(3)
        if self.driver.find_element_by_id("cn.jihaojia:id/t1").text<>"常用地址":
            print "Err,常用地址,标题不存在!"
        if operate=="1":
            self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
        if operate=="2":
            # 获取 第一排2个用户的用户名、电话、区、地址、收货时间
            tmpa1=[]
            tmpb1=[]
            tmpc1=[]
            tmpd1=[]
            tmpe1=[]
            tmpName=self.driver.find_elements_by_id("cn.jihaojia:id/addres_consignee")
            for tmpName1 in tmpName:
                tmpa1.append(tmpName1.text)
            tmpPhonee=self.driver.find_elements_by_id("cn.jihaojia:id/addres_phone")
            for tmpPhonee1 in tmpPhonee:
                tmpb1.append(tmpPhonee1.text)
            tmpProvince=self.driver.find_elements_by_id("cn.jihaojia:id/addres_province")
            for tmpProvince1 in tmpProvince:
                tmpc1.append(tmpProvince1.text)
            tmpSpecifically=self.driver.find_elements_by_id("cn.jihaojia:id/addres_specifically")
            for tmpSpecifically1 in tmpSpecifically:
                tmpd1.append(tmpSpecifically1.text)
            tmpTime=self.driver.find_elements_by_id("cn.jihaojia:id/deliveryTime")
            for tmpTime1 in tmpTime:
                tmpe1.append(tmpTime1.text)
            #检查支付页面中用户名是否与常用地址第一排2个中用户名一致，如一致则点击另一个用户名
            if tmpa1[0]==name:
                self.driver.tap([(800, 500)], 50) #点击第2个地址
                return tmpa1[1],tmpb1[1],tmpc1[1],tmpd1[1],tmpe1[1]
            if tmpa1[1]==name:
                self.driver.tap([(300, 500)], 50) #点击第1个地址
                return tmpa1[0],tmpb1[0],tmpc1[0],tmpd1[0],tmpe1[0]
            sleep(3)

        if operate=="3":
            pass

        # #C?,选择所有商品，检查总计单选框为自动选中。 ???总计单选框选中后checked仍然是false （暂停）
        # tmpAllradios=0
        # Allradios=self.driver.find_elements_by_id("cn.jihaojia:id/shopping_checkbox")
        # for Allradio in Allradios:
        #     self.driver.find_elements_by_id("cn.jihaojia:id/shopping_checkbox")[tmpAllradios].click()
        #     sleep(2)
        #     tmpAllradios=tmpAllradios+1
        # sleep(5)
        #print self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_button").get_attribute("checked")
        #C?,反选总计单选框，检查所有商品单选框为全部为反选。(暂停)
        #C?,勾选总计单选框，反选1个商品单选框，检查总计单选框为反选。（暂停）
        #ZDMsymbol1=0

    def ttt(self,goodsqty):
        ZDMsymbol1=0
        #获取购物车右上角商品数
        ShopCarQTYs=self.driver.find_elements_by_id("cn.jihaojia:id/shopping_checkbox")
        qtys=0
        for ShopCarQTY in ShopCarQTYs:
            qtys=qtys+1
        #C5-D-1，我的购物车、去结算、支付方式
        #选择商品（或多个），验证商品（价格*数量）的总价与总计、去结算是否一致
        #对选择的商品进行遍历，计算商品的合计，并将所有商品合计累加
        for i in range(goodsqty):  #range(2)=0,1
            self.driver.find_elements_by_id("cn.jihaojia:id/shopping_checkbox")[i].click()
            sleep(2)
        #价格
            SinglePrices=self.driver.find_elements_by_id("cn.jihaojia:id/shoping_money")
            tmp1=tmp2=0
            for SinglePrice in SinglePrices :
               if tmp1==i :  #累加2个价格之和
                  SglPrs=float(SinglePrice.text.replace("¥",""))
                  #self.assertEqual(float(SinglePrice.text.replace("¥","")),27.6)  #27.6
                  break
               tmp1=tmp1+1
            sleep(2)
        #数量
            SingleQtys=self.driver.find_elements_by_id("cn.jihaojia:id/shoping_cart_number")
            for SingleQty in SingleQtys :
                if tmp2==i :
                   SglNum=int(SingleQty.text)
                   #self.assertEqual(int(SingleQty.text),5)  #5
                   break
                tmp2=tmp2+1
            sleep(2)
        #所有商品累加价格验证
            ShopCarMoney=self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_money").text
            SglTotal = SglPrs * SglNum
            AllTotal = AllTotal + SglTotal
            QJSSglNum = QJSSglNum + SglNum

        self.assertEqual(float(ShopCarMoney.replace("¥","")),round(AllTotal,2))
        #去结算
        QJSNums=self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_pay").text
        tmp111=int(QJSNums.replace("去结算(","").replace(")",""))
        self.assertEqual(tmp111,QJSSglNum)
        # #newbk1 =copy(self.newbk)
        # newWs1=self.newbk.get_sheet(1)  # 0=sheet1 ,1=sheet2 以此类推
        # newWs1.write(4, 0, "OK")
        # self.newbk.save(self.fname)

        self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_pay").click()
        ###############################################################################################
        #【确认订单】
        self.driver.find_element_by_id("cn.jihaojia:id/iv_indext").click() #点击收货人信息

        #【常用地址】
        self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click()  #点击管理
        #self.ContactAddress()
        self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
        #C2,切换默认地址，验证地址是否及时更新 ，定位默认第一个商品
        XYdict1=self.driver.find_element_by_id("cn.jihaojia:id/addres_start").location #默认
        if XYdict1.get('x') == 448 :
              sleep(2)
              tmp5=0
              t1s=self.driver.find_elements_by_id("cn.jihaojia:id/addres_consignee") #收货人
              for t1 in t1s:
                  if tmp5==1:
                      tt1=t1.text
                      break
                  tmp5=tmp5+1
              tmp5=0
              t2s=self.driver.find_elements_by_id("cn.jihaojia:id/addres_phone") #手机号码
              for t2 in t2s:
                  if tmp5==1:
                      tt2=t2.text
                      break
                  tmp5=tmp5+1
              tmp5=0
              t3s=self.driver.find_elements_by_id("cn.jihaojia:id/addres_province") #所在地区
              for t3 in t3s:
                  if tmp5==1:
                      tt3=t3.text
                      break
                  tmp5=tmp5+1
              tmp5=0
              t4s=self.driver.find_elements_by_id("cn.jihaojia:id/addres_specifically") #详细地址
              for t4 in t4s:
                  if tmp5==1:
                      tt4=t4.text
                      break
                  tmp5=tmp5+1
              tmp5=0
              t5s=self.driver.find_elements_by_id("cn.jihaojia:id/deliveryTime") #收货时间
              for t5 in t5s:
                  if tmp5==1:
                      tt5=t5.text
                      break
                  tmp5=tmp5+1
              self.driver.tap([(800, 500)], 50) #点击第二个地址
              sleep(2)
              #C2,验证以上5个信息是否及时更新
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_name").text,tt1)
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_phone").text,tt2)
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_add").text,tt3)
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_adddetail").text,tt4)
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_takeTime").text,tt5)
        else:
              sleep(2)
              t1s=self.driver.find_elements_by_id("cn.jihaojia:id/addres_consignee") #收货人
              for t1 in t1s:
                   tt1=t1.text
                   break
              t2s=self.driver.find_elements_by_id("cn.jihaojia:id/addres_phone") #手机号码
              for t2 in t2s:
                   tt2=t2.text
                   break
              t3s=self.driver.find_elements_by_id("cn.jihaojia:id/addres_province") #所在地区
              for t3 in t3s:
                   tt3=t3.text
                   break
              t4s=self.driver.find_elements_by_id("cn.jihaojia:id/addres_specifically") #详细地址
              for t4 in t4s:
                   tt4=t4.text
                   break
              t5s=self.driver.find_elements_by_id("cn.jihaojia:id/deliveryTime") #收货时间
              for t5 in t5s:
                   tt5=t5.text
                   break
              #yeshen
              self.driver.tap([(300, 500)], 50) #点击第一个地址
              sleep(2)
              #C2,验证以上5个信息是否及时更新
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_name").text,tt1)
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_phone").text,tt2)
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_add").text,tt3)
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_adddetail").text,tt4)
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_takeTime").text,tt5)
        sleep(5)
        Verify_name=self.driver.find_element_by_id("cn.jihaojia:id/Verify_name").text
        Verify_phone=self.driver.find_element_by_id("cn.jihaojia:id/Verify_phone").text
        Verify_add=self.driver.find_element_by_id("cn.jihaojia:id/Verify_add").text
        Verify_adddetail=self.driver.find_element_by_id("cn.jihaojia:id/Verify_adddetail").text
        #【确认订单】
        # 验证 商品件数，订单总计，运费，金额
        #此处android上测试存在Bug以下语句暂时屏蔽，选择5个商品11件，但确认订单页面缺显示5件，应该是11件。
        #self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/item").text,str(QJSSglNum)+"件") #验证商品件数


        # 验证 运费规则:
         # 1、地区是上海安徽浙江苏州，订单金额大于等于69元包邮，否则运费6元。
         # 2、除以上地区，订单金额额大于等于129元包邮，否则运费9元。
        OrderTotal=0
        Yunfei=0.0
        info2=self.driver.find_element_by_id("cn.jihaojia:id/Verify_add").text
        if "上海" in info2 or "安徽" in info2 or "浙江" in info2 or "苏州" in info2:
            if round(AllTotal,2) >= 69 :
                 self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/freight").text,"0.0")  #0
                 OrderTotal=round(AllTotal,2)
            else :
                 self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/freight").text,"6.0")  #6元
                 Yunfei=6.0
                 OrderTotal=round(AllTotal,2)+Yunfei
        else :
            if round(AllTotal,2) >= 129 :
                 self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/freight").text,"0.0")  #0
                 OrderTotal=round(AllTotal,2)
            else :
                 self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/freight").text,"9.0")  #9元
                 Yunfei=9.0
                 OrderTotal=round(AllTotal,2)+Yunfei

        self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/sumprice").text,"¥"+ str(OrderTotal)) #验证订单总计=购物车合计价格+运费
        Sumprice=self.driver.find_element_by_id("cn.jihaojia:id/sumprice").text
        Worth=self.driver.find_element_by_id("cn.jihaojia:id/worth").text
        #self.assertEqual(Sumprice,Worth) #验证订单总计=金额（￥22.8）

        #【确认订单】 选择支付方式
        # 选择支付方式 0=支付宝 ， 1=微信   # self.PayWay(0)
        self.driver.find_element_by_id("cn.jihaojia:id/pay").click()
        sleep(3)
        self.PayWayPing("1")
        #self.driver.find_element_by_id("cn.jihaojia:id/backimage").click()
        #self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click() # 我的

        #【订单详情】
        # 验证右上角购物车数量，如支付前是5，对2个商品进行支付，取消支付后应该是3
        if self.isElement("cn.jihaojia:id/goshopnum")==False:
           print "\n【Warning，购物车内已无商品，请及时添加商品】"
        else:
           ShopCarQTYs= self.driver.find_element_by_id("cn.jihaojia:id/goshopnum").text
           self.assertEqual(int(ShopCarQTYs.encode("utf-8")),qtys-goodsqty) #购物车数量减去已下订单的数量

        # 验证商品总价、运费、待支付
        #总价 cn.jihaojia:id/realprice $36.0
        Realprice= self.driver.find_element_by_id("cn.jihaojia:id/realprice").text #总价
        OrderActuallyAmount= self.driver.find_element_by_id("cn.jihaojia:id/orderActuallyAmount").text #待支付427.2
        self.assertEqual(Sumprice,Realprice) #验证订单总计=总价
        self.assertEqual(Worth,"¥"+ OrderActuallyAmount) #验证总价=待支付
        #运费 cn.jihaojia:id/freightSubtatal 6.0
        FreightSubtatal= self.driver.find_element_by_id("cn.jihaojia:id/freightSubtatal").text  #0.0
        self.assertEqual(Yunfei,round(float(FreightSubtatal),1))
        # str(OrderTotal)
        # 验证收货人信息
        Reciver =self.driver.find_element_by_id("cn.jihaojia:id/reciver").text
        phone=self.driver.find_element_by_id("cn.jihaojia:id/phone").text
        reciveradd=self.driver.find_element_by_id("cn.jihaojia:id/reciveradd").text
        self.assertEqual(Reciver,Verify_name) #验证收货人
        self.assertEqual(phone,Verify_phone)  #验证电话号码
        self.assertEqual(reciveradd,Verify_add+Verify_adddetail) #验证收货地址 = 所在地区+详细地址

        # 记录订单信息
        #self.driver.find_element_by_id("cn.jihaojia:id/orderCode").text #1160225176177285
        #self.driver.find_element_by_id("cn.jihaojia:id/ordertime").text  #下单时间:2016-02-25 11:14

        # 第一种，不点击立即支付，返回购物车
        if ZDMsymbol1==1:
            self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()  # 回退到购物车
            self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()  # 回退到商品详情
            self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()  # 回退到值得买页面
            self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click() # 我的
        else:
            self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()  # 回退到购物车
            self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()  # 回退到我的页面

        # # 第二种，点击立即支付  继续支付
        # self.driver.find_element_by_id("cn.jihaojia:id/btndetail").click()  # 立即支付
        # sleep(2)
        # #【支付】
        # self.driver.find_element_by_id("cn.jihaojia:id/pay").click()  # 立即支付
        # #? 调用支付宝支付宝操作
        # #【订单详情】
        # self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()  # 回退到订单详情
        # self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()  # 回退到购物车
        # # 选择支付方式 0=支付宝 ， 1=微信
        # self.PayWay(1)

    # 我的  - 设置
    def mySetup(self):
         #设置
         sleep(2)
         #self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
         self.TestcaseModule()
    def MySetupLogin(self):
        # 我的设置 - 自动登录用户
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
        sleep(2)
        if self.isElement("cn.jihaojia:id/loginpic")==True :
            self.driver.find_element_by_id("cn.jihaojia:id/loginpic").click()
            self.Login("13816103333")
            sleep(4)
    def MySetupAccount(self):
         ##################
         #C6-2,设置中检查账号资料、头像图、昵称、性别
         sleep(3)
         self.driver.find_element_by_id("cn.jihaojia:id/setting").click()
         self.driver.find_element_by_id("cn.jihaojia:id/headpicrela").click()
         a = Jhj15_mysetup(self.driver)
         a.accountdata("Linghuchong")
    def MySetupAboutus(self):
        #关于我们
        self.driver.find_element_by_id("cn.jihaojia:id/jihaojia").click()
        b = Jhj15_mysetup(self.driver)
        b.aboutus()
    def MySetupExitLogin(self):
        #C6-4 我的设置-注销账号
        self.driver.find_element_by_id("cn.jihaojia:id/logout").click()
        if self.isElement("cn.jihaojia:id/loginpic")==True:
            pass
        else:
            print "Err,C6-4,注销后返回界面错误!"
    def Login(self,mobilephone):
        #C6-1 我的设置-获取验证码并自动登录
        self.driver.find_element_by_id("cn.jihaojia:id/gaga_login_account_edit").send_keys(mobilephone)
        self.driver.find_element_by_id("cn.jihaojia:id/codeButton").click()
        sleep(3)
        try:
            conn=MySQLdb.connect(host='192.168.0.100',user='root',passwd='',db='jtx001',port=3306)
            cur=conn.cursor()
            intmobilephone=int(mobilephone)
            cur.execute('select datas from cmn_short_message where mobiles=(%d) order by create_time desc' % intmobilephone)
            aa=cur.fetchone()
            bb="".join(tuple(aa))  #将元组转字符串
            #"".join(list(s)) 将列表转字符串
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
             print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        self.driver.find_element_by_id("cn.jihaojia:id/more_regist_email_edit").send_keys(bb[0:4])
        self.driver.find_element_by_id("cn.jihaojia:id/gaga_login").click()

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

    def Unionpage(self,codenum,title1):
         #self.unionpage(self,"C1-5","新人专享")
         #更多（推荐项合集页）的 3个检查点，标题、购物车、返回
         #检查 标题
         if self.driver.find_element_by_id("cn.jihaojia:id/home_title_txt").text==title1:
             pass
         else:
             print "Err,"+codenum+",首页"+title1+",推荐项合集页,"+title1+"标题错误!"
             self.assertEqual(1,0,"Err,"+codenum+",首页"+title1+",推荐项合集页,"+title1+"标题错误!")
         #检查 购物车Icon是否存在，并点击检查（登录状态）
         if self.isElement("cn.jihaojia:id/trolley")==True:
             self.driver.find_element_by_id("cn.jihaojia:id/trolley").click()
             sleep(2)
             #如果是登录界面则报错
             if self.isElement("cn.jihaojia:id/gaga_login_account_edit")==True:
                 print "Err,"+codenum+",首页"+title1+",购物车页面跳转到登录界面错误!"
                 self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
             else:
                 self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
         else:
             print "Err,"+codenum+",首页"+title1+",购物车Iocn不存在!"
             self.assertEqual(1,0,"Err,"+codenum+",首页"+title1+",购物车Iocn不存在!")
         #检查 返回
         if self.isElement("cn.jihaojia:id/home_qrcode_img")==True:
              self.driver.find_element_by_id("cn.jihaojia:id/home_qrcode_img").click()
         else:
             print "Err,"+codenum+",首页"+title1+",返回按钮不存在!"
    #公共支付方式 ，choiceone =0 支付宝 ， =1 微信
    def PayWay(self,choiceone):
        if choiceone == 0:
            #支付宝客户端支付
            self.driver.find_element_by_id("cn.jihaojia:id/zhifubaobtn").click()
            self.driver.find_element_by_id("cn.jihaojia:id/pay").click()  #立即支付
            sleep(5)
            # 正式支付宝支付平台
            self.driver.find_element_by_id("cn.jihaojia:id/backimage").click()#支付成功
            sleep(3)
            #【支付宝页面】
            self.driver.find_element_by_class_name("android.widget.Button").click() #点击返回
            sleep(2)
            self.driver.find_element_by_class_name("android.widget.ImageView").click()
            sleep(3)
            self.driver.find_element_by_id("android:id/button1").click()
        else:
            #微信支付
            self.driver.find_element_by_id("cn.jihaojia:id/wxpaybth").click()
            self.driver.find_element_by_id("cn.jihaojia:id/pay").click()  #立即支付
            sleep(5)
            #【微信页面】
            self.driver.find_element_by_id("com.tencent.mm:id/cdh").click() #点击关闭
    #模拟支付空间Ping++支付
    def PayWayPing(self,paystatus):
            #测试第三方支付控件ping++
            sleep(6)
            if paystatus=="1":
               self.driver.tap([(560,1100)], 50) #点击付款
            if paystatus=="2":
               self.driver.tap([(560,1314)], 50) #点击取消
            if paystatus=="3":
               self.driver.tap([(560,1465)], 50) #点击失败
            sleep(3)

    def GoodsDetails(self,operate,goodsqty):
         #【商品详情页】
         # operate 0=获取商品详情页具体数据、1=分享 、2=购物车商品数、3=收藏、4=加入购物车、5=立即支付
         sleep(3)
         # 获取 页面中商品名 和 单价
         if operate=="0":
             self.driver.find_element_by_id("cn.jihaojia:id/collectadd").click()
             sleep(3)
             #已知商品名是第八个，单价第九个
             tmp=0
             tmpGoodsDetails=self.driver.find_elements_by_class_name("android.view.View")
             for tmpGoodsDetails1 in tmpGoodsDetails:
                if tmp==8:
                    GoodsDetailsName=tmpGoodsDetails1.get_attribute("name") #压花条纹抗菌马桶垫
                if tmp==9:
                    tmpGoodsDetailsPrice=tmpGoodsDetails1.get_attribute("name") #¥12.60¥18.00
                    GoodsDetailsPrice=tmpGoodsDetailsPrice.split("¥",2)[1] #12.60
                    break
                tmp=tmp+1
             print GoodsDetailsName
             print GoodsDetailsPrice
         # 点击 “分享”
         if operate=="1":
             pass
         # 获取页面右上角购物车商品数
         if operate=="2":
             #判断是否存在这个数字，当购物车为空时，为空；
             if self.isElement("cn.jihaojia:id/goshopnum")==True:
                 tmpshopcarnums=self.driver.find_element_by_id("cn.jihaojia:id/goshopnum").text
             else:
                 tmpshopcarnums=0
         # 点击“收藏”
         if operate=="3":
             self.driver.find_element_by_id("cn.jihaojia:id/collectadd").click()
         # 点击“加入购物车”
         if operate=="4":
             self.driver.find_element_by_id("cn.jihaojia:id/add_shoppingcart").click()
             # 选择购买数量
             for a in range(goodsqty-1):
                 self.driver.find_element_by_id("cn.jihaojia:id/addquantity").click()
             self.driver.find_element_by_id("cn.jihaojia:id/confrim").click()
             sleep(3)
         # 点击“立即支付”
         if operate=="5":
             self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_pay").click()
             # 选择购买数量
             for a in range(goodsqty-1):
                 self.driver.find_element_by_id("cn.jihaojia:id/addquantity").click()
             self.driver.find_element_by_id("cn.jihaojia:id/confrim").click()
             sleep(3)
    def Pay(self,operate):
        #【支付】  过程：选择商品，点击立即支付，点击确定。
        # 默认检查标题
        # operate 1=返回（原路径返回）、2=个人信息、3=检查商品名、单价、选择数量、订单总计、金额 、4=选择支付方式 、5=立即支付
        sleep(3)
        if self.driver.find_element_by_id("cn.jihaojia:id/t1").text<>"支付":
            print "Err,支付,标题不存在!"
        #点击“返回”
        if operate=="1":
             self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
        #??个人信息
        if operate=="2":
             pass
        #检查商品名、单价、选择数量、订单总计、金额
        if operate=="3":
            pass
        #选择支付方式
        if operate=="4":
            pass
        #立即支付
        if operate=="5":
            self.driver.find_element_by_id("cn.jihaojia:id/pay").click()
    def OrderDetails(self,operate):
        #【订单详情】  过程：立即支付，点击“取消”或“失败”后的订单详情页
        # operate 1=返回（原路径返回到订单详情）、2=检查标题、商品名、单价、总价、运费、收货人信息、订单信息、待支付金额、3=立即支付
        pass
    def PayCancel(self,operate):
        #【支付】 ，过程：支付时选择了取消后再点击立即支付
        # operate 1=返回（原路径）、2=检查标题、订单总结、金额、选择支付方式、3=立即支付
        pass
    def PaySuccess(self,operate):
        #【支付成功】  过程：商品详情页中立即支付
        # 默认检查标题、提示信息
        # operate 1=返回（原路径） 、2=点击查看订单（跳转到我的订单）、3=再逛逛(跳转到值得买页面)
        sleep(3)
        if self.driver.find_element_by_id("cn.jihaojia:id/t1").text<>"支付成功":
            print "Err,支付成功,标题不存在!"
        tmpPaySuccess=self.driver.find_elements_by_class_name("android.widget.TextView")
        tmp=0
        for tmpPaySuccess1 in tmpPaySuccess:
             if tmpPaySuccess1.text=="支付成功":
                 tmp=tmp+1
             if  tmpPaySuccess1.text=="感谢您对别人家的支持":
                 tmp=tmp+1
        if tmp<>3: #页面中有2个支付成功
            print "Err,支付成功,提示信息有误!"
        #点击“返回”
        if operate=="1" :
            self.driver.find_element_by_id("cn.jihaojia:id/backimage").click()
        #点击“查看订单”
        if operate=="2":
            self.driver.find_element_by_id("cn.jihaojia:id/gotoOrder").click()
            sleep(3)
            # 跳转到我的订单，默认标签（全部）
            if self.driver.find_element_by_id("cn.jihaojia:id/t1").text<>"我的订单":
                print "Err,支付成功,标题不存在!"
        #点击“再逛逛”
        if operate=="3":
            if self.driver.find_element_by_class_name("android.widget.Button").text<>"再逛逛":
                print "Err,支付成功,再逛逛按钮不存在!"
            else:
                self.driver.find_element_by_class_name("android.widget.Button").click()
            sleep(3)
            #跳转到值得买页面
            if self.driver.find_element_by_id("cn.jihaojia:id/home_title_txt").text<>"值得买":
                print "Err,支付成功,跳转到值得买,值得买标题不存在!"

    #判断元素是否存在
    def isElement(self,locate):
        flag = False
        try:
            self.driver.find_element_by_id(locate)
            flag = True
        except :
            flag = False
        return flag
    #判断元素是否存在，不存在则截屏并存入excel，注意运行的函数必须增加IRow，如self.SearchZero(18,u"抽屉")，EXcel第19行。
    def isElementScreenShot(self,locate):
        flag = False
        flagfile=""
        try:
            self.driver.find_element_by_id(locate)
            flag = True
        except :
            flag = False
            flagfile=u"%s.png" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
            self.driver.get_screenshot_as_file(Err_Screenshot+flagfile)
        return flag,flagfile

if __name__ == '__main__':
    # unittest.main() # 用这个是最简单的，下面的用法可以同时测试多个类
    # unittest.TextTestRunner(verbosity=2).run(suite1) # 这个等价于上述但可设置verbosity=2，省去了运行时加-v
    suite1 = unittest.TestLoader().loadTestsFromTestCase(Jhj1_5) # 构造测试集
    # suite1=unittest.TestSuite()
    # suite1.addTest(Jhj1_5("SearchZero"))
    # suite1.addTest(Jhj1_5("Search1"))
    # 输出HTML报告
    # now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    # filename = 'C:\\Python27\\TMPappium\\report\\'+now+'result.htm'
    # fp = file(filename,'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(
    #     stream = fp,title=u'极好家V1.5自动化测试报告',description=u'用例执行情况：'
    # )
    # runner.run(suite1)
    #unittest.TextTestRunner(verbosity=2).run(suite1)
    unittest.TextTestRunner(verbosity=2).run(suite1) # 执行测试
    # suite2 = unittest.TestLoader().loadTestsFromTestCase(JHJ1_6) # 可以增加多个类，如Jhj1_5
    # allTests = unittest.TestSuite([suite1,suite2]) #执行多个类的Testcase
    # unittest.TextTestRunner(verbosity=2).run(allTests)
    # eg.http://canlynet.iteye.com/blog/1671750



#TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")
class Appium_Extend(object):
    def __init__(self, driver):
        self.driver = driver
    def get_screenshot_by_custom_size(self, start_x, start_y, end_x, end_y):
        #自定义截取范围
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)

        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        return self
    def write_to_file( self, dirPath, imageName, form = "png"):
        #将截屏文件复制到指定目录下
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        shutil.copyfile(TEMP_FILE, PATH(dirPath + "/" + imageName + "." + form))
    def load_image(self, image_path):
        #加载目标图片供对比用
        if os.path.isfile(image_path):
            load = Image.open(image_path)
            return load
        else:
            raise Exception("%s is not exist" %image_path)
    #http://testerhome.com/topics/202
    def same_as(self, load_image, percent):
        #对比图片，percent值设为0，则100%相似时返回True，设置的值越大，相差越大
        import math
        import operator

        image1 = Image.open(TEMP_FILE)
        image2 = load_image

        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2, \
                                                         histogram1, histogram2)))/len(histogram1))
        if differ <= percent:
            return True
        else:
            return False



