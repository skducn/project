# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Created on : 2018-7-2
# Description: Web 对象层
# ***************************************************************
# selenium
# 查看可安装的selenium版本， pip install selenium==
# 注：部分新版本 selenium 4.10 会引起浏览器自动关闭现象，实测建议安装4.4.3, pip install selenium==4.4.3

# pip install opencv_python    // cv2
# ***************************************************************
# chrome
# 1，查看Chrome浏览器版本，chrome://version
# print(driver.capabilities['browserVersion'])  # 浏览器版本，如：114.0.5735.198
# print(driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])  # chrome驱动版本，如：114.0.5735.90
# 以上两版本号前3位一样就可以，如 114.0.5735

# 2，下载及配置 chromedriver 驱动
# 下载1：http://chromedriver.storage.googleapis.com/index.html
# 下载2：https://npm.taobao.org/mirrors/chromedriver
# 系统默认调用路径：C:\Python38\Scripts\chromedrive.exe
# 自定义调用路径：
# from selenium.webdriver.chrome.service import Service
# driver = webdriver.Chrome(service=Service("/Users/linghuchong/Downloads/51/Python/project/instance/web/chromedriver"), options=options)

# 3，chrome的options参数
# https://blog.csdn.net/xc_zhou/article/details/82415870
# https://blog.csdn.net/amberom/article/details/107980370

# Q1：MAC 移动chromedriver时报错，如 sudo mv chromedriver /usr/bin 提示： Operation not permitted
# A1: 重启按住command + R,进入恢复模式，实用工具 - 终端，输入 csrutil disable , 重启电脑。
# ***************************************************************

# firefox
# geckodriver 0.14.0 for selenium3.0
# 下载地址：https://github.com/mozilla/geckodriver/releases
# ff 66.0.4 (64 位) , selenium =3.141.0，gecko = 0.24.0
# geckodriver下载：https://github.com/mozilla/geckodriver/releases

# Q1：WebDriverException:Message:'geckodriver'executable needs to be in Path
# A1：geckodriver是原生态的第三方浏览器，对于selenium3.x版本使用geckodriver来驱动firefox，需下载geckodriver.exe,下载地址：https://github.com/mozilla/geckodriver/releases
# 将 geckodriver 放在 C:\Python38\Scripts
# ***************************************************************


"""
1.1 打开网站 open()
1.2 打开标签页 openLabel("http://www.jd.com")
1.3 切换标签页 switchLabel(1)
1.4 关闭当前窗口 close()

2.1 获取当前浏览器宽高 getBrowserSize()
2.2 设置浏览器分辨率 setBrowserSize()
2.3 设置浏览器全屏 setBrowserMax()
2.4 缩放页面比率 zoom(20)
2.5 截取浏览器内屏幕 getBrowserScreen()
2.6 页面滚动条到底部 scrollBottom()

3.1 弹出框 popupAlert()
3.2 确认弹出框 confirmAlert("accept", 2)

4.1 关闭浏览器应用 quit()

5.1 app屏幕左移 scrollLeftByApp('1000',9)
5.2 app屏幕右移 scrollRightByApp('1000', 5)
5.3 app屏幕上移 scrollUpByApp('1000', 5)
5.4 app屏幕下移 scrollDownByApp('1000', 5)


元素拖动到可见的元素 scrollIntoView(varXpath)
内嵌窗口中滚动条操作 scrollTopById(varId)
动态加载页面滚动到底部（加载所有数据） dynamicLoadToEnd()
获取验证码 getCode()
"""

from DomPO import *

class WebPO(DomPO):


    def opn(self, varUrl):

        '''
        1.1 打开网页
        :param varURL:
        :return:
        '''
        self.driver.get(varUrl)

    def opnLabel(self, varURL):

        '''
        1.2 打开标签页
        :param varURL:
        :return:
        '''

        self.driver.execute_script('window.open("' + varURL + '");')

    def swhLabel(self, varSwitch, t=1):

        '''
        1.3 切换标签页
        :param varSwitch: 1
        :param t:
        :return:
         # self.Web_PO.switchLabel(0) # 0 = 激活第一个标签页 ， 1 = 激活第二个标签页 , 以此类推。
        '''

        all_handles = self.driver.window_handles
        sleep(t)
        self.driver.switch_to.window(all_handles[varSwitch])

    def cls(self):

        '''
        1.4 关闭当前窗口
        :return:
        '''

        self.driver.close()


    def getBrowserSize(self):

        '''
        2.1 获取当前浏览器宽高
        :return:
        '''

        d_size = self.driver.get_window_size()  # {'width': 1936, 'height': 1056}
        return d_size
        # return (d_size["width"] - 16, d_size["height"] + 24)

    def setBrowserSize(self, width, height):

        '''
        2.2 设置浏览器分辨率
        :param width: 1366
        :param height: 768
        :return:
        # Web_PO.setBrowser(1366, 768) # 按分辨率1366*768打开浏览器
        '''

        self.driver.set_window_size(width, height)

    def setBrowserMax(self):

        '''
        2.3 设置浏览器全屏
        :return:
        '''

        self.driver.maximize_window()

    def zoom(self, percent):

        '''
        2.4 缩放页面内容比率
        :param percent:  50
        :return:
        30表示内容缩小到 50%
        '''

        self.driver.execute_script("document.body.style.zoom='" + str(percent) + "%'")

    def getBrowserScreen(self, varImageFile="browser.png"):

        '''
        2.5 截取浏览器内屏幕
        :param varImageFile:  "d:\\screenshot.png"
        :return:
        前置条件：先打开浏览器后才能截屏.
        '''

        try:
            self.driver.get_screenshot_as_file(varImageFile)
        except:
            print("error, 请检查浏览器是否打开！")

    def scrollBottom(self, t=2):

        '''
        2.6 页面滚动条到底部
        :param t:
        :return:
        '''

        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(t)



    def popupAlert(self, varText, t=1):

        '''
        3.1 弹出框
        :param varText:
        :param t:
        :return:
        '''

        # 注意这里需要转义引号
        self.driver.execute_script("alert('" + varText + "');")
        sleep(t)

    def confirmAlert(self, varOperate, t=1):

        '''
        3.2 确认弹出框
        :param operate:
        :param t:
        :return:
        '''

        if varOperate == "accept":
            self.driver.switch_to.alert.accept()
            sleep(t)
        if varOperate == "dismiss":
            self.driver.switch_to.alert.dismiss()
            sleep(t)
        if varOperate == "text":
            x = self.driver.switch_to.alert.text
            self.driver.switch_to.alert.accept()
            return x


    def kilBrowser(self):

        '''
        4.1 关闭浏览器应用
        :return:
        '''

        self.driver.quit()


    def scrollLeftByApp(self, location, t=1):

        '''
        5.1 app屏幕左移
        :param location: "1000"
        :param t:
        :return:
         # Web_PO.scrollLeft('1000')  # 屏幕向左移动1000个像素
        '''

        self.driver.execute_script("var q=document.documentElement.scrollLeft=" + location)
        sleep(t)

    def scrollRightByApp(self, location, t=1):

        '''
        5.2 app屏幕右移
        :param location: "1000"
        :param t:
        :return:
        Web_PO.scrollRight('1000', 2)  # 屏幕向右移动1000个像素
        '''

        self.driver.execute_script("var q=document.documentElement.scrollRight=" + location)
        sleep(t)

    def scrollUpByApp(self, location, t=1):

        '''
        5.3 app屏幕上移
        :param location: :1000
        :param t:
        :return:
        Web_PO.scrollTop("1000",2) # 屏幕向上移动1000个像素
        '''

        # self.driver.execute_script("var q=document.body.scrollTop=" + location)
        self.driver.execute_script("var q=document.documentElement.scrollTop=" + location)
        sleep(t)

    def scrollDownByApp(self, location, t=1):

        '''
        5.4 app屏幕下移
        :param location:
        :param t:
        :return:
        Web_PO.scrollDown("1000",2) # 屏幕向下移动1000个像素
        '''

        self.driver.execute_script("var q=document.documentElement.scrollDown=" + location)
        sleep(t)



    def scrollIntoView(self, varXpath, t=1):

        '''
        元素拖动到可见的元素
        :param varXpath:
        :param t:
        :return:
        '''

        element = self.driver.find_element_by_xpath(varXpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(t)

    def scrollTopById(self, varId, t=1):

        """2.10 内嵌窗口中滚动条操作"""

        # 若要对页面中的内嵌窗口中的滚动条进行操作，要先定位到该内嵌窗口，在进行滚动条操作
        # self.screenTopId("zy.android.healthstatisticssystem:id/vp_content",2)
        js = "var q=document.getElementById('" + varId + "').scrollTop=100000"
        self.driver.execute_script(js)
        sleep(t)

    def getCode(self, capScrnPic, xStart, yStart, xEnd, yEnd):

        """8 获取验证码 ？？"""

        # Level_PO.getCode(u"test.jpg",2060, 850, 2187, 900）
        # 注：地址是图片元素中的位置。
        self.driver.save_screenshot(capScrnPic)
        i = Image.open(capScrnPic)
        frame4 = i.crop((xStart, yStart, xEnd, yEnd))
        frame4.save(capScrnPic)
        # im = Image.open(capScrnPic)
        # imgry = im.convert('L')
        # # 去噪,G = 50,N = 4,Z = 4
        # self.clearNoise(imgry, 50, 0, 4)
        # # imgry.save(capScrnPic)
        # filename = self.saveAsBmp(capScrnPic)
        # self.RGB2BlackWhite(filename)
        # im = Image.open(capScrnPic)
        # imgry = im.convert('L')
        # ''''''''''''''''''''''''''''''''''''''
        img = Image.open(capScrnPic)
        img = img.convert("RGBA")
        pixdata = img.load()

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][0] < 90:
                    pixdata[x, y] = (0, 0, 0, 255)

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][1] < 136:
                    pixdata[x, y] = (0, 0, 0, 255)

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)

        img.save(capScrnPic)
        im = Image.open(capScrnPic)
        imgry = im.resize((1000, 500), Image.NEAREST)
        return image_to_string(imgry)

    def dynamicLoadToEnd(self, varClassValue):

        """2.3 动态加载页面滚动到底部（加载所有数据）????

        varClassValue 参数是所需加载数据，如list中class值
        Web_PO.driver.find_elements(By.CLASS_NAME, "Eie04v01")
        return: 返回所需加载数据的数量
        """

        # dynamicLoadToEnd('Eie04v01')
        num, len_now = 0, 0
        _input = self.driver.find_element(By.TAG_NAME, "body")
        while True:
            _input.send_keys(Keys.PAGE_DOWN)
            self.driver.implicitly_wait(2)
            elem = self.driver.find_elements(By.CLASS_NAME, varClassValue)
            len_cur = len(elem)
            # print(len_now, len_cur)
            if len_now != len_cur:
                len_now = len_cur
                num = 0
            elif len_now == len_cur and num <= 2:
                num = num + 1
                sleep(0.5)
            else:
                sleep(2)
                break
        return len_cur

