# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2019-5-7
# Description: OA - 常用工作（）

#***************************************************************

import os, sys
# sys.path.append("../../../../")
from instance.zyjk.OA.PageObject.OaPO import *
Oa_PO = OaPO()
List_PO = ListPO()
Time_PO = TimePO()
Net_PO = NetPO()
Data_PO = DataPO()
File_PO = FilePO()
Excel_PO = ExcelPO()
Char_PO = CharPO()

#***************************************************************#***************************************************************
# 请假申请（默认请假1天）
# 1，请假1天
# Oa_PO.askOff("所有人")
# Oa_PO.askOff("空")
# Oa_PO.askOff('舒阳阳')
# Oa_PO.askOff("金浩,陈晓东")

# 2，请假申请3天以上
# Oa_PO.askOff("所有人", 4)
# Oa_PO.askOff("空", 4)
Oa_PO.askOff('赵云', 4)
Oa_PO.askOff("金浩,曲翰林,朱一航", 4)


#***************************************************************#***************************************************************
# 外出申请（默认外出1天）
# Oa_PO.egression('所有人')
# Oa_PO.egression('空')
# Oa_PO.egression('宾梓洋,李斌,唐坤超')


#***************************************************************#***************************************************************
# 出差申请（默认出差3天以内）
# 1，出差3天以内（包含3天）
# Oa_PO.evection('所有人')
# Oa_PO.evection('空')
# Oa_PO.evection('宾梓洋,李斌,唐坤超')

# 2，出差3天以上
# Oa_PO.evection('所有人', 4)
# Oa_PO.evection('空', 4)
# Oa_PO.evection('宾梓洋,李斌,唐坤超', 4)

