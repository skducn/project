# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-11-6
# Description: # dm for win
# ***************************************************************u**


from PO.DmPO import *
Dm_PO = DmPO("192.168.0.234", "PHUSERS", "Zy123456789", "5236")  # 测试环境


# result = Dm_PO.execQuery("select * from PHUSERS.SYS_DRUG where id=1")
# print(result[0])  # (1, '1', '阿莫西林', 'AMXL', '111', '1111', 'QD', '每天一次', '1', '颗', '3', '12:00', '1', '规律', False)


result = Dm_PO.execQuery("select * from 中医体质辨识 where id=%s" % (1))
print(result[0])  # (1, 'ok', '2023/10/26 13:16:46', 'r12', 'ABNORMAL_STATUS', 'GY_TZBS01', '体质=平和质', '郭斐', '')



Dm_PO.xlsx2db('规则db.xlsx', "疾病身份证", "疾病身份证")