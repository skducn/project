# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: 跑批
# HTMLTestRunner.py /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7
#***************************************************************

from Cos.Config.config import *

from TestCase import *

class RunCos(unittest.TestCase):
    suite = unittest.TestSuite()
    varExcel = os.path.abspath(varExcel)
    varExcelReport = ""
    l_varExcelReport = varLogPrefixPath.split('/')
    for i in range(1, len(l_varExcelReport)):
        varExcelReport = varExcelReport + "//" + l_varExcelReport[i]

    for i in range(1, sheetCase.nrows):
        if sheetCase.cell_value(i, 0) == "Y":
            exec("suite.addTest(unittest.makeSuite(" + sheetCase.cell_value(i, 2) + "))")

    fp = open(varExcelReport + time.strftime("%Y-%m-%d_%H:%M:%S",time.localtime(time.time())) + '.html', 'wb')
    print varExcelReport + time.strftime("%Y-%m-%d_%H:%M:%S",time.localtime(time.time())) + '.html'
    HTMLTestRunner.HTMLTestRunner(stream=fp, title=varProjectTitle, description=u'测试报告').run(suite)
    fp.close()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RunCos)

