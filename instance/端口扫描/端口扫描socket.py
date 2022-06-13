# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-1
# Description: 用python进行安全测试 - 端口扫描
# 使用 TCP 进行端口扫描
# http://download.51testing.com/wenzhang/51Testing_wenzhang64_1.pdf
# *****************************************************************

from socket import *
import time
startTime = time.time()

if __name__ == '__main__':
    target = input('采用socket方式扫描端口，请输入扫描的主机: ')

    # 指定待扫描的端口号范围
    st1 = int(input("请输入开始端口号: "))
    en1 = int(input("请输入结束端口号: "))
    en1 = en1 + 1
    t_IP = gethostbyname(target)
    # print('开始扫描主机: ', t_IP)
    for i in range(st1, en1):
        # print('当前正扫描端口号：'+str(i))  # 创建 socket 对象
        s = socket(AF_INET, SOCK_STREAM)
        # socket.connect_ex(IP,port)，如果端口连接成功 则返回 0
        conn = s.connect_ex((t_IP, i))
        if (conn == 0):
            print('端口%d: 占用中' % (i,))
        else:
            print('端口' + str(i))
        s.close()
print('扫描共花费的时间:', time.time() - startTime)
