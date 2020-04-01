# -*- coding: utf-8 -*-

import os, sys,requests, xlwt, xlrd, MySQLdb, redis, urllib3, random, time, urllib2, MultipartPostHandler, cookielib, string ,datetime, smtplib,email

import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.encoders import encode_base64

# a =9
# b =20
# print int(b/a)





# from email.utils import COMMASPACE,formatdate
# from email import encoders

# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEBase import MIMEBase
# from email.MIMEText import MIMEText
# from email.MIMEAudio import MIMEAudio
# from email.MIMEImage import MIMEImage
# from email.Encoders import encode_base64

def sendMail(subject, text, *attachmentFilePaths):
    gmailUser = 'jinhao@mo-win.com.cn'
    gmailPassword = 'Dlhy123456'
    recipient = 'jinhao@mo-win.com.cn'

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = subject
    # msg = MIMEText(text, 'plain', 'utf-8')

    # msg.attach(MIMEText(text))
    msg.attach(MIMEText(text, 'plain', 'utf-8'))


    for attachmentFilePath in attachmentFilePaths:
        if attachmentFilePath != '':
             msg.attach(getAttachment(attachmentFilePath))

    mailServer = smtplib.SMTP('smtp.exmail.qq.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()

    print('Sent email to %s' % recipient)

def getAttachment(attachmentFilePath):
    contentType, encoding = mimetypes.guess_type(attachmentFilePath)

    if contentType is None or encoding is not None:
        contentType = 'application/octet-stream'

    mainType, subType = contentType.split('/', 1)
    file = open(attachmentFilePath, 'rb')

    if mainType == 'text':
        attachment = MIMEText(file.read())
    elif mainType == 'message':
        attachment = email.message_from_file(file)
    elif mainType == 'image':
        attachment = MIMEImage(file.read(),_subType=subType)
    elif mainType == 'audio':
        attachment = MIMEAudio(file.read(),_subType=subType)
    else:
        attachment = MIMEBase(mainType, subType)
    attachment.set_payload(file.read())
    # encode(attachment)
    encode_base64(attachment)

    file.close()

    attachment.add_header('Content-Disposition', 'attachment',   filename=os.path.basename(attachmentFilePath))
    return attachment


# start to test
# sendMail('here is a subject', 'Send a email with Gmail', '/Users/linghuchong/Downloads/51/Project/mySVN/Test/Backup/InterfaceExcel.xls')
sendMail(u'报错!!!', u'你啊哈 \n\nSend a email with Gmail', '/Users/linghuchong/Downloads/51/Project/mySVN/Test/Backup/InterfaceExcel.xls')

