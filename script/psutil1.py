# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-08-20
# Description: python 根据进程名获取PID
# https://www.cnblogs.com/saneri/p/7528283.html
# https://www.jianshu.com/p/d9a3372cc04d
# https://www.cnblogs.com/cppddz/p/7758094.html  for linux
# ********************************************************************************************************************

import psutil, re

# 1，根据进程名获取PID
def processinfo(varProcessName):
    p = psutil.process_iter()
    for r in p:
        aa = str(r)
        f = re.compile(varProcessName, re.I)
        if f.search(aa):
           return (aa.split('pid=')[1].split(',')[0])

# 获取当前pycharm.exe的进程pid
pid = processinfo("pycharm.exe")
print(pid)  # 34168


# 2，根据pid获取进程的信息
p = psutil.Process(int(pid))

# 获取进程名
print(p.name())  # pycharm.exe

# 进程程序的路径
print(p.exe())  # C:\Program Files\JetBrains\PyCharm 2018.3.5\bin\pycharm.exe

# 进程的工作目录绝对路径
print(p.cwd())        # C:\Users\ZY

# 进程状态
print(p.status())     # running


# 进程创建时间
print(p.create_time())


p.cpu_times()    #进程的cpu时间信息,包括user,system两个cpu信息
# p.cpu_affinity()  #get进程cpu亲和度,如果要设置cpu亲和度,将cpu号作为参考就好

# 进程内存利用率
print(p.memory_percent())

# 进程内存rss,vms信息
print(p.memory_info())

# 进程的IO信息,包括读写IO数字及参数
print(p.io_counters())

# 进程开启的线程数
print(p.num_threads())


# # 听过psutil的Popen方法启动应用程序，可以跟踪程序的相关信息  for linux

# from subprocess import PIPE
# p = psutil.Popen(["/usr/bin/python", "-c", "print('hello')"],stdout=PIPE)
# print(p.name())
# print(p.username())


# for linux 未测试
# import os
# from subprocess import check_output
# def get_pid(name):
#     # return check_output(["pidof",name])
#     # return map(int,check_output(["pidof",name]).split())
#     return int(check_output(["pidof","-s",name]))
#
# # def get_pid(name):
# #     return int(check_output(["pidof","-s",name]))
#
# print(get_pid("chrome"))