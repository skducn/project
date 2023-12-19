# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2023-12-19
# Description: 公卫
# *****************************************************************


from GwPO import *
Gw_PO = GwPO()


# 1，登录
Gw_PO.login('http://192.168.0.203:30080/#/login', 'admin', 'zy@123456')

# 2.1 获取一级菜单字典
d_menu1 = Gw_PO.menu1()
# print(d_menu1)  # {'首页': 1, '基本公卫': 2, '三高共管六病同防': 3, '系统配置': 4, '社区管理': 5, '报表': 6, '更多菜单': 7}

# # 2.2 获取二级菜单字典
d_menu2 = Gw_PO.menu2(d_menu1, '基本公卫')
# # print(d_menu2)  # {'健康档案管理': 1, '儿童健康管理': 2, '孕产妇管理': 3, '老年人健康管理': 4, '肺结核患者管理': 5, '残疾人健康管理': 6, '严重精神障碍健康管理': 7, '健康教育': 8, '高血压管理': 9, '糖尿病管理': 10, '首页': 11, '基本公卫': 12, '三高共管六病同防': 13, '系统配置': 14, '社区管理': 15, '报表': 16, '更多菜单': 17}
#
# # # 2.3, 进入三级菜单
# Gw_PO.menu3(d_menu2, "高血压管理", "高血压随访")
# Web_PO.setTextById("name", "金浩")
# Web_PO.clk("//button[@type='button']", 1)
#
Gw_PO.menu3(d_menu2, "高血压管理", "高血压专项")
# 姓名
Web_PO.setTextById("name", "令狐冲")
# 身份证号
Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[1]/div[2]/div/div/div/input', "310101198004110014")
# 上次随访日期
Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[1]/div[3]/div/div/div[1]/input', '2023-12-12')
Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[1]/div[3]/div/div/div[2]/input', '2023-12-13')
# 高血压危险分层
Web_PO.jsReadonly('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[2]/div[4]/div/div/div/div/div/input')
Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[2]/div[4]/div/div/div/div/div/input', '高危险')
# 是否终止管理
Web_PO.jsReadonly('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[1]/div/div/div/div/div/input')
Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[1]/div/div/div/div/div/input', '否')
# 随访提醒分类
Web_PO.jsReadonly('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[4]/div/div/div/div/div/input')
Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[4]/div/div/div/div/div/input','常规管理')
Web_PO.clk("//button[@type='button']", 1)
# 查询
Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[5]/div/button[1]', 1)
# 导出
Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[5]/div/button[2]', 1)

#
# Gw_PO.menu3(d_menu2, "糖尿病管理", "糖尿病报病")
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div/div[1]/div/div/div/input', 'yoyo')  # 姓名
# Web_PO.clk("//button[@type='button']", 1)


# d_menu2 = Gw_PO.menu2(d_menu1, '系统配置')
# Gw_PO.menu3(d_menu2, "机构管理", "医院维护")
# 1, 新增医疗机构
# Gw_PO.newMedicalInstitution('lhc的诊所', '12345678', '555555', '三级', '令狐冲', '浦东南路1000号', '13816109050', '上海知名急救诊所\n专治疑难杂病')

# 2, 编辑医疗机构
# Gw_PO.editMedicalInstitution('lhc的诊所', 'lhc的诊所1', '123456781', '5555551', '二级', '令狐冲1', '浦东南路1000号1', '13816109051', '上海知名急救诊所\n专治疑难杂病1')

# 3，科室维护
# Gw_PO.editOffice('lhc的诊所1', {'儿科': '122233', '妇科': '665544', '骨科': '565656'})

# d_menu2 = Gw_PO.menu2(d_menu1, '系统配置')
# Gw_PO.menu3(d_menu2, "用户管理", "用户维护")


