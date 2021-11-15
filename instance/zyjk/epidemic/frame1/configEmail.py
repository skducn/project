# -*- coding: utf-8 -*-
import os, smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import parseaddr,formataddr
from datetime import datetime
import threading, zipfile, glob

import instance.zyjk.epidemic.frame1.readConfig as readConfig
localReadConfig = readConfig.ReadConfig()

from time import sleep

class Email:
    def __init__(self):

        global host, user, password, port, sender, title, senderNickName, subject
        self.receiverList = []
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        host = localReadConfig.get_email("mail_host")
        user = localReadConfig.get_email("mail_user")
        password = localReadConfig.get_email("mail_pass")
        port = localReadConfig.get_email("mail_port")
        sender = localReadConfig.get_email("sender")
        senderNickName = localReadConfig.get_email("senderNickName")
        subject = localReadConfig.get_email("subject") + " " + date

        self.receiver = localReadConfig.get_email("receiver")
        for n in str(self.receiver).split(","):
            self.receiverList.append(n)

        self.content = localReadConfig.get_email("content")
        self.attachment = localReadConfig.get_email("attachment")
        self.msg = MIMEMultipart('related')

    # 自定义处理邮件收发地址的显示内容
    def _format_addr(self, s):
        name, addr = parseaddr(s)
        # 将邮件的name转换成utf-8格式，addr如果是unicode，则转换utf-8输出，否则直接输出addr
        return formataddr((Header(name, 'utf-8').encode(), addr))


    def email_header(self):
        """ defined email header include subject, sender and receiver """
        self.msg['subject'] = subject
        # self.msg['from'] = sender     # 发件人： skducn<skducn@163.com>
        self.msg['from'] = self._format_addr(senderNickName + u' <%s>'% sender)    # 发件人： 令狐冲<skducn@163.com>
        self.msg['to'] = ";".join(self.receiverList)

    def email_content(self):
        """ email内容格式 """
        f = open(os.path.join(readConfig.proDir, 'email', self.content))
        content = f.read()
        f.close()
        content_plain = MIMEText(content, 'html', 'UTF-8')
        self.msg.attach(content_plain)
        self.email_image()

    def email_image(self):
        # 上传多个图片，如上传2张图片格式：image = logo1.jpg,logo2.jpg
        self.image = localReadConfig.get_email("image")
        if "," not in self.image:
            image1_path = os.path.join(readConfig.proDir, 'email', self.image)
            fp1 = open(image1_path, 'rb')
            msgImage1 = MIMEImage(fp1.read())
            fp1.close()
            msgImage1.add_header('Content-ID', '<image1>')  # # defined image id, 不能少
            self.msg.attach(msgImage1)
        else:
            imageLen = len(str(self.image).split(","))
            for i in range(imageLen):
                try:
                    image1_path = os.path.join(readConfig.proDir, 'email', str(self.image).split(",")[i])
                    fp1 = open(image1_path, 'rb')
                    msgImage1 = MIMEImage(fp1.read())
                    fp1.close()
                    msgImage1.add_header('Content-ID', "<image" + str(i + 1) + ">")  # # defined image id, 不能少
                    self.msg.attach(msgImage1)
                except:
                    pass

    def email_file(self):
        """ email附件 """
        varPath, varFile = os.path.split(self.attachment)
        reportfile = open(self.attachment, 'rb').read()
        filehtml = MIMEText(reportfile, 'base64', 'utf-8')
        filehtml['Content-Type'] = 'application/octet-stream'
        filehtml['Content-Disposition'] = 'attachment; filename=' + varFile   # 接收到邮件附件的文件名
        self.msg.attach(filehtml)


    def send_email(self):
        """ send email """
        self.email_header()
        self.email_content()
        self.email_file()
        try:
            smtp = smtplib.SMTP()
            smtp.connect(host)
            smtp.login(user, password)
            smtp.sendmail(sender, self.receiver, self.msg.as_string())
            smtp.quit()
        except Exception as e:
            # print(e.__traceback__)
            print("error, 邮件发送失败！")

class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():

        if MyEmail.email is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.email.send_email()
            MyEmail.mutex.release()
        return MyEmail.email


if __name__ == "__main__":


    email = Email()

    email.send_email()
    # email = MyEmail.get_email()
