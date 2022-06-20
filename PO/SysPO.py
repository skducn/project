# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2021-12-10
# Description: 系统对象
# ***************************************************************

'''
1 关闭进程

2.1 输出带颜色的系统错误（简）
2.2 输出带颜色的系统错误

3 切换各平台打开文件

'''

import psutil, os, sys, platform
from time import sleep
from PO.ColorPO import *
Color_PO = ColorPO()

class SysPO():

    def killPid(self, varApplication):

        # todo 1 关闭进程
        '''
        注意：如果 os.system 输出出现乱码，需将 File->Settings->Editor->File Encodings 中 Global Encoding 设置成 GBK
        '''

        try:
            pids = psutil.pids()
            for pid in pids:
                p = psutil.Process(pid)
                # print('pid=%s,pname=%s' % (pid, p.name()))
                if p.name() == varApplication:
                    cmd = 'taskkill /F /IM ' + varApplication
                    os.system(cmd)
                    sleep(2)
        except:
            None


    def outMsg1(self, msgStatus, errLine, func2, errMsg):

        # todo 2.1 输出带颜色的系统错误（简）

        if msgStatus == "error":
            Color_PO.consoleColor("31", "31", "[" + msgStatus + "], line " + str(errLine) + ", " + func2, errMsg)
        elif msgStatus == "warning":
            Color_PO.consoleColor("31", "33", "[" + msgStatus + "], line " + str(errLine) + ", " + func2, errMsg)

    def outMsg2(self, msgStatus, errLine, func1, file, func2):

        # todo 2.2 输出带颜色的系统错误

        if msgStatus == "error":
            Color_PO.consoleColor("31", "31", "[Error] , line " + str(errLine) + " (" + func1 + "()) jump to (" + file + " -> " + func2 + "())", "")
        elif msgStatus == "warning":
            Color_PO.consoleColor("31", "33", "[Warning] , line " + str(errLine) + " (" + func1 + "()) jump to (" + file + " -> " + func2 + "())", "")


    def openFile(self, varFile):

        # todo 3 切换各平台打开文件

        if platform.system() == 'Darwin':
            os.system("open " + varFile)
        if platform.system() == 'Windows':
            os.system("start " + varFile)

if __name__ == '__main__':

    Sys_PO = SysPO()

    # print(" 关闭进程".center(100, "-"))
    # Sys_PO.killPid('EXCEL.EXE')
    # Sys_PO.killPid('360Newsld.exe')
    #
    #
    # print("2.1 输出系统错误(简)".center(100, "-"))
    # Sys_PO.outMsg1("error", str(sys._getframe(0).f_lineno), sys._getframe(0).f_code.co_name)
    #
    # print("2.2 输出系统错误".center(100, "-"))
    # Sys_PO.outMsg2("error", str(sys._getframe(1).f_lineno), sys._getframe(1).f_code.co_name, sys._getframe().f_code.co_filename, sys._getframe(0).f_code.co_name)


    # print("3 切换各平台打开文件".center(100, "-"))
    # Sys_PO.openFile("rr.html")
    # Sys_PO.openFile("d://111.txt")