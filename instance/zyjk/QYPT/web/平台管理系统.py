# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-5-7
# Description: 区域平台
# 测试环境 # http://192.168.0.213:1080/admin/login  jh/123456
# typ: 选择解析yaml的方式
#  'rt'/None -> RoundTripLoader/RoundTripDumper(默认)
#  'safe'    -> SafeLoader/SafeDumper,
#  'unsafe'  -> normal/unsafe Loader/Dumper
#  'base'    -> baseloader
#***************************************************************


import pandas as pd
from Qypt_web_PO import *
qypt_web_PO = Qypt_web_PO()
qypt_web_PO.clsApp("Google Chrome")

from PO.OpenpyxlPO import *

from ruamel.yaml import YAML
yaml = YAML(typ='safe')

# todo 系统模块与菜单
with open('sys.yml', encoding='utf-8') as file:
    d_sys = yaml.load(file)
# print(d_sys)

# todo 平台管理系统测试用例
with open('case_platform.yml', encoding='utf-8') as file:
    d_case_platform = yaml.load(file)
# print(d_case_platform)



# --------------------------------------------------------------------------------------------

qypt_web_PO.login(d_sys['login']['url'], d_sys['login']['user'], d_sys['login']['pass'])  # 登录
d_menuUrl = qypt_web_PO.clkApp(d_sys['app']['platform'])  # 平台管理系统
# Web_PO.opn(d_menuUrl[d_sys['app']['platform_M']['application']], 2)  # 应用管理

'''权限管理 - 用户管理'''
Web_PO.opn(d_menuUrl[d_sys['app']['platform_M']['user']], 2)

l_all = []
l_c = []

# print(len(d_case_platform['user']))
for i in range(len(d_case_platform['user'])):
    NO = 'c' + str(i+1)
    actuall, r = qypt_web_PO.platform_user_search(NO, d_case_platform['user'][NO])
    # [平台管理系统,用户管理,检查点,预期值,实测值,结果]
    l_c = [NO, d_case_platform['name'], d_sys['app']['platform_M']['user'], d_case_platform['user'][NO][0], d_case_platform['user'][NO][5], actuall, r]
    l_all.append(l_c)
    l_c = []
    # 将yaml转excel
    Openpyxl_PO = OpenpyxlPO("101.xlsx")
    Openpyxl_PO.setRows({1: ["编号", "应用", "菜单", "检查点", "预期值", "实际值", "结果"]}, "Sheet1")
    Openpyxl_PO.appendRows(l_all)
    Openpyxl_PO.setAllCellDimensions(30, 20)
    Openpyxl_PO.setAllWordWrap("Sheet1")
    Openpyxl_PO.setFreeze('A1', "Sheet1")
    Openpyxl_PO.setRowColColor(1, "all", "ff0000")  # 设置第1行所有列背景色
    Openpyxl_PO.setRowColFont(1, "all")  # 第1行
    Openpyxl_PO.setCellDimensions(1, 30, 'd', 44)  # 设置第三行行高30，第f列宽34

    l_all = []

qypt_web_PO.clsApp("Google Chrome")


# Web_PO.opn(d_menuUrl[d_sys['app']['platform_M']['role']], 2)  # 权限管理 - 角色管理

# 3.4 安全管理
# Web_PO.opn(d_menuUrl['安全规则管理'], 2)
# 3.5 安全管理
# Web_PO.opn(d_menuUrl['接入系统登记'], 2)

# 3.6 标准注册
# Web_PO.opn(d_menuUrl['标准管理'], 2)
# 3.7 标准注册
# Web_PO.opn(d_menuUrl['卫生数据集'], 2)
# 3.8 标准注册
# Web_PO.opn(d_menuUrl['卫生数据元值域'], 2)
# 3.9 标准注册
# Web_PO.opn(d_menuUrl['CDA标准'], 2)

# 3.10 DRG分组管理
# Web_PO.opn(d_menuUrl['DRG规则设置'], 2)




