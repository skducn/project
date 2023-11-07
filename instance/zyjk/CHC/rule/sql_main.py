# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-1
# Description: SQLserver for chc
#***************************************************************
from Sql_chcPO import *

r = Sql_chcPO("健康评估")
# r = Sql_chcPO("健康干预")
# r = ChcRulePO_SQL("中医体质辨识")
# r = ChcRulePO_SQL("儿童健康干预")
# r = ChcRulePO_SQL("疾病评估")
# r.run(19)
r.run(1)


# r.i_startAssess("110101196407281501")
# r.i_startAssess("310101199004110011")

