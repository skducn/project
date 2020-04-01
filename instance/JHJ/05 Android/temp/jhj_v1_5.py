# coding: utf-8
import os
import sys
import unittest
from appium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import xlwt
import xlrd
import MySQLdb
from xlutils.copy import copy
from pyh import *
import win32api
import win32con
import platform
import tempfile
import shutil

from PIL import Image

########## 极好家V1.5 ##########
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

class Jhj1_5(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appPackage'] = 'cn.jihaojia'
        desired_caps['appActivity'] = 'cn.jihaojia.activity.GuidanceActivity'
        desired_caps['unicodeKeyboard'] ='True'
        desired_caps['resetKeyboard'] = 'True'
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        fname = "E:/51/01_Project/JHJ/JHJ_Case/jhj_1_2.xls"
        self.fname=fname
        bk = xlrd.open_workbook(fname,"formatting_info=1")
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
    def test_Main(self):
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
                           print "这是最后一行TestCase"
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
                   for m in range(5,20):
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
                   except:
                       print "Err,第"+str(l+1)+"行,"+self.sh2.cell_value(l,3)
                       newWs=self.newbk.get_sheet(1)
                       newWs.write(l,0,"error",self.styleE)
                       self.newbk.save(self.fname)


    def homepage(self):
         #首页
         self.TestcaseModule()

    def zdm(self):
         #值得买
         sleep(2)
         #self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[1].click()
         self.TestcaseModule()
        #

    def live(self):
         #生活家
         sleep(3)
         self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[2].click()
         self.TestcaseModule()

    def search(self):
        #搜索
        sleep(4)
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[3].click()
        self.TestcaseModule()


    def SearchZero(self,Goodsname):
        #C4-1, 搜索商品后检查价格是否为0
        self.driver.find_element_by_id("cn.jihaojia:id/home_search_edt").click()
        self.driver.find_element_by_id("cn.jihaojia:id/action_search_edt").send_keys(Goodsname)
        self.driver.find_element_by_id("action_search_but").click()
        #验证搜索后商品的价格不能为0.0（遍历）
        s_price=self.driver.find_elements_by_id("cn.jihaojia:id/recommend_price_txt")
        for s_price1 in s_price:
            if s_price1.text=="打新价：0.0元 ":
                print "Err,C4-1,搜索"+Goodsname+"后发现打新价为0元的商品"
                #break
        self.driver.find_element_by_id("cn.jihaojia:id/action_search_txt").click() #取消
        sleep(6)

    def Search1(self):
        #C4-2, 检查抵用券和购物车2个icon跳转及值得买T1广告位
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
        #检查值得买T1广告位?未做



    def mySetup(self):
         #设置
         self.TestcaseModule()

    def Hometop3(self):
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




    def ZDMchooseGoods(self,idvalue):
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
         #C2-2，添加1个商品到购物车(参数1=件数)
         sleep(4)
         if self.isElement("cn.jihaojia:id/goshopnum")==True:
             tmpShopnums=self.driver.find_element_by_id("cn.jihaojia:id/goshopnum").text
         else:
             tmpShopnums=0
         self.driver.find_element_by_id("cn.jihaojia:id/add_shoppingcart").click() #加入购物车
         for a in range(GoodsQty-1):
              self.driver.find_element_by_id("cn.jihaojia:id/addquantity").click() #商品+1
         self.driver.find_element_by_id("cn.jihaojia:id/confrim").click() #确认（默认数量为1）
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
          self.driver.find_element_by_id("cn.jihaojia:id/collectadd").click()
          sleep(3)
          pw=self.driver.find_elements_by_class_name("android.view.View")
          for p1 in pw:
              if bb==9:
                  print p1.get_attribute("name")  # =="欧式浮雕纸巾收纳盒"
                  sourcetitle=p1.get_attribute("name")
                  break

          self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
          sleep(2)
          self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
          #Excel中直接写id
          ZDMchooseGoods_list=self.str_list[:]
          # for i in range(0,len(self.str_list)):
          #     print self.str_list[i]
          #     print type(self.str_list[i])
          self.driver.find_element_by_id(str(ZDMchooseGoods_list[0])).click()
          sleep(3)
          myCollects=self.driver.find_elements_by_id("cn.jihaojia:id/productname")
          for my1 in myCollects:
               if my1.text==sourcetitle:
                   c1=1
                   break
               else:
                   c1=0
               my1.click()
               #再次反向验证商品详情页中商品标题是否与收藏夹中标题一致
               sleep(3)
               bb=0
               pw=self.driver.find_elements_by_class_name("android.view.View")
               for p1 in pw:
                   if bb==9:
                      print p1.get_attribute("name")  # =="欧式浮雕纸巾收纳盒"
                      sourcetitle=p1.get_attribute("name")
                      break
               if my1.text==sourcetitle:
                   print "ok"
               else:
                   print "error,1213"
               self.driver.find_element_by_id("cn.jihaojia:id/collectadd").click()
               self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
               self.driver.swipe(600, 500, 600, 1400, 0); #下拉刷屏

          if c1==0:
              print "err"









    def ZDM1(self):
        if self.ZDMchooseGoods("cn.jihaojia:id/worth_item_worry_img3")==0:
            self.assertEqual(1,0,"Err123")
        if self.ZDMchooseGoods("cn.jihaojia:id/worth_item_worry_img6")==0:
            self.assertEqual(1,0,"Err123")






    def MySetupLogin(self):
        # 我的设置 - 自动登录用户
        sleep(3)
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
        sleep(2)
        self.driver.find_element_by_id("cn.jihaojia:id/setting").click()
        self.Login("13816103333")
        sleep(5)

    def MySetupExitLogin(self):
        #C6-2 我的设置-注销账号
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
        sleep(2)
        self.driver.find_element_by_id("cn.jihaojia:id/setting").click()
        self.driver.find_element_by_id("cn.jihaojia:id/logout").click()

    ##########################################################################################


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

        # sleep(3)
        # if self.driver.find_element_by_id("cn.jihaojia:id/t1").text =="设置" :
        #     pass
        # else:
        #      print "Err，C6-1获取验证码并自动登录失败！！！"
        #      self.assertEqual(1,0,"Err，C6-1获取验证码并自动登录失败！！！")


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
        #进入值得买页面，给购物车添加商品
        self.ZDMgoodsToShopcar(2)
        #代付款
        #待发货，提交到 待收货，评价，返回评价成功页面
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

        # 待收货，点击确认收货，点击确定
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

        #点击评价菜单，点击评价
        #评价
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

    #我的抵用券
    def myVoucher(self):
        #我的
        sleep(3)
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
        sleep(2)
        #【抵用券】
        self.driver.find_element_by_id("cn.jihaojia:id/coupon_layout").click()
        sleep(4)
        self.TestcaseModule()

    def Voucher1(self):
        #C5-B-1,输入错误抵用券，提示错误信息
        self.driver.find_element_by_id("cn.jihaojia:id/input_recommendcode").send_keys("12345678")
        self.driver.find_element_by_id("cn.jihaojia:id/dialog_button_ok").click()
        if "兑换码错误" in self.driver.find_element_by_id("cn.jihaojia:id/txt_title").text :
            pass
        else :
            self.assertEqual(1,0,"Err，抵用券提示信息显示错误！！！")
            print "Err，抵用券提示信息显示错误！！！"
        sleep(2)
        self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()

    def Voucher2(self):
        #C5-B-2,输入正确抵用券
        self.driver.find_element_by_id("cn.jihaojia:id/input_recommendcode").send_keys("12345678")
        self.driver.find_element_by_id("cn.jihaojia:id/dialog_button_ok").click()
        if "兑换码错误" in self.driver.find_element_by_id("cn.jihaojia:id/txt_title").text :
             #self.assertEqual(1,0,"Err，抵用券提示信息显示错误！！！")
             print "Err，C5-B-2,抵用券提示信息显示错误！！！"
        else :
             pass
        self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()
        sleep(2)
        self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()



    #我的常用联系人地址
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
         #C5-C-1,新增地址，获取常用地址个数，如果个数小4个则循环新增，直到大于等于4个
         AddressNums=self.driver.find_elements_by_id("cn.jihaojia:id/addres_name")
         AddressCounts=0
         for AddressNum in AddressNums:  #遍历常用地址个数
              AddressCounts=AddressCounts+1
         for i in range(5):
             if AddressCounts < 4:
                  #添加地址，点击+
                  self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click()
                  self.driver.find_element_by_id("cn.jihaojia:id/reciver").send_keys(u"令狐冲")
                  self.driver.find_element_by_id("cn.jihaojia:id/mobile").send_keys("13816109050")
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
         self.driver.tap([(800, 800)], 3000)
         #确定要删除这个地址吗？
         if "确定要删除这个地址吗" in self.driver.find_element_by_id("cn.jihaojia:id/txt_title").text :
            self.assertEqual(1,1,"OK，提示信息显示正确")
         else :
            self.assertEqual(1,0,"Err，提示信息显示错误！！！")
         self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()

    def Myaddress3(self):
         #C5-C-3,设置默认地址，默认在第一二个之间切换
         XYdict=self.driver.find_element_by_id("cn.jihaojia:id/addres_start").location
         if XYdict.get('x') == 448 :
              self.driver.tap([(800, 500)], 50) #点击第二个地址
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click() #设为默认
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
              sleep(3)
              XYdict=self.driver.find_element_by_id("cn.jihaojia:id/addres_start").location
              if XYdict.get('x') != 448 :
                 self.assertEqual(1,1,"OK，默认地址切换正确")
              else :
                 self.assertEqual(1,0,"Err，第二个地址右上角没有默认字样！！！")
         else:
              self.driver.tap([(200, 500)], 50) #点击第一个地址
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click() #设为默认
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
              sleep(3)
              XYdict=self.driver.find_element_by_id("cn.jihaojia:id/addres_start").location
              if XYdict.get('x') != 980 :
                 self.assertEqual(1,1,"OK，默认地址切换正确")
              else :
                 self.assertEqual(1,0,"Err，第一个地址右上角没有默认字样！！！")
         self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()

    #我的购物车
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

    #公共 我的购物车
    def ShopCar(self,goodsqty):
         #【购物车】
         #遍历选择1个或多个商品
        AllTotal = QJSSglNum = 0
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

        #如果购物车为空，则先到值得买首页添加5个商品到购物车。
        ZDMsymbol1=0
        if self.isElement("cn.jihaojia:id/shoping_cart_pay")==False:
            #验证 购物车文字、提示信息文字、去逛逛按钮 是否存在
            self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/t1").text,"购物车")
            self.assertEqual(self.driver.find_elements_by_class_name("android.widget.TextView")[1].text,"您的购物车还是空荡荡的")
            self.assertEqual(self.driver.find_element_by_class_name("android.widget.Button").text,"去逛逛")
            ZDMsymbol1=1
            self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click() #返回
            sleep(2)
            if self.isElement("cn.jihaojia:id/backbtncomm")==True:
                self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click() #返回
            #点击值得买
            sleep(2)
            self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[1].click()
            self.ZDMgoodsToShopcar(5)  #跳转到值得买页面添加5个商品到购物车
        #获取购物车右上角商品数
        ShopCarQTYs=self.driver.find_elements_by_id("cn.jihaojia:id/shopping_checkbox")
        qtys=0
        for ShopCarQTY in ShopCarQTYs:
            qtys=qtys+1
        #C1-3,选择商品（或多个），验证商品（价格*数量）的总价与总计、去结算是否一致
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
        # 验证运费，规则是
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
        self.assertEqual(Sumprice,Worth) #验证订单总计=金额（￥22.8）

        #【确认订单】 选择支付方式
        # 选择支付方式 0=支付宝 ， 1=微信
        self.PayWay(0)
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

    #公共 支付方式
    def PayWay(self,choiceone):
        if choiceone == 0:
            #支付宝客户端支付
            self.driver.find_element_by_id("cn.jihaojia:id/zhifubaobtn").click()
            self.driver.find_element_by_id("cn.jihaojia:id/pay").click()  #立即支付
            sleep(5)
            #测试第三方支付控件ping++
            self.driver.tap([(560,1100)], 50) #点击付款
            #【支付成功】
            self.driver.find_element_by_id("cn.jihaojia:id/gotoOrder").click() #点击查看订单
            #验证待发货

            #self.driver.tap([(560,1314)], 50) #点击取消
            #self.driver.tap([(560,1465)], 50) #点击失败
            sleep(111)

            #正式支付宝支付平台
            #self.driver.find_element_by_id("cn.jihaojia:id/backimage").click()#支付成功
            #sleep(3)
            #【支付宝页面】
            #self.driver.find_element_by_class_name("android.widget.Button").click() #点击返回
            #sleep(2)
            #self.driver.find_element_by_class_name("android.widget.ImageView").click()
            #sleep(3)
            #self.driver.find_element_by_id("android:id/button1").click()
        else:
            #微信支付
            self.driver.find_element_by_id("cn.jihaojia:id/wxpaybth").click()
            self.driver.find_element_by_id("cn.jihaojia:id/pay").click()  #立即支付
            sleep(5)
            #【微信页面】
            self.driver.find_element_by_id("com.tencent.mm:id/cdh").click() #点击关闭
    #判断元素不存在
    def isElement(self,locate):
        flag = False
        try:
            self.driver.find_element_by_id(locate)
            flag = True
        except :
            flag = False
        return flag



if __name__ == '__main__':
## 对多个不同类进行测试    
    suite1 = unittest.TestLoader().loadTestsFromTestCase(Jhj1_5)
##    suite2 = unittest.TestLoader().loadTestsFromTestCase(MainTest2)
##    allTests = unittest.TestSuite([suite1,suite2])
##    unittest.TextTestRunner(verbosity=2).run(allTests)
    unittest.TextTestRunner(verbosity=2).run(suite1)


PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")

class Appium_Extend(object):
    def __init__(self, driver):
        self.driver = driver

    def get_screenshot_by_element(self, element):
        #先截取整个屏幕，存储至系统临时目录下
        self.driver.get_screenshot_as_file(TEMP_FILE)

        #获取元素bounds
        location = element.location
        size = element.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])

        #截取图片
        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        return self

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



## unittest https://docs.python.org/2/library/unittest.html
##可以使用unitest.skip装饰器族跳过test method或者test class,这些装饰器包括:
##① @unittest.skip(reason):无条件跳过测试，reason描述为什么跳过测试
##② @unittest.skipif(conditition,reason):condititon为true时跳过测试
##③ @unittest.skipunless(condition,reason):condition不是true时跳过测试
    # @unittest.skipIf(os.path.isfile("~/1.txt") != True , "can't find files) #带条件判断
##数字变为字符串 str(4)
##字符串变为数字 string.atoi(s,[，base]) //base为进制基数
##浮点数转换 string.atof(s)
##字符转数字 int(str)
#         eq = urllib2.Request("http://www.163.com/")##这里可以换成http://www.baidu.com,http://www.sohu.com
# content = urllib2.urlopen(req).read()
# typeEncode = sys.getfilesystemencoding()##系统默认编码
# infoencode = chardet.detect(content).get('encoding','utf-8')##通过第3方模块来自动提取网页的编码
# html = content.decode(infoencode,'ignore').encode(typeEncode)##先转换成unicode编码，然后转换系统编码输出
# print html

         # xy=sys.getfilesystemencoding() #mbcs
         # page = PyH('JHJ_V1.2_抵用券')
         # oo='OK，提示信息显示正'
         # pp=chardet.detect(oo).get('encoding','unicode')
         # kk=oo.decode().encode(pp)
         # page << h2(kk)
         # page.printOut('123.html')

    #import chardet
#print chardet.detect('中国')
#self.driver.open_notifications()
#print self.driver.network_connection
#写文件
# f=file("c:\hello.sql","w+")
# li=["use jtx001;\n","update ord_order_info set order_status=4 where order_code=1160308816769009;"]
# f.writelines(li)
# f.close()
# import commands
# commands.getstatusoutput('mysql -h192.168.0.100 -uroot < c:\hello.sql')
#os.popen('mysql -h192.168.0.100 -uroot < c:\hello.sql')
#os.system('notepad')