# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-7-2
# Description: threading
# 任务是多线程的，可以利用threading来创建一个守护线程，让它在主线程结束后依然执行：
# *****************************************************************

import threading, time

def timed_task():
    print("定时任务开始")
    time.sleep(2)  # 假设这是你的任务，实际替换为你的代码
    print("定时任务结束")

thread = threading.Thread(target=timed_task)
thread.setDaemon(True)  # 设为守护线程
thread.start()









