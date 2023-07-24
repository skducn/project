# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2023-7-24
# Description: 下载&解压chromedriver
# https://chromedriver.storage.googleapis.com/index.html
# ***************************************************************
import subprocess
import sys
import zipfile, requests, os
from PO.FilePO import *
File_PO = FilePO()
from urllib.request import urlretrieve


import re, subprocess
from webdriver_manager.chrome import ChromeDriverManager

chromeBrowserVer = subprocess.check_output("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version", shell=True)
chromeBrowserVer = bytes.decode(chromeBrowserVer)
print(chromeBrowserVer)  # Google Chrome 114.0.5735.198
chromeBrowserFirstVersion = (chromeBrowserVer.split('Google Chrome ')[1].split(".")[0])  # 114
resp = requests.get(url="https://chromedriver.storage.googleapis.com/")
content = resp.text
availableVersionList = re.search(f"<Contents><Key>({chromeBrowserFirstVersion}\.\d+\.\d+\.\d+)/chromedriver_mac64\.zip</Key>.*?", content, re.S)
# print(f'Available chromedriver version is {availableVersionList}')
print(availableVersionList.group(1))  # 114.0.5735.16
chromeDriverVer = availableVersionList.group(1)
driver_path = ChromeDriverManager(driver_version=chromeDriverVer).install()
print(driver_path)  # /Users/linghuchong/.wdm/drivers/chromedriver/mac64/114.0.5735.16/chromedriver

# shutil.move(driver_path, './')


# from webdriver_manager.core.utils import get_browser_version_from_os
# b = get_browser_version_from_os("google-chrome")
# # from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.chrome import ChromeDriver
# a = ChromeDriver.get_browser_version_from_os("Chrome")
# print(a)
#
#
# # vhttps://www.cnpython.com/pypi/webdrivermanager#google_vignette
# from webdrivermanager import ChromeDriverManager
# a = ChromeDriverManager()
# print(a.chrome_driver_base_url)
# print(a.chrome_version_commands)
# print(a.get_latest_version())
# a.download_and_install()

class ChromedriverPO:

    def dnldFile(self, varUrlFile, toSave="./"):

        # 下载文件（显示下载进度，数据块大小，文件大小）
        # Net_PO.dnldFile("https://www.7-zip.org/a/7z1900-x64.exe", "d:/1")

        def reporthook(a, b, c):
            print("\r下载进度: %5f%%" % (a * b * 100.0 / c), end="")

        filename = os.path.basename(varUrlFile)
        File_PO.newLayerFolder(toSave)  # 新增文件夹
        print("下载程序：{}".format(varUrlFile))
        # print("保存路径：{}".format(toSave))
        urlretrieve(varUrlFile, os.path.join(toSave, filename), reporthook=reporthook)


    def dnldChromedriver(self, browserVer, varSystem):

        # browserVer  # 114.0.5735.198
        browserVerLaster = int(browserVer.split(".")[3])  # 198
        browserVer3 = browserVer.replace(browserVer.split(".")[3], '')  # 114.0.5735.

        tmp = 1
        print("正在检查 https://chromedriver.storage.googleapis.com/index.html 上可用的chromedriver版本...")
        for i in range(browserVerLaster):
            x = browserVerLaster - tmp
            if varSystem == "mac":
                url = 'https://chromedriver.storage.googleapis.com/' + str(browserVer3) + str(x) + '/chromedriver_mac64.zip'
            elif varSystem == "win":
                url = 'https://chromedriver.storage.googleapis.com/' + str(browserVer3) + str(x) + '/chromedriver_win32.zip'
            response = requests.get(url)
            if response.status_code == 200:
                self.dnldFile(url)
                if varSystem == 'mac':
                    with zipfile.ZipFile('chromedriver_mac64.zip', 'r') as zip_ref:
                        zip_ref.extract('chromedriver', './')  # 解压一个文件 chromedriver
                        # zip_ref.extractall('./')  # 解压所有文件
                elif varSystem == "win":
                    with zipfile.ZipFile('chromedriver_win32.zip', 'r') as zip_ref:
                        zip_ref.extract('chromedriver', './')  # 解压一个文件 chromedriver
                        # zip_ref.extractall('./')  # 解压所有文件
                break
            else:
                tmp = tmp + 1


if __name__ == "__main__":

    Chromedriver_PO = ChromedriverPO()
    # Chromedriver_PO.dnldChromedriver("114.0.5735.198", "mac")
