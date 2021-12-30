# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2021-12-30
# Description: websocket client
# http://download.51testing.com/wenzhang/51Testing_wenzhang63_1.pdf
# *******************************************************************

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 23333
s.connect((host, port))
msg = s.recv(1024)
s.close()
print(msg.decode('utf-8'))

