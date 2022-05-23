# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2021-12-10
# Description: 系统对象
# ***************************************************************

'''
1，关闭进程
'''

import psutil, os, sys
from time import sleep
from PO.ColorPO import *
Color_PO = ColorPO()

class SysPO():

    def killPid(self, varApplication):
        '''
        1，关闭进程
        :param varApplication:
        :return:
                os.system 输出如果出现乱码，需将 File->Settings->Editor->File Encodings 中 Global Encoding 设置成 GBK
        '''

        pids = psutil.pids()
        for pid in pids:
            try:
                p = psutil.Process(pid)
                # print('pid=%s,pname=%s' % (pid, p.name()))
                if p.name() == varApplication:
                    cmd = 'taskkill /F /IM ' + varApplication
                    os.system(cmd)
                    sleep(2)
            except:
                print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def outMsg(self, msgStatus, errLine, func1, file, func2):
        '''2.1,输出系统错误'''

        if msgStatus == "error":
            Color_PO.consoleColor("31", "31", "[Error] , line " + str(errLine) + " (" + func1 + "()) jump to (" + file + " -> " + func2 + "())", "")
        elif msgStatus == "warning":
            Color_PO.consoleColor("31", "33", "[Warning] , line " + str(errLine) + " (" + func1 + "()) jump to (" + file + " -> " + func2 + "())", "")


    def outMsg2(self, msgStatus, errLine, func2, errMsg):
        '''2.2,输出系统错误'''

        if msgStatus == "error":
            Color_PO.consoleColor("31", "31", "[" + msgStatus + "], line " + str(errLine) + ", " + func2, errMsg)
        elif msgStatus == "warning":
            Color_PO.consoleColor("31", "33", "[" + msgStatus + "], line " + str(errLine) + ", " + func2, errMsg)


if __name__ == '__main__':

    Sys_PO = SysPO()

    # print("1，关闭进程".center(100, "-"))
    # Sys_PO.killPid('EXCEL.EXE')
    # Sys_PO.killPid('360Newsld.exe')

    print("2,输出系统错误".center(100, "-"))
    Sys_PO.outMsg("error", str(sys._getframe(1).f_lineno), sys._getframe(1).f_code.co_name, sys._getframe().f_code.co_filename, sys._getframe(0).f_code.co_name)

    print("2.2,输出系统错误(简)".center(100, "-"))
    Sys_PO.outMsg2("error", str(sys._getframe(0).f_lineno), sys._getframe(0).f_code.co_name)

