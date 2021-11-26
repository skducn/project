# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 招远防疫 epidemic 接口自动化
# 接口文档：http://192.168.0.237:8001/swagger-ui.html
# web页：http://192.168.0.243:8002/admin/notice/index  （测试243， 开发237）
# pip3 install nose-parameterized   for cmd
# pip3 install BeautifulReport for cmd
# pip3 install --upgrade pip
# 提示语:Done 在C:\Python39\Lib\site-packages\BeautifulReport\BeautifulReport.py
# *****************************************************************

import unittest, platform, os, sys
from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
from time import sleep

# 参数切换 test dev 环境
argvParam = sys.argv[1:3]

# 如果没有参数，默认test环境
if len(argvParam) == 0 :
    localReadConfig.cf['ENV'] = {'switchENV': 'test'}
    with open('config.ini', 'w') as configfile:
        localReadConfig.cf.write(configfile)

# 如果只有1个参数，这个参数可选择 dev 或 test ，两者都不是默认test
if len(argvParam) == 1 :
    if argvParam[0] == "-h" or argvParam[0] == "-help" or argvParam[0] == "/?":
        print("语法：python run.py 参数1 参数2\n")
        print("参数1：选择执行脚本的环境，两可选项 test 或 dev ， 如两者都不是则默认test\n")
        print("参数2：执行完后是否自动打开测试报告或测试用例表格，三可选项 report 、 excel 、 all ， all表示两者都打开\n")
        print("实例1： python run.py test    // 执行test环境\n")
        print("实例2： python run.py test report   // 执行test环境，完成后自动打开测试报告\n")
        print("实例3： python run.py test excel   // 执行test环境，完成后自动打开测试用例表格\n")
        print("实例4： python run.py test all   // 执行test环境，完成后自动打开测试报告和测试用例表格\n")
        exit()

    if argvParam[0] == "dev":
        localReadConfig.cf['ENV'] = {'switchENV': 'dev'}
        with open('config.ini', 'w') as configfile:
            localReadConfig.cf.write(configfile)
    else:
        localReadConfig.cf['ENV'] = {'switchENV': 'test'}
        with open('config.ini', 'w') as configfile:
            localReadConfig.cf.write(configfile)

# 如果有2个参数，则第一个参数是可选择 dev 或 test ，第二个参数是是否执行完自动打开 report.html
if len(argvParam) == 2 :
    if argvParam[0] == "dev":
        localReadConfig.cf['ENV'] = {'switchENV': 'dev'}
        with open('config.ini', 'w') as configfile:
            localReadConfig.cf.write(configfile)
    else:
        localReadConfig.cf['ENV'] = {'switchENV': 'test'}
        with open('config.ini', 'w') as configfile:
            localReadConfig.cf.write(configfile)


import xls as xls
xls1 = xls.XLS()


class run(unittest.TestCase):
    @parameterized.expand(xls1.getCaseParam())
    def test12(self, excelNo, iType, iSort, iName, iPath, iMethod, iParam, iKey, iValue, globalVar, sql):
        ' '
        xls1.result(excelNo, iType, iSort, iName, iPath, iMethod, iParam, iKey, iValue, globalVar, sql)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern='run.py', top_level_dir=None)
    runner = bf(suite)
    projectName = localReadConfig.get_system("projectName")
    reportName = localReadConfig.get_system("reportName")
    if platform.system() == 'Darwin':
        runner.report(filename='./data/' + reportName, description=projectName + '测试报告')
        if len(argvParam) == 2:
            if argvParam[1] == "report":
                os.system("open ./data/" + localReadConfig.get_system("reportName"))
            if argvParam[1] == "excel":
                os.system("open " + localReadConfig.get_system("excelName"))
            if argvParam[1] == "all":
                os.system("open ./data/" + localReadConfig.get_system("reportName"))
                os.system("open " + localReadConfig.get_system("excelName"))

    if platform.system() == 'Windows':
        runner.report(filename='data\\' + reportName, description=projectName)
        if len(argvParam) == 2:
            if argvParam[1] == "report":
                os.system("start .\\data\\" + localReadConfig.get_system("reportName"))
            if argvParam[1] == "excel":
                os.system("start " + localReadConfig.get_system("excelName"))
            if argvParam[1] == "all":
                os.system("start .\\data\\" + localReadConfig.get_system("reportName"))
                os.system("start " + localReadConfig.get_system("excelName"))