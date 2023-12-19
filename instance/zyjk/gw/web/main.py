# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2023-12-19
# Description: 公卫
# *****************************************************************
from PO.SysPO import *
Sys_PO = SysPO()

from GwPO import *
Gw_PO = GwPO()

# a = '高血压管理\n高血压专项\n高血压随访\n高血压报病'
# a = a.split("\n")
# print(a)
# l_menu1 = ['首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单', '', '', '', '', '', '', '']
# l_menu1 = [i for i in l_menu1 if i != '']
# print(l_menu1)
#
# d_menu1 = (dict(enumerate(l_menu1, start=1)))
# d_menu1 = {v: k for k, v in d_menu1.items()}
# print(d_menu1)
#
# sys.exit(0)


# 1，登录
Gw_PO.login('http://192.168.0.203:30080/#/login', 'admin', 'zy@123456')

# 2.1 获取一级菜单字典
d_menu1 = Gw_PO.menu1()
# print(d_menu1)  # {'首页': 1, '基本公卫': 2, '三高共管六病同防': 3, '系统配置': 4, '社区管理': 5, '报表': 6, '更多菜单': 7}

# # 2.2 获取二级菜单字典
# d_menu2 = Gw_PO.menu2(d_menu1, '基本公卫')
# # print(d_menu2)  # {'健康档案管理': 1, '儿童健康管理': 2, '孕产妇管理': 3, '老年人健康管理': 4, '肺结核患者管理': 5, '残疾人健康管理': 6, '严重精神障碍健康管理': 7, '健康教育': 8, '高血压管理': 9, '糖尿病管理': 10, '首页': 11, '基本公卫': 12, '三高共管六病同防': 13, '系统配置': 14, '社区管理': 15, '报表': 16, '更多菜单': 17}
#
# # # 2.3, 进入三级菜单
# Gw_PO.menu3(d_menu2, "高血压管理", "高血压随访")
# Web_PO.setTextById("name", "金浩")
# Web_PO.clk("//button[@type='button']", 1)
#
# Gw_PO.menu3(d_menu2, "高血压管理", "高血压专项")
# Web_PO.setTextById("name", "令狐冲")
# Web_PO.clk("//button[@type='button']", 1)
#
# Gw_PO.menu3(d_menu2, "糖尿病管理", "糖尿病报病")
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div/div[1]/div/div/div/input', 'yoyo')  # 姓名
# Web_PO.clk("//button[@type='button']", 1)


d_menu2 = Gw_PO.menu2(d_menu1, '系统配置')
Gw_PO.menu3(d_menu2, "机构管理", "医院维护")
# 1, 新增医疗机构
# Gw_PO.newMedicalInstitution('lhc的诊所', '12345678', '555555', '三级', '令狐冲', '浦东南路1000号', '13816109050', '上海知名急救诊所\n专治疑难杂病')

# 2, 编辑医疗机构
# Gw_PO.editMedicalInstitution('lhc的诊所', 'lhc的诊所1', '123456781', '5555551', '二级', '令狐冲1', '浦东南路1000号1', '13816109051', '上海知名急救诊所\n专治疑难杂病1')

# 3，科室维护
Gw_PO.editOffice('lhc的诊所1', {'儿科': '122233', '妇科': '665544', '骨科': '565656'})

# d_menu2 = Gw_PO.menu2(d_menu1, '系统配置')
# Gw_PO.menu3(d_menu2, "用户管理", "用户维护")





#
# # 首页，居民健康档案
# Base_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]', 1)  # 点击首页居民健康档案
# Base_PO.clickXpath('//*[@id="app"]/div/div[1]/div/div[1]/div/ul/div[2]/li', 1)  # 选择居民健康档案菜单
# Base_PO.clickXpath('//*[@id="app"]/div/div[1]/div/div[1]/div/ul/div[2]/li/ul/div[1]/a', 1)  # 选择个人健康档案菜单
#
# # 个人健康档案列表页，新增
# Base_PO.clickXpath('//*[@id="app"]/div/div[3]/section/div/div/div[1]/div/button[3]', 1)  # 点击新增
# # 身份证号码
# Base_PO.inputXpath('//*[@id="app"]/div/div[3]/section/div/form/div[2]/div[2]/div[1]/div[2]/div/div/div/input', '310101198004110017')
# # 姓名
# Base_PO.inputXpath('//*[@id="app"]/div/div[3]/section/div/form/div[2]/div[3]/div[1]/div[2]/div/div/div[1]/input', "张三")
# # 性别
# Base_PO.clickXpath('//*[@id="app"]/div/div[3]/section/div/form/div[2]/div[3]/div[2]/div[2]/div/div/div/div/div/input', 1)
# Base_PO.clickXpath('/html/body/div[2]/div[4]/div/div/div[1]/ul/li[2]', 1)  # 男
# # 户籍地址
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[4]/div[1]/div[2]/div/div/div/div/div/input', 1)  # 户籍地址（省）
# Base_PO.clickXpath('/html/body/div[2]/div[7]/div/div/div[1]/ul/li[2]', 1)  # 河北省
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[4]/div[2]/div[1]/div/div/div[1]/div/div/input', 1)  # 户籍地址（市）
# Base_PO.clickXpath('/html/body/div[2]/div[8]/div/div/div[1]/ul/li[2]', 1)  # 秦皇岛市
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[4]/div[2]/div[2]/div/div/div[1]/div/div/input', 1)  # 户籍地址（区）
# Base_PO.clickXpath('/html/body/div[2]/div[9]/div/div/div[1]/ul/li[2]', 1)  # 北戴河新区
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[4]/div[3]/div[1]/div/div/div[1]/div/div/input', 1)  # 户籍地址（镇）
# Base_PO.clickXpath('/html/body/div[2]/div[10]/div/div/div[1]/ul/li[2]', 1)  # 团林管理处
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[4]/div[3]/div[2]/div/div/div[1]/div/div/input', 1)  # 户籍地址（村民会员会）
# Base_PO.clickXpath('/html/body/div[2]/div[11]/div/div/div[1]/ul/li[2]', 1)  # 赤洋口一寸委会
# # 现住址
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[5]/div[1]/div[2]/div/div/div/div/div/input', 1)  # 现住址（省）
# Base_PO.clickXpath('/html/body/div[2]/div[12]/div/div/div[1]/ul/li[2]', 1)  # 省
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[5]/div[2]/div[1]/div/div/div[1]/div/div/input', 1)  # 现住址（市）
# Base_PO.clickXpath('/html/body/div[2]/div[13]/div/div/div[1]/ul/li[2]', 1)  # 市
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[5]/div[2]/div[2]/div/div/div[1]/div/div/input', 1)  # 现住址（区）
# Base_PO.clickXpath('/html/body/div[2]/div[14]/div/div/div[1]/ul/li[2]', 1)  # 区
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[5]/div[3]/div[1]/div/div/div[1]/div/div/input', 1)  # 现住址（镇）
# Base_PO.clickXpath('/html/body/div[2]/div[15]/div/div/div[1]/ul/li[2]', 1)  # 镇
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[5]/div[3]/div[2]/div/div/div[1]/div/div/input', 1)  # 现住址（街道社区）
# Base_PO.clickXpath('/html/body/div[2]/div[16]/div/div/div[1]/ul/li[2]', 1)  # 街道社区
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[5]/div[4]/div[2]/div/div/div[1]/input', "上海浦东新区南京路100号")  # 手工填写户籍地址
# # Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[5]/div[4]/div[3]/div/div/label/span[1]', 2)  # 勾选 同户籍地址
# # 本人电话
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[6]/div[1]/div[2]/div/div/div/input', '13816109022')
# # 联系人姓名
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[6]/div[2]/div[2]/div/div/div/input', '张三')
# # 联系人电话
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[6]/div[3]/div[2]/div/div/div[1]/input', '56776767')
# # 常住类型
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[6]/div[4]/div[2]/div/div/div[1]/label', 1)
# # 文化程度
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[7]/div[1]/div[2]/div/div/div/div/div/input', 1)
# Base_PO.clickXpath('/html/body/div[2]/div[17]/div/div/div[1]/ul/li[2]', 1)  # 大学本科
# # 职业
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[7]/div[2]/div[2]/div/div/div/div/div/input', 1)
# Base_PO.clickXpath('/html/body/div[2]/div[18]/div/div/div[1]/ul/li[2]', 1) # 专业技术人员
# # 工作单位
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[7]/div[3]/div[2]/div/div/div[1]/input', '上海智赢')
# # 婚姻状态
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[8]/div[1]/div[2]/div/div/div/div/div/input', 1)
# Base_PO.clickXpath('/html/body/div[2]/div[19]/div/div/div[1]/ul/li[2]', 1)  # 已婚
# # 血型
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[8]/div[2]/div[2]/div/div/div[2]/label', 1)  # B
# # Rh血型
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[8]/div[3]/div[2]/div/div/div[2]/label', 1)  # Rh阳性
# # 医疗费用支付方式
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[1]/div[1]/div/div/div/label', 1)  # 勾选 城镇或省直职工基本医疗保险
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/input', '1234567')  # 填写医保卡号
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/label', 1)  # 勾选 城镇居民基本医疗保险
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[1]/div[3]/div/div/div/div/input', '0000000')  # 填写医保卡号
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/label', 1)  # 勾选 贫困救助
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[1]/div[4]/div[2]/div/div/div/input', 'A99999999')  # 填写卡号
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[3]/label', 1)  # 新型农村合作医疗
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[5]/label', 1)  # 商业医疗保险
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[6]/label', 1)  # 全公费
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[7]/label', 1)  # 全自费
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[8]/label', 1)  # 城乡居民医疗保险
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[9]/label', 1)  # 其他
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[9]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/input', '医疗付费说明')  # 其他情况说明
# 药物过敏史
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[10]/div[1]/div[2]/div/div/div[1]/div[1]/label', 1)  # 无
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[10]/div[1]/div[2]/div/div/div/div[2]/label', 1)  # 药物
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[10]/div[1]/div[2]/div/div/div/div[3]/label', 1)  # 青霉素类抗生素
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[10]/div[1]/div[2]/div/div/div/div[4]/label', 1)  # 磺胺类抗生素
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[10]/div[1]/div[2]/div/div/div/div[5]/label', 1)  # 头孢类抗生素
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[10]/div[1]/div[2]/div/div/div/div[6]/label', 1)  # 含碘药品
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[10]/div[1]/div[2]/div/div/div/div[7]/label', 1)  # 酒精
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[10]/div[1]/div[2]/div/div/div/div[8]/label', 1)  # 镇静麻醉剂
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[10]/div[1]/div[2]/div/div/div/div[9]/label', 1)  # 链霉素类抗生素
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[10]/div[1]/div[2]/div/div/div/div[10]/label', 1)  # 其他药物过敏原
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[10]/div[2]/div/div/div/div/textarea', '药物过敏史说明\ntest')  # 其他情况说明
# 暴露史
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[11]/div/div[2]/div/div/div/div[1]/label', 1)  # 无
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[11]/div/div[2]/div/div/div/div[2]/label', 1)  # 化学品
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[11]/div/div[2]/div/div/div/div[3]/label', 1)  # 毒物
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[11]/div/div[2]/div/div/div/div[4]/label', 1)  # 射线
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[11]/div/div[2]/div/div/div/div[5]/label', 1)  # 不详
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[11]/div/div[2]/div/div/div/div[6]/label', 1)  # 其他
# # 既往史
# # 既往史 - 疾病
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[1]/div[1]/div[2]/div/div/div/label[2]', 1)  # 无
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[1]/div[1]/div[2]/div/div/div/label[1]', 1)  # 有
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div/div/div/div/input', 1)  # 疾病名称
# Base_PO.clickXpath('/html/body/div[2]/div[20]/div/div/div[1]/ul/li[2]', 1)  # 高血压
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div/div/div/input', "2023-07-12")  # 确诊时间
# # 既往史 - 疾病 - +
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[1]/div[1]/div[2]/div/div/i', 1)  # 点击 +
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div/input', 1)  # # 疾病名称
# Base_PO.clickXpath('/html/body/div[2]/div[30]/div/div/div[1]/ul/li[3]', 1)  # 糖尿病
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/div/input', "2023-07-14")  # 确诊时间
# # 既往史 - 手术
# # Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[2]/div[1]/div[2]/div/div/div/label[2]', 1)  # 无
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[2]/div[1]/div[2]/div/div/div/label[1]', 1)  # 有
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div/div/input', "第一场")  # 手术名称
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div/div/input', "2023-07-14")  # 手术时间
# # 既往史 - 手术 - +
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[2]/div[1]/div[2]/div/div/i', 1)  # 点击 +
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/div/input', "第二场")  # 手术名称
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div/input', "2023-07-14")  # 手术时间
# # 外伤
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[3]/div[1]/div[2]/div/div/div/label[2]', 1)  # 无
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[3]/div[1]/div[2]/div/div/div/label[1]', 1)  # 有
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[3]/div[2]/div/div[1]/div[2]/div/div/div/input', '脑外伤')  # 外伤名称
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[3]/div[2]/div/div[2]/div[1]/div/div/div/input', '2023-12-02')  # 外伤时间
# # 既往史 - 外伤 - +
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[3]/div[1]/div[2]/div/div/i', 1)  # +
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[3]/div[2]/div[2]/div[1]/div[2]/div/div/div/input', '大腿外伤')  # 外伤名称
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div/div/input', '2022-12-05')  # 外伤名称
# # 输血
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[4]/div[1]/div[2]/div/div/div/label[2]', 1)  # 无
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[4]/div[1]/div[2]/div/div/div/label[1]', 1)  # 有
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[4]/div[2]/div/div[1]/div[2]/div/div/div/input', '大量流血')  # 输血原因
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[4]/div[2]/div/div[2]/div[1]/div/div/div/input', '2022-12-06')  # 输血时间
# # 既往史 - 输血 - +
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[4]/div[1]/div[2]/div/div/i', 1)  # +
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[4]/div[2]/div[2]/div[1]/div[2]/div/div/div/input', '血量不够用')  # 输血原因
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[12]/div[2]/div[4]/div[2]/div[2]/div[2]/div[1]/div/div/div/input', '2023-02-12')  # 输血时间

# 家族史
# 家族史 - 父亲
# # Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div/div[1]/label', 1) # 无
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[2]/label', 1)  # 高血压
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[3]/label', 1)  # 糖尿病
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[4]/label', 1)  # 冠心病
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[5]/label', 1)  # 慢性组晒性肺疾病
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[6]/label', 1)  # 恶性肿瘤
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[7]/label', 1)  # 脑卒中
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[8]/label', 1)  # 重性精神疾病
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[9]/label', 1)  # 结核病
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[10]/label', 1)  # 肝脏疾病
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[11]/label', 1)  # 先天畸形
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[12]/label', 1)  # 职业病
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[13]/label', 1)  # 肾脏疾病
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[14]/label', 1)  # 贫血
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[15]/label', 1)  # 其他法定传染病
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[16]/label', 1)  # 其他
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div/input', '不知道')  # 其他原因
# # 家族史 - 母亲
# # Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[1]/label', 1)  # 无
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[3]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[4]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[5]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[6]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[7]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[8]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[9]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[10]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[11]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[12]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[13]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[14]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[15]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div/div[16]/label', 1)
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/input', '不知道111')  # 其他原因
# # 家族史 - 兄弟姐妹
# # Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[1]/label', 1)  # 无
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[2]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[3]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[4]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[5]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[6]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[7]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[8]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[9]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[10]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[11]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[12]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[13]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[14]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[15]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div/div[16]/label', 1)
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[3]/div/div[2]/div/div/div[2]/div/div/input', '不知道222')
# # 家族史 - 子女
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[1]/div/div/div/div/div/span/span/i', 1)  # 子女
# Base_PO.clickXpath('/html/body/div[2]/div[25]/div/div/div[1]/ul/li[1]') # 儿子
# # Base_PO.clickXpath('/html/body/div[2]/div[25]/div/div/div[1]/ul/li[2]') # 女儿
# # Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[1]/label', 1) # 无
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[2]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[3]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[4]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[5]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[6]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[7]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[8]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[9]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[10]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[11]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[12]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[13]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[14]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[15]/label', 1)
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div/div[16]/label', 1)
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[13]/div[2]/div[4]/div/div[2]/div/div/div[2]/div/div/input', '不知道333')

# 遗传病史
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[14]/div[1]/div[2]/div/div/label[1]', 1)  # 无
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[14]/div[1]/div[2]/div/div/label[2]', 1)  # 有
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[14]/div[2]/div[2]/div/div/div/input', '爱斯基摩血透') # 疾病名称
# # 残疾情况
# # Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[15]/div/div[2]/div/div/div/div/div[1]/label', 1)  # 无残疾
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[15]/div/div[2]/div/div/div/div/div[2]/label', 1)  # 视力残疾
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[15]/div/div[2]/div/div/div/div/div[3]/label', 1)  # 听力残疾
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[15]/div/div[2]/div/div/div/div/div[4]/label', 1)  # 言语残疾
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[15]/div/div[2]/div/div/div/div/div[5]/label', 1)  # 肢体残疾
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[15]/div/div[2]/div/div/div/div/div[6]/label', 1)  # 智力残疾
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[15]/div/div[2]/div/div/div/div/div[7]/label', 1)  # 精神残疾
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[15]/div/div[2]/div/div/div/div/div[8]/label', 1)  # 其他残疾
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[15]/div/div[2]/div/div/div/div[2]/div/div/input', '浑身都是疾病')
# # 家庭情况
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[16]/div[2]/div[1]/div[1]/div[2]/div/div/div/div/div/input', 1)  # 与户主关系
# Base_PO.clickXpath('/html/body/div[2]/div[26]/div/div/div[1]/ul/li[2]', 1)
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[16]/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/input', '金金')  # 户主姓名
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[16]/div[2]/div[1]/div[3]/div[2]/div/div/div[1]/input', '310101198004110014')  # 户主身份证号
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[16]/div[2]/div[1]/div[4]/div[2]/div/div/div/input','3')  # 家庭人口数
# Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[16]/div[2]/div[2]/div[1]/div[2]/div/div/div/input', '家庭结构不复杂')  # 家庭结构
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[16]/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/label', 1)  # 居住情况
# # 生活环境
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[17]/div[2]/div[1]/div/div[2]/div/div/div[2]/label', 1)  # 厨房排风设施
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[17]/div[2]/div[2]/div/div[2]/div/div/div[2]/label', 1)  # 燃料类型
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[17]/div[2]/div[3]/div/div[2]/div/div/div[2]/label', 1)  # 饮水
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[17]/div[2]/div[4]/div/div[2]/div/div/div[2]/label', 1)  # 厕所
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[17]/div[2]/div[5]/div/div[2]/div/div/div[2]/label', 1)  # 禽畜栏
# # 是否高危人群
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[18]/div/div[2]/div/div/div/label[1]') # 是
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[18]/div/div[2]/div/div/div/label[2]') # 否
# # 家庭团队
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[20]/div[1]/div[2]/div/div/div/div/div/input', 1)
# Base_PO.clickXpath('/html/body/div[2]/div[27]/div/div/div[1]')
# # 责任医生
# Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[20]/div[2]/div[2]/div/div/div/div/div/input', 1)
# Base_PO.clickXpath('/html/body/div[2]/div[28]/div', 1)
# # 建档日期
# Base_PO.inputXpathClear('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[20]/div[3]/div[2]/div/div/div/input','2023-12-12'
#                    )
#
#
# sys.exit(0)
#
#
# # 查询后更新记录
# Base_PO.clickXpath('//*[@id="app"]/div/div[3]/section/div/div/div[2]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[13]/div/div[2]', 2)
# Base_PO.inputXpathClear('//*[@id="app"]/div/div[3]/section/div/form/div[2]/div[3]/div[1]/div[2]/div/div/div/input', "小郭55")
# print("333")
#
# # 随访方式
# Base_PO.clickXpath('//*[@id="app"]/div/div[3]/section/div/form/div[3]/div[2]/div[2]/div[2]/div/div/div[1]/label[2]/span[1]/span', 2)
# Base_PO.inputXpath('//*[@id="app"]/div/div[3]/section/div/form/div[3]/div[3]/div[2]/div/div/div[1]/input', "1111")
# Base_PO.inputXpath('//*[@id="symptom"]/div/div/div/input', "2023-12-12")
# print("444")
#
# Base_PO.clickXpath('//*[@id="app"]/div/div[3]/section/div/div[1]/button[1]', 2)
# # 二次确认
# Base_PO.clickXpath('//*[@id="app"]/div/div[3]/section/div/div[2]/div/div/div[3]/span/button[1]', 2)
# print("5555")



# from PO.BasePO import *
# from PO.WebPO import *
# Web_PO = WebPO("chrome")
# Web_PO.openURL('http://192.168.0.203:30080')
# # # Web_PO.driver.maximize_window()  # 全屏
# # #
# Web_PO.inputXpath("//input[@placeholder='请输入用户名']", "jinhao")
# # Web_PO.inputXpath("//input[@placeholder='输入密码']", "Jinhao123")
# # Web_PO.inputXpath("//input[@placeholder='输入图形验证码']", "Jinhao123")
# # Web_PO.clickXpath("//button[@type='button']", 2)  # 登录
#
# # Web_PO.openURL('http://192.168.0.203:30080/workbench')


# Saas_PO.login("016", "123456")
#
# # # 1，元素库
# Saas_PO.clickMenuAll("随访", "元素库")
#
# def validateRule(varRule):
#     Saas_PO.Web_PO.clickId("tab-validationRules0", 2)  # 1验证规则
#     list1 = Saas_PO.Web_PO.getXpathsText("//span")
#     list1 = List_PO.listIntercept(list1, "保存并新增", 1)
#     list1 = List_PO.listDel(list1, "")
#     # print(list1)
#     for i in range(len(varRule)):
#         for j in range(len(list1)):
#             if list1[j] == varRule[i]:
#                 Saas_PO.Web_PO.clickXpath('//div[@id="pane-validationRules0"]/div/div[1]/div[1]/div[1]/div[' + str(j+1) + ']/div[1]/div/label', 2)
#                 Saas_PO.Web_PO.clickXpath('//div[@id="pane-validationRules0"]/div/div[1]/div[1]/div[1]/div[' + str(j+1) + ']/div[1]/div', 2)
#                 break
#
# validateRule(["数字范围","正则校验"])
#
#
# # Saas_PO.Web_PO.clickId("tab-attribute", 2)  # 组件属性
# # Saas_PO.Web_PO.inputXpathClear("//input[@placeholder='最大宽度24格']", 12)
# # Saas_PO.Web_PO.clickXpath('//*[@id="pane-attribute"]/form/div[1]/div/div[6]/div[2]/div/div/span')
#

