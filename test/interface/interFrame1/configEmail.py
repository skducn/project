# coding:utf-8

import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import threading, zipfile, glob

import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()


class Email:
    def __init__(self):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        global host, user, password, port, sender, title
        host = localReadConfig.get_email("mail_host")
        user = localReadConfig.get_email("mail_user")
        password = localReadConfig.get_email("mail_pass")
        port = localReadConfig.get_email("mail_port")
        sender = localReadConfig.get_email("sender")
        self.subject = localReadConfig.get_email("subject") + " " + date

        # get receiver list ,eg: receiver = skducn@163.com/jinhao@163.com
        self.value = localReadConfig.get_email("receiver")
        self.receiver = []
        for n in str(self.value).split("/"):
            self.receiver.append(n)

        self.content = localReadConfig.get_email("content")
        self.imageLogo1 = localReadConfig.get_email("imageLogo1")
        self.imageLogo2 = localReadConfig.get_email("imageLogo2")
        self.attachment = localReadConfig.get_email("attachment")
        self.msg = MIMEMultipart('related')

    def email_header(self):
        """ defined email header include subject, sender and receiver """
        self.msg['subject'] = self.subject
        self.msg['from'] = sender
        self.msg['to'] = ";".join(self.receiver)

    def email_content(self):
        """ email内容格式 """
        f = open(os.path.join(readConfig.proDir, 'email', self.content))
        content = f.read()
        f.close()
        content_plain = MIMEText(content, 'html', 'UTF-8')
        self.msg.attach(content_plain)
        self.email_image()

    def email_image(self):
        """ email内容中2个公司logo """
        image1_path = os.path.join(readConfig.proDir, 'email', self.imageLogo1)
        fp1 = open(image1_path, 'rb')
        msgImage1 = MIMEImage(fp1.read())
        fp1.close()
        # defined image id
        msgImage1.add_header('Content-ID', '<image1>')
        self.msg.attach(msgImage1)

        image2_path = os.path.join(readConfig.proDir, 'email', self.imageLogo2)
        fp2 = open(image2_path, 'rb')
        msgImage2 = MIMEImage(fp2.read())
        fp2.close()
        # defined image id
        msgImage2.add_header('Content-ID', '<image2>')
        self.msg.attach(msgImage2)

    def email_file(self):
        """ email附件 """
        zippath = os.path.join(readConfig.proDir, "report", self.attachment)  # 原始文件名
        reportfile = open(zippath, 'rb').read()
        filehtml = MIMEText(reportfile, 'base64', 'utf-8')
        filehtml['Content-Type'] = 'application/octet-stream'
        filehtml['Content-Disposition'] = 'attachment; filename=' + self.attachment   # 接收到邮件附件的文件名
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
    # email = MyEmail.get_email()
    email = Email()
    email.send_email()
