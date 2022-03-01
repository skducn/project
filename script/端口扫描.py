# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-1
# Description: 用python进行安全测试 - 端口扫描
# http://download.51testing.com/wenzhang/51Testing_wenzhang64_1.pdf
# *****************************************************************

import socket
from datetime import datetime
net = input("需要扫描的主机: ") # IP 地址拼接
net1 = net.split('.')
a = '.'

net2 = net1[0] + a + net1[1] + a + net1[2] + a


# 指定待扫描的端口号范围
st1 = int(input("请输入起始端口号: "))
en1 = int(input("请输入最后一个端口号: "))
en1 = en1 + 1

# 获取系统当前时间
t1 = datetime.now()
def scan(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = s.connect_ex((addr, 135))
    print(result)
    if result == 0:
        return 1
    else:
        return 0

def run_scan():
    for ip in range(st1, en1):
        addr = net2 + str(ip)
        if (scan(addr)):
            print(addr, "is live")


run_scan()
t2 = datetime.now()
total = t2 - t1
print("扫描共花费的时间: ", total)
