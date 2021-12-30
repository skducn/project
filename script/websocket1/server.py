# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2021-12-30
# Description: websocket server
# http://download.51testing.com/wenzhang/51Testing_wenzhang63_1.pdf
# *******************************************************************

import socket

def serverSide():
    host = socket.gethostname()
    port = 23333
    serversocket = socket.socket()
    serversocket.bind((host,port))
    serversocket.listen(1)
    print("socket 监听中...")

    while True:
        conn, addr = serversocket.accept()
        print("收到连接请求 %s" % str(addr))
        msg = "连接已建立" + "\r\n"
        conn.send(msg.encode('utf-8'))
        conn.close()

if __name__ == "__main__":

    serverSide()