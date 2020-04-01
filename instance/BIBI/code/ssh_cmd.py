import pexpect

def ssh_cmd(ip, user, passwd, cmd):
    ssh = pexpect.spawn('ssh %s@%s "%s"' % (user, ip, cmd))
    try:
        i = ssh.expect(['password: ', 'continue connecting (yes/no)?'])
        if i == 0 :
            ssh.sendline(passwd)
            r = ssh.read()
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(passwd)
            r = ssh.read()
    except pexpect.EOF:
        ssh.close()
    return r

# str1 = ""
# str1 = ssh_cmd("192.168.2.154", "root", "Dlhy66506043", "tail -70 /usr/local/tomcat/logs/catalina.out")
# print str1
