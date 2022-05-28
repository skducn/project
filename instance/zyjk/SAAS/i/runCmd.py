# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : saas高血压接口自动化 for cmd
# 接口文档：http://192.168.0.238:8001/swagger-ui.html
# pip3 install nose-parameterized
# pip3 install BeautifulReport
# pip3 install --upgrade pip
# 提示语:Done 在C:\Python39\Lib\site-packages\BeautifulReport\BeautifulReport.py
# for 2.7 下载：http://tungwaiyip.info/software/HTMLTestRunner.html(for py2.7)
# for 3.X 下载：http://pan.baidu.com/s/1dEZQ0pz （百度地址）
# for mac，将 HTMLTestRunner.py 拷贝到 /usr/local/lib/python3.7/site-packages
# for win，将 HTMLTestRunner.py 拷贝到 C:\Python27\Lib\site-packages
# *****************************************************************

import unittest, platform, os, sys
from datetime import date, datetime, timedelta
sys.path.append("../../../../")
import instance.zyjk.epidemic.interface.readConfig as readConfig
# import readConfig as readConfig
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

from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf
import instance.zyjk.epidemic.interface.xls as xls
# import xls as xls
xls1 = xls.XLS()

class run(unittest.TestCase):

    @parameterized.expand(xls1.getCaseParam())
    def test5(self, excelNo, iType, iSort, iName, iPath, iMethod, iParam, iKey, globalVar, sql, tester, caseQty):
        ' '
        xls1.result(excelNo, iType, iSort, iName, iPath, iMethod, iParam, iKey, globalVar, sql, tester, caseQty)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('./', pattern=os.path.split(__file__)[-1], top_level_dir=None)
    runner = bf(suite)
    iDoc = localReadConfig.get_system("iDoc")
    # rptName = localReadConfig.get_system("rptName")
    xlsName = localReadConfig.get_system("xlsName")
    rptTime = str(datetime.now().strftime("%Y%m%d%H%M%S"))
    if platform.system() == 'Darwin':
        # runner.report(filename=rptName, description=iDoc)
        runner.report(filename='./report/iReport_' + rptTime + '.html', description=iDoc)
        os.system("open ./report/iReport_" + rptTime + ".html")
        os.system("open " + xlsName)
    elif platform.system() == 'Windows':
        runner.report(filename='./report/iReport_' + rptTime + '.html', description=iDoc)
        # runner.report(filename=rptName, description=iDoc)
        os.system("start ./report/iReport_" + rptTime + ".html")
        # os.system("start " + xlsName)