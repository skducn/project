# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-3-2
# Description: 电子健康档案数据监控中心（PC端）之 系统管理 - 用户管理
# 技巧：去掉字符串两端的数字， astring.strip(string.digits) ,如 123姓名，输出：姓名
# 扩展：astring.lstrip(string.digits) 去掉左侧数字  , astring.rstrip(string.digits) 去掉右侧数字
# C4 ？开发bug，编辑后会刷新页面导致提示2次（成功及无数据），用户体验不好，自动化会报错，找不到数据。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()
from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()
from PO.StrPO import *
Str_PO = StrPO()

varNewUser = "auto1"
varNewNickName = "令狐冲1"
varNewPhone = "13816109050"

# 1，登录
# dataMonitor_PO.login("admin", "admin@123456")  # 管理员
dataMonitor_PO.login("test", "Qa@123456")  # 普通管理员

# 2，用户管理
dataMonitor_PO.clickMenu("系统管理", "用户管理")

# 3，显示用户列表
dataMonitor_PO.sys_userList()

# 3，用户管理 - 搜索
# dataMonitor_PO.sys_user_search("用户名", "ayida123")  # 依据用户名搜索
# dataMonitor_PO.sys_user_search("昵称", "令狐冲")  # 依据昵称搜索
# dataMonitor_PO.sys_user_search("手机", "13816109050")  # 依据收集搜索


# 4，用户管理 - 新增 （搜索定位用户名）
# 用户属性：['家庭医生', '家庭医生助理', '院长', '护士']
dataMonitor_PO.sys_user_add("linghuchong12", "令狐冲", "13816109050", "家庭医生助理")
# dataMonitor_PO.sys_user_add("linghuchong12", "令狐冲", "13816109050", "护士", "北站街道社区卫生服务中心")
#
# 5，用户管理 - 编辑 （搜索定位用户名）
# dataMonitor_PO.sys_user_edit("alibaba1", "阿里巴巴", "13613254658", "院长")
# dataMonitor_PO.sys_user_edit("ayida", "ayida123", "阿依达", "13613250400", "家庭医生")
#
# # 6，用户管理 - 角色(单选/多选)（搜索定位用户名）
# 角色：['社区机构管理员', '家庭医生', 'ai核对管理员', '档案查看管理员', '安全审计员', '测试管理人员']
# dataMonitor_PO.sys_user_role("ayida", "社区机构管理员", "安全审计员", "家庭医生")
# dataMonitor_PO.sys_user_role("ayida123")  # 清空所有角色
#
# # 7，用户管理 - 删除（除了admin其他账号无权限）
# dataMonitor_PO.sys_user_del("alibaba1")

