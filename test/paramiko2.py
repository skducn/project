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

import json

def connect(host):
    'this is use the paramiko connect the host,return conn'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        #        ssh.connect(host,username='root',allow_agent=True,look_for_keys=True)
        ssh.connect(host, username='root', password='root', allow_agent=True)
        return ssh
    except:
        return None


def command(args, outpath):
    'this is get the command the args to return the command'
    cmd = '%s %s' % (outpath, args)
    return cmd


def exec_commands(conn, cmd):
    'this is use the conn to excute the cmd and return the results of excute the command'
    stdin, stdout, stderr = conn.exec_command(cmd)
    results = stdout.read()
    return results


def excutor(host, outpath, args):
    conn = connect(host)
    if not conn:
        return [host, None]
        # exec_commands(conn,'chmod +x %s' % outpath)
    cmd = command(args, outpath)
    result = exec_commands(conn, cmd)
    result = json.dumps(result)
    return [host, result]

def copy_module(conn, inpath, outpath):
    'this is copy the module to the remote server'
    ftp = conn.open_sftp()
    ftp.put(inpath, outpath)
    ftp.close()
    return outpath


if __name__ == '__main__':
    # print json.dumps(excutor(hostname, 'ls', ' -l'), indent=4, sort_keys=True)
    # print copy_module(connect(hostname), 'kel.txt', '/root/kel.1.txt')
    x = exec_commands(connect(hostname), command(' -l', 'ls'))
    print x
