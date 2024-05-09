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
d_menuUrl = qypt_web_PO.clkApp("平台管理系统")

# 3.1 应用管理
# Web_PO.opn(d_menuUrl['应用管理'], 2)

# 3.2 权限管理
Web_PO.opn(d_menuUrl['用户管理'], 2)
# 3.2.1, 用户管理 - 搜索，检查搜索结果
qypt_web_PO.platformManagement_userManagement_search("登录名", "mql", "招远市妇幼医院", "启用")
Web_PO.refresh()
qypt_web_PO.platformManagement_userManagement_search("用户工号", "wg", "第一人民医院", "启用")
Web_PO.refresh()
qypt_web_PO.platformManagement_userManagement_search("用户姓名", "卫生局", "卫生局", "")
Web_PO.refresh()
qypt_web_PO.platformManagement_userManagement_search("登录名", "", "招远市妇幼医院", "限制登录")
Web_PO.refresh()

# 3.3 权限管理
# Web_PO.opn(d_menuUrl['角色管理'], 2)

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




