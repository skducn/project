# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-08-20
# Description: python 根据进程名获取PID
# python模块之psutil详解: https://www.cnblogs.com/saneri/p/7528283.html
# python 模块psutil获取进程信息: https://www.jianshu.com/p/d9a3372cc04d
# https://www.cnblogs.com/cppddz/p/7758094.html  for linux
# ********************************************************************************************************************

import psutil, re

# 1，获取进程pid
def getPid(varProcessName):
    p = psutil.process_iter()
    for r in p:
        f = re.compile(varProcessName, re.I)
        # print(r)
        if f.search(str(r)):
            return (str(r).split('pid=')[1].split(',')[0])

# 获取程序的进程pid
# pid = processinfo("pycharm.exe")
pid = getPid("DBeaver")
print(pid)  # 34168

# 根据pid获取进程的信息
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
print(p.create_time())  # 1669855454.2351408

# 进程cpu时间信息,包括user,system
print(p.cpu_times())    # pcputimes(user=1676.90625, system=242.828125, children_user=0.0, children_system=0.0)

# 进程cpu亲和度,如果要设置cpu亲和度,将cpu号作为参考就好
# print(p.cpu_affinity())  #[0, 1, 2, 3]

# 进程内存利用率
print(p.memory_percent())  # 5.433379501218663

# 进程内存rss,vms信息
print(p.memory_info())  # pmem(rss=926334976, vms=925048832, num_page_faults=1334125, peak_wset=934563840, wset=926334976, peak_paged_pool=423144, paged_pool=391224, peak_nonpaged_pool=101184, nonpaged_pool=92184, pagefile=925048832, peak_pagefile=926392320, private=925048832)

# 进程的IO信息,包括读写IO数字及参数
# print(p.io_counters())  # pio(read_count=403123, write_count=19337, read_bytes=1447829500, write_bytes=4287870945, other_count=1411793, other_bytes=35545815)

# 进程开启的线程数
print(p.num_threads())  # 45

print(p.environ())
# {'.EXE;.DOC;.TXT;.XLSX;.LNK;.URL;.BAT;': 'pathext', 'ALLUSERSPROFILE': 'C:\\ProgramData', 'APPDATA': 'C:\\Users\\jh\\AppData\\Roaming', 'CHOCOLATEYINSTALL': 'C:\\ProgramData\\chocolatey', 'CHOCOLATEYLASTPATHUPDATE': '132549906292427002', 'CLASSPATH': '.;C:\\Program Files\\Java\\jdk1.8.0_211\\lib\\dt.jar;C:\\Program Files\\Java\\jdk1.8.0_211\\lib\\tools.jar;', 'COMMONPROGRAMFILES': 'C:\\Program Files\\Common Files', 'COMMONPROGRAMFILES(X86)': 'C:\\Program Files (x86)\\Common Files', 'COMMONPROGRAMW6432': 'C:\\Program Files\\Common Files', 'COMPUTERNAME': 'DESKTOP-DO7AEPU', 'COMSPEC': 'C:\\WINDOWS\\system32\\cmd.exe', 'DRIVERDATA': 'C:\\Windows\\System32\\Drivers\\DriverData', 'ES_JAVA_HOME': 'D:\\51\\ES\\windows\\elasticsearch-7.17.0\\jdk', 'FPS_BROWSER_APP_PROFILE_STRING': 'Internet Explorer', 'FPS_BROWSER_USER_PROFILE_STRING': 'Default', 'HOMEDRIVE': 'C:', 'HOMEPATH': '\\Users\\jh', 'JAVA_HOME': 'C:\\Program Files\\Java\\jdk1.8.0_211', 'JMETER_HOME': 'C:\\apache-jmeter-5.1.1', 'LOCALAPPDATA': 'C:\\Users\\jh\\AppData\\Local', 'LOGONSERVER': '\\\\DESKTOP-DO7AEPU', 'NUMBER_OF_PROCESSORS': '4', 'ONEDRIVE': 'C:\\Users\\jh\\OneDrive', 'OS': 'Windows_NT', 'PATH': 'C:\\ProgramData\\Anaconda3;C:\\ProgramData\\Anaconda3\\Library\\mingw-w64\\bin;C:\\ProgramData\\Anaconda3\\Library\\usr\\bin;C:\\ProgramData\\Anaconda3\\Library\\bin;C:\\ProgramData\\Anaconda3\\Scripts;C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\javapath;C:\\Python39\\Scripts\\;C:\\Python39\\;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\WINDOWS\\System32\\OpenSSH\\;C:\\ProgramData\\chocolatey\\bin;C:\\Program Files\\Java\\jdk1.8.0_211\\bin;C:\\Program Files\\Java\\jdk1.8.0_211\\jre\\bin;C:\\apache-jmeter-5.1.1\\bin;C:\\apache-jmeter-5.1.1\\lib\\ext\\ApacheJMeter_core.jar;C:\\apache-jmeter-5.1.1\\lib\\jorphan.jar;C:\\apache-jmeter-5.1.1\\lib\\logkit-2.0.jar;C:\\swigwin-4.0.2\\;D:\\voice\\ffmpeg-n4.4-80-gbf87bdd3f6-win64-gpl-4.4\\bin\\;C:\\Program Files\\nodejs\\;C:\\Program Files (x86)\\NetSarang\\Xshell 7\\;C:\\Program Files\\Git\\cmd;C:\\Python39\\Scripts;C:\\Python39;C:\\Users\\jh\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Program Files\\JetBrains\\PyCharm 2018.3.5\\bin;d:\\myLNK;C:\\Users\\jh\\AppData\\Local\\Programs\\Fiddler;C:\\Users\\jh\\AppData\\Roaming\\npm;', 'PATHEXT': '.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.PY;.PYW', 'PROCESSOR_ARCHITECTURE': 'AMD64', 'PROCESSOR_IDENTIFIER': 'Intel64 Family 6 Model 158 Stepping 9, GenuineIntel', 'PROCESSOR_LEVEL': '6', 'PROCESSOR_REVISION': '9e09', 'PROGRAMDATA': 'C:\\ProgramData', 'PROGRAMFILES': 'C:\\Program Files', 'PROGRAMFILES(X86)': 'C:\\Program Files (x86)', 'PROGRAMW6432': 'C:\\Program Files', 'PSMODULEPATH': 'C:\\Program Files\\WindowsPowerShell\\Modules;C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\Modules', 'PUBLIC': 'C:\\Users\\Public', 'PYCHARM': 'C:\\Program Files\\JetBrains\\PyCharm 2018.3.5\\bin;', 'SESSIONNAME': 'Console', 'SYSTEMDRIVE': 'C:', 'SYSTEMROOT': 'C:\\WINDOWS', 'TEMP': 'C:\\Users\\jh\\AppData\\Local\\Temp', 'TMP': 'C:\\Users\\jh\\AppData\\Local\\Temp', 'TNS_ADMIN': 'D:\\51\\oracle\\instantclient_21_7\\network\\admin', 'USERDOMAIN': 'DESKTOP-DO7AEPU', 'USERDOMAIN_ROAMINGPROFILE': 'DESKTOP-DO7AEPU', 'USERNAME': 'jh', 'USERPROFILE': 'C:\\Users\\jh', 'VS140COMNTOOLS': 'C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\Common7\\Tools\\', 'WINDIR': 'C:\\WINDOWS'}

# print('-----------------------------cpu---------------------------------------')
#
# # 获取cpu的完整信息
# print(psutil.cpu_times())  # scputimes(user=127223.09374999999, system=95727.90625, idle=1888597.8906249998, interrupt=4651.59375, dpc=1930.0625)
#
# # 用户的cpu等待时间
# print(psutil.cpu_times().user)  # 127243.18749999999
#
# # CPU逻辑个数
# print(psutil.cpu_count())  # 4
#
# # CPU物理个数
# print(psutil.cpu_count(logical=False))  # 4
#
# # # 获取cpu的使用率
# # print(psutil.cpu_percent())  # 0.0
# # print(psutil.cpu_percent(1))  # 15.6
# # print(psutil.cpu_percent(2))  # 2.7
# # print(psutil.cpu_percent(3))  # 4.6
#
# print('-----------------------------内存---------------------------------------')
#
#
# # 通过 virtual_memory() 获取内存信息
# mem = psutil.virtual_memory()
# print(mem)  # svmem(total=17048965120, available=9785143296, percent=42.6, used=7263821824, free=9785143296)
# print(mem.total)  # 17048965120
# print(mem.available)  # 9785143296   //还可以使用的内存
# print(mem.percent)  # 42.6   //实际已经使用的内存占比
# print(mem.used)  # 7263821824
# print(mem.free)  # 9785143296
# print(mem.total / 1024 / 1024)  # 16259.16015625
#
# # 通过 swap_memory() 获取swap内存信息
# swap = psutil.swap_memory()
# print(swap)  # sswap(total=19599101952, used=10249875456, free=9349226496, percent=52.3, sin=0, sout=0)
#
#
# print('-----------------------------磁盘信息---------------------------------------')
#
# # 获取分区信息
# print(psutil.disk_partitions())
# # [sdiskpart(device='C:\\', mountpoint='C:\\', fstype='NTFS', opts='rw,fixed', maxfile=255, maxpath=260), sdiskpart(device='D:\\', mountpoint='D:\\', fstype='NTFS', opts='rw,fixed', maxfile=255, maxpath=260), sdiskpart(device='E:\\', mountpoint='E:\\', fstype='NTFS', opts='rw,fixed', maxfile=255, maxpath=260), sdiskpart(device='H:\\', mountpoint='H:\\', fstype='CDFS', opts='ro,readonly,cdrom', maxfile=110, maxpath=260)]
#
# # 磁盘的利用率
# print(psutil.disk_usage('/'))  # sdiskusage(total=504594231296, used=109738389504, free=394855841792, percent=21.7)
#
# # 获取硬盘总的io数和读写信息
# print(psutil.disk_io_counters())  # sdiskio(read_count=4145072, write_count=7907086, read_bytes=523096242688, write_bytes=520049804800, read_time=15003, write_time=17854)
#
# # 获取单个分区的io和读写信息加上"perdisk=True"参数
# print(psutil.disk_io_counters(perdisk=True))
# # {'PhysicalDrive0': sdiskio(read_count=991051, write_count=828306, read_bytes=414168540672, write_bytes=399525044224, read_time=12272, write_time=16017),
# # 'PhysicalDrive1': sdiskio(read_count=3154022, write_count=7079394, read_bytes=108927734784, write_bytes=120571209728, read_time=2731, write_time=1837)}
#
# print('-----------------------------网络信息---------------------------------------')
#
# # 获取网络总的io情况
# print(psutil.net_io_counters())  # snetio(bytes_sent=1972189799, bytes_recv=38911659689, packets_sent=13305958, packets_recv=29879423, errin=0, errout=0, dropin=0, dropout=0)
#
# # 获取网卡的io情况
# print(psutil.net_io_counters(pernic=True))
# # {'以太网': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0),
# # '本地连接* 1': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0),
# # '本地连接* 2': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0),
# # '以太网 2': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0),
# # 'WLAN': snetio(bytes_sent=1972189799, bytes_recv=38911659689, packets_sent=13305958, packets_recv=29879423, errin=0, errout=0, dropin=0, dropout=0),
# # 'Loopback Pseudo-Interface 1': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0)}




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