# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-3-8
# Description: 导入数据库
# 将规则用例（chcRuleCase.xlsx）导入db
# 规则：自动将SheetName转为拼音字母，并添加前缀a_, 如"健康评估: => a_jinhaogaoge
#***************************************************************
from ChcRulePO import *
ChcRule_PO = ChcRulePO()

# ver 1.11

# [FILE]
# case = chcRuleCase1.11.xlsx
# # ChcRule_PO.importDB('评估疾病表')
# # # 初始化疾病身份证
# ChcRule_PO.initDiseaseIdcardAll('评估疾病表')

# [FILE]
# case = chcRuleCase.xlsx
# ChcRule_PO.importDB('疾病身份证')
# # # 疾病身份证
# ChcRule_PO.initDiseaseIdcardAll('疾病身份证')



# # ver old
# # ChcRule_PO.importDB('健康评估')
# ChcRule_PO.importDB('健康干预')
# # ChcRule_PO.importDB("中医体质辨识")
# # ChcRule_PO.importDB('疾病评估')
# # ChcRule_PO.importDB('儿童健康干预')
# # ChcRule_PO.importDB('测试规则')

# # ChcRule_PO.importDB('temporaryTable')




