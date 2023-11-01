# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-1
# Description: db
#***************************************************************
from ChcRulePO2 import *

# r = ChcRulePO2("健康评估")
r = ChcRulePO2("健康干预")
# r = ChcRulePO2("中医体质辨识")
# r = ChcRulePO2("儿童健康干预")
# r = ChcRulePO2("疾病评估")
r.run(92)

# r.runResult("")  # 执行result为空的规则
# r.runResult("error")  # 执行result为error的规则
# r.runResult("ok")  # 执行result为ok的规则
# r.runResult("all")  # 执行所有的规则






# r.i_startAssess("110101196407281501")
# r.i_startAssess("310101199004110011")

