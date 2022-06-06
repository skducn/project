# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2017-11-8
# Description: sh,http://amoffat.github.io/sh/
# ImportError: sh 1.12.14 is currently only supported on linux and osx. please install pbs 0.110 (http://pypi.python.org/pypi/pbs) for windows support.
# sh is a full-fledged subprocess replacement for Python 2.6 - 3.5, PyPy and PyPy3 that allows you to call any program as if it were a function:
# 执行命令行 os.system , os.popen , subprocess.Popen , commands
#***************************************************************

import sh as pbs
import sh,os, subprocess

# 1，系统级启动程序，如 appium 启动，获取进程，杀进程，启动
# os.system("appium -p 4723")
# list1 = os.popen("lsof -i tcp:4723 | awk '{print($2}' | grep -v PID").readlines()
# os.system("kill " + list1[0])
# os.system("appium -p 4723")

# 获取返回信息。
# list1 = os.popen("lsof -i tcp:4723").readlines()  # 返回列表
# print(list1[1])


# 2，获取 当前网卡信息
# from sh import ifconfig
# print(ifconfig("en0"))
# print("@@@@@@@@@@@@@@@@@@@@")

# # 不支持windows，只支持linux和mac

#
# for i in range(1,2):
#     pbs.mkdir("hello"+"%d"%i)



# print(pbs.ipconfig("eth0"))

#
# from pbs import ifconfig
# print(ifconfig("eth0"))




#
# # # 3、使用subprocess模块
# # # 执行命令的参数或返回中包含中文文字，建议使用。
# # p = subprocess.Popen("lsof -i http:80",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
# # for line in p.stdout.readlines():
# #     print(line
# #     print(type(line)   # 返回字符串
# # retval=p.wait()
# # print("@@@@@@@@@@@@@@@@@@@@"
#
#
# # # 4、使用commands模块
# import commands
# print(dir(commands))  #  ['__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', 'getoutput', 'getstatus', 'getstatusoutput', 'mk2arg', 'mkarg']
# print(commands.getoutput("date"))  # Wed Dec 20 12:19:42 CST 2017
# print(commands.getstatusoutput("date"))  # (0, 'Wed Dec 20 12:19:42 CST 2017')
# print(commands.getstatusoutput("ulimit -a"))
# print("@@@@@@@@@@@@@@@@@@@@")
#
#
# # # 显示目录清单
# print((sh.ls("-F", "/Users/linghuchong")))   # 按照天数字符对文件进行分类，如 ／ 表示目录， *表示可执行
# print((sh.ls("-s", "/Users/linghuchong")))   # 显示文件和目录大小，以区块为单位
# print((sh.ls("-m", "/Users/linghuchong")))  # 用逗号分隔
# print((sh.ls("-t", "/Users/linghuchong"))) # 最近一次修改的文件显示在最上面
# print((sh.ls("-n", "/Users/linghuchong")))   # 显示文件的UID ， GID
# print((sh.ls("-i", "/Users/linghuchong")))   # 显示文件索引节点号inode（index node），具有相同索引节点号的两个文本本质上是同一个文件。
# print("@@@@@@@@@@@@@@@@@@@@")
#
#
#
# # # # glob模式（shell通配符）
# # # 用途：通常用来匹配目录及文件，而不是文本
# list2 = sh.glob('/users/linghuchong/*')  # 获得的类型是列表 ， 获取指定目录下所有的目录与文件，
# print(list2)
# # print(list2[2]
# #
# # # ['/users/linghuchong/Desktop', '/users/linghuchong/Documents', '/users/linghuchong/Downloads', '/users/linghuchong/java_error_in_pycharm.hprof', '/users/linghuchong/Library', '/users/linghuchong/Movies', '/users/linghuchong/Music', '/users/linghuchong/package-lock.json', '/users/linghuchong/package.json', '/users/linghuchong/Pictures', '/users/linghuchong/Public', '/users/linghuchong/Thumbs.db', '/users/linghuchong/VirtualBox VMs', '/users/linghuchong/WebDriverAgent', '/users/linghuchong/ynm3k']
# # # /users/linghuchong/Downloads
# #
# # print(sh.glob('/users/linghuchong/Do*')  # 获得的类型是列表 ， 获取指定目录下所有的目录与文件，
# # # ['/users/linghuchong/Documents', '/users/linghuchong/Downloads']
#
#
# # # # 调用自己的程序
# # r = sh.Command('/Users/linghuchong/Downloads/51/Project/common/yaml1.py')
# # print(r
#
#
#
#
