# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-2-8
# Description: aiohttp 异步操作请求
# import asyncio  异步协程
# import aiohttp  异步操作请求，相当于requests
# import aiofiles 异步操作文件
# aiohttp与aiofiles模块的使用 https://blog.csdn.net/liranke/article/details/127495572
# *****************************************************************


import aiohttp, asyncio

async def main():
    async with aiohttp.ClientSession() as session:   # 相当于 requests
        async with session.get('https://www.baidu.com') as resp:
            print(resp.status)
            print(await resp.text())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# asyncio.run(main())  执行后会报错，是因为asyncio.run()会自动关闭循环,并且调用_ProactorBasePipeTransport.__del__报错, 而asyncio.run_until_complete()不会.











