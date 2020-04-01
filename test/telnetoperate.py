# coding=utf-8

import time, sys, logging, traceback, telnetlib, socket


class TelnetAction:
    def __init__(self, host, prompt, account, accountPasswd, RootPasswd=""):
        self.log = logging.getLogger()
        self.host = host
        self.account = account
        self.accountPasswd = accountPasswd
        self.RootPasswd = RootPasswd
        self.possible_prompt = ["#", "$"]
        self.prompt = prompt
        self.default_time_out = 20
        self.child = None
        self.login()

    def expand_expect(self, expect_list):
        try:
            result = self.child.expect(expect_list, self.default_time_out)
        except EOFError:
            self.log.error("No text was read, please check reason")
        if result[0] == -1:
            self.log.error("Expect result" + str(expect_list) + " don't exist")
        else:
            pass
        return result

    def login(self):
        """Connect to a remote host and login. 

        """
        try:
            self.child = telnetlib.Telnet(self.host)
            self.expand_expect(['login:'])
            self.child.write(self.account + '\n')
            self.expand_expect(['assword:'])
            self.child.write(self.accountPasswd + '\n')
            self.expand_expect(self.possible_prompt)
            self.log.debug("swith to root account on host " + self.host)
            if self.RootPasswd != "":
                self.child.write('su -' + '\n')
                self.expand_expect(['assword:'])
                self.child.write(self.RootPasswd + '\n')
                self.expand_expect(self.possible_prompt)
                # self.child.write('bash'+'\n')
            self.expand_expect(self.possible_prompt)
            # self.child.read_until(self.prompt)
            self.log.info("login host " + self.host + " successfully")
            return True
        except:
            print("Login failed,please check ip address and account/passwd")
            self.log.error("log in host " + self.host + " failed, please check reason")
            return False

    def send_command(self, command, sleeptime=0.5):
        """Run a command on the remote host. 

        @param command: Unix command 
        @return: Command output 
        @rtype: String 
        """
        self.log.debug("Starting to execute command: " + command)
        try:
            self.child.write(command + '\n')
            if self.expand_expect(self.possible_prompt)[0] == -1:
                self.log.error("Executed command " + command + " is failed, please check it")
                return False
            else:
                time.sleep(sleeptime)
                self.log.debug("Executed command " + command + " is successful")
                return True
        except socket.error:
            self.log.error("when executed command " + command + " the connection maybe break, reconnect")
            traceback.print_exc()
            for i in range(0, 3):
                self.log.error("Telnet session is broken from " + self.host + ", reconnecting....")
                if self.login():
                    break
            return False

    def get_output(self, prompt,time_out=2):
        reponse = self.child.read_until(self.prompt,time_out)
        # print "response:",reponse
        self.log.debug("reponse:" + reponse)
        return self.__strip_output(reponse)

    def send_atomic_command(self, command):
        self.send_command(command)
        command_output = self.get_output()
        self.logout()
        return command_output

    def process_is_running(self, process_name, output_string):
        self.send_command("ps -ef | grep " + process_name + " | grep -v grep")
        output_list = [output_string]
        if self.expand_expect(output_list)[0] == -1:
            return False
        else:
            return True

    def __strip_output(self, response):
        # Strip everything from the response except the actual command output.

        # split the response into a list of the lines

        lines = response.splitlines()
        self.log.debug("lines:" + str(lines))
        if len(lines) > 1:
            # if our command was echoed back, remove it from the output
            if self.prompt in lines[0]:
                lines.pop(0)
                # remove the last element, which is the prompt being displayed again
            lines.pop()
            # append a newline to each line of output
            lines = [item + '\n' for item in lines]
            # join the list back into a string and return it
            return ''.join(lines)
        else:
            self.log.info("The response is blank:" + response)
            return "Null response"

    def logout(self):

        self.child.close()