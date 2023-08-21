# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-7-19
# Description: 静安健康档案数据治理页面自动化更新脚本
# https://chromedriver.storage.googleapis.com/index.html
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import re, subprocess, requests, os, sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_argument("--start-maximized")
# screen_width, screen_height = pyautogui.size()  # 通过pyautogui方法获得屏幕尺寸
# print(screen_width, screen_height)
# options.add_argument('--window-size=%sx%s' % (screen_width, screen_height))
# options.add_argument('--incognito')  # 无痕隐身模式
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 不显示 chrome正受到自动测试软件的控制的提示
options.add_argument("disable-cache")  # 禁用缓存
# options.add_argument("--disable-blink-features=AutomationControlled")  # 禁止浏览器出现验证滑块
# options.add_argument(r"--user-data-dir=.\selenium_user_data")  # 设置用户文件夹，可存储登录信息，解决每次要求登录问题
# options.add_argument('--ignore-certificate-errors')
# options.add_argument("--disable-extensions")  # 禁用扩展插件的设置参数项
# options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 屏蔽--ignore-certificate-errors提示信息的设置参数项
# options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
# options.headless = True  # 无界面模式
options.add_argument('--no-sandbox')  # 解决文件不存咋的报错
options.add_argument('-disable-dev-shm-usage')  # 解决DevToolsActivePort文件不存咋的报错
options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--hide-scrollbars')  # 隐藏滚动条，因对一些特殊页面
# options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升速度
# chrome程序版本
# chromeBrowserVer = subprocess.check_output('wmic datafile where name=\"C:\\\\Users\\\\ZY\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe\" get Version /value', shell=True)
# chromeBrowserVer = str(chromeBrowserVer).split("=")[1].split("\\")[0]
# print(chromeBrowserVer) # 115.0.5790.110

# driver = webdriver.Chrome(service=Service("D:\HRDG\web\chromedriver.exe"), options=options)
driver = webdriver.Chrome(service=Service("/Users/linghuchong/.wdm/drivers/chromedriver/mac64/114.0.5735.16/chromedriver"), options=options)


from WebPO import *
Web_PO = WebPO(driver)

class JinganPO():

    def clsApp(self, varApp):
        """关闭应用程序"""
        # closeApp("chrome.exe")
        l_pid = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_pid.append(pid)
        for i in range(len(l_pid)):
            p = psutil.Process(l_pid[i])
            p.terminate()

    def reqPost(self, varUrl, headers={}, params=None):
        '''2.2 获取内容带参数'''

        # headers['User-Agent'] = self.getUserAgent()
        headers['Content-Type'] = 'application/json'
        print(headers)
        r = requests.post(url=varUrl, headers=headers, params=params)
        # r = requests.post(url=varUrl, headers=headers, params=params, proxies=self.getProxies())
        # r = requests.get(url=arUrl, headers=headers, params=params, proxies=self.getProxies(), timeout=30)

        # 如果返回的状态码不是200，则报错返回一个 HTTPError 对象，如403
        r.raise_for_status()

        # 设置内容编码，将文件第一行 # -*- coding: utf-8 -*- 即 返回内容转换成utf-8编码
        r.encoding = r.apparent_encoding
        headers['User-Agent'] = ''

        # r.text 返回响应的内容(unicode 类型数据)
        # r.content 返回响应的内容(字节为单位)  # r.content.decode("utf8", "ignore")
        # r.json 返回响应的内容(字典格式)
        return r

    def fmtData(self, varData):
        ...

    def login(self, varUrl, varUser, varPass):
        # 登录
        Web_PO.opn(varUrl)
        Web_PO.setTextById("username", varUser)
        Web_PO.setTextById("password", varPass)
        Web_PO.clkById("loginBtn", 1)

    # Web_PO.clk('/html/body/div/div[2]/div[2]/ul/li[1]/a', 1)
    # Web_PO.switchLabel(1)
    # sleep(2)
    # 健康档案
    # Web_PO.clk('/html/body/div[1]/div/div/div[2]/ul/li[3]/a', 1)
    # Web_PO.inputId("keyword",r'310107194812044641') # 魏梅娣
    # Web_PO.clk('/html/body/div[5]/div/div[1]/table/tbody/tr/td[1]/div/div', 2)
    # Web_PO.clk('/html/body/div[5]/div/div[2]/div/div[2]/div[4]/div[2]/div/table/tbody/tr[3]/td[2]/div/input[1]',1)
    # 健康档案 - 基本信息

    def setText(self, varXpath, varField):
        Web_PO.jsReadonly(varXpath)
        Web_PO.setTextEnter(varXpath, varField)


    def cjqk(self, var):

        # 基本信息 - 残疾情况

        for k, v in var.items():
            if k == '视力残疾':
                Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
            if k == '听力残疾':
                Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
            if k == '语言残疾':
                Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
            if k == '肢体残疾':
                Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[5]/span/input',1)
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
            if k == '智力残疾':
                Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[1]/span/input', 1)
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
            if k == '精神残疾':
                Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[2]/span/input', 1)
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
            if k == '其他残疾':
                Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[3]', 1)
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[4]/span/span/input', v)  # 残疾说明

    def thjdz(self, var):

        for k, v in var.items():
            if k == '省（自治区、直辖市）':
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[2]/span/span/input', v)
            if k == '市（地区/州）':
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[4]/span/span/input', v)
            if k == '县（区）':
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[6]/span/span/input', v)
            if k == '街道（镇）':
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]/span/span/input', v)
            if k == '居委（村）':
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[4]/span/span/input', v)
            if k == '详细地址':
                Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]/span/span/input', v)

    def edtBasicInfo(self, idCard):
        # 2，通过身份证打开用户页
        # Web_PO.opnLabel('http://172.16.209.10:9071/cdc/a/doctor/archive/detail?personcard=' + str(idCard))

        # Web_PO.opnLabel('http://200.200.200.14:9071/cdc/a/doctor/archive/detail?personcard=' + str(idCard))
        # Web_PO.swhLabel(1)
        # Web_PO.clkById('one2', 1)  # 基本信息

        # todo 基本信息
        #
        # var = {'姓名': '魏梅娣', '民族': '苗族', '文化程度': '小学教育', '职业': '军人', '就业状态': '其他',
        #        '婚姻状况': '离婚', '工作单位': '北京科美有限公司', '手机号': '13011234567', '固定电话': '58776543', '联系人姓名': '魏梅名', '联系人电话': '13356789098',
        #        '血型': 'B型', 'Rh血型': '不详', '医疗费用支付方式': '全自费', '残疾情况': {"智力残疾": "7777", "肢体残疾": "3333", "其他残疾": "121212"}}
        #
        # # var = {'姓名': '魏梅娣', '民族': '苗族', '文化程度': '小学教育', '职业': '军人', '就业状态': '其他',
        # #                '婚姻状况': '离婚', '工作单位': '北京科美有限公司', '手机号': '13011234567', '固定电话': '58776543', '联系人姓名': '魏梅名', '联系人电话': '13356789098',
        # #                '血型': 'B型', 'Rh血型': '不详', '医疗费用支付方式': '全自费', '残疾情况': "无残疾"}

        # for k, v in var.items():
        #     if k == '姓名':
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[1]/td[2]/span/span/input', v)
        #     if k == '民族':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[2]/span/span/input', v)
        #     if k == '文化程度':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[4]/span/span/input', v)
        #     if k == '职业':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[4]/td[2]/span/span/input', v)
        #     if k == '就业状态':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[5]/td[2]/span/span/input', v)
        #     if k == '婚姻状况':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[7]/td[2]/span/span/input', v)
        #     if k == '工作单位':
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[7]/td[4]/span/span/input', v)
        #     if k == '手机号':
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[8]/td[2]/span/span/input', v)
        #     if k == '固定电话':
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[9]/td[2]/span/span/input', v)
        #     if k == '联系人姓名':
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[10]/td[2]/span/span/input', v)
        #     if k == '联系人电话':
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[10]/td[4]/span/span/input', v)
        #     if k == '血型':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[2]/span/span/input', v)
        #     if k == 'Rh血型':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[4]/span/span/input', v)
        #     if k == '医疗费用支付方式':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[12]/td[2]/span/span/input', v)

        # dd = {'handicapState': {'no': False, "other": "5555", "spirit": True, "member": "0"} }
        #
        # # 判断
        # currStatus = Web_PO.isSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]/span/input')
        # print(currStatus)
        #
        # # cj1, 当前已勾选无，要求勾选无，什么都不做。
        # if dd['handicapState']['no'] == True and currStatus == True:
        #     ...
        # elif currStatus == True and dd['handicapState']['no'] == False:
        #     # cj2，当前已勾选无，要求勾选视力障碍
        #     Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]', 1)  # 无
        #
        #     for k, v in dd['handicapState'].items():
        #         if k == 'vision' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
        #         if k == 'audition' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
        #         if k == 'language' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
        #         if k == 'member' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[5]/span/input',1)
        #         if k == 'wit' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[1]/span/input', 1)
        #         if k == 'spirit' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[2]/span/input', 1)
        #         if k == 'other' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[3]', 1)
        #             Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[4]/span/span/input', v)  # 残疾说明
        #         if k != 'no':
        #             Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', dd['handicapState']['member'])  # 残疾证号码
        # elif currStatus == False and dd['handicapState']['no'] == True:
        #     # cj3, 当前有残疾情况，要求勾选无
        #     Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]', 1)  # 无
        # else:
        #     # cj4,当前有残疾情况，要更改残疾情况，勾选2次无，在勾选残疾情况
        #     Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]', 1)  # 无
        #     Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]', 1)  # 无
        #
        #     for k, v in dd['handicapState'].items():
        #         if k == 'vision' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
        #         if k == 'audition' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
        #         if k == 'language' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
        #         if k == 'member' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[5]/span/input',1)
        #         if k == 'wit' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[1]/span/input', 1)
        #         if k == 'spirit' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[2]/span/input', 1)
        #         if k == 'other' and v == True:
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[3]', 1)
        #             Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[4]/span/span/input', v)  # 残疾说明
        #         if k != 'no':
        #             Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', dd['handicapState']['member'])  # 残疾证号码


        # # todo 户籍地址
        # #
        # d_var = {'省（自治区、直辖市）': '上海市', '市（地区/州）': '市辖区', '县（区）': '虹口区', '街道（镇）': '广中路街道', '居委（村）': '新虹居委会', '详细地址': '洪都拉斯100号'}
        # for k, v in d_var.items():
        #     if k == '省（自治区、直辖市）':
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[2]/span/span/input', v)
        #     if k == '市（地区/州）':
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[4]/span/span/input', v)
        #     if k == '县（区）':
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[6]/span/span/input', v)
        #     if k == '街道（镇）':
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[2]/span/span/input', v)
        #     if k == '居委（村）':
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[4]/span/span/input', v)
        #     if k == '详细地址':
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[3]/td[2]/span/span/input', v)
        #
        #
        #
        # # todo 居住地址 - 同户籍地址
        #
        # needStatus = False
        # # l_var = ['北京市', '市辖区', '丰台区', '南苑街道办事处', '机场社区居委会', '洪都拉斯100号']
        # # d_var = {'省（自治区、直辖市）': '北京市', '市（地区/州）': '市辖区', '县（区）': '丰台区', '街道（镇）': '南苑街道办事处', '居委（村）': '机场社区居委会', '详细地址': '洪都拉斯100号'}
        # d_var = {'省（自治区、直辖市）': '上海市', '市（地区/州）': '市辖区', '县（区）': '徐汇区', '街道（镇）': '斜土路街道', '居委（村）': '康巨居委会', '详细地址': '洪都拉斯300号'}
        #
        # currStatus = Web_PO.isSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/thead[3]/tr/th/span/input')
        #
        # if currStatus == True:
        #     # 当前已勾选同户籍地址
        #     if needStatus == True:
        #         # cj1, 要求也是勾选同户籍地址，不操作
        #         ...
        #     else:
        #         # cj2，要求不勾选同户籍地址，操作反勾选同户籍地址，同时填入一下信息
        #         Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/thead[3]/tr/th/span/input', 1)  # 点击同户籍地址复选框
        #
        #         for k, v in d_var.items():
        #             if k == '省（自治区、直辖市）':
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[2]/span/span/input', v)
        #             if k == '市（地区/州）':
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[4]/span/span/input', v)
        #             if k == '县（区）':
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[6]/span/span/input', v)
        #             if k == '街道（镇）':
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]/span/span/input', v)
        #             if k == '居委（村）':
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[4]/span/span/input', v)
        #             if k == '详细地址':
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]/span/span/input', v)
        #
        #
        # else:
        #     # 当前未勾选同户籍地址
        #     if needStatus == True:
        #         # cj3，要求勾选同户籍地址
        #         Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/thead[3]/tr/th/span/input', 1)  # 点击同户籍地址复选框
        #     else:
        #         # cj4，要求更新当前户籍地址。
        #
        #         for k, v in d_var.items():
        #             if k == '省（自治区、直辖市）':
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[2]/span/span/input', v)
        #             if k == '市（地区/州）':
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[4]/span/span/input', v)
        #             if k == '县（区）':
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[6]/span/span/input', v)
        #             if k == '街道（镇）':
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]/span/span/input', v)
        #             if k == '居委（村）':
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[4]/span/span/input', v)
        #             if k == '详细地址':
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]/span/span/input', v)



        # todo 其他信息

        # d_var = {'家庭厨房排风设施标识': '烟囱', '家庭燃料类别': '煤', '家庭饮用水类别': '井水', '家庭厕所类别': '马桶', '家庭禽畜栏类别': '室内'}
        # for k, v in d_var.items():
        #     if k == '家庭厨房排风设施标识':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[2]/span/span/input', v)
        #     if k == '家庭燃料类别':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[4]/span/span/input', v)
        #     if k == '家庭饮用水类别':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[6]/span/span/input', v)
        #     if k == '家庭厕所类别':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[2]/span/span/input', v)
        #     if k == '家庭禽畜栏类别':
        #         self.setText('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[4]/span/span/input', v)


        # # todo: 药物过敏史
        #
        # varStatus = '有'
        # var = ['头孢类抗生素', '酒精', {"其他药物过敏原": '3333'}]
        # # 判断默认勾选的是无还是有
        # currStatus = Web_PO.getValueByAttr(u'//div[@id="signAllergy"]/table/tbody/tr/td/div/div[1]', 'class')
        # if currStatus == "mini-radiobuttonlist-item":
        #     currStatus = '无'
        # else:
        #     currStatus = '有'
        # if currStatus == '无':
        #     # cj1,默认无，要求无，不操作
        #     if varStatus == '无':
        #         ...
        #     else:
        #         # cj2，默认无，要求有，勾选有，勾选酒精
        #         Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[1]/div/table/tbody/tr/td/div[1]/div[1]/input', 1)
        #         for i in range(len(var)):
        #             if var[i] == '青霉素抗生素':
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[1]/input', 1)
        #             if var[i] == '磺胺类抗生素':
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[2]/input', 1)
        #             if var[i] == '头孢类抗生素':
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[3]/input', 1)
        #             if var[i] == '含碘药品':
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[1]/input', 1)
        #             if var[i] == '酒精':
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[2]/input', 1)
        #             if var[i] =='镇静麻醉剂':
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[3]/input', 1)
        #             if isinstance(var[i], dict) == True:
        #                 for k1, v1 in var[i].items():
        #                     if k1 == '其他药物过敏原':
        #                         Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[4]/input', 1)
        #                         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[5]/span/input', v1)
        # else:
        #     # cj3,默认有，要求无，勾选无
        #     Web_PO.clk(
        #         '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[1]/div/table/tbody/tr/td/div[1]/div[2]/input',
        #         1)
        #     if varStatus == '无':
        #         ...
        #     else:
        #         # cj4，默认有，取消所有复选框，勾选酒精
        #         Web_PO.clk(
        #             '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[1]/div/table/tbody/tr/td/div[1]/div[1]/input',
        #             1)
        #         for i in range(1, 3):
        #             Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[' + str(i) + ']/input')
        #         for i in range(1, 4):
        #             Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[' + str(i) + ']/input')
        #         for i in range(len(var)):
        #             if var[i] == '青霉素抗生素':
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[1]/input', 1)
        #             if var[i] == '磺胺类抗生素':
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[2]/input', 1)
        #             if var[i] == '头孢类抗生素':
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[3]/input', 1)
        #             if var[i] == '含碘药品':
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[1]/input', 1)
        #             if var[i] == '酒精':
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[2]/input', 1)
        #             if var[i] =='镇静麻醉剂':
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[3]/input', 1)
        #             if isinstance(var[i], dict) == True:
        #                 for k1, v1 in var[i].items():
        #                     if k1 == '其他药物过敏原':
        #                         Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[4]/input', 1)
        #                         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[5]/span/input', v1)



        # # 环境危险因素暴露类别
        # # 'environmentDanger': {'no' : true, 'chemistry' : false, 'poison':false, 'ray': true, 'notInDetail': true , 'other':'111'}
        # dd = {'environmentDanger': {'no' : False, 'chemistry' : True, 'poison':True, 'ray': True, 'notInDetail': False , 'other':'111'}  }
        #
        # # 判断是否勾选了无
        # currStatus = Web_PO.isSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input')
        # # print(currStatus)
        #
        # # cj1, 当前已勾选无，要求勾选无，什么都不做。
        # if currStatus == True and dd['environmentDanger']['no'] == True:
        #     ...
        # elif currStatus == True and dd['environmentDanger']['no'] == False:
        #     # cj2，当前已勾选无，要求勾选视力障碍
        #         # 取消无勾选
        #         Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input', 1)  # 无
        #
        #         for k1, v1 in dd['environmentDanger'].items():
        #             if k1 == 'chemistry' and v1 == True :
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
        #             if k1 == 'poison' and v1 == True :
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
        #             if k1 == 'ray' and v1 == True :
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
        #             if k1 == 'notInDetail' and v1 == True :
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[1]/span/input', 1)
        #             if k1 == 'other' :
        #                 Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[2]/span/input', 1)
        #                 Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[3]/span/span/input', v1)
        # elif currStatus == False and dd['environmentDanger']['no'] == True:
        #     # cj3, 当前有残疾情况，要求勾选无
        #     Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input', 1)  # 无
        # else:
        #     # cj4,当前有残疾情况，要更改残疾情况，勾选2次无，在勾选残疾情况
        #     Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input', 1)  # 无
        #     Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input', 1)  # 无
        #
        #     for k1, v1 in dd['environmentDanger'].items():
        #         if k1 == 'chemistry' and v1 == True :
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
        #         if k1 == 'poison' and v1 == True :
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
        #         if k1 == 'ray' and v1 == True :
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
        #         if k1 == 'notInDetail' and v1 == True :
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[1]/span/input', 1)
        #         if k1 == 'other' :
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[2]/span/input', 1)
        #             Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[3]/span/span/input', v1)



        # # todo 疾病信息
        # # # 疾病史
        # # 风险1：不知道当前用户有多少疾病史，默认最多5个，全部关闭。???
        # varQty = 10
        # dd = {'disease':[{'type':'脑卒中', 'date':'2010-12-01'},
        #                  {'type':'其他法定传染病', 'name':'1212', 'date':'2010-12-03'},
        #                   {'type':'其他', 'name':'6666', 'date':'2010-12-06'}]}
        #
        # for i in range(varQty):
        #     Web_PO.jsReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[2]/td[3]/span[1]/span/input')
        #     x = Web_PO.isElementAttr(
        #         "/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[2]/td[3]/span[1]/span/input",
        #         "disabled")
        #     if x == False:
        #         Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[2]/td[2]/input', 1)  # -
        #         Web_PO.clk(u"//a[@href='javascript:void(0)']", 2)  # 弹框确认
        #     else:
        #         break
        # x = 1
        #
        # for d in range(len(dd['disease'])):
        #     x = x + 1
        #     # print(dd['disease'][d])
        #     Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[1]/td[2]/input[1]')  # +
        #     if dd['disease'][d]['type'] == '其他' or dd['disease'][d]['type'] == '其他法定传染病':
        #         Web_PO.jsReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[1]/span/input')
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[1]/span/input', dd['disease'][d]['type'])
        #         sleep(2)
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[2]/span/input', dd['disease'][d]['name'])
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', dd['disease'][d]['date'])
        #     else:
        #         Web_PO.jsReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[1]/span/input')
        #         Web_PO.setTextEnter('//html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[1]/span/input', dd['disease'][d]['type'])
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', dd['disease'][d]['date'])





        # # # 手术史
        # dd = {'operation': {'value': False,
        #                     'relation': [{'name': '手术5', 'date': '2010-12-01'}, {'name': '手术2', 'date': '2010-12-03'}]
        #                     }
        #       }
        # # cj1，要求无，点击无，弹出框确认
        # currStatus = Web_PO.isSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input')
        # # print(currStatus)
        # Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input', 1)  # 无
        # if Web_PO.isElement(u"//a[@href='javascript:void(0)']") == True:
        #     Web_PO.clk(u"//a[@href='javascript:void(0)']", 1)  # 确定删除记录
        # # cj2,默认无，要求有，点击有，输入内容
        # # cj3，默认有，要求有，修改原有数据
        # if dd['operation']['value'] == True:
        #     Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[1]/input', 1)  # 有
        #     x = 1
        #     for d in range(len(dd['operation']['relation'])):
        #         # print(dd['operation']['relation'][d])
        #         x = x + 1
        #         Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr/td[2]/input', 1)  # +
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr[' + str(x) + ']/td[3]/span/span/input', dd['operation']['relation'][d]['name'])  # 名称
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', dd['operation']['relation'][d]['date'])  # 手术日期



        # # 外伤史
        # dd = {'trauma': {'value': True,
        #                         'relation': [{'name': '外伤3', 'date': '2010-12-01'},
        #                                      {'name': '外伤4', 'date': '2010-12-03'}]
        #                         }
        #           }
        # # cj1，要求无，点击无，弹出框确认
        # currStatus = Web_PO.isSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input')
        # Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input', 1)  # 无
        # if Web_PO.isElement(u"//a[@href='javascript:void(0)']") == True:
        #     Web_PO.clk(u"//a[@href='javascript:void(0)']", 1)  # 确定删除记录
        # # cj2,默认无，要求有，点击有，输入内容
        # # cj3，默认有，要求有，修改原有数据
        # if dd['trauma']['value'] == True:
        #     Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[1]/input', 1)  # 有
        #     x = 1
        #     for d in range(len(dd['trauma']['relation'])):
        #         x = x + 1
        #         Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr/td[2]/input', 1)  # +
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr[' + str(x) + ']/td[3]/span/span/input', dd['trauma']['relation'][d]['name'])  # 名称
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', dd['trauma']['relation'][d]['date'])  # 发生日期


        # sys.exit(0)

        # # 输血史
        # dd = {'transfusion': {'value': True,
        #                  'relation': [{'name': '输血7', 'date': '2010-12-01'},
        #                               {'name': '输血8', 'date': '2010-12-03'}]
        #                  }
        #       }
        # # cj1，要求无，点击无，弹出框确认
        # currStatus = Web_PO.isSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input')
        # Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input', 1) # 无
        # if Web_PO.isElement(u"//a[@href='javascript:void(0)']") == True:
        #     Web_PO.clk(u"//a[@href='javascript:void(0)']", 1)  # 确定删除记录
        # # cj2,默认无，要求有，点击有，输入内容
        # # cj3，默认有，要求有，修改原有数据
        # if dd['transfusion']['value'] == True:
        #     Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[1]/input', 1)# 有
        #     x = 1
        #     for d in range(len(dd['transfusion']['relation'])):
        #         x = x + 1
        #         Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr/td[2]/input', 1)  # +
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr[' + str(x) + ']/td[3]/span/span/input', dd['transfusion']['relation'][d]['name'])  # 名称
        #         Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', dd['transfusion']['relation'][d]['date'])  # 发生日期

        # sys.exit(0)





        # 家族史
        # # epidemic = 其他法定传染病
        # # other = 其他
        # dd = {'clan': [
        #     {'relation': "母亲", 'dis': ['高血压', '糖尿病', '其他法定传染病', '其他'], 'epidemic': "1212", 'other':"456"},
        #     {'relation': "父亲", 'dis': ['高血压', '糖尿病', '其他法定传染病', '贫血'], 'epidemic': "1212"}]
        # }
        # for i in range(8):
        #     if Web_PO.isElement('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[2]/input') == True:
        #         Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[2]/input', 1)  # -
        #         if Web_PO.isElement(u"//a[@href='javascript:void(0)']") == True:
        #             Web_PO.clk(u"//a[@href='javascript:void(0)']", 1)  # 确定删除记录
        #     else:
        #         break
        # for d in range(len(dd['clan'])):
        #     # print(dd['clan'][d])
        #     Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr/td[2]/input', 1)  # +
        #     Web_PO.jsReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[3]/span/span/input')  # 家庭关系
        #     Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[3]/span/span/input', dd['clan'][d]['relation'])  # mother
        #     for i in range(len(dd['clan'][d]['dis'])):
        #         # print(dd['clan'][d]['dis'][i])
        #         if dd['clan'][d]['dis'][i] == '高血压':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[2]/input',1) # 高血压
        #         if dd['clan'][d]['dis'][i] == '糖尿病':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[3]/input',1) # 糖尿病
        #         if dd['clan'][d]['dis'][i] == '冠心病':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[4]/input',1) # 冠心病
        #         if dd['clan'][d]['dis'][i] == '慢性阻塞性肺疾病':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[5]/input',1) # 慢性阻塞性肺疾病
        #         if dd['clan'][d]['dis'][i] == '恶性肿瘤':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[6]/input',1) # 恶性肿瘤
        #         if dd['clan'][d]['dis'][i] == '脑卒中':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[7]/input',1) # 脑卒中
        #         if dd['clan'][d]['dis'][i] == '重性精神疾病':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[8]/input',1) # 重性精神疾病
        #         if dd['clan'][d]['dis'][i] == '结核病':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[9]/input',1) # 结核病
        #         if dd['clan'][d]['dis'][i] == '肝炎':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[10]/input',1) # 肝炎
        #         if dd['clan'][d]['dis'][i] == '先天畸形':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[11]/input',1) # 先天畸形
        #         if dd['clan'][d]['dis'][i] == '职业病':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[12]/input',1) # 职业病
        #         if dd['clan'][d]['dis'][i] == '肾脏疾病':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[13]/input',1) # 肾脏疾病
        #         if dd['clan'][d]['dis'][i] == '贫血':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[14]/input',1) # 贫血
        #         if dd['clan'][d]['dis'][i] == '其他法定传染病':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[15]/input',1)  # 其他法定传染病
        #             Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[16]/span/input', dd['clan'][d]['epidemic'])
        #         if dd['clan'][d]['dis'][i] == '其他':
        #             Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[17]/input',1)  # 其他法定传染病
        #             Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[18]/span/input', dd['clan'][d]['other'])


        # 遗传性疾病史
        dd = {'transmissibility':'test'}
        Web_PO.setTextEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[6]/tbody/tr/td[2]/span/span/textarea', dd['transmissibility'])

        # 保存
        # Web_PO.setTextById('button1', 1)
        Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[4]/input', 1)

        # 关闭
        # Web_PO.clk('/html/body/div[1]/div/div[2]/div[2]/div/div/div[4]/a/input', 1)

