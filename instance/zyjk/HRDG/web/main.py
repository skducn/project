# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-22
# Description: 静安健康档案数据治理页面自动化更新脚本
#***************************************************************


from JinganPO import *
Jingan_PO = JinganPO()
Jingan_PO.clsApp("chrome.exe")

# 1，获取业务数据
# d_data = Jingan_PO.reqPost(varurl)
# d_fData = fmtData(d_data) #格式化数据格式


# 2，医生登录并且更新数据
Jingan_PO.login('http://172.16.209.10:9071/health/select', "panxiaoye", "Pamam751200")
Jingan_PO.edtBasicInfo("310107194812044641")  # 魏梅娣

# try:
#     for d in range(len(d_fData)):
#         Jingan_PO.edtBasicInfo(d_fData)
#         Web_PO.cls()
# except:
#     print(d_fData[idcard])

# 3，回填接口 更新状态
# Jingan_PO.reqPost(varurl)
