# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description:paramiko是Python的一个库，实现了SSHv2协议(底层使用cryptography)。
# 有了Paramiko以后，我们就可以在Python代码中直接使用SSH协议对远程服务器执行操作，而不是通过ssh命令对远程服务器进行操作。
#***************************************************************

import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(hostname="192.168.1.101", port=22, username="lhc", password="jinhao123")
ssh.connect(hostname="192.168.1.105", port=22, username="linghuchong", password="Jinhao")
stdin, stdout, stderr = ssh.exec_command("ls Downloads/")   # 将显示结果在本机上输出
# stdin, stdout, stderr = ssh.exec_command("open Downloads/test.jpeg")  # 在服务器端打开图片
result = stdout.read()
print(result.decode())

ssh.close()
# 关闭连接


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



# print(stdout.read().decode())
# lines=stdout.readlines()
# print(type(lines))
# for line in lines:
#     print(line)

