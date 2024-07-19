# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-3-8
# Description: CHC规则主程序
#***************************************************************
from ChcrulePO import *

# todo 1, 将规则用例（chcRuleCase.xlsx）导入db
# 自动将SheetName转为拼音字母，并添加前缀a_, 如"健康评估: => a_jinhaogaoge
Chcrule_PO = ChcrulePO()
# Chcrule_PO.createTable('健康评估')
Chcrule_PO.createTable('健康干预')
# Chcrule_PO.createTable("中医体质辨识")
# Chcrule_PO.createTable('疾病评估')
# Chcrule_PO.createTable('儿童健康干预')
# Chcrule_PO.createTable('测试规则')
# Chcrule_PO.createTable('疾病身份证')
# Chcrule_PO.createTable('temporaryTable')

# 初始化疾病身份证
# Chcrule_PO.initDiseaseIdcard('310101202308070002')
# Chcrule_PO.initDiseaseIdcardAll()

# todo 2, 从db中执行规则用例
# 健康评估,健康干预,中医体质辨识,疾病评估,儿童健康干预
# r = ChcrulePO("健康干预")
# #
# # # 按id执行
# r.runId([2])

# 按id区间执行
# r.runIdArea([1,5])
# r.runIdArea([1, 25])
# r.runIdArea([40,100])

# 按rule执行
# r.runRule(['r6'])
# r.runRule(['r9', 'r2'])

# 按result执行
# r.runResult("error")

# 执行所有规则
# r.runResult("all")

# 按时间执行（执行库中非2024-07-19的规则）
# r.runDate("2024-07-19")
# r.runDate()  # 默认是当天日期

# 按当前日期执行几天以前的规则（如执行3天以前的规则，即最近3天执行过的规则忽略）
# r.runDateAgo(-3)

# 执行几天以前且状态是error的规则
# r.runDateAgoResult(-3, 'error')
