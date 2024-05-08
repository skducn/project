# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-5-7
# Description: 区域平台
# 测试环境 # http://192.168.0.213:1080/admin/login  jh/123456
#***************************************************************

from Qypt_web_PO import *
qypt_web_PO = Qypt_web_PO()

qypt_web_PO.clsApp("Google Chrome")

# 1, 登录
qypt_web_PO.login('http://192.168.0.213:1080/admin/login', 'jh', '123456')

# 2, 打开应用
d_menuUrl = qypt_web_PO.clkApp("平台管理系统")

# 3.1 选择一级菜单
Web_PO.opn(d_menuUrl['应用管理'], 2)

# 3.2 选择二级菜单, 权限管理 - 用户管理
Web_PO.opn(d_menuUrl['用户管理'], 2)

# 4, 用户管理 - 搜索，检查搜索结果
qypt_web_PO.userManager_search("登录名", "mql", "招远市妇幼医院", "启用")
Web_PO.refresh()
qypt_web_PO.userManager_search("用户工号", "wg", "第一人民医院", "启用")
Web_PO.refresh()
qypt_web_PO.userManager_search("用户姓名", "卫生局", "卫生局", "")
Web_PO.refresh()
qypt_web_PO.userManager_search("登录名", "", "招远市妇幼医院", "限制登录")
Web_PO.refresh()



# Web_PO.opn(d_menuUrl['角色管理'])
# sleep(3)
# Web_PO.opn(d_menuUrl['安全规则管理'])
# sleep(3)
# Web_PO.opn(d_menuUrl['接入系统登记'])
# sleep(3)
# Web_PO.opn(d_menuUrl['标准管理'])
# sleep(3)
# Web_PO.opn(d_menuUrl['卫生数据集'])
# sleep(3)
# Web_PO.opn(d_menuUrl['卫生数据元值域'])
# sleep(3)
# Web_PO.opn(d_menuUrl['CDA标准'])
# sleep(3)
# Web_PO.opn(d_menuUrl['DRG规则设置'])




