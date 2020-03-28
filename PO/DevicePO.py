# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2019-9-19
# Description: 电脑设备对象层（获取本机mac、本机IP、本机电脑名，调用本机摄像头（笔记本））
# 调用笔记本摄像头，需安装opencv包，pip install opencv-python
# ***************************************************************
import socket, uuid,  subprocess, os
import cv2

class DevicePO():

    def getPlatform(self):
        '''获取当前使用平台 (Windows返回'nt'，Linux/Unix返回'posix')'''
        return (os.name)  # nt

    def getMAC(self):
        ''' 获取本机硬件 mac 地址'''
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

    def getLocalIP(self):
        ''' 获取本机ip'''
        varLocalName = socket.getfqdn(socket.gethostname())
        return socket.gethostbyname(varLocalName)

    def getLocalName(self):
        ''' 获取本机电脑名'''
        return socket.getfqdn(socket.gethostname())

    def callCamera(self, varSaveFile):
        ''' 调用笔记本摄像头进行拍摄，并将图片进行保存.(暂不支持中文文件名)'''
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite(varSaveFile, frame)
        cap.release()

    def installAPK(self, varPath):
        ''' 使用 adb、aapt 安装与查看apk '''
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

if __name__ == '__main__':
    Device_PO = DevicePO()
    # print(Device_PO.getMAC())
    # print(Device_PO.getLocalIP())
    # print(Device_PO.getLocalName())
    # Device_PO.callCamera("d:\\51\\123.jpg")
    # Device_PO.installAPK(u"c:\\1")  # 自动安装目录里日期最新的包。
    # Device_PO.uninstallAPK(u"c:\\1")  # 自动卸载目录里日期最新的包。

    print(Device_PO.getPlatform())


