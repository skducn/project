# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2019-9-19
# Description: 电脑设备对象层（获取本机mac、本机IP、本机电脑名，调用本机摄像头（笔记本））
# 调用笔记本摄像头，需安装opencv包，pip install opencv-python
# ***************************************************************
import socket, uuid, subprocess, os, cv2, sys
import psutil, re

from PO.TimePO import *
Time_PO = TimePO()
from PO.FilePO import *
File_PO = FilePO()

'''
1，获取当前系统平台
2，获取本机硬件mac地址
3，获取当前IP地址
4，获取本机电脑名
5，调用当前笔记本摄像头拍照
6.1，安装apk
6.2，卸载apk

7.1，根据进程名获取PID
7.2，根据pid获取进程的信息
'''


class DevicePO():

    # 1，获取当前系统平台
    def getLocalPlatform(self):
        # 获取当前系统平台
        # Windows系统返回 nt
        # Linux/Unix/Mac系统返回 posix
        return os.name

    # 2，获取本机硬件mac地址
    def getLocalMac(self):
        # 获取本机硬件mac地址
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

    # 3，获取当前IP地址
    def getLocalIp(self):
        # 获取当前IP地址
        varLocalName = socket.getfqdn(socket.gethostname())
        return socket.gethostbyname(varLocalName)

    # 4，获取本机电脑名
    def getLocalName(self):
        # 获取本机电脑名
        return socket.getfqdn(socket.gethostname())

    # 5，调用当前笔记本摄像头拍照
    def callCamera(self, varFilePath=0):
        # 调用当前笔记本摄像头拍照
        # 将拍照照片保存到本地.(不支持中文文件名)
        try:
            if varFilePath == 0:
                tmp = Time_PO.getDatetime()
                varSaveFile = os.getcwd() + "\callCamera" + str(tmp) + ".jpg"
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                cv2.imwrite(varSaveFile, frame)
                cap.release()
            else:
                varPath, varSaveFile = os.path.split(varFilePath)
                File_PO.newLayerFolder(varPath)
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                cv2.imwrite(varFilePath, frame)
                cap.release()
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 6.1，安装apk
    def installAPK(self, varPath):
        ''' ？ 使用 adb、aapt 安装与查看apk '''
        list1 = []
        l = os.listdir(varPath)
        for i in l:
            if u'apk' in i:
                list1.append(i)
        l = list1
        l.sort(key=lambda fn: os.path.getmtime(varPath + "\\" + fn) if not os.path.isdir(varPath + "\\" + fn) else 0)

        # 1，当前设备信息
        device = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE).stdout.read().strip().decode('gbk')
        device = device.split("List of devices attached")[1].split("device")[0].replace("\r\n", "")
        if device != "" :
            print("设备名称 => " + device)

            # 2，定位apk，获取apk包信息（包名 和 launchable-activity）
            fullpath = varPath + "\\" + l[-1]
            print("待处理包 => " + fullpath)
            apkInfo = subprocess.Popen(u"aapt dump badging " + fullpath, shell=True,stdout=subprocess.PIPE).stdout.read().decode('gbk')
            print("name = " + apkInfo.split(" versionCode")[0].replace("package: name=", "").replace("'", ""))  # com.sy.familydoctorandroid
            print("launchable-activity = " + apkInfo.split("launchable-activity: name='")[1].split("'")[0])  # com.sy.familydoctorandroid.mvp.activity.WelcomeActivity

            # 3，卸载（不管有没有安装此包，安装前先卸载）
            subprocess.Popen('adb uninstall ' + apkInfo.split(" versionCode")[0].replace("package: name=", "").replace("'", ""), shell=True, stdout=subprocess.PIPE).stdout.read()
            print(u'已卸载包 => ' + apkInfo.split(" versionCode")[0].replace("package: name=", "").replace("'", ""))

            # 4，安装
            print(u'安装中 ... ')
            print(subprocess.Popen('adb install ' + fullpath, shell=True, stdout=subprocess.PIPE).stdout.read().decode('gbk'))
        else:
            print("error，设备未找到！")

    # 6.2，卸载apk
    def uninstallAPK(self, varPath):
        ''' 使用 adb、aapt 卸载与查看apk '''
        list1 = []
        l = os.listdir(varPath)
        for i in l:
            if u'apk' in i:
                list1.append(i)
        l = list1
        l.sort(key=lambda fn: os.path.getmtime(varPath + "\\" + fn) if not os.path.isdir(varPath + "\\" + fn) else 0)

        # 1，当前设备信息
        device = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE).stdout.read().strip().decode('gbk')
        device = device.split("List of devices attached")[1].split("device")[0].replace("\r\n", "")
        if device != "" :
            print("设备名称 => " + device)

            # 2，定位apk，获取apk包信息（包名 和 launchable-activity）
            fullpath = varPath + "\\" + l[-1]
            print("待处理包 => " + fullpath)
            apkInfo = subprocess.Popen(u"aapt dump badging " + fullpath, shell=True,stdout=subprocess.PIPE).stdout.read().decode('gbk')
            print("name = " + apkInfo.split(" versionCode")[0].replace("package: name=", "").replace("'", ""))  # com.sy.familydoctorandroid
            print("launchable-activity = " + apkInfo.split("launchable-activity: name='")[1].split("'")[0])  # com.sy.familydoctorandroid.mvp.activity.WelcomeActivity

            # 3，卸载（不管有没有安装此包，安装前先卸载）
            subprocess.Popen('adb uninstall ' + apkInfo.split(" versionCode")[0].replace("package: name=", "").replace("'", ""), shell=True, stdout=subprocess.PIPE).stdout.read()
            print(u'已卸载包 => ' + apkInfo.split(" versionCode")[0].replace("package: name=", "").replace("'", ""))
        else:
            print("error，设备未找到！")

    # 7，根据进程名获取PID
    def getProcessPid(self, varProcessName):
        p = psutil.process_iter()
        for r in p:
            aa = str(r)
            f = re.compile(varProcessName, re.I)
            if f.search(aa):
                return (aa.split('pid=')[1].split(',')[0])

if __name__ == '__main__':

    Device_PO = DevicePO()

    print("1，获取当前系统平台".center(100, "-"))
    print(Device_PO.getLocalPlatform())  # nt

    print("2，获取本机硬件mac地址".center(100, "-"))
    print(Device_PO.getLocalMac())  # 50:5b:c2:b6:37:ea

    print("3，获取当前IP地址".center(100, "-"))
    print(Device_PO.getLocalIp())  # 172.21.200.153

    print("4，获取本机电脑名".center(100, "-"))
    print(Device_PO.getLocalName())  # DESKTOP-EOCO1V0

    # print("5，调用当前笔记本摄像头拍照".center(100, "-"))
    # Device_PO.callCamera()   # 无参数，则默认保存在当前路径，文件名为 callCamera当前日期时间，如 callCamera20200312121012.jpp
    # Device_PO.callCamera("d:/filepo/filepo3/h3/h4/123.jpg")  # 如果目录不存在则自动新建，如果文件名重复则覆盖。


    # print("6.1，安装apk".center(100, "-"))
    # Device_PO.installAPK(u"c:\\1")  # 自动安装目录里日期最新的包。

    # print("6.2，卸载apk".center(100, "-"))
    # Device_PO.uninstallAPK(u"c:\\1")  # 自动卸载目录里日期最新的包。


    print("7.1，根据进程名获取PID".center(100, "-"))
    print(Device_PO.getProcessPid("pycharm.exe"))  # 34168

    print("7.2，根据pid获取进程的信息".center(100, "-"))
    p = psutil.Process(int(Device_PO.getProcessPid("pycharm.exe")))

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
