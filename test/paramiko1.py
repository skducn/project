# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description:
#***************************************************************

import paramiko
hostname="10.111.11.31"
port=22
username="linghuchong"
password="Jinhao"

def command(outpath, args2,args3,arg4,args5):
    'this is get the command the args to return the command'
    cmd = '%s %s %s %s %s' % (outpath, args2,args3,arg4,args5)
    return cmd

if __name__=="__main__":
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname,port,username,password)
    # stdin,stdout,sterr=s.exec_command('ps -ef | grep httpd')
    stdin,stdout,sterr=s.exec_command('python /Users/linghuchong/Downloads/51/Project/Public/line.py hjk search tt_store char 666001')
    # stdin, stdout, sterr = s.exec_command('python /Users/linghuchong/Downloads/51/Project/Public/123.py 444')

    print(stdout.read())
    s.close()
