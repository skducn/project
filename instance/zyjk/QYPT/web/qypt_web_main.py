# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-5-7
# Description: 区域平台
# 测试环境 # http://192.168.0.213:1080/admin/login  jh/123456

#***************************************************************

from PO.SysPO import *
Sys_PO = SysPO()

from Qypt_web_PO import *
qypt_web_PO = Qypt_web_PO()

varUrl = 'http://192.168.0.213:1080/admin/login'

# 1, 登录
qypt_web_PO.login(varUrl, 'jh', '123456')

# 2, 打开应用列表
qypt_web_PO.clkApp("平台管理系统")

# 3，点击菜单
# qypt_web_PO.clkMenu("应用管理")
# qypt_web_PO.clkMenu("权限管理", "角色管理")
qypt_web_PO.clkMenu("标准注册", "卫生数据集")










# 签约居民管理 - 健康服务
# Web_PO.opn(varUrl + 'SignManage/service')








# # 签约居民管理 - 健康评估
# Web_PO.opnLabel(varUrl + 'SignManage/signAssess')
# # 用户中心 -机构维护
# Web_PO.opnLabel(varUrl + 'UserManage/org')
# # 用户中心 -用户维护
# Web_PO.opnLabel(varUrl + 'UserManage/user')
# # 用户中心 -角色维护
# Web_PO.opnLabel(varUrl + 'UserManage/role')
# # 用户中心 -接口管理
# Web_PO.opnLabel(varUrl + 'UserManage/interface')


# 社区配置 - 常住人口
# Web_PO.opnLabel(varUrl + 'Community/permanent')
# 社区配置 - 家医团队维护
# Web_PO.opnLabel(varUrl + 'Community/team')
# 社区配置 - 家医助手
# Web_PO.opnLabel(varUrl + 'Community/assistant')


# 系统监控 - 定时任务
# Web_PO.opnLabel(varUrl + 'monitor/index')


# 大屏可视化 - 社区中心
# Web_PO.opnLabel(varUrl + 'largeScreen/community')

