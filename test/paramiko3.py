# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: paramiko 实现了SSH2协议(支持加密和认证的方式、底层使用cryptography)的远程服务器连接
# 可实现远程连接后查看服务器日志（cmd）、上传文件（update）、下载文档（downloads）
# pip install paramiko
# paramiko有两个模块SSHClient()和SFTPClient()
# 参考：https://www.cnblogs.com/qianyuliang/p/6433250.html
#***************************************************************
import paramiko
import uuid

class SSHConnection(object):

    def __init__(self, host='192.168.1.110', port=22, username='jh', pwd='jinhao123'):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username,password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def upload(self,local_path,target_path):
        # 连接，上传
        # file_name = self.create_file()
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 上传至服务器 /tmp/test.py
        sftp.put(local_path, target_path)

    def download(self,remote_path,local_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path,local_path)

    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        print (str(result, encoding='utf-8'))
        return result

ssh = SSHConnection()
ssh.connect()
# ssh.upload('c:\startIIS.bat','/Users/linghuchong/Downloads/startIIS.bat')   # 上传（本地文件，远端文件）
# ssh.download('/Users/linghuchong/Downloads/test.jpeg', 'kkkk.jpeg')   # 下载（远端文件，本地文件）
# ssh.cmd("ls Downloads/")  # 显示远程文档内容
ssh.cmd("dir")  # 显示远程文档内容
ssh.close()