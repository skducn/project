# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 招远防疫 epidemic 接口自动化
# 接口文档1：http://192.168.0.237:8001/swagger-ui.html
# 接口文旦2：http://192.168.0.243:8001/doc.html#/
# web页：http://192.168.0.243:8002/admin/notice/index  （测试243， 开发237）
# pip3 install nose-parameterized   for cmd
# pip3 install BeautifulReport for cmd
# pip3 install --upgrade pip
# 提示语: 在 C:\Python39\Lib\site-packages\BeautifulReport\BeautifulReport.py
# pip3 install web.py

# 执行顺序：修改 C:\Python39\Lib\unittest\util.py , return x < y
# def three_way_cmp(x, y):
#     """Return -1 if x < y, 0 if x == y and 1 if x > y"""
#     # return (x > y) - (x < y)
#     return x < y
# 根据排序规则，unittest执行测试用例，默认是根据ASCII码的顺序加载测试用例，数字与字母的顺序为：0-9，A-Z，a-z。
# 参考文档：https://www.cnblogs.com/du-hong/p/10755530.html

# cmd执行：c:\Python39\python run_epidemic.py
# *****************************************************************

import unittest, platform, os
from datetime import datetime
from BeautifulReport import BeautifulReport as bf
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern="epidemic.py", top_level_dir=None)
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
        os.system("start " + xlsName)