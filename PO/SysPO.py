# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2021-12-10
# Description: 系统对象（获取进程名，获取Pid，获取进程工作目录，当前目录，状态，关闭进程Pid）
# 注意：如果 os.system 输出乱码，需将 File->Settings->Editor->File Encodings 中 Global Encoding 设置成 GBK
# ***************************************************************

'''
1.1，获取进程pid，返回列表 getPid('notepad.exe')
1.2，获取进程名 getApp(13860)
1.3，获取进程的工作目录byApp getExeByApp('notepad.exe')
1.4，获取进程的工作目录byPid getExeByPid(13860)
1.5，获取进程的当前目录byApp getCwdByApp('notepad.exe')
1.6，获取进程的当前目录byPid getCwdByPid(13860)
1.7，获取进程状态byApp getStatusByApp('notepad.exe')
1.8，获取进程状态byPid getStatusByPid(13860)


2.1，关闭进程pid  killPid(13860)
2.1，关闭进程名  killApp('notepad.exe')

3.1 输出带颜色的系统错误（简）
3.2 输出带颜色的系统错误

'''

import psutil, os, sys, platform
from time import sleep
from PO.ColorPO import *
Color_PO = ColorPO()

class SysPO():


    def getPid(self, varApp):

        # 1.1，获取进程pid，返回列表

        l_pid = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_pid.append(pid)
        return l_pid


    def getApp(self, varPid):

        # 1.2，获取进程名

        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if pid == varPid:
                return p.name()


    def getExeByApp(self, varApp):

        # 1.3，获取进程的工作目录byApp

        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                return (p.exe())

    def getExeByPid(self, varPid):

        # 1.4，获取进程的工作目录byPid

        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if pid == varPid:
                return (p.exe())


    def getCwdByApp(self, varApp):

        # 1.5，获取进程的当前目录byApp

        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                return (p.cwd())


    def getCwdByPid(self, varPid):

        # 1.6，获取进程的当前目录byPid

        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if pid == varPid:
                return (p.cwd())


    def getStatusByApp(self, varApp):

        # 1.7，获取进程状态byApp

        l_status = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_status.append(p.status())
        return l_status


    def getStatusByPid(self, varPid):

        # 1.8，获取进程状态byPid

        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if pid == varPid:
                return (p.status())

    def killPid(self, varPid):

        ''' 2.1，关闭进程pid '''

        # if platform.system() == 'Darwin':
        #     os.system('sudo kill -9 ' + varPid)
        # if platform.system() == 'Windows':
        #     os.system('taskkill /F /IM ' + self.getApp(varPid) + "> t")

        l_pid = psutil.pids()
        if varPid in l_pid:
            p = psutil.Process(varPid)
            p.terminate()



    def killApp(self, varApp):

        ''' 2.2，关闭进程名 '''

        l_pid = self.getPid(varApp)
        for i in range(len(l_pid)):
            p = psutil.Process(l_pid[i])
            p.terminate()



    def outMsg1(self, msgStatus, errLine, func2, errMsg):

        # 3.1 输出带颜色的系统错误（简）

        if msgStatus == "error":
            Color_PO.consoleColor("31", "31", "[" + msgStatus + "], line " + str(errLine) + ", " + func2, errMsg)
        elif msgStatus == "warning":
            Color_PO.consoleColor("31", "33", "[" + msgStatus + "], line " + str(errLine) + ", " + func2, errMsg)

    def outMsg2(self, msgStatus, errLine, func1, file, func2):

        # 3.2 输出带颜色的系统错误

        if msgStatus == "error":
            Color_PO.consoleColor("31", "31", "[Error] , line " + str(errLine) + " (" + func1 + "()) jump to (" + file + " -> " + func2 + "())", "")
        elif msgStatus == "warning":
            Color_PO.consoleColor("31", "33", "[Warning] , line " + str(errLine) + " (" + func1 + "()) jump to (" + file + " -> " + func2 + "())", "")




if __name__ == '__main__':

    Sys_PO = SysPO()


    # print("1.1，获取进程pid，返回列表".center(100, "-"))
    # print(Sys_PO.getPid('360se.exe'))  # [11052, 20820]
    # print(Sys_PO.getPid('notepad.exe'))  # [11052]

    # # print("1.2，获取进程名".center(100, "-"))
    # print(Sys_PO.getApp(Sys_PO.getPid('notepad.exe')[0]))  # notepad.exe
    # print(Sys_PO.getApp(14164))  # notepad.exe

    # print("1.3，获取进程的工作目录byApp".center(100, "-"))
    # print(Sys_PO.getExeByApp('notepad.exe'))  # C:\Windows\System32\notepad.exe
    #
    # print("1.4，获取进程的工作目录byPid".center(100, "-"))
    # print(Sys_PO.getExeByPid(20824))  # C:\Windows\System32\notepad.exe
    #
    # print("1.5，获取进程的当前目录byApp".center(100, "-"))
    # print(Sys_PO.getCwdByApp('notepad.exe'))  # C:\Users\jh\Desktop
    #
    # print("1.6，获取进程的当前目录byPid".center(100, "-"))
    # print(Sys_PO.getCwdByPid(20824))  # C:\Users\jh\Desktop

    # print("1.7，获取进程状态byApp".center(100, "-"))
    # print(Sys_PO.getStatusByApp('360se.exe'))  # running
    # #
    # # print("1.8，获取进程状态byPid".center(100, "-"))
    # print(Sys_PO.getStatusByPid(20824))  # running


    # # print("2.1，关闭进程pid".center(100, "-"))
    # Sys_PO.killPid(21500)
    #
    # print("2.2，关闭进程名".center(100, "-"))
    Sys_PO.killApp('notepad.exe')






    # print("3.1 输出系统错误(简)".center(100, "-"))
    # Sys_PO.outMsg1("error", str(sys._getframe(0).f_lineno), sys._getframe(0).f_code.co_name)
    #
    # print("3.2 输出系统错误".center(100, "-"))
    # Sys_PO.outMsg2("error", str(sys._getframe(1).f_lineno), sys._getframe(1).f_code.co_name, sys._getframe().f_code.co_filename, sys._getframe(0).f_code.co_name)

