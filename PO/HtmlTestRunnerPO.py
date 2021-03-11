# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018/4/20 15:04
# Description: HTMLTestRunner 对象层
# for 2.7 下载：http://tungwaiyip.info/software/HTMLTestRunner.html(for py2.7)
# for 3.X 下载：http://pan.baidu.com/s/1dEZQ0pz （百度地址）
# for mac，将 HTMLTestRunner.py 拷贝到 /usr/local/lib/python3.7/site-packages
# for win，将 HTMLTestRunner.py 拷贝到 C:\Python27\Lib\site-packages
# HtmlTestRunner_PO = HtmlTestRunnerPO("./", "test*.py", "." + "/h4" + "/", "result_" + Time_PO.getDatetime() + ".html","功能测试报告 - Func123", "副标题用例执行详细信息")
# 参数1，./  表示当前目录
# 参数2，test*.py 表示执行所有test开头的脚本
# 参数3，"." + "/h4" + "/"， 表示将结果html保存在当前h4目录中，如果h4不存在则自动创建此目录
# 参数4，"result_" + Time_PO.getDatetime() + ".html" ，表示文件名
# 参数5，"功能测试报告 - Func123" 表示html报告中大标题
# 参数6，副标题用例执行详细信息 表示html报告中副标题
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import unittest
from HTMLTestRunner import HTMLTestRunner
from PO.TimePO import *
from PO.FilePO import *
Time_PO = TimePO()
File_PO = FilePO()


class HtmlTestRunnerPO():

    def __init__(self, varFolder, varPattern, varReportFolder, varReport, varTitle, varDesc):
        # 类的构造函数
        self.varFolder = varFolder
        self.varPattern = varPattern
        self.varReportFolder = varReportFolder
        self.varReport = varReport
        self.varTitle = varTitle
        self.varDesc = varDesc
        File_PO.newFolder(os.getcwd() + "/" + varReportFolder)

    def runner(self):
        # 批量执行文件
        discover = unittest.defaultTestLoader.discover(self.varFolder, pattern=self.varPattern)

        # 报告存放的文件夹
        report_path = self.varReportFolder + self.varReport

        # 生成测试报告
        with open(report_path, 'wb') as f:
            runner = HTMLTestRunner(stream=f, verbosity=2, title=self.varTitle, description=self.varDesc)
            runner.run(discover)
        f.close()


if __name__ == '__main__':
    # 执行当前目录下所有test开头的脚本，将结果保存到report目录下。(如果目录不存在，则自动创建)
    HtmlTestRunner_PO = HtmlTestRunnerPO("./", "test*.py", "." + "/HtmlTestRunnerPO" + "/", "report_" + Time_PO.getDatetime() + ".html", "功能测试报告 - Func123", "副标题用例执行详细信息")
    HtmlTestRunner_PO.runner()