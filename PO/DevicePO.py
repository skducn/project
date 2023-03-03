# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2019-9-19
# Description: 硬件设备层（获取系统，mac地址，本机IP，本机电脑名，调用本机摄像头（笔记本），屏幕分辨率，安装卸载apk，获取停用PID）
# 调用笔记本摄像头，需安装opencv包(cv2)，pip install opencv-python
# ***************************************************************

"""

1，调用当前笔记本摄像头拍照  callCamera()

2.1，安装apk  installAPK()
2.2，卸载apk  uninstallAPK()


"""

import socket, uuid, subprocess, cv2, psutil, re, pyautogui

from PO.TimePO import *
Time_PO = TimePO()

from PO.FilePO import *
File_PO = FilePO()


class DevicePO:
    def callCamera(self, varFilePath=0):

        """1，调用当前笔记本摄像头拍照"""

        # 调用当前笔记本摄像头拍照
        # 将拍照照片保存到本地.(不支持中文文件名)
        try:
            if varFilePath == 0:
                tmp = Time_PO.getDateTime()
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
                cv2.waitKey(2)
                cv2.imwrite(varFilePath, frame)
                cap.release()
                cv2.destroyAllWindows()
        except:
            print(
                "[ERROR], "
                + sys._getframe(1).f_code.co_name
                + ", line "
                + str(sys._getframe(1).f_lineno)
                + ", in "
                + sys._getframe(0).f_code.co_name
                + ", SourceFile '"
                + sys._getframe().f_code.co_filename
                + "'"
            )

    def callCamera2(self):

        import cv2

        cap = cv2.VideoCapture(0)
        i = 0
        while (1):
            ret, frame = cap.read()
            k = cv2.waitKey(1)
            if k == 27:
                break
            elif k == ord('s'):
                # 注意修改保持路径
                cv2.imwrite('/Users/linghuchong/' + str(i) + '.jpg', frame)
                i += 1
            cv2.imshow("capture", frame)
        cap.release()
        cv2.destroyAllWindows()

    def installAPK(self, varPath):

        """2.1，安装apk"""
        """ ？ 使用 adb、aapt 安装与查看apk """
        list1 = []
        l = os.listdir(varPath)
        for i in l:
            if "apk" in i:
                list1.append(i)
        l = list1
        l.sort(
            key=lambda fn: os.path.getmtime(varPath + "\\" + fn)
            if not os.path.isdir(varPath + "\\" + fn)
            else 0
        )

        # 1，当前设备信息
        device = (
            subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE)
            .stdout.read()
            .strip()
            .decode("gbk")
        )
        device = (
            device.split("List of devices attached")[1]
            .split("device")[0]
            .replace("\r\n", "")
        )
        if device != "":
            print("设备名称 => " + device)

            # 2，定位apk，获取apk包信息（包名 和 launchable-activity）
            fullpath = varPath + "\\" + l[-1]
            print("待处理包 => " + fullpath)
            apkInfo = (
                subprocess.Popen(
                    "aapt dump badging " + fullpath, shell=True, stdout=subprocess.PIPE
                )
                .stdout.read()
                .decode("gbk")
            )
            print(
                "name = "
                + apkInfo.split(" versionCode")[0]
                .replace("package: name=", "")
                .replace("'", "")
            )  # com.sy.familydoctorandroid
            print(
                "launchable-activity = "
                + apkInfo.split("launchable-activity: name='")[1].split("'")[0]
            )  # com.sy.familydoctorandroid.mvp.activity.WelcomeActivity

            # 3，卸载（不管有没有安装此包，安装前先卸载）
            subprocess.Popen(
                "adb uninstall "
                + apkInfo.split(" versionCode")[0]
                .replace("package: name=", "")
                .replace("'", ""),
                shell=True,
                stdout=subprocess.PIPE,
            ).stdout.read()
            print(
                "已卸载包 => "
                + apkInfo.split(" versionCode")[0]
                .replace("package: name=", "")
                .replace("'", "")
            )

            # 4，安装
            print("安装中 ... ")
            print(
                subprocess.Popen(
                    "adb install " + fullpath, shell=True, stdout=subprocess.PIPE
                )
                .stdout.read()
                .decode("gbk")
            )
        else:
            print("error，设备未找到！")

    def uninstallAPK(self, varPath):

        """2.2，卸载apk"""
        """ 使用 adb、aapt 卸载与查看apk """
        list1 = []
        l = os.listdir(varPath)
        for i in l:
            if "apk" in i:
                list1.append(i)
        l = list1
        l.sort(
            key=lambda fn: os.path.getmtime(varPath + "\\" + fn)
            if not os.path.isdir(varPath + "\\" + fn)
            else 0
        )

        # 1，当前设备信息
        device = (
            subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE)
            .stdout.read()
            .strip()
            .decode("gbk")
        )
        device = (
            device.split("List of devices attached")[1]
            .split("device")[0]
            .replace("\r\n", "")
        )
        if device != "":
            print("设备名称 => " + device)

            # 2，定位apk，获取apk包信息（包名 和 launchable-activity）
            fullpath = varPath + "\\" + l[-1]
            print("待处理包 => " + fullpath)
            apkInfo = (
                subprocess.Popen(
                    "aapt dump badging " + fullpath, shell=True, stdout=subprocess.PIPE
                )
                .stdout.read()
                .decode("gbk")
            )
            print(
                "name = "
                + apkInfo.split(" versionCode")[0]
                .replace("package: name=", "")
                .replace("'", "")
            )  # com.sy.familydoctorandroid
            print(
                "launchable-activity = "
                + apkInfo.split("launchable-activity: name='")[1].split("'")[0]
            )  # com.sy.familydoctorandroid.mvp.activity.WelcomeActivity

            # 3，卸载（不管有没有安装此包，安装前先卸载）
            subprocess.Popen(
                "adb uninstall "
                + apkInfo.split(" versionCode")[0]
                .replace("package: name=", "")
                .replace("'", ""),
                shell=True,
                stdout=subprocess.PIPE,
            ).stdout.read()
            print(
                "已卸载包 => "
                + apkInfo.split(" versionCode")[0]
                .replace("package: name=", "")
                .replace("'", "")
            )
        else:
            print("error，设备未找到！")


if __name__ == "__main__":

    Device_PO = DevicePO()

    # print("1，调用当前笔记本摄像头拍照".center(100, "-"))
    # Device_PO.callCamera()   # 无参数，则默认保存在当前路径，文件名为 callCamera当前日期时间，如 callCamera20200312121012.jpp
    # Device_PO.callCamera("d:/11/6/123.jpg")  # 如果目录不存在则自动新建，如果文件名重复则覆盖。
    Device_PO.callCamera("/Users/linghuchong/capture123.jpg")  # 如果目录不存在则自动新建，如果文件名重复则覆盖。
    # Device_PO.callCamera2()  # 如果目录不存在则自动新建，如果文件名重复则覆盖。

    # print("2.1，安装apk".center(100, "-"))
    # Device_PO.installAPK(u"c:\\1")  # 自动安装目录里日期最新的包。
    # Device_PO.installAPK(u"c:\\1")  # 自动安装目录里日期最新的包。

    # print("2.2，卸载apk".center(100, "-"))
    # Device_PO.uninstallAPK(u"c:\\1")  # 自动卸载目录里日期最新的包。
