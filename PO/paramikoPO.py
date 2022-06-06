# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: paramiko 实现了SSH2协议(支持加密和认证的方式、底层使用cryptography)的远程服务器连接
# 可实现远程连接后查看服务器日志（cmd）、上传文件（update）、下载文档（downloads）
# pip install paramiko
# paramiko有两个模块SSHClient()和SFTPClient()
# 参考：https://www.cnblogs.com/qianyuliang/p/6433250.html
# https://blog.csdn.net/zangba9624/article/details/118398648
#***************************************************************


import paramiko

class SSHConnection(object):

    def __init__(self, host, port, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username,password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def upload(self, local_path, target_path):
        # 上传
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, target_path)

    def download(self, remote_path, local_path):
        # 下载
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path, local_path)

    def cmd(self, command):
        # 执行服务器命令
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read()
        print(str(result, encoding='utf-8'))
        return result



if __name__ == "__main__":

    ssh = SSHConnection(host='192.168.0.243', port=22, username='root', pwd='Benetech79$#-')

    print("1 上传（本地文件，远端文件）".center(100, "-"))
    ssh.upload('d:\\111.txt', '/root/111.txt')   # 上传（本地文件，远端文件）


    print("2 下载（远端文件，本地文件）".center(100, "-"))
    ssh.download('/root/111.txt', 'd:\\222.txt')   # 下载（远端文件，本地文件）


    print("3 执行服务器命令".center(100, "-"))
    ssh.cmd("cat 111.txt")  # 查看服务器上文件内容
    ssh.cmd("ls")


    ssh.close()