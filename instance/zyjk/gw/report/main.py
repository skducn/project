# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-7-30
# Description: 公卫报表主程序
# http://192.168.0.203:30080/#/report/Statistics/report7
# sj,12345678 （三级管理员）
# 统计报表 - 严重精神障碍患者健康管理报表
#***************************************************************
from GwIndexPO import *

# todo 1 初始化数据参数
# p = {'org_name': '道头卫生院', 'year': '2024', 'method': 'GET', 'path': '/serverExport/report/getSmiBi?0=', 'res':'registered'}
# # 获取二级医院机构
# l_d2 = Sqlserver_PO1.select("select org_code, org_name from sys_hospital")
# # print(l_d)  # [{'org_code': '370685004', 'org_name': '金岭镇卫生院'}, {'org_code': '370685005', 'org_name': '阜山卫生院'}...
# for i in range(len(l_d2)):
#     # print(l_d2[i])
#     if l_d2[i]['org_name'] == p['org_name']:
#         p.update({'orgCode': l_d2[i]['org_code']})
#         break
# print(p)  # {'org_name': '道头卫生院', 'year': '2024', 'method': 'GET', 'path': '/serverExport/report/getSmiBi?0=', 'res': 'registered', 'orgCode': '370685009'}
# # 获取三级医院机构
# l_d3 = Sqlserver_PO1.select("select org_sub_code, org_sub_name from sys_sub_hospital where org_code='%s'" % (p['orgCode']))
# # print(l_d3)  # [{'org_sub_code': '370685009001', 'org_sub_name': '雀头孙家村卫生室'}, {'org_sub_code': '370685009002', 'org_sub_name': '招远市齐山镇梁家村卫生室'}, ...
# p.update({'org3': l_d3})
# print(p)

# todo 2, 将公卫报表指标检查点用例（gwCase.xlsx）导入db
# 自动将SheetName转为拼音字母，并添加前缀a_, 如"7精神障碍: => a_7jingshenzhangai
GwIndex_PO = GwIndexPO()
GwIndex_PO.createTable('7精神障碍')

# sys.exit(0)
# todo 3, 从db中执行用例
GwIndex_PO = GwIndexPO("7精神障碍")

# 批量创建数据
# for i in range(3):
#     GwIndex_PO.gen({"index":1, "type":"level3"})

GwIndex_PO.gen({"index":1, "type":"level3", 'org_code': '370685009014'})


# 执行index1的type为param的content
# GwIndex_PO.run({"index":1, "type":"level3"})
# GwIndex_PO.run({"index":1, "type":"level2"})
# GwIndex_PO.run({"index":1, "type":"level1"})





