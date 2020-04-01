# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: android自动化测试 for 2.0
# pip install -U selenium
# pip install Appium-Python-Client
#***************************************************************


import os,sys,unittest,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis,commands
from appium import webdriver
# from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
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
import subprocess,re

# from Public.PageObject.BasePage import *

# os.system("appium -p 4723")


# 初始化参数化
varExcel = os.path.abspath(r"dangjian1.5.xls")
# varReport = "/Users/linghuchong/Downloads/51/Project/CJL/report/CJLreport1_0.html"
varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取当天日期时间,格式：20161020130318
bk = xlrd.open_workbook(varExcel, formatting_info=True)
newbk = copy(bk)
sheetMain = bk.sheet_by_name("main")
sheetTestCase = bk.sheet_by_name("testcase")
styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')


# # 获取包的Package 和 LaunchActivityName
# appLocation = '/Users/linghuchong/Desktop/PartyBuilding1.5.6_test.apk'
# devicesinfo1 = subprocess.Popen("aapt dump badging {}".format(appLocation),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
# devicesinfo2 = devicesinfo1.stdout.read()
# print devicesinfo2
# PackageName = devicesinfo2.split(" versionCode")[0].replace("package: name=","").replace("'","")
# LaunchActivityName = devicesinfo2.split("launchable-activity: name='")[1].split("'")[0]

# from uiautomator import Device


# 获取手机制造商信息,  如 adb shell getprop | grep "model\|version.sdk\|manufacturer\|hardware\|platform\|revision\|serialno\|product.name\|brand"
androidVersion = commands.getoutput('adb shell getprop ro.build.version.release')
androidSerialno = commands.getoutput('adb shell getprop ro.serialno')

# android
desired_caps = {}
# desired_caps['automationName'] = 'Selendroid'
# desired_caps['automationName'] = 'UiAutomator2'
# npm install appium-uiautomator2-drvapp
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = str(androidVersion.strip())  # '4.4'   # str(float(androidVersion[0:3]))
desired_caps['deviceName'] = androidSerialno
# desired_caps['app'] = '/Users/linghuchong/Downloads/51/android/dangjian/PartyBuilding1.0.0_prod.apk'
desired_caps['appPackage'] = 'com.cetc.partybuilding' #PackageName
desired_caps['appActivity'] = "com.cetc.partybuilding.activity.InitActivity"  # LaunchActivityName  #
desired_caps['unicodeKeyboard'] = 'True'
desired_caps['resetKeyboard'] = 'True'
desired_caps['recreateChromeDriverSessions'] = 'true'

drvapp = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
reload(sys)
sys.setdefaultencoding('utf8')
# BasePage_PO = BasePage(drvapp)



print ">" * 150
# 手机信息定义与输出 , 定义手机分辨率的宽,高
screenX = drvapp.get_window_size()['width']
screenY = drvapp.get_window_size()['height']
tmpProductmodel = commands.getoutput('adb shell getprop ro.product.model')
tmpProductdevice = commands.getoutput('adb shell getprop ro.product.device')
tmpSdk = commands.getoutput('adb shell getprop ro.build.version.sdk')
tmpAbi = commands.getoutput('adb shell getprop ro.product.cpu.abi')
tmpSerialno = commands.getoutput('adb shell getprop ro.serialno')
productmodel = tmpProductmodel.strip()
# print "测试机品牌 = " + str(tmpProductmodel.strip()) + " , 设备号 = " + str(
#     tmpProductdevice.strip()) + " , 分辨率 = " + str(screenX) + "*" + str(
#     screenY) + " , Android版本 = " + str(androidVersion.strip()) + " , SDK = " + str(
#     tmpSdk.strip()) + " , CPU = " + str(tmpAbi.strip()) + " , SerialNo = " + str(tmpSerialno.strip())

print "测试机 = " + str(tmpProductmodel.strip()) + " , 分辨率 = " + str(screenX) + "*" + str(
    screenY) + " , Android版本 = " + str(androidVersion.strip()) + " , SDK = " + str(
    tmpSdk.strip())


class AppDangjian(unittest.TestCase):

    def runTest(self):
        pass

    @classmethod
    def setUpClass(self):
        print "12121212"

    @classmethod
    def tearDownClass(self):
        drvapp.quit()
    def test_Main(self):
        for i in range(1, sheetMain.nrows):
            if sheetMain.cell_value(i, 0) == "Y":
                self.Maincol1 = sheetMain.cell_value(i, 1)
                self.Maincol2 = sheetMain.cell_value(i, 2)
                exec(sheetMain.cell_value(i, 4))
    def TestcaseModule(self):
         # 遍历TestCase及调用函数模块,定位测试用例位置及数量
         case1 = caseN = 0
         for j in range(1, sheetTestCase.nrows):
              case1 = case1 + 1
              if sheetTestCase.cell_value(j, 2) == self.Maincol1:
                  for k in range(case1+1, 100):  # 假设有100个Case
                      if k + 1 > sheetTestCase.nrows:  # 最后一行
                           caseN = caseN + 1
                           break
                      elif sheetTestCase.cell_value(k, 1) == "" and sheetTestCase.cell_value(k, 2) == "":
                           caseN = caseN + 1
                      elif sheetTestCase.cell_value(k, 1) == "skip":
                           caseN = caseN + 1
                      else:
                           caseN = caseN + 1
                           break
                  break
         if self.Maincol2 == "skip":
             case1 = case1 + 1
             caseN = caseN - 1

         #遍历 Testcase1~TestCaseN
         for l in range(case1, caseN+case1):
              str_list = []
              for m in range(7, 30):  # id0 - id16
                  if sheetTestCase.cell(l, m).value != "":
                      N = sheetTestCase.cell_value(l, m)
                      if "=" in N:
                          N = sheetMain.cell_value(1, 5) + ":" + N
                      str_list.append(str(N))
                  else:
                      break
              self.str_list = str_list
              # try :
              if sheetTestCase.cell_value(l, 1) == "skip":
                  newWs = newbk.get_sheet(1)
                  newWs.write(l, 0, "skip", styleGray25)
                  newbk.save(varExcel)
              elif sheetTestCase.cell_value(l, 5) == "":
                  pass
              else:
                  self.l = l
                  exec(sheetTestCase.cell_value(l, 5))
                  newWs=newbk.get_sheet(1)
                  newWs.write(l, 0, varTimeYMDHSM, styleBlue)
                  newbk.save(varExcel)
              # except:
              print "Errorrrrrrr , Excel("+str(l+1)+") , " + sheetTestCase.cell_value(case1, 2) + " , " + sheetTestCase.cell_value(l, 3) + " , " +sheetTestCase.cell_value(l, 4) + " , " +sheetTestCase.cell_value(l, 5)
              newWs = newbk.get_sheet(1)
              newWs.write(l, 0, varTimeYMDHSM, styleRed)
              newbk.save(varExcel)

    def find_toast(self, message):
         # '''''判断toast信息'''
         try:
             element = WebDriverWait(drvapp, 2).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, message)))
             return True
         except:
             return False

    def _find_toast(self, message, timeout, poll_frequency, drvapp):
         message = '//*[@text=\'{}\']'.format(message)
         try:
             # element = WebDriverWait(drvapp,timeout,poll_frequency).until(expected_conditions.presence_of_element_located((By.XPATH,message)))
             # print element
             element1 = WebDriverWait(drvapp, 2).until(
                 EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, message)))
             print element1
             return True
         except:
             return False
             # self.find_toast("登录成功")

    # 登录

    def drv_login(self):
        self.TestcaseModule()

    def shellClick(self,dx,dy):
        # 直接用adb来点击触发
        os.popen("adb shell input tap " + str(dx) + " " + str(dy))

    def shellSwipe(self, x0, y0,x1,y1):
        # 直接用adb来点击触发
        os.popen("adb shell input swipe " + str(x0) + " " + str(y0) + " " + str(x1) + " " + str(y1))
        sleep(2)

    def login(self, varUser, varPass):
        # if .isElementId("com.cetc.partybuilding:id/et_phonenum_login"):
        sleep(6)
        # d = Device('c2f8b67a')
        # x = d.info
        # print x
        # from jsonrpc2 import JsonRpc
        # d(resourceId="com.cetc.partybuilding:id/et_phonenum_login").set_text(u"13636371320")
        # d(resourceId="com.cetc.partybuilding:id/et_psw_login").set_text(u"123456")
        # sleep(1212)
        drvapp.find_element_by_id("com.cetc.partybuilding:id/et_phonenum_login").send_keys(varUser)
        drvapp.find_element_by_id("com.cetc.partybuilding:id/et_psw_login").send_keys(varPass)
        drvapp.find_element_by_id("com.cetc.partybuilding:id/btn_login").click()
        sleep(4)

        # 学习计划
        drvapp.find_element_by_id("com.cetc.partybuilding:id/learn_plan").click()
        sleep(2)
        drvapp.find_element_by_id("com.cetc.partybuilding:id/listview").find_element_by_xpath("//android.widget.LinearLayout[contains(@index,1)]").click()
        sleep(3)


        # 点击任务
        # self.shellSwipe("300","600","300","600")
        drvapp.find_element_by_id("com.cetc.partybuilding:id/ll_subject_item").click()
        sleep(6)

        # 收藏任务
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/nav_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").click()

        # # 等待8s，打印播放时间，暂停。
        # sleep(8)
        # print drvapp.find_element_by_id("com.cetc.partybuilding:id/current_time_tv").text
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/play_btn").click()
        # sleep(3)
        self.shellSwipe("600", "300", "600", "300")

        contexts = drvapp.contexts
        for context in contexts:
            print context.encode("utf-8")
            # print type(context.encode("utf-8"))
            if u"WEBVIEW" in context.encode("utf-8"):
                 drvapp.switch_to.context(context)
                 sleep(4)
                 print drvapp.current_context
                 print drvapp.page_source
            else:
                print "121212"
        sleep(6)
        # drvapp.context("WEBVIEW")
        print drvapp.current_context
        print drvapp.page_source

        print "end"


            # x = drvapp.switch_to_default_content()
            # x = drvapp.contexts()
            # print x
            #
            # print drvapp.current_context
            # drvapp.switch_to.context('WEBVIEW_com.tencent.mm:tools')
            # print drvapp.current_context
            # print drvapp.page_source
            # drvapp.find_element_by_xpath('//*[@id="btnRecommend"]/div[1]').click()
            # drvapp.switch_to_default_content()
            # time.sleep(2)
            # drvapp.quit()
            #
            # sleep(1212)
            #
            #
            # # 聊天
            # # drvapp.find_element_by_id("com.cetc.partybuilding:id/ll_switch").click()
            # # sleep(4)
            # # drvapp.find_element_by_id("com.cetc.partybuilding:id/chatting_content_et").send_keys(u"q")
            # # sleep(2)
            # # drvapp.find_element_by_id("com.cetc.partybuilding:id/chatting_send_btn").click()
            #
            #
            # # 点击 +
            # drvapp.find_element_by_id("com.cetc.partybuilding:id/chatting_attach_btn").click()
            # # 点击收藏夹
            # drvapp.find_element_by_id("com.cetc.partybuilding:id/app_panel_grid").find_element_by_xpath("//android.widget.LinearLayout[contains(@index,2)]").click()
            # sleep(2)
            # drvapp.find_element_by_id("com.cetc.partybuilding:id/listview").find_element_by_xpath("//android.widget.LinearLayout[contains(@index,2)]").click()
            # sleep(2)




            # list1 = os.popen("lsof -i tcp:4723 | awk '{print $2}' | grep -v PID").readlines()
            # os.system("kill " + list1[0])

        # # 我的学习群
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/my_learn_group").click()
        # sleep(2)
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/doctor_office_list_header_ll_group").click()
        # sleep(2)
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/groupList_lv_info").find_element_by_xpath("//android.widget.LinearLayout/android.widget.RelativeLayout[contains(@index,0)]").click()
        # sleep(2)
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/chatting_icq_iv_group_setting").click()
        # sleep(2)
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/groupsetting_notice_tb").click()
        # sleep(6)
        # # print self.find_toast(u"已开启")
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/back_btn").click()
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/chatting_icq_iv_back").click()
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/back_btn").click()
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/back_btn").click()


        # commands.getoutput('say 检查CETC新闻')

        # 点击CETC
        drvapp.find_element_by_id("com.cetc.partybuilding:id/ll_news_tabs").click()
        # print drvapp.contexts
        # 选择抗战胜利
        drvapp.find_element_by_id("android:id/tabs").find_element_by_xpath("//android.widget.FrameLayout[3]/android.widget.TextView[contains(@index,0)]").click()
        sleep(2)
        # 选择第一条新闻
        drvapp.find_element_by_id("com.cetc.partybuilding:id/listview").find_element_by_xpath("//android.widget.RelativeLayout[contains(@index,1)]").click()
        sleep(5)
        print drvapp.contexts
        print drvapp.contexts[0]
        print drvapp.contexts[-1]
        # print drvapp.current_context
        # drvapp.switch_to_default_content()
        print "0000000000000000000"
        drvapp.switch_to.context('WEBVIEW_com.cetc.partybuilding')
        sleep(6)
        print drvapp.current_context
        print "11111111111111111"
        # drvapp.switch_to.context(drvapp.contexts[0])
        # print drvapp.current_context
        # print "111111111111343434343434"
        drvapp.find_element_by_xpath(u'//button[@ng-click="$ctrl.backward()"]').click()
        drvapp.switch_to.default_content()
        print drvapp.contexts
        # print drvapp.page_source

        sleep(1212)

        # # 学习计划
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/learn_plan").click()
        # sleep(2)
        # x = drvapp.find_element_by_id("com.cetc.partybuilding:id/layout").find_element_by_xpath(
        #     "//android.widget.RadioGroup/android.widget.RadioButton[contains(@index,0)]").text
        # x = str(x).split("(")[1].replace(")", "")
        # # 显示 待完成计划数量
        # print u"待完成计划(" + x + ")"
        #
        # # 显示 第一条计划的 学习方式、子项目名、机构、时间、百分比
        # print drvapp.find_element_by_id("com.cetc.partybuilding:id/title_tv").text
        # print drvapp.find_element_by_id("com.cetc.partybuilding:id/company_tv").text
        # print drvapp.find_element_by_id("com.cetc.partybuilding:id/time_tv").text
        # print drvapp.find_element_by_id("com.cetc.partybuilding:id/progress_tv").text
        #
        # # 点击第一个学习计划的图片
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/image_iv").click()
        # # 点击收缩尖头
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/iv_switch").click()
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/chatting_content_et").send_keys(u"今天顺利吗？")
        # sleep(2)
        # drvapp.keyevent(66)  # drvapp.press_keycode(66)
        #
        # sleep(1212)

        commands.getoutput('say 登录成功')


        # 引导学
        commands.getoutput('say 打开引导学')
        drvapp.find_element_by_id("com.cetc.partybuilding:id/learn_one").click()
        sleep(2)

        # 点击更多
        drvapp.find_element_by_id("com.cetc.partybuilding:id/more_tv").click()


        # 点击 +
        commands.getoutput('say 我来新增一个问题')
        drvapp.find_element_by_id("com.cetc.partybuilding:id/nav_layout").find_element_by_xpath("//android.widget.ImageView[contains(@index,3)]").click()
        sleep(2)
        drvapp.find_element_by_id("com.cetc.partybuilding:id/et_title_ask_question").send_keys(u"问题12")
        drvapp.find_element_by_id("com.cetc.partybuilding:id/et_content_ask_question").send_keys(u"我要回答1234")

        # @向他人请教
        drvapp.find_element_by_id("com.cetc.partybuilding:id/ll_invite_ask_question").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").click()

        # 选择第一条@对象，返回到上一页
        drvapp.find_element_by_id("com.cetc.partybuilding:id/listview").find_element_by_xpath("//android.widget.LinearLayout[contains(@index,1)]").click()

        # 删除选择的@对象
        drvapp.find_element_by_id("com.cetc.partybuilding:id/iv_delete_invite_ask_question").click()


        # drvapp.find_element_by_id("com.cetc.partybuilding:id/ll_invite_ask_question").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").click()
        # # 切换输入法（# adb shell ime list - s， 显示可用的输入法，切换后点击输入框后模拟键盘回撤）
        # # 搜索框输入111
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/et_search_invite_people").send_keys(u"111")
        # commands.getoutput('adb shell ime set com.samsung.inputmethod/.SamsungIME')
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/et_search_invite_people").click()
        # drvapp.press_keycode(66)
        # sleep(2)
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/listview").find_element_by_xpath("//android.widget.LinearLayout[contains(@index,2)]").click()
        # print drvapp.find_element_by_id("com.cetc.partybuilding:id/tv_invite_name_ask_question").text

        # 点击添加图片 +
        commands.getoutput('say 添加了图片')
        drvapp.find_element_by_id("com.cetc.partybuilding:id/ll_show_pic_ask_question").find_element_by_xpath("//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView[contains(@index,0)]").click()
        # 点击 从手机相册选择
        drvapp.find_element_by_id("com.cetc.partybuilding:id/ll_album_dialog_photo").click()
        self.shellClick(200, 300)  # 选照片
        self.shellClick(240, 100)  # 点击照片
        sleep(2)

        # 删除图片 X
        commands.getoutput('say 不好看 删了算了')
        drvapp.find_element_by_id("com.cetc.partybuilding:id/ll_show_pic_ask_question").find_element_by_xpath("//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.ImageView[contains(@index,1)]").click()

        # # 提交
        commands.getoutput('say 准备提交')

        drvapp.find_element_by_id("com.cetc.partybuilding:id/nav_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").click()


        # # 显示 问题提交者
        xx = drvapp.find_element_by_id("com.cetc.partybuilding:id/quetion_tv_name").text
        print xx
        commands.getoutput('say ' + xx)

        print drvapp.find_element_by_id("com.cetc.partybuilding:id/quetion_tv_title").text
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/quetion_tv_content").text
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/quetion_tv_time").text
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/quetion_tv_praise_num").text
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/quetion_tv_answer").text
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/question_tv_status").text
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/back_btn").click()

        commands.getoutput('say 吧啦吧啦吧啦  输出了一大堆 测试成功')

        sleep(1212)

        # # 点击 搜索
        drvapp.find_element_by_id("com.cetc.partybuilding:id/nav_layout").find_element_by_xpath("//android.widget.ImageView[contains(@index,2)]").click()
        sleep(2)
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/search_et").click()
        drvapp.find_element_by_id("com.cetc.partybuilding:id/search_et").clear()
        drvapp.find_element_by_id("com.cetc.partybuilding:id/search_et").send_keys(u"q")
        sleep(2)
        drvapp.keyevent(66)   # drvapp.press_keycode(66)
        sleep(1)


        # adb shell ime list - s
        # excuteAdbShell("adb shell ime set com.sohu.inputmethod.sogou/.SogouIME");
        commands.getoutput('com.samsung.inputmethod/.SamsungIME')
        drvapp.find_element_by_id("com.cetc.partybuilding:id/search_et").click()
        # drvapp.press_keycode(AndroidKeyCode.Enter)
        drvapp.press_keycode(66)


        # 点击搜索后的结果
        drvapp.find_element_by_id("com.cetc.partybuilding:id/title_tv").click()

        # 返回到搜索框
        drvapp.find_element_by_id("com.cetc.partybuilding:id/back_btn").click()

        # 返回到你问我答列表页
        drvapp.find_element_by_id("com.cetc.partybuilding:id/back_btn").click()

        # 返回到问卷答题引导学列表页
        drvapp.find_element_by_id("com.cetc.partybuilding:id/back_btn").click()

        # 返回到首页
        drvapp.find_element_by_id("com.cetc.partybuilding:id/back_btn").click()





        # # 交流学
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/learn_two").click()
        #
        # # 结合学
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/learn_three").click()
        #
        # # 自省学
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/learn_four").click()
        #

        # 学习计划
        drvapp.find_element_by_id("com.cetc.partybuilding:id/learn_plan").click()
        sleep(2)
        x = drvapp.find_element_by_id("com.cetc.partybuilding:id/layout").find_element_by_xpath("//android.widget.RadioGroup/android.widget.RadioButton[contains(@index,0)]").text
        x = str(x).split("(")[1].replace(")","")
        # 显示 待完成计划数量
        print u"待完成计划(" + x + ")"

        # 显示 第一条计划的 学习方式、子项目名、机构、时间、百分比
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/title_tv").text
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/company_tv").text
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/time_tv").text
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/progress_tv").text

        # 点击第一个学习计划的图片
        drvapp.find_element_by_id("com.cetc.partybuilding:id/image_iv").click()
        # 点击收缩尖头
        drvapp.find_element_by_id("com.cetc.partybuilding:id/iv_switch").click()
        drvapp.find_element_by_id("com.cetc.partybuilding:id/chatting_content_et").send_keys(u"今天顺利吗？")
        sleep(2)
        drvapp.keyevent(66)  # drvapp.press_keycode(66)



        # 项目榜
        drvapp.find_element_by_id("com.cetc.partybuilding:id/nav_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,3)]").click()
        sleep(2)
        # 分类
        drvapp.find_element_by_id("com.cetc.partybuilding:id/nav_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").click()
        sleep(2)
        # 选择 资料学习
        drvapp.find_element_by_id("com.cetc.partybuilding:id/gridview_one").find_element_by_xpath("//android.widget.TextView[contains(@index,3)]").click()
        # 确定
        drvapp.find_element_by_id("com.cetc.partybuilding:id/nav_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").click()
        # 返回
        drvapp.find_element_by_id("com.cetc.partybuilding:id/back_btn").click()


        # 已结束计划
        drvapp.find_element_by_id("com.cetc.partybuilding:id/layout").find_element_by_xpath("//android.widget.RadioGroup/android.widget.RadioButton[contains(@index,1)]").click()
        sleep(2)
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/title_tv").text
        self.shellSwipe(300, 700, 300, 420)
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/title_tv").text
        self.shellSwipe(300, 700, 300, 420)
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/title_tv").text
        self.shellSwipe(300, 700, 300, 420)
        print drvapp.find_element_by_id("com.cetc.partybuilding:id/title_tv").text

        # 返回首页
        drvapp.find_element_by_id("com.cetc.partybuilding:id/back_btn").click()

        # 个人学习统计 或 驾驶仓
        drvapp.find_element_by_id("android:id/tabs").find_element_by_xpath("//android.widget.FrameLayout[contains(@index,1)]").find_element_by_id("com.cetc.partybuilding:id/framelayout").click()
        sleep(3)

        # 个人中心
        drvapp.find_element_by_id("android:id/tabs").find_element_by_xpath("//android.widget.FrameLayout[contains(@index,2)]").find_element_by_id("com.cetc.partybuilding:id/framelayout").click()
        sleep(3)

        # # 退出
        # self.shellSwipe(300, 700, 300, 450)
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/myInfo_tv_exit").click()
        # drvapp.find_element_by_id("com.cetc.partybuilding:id/enterCancel_dialog_tv_left").click()




    def exitMember(self):
        drvapp.find_element_by_id("com.cetc.partybuilding:id/back_btn").click()





    # 功能点
    def drv_func(self):
        self.TestcaseModule()
        sleep(2)
    def uninstallAPK(self, appPackage):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        if self.drvapp.is_app_installed(appPackage) == True:
            os.system('adb uninstall ' + appPackage + "> null")
            print "[OK, " + str(appPackage) + " 卸载成功]"
        else:
            print "[Warning, 无" + str(appPackage) + "包]"
        sleep(2)
    def installAPK(self, ApkName, appPackage, appActivity):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        print "[doing..., " + str(ApkName) + "]"
        os.system('adb install ' + ApkName + "> null")
        sleep(3)
        self.drvapp.start_activity(appPackage,appActivity)
        print "[OK, " + str(appPackage) + " 安装成功]"
        # if os.path.isfile(ApkName): os.remove(ApkName)



    # 我
    def drv_me(self):
        self.TestcaseModule()

    # 附近场景
    def drv_near(self):
        self.TestcaseModule()


    # 我的场景
    def drv_my(self):
        self.TestcaseModule()





if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(AppDangjian)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试

