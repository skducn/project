# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2017-5-23
# Description: 网络对象（发邮件，获取网页状态码，网页header，网页内容，下载文件,下载网页，下载图片
# ***************************************************************

import smtplib, os, base64, requests,urllib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from urllib.request import urlretrieve
import json, jsonpath

class NetPO():

    def sendEmail(self, varFrom, varTo, varSubject, varConent, varPic, varFile, varHtmlFileName, varHtmlContent):
        ''' 发送163邮件 '''
        # 注意：邮件主题为‘test’时，会出现错误。
        # 163邮箱需要设置 客户端授权密码为开启，并且脚本中设置的登录密码是授权码
        # 参数：发送者邮箱，接收者邮箱，主题，邮件正文，附件图片，附件文档，附件html名，附件html正文。
        # sendEmail('skducn@163.com',"skducn@163.com",
        #           "屏幕劫持",
        #           "开发同学，您好！\n\n\n 以下是本次接口测试报错信息，请检查。\n\n" + "tesst" + "\n\n 如果这不是您的邮件请忽略，很抱歉打扰您，请原谅。\n\n" \
        #           "(这是一封自动产生的email，请勿回复) \n\nCETC测试组 \n\nBest Regards",
        #           "","","",""
        #           )

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
        if varPic != "":
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
            text_att.add_header("Content-Disposition", "attachment",
                                filename=("utf-8", "", os.path.basename(varFile)))  # 支持中文格式文件名
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

    def getURLCode(self, varURL):
        # 获取网站的statuscode，如 200 404 500'''
        response = requests.get(varURL)
        return response.status_code

    def getHeaders(self, varURL):
        # 获取网站的header，如:
        # {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'Keep-Alive',
        #  'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Fri, 20 Sep 2019 07:12:16 GMT',
        #  'Last-Modified': 'Mon, 23 Jan 2017 13:23:55 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18',
        #  'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}'''
        response = requests.get(varURL)
        return response.headers

    def getHtml(self, varURL):
        # 获取网站内容
        response = requests.get(varURL)
        return response.text


    def downloadFile(self, varURLFile, savepath='./'):
        # 下载文件（显示下载进度，数据块大小，文件大小）
        # Net_PO.downloadFile("https://www.7-zip.org/a/7z1900-x64.exe", "")
        def reporthook(a, b, c):
            print("\r下载进度: %5.1f%%" % (a * b * 100.0 / c), end="")
        filename = os.path.basename(varURLFile)
        # 判断文件是否存在，如果不存在则下载
        if not os.path.isfile(os.path.join(savepath, filename)):
            print('下载数据: %s' % varURLFile)
            print("保存路径：%s" % savepath)
            urlretrieve(varURLFile, os.path.join(savepath, filename), reporthook=reporthook)
            print('\nDownload finished!')
        else:
            print('File already exsits!')
        # 获取文件大小
        filesize = os.path.getsize(os.path.join(savepath, filename))
        # 文件大小默认以Bytes计， 转换为Mb
        print('File size = %.2f Mb' % (filesize / 1024 / 1024))

    def downloadHtml(self, varURL, varLocalHtmlFile):
        # 下载页面，将页面保存到本地。
        # Net_PO.downloadHtml(u"http://www.jb51.net/Special/636.htm", "1234.html")
        urllib.request.urlretrieve(varURL, varLocalHtmlFile)

    def downloadImage(self, varURLImageFile, varLocalImageFile):
        # 下载图片，将网上图片保存到本地。
        # Net_PO.downloadPIC("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg","john.jpg")  
        sess = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36","Connection": "keep-alive"}
        image = sess.get(varURLImageFile, headers=headers).content
        with open(varLocalImageFile, "wb") as f:
            f.write(image)

    
if __name__ == '__main__':
    Net_PO = NetPO()

    # Net_PO.sendEmail('skducn@163.com', "skducn@163.com", "今天的测试",
    #           "开发同学，您好！\n\n\n 以下是本次接口测试报错信息，请检查。\n\n" + "tesst" + "\n\n 如果这不是您的邮件请忽略，很抱歉打扰您，请原谅。\n\n" \
    #           "(这是一封自动产生的email，请勿回复) \n\nCETC测试组 \n\nBest Regards",
    #           "","","","")

    # print(Net_PO.getURLCode("https://www.baidu.com"))
    # print(Net_PO.getHeaders("https://www.baidu.com"))
    # print(Net_PO.getHtml("https://www.baidu.com"))

    # print(Net_PO.getJsonPath('{"status":200,"msg":"success","token":"e351b73b1c6145ceab2a02d7bc8395e7"}', '$.token'))  # ['e351b73b1c6145ceab2a02d7bc8395e7']

    # Net_PO.downloadFile("https://www.7-zip.org/a/7z1900-x64.exe", "")
    # Net_PO.downloadHtml(u"http://www.jb51.net/Special/636.htm", "1234.html")
    # Net_PO.downloadImage("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg", "test.jpg")



