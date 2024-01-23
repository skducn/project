# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-1-10
# Description: 公卫 - 老年人上传到公卫
# 【腾讯文档】老年人上传公卫流程测试
# https://docs.qq.com/doc/DS25UWkVTQnN0bmxF
# *****************************************************************

# 解决方法：
import warnings
warnings.simplefilter("ignore")

from PO.SqlserverPO import *
Sqlserver_PO_PHUSERS = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS")  # 公卫
Sqlserver_PO_PHS = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHS")  # 老年人体检

from PO.DataPO import *
Data_PO = DataPO()

# todo 公卫，从T_EHR_INFO 表中随机获取一个身份证，如 411526199505275413
# a = Sqlserver_PO_PHUSERS.execQuery("select * from PHUSERS.dbo.T_EHR_INFO where IDCARD = '411526199505275413'")
phusers_idcard = '411526199505275413'


# # todo 1，初始化a_phs2gw表
# # 删除表
Sqlserver_PO_PHS.execute("drop table PHS.dbo.a_phs2gw")
# 创建a_phs2gw表，用于保存phs和phusers的字段和值
Sqlserver_PO_PHS.crtTable('a_phs2gw', 'phsField VARCHAR(100) NULL, phsValue VARCHAR(5000) NULL, phusersField VARCHAR(100) NULL, phusersValue VARCHAR(5000) NULL, result VARCHAR(10) NULL')


# todo 2，老年人，依据身份证更新24小时前日期和时间
# 0 表示不存在； 1 表示存在；
isIdcard = Sqlserver_PO_PHS.execQuery("select count(*) as count from PHS.dbo.t_snr_patient_info where id_card = '%s' " % (phusers_idcard))
# print(isIdcard[0]['count'])  # 1

# 不存在，则自动将第一条的id_card更新为phusers_idcard
if isIdcard[0]['count'] == 0:
    Sqlserver_PO_PHS.execute("update top(1) PHS.dbo.t_snr_patient_info set id_card = '%s'" % (phusers_idcard))
    # 获取examination_num
    phs = Sqlserver_PO_PHS.execQuery("select examination_num from PHS.dbo.t_snr_patient_info where id_card = '%s' " % (phusers_idcard))
    phs_examination_num = phs[0]['examination_num']
    # print(phs_examination_num)  # 100200100710003
    Sqlserver_PO_PHS.execute("UPDATE top(1) dbo.t_snr_examination_info SET examination_num = '%s' " % (phs_examination_num))

# 获取 examination_num
phs = Sqlserver_PO_PHS.execQuery("select examination_num from PHS.dbo.t_snr_patient_info where id_card = '%s' " % (phusers_idcard))
phs_examination_num = phs[0]['examination_num']
# print(phs_examination_num)  # 2301890006

# 更新日期
testDate = (datetime.datetime.now() + datetime.timedelta(hours=-24)).strftime("%Y-%m-%d %H:%M:%S")  # 获取24小时前日期和时间
Sqlserver_PO_PHS.execute("update PHS.dbo.t_snr_examination_info set update_date = '%s' where examination_num = '%s'" % (testDate, phs_examination_num))
# print(testDate)  # 2024-01-21 16:09:28

# 获取视图中记录
phs_record = Sqlserver_PO_PHS.execQuery("select * from PHS.dbo.v_snr_examination_info where id_card = '%s'" % (phusers_idcard))
# phs_record = Sqlserver_PO_PHS.execQuery("select * from PHS.dbo.t_snr_examination_info where examination_num = '%s'" % (lnr_examination_num)) # 废弃
# print(phs_record)
# print(len(phs_record[0]))  # 194


# todo 3，将老年人记录插入到a_phs2gw表
for k, v in phs_record[0].items():
    Sqlserver_PO_PHS.execute("insert into PHS.dbo.a_phs2gw (phsField, phsValue) values('%s','%s') " % (k, v))


# todo 4，执行存储过程
Sqlserver_PO_PHUSERS.execCall("PHS_EXAMTO_PHSSERS")


# todo 5，判断老年人记录是否已经在公卫中，存在则更新到公卫，不存在则复制到公卫。
# # 老年人，获取 odlId
phs_odlId = Sqlserver_PO_PHS.execQuery("select odlId from PHS.dbo.v_snr_examination_info where id_card = '%s'" % (phusers_idcard))
phs_odlId = phs_odlId[0]['odlId']
# print(phs_odlId)  # 3029
#
# # 判断老年人odlId值是否存在于公卫patient_id中，0表示不存在，非0表示存在
# isExist = Sqlserver_PO_PHUSERS.execQuery("SELECT count(*) as result FROM PHUSERS.dbo.T_SNR_EXAMINATION_INFO  t1  inner JOIN phs.dbo.V_SNR_EXAMINATION_INFO t2 ON t1.PATIENT_ID=t2.odlId  where t2.odlId   in (select PATIENT_ID from PHUSERS.dbo.T_SNR_EXAMINATION_INFO) and t2.odlId = '%s'" % (phs_odlId))
# print(isExist[0]['result'])  # 1

# if isExist[0]['result'] == 0:
#     # 不存在则复制到公卫。
#     ...
# else:
#     # 存在则更新到公卫。（未完成，需要更新全部字段值或空的字段值？？？）
#     ...
#     # Sqlserver_PO_PHUSERS.execute("update PHUSERS.dbo.t_snr_examination_info set temperature='100.12' where examination_num = '%s'" % (phs_examination_num))




# todo 6，依据老年人phsField，将公卫记录更新到a_phs2gw表
gw = Sqlserver_PO_PHUSERS.execQuery("select * from PHUSERS.dbo.t_snr_examination_info where patient_id='%s'" % (phs_odlId))
for k, v in gw[0].items():
    k = str(k).lower()
    Sqlserver_PO_PHS.execute("update PHS.dbo.a_phs2gw set phusersField = '%s', phusersValue = '%s' where phsField = '%s' " % (k, v, k))
    if k == 'patient_id':
        Sqlserver_PO_PHS.execute("update PHS.dbo.a_phs2gw set phusersField = '%s', phusersValue = '%s' where phsField = 'odLid' " % (k, v))
    if k == 'idcard':
        Sqlserver_PO_PHS.execute("update PHS.dbo.a_phs2gw set phusersField = '%s', phusersValue = '%s' where phsField = 'id_card' " % (k, v))


# todo 7，a_phs2gw表比对
l_d_row = Sqlserver_PO_PHS.execQuery("select * from a_phs2gw")
for r, index in enumerate(l_d_row):
    if l_d_row[r]['phsValue'] == l_d_row[r]['phusersValue']:
        Sqlserver_PO_PHS.execute("update a_phs2gw set result='ok' where phsValue='%s' and phusersValue='%s' " % (l_d_row[r]['phsValue'], l_d_row[r]['phusersValue']))
    else:
        Sqlserver_PO_PHS.execute("update a_phs2gw set result='error' where phsValue='%s' and phusersValue='%s' " % (l_d_row[r]['phsValue'], l_d_row[r]['phusersValue']))


# 最后手工打开 a_phs2gw表，人工审核检查result为error值。




