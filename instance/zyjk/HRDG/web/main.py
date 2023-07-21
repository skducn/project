# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-22
# Description:
#***************************************************************

import os, sys
sys.path.append("../../../../")

from JinganPO import *
Jingan_PO = JinganPO()
Jingan_PO.closeApp("chrome.exe")

# 业务
Jingan_PO.login('http://172.16.209.10:9071/health/select', "panxiaoye", "Pamam751200")

# 1，获取数据源，通过医生，获取他所有患者信息，每个患者用身份证识别
# data = interface1('panxiaoye')
# 遍历获取每个患者数据（身份证）
idCard = {'310107194812044641': data}

# 2，更新数据
Jingan_PO.basicInfo({'310107194812044641': data})
Jingan_PO.basicInfo({'310107194812044641': data})

# 3，回填状态
# interface2(id, 状态)