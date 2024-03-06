# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-1
# Description: SQLserver for chc
#***************************************************************
from Chc_sqlPO import *


r = Chc_sqlPO("健康评估")
# r = Chc_sqlPO("健康干预")
# r = Chc_sqlPO("中医体质辨识")
# r = Chc_sqlPO("儿童健康干预")
# r = Chc_sqlPO("疾病评估")

# r.run(19)
r.run(2)



# r.i_startAssess("110101196407281501")
# r.i_startAssess("310101199004110011")