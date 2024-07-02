# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2023-12-19
# Description: 公卫
# *****************************************************************


from GwPO import *
Gw_PO = GwPO()

from PO.ListPO import *
List_PO = ListPO()

# 1，登录
Gw_PO.login('http://192.168.0.203:30080/#/login', 'testwjw', 'Qa@123456')
# # # 获取登录后的解密数据
# d = Gw_PO.getDecode('account', '40d73255e78d004d12327ffed970f0a51f33e4cc0016512aa422fe7278d4cf38cb458af261b2314944a1f421299d27b2bc16193b918c3d570e68250e186990892c403ee267a7700f7f02fbcc19439ae6ae7209f0257555ba11a5906f52f9b00972bf8461fdb723a880a2771b8c9732ab7ec6ba97d4d50ae1ae3e070676e417c39876e15ad54a7c13383ce7e0d902e3cc69efd63b5e4d82ed5baa9f028e3e812e3a')
# print(d)  # {'account': {'username': 'testwjw', 'password': 'Qa@123456', 'code': '', 'uuid': ''}}
# print(d['account']['password'])  # Qa@123456


# 2, 基本公卫菜单连接(登录后点击)
Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[2]", 2)
d_menu2Url = Gw_PO.getMenu2Url()
print('基本公卫 => ', d_menu2Url)


# todo 2.1, 健康档案概况 (基本公卫)
# Web_PO.opnLabel(d_menu2Url['健康档案概况'])
# Web_PO.swhLabel(1)
# # 2.1.1, 请选择
# # Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[1]/div/div/input", 2)
# # Web_PO.clkByX("/html/body/div[2]/div[2]/div/div/div[1]/ul/li/label", 2)
# # Web_PO.clkByX("/html/body/div[2]/div[2]/div/div[2]/div[1]/ul/li[3]/label", 2)
# # Web_PO.clkByX("/html/body/div[2]/div[2]/div/div[3]/div[1]/ul/li/label", 2)
# # Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[1]", 2)
# Web_PO.cls()
# Web_PO.swhLabel(0)

# todo 2.2, 个人健康档案 (基本公卫)
# Web_PO.opnLabel(d_menu2Url['个人健康档案'])
# Web_PO.swhLabel(1)
# # 2.2.1, 查询（通过身份证查找唯一记录）
# Gw_PO.personalHealthRecord('110101196001193209')
# # 已建专项
# Gw_PO.yjzx('高血压专项','专项登记')
# # Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]", 2)  # 随访记录
# # # 高血压随访记录
# # l_div = Web_PO.getTextListByX("//td/div")
# # l_div = List_PO.dels(l_div, '')
# # l_div = List_PO.dels(l_div, '详情\n编辑\n删除')
# # print(l_div) # ['刘斌龙卫健委', '111 mmHg', '11 mmHg', '门诊', '2024-06-26', '控制满意', '2024-09-24', '公卫随访']
# Gw_PO.yjzx('糖尿病专项','专项登记')
# # Gw_PO.yjzx('高血脂专项','专项登记')


# todo 2.3, 家庭健康档案 (基本公卫)
# Web_PO.opnLabel(d_menu2Url['家庭健康档案'])
# Web_PO.swhLabel(1)
# # 获取列表中用户的居民健康档案
# # Gw_PO.runUser('all')
# Gw_PO.runUser('测试')
# # Gw_PO.runUser('黎明', '测试')


# Web_PO.opnLabel(d_menu2Url['死亡管理'])
# Web_PO.swhLabel(1)
# 死亡管理 - 孙竹华
# Gw_PO.residentHealthRecord_update('孙竹华', 'http://192.168.0.203:30080/#/phs/personalAddOrUpdate/healthDetail?id=132')

# # 肺结核专项 （基本公卫 - 家庭健康档案 - 领跑）
# Gw_PO.phthisisVisit('零跑',"http://192.168.0.203:30080/#/phs/Tuberculosis/tuberculosisTableForm?id=148&isNav=true")
# Gw_PO.phthisisVisit('零跑', "http://192.168.0.203:30080/#/phs/Tuberculosis/firstVisit?id=148&idCard=110117199001013970&page=1&isNav=1")  # 其他错误

# 已建肺结核专项(正确)
# Gw_PO.phthisisVisit('零跑', "http://192.168.0.203:30080/#/phs/Tuberculosis/firstVisit?id=148&idCard=110117199001013970&page=1&isNav=1")

# 严重精神障碍患者个人信息补充表
Gw_PO.hypophrenia('陈平安', "http://192.168.0.203:30080/#/phs/MentalDisorder/FollowUpRecord?ehrId=111&ehrNum=37068500100200002")

# span = Web_PO.getTextListByX("//label/span")
# print(span)

# Web_PO.cls()
# Web_PO.swhLabel(0)




# # 三高共管菜单连接
# Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/ul/li[3]", 2)
# d_menu2Url = Gw_PO.getMenu2Url()
# print(d_menu2Url)
#
# # 家医签约菜单连接
# Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/ul/li[4]", 2)
# d_menu2Url = Gw_PO.getMenu2Url()
# print(d_menu2Url)
#
# # 统计报表菜单连接
# Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/ul/li[5]", 2)
# d_menu2Url = Gw_PO.getMenu2Url()
# print(d_menu2Url)
#
# # 系统配置菜单连接
# Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/ul/li[6]", 2)
# d_menu2Url = Gw_PO.getMenu2Url()
# print(d_menu2Url)

# # 数据维护菜单连接
# Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/ul/li[7]", 2)
# d_menu2Url = Gw_PO.getMenu2Url()
# print(d_menu2Url)





# # 2.1 点击一级菜单
# Gw_PO.menu1('首页')
# Gw_PO.menu1('基本公卫')
# Gw_PO.menu1('三高共管')
# Gw_PO.menu1('家庭签约')
# Gw_PO.menu1('统计报表')
# Gw_PO.menu1('系统配置')
# Gw_PO.menu1('系统配置')


#
# # # 2.2 获取二级菜单字典
# d_menu2 = Gw_PO.menu2(d_menu1, '基本公卫')
# print(d_menu2)  # {'健康档案管理': 1, '儿童健康管理': 2, '孕产妇管理': 3, '老年人健康管理': 4, '肺结核患者管理': 5, '残疾人健康管理': 6, '严重精神障碍健康管理': 7, '健康教育': 8, '高血压管理': 9, '糖尿病管理': 10, '首页': 11, '基本公卫': 12, '三高共管六病同防': 13, '系统配置': 14, '社区管理': 15, '报表': 16, '更多菜单': 17}
# #
# # # # 2.3, 进入三级菜单
# # Gw_PO.menu3(d_menu2, "高血压管理", "高血压随访")
# # Web_PO.setTextById("name", "金浩")
# # Web_PO.clk("//button[@type='button']", 1)
# #
# Gw_PO.menu3(d_menu2, "高血压管理", "高血压专项")
# # 姓名
# Web_PO.setTextById("name", "令狐冲")
# # 身份证号
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[1]/div[2]/div/div/div/input', "310101198004110014")
# # 上次随访日期
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[1]/div[3]/div/div/div[1]/input', '2023-12-12')
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[1]/div[3]/div/div/div[2]/input', '2023-12-13')
# # 高血压危险分层
# Web_PO.jsReadonly('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[2]/div[4]/div/div/div/div/div/input')
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[2]/div[4]/div/div/div/div/div/input', '高危险')
# # 是否终止管理
# Web_PO.jsReadonly('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[1]/div/div/div/div/div/input')
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[1]/div/div/div/div/div/input', '否')
# # 随访提醒分类
# Web_PO.jsReadonly('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[4]/div/div/div/div/div/input')
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[4]/div/div/div/div/div/input','常规管理')
# Web_PO.clk("//button[@type='button']", 1)
# # 查询
# Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[5]/div/button[1]', 1)
# # 导出
# Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[5]/div/button[2]', 1)

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


