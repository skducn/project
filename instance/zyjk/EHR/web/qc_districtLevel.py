# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2020-9-30
# Description: EHR 质量管理系统 (质控结果分析 - 区级)
# chrome版本：94.0.4606.81
# webdriver驱动：https://npm.taobao.org/mirrors/chromedriver
# 本地路径：C:\Python39\Scripts
# *****************************************************************

from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()


# 1，登录
dataMonitor_PO.login("test", "Qa@123456")

# 2，菜单
dataMonitor_PO.clickMenu("质控结果分析", "区级")

# 3.1，检查质控数据截止日期，日期不能早于2000.1.5
dataMonitor_PO.checkDate(dataMonitor_PO.getUpdateDate())

# 3.2, 辖区常住人口（人） - 人数、建档率、截止日期
# 1+1+1签约居民人数（人） - 人数、签约率、签约完成率、签约人数、签约机构与档案管理机构不一致人数
# 签约居民分类（重点人群，非重点人群）
czrk, jdl, jzrq, qyjmrs, qyl, qywcl, byzrs, zdrq, fzdrq = dataMonitor_PO.getDistrictLevel()

# sql测试
print("辖区常住人口（人）".center(100, "-"))
sql_czrk = dataMonitor_PO.testSql('select top 1 (select sum(live_people_num) from (select live_people_num,org_name from report_qyyh group by org_code,org_name,live_people_num) a)  livePeopleNum from report_qyyh')
WebPO.assertEqual("",int(czrk), int(sql_czrk), "ok,辖区常住人口（人）", "errorrrrrrrrrr,辖区常住人口（人）")

print("建档率".center(100, "-"))
sql_jdl = dataMonitor_PO.testSql('SELECT count(*) FROM report_qyyh WHERE A4="1"')
x = sql_jdl / sql_czrk * 100
print(str(x) + "%")
WebPO.assertEqual("",int(jdl), int(x), "ok,建档率", "errorrrrrrrrrr,建档率")





print("1+1+1签约居民人数（人）".center(100, "-"))
sql_qyjmrs = dataMonitor_PO.testSql('SELECT count(*) FROM report_qyyh')
WebPO.assertEqual("",int(qyjmrs), int(sql_qyjmrs), "ok,1+1+1签约居民人数（人）", "errorrrrrrrrrr,1+1+1签约居民人数（人）")





# # 3.3，各社区签约居民电子健康档案指标 - 详细
# dataMonitor_PO.openNewLabel("http://192.168.0.243:8082/#/recordService/list?docCode=0041&orgCode=310118001&isDistrict=true")
# l_all = dataMonitor_PO.recordService("医疗机构名称")  # 获取字段与所有值列表
# print(l_all)
# # value = dataMonitor_PO.getRecordServiceValue(l_all, "上海市青浦区练塘镇社区卫生服务中心", "档案更新率(%)")   # 获取某机构的某个字段值。
# # print(value)
#
# l_all = dataMonitor_PO.recordService("签约医生", 4)
# print(l_all)
# # value = dataMonitor_PO.getRecordServiceValue(l_all, "黄*美", "建档率(%)")   # 获取某医生的某个字段值。
# # print(value)





