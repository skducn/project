# coding: utf-8
#***************************************************************
# Author     : John
# Created on : 2016-7-29
# Description: 基础类BasePage，封装所有页面都公用的方法，例如driver, url ,FindElement等
#***************************************************************

'''
定义open函数，重定义find_element，switch_frame，send_keys等函数。
在初始化方法中定义驱动driver，基本url，title
WebDriverWait提供了显式等待方式。
'''

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import sys, json
import smtplib,email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
import mimetypes

reload(sys)
typ = sys.setdefaultencoding("utf-8")
from time import sleep
varStatusOK = '[Ok]，'
varStatusFault = '[Faultttttttttt]，'
varStatusErr = '[Errorrrrrrrrrr]，'
varStatusWarning = '[Warning]，'


class BasePage(object):

    def __init__(self, selenium_driver, base_url, pagetitle):
        # 初始化 driver、url、pagetitle等
        # 实例化BasePage类时，最先执行的是__init__方法，该方法的入参，就是BasePage类的入参。
        # __init__方法返回None
        # self只实例本身，相较于类Page而言。
        self.driver = selenium_driver
        self.base_url = base_url
        self.pagetitle = pagetitle

    def _open(self, url, pagetitle):
        # 以单下划线_开头的方法，在使用import *时，该方法不会被导入，保证该方法为类私有的。
        # 打开页面，并校验页面链接是否加载正确
        self.driver.get(url)
        self.driver.maximize_window()
        # 使用assert进行校验，打开的窗口title是否与配置的title一致。调用on_page()方法
        # try:
        #     assert self.on_page(pagetitle), u"%s, expected=%s, actual=%s" % (url, self.driver.title, pagetitle)
        #
        # finally:  pass

    def open(self, t):
        self._open(self.base_url, self.pagetitle)
        self.now_handle = self.driver.current_window_handle  # 获取当前窗口句柄
        sleep(t)
        return self.now_handle

    def on_page(self, pagetitle):
        # 使用title获取当前窗口title，检查输入的title是否在当前title中，返回比较结果（True 或 False）
        return pagetitle in self.driver.title

    def _check_title(self, url, pagetitle):
        try:
            assert self.on_page(pagetitle), u"%s, expected=%s, actual=%s" % (url, self.driver.title, pagetitle)
        finally:
            pass

    def checkk_title(self):
        self._check_title(self.base_url, self.pagetitle)

    def find_element(self, *loc):
        # 重写元素定位方法
        try:
            # 确保元素是可见的。
            # 注意：入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            # WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            # print u"%s 页面中未能找到元素 %s "%(self, loc)
            print u"页面中未找到元素 %s " %(loc)

    def find_elements(self, *loc):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_elements(*loc)
        except:
            print u"页面中未找到元素 %s " %(loc)

    def script(self, src):
        # 定义script方法，用于执行js脚本，范围执行结果
        self.driver.execute_script(src)

    def send_keys(self, loc, vaule, clear_first=True, click_first=True):
        # 重写定义send_keys方法
        try:
            loc = getattr(self,"_%s"% loc)  #getattr相当于实现self.loc
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(vaule)
        except AttributeError:
            # print u"%s 页面中未能找到 %s 元素"%(self, loc)
            print u"页面中未找到元素 %s " %(loc)

    def close_driver(self):
        self.driver.close()
        # self.driver.quit()

    def move_screenLeft(self, location, t):
        # 屏幕向左移动
        # Home_PO.move_screenLeft('1000', 2)  # 屏幕向左移动1000个像素
        js = "var q=document.documentElement.scrollLeft=" + location
        self.driver.execute_script(js)
        sleep(t)

    def move_screenTop(self, location, t):
        # 屏幕向上移动
        js = "var q=document.documentElement.scrollTop=" + location
        self.driver.execute_script(js)
        sleep(t)

    def inIframeDiv(self, xpath, t):
        # 进入iframe框架/div
        # e.g. Home_PO.inIframeDiv("[@id='task_view_target']", 2)
        # e.g. Home_PO.inIframeDiv("[@class='cetc-popup-content']/div", 2)
        # print self.driver.find_element_by_xpath("//div[@class='cetc-popup-content']/div/iframe").get_attribute("src")
        iframe = self.driver.find_element_by_xpath("//div" + xpath + "/iframe")
        self.driver.switch_to_frame(iframe)
        sleep(t)

    def outIframe(self, t):
        # 退出iframe框架
        self.driver.switch_to_default_content()
        sleep(t)

    def isElementXpath(self, loc):
        flag = False
        try:
            self.driver.find_element_by_xpath(loc)
            flag = True
        except:
            flag = False
        return flag

    def isElementId(self, locate):
        flag = False
        try:
            self.driver.find_element_by_id(locate)
            flag = True
        except :
            flag = False
        return flag

    def select_byName(self, varByname, varContent):
        # 下拉框，定位ByName，选择某一内容， text = value
        try :
            Select(self.driver.find_element_by_name(varByname)).select_by_value(varContent)
        except:
            print u"页面中未找到'%s'选项" %(varContent)

    def select_byName1(self, byname1, content1):
         # 下拉框，定位ByName，选择某一内容， text != value
         s1 = self.driver.find_element_by_name(byname1)
         l_content1 = []
         l_value1 = []
         varContents = self.driver.find_elements_by_xpath("//select[@name='" + byname1 + "']/option")
         # varContents = self.find_elements(*(By.XPATH, "//select[@name='" + byname1 + "']/option"))
         for a in varContents:
            l_content1.append(a.text)
            l_value1.append(a.get_attribute('value'))
         # print json.dumps(l_content1, encoding="UTF-8", ensure_ascii=False)
         d_total1 = dict(zip(l_content1, l_value1))
         for i in range(len(d_total1)):
             if sorted(d_total1.items())[i][0] == content1:
                 value = sorted(d_total1.items())[i][1]
         # print json.dumps(l_value1, encoding="UTF-8", ensure_ascii=False)
         d_total1 = json.dumps(d_total1, encoding="UTF-8", ensure_ascii=False)  # 字典 转 unicode
         # print d_total1
         Select(s1).select_by_value(value)


    def assertTrue(self, expected, msg, t):
        if expected == True :
            print varStatusOK + msg
        else:
            print varStatusFault + msg
        sleep(t)

    def assertEqual(self, expected, actual, msg, t):
        if expected == actual:
            print varStatusOK + msg
        else:
            print varStatusFault + msg
        sleep(t)

    def assertContain(self, one, allcontain, msg, t):
        if one in allcontain:
            print varStatusOK + msg
        else:
            print varStatusFault + msg
        sleep(2)



    # def assertSplit(self, varExcel):
    #     # 拆分两个值，如 id/cance=取消
    #     x = varExcel.split("=")
    #     return (x[0], x[1])


    def getAttachment(self, attachmentFilePath):
        contentType, encoding = mimetypes.guess_type(attachmentFilePath)
        if contentType is None or encoding is not None:
            contentType = 'application/octet-stream'
        mainType, subType = contentType.split('/', 1)
        file = open(attachmentFilePath, 'rb')
        if mainType == 'text':
            attachment = MIMEText(file.read())
        elif mainType == 'message':
            attachment = email.message_from_file(file)
        elif mainType == 'image':
            attachment = MIMEImage(file.read(), subType=subType)
        elif mainType == 'audio':
            attachment = MIMEAudio(file.read(), subType=subType)
        else:
            attachment = MIMEBase(mainType, subType)
        attachment.set_payload(file.read())
        encode_base64(attachment)
        file.close()
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachmentFilePath))
        return attachment

    def sendemail(self, subject, text, *attachmentFilePaths):
        gmailUser = 'jinhao@mo-win.com.cn'
        gmailPassword = 'Dlhy123456'
        recipient = 'jinhao@mo-win.com.cn'
        # recipient = "'jinhao@mo-win.com.cn', 'guoweiliang@mo-win.com.cn'"
        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(text, 'plain', 'utf-8'))
        # 附件是可选项
        for attachmentFilePath in attachmentFilePaths:
            if attachmentFilePath != '':
                 msg.attach(self.getAttachment(attachmentFilePath))
        mailServer = smtplib.SMTP('smtp.exmail.qq.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, msg.as_string())
        mailServer.close()
        print('Sent email to %s' % recipient)


    # 项目 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 项目 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 项目 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



# # 》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》
#
#     def current_windows(self,now_handle):
#         print now_handle
#         self.driver.switch_to_window(now_handle)
#         # now_handle = self.driver.current_window_handle #获取当前窗口句柄
#         # print now_handle   #输出当前获取的窗口句柄
#         # driver.find_element_by_id("kw1").send_keys("selenium")
#         # driver.find_element_by_id("su1").click()
#         # driver.find_element_by_xpath("//*[@id='1']/h3/a[1]").click()
#         # time.sleep(2)
#         # all_handles = self.now_handle  #获取所有窗口句柄
#         # for handle in all_handles:
#         # #
#         # #     if handle != self.now_handle:
#         # #         print handle    #输出待选择的窗口句柄
#         #     self.driver.switch_to_window(handle)
#         # self._current_windows(self.now_handle)
#
#
#     def _current_windows(self, now_handle):
#         self.driver.switch_to_window(now_handle)
#         # all_handles = now_handle  #获取所有窗口句柄
#         # for handle in all_handles:
#         #     self.driver.switch_to_window(handle)

