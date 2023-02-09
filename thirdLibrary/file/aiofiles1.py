# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-2-8
# Description: aiofiles 异步操作文件
# import asyncio  异步协程
# import aiohttp  异步操作请求，相当于requests
# import aiofiles 异步操作文件
# async，await的理解与使用 https://blog.csdn.net/pydby01/article/details/122019243?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-122019243-blog-126543307.pc_relevant_recovery_v2&spm=1001.2101.3001.4242.1&utm_relevant_index=3
# aiofiles：https://github.com/Tinche/aiofiles/
# asyncio filesystem进展：https://github.com/python/asyncio/wiki/ThirdParty#filesystem
# *****************************************************************

import asyncio, aiofiles

async def wirte_demo():
    async with aiofiles.open("1.txt","w",encoding="utf-8") as fp:
        await fp.write("hello world \n")
        await fp.write("test")


async def read_demo():
    async with aiofiles.open("1.txt","r",encoding="utf-8") as fp:
        content = await fp.read()
        print(content)

async def read2_demo():
    async with aiofiles.open("1.txt","r",encoding="utf-8") as fp:
        # 读取每行
        async for line in fp:
            print(line)

if __name__ == "__main__":

    asyncio.run(wirte_demo())
    asyncio.run(read_demo())
    asyncio.run(read2_demo())













