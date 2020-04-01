#!/usr/bin/env python3
#coding: utf-8

import os
import sys
import unittest
from time import sleep
from appium import webdriver
import time
import re
import subprocess
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By






PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)






try:
    # 获取devices列表
    devicesNum = subprocess.Popen("adb devices",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)


except:
    print("未获取到设备列表-请使用 adb devices 查看")
else:
    # 类迭代对象 标准输出读取数据
    devicesReadNum = devicesNum.stdout.read()
    # 类迭代对象转换成str类型，使用设备名称进行匹配-会返回1个【元组】格式数据
    devicesName = re.findall(r'\\n(\w{3,4}(\.|-)\w{3}(\.|-)\w{2,10}\.?\w{3}?)', str(devicesReadNum), re.S)

    # 根据设备列表---进行元组索引取值--来获取测试设备版本号并【运行该设备】：[0][0]是列表中第1个设备
    # platformVersioninfo = list(os.popen("adb -s {} shell getprop ro.build.version.release".format(devicesName[0][0])).readlines())
    # print("设备版本号:{}".format(platformVersioninfo))
    # 获取到的['5.1\n']是迭代对象，需要对迭代对象使用正则取出【版本号】
    bianyiVersion = re.compile(r'^\w*\b')  # 编译正则
    # deviceVersion = bianyiVersion.findall(platformVersioninfo[0])[0]  # 对【版本号】进行匹配并赋值
    #
    #




try:
    # 获取测试包路径
    appLocation = '/Users/guolong/Desktop/Test_Package/Android/appium_android/app-Offical-debug.apk'
    # 生成一个类迭代对象 #每个包的packname与Activityname格式可能是不一样，所以需要使用 appt 命令先查看再正则
    devicesinfo1 = subprocess.Popen("aapt dump badging {}".format(appLocation),
                                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    devicesinfo2 = devicesinfo1.stdout.read()  # 对类迭代对象 标准输出读取数据
    # 使用正则来匹配获取package名称 --类字节对象必须转换成str格式-
    PackageName = re.findall(r'^b\"package: name=\'(com\.\w+\.\w+\.\w+\.\w+\.\w+)', str(devicesinfo2), re.S)[0]
except:
    print("无此安装包，请检查:/Users/guolong/Desktop/Test_Package/Android/appium_android/ 目录下是否有该安装包")
else:
    # 使用正则来匹配获取activity名称 --类字节对象必须转换成str格式-
    LaunchActivityName = \
    re.findall(r'launchable-activity: name=\'(com\.\w+\.\w+\.\w+\.\w+\.\w+\.\w+\.\w+)', str(devicesinfo2), re.S)[0]















class blm(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = deviceVersion
        desired_caps['deviceName'] = "Appium"
        desired_caps['app'] = PATH(
            appLocation
        ) #['app'] 加入将自动检测是否有该app，没有就安装，有也会卸载后重新安装
        desired_caps['appPackage'] = PackageName
        desired_caps['appActivity'] = LaunchActivityName
        desired_caps['unicodeKeyboard'] = 'True' #使用unicode编码方式发送字符串
        desired_caps['resetKeyboard'] = 'True' #重置键盘
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        # reload(sys)
        # sys.setdefaultencoding('utf8')
        self.driver.implicitly_wait(10)


    @classmethod
    def tearDownClass(self):
        self.driver.quit() #执行后appium再无日志，但app并未关闭，是置于运行后台了可再次唤醒



















    def test_Main(self):






        # 点击权限提示窗中'允许'按钮 设置等待元素出现后再进行点击，如果没有出现就一直重试10s
        def permission_allow(self):

            WebDriverWait(
                driver=self.driver, timeout=10, poll_frequency=0.5, ignored_exceptions=None).until(
                method=EC.visibility_of_element_located(
                    (By.ID, ("com.android.packageinstaller:id/permission_allow_button"))),
                message="未找到'权限'是否允许访问相册、文件-按钮").click()

            """"判断元素是否出现"""
            located = (By.ID,("com.android.packageinstaller:id/permission_allow_button"))
            PanDuanElement = EC.visibility_of_element_located(located)
            WebDriverWait(
                driver=self.driver, timeout=10, poll_frequency=0.5, ignored_exceptions=None).until(
                method=PanDuanElement,message="未找到'权限'是否允许定位-按钮").click()

        # permission_allow(self)





        self.driver.implicitly_wait(5)
        # '载入界面'自右向左滑动3次
        def GetPageSize(self):
            x = self.driver.get_window_size()['width']
            y = self.driver.get_window_size()['height']
            return (x, y)

        # '定义x，y轴的'界面比例''
        def MoveGuide_ScreenLeft():
            g = GetPageSize(self)
            sx = g[0] * 0.80
            sy = g[1] * 0.55
            ex = g[0] * 0.10
            ey = g[1] * 0.55

            sleep(3)
            # 获取'引导页'元素信息
            # Guidenum = self.driver.find_elements_by_xpath("//android.widget.LinearLayout/android.view.View")
            # print(self.driver.find_elements_by_id("//android.widget.LinearLayout/android.view.View"))
            # # 输出结果：[<appium.webdriver.webelement.WebElement (session="6c58fdc6-bcfa-4276-8539-08434b544278", element="3")>]
            # # 元素信息中'获取引导页数量'
            # for a in Guidenum:
            #     ElementID = int(a.id)

                # print(int(a.id))
            # 循环滑动'引导页'list(range(GuideNum1))--根据获取的元素数量来做自动循环次数
            for b in list(range(1,5)):
                self.driver.swipe(sx, sy, ex, ey, 1000)
                sleep(2)

        MoveGuide_ScreenLeft()






        def permission_Open(self):

            self.driver.implicitly_wait(10)
            WebDriverWait(
                driver=self.driver, timeout=10, poll_frequency=0.5, ignored_exceptions=None).until(
                method=EC.visibility_of_element_located(
                    (By.ID, ("com.kuping.android.boluome.life.debug:id/iv_btn_open_now"))),
                message="未找到'载入界面'中'立即开启'按钮").click()

        permission_Open(self)

        # 是否'拨打电话'与'管理通话'弹窗中'允许'按钮
        # self.driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button").click()
        sleep(1)





        # 进入界面下拉刷新 1 次
        def Moverenovate_ScreenLeft():
            br = GetPageSize(self)
            sx = br[0] * 0.55
            sy = br[1] * 0.15
            ex = br[0] * 0.55
            ey = br[1] * 0.35
            for c in list(range(1,2)):
                self.driver.swipe(sx,sy,ex,ey,2000)
        Moverenovate_ScreenLeft()
        sleep(5)

        # # 'banner'自右向左滑动5次
        # def MoveBanner_ScreenLeft():
        #     ba = GetPageSize(self)
        #     sx = ba[0] * 0.80
        #     sy = ba[1] * 0.15
        #     ex = ba[0] * 0.10
        #     ey = ba[1] * 0.15
        #     bannernum = self.driver.find_elements_by_id("com.kuping.android.boluome.life:id/loPageTurningPoint")
        #     for d in bannernum:
        #         BannerNum = int(d.id)
        #     for e in list(range(BannerNum)):
        #         self.driver.swipe(sx,sy,ex,ey,800)
        #         sleep(0.5)
        # MoveBanner_ScreenLeft()



        # 点击'品牌'
        # def permission_Tab_brands2():
        #
        #     WebDriverWait(
        #         driver=self.driver, timeout=10, poll_frequency=0.5, ignored_exceptions=None
        #     ).until(
        #         method=EC.visibility_of_element_located((By.XPATH,("//android.widget.TabWidget/android.widget.RelativeLayout[2]/android.widget.TextView[contains(@text,'品牌')]"))),
        #         message="未找到'Buttom_Tab'中'品牌'按钮").click()

        # permission_Tab_brands2()

        self.driver.find_element_by_id("android:id/tabs").find_element_by_xpath(
            "//android.widget.RelativeLayout[contains(@index,1)]").click()



        # 点击'订单'
        def permission_Tab_brands3():

            WebDriverWait(
                driver=self.driver, timeout=10, poll_frequency=0.5, ignored_exceptions=None
            ).until(
                method=EC.visibility_of_element_located((By.XPATH,("//android.widget.TabWidget/android.widget.RelativeLayout[3]"))),
                message="未找到'Buttom_Tab'中'订单'按钮").click()

        permission_Tab_brands3()




        # 点击'我的'
        def permission_Tab_brands4():

            WebDriverWait(
                driver=self.driver, timeout=10, poll_frequency=0.5, ignored_exceptions=None
            ).until(
                method=EC.visibility_of_element_located((By.XPATH,("//android.widget.TabWidget/android.widget.RelativeLayout[4]"))),
                message="未找到'Buttom_Tab'中'我的'按钮").click()

        permission_Tab_brands4()




        # 点击头像
        def permission_account():

            WebDriverWait(
                driver=self.driver, timeout=10, poll_frequency=0.5, ignored_exceptions=None
            ).until(
                method=EC.visibility_of_element_located((By.ID,("com.kuping.android.boluome.life.debug:id/iv_mine_avatar"))),
                message="未找到'我的'中'头像'按钮").click()

        permission_account()

        # 进入 '登录'界面，点击'是否允许自动填充验证'中'允许'按钮
        # self.driver.find_element_by_id("android:id/button1").click()
        # sleep(1)
        # 点击'是否允许菠萝觅读取、查看短信信息'
        # self.driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button").click()




        # 输入手机号
        def permission_Phone():

            WebDriverWait(
                driver=self.driver, timeout=10, poll_frequency=0.5, ignored_exceptions=None
            ).until(
                method=EC.visibility_of_element_located((By.ID,("com.kuping.android.boluome.life.debug:id/et_mobile"))),
                message="未找到'登录账号'中'账号文本框'按钮").send_keys('13512119091')

        permission_Phone()



        # 点击'获取验证码'
        def permission_auth_code():

            WebDriverWait(
                driver=self.driver, timeout=10, poll_frequency=0.5, ignored_exceptions=None
            ).until(
                method=EC.visibility_of_element_located((By.ID,("com.kuping.android.boluome.life.debug:id/btn_get_code"))),
                message="未找到'登录账号'中'获取验证码'按钮").click()

        permission_auth_code()



        # 点击'登录'
        def permission_login():

            WebDriverWait(
                driver=self.driver, timeout=10, poll_frequency=0.5, ignored_exceptions=None
            ).until(
                method=EC.visibility_of_element_located((By.ID,("com.kuping.android.boluome.life.debug:id/btn_login"))),
                message="未找到'登录账号'中'获取验证码'按钮").click()

        permission_login()





















        print()
        print("执行完毕")
if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(blm)
    unittest.TextTestRunner(verbosity=2).run(suite1)