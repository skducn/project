# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2017-10-26
# Description   : 文件对象层 (获取路径、目录和文件信息、操作文件、系统级别)
# *********************************************************************

import os, sys
import shutil

class FilePO():

    def __init__(self):
        pass

    ''' 环境变量及路径 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''

    def getEnv(self, name):
        # 返回当前环境变量值，如 'JAVA_HOME'
        # print(File_PO.getEnv('JAVA_HOME'))
        return (os.getenv(name))

    def addPath(self, newPath):
        # 添加 路径到系统环境变量中，返回列表！
        # print(File_PO.addPath("D:\\51\\python\\project\\PO"))
        sys.path.append(newPath)
        return sys.path

    def getCurrentPath(self):
        # 返回当前路径，如 E:\51\Python\09project\common
        return os.getcwd()

    def getCurrentPath_backslash(self):
        # 返回当前路径（注意是反斜杠），如：D:/51/Python/09project/common
        return os.path.dirname(__file__)

    def getUpPath(self):
        # 返回上一级目录路径，如：D:\51\Python\09project
        return (os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
        # print(os.path.abspath(os.path.dirname(os.getcwd())))  #  如：D:\51\Python\09project

    def getUpPath_backslash(self):
        # 返回上一级目录路径（注意是反斜杠），如：D:/51/Python/09project
        return (os.path.dirname(os.path.dirname(__file__)))

    def getLayerPath(self, varPath):
        # 返回到自定义的上上一级目录路径
        # print(File_PO.getUp2Path("../../"))
        # print(File_PO.getUp2Path("/"))
        return (os.path.abspath(os.path.join(os.getcwd(), varPath)))

    def getChdirPath(self, varNewPath):
        # 从当前目录 切换到 指定的目录（如：d:\work）
        # print(File_PO.getChdirPath("FilePO\\201 UI"))
        if os.path.exists(varNewPath) == True:
            # 路径是否存在
            os.chdir(varNewPath)
            return os.getcwd()

    ''' 操作目录和文件 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''

    def getPathContent_noPath_list(self, varPath):
        # 以列表方式遍历目录里内容，依照数字、字符、中文顺序排列，
        # 如：['001 基层健康管理平台', '101 智慧门诊', '102 家庭病床管理平台', '103 CRM', '201 UI', '301 模板', 'test.txt', '产品规划']
        # print(File_PO.getPathContent_List("FilePO"))
        try:
            return(os.listdir(varPath))
        except:
            return("error")


    def getPathLastFolder_tuple(self, varPath):
        # # 以元组方式返回一个路径和最后一个目录名，如 ('D:\\51\\python\\project', 'PO')
        # print(File_PO.getContent_tuple(File_PO.getCurrentPath()))
        return (os.path.split(varPath))

    def getPathFileExtension_tuple(self, varPath):
        # 分离扩展名，如
        # print(File_PO.getPathLastName("D:\work\\test.txt"))  # ('FilePO\\test', '.txt')
        return (os.path.splitext(varPath))

    def getPathPath(self, pathFile):
        # # 获取文件路径中的路径名（包括盘符）， 如 print(File_PO.getPathPath("D:\\51\\python\\project\\PO\\123.txt"))  # D:\51\python\project\PO
        return (os.path.dirname(pathFile))

    def getPathFile(self, pathFile):
        # 获取文件路径中的文件名， 如print(File_PO.getPathFile("D:\work\\test.txt"))  # test.txt
        return (os.path.basename(pathFile))

    def isFolder(self, varPath):
        # 是否是目录，返回 Ture or False
        return (os.path.isdir(varPath))

    def isAbs(self, varPath):
        # 是否是绝对路径，返回 Ture or False
        return (os.path.isabs(varPath))

    def isFile(self, varPath):
        # # 是否是文件，返回Ture or False , 如 print(File_PO.isFile("D:\work\\test.txt"))
        return (os.path.isfile(varPath))

    def getFileAttr(self, filePath):
        # # 获取文件属性， 如 print(File_PO.getFileAttr("D:\work\\test.txt"))
        # os.stat_result(st_mode=33206, st_ino=6755399441380345, st_dev=2320466551, st_nlink=1, st_uid=0, st_gid=0, st_size=0, st_atime=1548830919, st_mtime=1548830919, st_ctime=1548830919)
        return (os.stat(filePath))

    def getFileSize(self, filePath):
        # 获取文件大小(字节数)，如  print(File_PO.getFileSize("D:\work\\test.txt"))
        return (os.path.getsize(filePath))  # 71

    def getPathAllFile_list(self, filePath ):
        # 遍历目录获取指定的文件，如 所有doc文件, * 所有文件
        # print(File_PO.getAllFile_list("D:\work\\*.doc"))
        # print(File_PO.getPathAll_list("D:\work\\*"))
        import glob
        list1 = []
        for name in glob.glob(filePath):
            list1.append(name)
        return list1

    def getDeepPath(self, l_path):
        # 返回所有path共有的最深的路径
        # print(File_PO.getDeepPath(['e:\\tmp\\a','e:\\tmp\\b','e:\\tmp\b\\b4']))  # e:\tmp
        # print(File_PO.getDeepPath(['/home/td','/home/td/ff','/home/td/fff']))  # /home/td
        return (os.path.commonprefix(l_path))


    def newFile(self, varPath, name, text):
        # 创建文件
        # File_PO.newFile("D:\work", '11.txt', 'hello,python')
        if not os.path.exists(varPath):  # 判断当前路径目录是否存在，不存在则自动创建文件夹
            os.makedirs(varPath)
        # else:
        #     # shutil.rmtree(varPath)
        #     os.makedirs(varPath)
        file = open(varPath + "\\" + name, 'w')
        file.write(text)  # 写入内容信息
        file.close()

    def newLayerFolder(self, varPath, layerFolder):
        # 创建多级目录，如在 d:\work下创建 h1\h2目录
        # File_PO.newFolder("D:\work", "\h1\h2")
        try:
            os.makedirs(varPath + layerFolder)
        except:
            return None

    def newFolder(self, varPath, folderName):
        # 创建目录，判断当前路径下目录是否存在，不存在则自动创建
        # 如  File_PO.newFolder("D:\work","\h3")
        try:
            os.mkdir(varPath + folderName)
        except:
            return None

    def copyFolder(self, srcFolder, newFolder):
        # 复制目录，目标newFoler目录不能存在，否则报错；复制目录包含目录里的文件和子目录。
        # 如 File_PO.copyFolder("FilePO\\h3", "FilePO2\\h5")  将 d:\work\h3 拷贝到 d:\work2\h5
        try:
            shutil.copytree(srcFolder, newFolder)
        except:
            return None

    def copyFile(self, srcFile, newFile):
        # 复制文件，将 d:\work\test.txt 复制到 d:\work\h6\91.txt
        # 如 File_PO.copyFile("FilePO\\test.txt", "FilePO\h6\\91.txt")
        try:
            shutil.copyfile(srcFile, newFile)
        except:
            return None

    def moveFolder(self, srcFolder, newFolder):
        # 移动目录（支持改名），将 h3 移动后改名为 h6
        # 如 File_PO.moveFolder("FilePO\\h3", "FilePO\\h6")
        try:
            os.rename(srcFolder, newFolder)
        except:
            return None

    def moveFile(self, srcFile, newFile):
        # 移动文件（支持改名），将 d:\work\6.txt 移动到 d:\work\h1\61.txt
        # 如 File_PO.moveFile("FilePO\\6.txt", "D:\work\\h1\\61.txt")
        try:
            os.rename(srcFile, newFile)
        except:
            return None

    def delFolder(self, varPath):
        # 删除目录(为空)
        try:
            os.rmdir(varPath)
        except:
            return None

    def delLayerFolder(self, varPath):
        # 递归删除目录（目录里空的子目录一起删除）
        # 如 ：File_PO.delLayerFolder("d:\work\h4\h44")
        # 场景1: \h4 目录下没有文件且只有 \h44 一个空目录，执行命令后，删除了这2个级联目录。
        # 场景2: \h4 目录下有文件和有目录，其中 \h44 是一个空目录，执行命令后，删除\h44目录，其他\h4下的文件或目录不变。
        try:
            os.removedirs(varPath)
        except:
            return None

    def delFile(self, varFile):
        # 删除文件，如  File_PO.delFile("FilePO\\13.txt")
        try:
            os.remove(varFile)
        except:
            return None

    def deltreeFoler(self, varFolder):
        # 删除目录(强制删除所有目录)
        try:
            shutil.rmtree(varFolder)
        except:
            return None


    # *******************************************************************

    # os.path.expanduser(path)  #把path中包含的"~"和"~user"转换成用户目录
    # os.path.expandvars(path)  #根据环境变量的值替换path中包含的”$name”和”${name}”
    # os.path.getatime(path)  #返回最后一次进入此path的时间。
    # os.path.getmtime(path)  #返回在此path下最后一次修改的时间。
    # os.path.getctime(path)  #返回path的大小
    # os.path.getsize(path)  #返回文件大小，如果文件不存在就返回错误
    # os.path.isfile(path)  #判断路径是否为文件
    # os.path.isdir(path)  #判断路径是否为目录
    # os.path.islink(path)  #判断路径是否为链接
    # os.path.ismount(path)  #判断路径是否为挂载点（）
    # os.path.join(path1[, path2[, ...]])  #把目录和文件名合成一个路径
    # os.path.normcase(path)  #转换path的大小写和斜杠
    # os.path.normpath(path)  #规范path字符串形式
    # os.path.realpath(path)  #返回path的真实路径
    # os.path.relpath(path[, start])  #从start开始计算相对路径
    # os.path.samefile(path1, path2)  #判断目录或文件是否相同
    # os.path.sameopenfile(fp1, fp2)  #判断fp1和fp2是否指向同一文件
    # os.path.samestat(stat1, stat2)  #判断stat tuple stat1和stat2是否指向同一个文件
    # os.path.splitdrive(path)   #一般用在windows下，返回驱动器名和路径组成的元组
    # os.path.splitext(path)  #分割路径，返回路径名和文件扩展名的元组
    # os.path.splitunc(path)  #把路径分割为加载点与文件
    # os.path.walk(path, visit, arg)  #遍历path，进入每个目录都调用visit函数，visit函数必须有3个参数(arg, dirname, names)，dirname表示当前目录的目录名，names代表当前目录下的所有文件名，args则为walk的第三个参数
    # os.path.supports_unicode_filenames  #设置是否支持unicode路径名

if __name__ == "__main__":
    File_PO = FilePO()

    File_PO.newFolder(File_PO.getCurrentPath(), "/h3")

    # print(File_PO.addPath("D:\\51\\python\\project\\PO"))
    # print(File_PO.getCurrentPath())  # D:\51\python\project\PO
    # print(File_PO.getCurrentPath_backslash())  # D:/51/python/project/PO
    # print(File_PO.getUpPath())  # D:\51\python\project
    # print(File_PO.getUpPath_backslash())  # D:/51/python/project
    # print(File_PO.getLayerPath("../../"))  # D:\51\python
    # print(File_PO.getLayerPath("/"))  # D:\
    # print(File_PO.getChdirPath("FilePO\\Dir1"))  # D:\51\python\project\PO\FilePO\Dir1
    # print(File_PO.getPathContent_noPath_list("D:\\51\\python"))  # ['00doc', 'install', 'project', 'project2020.03.20.7z', 'project20200319.7z', 'Python27.zip']
    # print(File_PO.isFolder("D:\\51\\python"))  # True
    # print(File_PO.isAbs("D:\\51\\python"))  # True
    # print(File_PO.getPathLastFolder_tuple(File_PO.getCurrentPath()))  # ('D:\\51\\python\\project', 'PO')
    # print(File_PO.getPathFileExtension_tuple("FilePO\\test.txt"))  # ('FilePO\\test', '.txt')
    # print(File_PO.getPathPath("D:\\51\\python\\project\\PO\\FilePO\\text.txt"))  #D :\51\python\project\PO\FilePO
    # print(File_PO.getPathFile("D:\work\\test.txt"))  # test.txt
    # print(File_PO.isFile("D:\\51\\python\\project\\PO\\FilePO\\test.txt"))  # True
    # print(File_PO.getFileAttr("D:\\51\\python\\project\\PO\\FilePO\\test.txt"))  # os.stat_result(st_mode=33206, st_ino=3096224743818288, st_dev=976124684, st_nlink=1, st_uid=0, st_gid=0, st_size=46, st_atime=1584929127, st_mtime=1584929124, st_ctime=1584929038)
    # print(File_PO.getFileSize("D:\\51\\python\\project\\PO\\FilePO\\test.txt"))  # 46
    # print(File_PO.getPathAllFile_list("FilePO\\*"))  # ['FilePO\\dir1', 'FilePO\\test.txt']
    # print(File_PO.getPathAllFile_list("FilePO\\*.docx"))  # ['FilePO\\john.docx', 'FilePO\\yoyo.docx']
    # print(File_PO.getDeepPath(['e:\\tmp\\a', 'e:\\tmp\\b', 'e:\\tmp\b\\b4'])) # e:\tmp

    # 创建文件
    # File_PO.newFile("D:\work", '13.txt', 'hello,python')
    # File_PO.newLayerFolder("D:\work", "\h1\h2")
    # File_PO.newFolder("D:\work", "\h3")
    # File_PO.copyFolder("D:\work\h3", "D:\work2\h5")
    # File_PO.moveFolder("D:\work\h3", "D:\work\h6")
    # File_PO.moveFile("FilePO\\61.txt", "FilePO\\h1\\61.txt")
    # File_PO.moveFile("FilePO\\71.txt", "FilePO\h6\\81.txt")
    # File_PO.copyFile("FilePO\\test.txt", "FilePO\h6\\91.txt")
    # File_PO.delFolder("D:\work\h6")
    # File_PO.delLayerFolder("d:\work\h4\h44")
    # File_PO.deltreeFoler("FilePO\\h6")
