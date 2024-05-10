# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-25
# Description: 社区健康管理中心
# 测试环境 # http://192.168.0.243:8010/#/login
#***************************************************************

from Chc_web_PO import *
Chc_web_PO = Chc_web_PO()
from bs4 import BeautifulSoup

varUrl = 'http://192.168.0.243:8010/#/'

# 1, 登录
# Chc_web_PO.login(varUrl + 'login', 'admin', 'Zy@123456')
Chc_web_PO.login(varUrl + 'login', 'cs', '12345678')

# 2, 获取首页源码，点击菜单
html_source = Web_PO.getSource()
# print(html_source)

# 获取首页上指标名称与值
Chc_web_PO.getTechnicalTarget(html_source)

# 首页
# Chc_web_PO.clkMenu(html_source, '首页')

# # 居民健康服务
# Chc_web_PO.clkMenu(html_source, '健康服务')
# Chc_web_PO.clkMenu(html_source, '健康评估及干预')
# Chc_web_PO.clkMenu(html_source, '慢病管理')
# Chc_web_PO.clkMenu(html_source, '老年人体检')
# Chc_web_PO.clkMenu(html_source, '重点人群')

# 健康管理门诊
# Chc_web_PO.clkMenu(html_source, '居民登记')
# Chc_web_PO.clkMenu(html_source, '健康评估')

# 用户中心
# Chc_web_PO.clkMenu(html_source, '机构维护')
# Chc_web_PO.clkMenu(html_source, '用户维护')
# Chc_web_PO.clkMenu(html_source, '角色维护')
# Chc_web_PO.clkMenu(html_source, '接口管理')
# Chc_web_PO.clkMenu(html_source, '批量评估')
# Chc_web_PO.clkMenu(html_source, '错误日志')

# 社区配置
# Chc_web_PO.clkMenu(html_source, '常住人口')
# Chc_web_PO.clkMenu(html_source, '家医团队维护')
# Chc_web_PO.clkMenu(html_source, '家医助手')
# Chc_web_PO.clkMenu(html_source, '干预规则配置')
# Chc_web_PO.clkMenu(html_source, '停止评估名单')
# Chc_web_PO.clkMenu(html_source, '社区用户维护')
# Chc_web_PO.clkMenu(html_source, '评估建议')

# 系统监控
# Chc_web_PO.clkMenu(html_source, '定时任务')

# 统计分析
# Chc_web_PO.clkMenu(html_source, '社区健康评估')
# Chc_web_PO.clkMenu(html_source, '全区健康评估')

# 大屏可视化 - 社区中心 (必须放在最后)
# Web_PO.opn(varUrl + "largeScreen/community")
