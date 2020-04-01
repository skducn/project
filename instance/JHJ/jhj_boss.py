# coding: utf-8
#****************************************************************
# jhj_boss.py
# Author     : John
# Version    : 1.0.0
# Date       : 2016-4-7
# Description: Boss后台
#****************************************************************
#http://tungwaiyip.info/software/HTMLTestRunner.html
import os,sys,unittest,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,win32api,win32con,platform,string,datetime,win32gui,re,SendKeys
import HTMLTestRunner,smtplib
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

# 环境变量
File_ExcelName = "/Users/linghuchong/Downloads/51/ForWin/Python/02_code/excel/jhj_boss.xls"
Html_Testreport = "/Users/linghuchong/Downloads/51/ForWin/Python/02_code/report/b_testreport.html" # TestReport文件
Err_Screenshot = "/Users/linghuchong/Downloads/51/ForWin/Python/02_code/screenshot/"  # 错误截屏


# 页面格式化 http://www.tuicool.com/articles/IRvEBr
page =PyH('JHJ_TestReport')
page.addCSS('myStylesheet1.css','myStylesheet2.css')
page << h2(u'极好家后台自动化测试报告', cl='center')
page << h4(u'Start Time:',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
page << h4(u'用例执行情况：')


#os.path.abspath() 方法用于获取当前路径下的文件
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

class WindowFinder:
    """Class to find and make focus on a particular Native OS dialog/Window """
    def __init__ (self):
        self._handle = None
    def find_window(self, class_name, window_name = None):
        """Pass a window class name & window name directly if known to get the window """
        self._handle = win32gui.FindWindow(class_name, window_name)
    def _window_enum_callback(self, hwnd, wildcard):
        '''Call back func which checks each open window and matches the name of window using reg ex'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd
    def find_window_wildcard(self, wildcard):
        """ This function takes a string as input and calls EnumWindows to enumerate through all open windows """
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)
    def set_foreground(self):
        """Get the focus on the desired open window"""
        win32gui.SetForegroundWindow(self._handle)

def send_keys_to_dialog(title, key_valus):
        win_dialog = WindowFinder()
        win_dialog.find_window_wildcard(title)
        #win_dialog.set_foreground()
        sleep(2)
        SendKeys.SendKeys(key_valus)
        SendKeys.SendKeys("{ENTER}")

class Jhj_boss(unittest.TestCase):

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
        browser = webdriver.Firefox()
        browser.get("http://192.168.0.100:8181/login")
        sleep(3)
        browser.find_element_by_name("account").clear() #清空输入框默认内容
        browser.find_element_by_name("account").send_keys("admin")
        browser.find_element_by_name("password").send_keys("123456")
        browser.find_element_by_class_name("login_btn").click()
        self.browser=browser
        sleep(3)
        nowhandle=browser.current_window_handle
        self.nowhandle=nowhandle

    @classmethod
    def tearDownClass(self):
        self.browser.quit()

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
        msg['Subject'] = u'极好家后台自动化测试报告'
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
                       page << p("<font color=blue>[Pass]</font> ",self.sh2.cell_value(l,3))  #输出测试用例
                   except:
                       print "Err,第"+str(l+1)+"行,"+self.sh2.cell_value(l,3)
                       newWs=self.newbk.get_sheet(1)
                       newWs.write(l,0,"error",self.styleE)
                       self.newbk.save(self.fname)
                       page << p("<font color=red>[Error]</font> ",self.sh2.cell_value(l,3))  #输出测试用例
                   page.printOut(Html_Testreport)
                   #open HTML
                   if self.sh1.cell_value(1,6) == "Y":
                      webbrowser.open(Html_Testreport)

    ##############################################################################################
    #商品
    def Goods(self):
         self.TestcaseModule()

    def b_Goods(self,GoodsName):
        # B1-A, 检查商品、删除商品
        # 商品管理列表页，检查（"自动化商品1"），存在则删除，否则添加此商品
        if self.browser.find_elements_by_xpath("//td[@class='goods_list_name']")[0].text==GoodsName:
           # 删除
           self.browser.find_elements_by_xpath("//input[@class='checkbox']")[0].click()
           self.browser.find_element_by_xpath("//button[@class='delete_goods']").click()
           self.browser.find_element_by_xpath("//button[@id='allDelete']").click()
           self.browser.refresh()
           sleep(3)
           if self.browser.find_elements_by_xpath("//td[@class='goods_list_name']")[0].text==GoodsName:
               print "Err,"+GoodsName+",无删除!"

    def b_AddGoods(self,GoodsName):
           #B1-A, 添加新品
           # 商品管理 - 添加商品
           self.browser.get("http://192.168.0.100:8181/prd/item/edit")
           allhandles=self.browser.window_handles
           for handle in allhandles:
               if handle != self.nowhandle:
                   self.browser.switch_to_window(handle)
           sleep(3)
           self.browser.maximize_window()
           # 商品标题
           self.browser.find_element_by_id("itemTitle").send_keys(GoodsName)
           # 商品副标题
           self.browser.find_element_by_id("itemSubTitle").send_keys(u"自动化商品副标题1")
           # 参考价格
           self.browser.find_element_by_id("refPrice").send_keys(u"12.44")
           self.browser.find_element_by_id("goods_c_a").click()
           xx=self.browser.find_elements_by_class_name("select_cat")
           for x1 in xx:
               if x1.text==u"好货优先":
                   x1.click()
           # 保存
           self.browser.find_element_by_id("categorSelect").click()
           sleep(2)
           # 商品大图
           #browser.find_element_by_id("pickfiles1").click()
           #browser.find_element_by_xpath("//input[@type='file']")
           self.browser.find_element_by_id("pickfiles1").click()
           sleep(2)
           # http://sleepycat.org/blog/35/
           send_keys_to_dialog(u".*文件上传.*","/Users/linghuchong/Downloads/51/ForWin/Python/02_code/pic/test1.png")
           sleep(2)
           self.browser.find_element_by_id("pickfiles").click()
           send_keys_to_dialog(u".*文件上传.*","/Users/linghuchong/Downloads/51/ForWin/Python/02_code/pic/test2.png")
           # 商品描述
           # browser.find_element_by_class_name("view").send_keys(u"托尔斯泰")
           sleep(4)
           # 可选类型1 - 尺寸
           self.browser.find_element_by_xpath("//select[@id='attributeSelect1']").find_element_by_xpath("//option[@value='1']").click()
           self.browser.find_element_by_xpath("//span[@class='add_more addAttribute1']").click()
           self.browser.find_element_by_xpath("//input[@class='add_more_goods addSku1']").send_keys("12")
           # 可选类型2 - 温度
           self.browser.find_element_by_id("attributeSelect2").find_elements_by_tag_name("option")[4].click()
           self.browser.find_element_by_xpath("//span[@class='add_more addAttribute2']").click()
           self.browser.find_element_by_xpath("//input[@class='add_more_goods addSku2']").send_keys("1200")
           # 添加SKU
           self.browser.find_element_by_id("addSKuTest").click()
           sleep(2)
              # 价格
           self.browser.find_element_by_xpath("//input[@class='numberAndpoint input-1026 sku_skuPrice']").send_keys("300")
              # 条形码
           self.browser.find_element_by_xpath("//input[@class=' input-1026 sku_barCode']").send_keys("123456")
           # 规格名称
           self.browser.find_element_by_class_name("select-1026").find_elements_by_tag_name("option")[3].click() #
           # 参数
           self.browser.find_element_by_xpath("//textarea[@class='input-1026']").send_keys("555")
           # 确定
           self.browser.find_element_by_xpath("//button[@class='button_btn button_btn_save saveItem']").click()
           sleep(4)
           # 跳转到商品管理，检查是否存在此商品
           if self.browser.find_elements_by_xpath("//td[@class='goods_list_name']")[0].text<>GoodsName:
                print "Err,"+GoodsName+"，添加失败!"


if __name__ == '__main__':
    # unittest.main() # 用这个是最简单的，下面的用法可以同时测试多个类
    # unittest.TextTestRunner(verbosity=2).run(suite1) # 这个等价于上述但可设置verbosity=2，省去了运行时加-v
    suite1 = unittest.TestLoader().loadTestsFromTestCase(Jhj_boss) # 构造测试集
    # suite1=unittest.TestSuite()
    # suite1.addTest(Jhj1_5("SearchZero"))
    # suite1.addTest(Jhj1_5("Search1"))
    # 输出HTML报告
    # now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    # filename = 'C:\\Python27\\TMPappium\\report\\'+now+'result.htm'
    # fp = file(filename,'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(
    #     stream = fp,title=u'极好家后台自动化测试报告',description=u'用例执行情况：'
    # )
    # runner.run(suite1)
    #unittest.TextTestRunner(verbosity=2).run(suite1)
    unittest.TextTestRunner(verbosity=2).run(suite1) # 执行测试
    # suite2 = unittest.TestLoader().loadTestsFromTestCase(JHJ1_6) # 可以增加多个类，如Jhj1_5
    # allTests = unittest.TestSuite([suite1,suite2]) #执行多个类的Testcase
    # unittest.TextTestRunner(verbosity=2).run(allTests)
    # eg.http://canlynet.iteye.com/blog/1671750


# #browser.implicitly_wait(3)
# #cookie = browser.get_cookies()
# #print cookie
# xx=browser.find_element_by_name("account").send_keys("adminp")
# #ActionChains(browser).context_click(xx).perform()
# element = WebDriverWait(browser,3).until(lambda browser: browser.find_element_by_name("account"))
# element.clear()
# element.send_keys("selenium")
#
# time.sleep(3)
# browser.find_element_by_name("account").send_keys(Keys.BACK_SPACE) #删除adminp 中 p字母
# browser.find_element_by_name("account").send_keys(Keys.SPACE) #输入空格
# browser.find_element_by_name("account").send_keys(u"测试") #输入测试
# browser.find_element_by_name("account").send_keys(Keys.CONTROL,'a') # ctrl+a 全选
# browser.find_element_by_name("account").send_keys(Keys.CONTROL,'x') # ctrl+x 剪切
# browser.find_element_by_name("account").send_keys(Keys.ENTER) # 通过回车键盘来代替点击操作
# time.sleep(3)
#
# print browser.find_element_by_name("account").size  # 获取输入框的尺寸{'width': 376, 'height': 52}
# print browser.find_element_by_name("account").text
# yy=browser.find_element_by_name("password").send_keys("123456")
# ##ActionChains(browser).move_to_element(yy).perform()
# browser.find_element_by_class_name("login_btn").click()
# # 浏览器最大化
# browser.maximize_window()
#
# # 设置浏览器款480 * 高800 ,一般用于移动屏幕，
# browser.set_window_size(480,800)
# #browser.quit()

# # 探享广告位 推荐项列表页
# browser.get("http://192.168.0.100:8181/cms/recommend/detail/list.htm?positionCode=T1")
# allhandles=browser.window_handles
# for handle in allhandles:
#     if handle != nowhandle:
#         browser.switch_to_window(handle)
# sleep(3)
# xx=browser.find_elements_by_class_name("change_href")
# pp=0
# oo=0
# for x1 in xx:
#     if x1.text==u"下线":
#         pp=1
# for x2 in xx:
#     if pp==0 and oo==2:
#         x2.click()
#         break
#     else:
#         oo=oo+1