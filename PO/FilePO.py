# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2017-10-26
# Description   : 文件对象层 (获取路径、目录和文件信息、操作文件、系统级别)
# *********************************************************************
"""
3，目录与文件
3.2 获取路径下目录及文件清单（包括路径） getWalk()

3.16 遍历目录中指定扩展名文件
3.17 判断文件的存在、读、写、执行
	文件是否存在 print(os.access("d:\\a.jpg", os.F_OK))
	文件是否可读 print(os.access("d:\\a.jpg", os.R_OK))
	文件是否可以写入 print(os.access("d:\\a.jpg", os.W_OK))
	文件是否可以执行  print(os.access("d:\\a.jpg", os.X_OK))
3.18 判断文件类型 isFileType()

4，操作目录文件
4.3 copyFolder  复制目录
4.5 newFile  新建文件
4.6 copyFile  复制文件
4.7 renameFile  文件改名/移动
4.12  delCascadeFiles  级联删除一个目录下的所有文件，包括子目录下的文件（保留所有子目录，最终保留这个目录架构）

"""

import os, shutil, glob, sys, pathlib, mimetypes

class FilePO:

    def __init__(self):
        pass


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

    def newFile(self, varPath, varFile, text=""):

        '''
        新建文件 (自动创建目录、文件、内容)
        # File_PO.newFile(os.getcwd(), '13.txt')  #  在当前目录下新建13.txt文件
        # File_PO.newFile(os.getcwd(), '13.txt', '你好')  #  在当前目录下新建13.txt文件，并写入"你好"
        # File_PO.newFile(os.getcwd() + "/folder5",'16.txt')  # 在当前目录下的folder5目录下新建16.txt空文件
        '''

        if not os.path.exists(varPath):
            os.makedirs(varPath)
        file = open(varPath + "/" + varFile, "w")
        file.write(text)
        file.close()


    def copyFolder(self, srcFolderPath, tgtFolderPath, varMode="i"):
        # 复制目录
        # 1，目标目录不存在，则正常复制。
        # 2，目标目录存在，参数varMode = w 进行覆盖。
        # File_PO.copyFolder("/Users/linghuchong/Downloads/1", "/Users/linghuchong/Downloads/51/2")  # 如果目标目录已存在，则不覆盖。
        # File_PO.copyFolder("/Users/linghuchong/Downloads/1", "/Users/linghuchong/Downloads/51/2", 'w')  # 如果目标目录已存在，则覆盖。

        if not os.path.exists(tgtFolderPath):
            shutil.copytree(srcFolderPath, tgtFolderPath)
        else:
            if varMode == "w":
                shutil.rmtree(tgtFolderPath)  # 强制删除目录
                shutil.copytree(srcFolderPath, tgtFolderPath)

    def copyFile(self, srcFilePath, tgtFilePath, varMode="i"):
        # 复制文件
        # File_PO.copyFile(os.getcwd() + "/folder9/13.txt", os.getcwd() + "/folder7/77.txt")  # 将 folder9 下 13.txt 复制到 folder7 下，并改名为 77.txt
        # File_PO.copyFile(os.getcwd() + "/folder9/13.txt", os.getcwd() + "/folder7/77.txt")  # 目标文件已存在，则忽略
        # File_PO.copyFile(os.getcwd() + "/folder9/13.txt", os.getcwd() + "/folder7/77.txt", 'w')  # 目标目录已存在，则覆盖（w = 覆盖）
        if os.path.exists(tgtFilePath):
            if varMode == "w":
                os.remove(tgtFilePath)
                shutil.copyfile(srcFilePath, tgtFilePath)
        else:
            shutil.copyfile(srcFilePath, tgtFilePath)

    def removeFile(self, varPath, varFile):

        '''
        删除文件
        :param varFilePath:
        :return:
        File_PO.removeFile(os.getcwd() + "/filepo/filepo2", "13.txt")  # 删除1个文件
        File_PO.removeFile(os.getcwd() + "/filepo/filepo2", "*.txt")  # 批量删除文件
        File_PO.removeFile(os.getcwd() , "*.*")  # 删除当前路径下所有文件
        '''

        list1 = []

        varFilePath = varPath + "/" + varFile

        if "*." in varFilePath:
            list1 = File_PO.getListFile(varFilePath)
            for i in range(len(list1)):
                os.remove(list1[i])
        else:
            os.remove(varFilePath)


    def delCascadeFiles(self, varPath):
        # 级联删除一个目录下的所有文件，包括子目录下的文件（保留所有子目录，最终保留这个目录架构）

        ls = os.listdir(varPath)
        for i in ls:
            c_path = os.path.join(varPath, i)
            if os.path.isdir(c_path):
                self.delCascadeFiles(c_path)
            else:
                os.remove(c_path)




if __name__ == "__main__":

    File_PO = FilePO()

    # print("3.16 遍历目录中指定扩展名文件".center(100, "-"))
    # filelist = []
    # File_PO.getfilelist(filelist, "../test/upload", [".png", ".jpg"])
    # print(filelist)



    # print("4.3 复制目录".center(100, "-"))
    # File_PO.copyFolder("/Users/linghuchong/Downloads/1", "/Users/linghuchong/Downloads/51/2")  # 如果目标目录已存在，则不覆盖。
    # File_PO.copyFolder("/Users/linghuchong/Downloads/1", "/Users/linghuchong/Downloads/51/2", 'w')  # 如果目标目录已存在，则覆盖。

    # print("4.6 复制文件".center(100, "-"))
    # File_PO.copyFile("/Users/linghuchong/Downloads/1.doc", "/Users/linghuchong/Downloads/2.doc")
    # File_PO.copyFile("/Users/linghuchong/Downloads/1.doc", "/Users/linghuchong/Downloads/2.doc", 'w')  # 目标目录已存在，则覆盖


    # print("4.10 删除文件（支持通配符）".center(100, "-"))
    # File_PO.removeFile(os.getcwd() + "/filepo/filepo2", "13.txt")  # 删除1个文件
    # File_PO.removeFile(os.getcwd() + "/filepo/filepo2", "*.txt")  # 批量删除文件
    # File_PO.removeFile(os.getcwd(), "*.*")  # 删除当前路径下所有文件
    # File_PO.removeFile('', "/Users/linghuchong/Downloads/51/Python/project/PO/captcha.gif")  # 删除当前路径下所有文件



    # print("4.12 级联删除一个目录下的所有文件，包括子目录下的文件（保留所有子目录，最终保留这个目录架构）".center(100, "-"))
    # File_PO.delCascadeFiles("d:/test1")
