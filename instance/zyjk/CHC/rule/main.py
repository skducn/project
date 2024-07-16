# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-3-8
# Description: CHC规则主程序
#***************************************************************
from ChcrulePO import *

# todo 1, 将规则用例（chcRuleCase.xlsx）导入db
# 自动将SheetName转为拼音字母，并添加前缀a_, 如"健康评估: => a_jinhaogaoge
# Chcrule_PO = ChcrulePO()
# Chcrule_PO.createTable('健康评估')
# Chcrule_PO.createTable('健康干预')
# Chcrule_PO.createTable("中医体质辨识")
# Chcrule_PO.createTable('疾病评估')
# Chcrule_PO.createTable('儿童健康干预')
# Chcrule_PO.createTable('疾病身份证')
# Chcrule_PO.createTable('测试规则')


# todo 2, 从db中执行规则用例
# 健康评估,健康干预,中医体质辨识,疾病评估,儿童健康干预
r = ChcrulePO("中医体质辨识")
# r.runResult("all")  # 执行所有规则
r.runRow(1)  # # 按id执行
# r.runRule(('r12',''))
# r.runRule(('r9', 'r2'))  # 按rule执行(按照这个格式)
# r.runResult("error")  # # 按result执行

