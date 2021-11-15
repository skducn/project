# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 招远防疫 epidemic 接口自动化
# 接口文档：http://192.168.0.237:8001/swagger-ui.html
# md5在线加密  https://md5jiami.51240.com/
# *****************************************************************

import unittest
from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf

import instance.zyjk.epidemic.frame1.readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
# on_off = localReadConfig.get_email("on_off")

from instance.zyjk.epidemic.frame1.iDriven import *
http = HTTP()

from instance.zyjk.epidemic.frame1.xls import *
xls = XLS()

from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.231", "root", "Zy123456", "epidemic_center", 3306)

from PO.DataPO import *
data_PO = DataPO()

# l_interIsRun = (xls.getInterIsRun())  # 初始化inter中isRun执行筛选列表 ，[[], [], 3]
# 获取接口文档中接口名与属性名，生成字典
# print(xls.d_inter)
# {'/inter/HTTP/auth': 'none', '/inter/HTTP/login': 'username,password', '/inter/HTTP/logout': 'test,userid,id'}


# **********************************************************************************************************************************

class run(unittest.TestCase):
    @parameterized.expand(xls.getCaseParam())
    def test11(self, excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_KeyValueQuote):
        ' '
        xls.result(excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_KeyValueQuote)

        # if interMethod == "postLogin": xls.result(excelNo, interCase, interUrl, interMethod, dict(eval(interParam)), interCheck, interExpected, d_KeyValueQuote)
        # elif interMethod == "post": xls.result(excelNo, interCase, interUrl, interMethod, dict(eval(interParam)), interCheck, interExpected, d_KeyValueQuote)
        # elif interMethod == "get": xls.result(excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_KeyValueQuote)
        # else: xls.result(excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_KeyValueQuote)   # postget

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
    # if on_off == 'on':
    #     email.send_email()


