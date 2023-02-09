# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description:
# aiofiles：基于 asyncio，提供文件异步操作。
#
# imghdr：（Python 标准库）检测图片类型。
#
# mimetypes：（Python 标准库）将文件名映射为 MIME 类型。
#
# path.py：对 os.path 进行封装的模块。
#
# pathlib：（Python3.4+ 标准库）跨平台的、面向对象的路径操作库。
#
# python-magic：文件类型检测的第三方库 libmagic 的 Python 接口。
#
# Unipath：用面向对象的方式操作文件和目录。
#
# watchdog：管理文件系统事件的 API 和 shell 工具。
#
# PyFilesystem2：Python 的文件系统抽象层。
# ————————————————
# *****************************************************************

import aiofiles, asyncio


class FilePO3:
    def __init__(self):
        pass


    async def openReadFile(self, filename):

        '''
        获取文件内容（文件的非阻塞异步模式） '''

        async with aiofiles.open(filename, mode='r') as f:
            contents = await f.read()
            return contents
            # print(contents)

    async def readFile(self, filename):

        ''' 异步迭代 '''
        async with aiofiles.open(filename) as f:
            async for line in f:
                print(line)

    def run(self, coro):
        try:
            coro.send(None)
        except StopIteration as e:
            return e.value

if __name__ == "__main__":

    File_PO3 = FilePO3()

    x = File_PO3.openReadFile("1.txt")

    x = File_PO3.run(x)
    print(x)
    # https://blog.csdn.net/pydby01/article/details/122019243?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-122019243-blog-126543307.pc_relevant_recovery_v2&spm=1001.2101.3001.4242.1&utm_relevant_index=3
    # print(await x)

    # File_PO3.readFile("1.txt")












