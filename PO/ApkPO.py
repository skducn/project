# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2017-10-26
# Description   : 自动安装目录里日期最新的包。
# *******************************************************************************************************************************
import subprocess, os

class ApkPO():

    def installAPK(self, varPath):
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
    Apk_PO = ApkPO()
    
    Apk_PO.installAPK(u"c:\\1")  # 安装c:\1目录里最新的安装包
    Apk_PO.uninstallAPK(u"c:\\1")  # 卸载c:\1目录里最新的安装包

