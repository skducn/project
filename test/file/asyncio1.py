# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-2-8
# Description: asyncio 异步操作请求, 协程
# import asyncio  异步协程
# import aiohttp  异步操作请求，相当于requests
# import aiofiles 异步操作文件
# https://blog.csdn.net/zyy247796143/article/details/125595324
# *****************************************************************

# import asyncio
#
# async def time():
#     asyncio.sleep(3)
#
# t = time()
# asyncio.iscoroutine(t)
# asyncio.iscoroutinefunction(time)


# *****************************************************************

# import time
# import asyncio
#
# async def say_after_time(delay, what):
#     await asyncio.sleep(delay)
#     print(what)
#
#
# async def main():
#     print(f"开始时间为：{time.time()}")
#     await say_after_time(1, "hello")
#     await say_after_time(2, "world")
#     print(f"结束时间为：{time.time()}")
#
#
# loop = asyncio.get_event_loop()  # 获得一个事件循环，如果当前线程还没有事件循环，则创建一个新的事件循环loop
# # loop=asyncio.new_event_loop()   #与上面等价，创建新的事件循环
# # loop=asyncio.set_event_loop(loop)  设置一个事件循环为当前线程的事件循环。
# # loop=asyncio.get_running_loop() 返回（获取）在当前线程中正在运行的事件循环，如果没有正在运行的事件循环，则会显示错误；它是python3.7中新添加的。
# loop.run_until_complete(main())  # 通过事件循环对象运行协程函数，是相对较低层的API
# loop.close()


# *****************************************************************

import asyncio
import time

a = time.time()


async def sleep1():  # 大约1秒
    print("sleep1 begin")
    await asyncio.sleep(1)
    print("sleep1 end")


async def sleep2():  # 大约2秒
    print("sleep2 begin")
    await asyncio.sleep(2)
    print("sleep2 end")


async def sleep3():  # 大约3秒
    print("sleep3 begin")
    await asyncio.sleep(3)
    print("sleep3 end")


async def main():  # 入口函数
    done, pending = await asyncio.wait({sleep1(), sleep2(), sleep3()}, return_when=asyncio.FIRST_COMPLETED)
    for i in done:
        print(i)
    for j in pending:
        print(j)


asyncio.run(main())  # 运行入口函数
b = time.time()
print('---------------------------------------')
print(b - a)







