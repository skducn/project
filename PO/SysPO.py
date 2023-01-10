# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2021-12-10
# Description: 系统对象（获取进程名，获取Pid，获取进程工作目录，当前目录，状态，关闭进程Pid）
# 注意：如果 os.system 输出乱码，需将 File->Settings->Editor->File Encodings 中 Global Encoding 设置成 GBK
# ***************************************************************

"""

1.1，获取当前系统  getPlatform()
1.2，获取本机mac地址  getMacAddress()
1.3，获取当前IP地址  getIp()
1.4，获取本机电脑名  getComputerName()
1.5，获取当前屏幕分辨率 getResolution()

2.1，获取应用程序进程的PID  getPID(app)
2.2，获取应用程序进程名 getApp(pid)
2.3，获取应用程序进程的工作目录 getAppWorkFolder(app)
2.4，获取PID进程的工作目录 getPIDWorkFolder(pid)
2.5，获取应用程序进程的当前目录 getAppCurrFolder(app)
2.6，获取PID进程的当前目录 getPIDcurrFolder(pid)
2.7，获取应用程序进程的状态 getAppStatus(app)
2.8，获取PID进程的状态 getPIDstatus(pid)
2.9，关闭应用程序进程的PID  closePID(pid)
2.10，关闭应用程序进程名 closeApp(app)
2.11，获取应用程序的信息  p = psutil.Process(int(Sys_PO.getPID("pycharm.exe")))


3.1 输出带颜色的系统错误（简）
3.2 输出带颜色的系统错误

"""

import socket, uuid, subprocess, cv2, psutil, re, pyautogui
from time import sleep
from PO.TimePO import *

Time_PO = TimePO()

from PO.FilePO import *

File_PO = FilePO()

from PO.ColorPO import *

Color_PO = ColorPO()


class SysPO:
    def getPlatform(self):

        """
        1.1，获取当前系统
        # Windows系统返回 nt
        # Linux/Unix/Mac系统返回 posix
        :return:
        """

        return os.name

    def getMacAddress(self):

        """
        1.2，获取本机mac地址
        :return:
        """

        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e : e + 2] for e in range(0, 11, 2)])

    def getIp(self):

        """
        1.3，获取当前IP地址
        :return:
        """

        varLocalName = socket.getfqdn(socket.gethostname())
        return socket.gethostbyname(varLocalName)

    def getComputerName(self):

        """
        1.4，获取本机电脑名
        :return:
        """

        return socket.getfqdn(socket.gethostname())

    def getResolution(self):

        """1.5，获取当前屏幕分辨率"""

        width, height = pyautogui.size()
        return (width, height)

    def getPID(self, varApp):

        """2.1，获取应用程序进程的PID"""

        l_pid = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_pid.append(pid)
        return l_pid

    def getApp(self, varPid):

        """2.2，获取应用程序进程名"""

        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if pid == varPid:
                return p.name()

    def getAppWorkFolder(self, varApp):

        """2.3，获取应用程序进程的工作目录"""

        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                return p.exe()

    def getPIDworkFolder(self, varPid):

        """2.4，获取PID进程的工作目录"""

        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if pid == varPid:
                return p.exe()

    def getAppCurrFolder(self, varApp):

        """2.5，获取应用程序进程的当前目录"""

        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                return p.cwd()

    def getPIDcurrFolder(self, varPid):

        """2.6，获取PID进程的当前目录"""

        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if pid == varPid:
                return p.cwd()

    def getAppStatus(self, varApp):

        """2.7，获取应用程序进程的状态"""

        l_status = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_status.append(p.status())
        return l_status

    def getPIDstatus(self, varPid):

        """2.8，获取PID进程的状态"""

        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if pid == varPid:
                return p.status()

    def closePID(self, varPid):

        """2.9，关闭应用程序进程的PID"""

        l_pid = psutil.pids()
        if varPid in l_pid:
            p = psutil.Process(varPid)
            p.terminate()

    def closeApp(self, varApp):

        """2.10，关闭应用程序进程名"""

        l_pid = self.getPID(varApp)
        for i in range(len(l_pid)):
            p = psutil.Process(l_pid[i])
            p.terminate()

    def getAppInfo(self):

        """2.11，获取应用程序的信息"""

        p = psutil.Process(int(self.getPID("pycharm.exe")))

        # 获取进程名
        print(p.name())  # pycharm.exe
        # 进程程序的路径
        print(p.exe())  # C:\Program Files\JetBrains\PyCharm 2018.3.5\bin\pycharm.exe
        # 进程的工作目录绝对路径
        print(p.cwd())  # C:\Users\ZY
        # 进程状态
        print(p.status())  # running
        # 进程创建时间
        print(p.create_time())
        # 进程的cpu时间信息,包括user,system两个cpu信息
        print(p.cpu_times())
        # get进程cpu亲和度,如果要设置cpu亲和度,将cpu号作为参考就好
        print(p.cpu_affinity())
        # 进程内存利用率
        print(p.memory_percent())
        # 进程内存rss,vms信息
        print(p.memory_info())
        # 进程的IO信息,包括读写IO数字及参数
        print(p.io_counters())
        # 进程开启的线程数
        print(p.num_threads())

    def outMsg1(self, msgStatus, errLine, func2, errMsg):

        # 3.1 输出带颜色的系统错误（简）

        if msgStatus == "error":
            Color_PO.consoleColor(
                "31",
                "31",
                "["
                + msgStatus
                + "], line "
                + str(errLine)
                + ", "
                + str(func2)
                + ", "
                + errMsg,
                "",
            )
        elif msgStatus == "warning":
            Color_PO.consoleColor(
                "31",
                "33",
                "["
                + msgStatus
                + "], line "
                + str(errLine)
                + ", "
                + str(func2)
                + ", "
                + errMsg,
                "",
            )

    def outMsg2(self, msgStatus, errLine, func1, file, func2):

        # 3.2 输出带颜色的系统错误??

        if msgStatus == "error":
            Color_PO.consoleColor(
                "31",
                "31",
                "[Error] , line "
                + str(errLine)
                + " ("
                + func1
                + "()) jump to ("
                + file
                + " -> "
                + func2
                + "())",
                "",
            )
        elif msgStatus == "warning":
            Color_PO.consoleColor(
                "31",
                "33",
                "[Warning] , line "
                + str(errLine)
                + " ("
                + func1
                + "()) jump to ("
                + file
                + " -> "
                + func2
                + "())",
                "",
            )


if __name__ == "__main__":

    Sys_PO = SysPO()

    # print("1.1，获取当前系统".center(100, "-"))
    # print(Sys_PO.getPlatform())  # nt  //表示windows
    #
    # print("1.2，获取本机mac地址".center(100, "-"))
    # print(Sys_PO.getMacAddress())  # 00:e1:8c:93:f6:76
    #
    # print("1.3，获取当前IP地址".center(100, "-"))
    # print(Sys_PO.getIp())  # 192.168.1.111
    #
    # print("1.4，获取本机电脑名".center(100, "-"))
    # print(Sys_PO.getComputerName())  # DESKTOP-DO7AEPU
    #
    # print("1.5，获取当前屏幕分辨率".center(100, "-"))
    # print(Sys_PO.getResolution())  # [1536, 864]
    #
    #
    # print("2.1，获取应用程序进程的PID".center(100, "-"))
    # print(Sys_PO.getPID('360se.exe'))  # [11052, 20820]
    # print(Sys_PO.getPID('notepad.exe'))  # [11052]
    #
    # print("2.2，获取应用程序进程名".center(100, "-"))
    # print(Sys_PO.getApp(Sys_PO.getPID('notepad.exe')[0]))  # notepad.exe
    # print(Sys_PO.getApp(14164))  # notepad.exe
    #
    # print("2.3，获取应用程序进程的工作目录".center(100, "-"))
    # print(Sys_PO.getAppWorkFolder('notepad.exe'))  # C:\Windows\System32\notepad.exe
    #
    # print("2.4，获取PID进程的工作目录".center(100, "-"))
    # print(Sys_PO.getPIDworkFolder(20824))  # C:\Windows\System32\notepad.exe
    #
    # print("2.5，获取应用程序进程的当前目录".center(100, "-"))
    # print(Sys_PO.getAppCurrFolder('notepad.exe'))  # C:\Users\jh\Desktop
    #
    # print("2.6，获取PID进程的当前目录".center(100, "-"))
    # print(Sys_PO.getPIDcurrFolder(20824))  # C:\Users\jh\Desktop
    #
    # print("2.7，获取应用程序进程的状态".center(100, "-"))
    # print(Sys_PO.getAppStatus('notepad.exe'))  # running
    # #
    # print("2.8，获取PID进程的状态".center(100, "-"))
    # print(Sys_PO.getPIDstatus(20824))  # running

    # # print("2.9，关闭应用程序进程的PID".center(100, "-"))
    # Sys_PO.closePID(21500)
    #
    # print("2.10，关闭应用程序进程名".center(100, "-"))
    # Sys_PO.closeApp('notepad.exe')

    # # print("3.1 输出系统错误(简)".center(100, "-"))
    # Sys_PO.outMsg1("error", str(sys._getframe(0).f_lineno), sys._getframe(0).f_code.co_name , "错误提示")
    # Sys_PO.outMsg1("warning", str(sys._getframe(0).f_lineno), sys._getframe(0).f_code.co_name , "错误提示")
    # #
    # # print("3.2 输出系统错误".center(100, "-"))
    # Sys_PO.outMsg2("error", str(sys._getframe(1).f_lineno), sys._getframe(1).f_code.co_name, sys._getframe().f_code.co_filename, sys._getframe(0).f_code.co_name)
    #
