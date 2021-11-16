# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 招远防疫 epidemic 接口自动化
# 接口文档：http://192.168.0.237:8001/swagger-ui.html
# web页：http://192.168.0.243:8002/admin/notice/index  （测试243， 开发237）
# *****************************************************************

import unittest
from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf
from PO.MysqlPO import *

import instance.zyjk.epidemic.frame1.readConfig as readConfig
localReadConfig = readConfig.ReadConfig()

if localReadConfig.get_system("switchENV") == "test":
    db_ip = localReadConfig.get_test("db_ip")
    db_username = localReadConfig.get_test("db_username")
    db_password = localReadConfig.get_test("db_password")
    db_port = localReadConfig.get_test("db_port")
    db_database = localReadConfig.get_test("db_database")
else:
    db_ip = localReadConfig.get_dev("db_ip")
    db_username = localReadConfig.get_dev("db_username")
    db_password = localReadConfig.get_dev("db_password")
    db_port = localReadConfig.get_dev("db_port")
    db_database = localReadConfig.get_dev("db_database")

Mysql_PO = MysqlPO(db_ip, db_username, db_password, db_database, db_port)

from instance.zyjk.epidemic.frame1.iDriven import *
http = HTTP()

from instance.zyjk.epidemic.frame1.xls import *
xls = XLS()

from PO.DataPO import *
data_PO = DataPO()


class run(unittest.TestCase):
    @parameterized.expand(xls.getCaseParam())
    def test11(self, excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_var):
        ' '
        xls.result(excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_var)

if __name__ == '__main__':

    suite = unittest.defaultTestLoader.discover('.', pattern='run.py', top_level_dir=None)
    runner = bf(suite)
    projectName = localReadConfig.get_system("projectName")
    reportName = localReadConfig.get_system("reportName")
    runner.report(filename='report\\' + reportName, description= projectName + '测试报告')
    # runner.report(filename='./report/report_' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.html', description='logo的测试报告')
    if platform.system() == 'Darwin':
        os.system("open ./report/report.html")
        os.system("open ./config/interface.xlsx")
    if platform.system() == 'Windows':
        os.system("start .\\report\\report.html")
        os.system("start .\\config\\interface.xlsx")