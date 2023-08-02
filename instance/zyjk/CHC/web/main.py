# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-25
# Description: 社区健康管理中心
#***************************************************************

from PO.SysPO import *
Sys_PO = SysPO()
# Sys_PO.clsApp("Google Chrome")

from ChcPO import *
Chc_PO = ChcPO()


varUrl = 'http://192.168.0.243:8010/#/'

# 1，登录
Chc_PO.login('http://192.168.0.243:8010/#/login', 'admin', 'Zy@123456')

# 签约居民管理 - 健康服务
Web_PO.opn(varUrl + 'SignManage/service')


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

