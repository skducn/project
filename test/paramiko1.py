# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description:paramiko是Python的一个库，实现了SSHv2协议(底层使用cryptography)。
# 有了Paramiko以后，我们就可以在Python代码中直接使用SSH协议对远程服务器执行操作，而不是通过ssh命令对远程服务器进行操作。
#***************************************************************

import paramiko
# hostname="172.21.200.218"
# port=22
# username="linghuchong"
# password="Jinhao"
#
# def command(outpath, args2,args3,arg4,args5):
#     'this is get the command the args to return the command'
#     cmd = '%s %s %s %s %s' % (outpath, args2,args3,arg4,args5)
#     return cmd
#
# if __name__=="__main__":
#     s = paramiko.SSHClient()
#     s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     s.connect(hostname,port,username,password)
#     # stdin,stdout,sterr=s.exec_command('ps -ef | grep httpd')
#     stdin,stdout,sterr=s.exec_command('python /Users/linghuchong/Downloads/51/Project/Public/line.py hjk search tt_store char 666001')
#     # stdin, stdout, sterr = s.exec_command('python /Users/linghuchong/Downloads/51/Project/Public/123.py 444')
#
#     print(stdout.read())
#     s.close()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
r=ssh.connect("172.21.200.153",22,"ZY", "jinhao123")
stdin, stdout, stderr = ssh.exec_command("export")
lines=stdout.readlines()
print(type(lines))
for line in lines:
    print(line)
ssh.close()
