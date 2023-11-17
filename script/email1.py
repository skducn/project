# coding: utf-8
# *******************************************************************************************************************************
# Author     : John
# Date       : 2018-10-30
# Description: 发送163邮箱功能(废弃，请参考NetPO.py)
# 注意：邮件主题为‘test’时，会出现错误。
# 163邮箱需要设置 客户端授权密码为开启，并且脚本中设置的登录密码是授权码
# *******************************************************************************************************************************

import smtplib, os, base64
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

def sendEmail(varFrom, varTo, varSubject, varConent, varPic, varFile, varHtmlFileName, varHtmlContent):
    msg = email.mime.multipart.MIMEMultipart()
    msg['From'] = varFrom
    if "," in varTo:
        # 收件人为多个收件人
        varTo = [varTo.split(",")[0], varTo.split(",")[1]]

    '''主题'''
    msg['Subject'] = Header(varSubject, 'utf-8').encode()
    txt = MIMEText(varConent, 'plain', 'utf-8')
    msg.attach(txt)

    '''附件图片'''
    if varPic != "" :
        sendimagefile = open(varPic, 'rb').read()
        image = MIMEImage(sendimagefile)
        # image.add_header('Content-ID', '<image1>')  # 默认文件名
        image.add_header("Content-Disposition", "attachment", filename=("utf-8", "", os.path.basename(varPic)))
        msg.attach(image)

    ''' 附件文件 '''
    if varFile != "":
        sendfile = open(varFile, 'rb').read()
        text_att = MIMEText(sendfile, 'base64', 'utf-8')
        text_att["Content-Type"] = 'application/octet-stream'
        # text_att.add_header('Content-Disposition', 'attachment', filename='interface.xls')   # 不支持中文格式文件名
        text_att.add_header("Content-Disposition", "attachment", filename=("utf-8", "", os.path.basename(varFile)))  # 支持中文格式文件名
        msg.attach(text_att)

    '''附件HTML'''
    if varHtmlFileName != "" and varHtmlContent != "":
        text_html = MIMEText(varHtmlContent, 'html', 'utf-8')
        text_html.add_header("Content-Disposition", "attachment", filename=("utf-8", "", varHtmlFileName))
        msg.attach(text_html)

    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com', '25')
    smtp.login(varFrom, str(base64.b64decode("amluaGFvMTIz"), encoding="utf-8"))  # byte转str
    smtp.sendmail(varFrom, varTo, msg.as_string())
    smtp.quit()
    print(u"邮件成功发送给：" + str(varTo))

# *******************************************************************************************************************************
# 参数分别是：发送邮箱，接收邮箱，主题，邮件正文，附件图片，附件文档，附件html名，附件html正文。

sendEmail('skducn@163.com',"skducn@163.com",
          "屏幕劫持",
          "开发同学，您好！\n\n\n 以下是本次接口测试报错信息，请检查。\n\n" + "tesst" + "\n\n 如果这不是您的邮件请忽略，很抱歉打扰您，请原谅。\n\n" \
          "(这是一封自动产生的email，请勿回复) \n\nCETC测试组 \n\nBest Regards",
          "","","",""
          )

# sendEmail('skducn@163.com',
#           "skducn@163.com",
#           "屏幕劫持",
#           "开发同学，您好！\n\n\n 以下是本次接口测试报错信息，请检查。\n\n" + "tesst" + "\n\n 如果这不是您的邮件请忽略，很抱歉打扰您，请原谅。\n\n" \
#           "(这是一封自动产生的email，请勿回复) \n\nCETC测试组 \n\nBest Regards",
#           r'D:\\51\\python\\project\\common\\20190918160419金浩.jpg',
#           r'D:\\51\\python\\project\\common\\code测试.txt',
#           "我的.html",
#           """
#           <html>
#             <head></head>
#             <body>
#               <p>Hi!<br>
#                  How are you?是否看到<br>
#                  Here is the <a href="http://www.baidu.com">link</a> you wanted.<br>
#               </p>
#             </body>
#           </html>
#           """
#           )


