# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2023-7-14
# Description: 公卫 - 居民将康档案
# *****************************************************************
# #
# from GwPO import *
# Gw_PO = GwPO()
import sys

from PO.BasePO import *


# 登录
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
options = Options()
# options.headless = True  # 无界面模式
options.add_argument("--start-maximized")  # 最大化

s = Service("/Users/linghuchong/miniconda3/envs/py308/bin/chromedriver")
driver = webdriver.Chrome(service=s, options=options)
Base_PO = BasePO(driver)
driver.get('http://192.168.0.203:30080')

# 登录
Base_PO.inputXpath("//input[@placeholder='请输入用户名']", "jinhao")
Base_PO.inputXpath("//input[@placeholder='输入密码']", "Jinhao123")
Base_PO.inputXpath("//input[@placeholder='输入图形验证码']", "111")
Base_PO.clickXpath("//button[@type='button']", 1)


# 首页，居民健康档案
Base_PO.clickXpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]', 1)  # 点击首页居民健康档案
Base_PO.clickXpath('//*[@id="app"]/div/div[1]/div/div[1]/div/ul/div[2]/li', 1)  # 选择居民健康档案菜单
Base_PO.clickXpath('//*[@id="app"]/div/div[1]/div/div[1]/div/ul/div[2]/li/ul/div[1]/a', 1)  # 选择个人健康档案菜单

# 个人健康档案列表页，新增
Base_PO.clickXpath('//*[@id="app"]/div/div[3]/section/div/div/div[1]/div/button[3]', 1)  # 点击新增
# 身份证号码
Base_PO.inputXpath('//*[@id="app"]/div/div[3]/section/div/form/div[2]/div[2]/div[1]/div[2]/div/div/div/input', '310101198004110017')
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
# 家庭情况
Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[16]/div[2]/div[1]/div[1]/div[2]/div/div/div/div/div/input', 1)  # 与户主关系
Base_PO.clickXpath('/html/body/div[2]/div[26]/div/div/div[1]/ul/li[2]', 1)
Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[16]/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/input', '金金')  # 户主姓名
Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[16]/div[2]/div[1]/div[3]/div[2]/div/div/div[1]/input', '310101198004110014')  # 户主身份证号
Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[16]/div[2]/div[1]/div[4]/div[2]/div/div/div/input','3')  # 家庭人口数
Base_PO.inputXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[16]/div[2]/div[2]/div[1]/div[2]/div/div/div/input', '家庭结构不复杂')  # 家庭结构
Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[16]/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/label', 1)  # 居住情况
# 生活环境
Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[17]/div[2]/div[1]/div/div[2]/div/div/div[2]/label', 1)  # 厨房排风设施
Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[17]/div[2]/div[2]/div/div[2]/div/div/div[2]/label', 1)  # 燃料类型
Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[17]/div[2]/div[3]/div/div[2]/div/div/div[2]/label', 1)  # 饮水
Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[17]/div[2]/div[4]/div/div[2]/div/div/div[2]/label', 1)  # 厕所
Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[17]/div[2]/div[5]/div/div[2]/div/div/div[2]/label', 1)  # 禽畜栏
# 是否高危人群
Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[18]/div/div[2]/div/div/div/label[1]') # 是
Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[18]/div/div[2]/div/div/div/label[2]') # 否
# 家庭团队
Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[20]/div[1]/div[2]/div/div/div/div/div/input', 1)
Base_PO.clickXpath('/html/body/div[2]/div[27]/div/div/div[1]')
# 责任医生
Base_PO.clickXpath('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[20]/div[2]/div[2]/div/div/div/div/div/input', 1)
Base_PO.clickXpath('/html/body/div[2]/div[28]/div', 1)
# 建档日期
Base_PO.inputXpathClear('/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[20]/div[3]/div[2]/div/div/div/input','2023-12-12'
                   )


sys.exit(0)


# 查询后更新记录
Base_PO.clickXpath('//*[@id="app"]/div/div[3]/section/div/div/div[2]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[13]/div/div[2]', 2)
Base_PO.inputXpathClear('//*[@id="app"]/div/div[3]/section/div/form/div[2]/div[3]/div[1]/div[2]/div/div/div/input', "小郭55")
print("333")

# 随访方式
Base_PO.clickXpath('//*[@id="app"]/div/div[3]/section/div/form/div[3]/div[2]/div[2]/div[2]/div/div/div[1]/label[2]/span[1]/span', 2)
Base_PO.inputXpath('//*[@id="app"]/div/div[3]/section/div/form/div[3]/div[3]/div[2]/div/div/div[1]/input', "1111")
Base_PO.inputXpath('//*[@id="symptom"]/div/div/div/input', "2023-12-12")
print("444")

Base_PO.clickXpath('//*[@id="app"]/div/div[3]/section/div/div[1]/button[1]', 2)
# 二次确认
Base_PO.clickXpath('//*[@id="app"]/div/div[3]/section/div/div[2]/div/div/div[3]/span/button[1]', 2)
print("5555")



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

