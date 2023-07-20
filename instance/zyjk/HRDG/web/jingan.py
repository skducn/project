# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-7-19
# Description: 静安健康档案数据治理页面自动化更新脚本
# https://chromedriver.storage.googleapis.com/index.html
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.

from BasePO import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import psutil

def closeApp(varApp):
    """关闭应用程序"""
    l_pid = []
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == varApp:
            l_pid.append(pid)
    for i in range(len(l_pid)):
        p = psutil.Process(l_pid[i])
        p.terminate()
closeApp("chrome.exe")


options = Options()
options.add_argument("--start-maximized")
s = Service("d:\project\web\chromedriver.exe")
driver = webdriver.Chrome(service=s, options=options)
# print(driver.capabilities['browserVersion'])
# print(driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])
Base_PO = BasePO(driver)

# 1，登录页
driver.get('http://172.16.209.10:9071/health/select')
Base_PO.inputId("username", "panxiaoye")
Base_PO.inputId("password","Pamam751200")
Base_PO.clickId("loginBtn", 1)

# Base_PO.clickXpath('/html/body/div/div[2]/div[2]/ul/li[1]/a', 1)
# Base_PO.switchLabel(1)
# sleep(2)

# 健康档案
# Base_PO.clickXpath('/html/body/div[1]/div/div/div[2]/ul/li[3]/a', 1)
# Base_PO.inputId("keyword",r'310107194812044641') # 魏梅娣
# Base_PO.clickXpath('/html/body/div[5]/div/div[1]/table/tbody/tr/td[1]/div/div', 2)
# Base_PO.clickXpath('/html/body/div[5]/div/div[2]/div/div[2]/div[4]/div[2]/div/table/tbody/tr[3]/td[2]/div/input[1]',1)
# 健康档案 - 基本信息

# 2，通过身份证打开用户页
driver.get('http://172.16.209.10:9071/cdc/a/doctor/archive/detail?personcard=310107194812044641')
# Base_PO.switchLabel(1)
Base_PO.clickId('one2',1)  # 基本信息

# todo 基本信息
# 姓名
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[1]/td[2]/span/span/input', '魏梅娣')
# 民族
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[2]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[2]/span/span/input', '苗族')
# 文化程度
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[4]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[4]/span/span/input', '小学教育')
# 职业
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[4]/td[2]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[4]/td[2]/span/span/input', '军人')
# 就业状态
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[5]/td[2]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[5]/td[2]/span/span/input','其他')
# 婚姻状况
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[7]/td[2]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[7]/td[2]/span/span/input','离婚')
# 工作单位
Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[7]/td[4]/span/span/input','北京科美有限公司')
# 手机号
Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[8]/td[2]/span/span/input','13011234567')
# 固定电话
Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[9]/td[2]/span/span/input','58776543')
# 联系人姓名
Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[10]/td[2]/span/span/input','魏梅名')
# 联系人电话
Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[10]/td[4]/span/span/input','13356789098')
# 血型 ？？
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[2]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[2]/span/span/input','B型')
# Rh血型
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[4]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[4]/span/span/input','B型')
# 医疗费用支付方式
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[12]/td[2]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[12]/td[2]/span/span/input','全自费')
# 残疾情况
varParam = "视力残疾"
isNoDisability = Base_PO.isCheckbox('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]/span/input')  # 无残疾是否勾选
# cj1,默认无残疾，要求无残疾，不操作
if isNoDisability == True:
    if varParam == "无":
        ...
    else:
        # cj2,默认无残疾，要求视力残疾，翻勾选无，勾选视力残疾。
        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]', 1)  # 无
        # 勾选精神残疾。
        if varParam == '视力残疾':
            Base_PO.clickXpath(
                '/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[2]/span/input',
                1)
        if varParam == '听力残疾':
            Base_PO.clickXpath(
                '/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[3]/span/input',
                1)
        if varParam == '语言残疾':
            Base_PO.clickXpath(
                '/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[4]/span/input',
                1)
        if varParam == '肢体残疾':
            Base_PO.clickXpath(
                '/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[5]/span/input',
                1)
        if varParam == '智力残疾':
            Base_PO.clickXpath(
                '/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[6]/span/input',
                1)
        if varParam == '精神残疾':
            Base_PO.clickXpath(
                '/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[7]/span/input',
                1)
        if varParam == '其他残疾':
            Base_PO.clickXpath(
                '/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[3]',
                1)
            Base_PO.inputXpathClearEnter(
                '/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[4]/span/span/input',
                'reason')  # 残疾说明
        # 残疾证号码
        Base_PO.inputXpathClear(
            '/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', '1234')

if isNoDisability == False:
    # cj3,默认视力残疾，要求无残疾，勾选无残疾。
    if varParam == '无':
        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]', 1)  # 无
    # cj4，默认视力残疾，要求精神残疾，操作取消所有勾选，勾选精神残疾。
    else:
        # 取消所有勾选项
        Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[2]/span/input') # 视力残疾
        Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[3]/span/input') # 听力残疾
        Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[4]/span/input') # 语言残疾
        Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[5]/span/input') # 肢体残疾
        Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[1]/span/input') # 智力残疾
        Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[2]/span/input') # 精神残疾
        Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[3]/span/input') # 其他残疾
        # 勾选精神残疾。
        if varParam == '视力残疾':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[2]/span/input',1)
        if varParam == '听力残疾':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
        if varParam == '语言残疾':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
        if varParam == '肢体残疾':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[5]/span/input', 1)
        if varParam == '智力残疾':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[6]/span/input', 1)
        if varParam == '精神残疾':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[7]/span/input', 1)
        if varParam == '其他残疾':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[3]',1)
            Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[4]/span/span/input', 'reason')  # 残疾说明
        # 残疾证号码
        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', '1234')



#todo 户籍地址

# 省（自治区、直辖市）
# Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[2]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[2]/span/span/input','北京市')
# 市（地区/州）
# Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[4]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[4]/span/span/input','市辖区')
# 县（区）
# Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[6]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[6]/span/span/input','丰台区')
# 街道（镇）
# Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[2]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[2]/span/span/input','南苑街道办事处')
# 居委（村）
# Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[4]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[4]/span/span/input','机场社区居委会')
# 详细地址
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[3]/td[2]/span/span/input','洪都拉斯100号')

# todo 居住地址
# 同户籍地址
varParam = True
isThjdz = Base_PO.isCheckbox('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/thead[3]/tr/th/span/input')
if isThjdz == True:
    # cj1, 默认是勾选同户籍地址，要求也是勾选同户籍地址，不操作
    if varParam == True:
        ...
    else:
        # cj2，默认是勾选同户籍地址，要求不勾选同户籍地址，操作反勾选同户籍地址，同时填入一下信息
        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/thead[3]/tr/th/span/input',1) # 不勾选同户籍地址
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[2]/span/span/input','北京市')  # 省（自治区、直辖市）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[4]/span/span/input','市辖区') # 市（地区/州）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[6]/span/span/input','丰台区') # 县（区）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]/span/span/input','南苑街道办事处') # 街道（镇）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[4]/span/span/input','机场社区居委会') # 居委（村）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]/span/span/input','洪都拉斯100号') # 详细地址
else:
    # cj3，默认是不勾选同户籍地址，要求勾选同户籍地址
    if varParam == True:
        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/thead[3]/tr/th/span/input', 1)
    else:
        # cj4,默认是不勾选同户籍地址，要求更新以下信息。
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[2]/span/span/input','北京市')  # 省（自治区、直辖市）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[4]/span/span/input','市辖区') # 市（地区/州）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[6]/span/span/input','丰台区') # 县（区）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]/span/span/input','南苑街道办事处') # 街道（镇）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[4]/span/span/input','机场社区居委会') # 居委（村）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]/span/span/input','洪都拉斯100号') # 详细地址


# todo 其他信息
# 家庭厨房排风设施标识
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[2]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[2]/span/span/input','烟囱')
# 家庭燃料类别
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[4]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[4]/span/span/input', '煤')
# 家庭饮用水类别
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[6]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[6]/span/span/input', '井水')
# 家庭厕所类别
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[2]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[2]/span/span/input','马桶')
# 家庭禽畜栏类别
Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[4]/span/span/input')
Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[4]/span/span/input','室内')
# 药物过敏史
varParam = '有'
var = '头孢类抗生素'
# 判断默认勾选的是无还是有
isYwgms = Base_PO.getXpathAttr(u'//div[@id="signAllergy"]/table/tbody/tr/td/div/div[1]','class')
# print(isYwgms)
# isYwgms = Base_PO.getXpathAttr(u'//div[@id="signAllergy"]/table/tbody/tr/td/div/div[2]','class')
# print(isYwgms)
if isYwgms == "mini-radiobuttonlist-item":
    isYwgms = '无'
else:
    isYwgms = '有'
if isYwgms == '无':
    # cj1,默认无，要求无，不操作
    if varParam == '无':
        ...
    else:
        # cj2，默认无，要求有，勾选有，勾选酒精
        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[1]/div/table/tbody/tr/td/div[1]/div[1]/input',1)
        # ???
else:
    # cj3,默认有，要求无，勾选无
    if varParam == '无':
        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[1]/div/table/tbody/tr/td/div[1]/div[2]/input', 1)
    else:
        # cj4，默认有，取消所有复选框，勾选酒精
        for i in range(1, 3):
            Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[' + str(i) + ']/input')
        for i in range(1, 4):
            Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[' + str(i) + ']/input')
        if var == '青霉素抗生素':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[1]/input', 1)
        if var == '磺胺类抗生素':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[2]/input', 1)
        if var == '头孢类抗生素':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[3]/input', 1)
        if var == '含碘药品':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[1]/input', 1)
        if var == '酒精':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[2]/input', 1)
        if var =='镇静麻醉剂':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[3]/input', 1)
        if var =='其他药物过敏原':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[4]/input', 1)
            Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[5]/span/input', '1111')

# 环境危险因素暴露类别
varParam = False
var = '毒物'

# 判断是否勾选了无
isNo = Base_PO.isCheckbox('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input')
if isNo == True:
    # cj1,默认勾选无，要求勾选无，不操作。
    if varParam == True:
        ...
    # cj2，默认勾选无，要求勾选其他，操作取消无勾选，勾选其他
    elif varParam == False:
        # 取消无勾选
        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input', 1)
        if var == '化学品':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
        if var == '毒物':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
        if var == '射线':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
        if var == '不详':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[1]/span/input', 1)
        if var == '其他':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[2]/span/input', 1)
            Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[3]/span/span/input', '222222')
else:
    # cj3，默认不勾选无，要求勾选无，直接勾选无。
    if varParam == True:
        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input', 1)
    else:
        # cj4，默认不勾选无，要求勾选化学，操作取消所有勾选，勾选化学。
        Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[2]/span/input')
        Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[3]/span/input')
        Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[4]/span/input')
        Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[1]/span/input')
        Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[2]/span/input')
        if var == '化学品':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
        if var == '毒物':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
        if var == '射线':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
        if var == '不详':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[1]/span/input', 1)
        if var == '其他':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[2]/span/input', 1)
            Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[3]/span/span/input', '222222')

# todo 疾病信息




# Base_PO.clickId('button1', 1)  # 保存
# Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[4]/a/input', 1)  #关闭

