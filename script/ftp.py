# coding: utf-8
from ftplib import FTP
import time
import tarfile
import os

from ftplib import FTP            #加载ftp模块

ftp=FTP()                         #设置变量
ftp.set_debuglevel(2)             #打开调试级别2，显示详细信息
ftp.connect("http://10.111.3.22/",21)          #连接的ftp sever和端口
ftp.login("Administrator","1q2w3e$R")      #连接的用户名，密码
print(ftp.getwelcome())            #打印出欢迎信息
ftp.cmd("e:\engine")                #进入远程目录
bufsize=1024                      #设置的缓冲区大小
filename="john.txt"           #需要下载的文件
file_handle=open(filename,"wb").write #以写模式在本地打开文件
ftp.retrbinaly("RETR filename.txt",file_handle,bufsize) #接收服务器上文件并写入本地文件
ftp.set_debuglevel(0)             #关闭调试模式
ftp.quit()                        #退出ftp


# from ftplib import FTP
#
# def ftpconnect(host, username, password):
#     ftp = FTP()
#     # ftp.set_debuglevel(2)
#     ftp.connect(host, 21)
#     ftp.login(username, password)
#     return ftp
#
# #从ftp下载文件
# def downloadfile(ftp, remotepath, localpath):
#     bufsize = 1024
#     fp = open(localpath, 'wb')
#     ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
#     ftp.set_debuglevel(0)
#     fp.close()
#
# #从本地上传文件到ftp
# def uploadfile(ftp, remotepath, localpath):
#     bufsize = 1024
#     fp = open(localpath, 'rb')
#     ftp.storbinary('STOR ' + remotepath, fp, bufsize)
#     ftp.set_debuglevel(0)
#     fp.close()
#
# if __name__ == "__main__":
#     ftp = ftpconnect("http://10.111.3.22", "Administrator", "1q2w3e$R")
#     downloadfile(ftp, "e:\engine\john.txt", "c:\john111.txt")
#     #调用本地播放器播放下载的视频
#     # os.system('start "C:\Program Files\Windows Media Player\wmplayer.exe" "C:/Users/Administrator/Desktop/test.mp4"')
#     # uploadfile(ftp, "C:/Users/Administrator/Desktop/test.mp4", "test.mp4")
#
#     ftp.quit()
