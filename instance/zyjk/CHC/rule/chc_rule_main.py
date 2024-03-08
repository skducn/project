# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-3-8
# Description: CHC规则主程序
#***************************************************************
from Chc_rule_PO import *

# todo 1, 将规则用例（rulecase.xlsx）导入db
# 自动将SheetName转为拼音字母，并添加前缀a_, 如"健康评估: => a_jinhaogaoge
# chc_sqlPO = Chc_rule_PO('')
# chc_sqlPO.createTable('健康评估')
# chc_sqlPO.createTable('健康干预')
# chc_sqlPO.createTable('中医体质辨识')
# chc_sqlPO.createTable('疾病评估')
# chc_sqlPO.createTable('儿童健康干预')
# chc_sqlPO.createTable('疾病身份证')
# chc_sqlPO.createTable('测试规则')


# todo 2, 从db中执行规则用例
# 健康评估,健康干预,中医体质辨识,疾病评估,儿童健康干预
r = Chc_rule_PO("中医体质辨识")

# 按行执行
r.runRow(4)
# r.runRow(32)
# r.runRow(33)
# r.runRow(34)
# r.runRow(98)
# r.runRow(40)
# r.runRow(41)

# 按规则名执行
# r.runRule(('r1', ''))   # 执行单个规则，按照这个格式保留
# r.runRule(('r9', 'r2'))

# 按结果执行
# r.runResult("error")
# r.runResult("all")
