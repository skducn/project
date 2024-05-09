# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-5-7
# Description: 区域平台
# 测试环境 # http://192.168.0.213:1080/admin/login  jh/123456
#***************************************************************

from Qypt_web_PO import *
qypt_web_PO = Qypt_web_PO()

# qypt_web_PO.clsApp("Google Chrome")

# 1, 登录
qypt_web_PO.login('http://192.168.0.213:1080/admin/login', 'jh', '123456')

# 2, 打开应用
d_menuUrl = qypt_web_PO.clkApp("主数据管理")

# 3.1 机构管理
Web_PO.opn(d_menuUrl['机构管理'], 2)
# qypt_web_PO.mainDataManagement_orgManagement_search({"机构名称": "卫生局15", "机构类别": "", "所属街道": "", "状态": ""})
# Web_PO.refresh()
# qypt_web_PO.mainDataManagement_orgManagement_search({"机构名称": "", "机构类别": "医院", "所属街道": "", "状态": ""})
# Web_PO.refresh()
# qypt_web_PO.mainDataManagement_orgManagement_search({"机构名称": "", "机构类别": "", "所属街道": "泉山街道", "状态": ""})
# Web_PO.refresh()
# qypt_web_PO.mainDataManagement_orgManagement_search({"机构名称": "卫生局", "机构类别": "", "所属街道": "辛庄镇", "状态": ""})
# Web_PO.refresh()
qypt_web_PO.mainDataManagement_orgManagement_search({"机构名称": "", "机构类别": "医院", "所属街道": "泉山街道", "状态": ""})
Web_PO.refresh()
qypt_web_PO.mainDataManagement_orgManagement_search({"机构名称": "", "机构类别": "医院", "所属街道": "泉山街道", "状态": "启用"})


# 操作 - 状态、修改、删除
# qypt_web_PO.mainDataManagement_orgManagement_revise("启用", {"机构名称": "卫生局15", "招远市医疗机构代码": "0001", "机构类别": "卫生局", "所属街道": "辛庄镇", "机构地址": "百度", "状态": "启用"}, "")


# # 3.2 科室管理
# Web_PO.opn(d_menuUrl['科室管理'], 2)
# # 3.3 卫生人员管理
# Web_PO.opn(d_menuUrl['卫生人员管理'], 2)
# # 3.4 卫生人力资源安排
# Web_PO.opn(d_menuUrl['卫生人力资源安排'], 2)

# 3.5 字典映射
# Web_PO.opn(d_menuUrl['标准值域管理'], 2)
# 3.6 字典映射
# Web_PO.opn(d_menuUrl['待映射字典注册'], 2)
# 3.7 字典映射
# Web_PO.opn(d_menuUrl['字典映射'], 2)








