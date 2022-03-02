# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-1
# Description: 使用TCP进行端口扫描
# http://download.51testing.com/wenzhang/51Testing_wenzhang64_1.pdf
# *****************************************************************

import socket
from datetime import datetime

net = input("采用tcp方式扫描端口，请输入扫描的主机: ")


# 指定待扫描的端口号范围
st1 = int(input("请输入开始端口号: "))
en1 = int(input("请输入结束端口号: "))
en1 = en1 + 1

# 获取系统当前时间
t1 = datetime.now()

def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    # 如果操作成功则为 0，否则为 error 变量的值
    result = s.connect_ex((net, port))
    # print(result)
    if result == 0:
        return 1
    else:
        return 0

def run_scan():
    for port in range(st1, en1):
        if (scan(port)):
            print('端口%d: 占用中' % (port,))

run_scan()
t2 = datetime.now()
total = t2 - t1
print("扫描共花费的时间: ", total)
