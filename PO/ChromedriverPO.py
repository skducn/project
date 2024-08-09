# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2023-7-24
# Description: 下载&解压chromedriver
# https://chromedriver.storage.googleapis.com/index.html
# ***************************************************************
import zipfile, requests, re, subprocess
from urllib.request import urlretrieve
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from PO.FilePO import *
File_PO = FilePO()

# googleChromeVer = subprocess.check_output("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version", shell=True)
# googleChromeVer = bytes.decode(googleChromeVer).replace("\n", '')
# print("当前版本 =>", googleChromeVer)  # Google Chrome 114.0.5735.198
# googleChromeMainVer = (googleChromeVer.split('Google Chrome ')[1].split(".")[0])  # 114
# # googleChromeMainVer = (googleChromeVer.split('Google Chrome ')[1].strip())  # 114.0.5735.198
# print(googleChromeMainVer)
#
# try:
#     resp = requests.get(url="https://chromedriver.storage.googleapis.com/")
#     content = resp.text
#     availableVersionList = re.search(f"<Contents><Key>({googleChromeMainVer}\.\d+\.\d+\.\d+)/chromedriver_mac64\.zip</Key>.*?", content, re.S)
#     # print(f'Available chromedriver version is {availableVersionList}')
#     print(availableVersionList.group(1))  # 114.0.5735.16
#     chromeDriverVer = availableVersionList.group(1)
#     driver_path = ChromeDriverManager(driver_version=chromeDriverVer).install()
#     print(driver_path)  # /Users/linghuchong/.wdm/drivers/chromedriver/mac64/120.0.6099.109/chromedriver-mac-x64/chromedriver
# except:
#     driver_path = ChromeDriverManager().install()
#     print("已安装版本 =>", driver_path)  # /Users/linghuchong/.wdm/drivers/chromedriver/mac64/120.0.6099.109/chromedriver-mac-x64/chromedriver

from PO.DomPO import *

class ChromedriverPO(DomPO):

    def dnldFile(self, varUrlFile, toSave="./"):

        # 下载文件（显示下载进度，数据块大小，文件大小）
        # Net_PO.dnldFile("https://www.7-zip.org/a/7z1900-x64.exe", "d:/1")

        def reporthook(a, b, c):
            print("\r下载进度 => %.0f%%" % int(a * b * 100 / c), end="")

        filename = os.path.basename(varUrlFile)
        # File_PO.newLayerFolder(toSave)  # 新增文件夹
        print("下载 => {}".format(varUrlFile))
        # print("保存路径：{}".format(toSave))
        urlretrieve(varUrlFile, os.path.join(toSave, filename), reporthook=reporthook)

    def dnldChromedriver(self, browserVer, default = 'mac'):

        # 下载指定版本的chromedriver ，如 114.0.5735.198
        # 1，获取下载版本的前三个主版本号，如 114.0.5735.
        browserVerLaster = int(browserVer.split(".")[3])  # 198
        browserVer3 = browserVer.replace(browserVer.split(".")[3], '')  # 114.0.5735.

        tmp = 1
        print("检查 <" + browserVer3 + "?> 版本 => https://chromedriver.storage.googleapis.com/index.html")
        for i in range(browserVerLaster):
            x = browserVerLaster - tmp
            if default == "mac":
                url = 'https://chromedriver.storage.googleapis.com/' + str(browserVer3) + str(x) + '/chromedriver_mac64.zip'
            elif default == "win":
                url = 'https://chromedriver.storage.googleapis.com/' + str(browserVer3) + str(x) + '/chromedriver_win32.zip'
            response = requests.get(url)
            if response.status_code == 200:
                if default == 'mac':
                    path = '/Users/linghuchong/.wdm/drivers/chromedriver/mac64/' + browserVer
                    self.dnldFile(url, path)
                    with zipfile.ZipFile(path + '/chromedriver_mac64.zip', 'r') as zip_ref:
                        zip_ref.extractall(path + '/chromedriver_mac64')  # 将所有文件解压到 chromedriver_mac64目录
                        # zip_ref.extract('chromedriver', path + '/chromedriver_mac64')  # 将指定一个文件 chromedriver 解压到 chromedriver_mac64目录

                elif default == "win":
                    path = '/Users/linghuchong/.wdm/drivers/chromedriver/win32/' + browserVer
                    self.dnldFile(url, path)
                    with zipfile.ZipFile(path + '/chromedriver_win32.zip', 'r') as zip_ref:
                        zip_ref.extractall(path + '/chromedriver_win32')  # 解压所有文件
                        zip_ref.extract('chromedriver.exe', path + '/chromedriver_win32')  # 解压一个文件 chromedriver.exe
                break
            else:
                tmp = tmp + 1


if __name__ == "__main__":

    from PO.WebPO import *
    Web_PO = WebPO("chrome")
    Chromedriver_PO = ChromedriverPO(Web_PO)
    Chromedriver_PO.dnldFile("https://www.7-zip.org/a/7z1900-x64.exe", "/Users/linghuchong/Downloads")


    # Chromedriver_PO.dnldChromedriver("114.0.5735.198", "mac")
    # Chromedriver_PO.dnldChromedriver("114.0.5735.198", "win")
    # Chromedriver_PO.dnldChromedriver("120.0.6099.129 ", "win")
