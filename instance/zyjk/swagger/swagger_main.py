# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : 获取swagger内容 另存为excel
# http://192.168.0.238:8801/doc.html
# http://192.168.0.238:8801/saasuser/v2/api-docs
# http://192.168.0.238:8090/doc.html
# *********************************************************************

from SwaggerPO import *
SwaggerPO_PO = SwaggerPO()

SwaggerPO_PO.getAll('http://192.168.0.238:8801', '/doc.html', 'saas.xlsx')


SwaggerPO_PO.getOne('http://192.168.0.238:8801', '/doc.html', "auth", "auth.xlsx")
# SwaggerPO_PO.getI('http://192.168.0.238:8801', '/doc.html', "saasuser", "saasuser.xlsx")
# SwaggerPO_PO.getI('http://192.168.0.238:8801', '/doc.html',"cms", "cms.xlsx")
# SwaggerPO_PO.getI('http://192.168.0.238:8801', '/doc.html',"oss", "oss.xlsx")
# SwaggerPO_PO.getI('http://192.168.0.238:8801', '/doc.html',"saascrf", "saascrf.xlsx")
# SwaggerPO_PO.getI('http://192.168.0.238:8801', '/doc.html',"ecg", "ecg.xlsx")
# SwaggerPO_PO.getI('http://192.168.0.238:8801', '/doc.html',"cuser", "cuser.xlsx")
# SwaggerPO_PO.getI('http://192.168.0.238:8801', '/doc.html', "hypertension", "hypertension.xlsx")


# SwaggerPO_PO.getI('http://192.168.0.238:8090', '/doc.html', "default", "erp.xlsx")



