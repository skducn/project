# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2017-10-26
# Description   : 文件对象层 (获取路径、目录和文件信息、操作文件、系统级别)
# os.path.expanduser(path)  #把path中包含的"~"和"~user"转换成用户目录
# os.path.getatime(path)  #返回最后一次进入此path的时间。
# os.path.getmtime(path)  #返回在此path下最后一次修改的时间。
# os.path.getctime(path)  #返回path的大小
# os.path.islink(path)  #判断路径是否为链接
# os.path.ismount(path)  #判断路径是否为挂载点（）
# os.path.normcase(path)  #转换path的大小写和斜杠
# os.path.normpath(path)  #规范path字符串形式
# os.path.realpath(path)  #返回path的真实路径
# os.path.relpath(path[, start])  #从start开始计算相对路径
# os.path.samefile(path1, path2)  #判断目录或文件是否相同
# os.path.sameopenfile(fp1, fp2)  #判断fp1和fp2是否指向同一文件
# os.path.samestat(stat1, stat2)  #判断stat tuple stat1和stat2是否指向同一个文件
# os.path.splitunc(path)  #把路径分割为加载点与文件
# os.path.supports_unicode_filenames  #设置是否支持unicode路径名
# *********************************************************************
'''
1.1，获取环境变量的值
1.2，添加路径到系统环境变量中
1.3 根据环境变量的值替换path

2.1，获取当前路径（反斜线）
2.2，获取当前路径
2.3，获取上层目录路径（反斜线）
2.4，获取上层目录路径
2.5，获取自定义上层目录路径
2.6 切换路径，影响os.getcwd()

3.1，获取目录清单（目录或文件按照数字、字符、中文顺序排列输出），无参数默认输出os.getcwd()系统当前路径下内容。
3.2，获取路径下目录及文件清单（包括路径）
3.3，分割路径和文件名
3.4，分割文件名和扩展名
3.5，获取文件大小（字节数）
3.6 分割路径和文件名
3.7 分割文件名和扩展名
3.8 分割驱动器名和路径（用在windows下）
3.9，去掉路径后端文件名或目录（就是os.path.split(path)的第一个元素）
3.10 连接两个或更多的路径名
3.11 获取列表中公共最长路径
3.12 获取规范化的绝对路径
3.13 判断路径是否是绝对路径
3.14 判断路径是否是目录
3.15 判断路径是否是文件
3.16 遍历目录中指定扩展名文件

4.1 新建目录
4.2 新建多级目录
4.3 复制目录
4.4 目录改名/移动（先移动，在改名，如重名则原路返回）
4.5 新建文件
4.6 复制文件
4.7 文件改名/移动
4.8 删除空目录
4.9 递归删除目录
4.10 删除文件（支持通配符）
4.11强制删除目录
4.12 级联删除一个目录下的所有文件，包括子目录下的文件（保留所有子目录，最终保留这个目录架构）
'''

import os, shutil, glob, sys

class FilePO():

    def __init__(self):
        pass

    # 2.3，获取上级目录路径(反斜线)，如：D:\51\python\project\PO
    def getUpPath(self):
        return (os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

    # 2.4，获取上级目录路径，如：D:/51/Python/09project
    def getUpPathSlash(self):
        return (os.path.dirname(os.path.dirname(__file__)))

    # 2.5，获取自定义上级目录路径
    def getLayerPath(self, varPath):
        # print(File_PO.getLayerPath("../../"))  # 获取上上层路径
        # print(File_PO.getLayerPath("/")) # 获取根路径
        return (os.path.abspath(os.path.join(os.getcwd(), varPath)))

    # 2.6，切换路径
    def getChdirPath(self, varPath):
        # 从当前路径切换到指定的目录
        if os.path.exists(varPath) == True:
            os.chdir(varPath)
            return os.getcwd()

    # 3.1， 获取目录清单
    def getListDir(self, varPath=None):
        # 遍历目录清单（目录或文件按照数字、字符、中文顺序排列输出）
        # 如：['001 基层健康管理平台', '101 智慧门诊', '102 家庭病床管理平台', '103 CRM', '201 UI', '301 模板', 'test.txt', '产品规划']
        # print(File_PO.getListDir(os.getcwd()))
        try:
            return(os.listdir(varPath))
        except:
            return None

    # 3.2，获取路径下目录及文件清单（包括路径）
    def getWalk(self, varPath):
        # 获取路径下所有目录及文件
        # File_PO.walk(os.getcwd())
        # 结果：
        # D:\51\python\project\PO\FilePO\11.txt
        # D:\51\python\project\PO\FilePO\FilePO.py
        # D:\51\python\project\PO\FilePO\john.docx
        # D:\51\python\project\PO\FilePO\test.txt
        # D:\51\python\project\PO\FilePO\yoyo.docx
        # D:\51\python\project\PO\FilePO\folder11\3333.txt
        # D:\51\python\project\PO\FilePO\folder3\test.txt
        # D:\51\python\project\PO\FilePO\folder4\ff\13.txt
        # D:\51\python\project\PO\FilePO\folder5\h1\新建文本文档.txt
        # D:\51\python\project\PO\FilePO\folder7\folder77\99.txt
        # D:\51\python\project\PO\FilePO\folder9\13.txt
        # D:\51\python\project\PO\FilePO\recursion\h1\h2\test.txt
        if not os.path.exists(varPath):
            return -1
        for root, dirs, names in os.walk(varPath):
            for filename in names:
                print(os.path.join(root, filename))  # 路径和文件名连接构成完整路径

    # 3.3，获取文件清单
    def getListFile(self, varFilePath='*.*' ):
        # 获取指定路径下的文件清单，如 所有doc文件, * 所有文件
        # print(File_PO.getListFile("D:\work\\*.doc"))
        # print(File_PO.getListFile("D:\work\\*.*"))
        list1 = []
        if varFilePath == '*':
            varFilePath = '*.*'
        for name in glob.glob(varFilePath):
            list1.append(name)
        return list1

    # 3.5，获取文件大小
    def getFileSize(self, varFilePath):
        # 获取文件大小(字节数)
        # 如  print(File_PO.getFileSize("D:\work\\test.txt")) ，结果 71
        try:
            return (os.path.getsize(varFilePath))
        except:
            None

    # 3.16 遍历目录中指定扩展名文件(级联目录)
    def getfilelist(self, varPathList, varPath, EXTEND):
        file = os.listdir(varPath)
        for im_name in file:
            if os.path.isdir(os.path.join(varPath, im_name)):
                self.getfilelist(varPathList, os.path.join(varPath, im_name), EXTEND)
            else:
                # 根据后缀判断是否为图片
                ext = os.path.splitext(im_name)[1]
                if ext in EXTEND:
                    name = os.path.join(varPath, im_name)
                    filelist.append(name)



    ''' 操作目录和文件 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''

    # 新建目录
    def newFolder(self, varFolderPath):
        # 新建目录，自动在当前路径下新建目录，如果存在则忽略（不覆盖）
        # File_PO.newFolder(os.getcwd() + "/" + "folder3")  # 在当前目录下创建 folder3 目录
        try:
            os.mkdir(varFolderPath)
        except:
            return None

    # 新建多级目录
    def newLayerFolder(self, varLayerFolderPath):
        # 新建多级目录，如果目录路径不存在，则新建路径目录
        # File_PO.newLayerFolder(os.getcwd() + "/folder5/h1/h2")  # 新建 /folder5/h1/h2 三层目录，目录存在则忽略
        try:
            if not os.path.exists(varLayerFolderPath):
                os.makedirs(varLayerFolderPath)
        except:
            return None

    # 复制目录
    def copyFolder(self, srcFolderPath, tgtFolderPath, varMode='i'):
        # 复制目录（同级目录）
        # 1，目标目录不存在，将源目录所有内容（文件和子目录）进行复制。
        # 2，目标目录存在，选择性覆盖或忽略。  w = 覆盖， i = 忽略
        # File_PO.copyFolder(os.getcwd() + "/folder3", os.getcwd() + "/folder11")  //将 folder3 复制成 folder11 , 如果folder6原本存在，则覆盖
        # File_PO.copyFolder(os.getcwd() + "/folder3", os.getcwd() + "/folder6", 'w')  //将 folder3 复制成 folder6 , 如果folder6原本存在，则忽略
        try:
            if not os.path.exists(tgtFolderPath):
                shutil.copytree(srcFolderPath, tgtFolderPath)
            else:
                if varMode == 'w':
                    shutil.rmtree(tgtFolderPath)  # 强制删除目录
                    shutil.copytree(srcFolderPath, tgtFolderPath)
        except:
            return None

    # 目录改名
    def renameFolder(self, srcFolder, tgtFolder):
        # 目录改名
        # File_PO.moveFolder(os.getcwd() + "/folder3", os.getcwd() + "/folder9")  # 改名，将 folder3 改名为 folder9
        try:
            os.rename(srcFolder, tgtFolder)
        except:
            return None

    # 新建文件
    def newFile(self, varPath, name, text=None):
        # 新建文件，在指定路径目录下新建文件及内容
        # File_PO.newFile(os.getcwd() + '/folder3', '13.txt', 'hello,john\ntest测试一下')  #  在 D:\51\python\project\PO\FilePO\folder3 目录下新建文件 13.txt, 并写入 hello,john\ntest测试一下
        # File_PO.newFile(os.getcwd() + "/folder5",'16.txt')  # 在 folder5目录下新建16.txt空文件，如果 folder5目录不存在，则自动新建目录
        try:
            if not os.path.exists(varPath):
                os.makedirs(varPath)
            # else:
            #     # shutil.rmtree(varPath)
            #     os.makedirs(varPath)
            file = open(varPath + "/" + name, 'w')
            file.write(text)  # 写入内容信息
            file.close()
        except:
            None

    # 复制文件
    def copyFile(self, srcFilePath, tgtFilePath, varMode='i'):
        # 复制文件，支持文件另存为。
        # File_PO.copyFile(os.getcwd() + "/folder9/13.txt", os.getcwd() + "/folder7/77.txt")  # 将 folder9 下 13.txt 复制到 folder7 下，并改名为 77.txt
        # File_PO.copyFile(os.getcwd() + "/folder9/13.txt", os.getcwd() + "/folder7/77.txt")  # 目标文件已存在，则忽略
        # File_PO.copyFile(os.getcwd() + "/folder9/13.txt", os.getcwd() + "/folder7/77.txt", 'w')  # 目标目录已存在，则覆盖（w = 覆盖）
        try:
            if os.path.exists(tgtFilePath):
                if varMode == 'w':
                    os.remove(tgtFilePath)
                    shutil.copyfile(srcFilePath, tgtFilePath)
            else:
                shutil.copyfile(srcFilePath, tgtFilePath)
        except:
            return None

    # 文件改名
    def renameFile(self, srcFile, tgtFile):
        # 文件改名/移动
        # File_PO.renameFile(os.getcwd() + "/folder7/77.txt", os.getcwd() + "/folder7/88.txt")
        # File_PO.renameFile(os.getcwd() + "/folder7/88.txt", os.getcwd() + "/folder7/folder77/99.txt")  # 将 folder7 下 88.txt 改名为 99.txt,并移动到 folder77目录下
        try:
            os.rename(srcFile, tgtFile)
        except:
            return None

    # 删除空目录
    def delEmptyFolder(self, varFolderPath):
        # # 删除空目录
        # File_PO.delEmptyFolder(os.getcwd() + "/eee")
        try:
            os.rmdir(varFolderPath)
        except:
            return None

    # 删除递归目录
    def delLayerFolder(self, varFolderPath):
        # 删除递归目录（只删除空目录）
        # File_PO.newFolder(os.getcwd(), "recursion")  # 在当前目录下创建 recursion 目录
        # File_PO.newLayerFolder(os.getcwd() + "/" + "recursion", "\h1\h2")  # 在 recursion 目录中新建\h1\h2 二层目录。
        # File_PO.delLayerFolder(os.getcwd() + "/" + "recursion/h1/h2")  #  recursion/h1/h2 这3个都是空目录，递归删除了3个目录。
        # File_PO.delLayerFolder(os.getcwd() + "/" + "recursion/h1/h2")  # recursion下有文件，递归删除h1和h2目录。
        # File_PO.delLayerFolder(os.getcwd() + "/" + "recursion/h1/h2")  # h2下有文件，三个目录都没有被删除。
        try:
            os.removedirs(varFolderPath)
        except:
            return None

    # 强制删除目录
    def deltreeFolder(self, varFolder):
        # 强制删除目录
        # File_PO.deltreeFolder(os.getcwd() + "/" + "folder5")
        try:
            shutil.rmtree(varFolder)
        except:
            return None

    # 删除文件
    def delFile(self, varFilePath):
        # 删除文件
        # File_PO.delFile(os.getcwd() + "/filepo/filepo2/13.txt")
        list1 = []
        try:
            if '*.' in varFilePath:
                list1 = File_PO.getListFile(varFilePath)
                for i in range(len(list1)):
                    os.remove(list1[i])
            else:
                os.remove(varFilePath)
        except:
            return None

    # 级联删除一个目录下的所有文件，包括子目录下的文件（保留所有子目录，最终保留这个目录架构）
    def delCascadeFiles(self, varPath):
        try:
            ls = os.listdir(varPath)
            for i in ls:
                c_path = os.path.join(varPath, i)
                if os.path.isdir(c_path):
                    self.delCascadeFiles(c_path)
                else:
                    os.remove(c_path)
        except:
            return None

if __name__ == "__main__":

    File_PO = FilePO()

    # print("1.1，获取环境变量信息".center(100, "-"))
    # print(os.environ.keys())
    # # # KeysView(environ({'ALLUSERSPROFILE': 'C:\\ProgramData', 'APPDATA': 'C:\\Users\\ZY\\AppData\\Roaming', 'CLASSPATH': '.;C:\\Program Files\\JAVA\\jdk1.8.0_211/lib/dt.jar;C:\\Program Files\\JAVA\\jdk1.8.0_211/lib/tools.jar;', 'COMMONPROGRAMFILES': 'C:\\Program Files\\Common Files', 'COMMONPROGRAMFILES(X86)': 'C:\\Program Files (x86)\\Common Files', 'COMMONPROGRAMW6432': 'C:\\Program Files\\Common Files', 'COMPUTERNAME': 'DESKTOP-EOCO1V0', 'COMSPEC': 'C:\\Windows\\system32\\cmd.exe', 'DRIVERDATA': 'C:\\Windows\\System32\\Drivers\\DriverData', 'FPS_BROWSER_APP_PROFILE_STRING': 'Internet Explorer', 'FPS_BROWSER_USER_PROFILE_STRING': 'Default', 'HOMEDRIVE': 'C:', 'HOMEPATH': '\\Users\\ZY', 'JAVA_HOME': 'C:\\Program Files\\JAVA\\jdk1.8.0_211', 'JMETER_HOME': 'C:\\apache-jmeter-5.1.1', 'LOCALAPPDATA': 'C:\\Users\\ZY\\AppData\\Local', 'LOGONSERVER': '\\\\DESKTOP-EOCO1V0', 'MYSQL_HOME': 'c:\\mysql-8.0.18-winx64', 'NUMBER_OF_PROCESSORS': '4', 'ONEDRIVE': 'C:\\Users\\ZY\\OneDrive', 'OS': 'Windows_NT', 'PATH': 'C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\javapath;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\;C:\\Windows\\System32\\OpenSSH\\;C:\\Program Files (x86)\\NVIDIA Corporation\\PhysX\\Common;C:\\Program Files\\NVIDIA Corporation\\NVIDIA NvDLISR;C:\\Program Files\\Git\\cmd;C:\\Program Files (x86)\\Windows Kits\\8.1\\Windows Performance Toolkit\\;C:\\Python38\\Scripts\\;C:\\Python38\\;C:\\Users\\ZY\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Users\\ZY\\AppData\\Local\\Programs\\Fiddler;C:\\Program Files\\JetBrains\\PyCharm 2018.3.5\\bin;;d:\\myLNK;C:\\mysql-8.0.18-winx64\\bin;', 'PATHEXT': '.exe;.doc;.txt;.xlsx;.lnk;.url;.bat;', 'PROCESSOR_ARCHITECTURE': 'AMD64', 'PROCESSOR_IDENTIFIER': 'Intel64 Family 6 Model 158 Stepping 9, GenuineIntel', 'PROCESSOR_LEVEL': '6', 'PROCESSOR_REVISION': '9e09', 'PROGRAMDATA': 'C:\\ProgramData', 'PROGRAMFILES': 'C:\\Program Files', 'PROGRAMFILES(X86)': 'C:\\Program Files (x86)', 'PROGRAMW6432': 'C:\\Program Files', 'PSMODULEPATH': 'C:\\Program Files\\WindowsPowerShell\\Modules;C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\Modules', 'PUBLIC': 'C:\\Users\\Public', 'PYCHARM': 'C:\\Program Files\\JetBrains\\PyCharm 2018.3.5\\bin;', 'PYCHARM_HOSTED': '1', 'PYCHARM_MATPLOTLIB_PORT': '53639', 'PYTHONIOENCODING': 'UTF-8', 'PYTHONPATH': 'D:\\51\\python\\project;C:\\Program Files\\JetBrains\\PyCharm 2018.3.5\\helpers\\pycharm_matplotlib_backend', 'PYTHONUNBUFFERED': '1', 'SESSIONNAME': 'Console', 'SYSTEMDRIVE': 'C:', 'SYSTEMROOT': 'C:\\Windows', 'TEMP': 'C:\\Users\\ZY\\AppData\\Local\\Temp', 'TESSDATA_PREFIX': 'C:\\Program Files (x86)\\Tesseract-OCR\\tessdata', 'TMP': 'C:\\Users\\ZY\\AppData\\Local\\Temp', 'USERDOMAIN': 'DESKTOP-EOCO1V0', 'USERDOMAIN_ROAMINGPROFILE': 'DESKTOP-EOCO1V0', 'USERNAME': 'ZY', 'USERPROFILE': 'C:\\Users\\ZY', 'VS140COMNTOOLS': 'C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\Common7\\Tools\\', 'WINDIR': 'C:\\Windows'}))
    # print(os.environ['HOMEPATH'])  # \Users\ZY   //当前用户主目录。
    # print(os.environ['TEMP'])  # C:\Users\ZY\AppData\Local\Temp   //# 临时目录路径。
    # print(os.environ['PATHEXT'])  # .exe;.doc;.txt;.xlsx;.lnk;.url;.bat;   //# 可执行文件。
    # print(os.environ['SYSTEMROOT'])  # C:\Windows  //# 系统主目录。
    # print(os.environ['LOGONSERVER'])  # \\DESKTOP-EOCO1V0  /# 机器名。
    # print(os.getenv("JAVA_HOME"))  # C:\Program Files\JAVA\jdk1.8.0_211
    #
    #
    # print("1.2，添加路径到系统环境变量".center(100, "-"))
    # sys.path.append("D:\\51\\python\\project\\PO")
    # print(sys.path)
    #
    #
    # print("1.3，根据环境变量的值替换path".center(100, "-"))
    # # 1.3 os.path.expandvars(path)，根据环境变量的值替换path中包含的”$name”和”${name}”
    # os.environ['testPATH'] = 'D:/thunder'
    # path = '$testPATH/train/13.png'
    # print(os.path.expandvars(path))  # D:/thunder/train/13.png
    #
    #
    # print("2.1 获取当前路径（反斜线）".center(100, "-"))
    # print(os.getcwd())  # D:\51\python\project\PO\FilePO
    #
    # print("2.2 获取当前路径".center(100, "-"))
    # print(os.path.dirname(__file__))  # D:/51/python/project/PO/FilePO
    #
    # print("2.3 获取上层目录路径（反斜线）".center(100, "-"))
    # print(File_PO.getUpPath())  # D:\51\python\project\PO
    #
    # print("2.4 获取上层目录路径".center(100, "-"))
    # print(File_PO.getUpPathSlash())  # D:/51/python/project
    #
    # print("2.5 获取自定义上层目录路径".center(100, "-"))
    # print(File_PO.getLayerPath("../../"))  # D:\51\python\project
    # print(File_PO.getLayerPath("/"))  # D:\
    #
    # print("2.6 切换路径，影响os.getcwd()".center(100, "-"))
    # print(File_PO.getChdirPath("D:\\51\\python"))  # D:\51\python
    # print(os.getcwd())  # D:\51\python
    #
    #
    # print("3.1 获取路径下目录及文件清单（排列顺序按照数字、字符、中文输出）".center(100, "-"))
    # print(File_PO.getListDir("D:\\51\\python\\project"))  # ['.git', '.gitignore', '.idea', 'instance', 'lib', 'PO', 'PO.7z', 'README.md', 'script', 'test', 'venv']
    # print(File_PO.getListDir())  # ['00doc', 'install', 'project', 'project2020.03.20.7z', 'project20200319.7z', 'Python27.zip']  //默认输出os.getcwd()系统当前路径下内容。
    #
    # print("3.2 获取路径下目录及文件清单（包括路径）".center(100, "-"))
    # File_PO.getWalk(os.getcwd())
    # # # 结果：
    # # # D:\51\python\project\PO\FilePO\11.txt
    # # # D:\51\python\project\PO\FilePO\FilePO.py
    # # # D:\51\python\project\PO\FilePO\john.docx
    # # # D:\51\python\project\PO\FilePO\test.txt
    # # # D:\51\python\project\PO\FilePO\yoyo.docx
    # #
    #
    # print("3.3 获取文件清单".center(100, "-"))
    # print(File_PO.getChdirPath("D:\\51\\python\\project\\PO\\FilePO"))  # 切换当前路径 os.getcwd()
    # print(File_PO.getListFile("*.txt"))  # ['john.docx', 'yoyo.docx']   //获取当前路径下所有docx文件
    # print(File_PO.getListFile())  # 获取当前路径下所有文件名清单
    #
    #
    # print("3.4 获取路径中的文件名".center(100, "-"))
    # print(os.path.basename("D:\work\\test.txt"))  # test.txt
    # print(os.path.basename('W:\python_File'))  # python_File
    # print(os.path.basename('D:\\51\\python\\project\\PO\\123.txt'))  # 123.txt
    # print(os.path.basename('/home/ubuntu/python_coding/split_func/split_function.py'))  # split_function.py
    #
    # print("3.5 获取文件大小（字节数）".center(100, "-"))
    # print(File_PO.getFileSize("D:\\51\\python\\project\\PO\\FilePO\\test.txt"))  # 46
    #
    # print("3.6 分割路径和文件名".center(100, "-"))
    # print(os.path.split('D:\\51\\python\\project\\PO\\123.txt'))  # ('D:\\51\\python\\project\\PO', '123.txt')
    # varPath, varFile = os.path.split("E:/lpthw/zedshaw/ex19.py")
    # print(varPath)  # E:/lpthw/zedshaw
    # print(varFile)  # ex19.py
    #
    # print("3.7 分割文件名和扩展名".center(100, "-"))
    # varPath, varEXT = os.path.splitext('/home/ubuntu/python_coding/split_func/split_function.py')
    # print(varPath)  # /home/ubuntu/python_coding/split_func/split_function
    # print(varEXT)  # .py
    #
    # print("3.8 分割驱动器名和路径（用在windows下）".center(100, "-"))
    # print(os.path.splitdrive('D:\\51\\python\\project\\PO\\123.txt'))  # ('D:', '\\51\\python\\project\\PO\\123.txt')
    #
    # print("3.9 去掉路径后端文件名或目录（就是os.path.split(path)的第一个元素）".center(100, "-"))
    # print(os.path.dirname('W:\python_File'))  # W:\    //去掉目录 python_File
    # print(os.path.dirname('D:\\51\\python\\project\\PO\\123.txt'))  # D:\51\python\project\PO   //去掉文件 123.txt
    # print(os.path.dirname('/home/ubuntu/python_coding/split_func/split_function.py'))  # /home/ubuntu/python_coding/split_func   //去掉文件 split_function.py
    #
    # print("3.10 连接两个或更多的路径名".center(100, "-"))
    # print(os.path.join(os.getcwd(), "ddd"))  # D:\51\python\project\PO\FilePO\ddd
    # print(os.path.join(os.getcwd(), "ddd", "eee", 'fff'))  # D:\51\python\project\PO\FilePO\ddd\eee\fff
    # print(os.path.join(os.getcwd(), "/ddd"))  # D:/ddd
    # print(os.path.join(os.getcwd(), "\ddd"))  # D:\ddd
    # print(os.path.join(os.getcwd(), "\ddd", "eee"))  # D:\ddd\eee
    # print(os.path.join(os.getcwd(), "\ddd", "/eee"))  # D:/eee
    #
    # print("3.11 获取列表中公共最长路径".center(100, "-"))
    # print(os.path.commonprefix(['/home/td', '/home/td/ff/a/b/d/c', '/home/td/fff']))  # /home/td
    #
    # print("3.12 获取规范化的绝对路径".center(100, "-"))
    # print(os.path.abspath('test.csv'))  # D:\51\python\test.csv
    #
    # print("3.13 判断路径是否是绝对路径".center(100, "-"))
    # print(os.path.isabs("D:\\51\\python"))  # True
    # print(os.path.isabs("\abc"))  # False   , 控制台中输入'\abc' 返回 '\x07bc'
    # print(os.path.isabs("\sbc"))  # True   , 控制台中输入'\sbc' 返回 '\\sbc', 在Windows系统上，以 \\ 开头的字符串，os.path.isabs就会返回True
    # print(os.path.isabs("/sbc"))  # True    在window系统下，如果输入的字符串以" / "开头，os.path.isabs()就会返回True
    #
    # print("3.14 判断路径是否是目录".center(100, "-"))
    # print(os.path.isdir(""))  # False
    # print(os.path.isdir("d:\\51\\python"))  # True
    #
    # print("3.15 判断路径是否是文件".center(100, "-"))
    # print(os.path.isfile("D:\\51\\python\\project\\PO\\FilePO\\test.txt"))  # True
    #
    # print("3.16 遍历目录中指定扩展名文件".center(100, "-"))
    # filelist = []
    # File_PO.getfilelist(filelist, "../test/upload", [".png", ".jpg"])
    # print(filelist)
    #
    #
    #
    # print("4.1 新建目录".center(100, "-"))
    # # File_PO.newFolder(os.getcwd() + "/filepo/")  # 在当前目录下创建 filepo 目录
    # # File_PO.newFolder(os.getcwd() + "/filepo/filepo1")  # 在当前目录下创建 filepo1 目录
    # # File_PO.newFolder(os.getcwd() + "/filepo/filepo2")
    # # File_PO.newFolder(os.getcwd() + "/filepo/filepo3")
    #
    # print("4.2 新建多级目录".center(100, "-"))
    # # File_PO.newLayerFolder(os.getcwd() + "/filepo/filepo2/h1/h2")  # 新建 filepo1/h1/h2 三层目录，目录存在则忽略
    # # File_PO.newLayerFolder(os.getcwd() + "/filepo/filepo3/h3/h4")
    #
    # print("4.3 复制目录".center(100, "-"))
    # # File_PO.copyFolder(os.getcwd() + "/filepo/filepo1", os.getcwd() + "/filepo/filepo2")  # 如果目标目录已存在则忽略。
    # # File_PO.copyFolder(os.getcwd() + "/filepo/filepo1", os.getcwd() + "/filepo/filepo3", 'w')  # 如果目标目录已存在则覆盖（w = 覆盖）。
    #
    # print("4.4 目录改名/移动（先移动，在改名，如重名则原路返回）".center(100, "-"))
    # # File_PO.renameFolder(os.getcwd() + "/filepo/filepo1", os.getcwd() + "/filepo/filepo4")  # 将 filepo1 改名为 filepo4
    # # File_PO.renameFolder(os.getcwd() + "/filepo/filepo3", os.getcwd() + "/filepo/filepo2/h1/ff")  # 将 filepo3 移动到 /filepo2/h1/ 下，并改名ff
    #
    # print("4.5 新建文件".center(100, "-"))
    # # File_PO.newFile(os.getcwd() + '/filepo/filepo4', '13.txt', 'hello,john\ntest测试一下')  # 在 filepo4 目录下新建文件 13.txt, 并写入 hello,john\ntest测试一下
    # # File_PO.newFile(os.getcwd() + "/filepo/filepo4", '16.txt')  # 在 filepo4 目录下新建 16.txt 空文件，如果目录不存在则自动新建目录
    # # File_PO.newFile(os.getcwd() + "/filepo/filepo2", '100.txt')
    #
    # print("4.6 复制文件".center(100, "-"))
    # # File_PO.copyFile(os.getcwd() + "/filepo/filepo4/13.txt", os.getcwd() + "/filepo/filepo2/13.txt")  # 将 filepo4/13.txt  复制到 filepo2/13.txt
    # # File_PO.copyFile(os.getcwd() + "/filepo/filepo4/13.txt", os.getcwd() + "/filepo/filepo2/h1/77.txt")  # 将 folder9 下 13.txt 复制到 folder7 下，并改名为 77.txt
    # # File_PO.copyFile(os.getcwd() + "/filepo/filepo4/16.txt", os.getcwd() + "/filepo/filepo2/h1/77.txt")  # 目标文件已存在，则忽略
    # # File_PO.copyFile(os.getcwd() + "/filepo/filepo4/16.txt", os.getcwd() + "/filepo/filepo2/13.txt", 'w')  # 目标目录已存在，则覆盖（w = 覆盖）
    #
    # print("4.7 文件改名/移动".center(100, "-"))
    # # File_PO.renameFile(os.getcwd() + "/filepo/filepo4/16.txt", os.getcwd() + "/filepo/filepo4/22.txt")
    # # File_PO.renameFile(os.getcwd() + "/filepo/filepo4/13.txt", os.getcwd() + "/filepo/filepo2/h1/ff/99.txt")  # 将 folder7 下 88.txt 改名为 99.txt,并移动到 folder77目录下
    #
    # print("4.8 删除空目录".center(100, "-"))
    # # File_PO.delEmptyFolder(os.getcwd() + "/filepo/filepo2/h1")  # 目录不为空，无法删除
    # # File_PO.delEmptyFolder(os.getcwd() + "/filepo/filepo2/h1/h2")  # 删除空目录
    #
    # print("4.9 递归删除目录".center(100, "-"))
    # # File_PO.newFolder(os.getcwd() + "/filepo/recursion")  # 在当前目录下创建 recursion 目录
    # # File_PO.newLayerFolder(os.getcwd() + "/filepo/recursion/h1/h2")  # 在 recursion 目录中新建\h1\h2 二层目录。
    # # File_PO.newLayerFolder(os.getcwd() + "/filepo/recursion/h3/h4")  # 在 recursion 目录中新建\h1\h2 二层目录。
    # # File_PO.newFile(os.getcwd() + "/filepo/recursion/h1/h2", '16.txt')
    # # File_PO.delLayerFolder(os.getcwd() + "/recursion/h1/h2")  # h2下有文件，/recursion/h1/h2 三个目录都没有被删除。
    # # File_PO.renameFile(os.getcwd() + "/filepo/recursion/h1/h2/16.txt", os.getcwd() + "/filepo/recursion/11.txt")
    # # File_PO.delLayerFolder(os.getcwd() + "/filepo/recursion/h1/h2")  # recursion下有文件，递归删除h1和h2目录。
    # # File_PO.delFile(os.getcwd() + "/filepo/recursion/11.txt")
    # # File_PO.delLayerFolder(os.getcwd() + "/filepo/recursion/h3/h4")  #  recursion/h1/h2 这3个都是空目录，递归删除了3个目录。
    #
    # print("4.10 删除文件（支持通配符）".center(100, "-"))
    # # File_PO.delFile(os.getcwd() + "/filepo/filepo2/13.txt")  # 删除1个文件
    # # File_PO.delFile(os.getcwd() + "/filepo/filepo2/*.txt")  # 批量删除文件
    # # File_PO.delFile(os.getcwd() + "/filepo/filepo2/*.*")  # 删除所有文件
    #
    # print("4.11 强制删除目录".center(100, "-"))
    # # File_PO.deltreeFolder(os.getcwd() + "/filepo")
    #
    # print("4.12 级联删除一个目录下的所有文件，包括子目录下的文件（保留所有子目录，最终保留这个目录架构）".center(100, "-"))
    # # File_PO.delCascadeFiles("d:/test1")

