# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018/4/20 15:04
# Description: HTMLTestRunner1.py 通过测试套件执行多个测试用例，并生成报告
# 参数：HTMLTestRunnerPO("脚本路径", "需批量执行的脚本文件 test*.py", "报告路径", "报告名称", "报告标题", "报告主题")
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PO.htmlTestRunnerPO import *
from PO.timePO import *
time_PO = TimePO()

htmlTestRunner_PO = HTMLTestRunnerPO("./", "test*.py", "./", time_PO.getDatetime()+"result.html", "math测试报告名称123", "用例执行详细信息")
htmlTestRunner_PO.runner()
