# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-2-8
# Description: 单线程多任务异步协程爬取图片
# import asyncio  异步协程
# import aiohttp  异步操作请求，相当于requests
# import aiofiles 异步操作文件
# *****************************************************************

import asyncio
import aiohttp
import aiofiles

urls = ["https://img.lianzhixiu.com/uploads/allimg/202109/9999/d1eeaa0450.jpg",
        "https://img.lianzhixiu.com/uploads/allimg/202109/9999/6747451f08.jpg",
        "https://img.lianzhixiu.com/uploads/allimg/202108/9999/88abd53cc1.jpg"
        ]

async def aioDownload(url):
    # 发送请求
    # 得到图片内容
    # 保存到文件
    print("开始下载")
    name = url.rsplit("/", 1)[1]  # 获取文件名，如d1eeaa0450.jpg
    async with aiohttp.ClientSession() as session:  # 相当于requests
        async with session.get(url) as resp:  # 相当于resp = requests.get()
            # aiofiles写文件
            async with aiofiles.open(name, mode='wb') as f:  # 创建文件
                await f.write(await resp.content.read())  # 读取内容是异步的，需要await挂起，resp.text()
    print("下载完成")


async def main():
    # 准备异步协程对象列表
    tasks = []

    for url in urls:
        task = asyncio.create_task(aioDownload(url))
        tasks.append(task)

    await asyncio.wait(tasks)


if __name__ == '__main__':

    # 一次性启动多个任务
    # asyncio.run(main())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())









