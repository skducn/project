# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2017-5-23
# Description: 网络对象（发邮件，获取网页状态码，网页header，网页内容，下载文件,下载网页，下载图片
# ***************************************************************

'''
1，发送邮件

2.1，获取网站状态码
2.2，获取网站的header
2.3，获取网站内容

3.1，下载程序
3.2，下载网页/图片
3.3，下载图片
3.4，异步多线程下载图片

4， 将图片转换成二进制或字符串
'''

import sys, smtplib, os, base64, requests, urllib,json, jsonpath, logging, time
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from urllib.request import urlretrieve
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr,formataddr
from multiprocessing import Pool, cpu_count
from PO.FilePO import *
File_PO = FilePO()

class NetPO():

    # 1，发送邮件
    def sendEmail(self, varNickNameByFrom, varFrom, varTo, varSubject, varConent, varFile="", varPic="", varHtmlFileName="", varHtmlContent=""):
        # 发163邮件
        # 注意：邮件主题为‘test’时，会出现错误。
        # 163邮箱需要设置 客户端授权密码为开启，并且脚本中设置的登录密码是授权码
        # 参数：发送者邮箱，接收者邮箱，主题，邮件正文，附件图片，附件文档，附件html名，附件html正文。
        # sendEmail("昵称",'skducn@163.com',"skducn@163.com",
        #           "屏幕劫持",
        #           "开发同学，您好！\n\n\n 以下是本次接口测试报错信息，请检查。\n\n" + "tesst" + "\n\n 如果这不是您的邮件请忽略，很抱歉打扰您，请原谅。\n\n" \
        #           "(这是一封自动产生的email，请勿回复) \n\nCETC测试组 \n\nBest Regards",
        #           "","","",""
        #           )

        # sendEmail("昵称",'skducn@163.com',
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

        try:
            msg = email.mime.multipart.MIMEMultipart()
            # msg['From'] = varFrom   # 发件人：skducn@163.com
            # 自定义处理邮件收发地址的显示内容，如： 令狐冲<skducn@163.com>
            # 将邮件的name转换成utf-8格式，addr如果是unicode，则转换utf-8输出，否则直接输出addr，如：令狐冲<skducn@163.com>
            name, addr = parseaddr(varNickNameByFrom + u' <%s>' % varFrom)
            msg['From'] =formataddr((Header(name, 'utf-8').encode(), addr))  # 发件人： 令狐冲<skducn@163.com>

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
            smtp.login(varFrom, str(base64.b64decode("amluaGFvMTIzbak"), encoding="utf-8"))  # byte转str
            smtp.sendmail(varFrom, varTo, msg.as_string())
            smtp.quit()
            print(u"邮件已发送给：" + str(varTo))
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    # 2.1，获取网站状态码
    def getURLCode(self, varURL):
        # 获取网站的 statuscode，如 200 404 500'''
        try:
            response = requests.get(varURL)
            return response.status_code
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 2.2，获取网站的header
    def getHeaders(self, varURL):
        # 获取网站的header，如:
        # {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'Keep-Alive',
        #  'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Fri, 20 Sep 2019 07:12:16 GMT',
        #  'Last-Modified': 'Mon, 23 Jan 2017 13:23:55 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18',
        #  'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}'''
        try:
            response = requests.get(varURL)
            return response.headers
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 2.3，获取网站内容
    def getHtml(self, varURL):
        # 获取网站内容
        try:
            response = requests.get(varURL)
            return response.text
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    # 3.1，下载程序
    def downloadProgram(self, varUrlFile, varFilePath='./'):
        # 下载文件（显示下载进度，数据块大小，文件大小）
        # Net_PO.downloadFile("https://www.7-zip.org/a/7z1900-x64.exe", "")
        try:
            def reporthook(a, b, c):
                print("\r下载进度: %5.1f%%" % (a * b * 100.0 / c), end="")
            filename = os.path.basename(varUrlFile)
            File_PO.newLayerFolder(varFilePath)  # 强制新增文件夹
            # 判断文件是否存在，如果不存在则下载
            if not os.path.isfile(os.path.join(varFilePath, filename)):
                print('下载数据: %s' % varUrlFile)
                print("保存路径：%s" % varFilePath)
                urlretrieve(varUrlFile, os.path.join(varFilePath, filename), reporthook=reporthook)
                print('\nDownload finished!')
            else:
                print('File already exsits!')
            # 获取文件大小
            filesize = os.path.getsize(os.path.join(varFilePath, filename))
            # 文件大小默认以Bytes计， 转换为Mb
            print('File size = %.2f Mb' % (filesize / 1024 / 1024))
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 3.2，下载网页/图片
    def downloadFile(self, varUrlHtml, varFilePath='./'):
        # 下载页面，将页面保存到本地。
        # Net_PO.downloadHtml(u"http://www.jb51.net/Special/636.htm", "1234.html")
        # File_PO.newLayerFolder(savepath)  # 强制新增文件夹
        try:
            if varFilePath == './':
                varPath, varFile = os.path.split(varUrlHtml)
                urllib.request.urlretrieve(varUrlHtml, varFile)
            else:
                varPath, varFile = os.path.split(varFilePath)
                if varPath == "":
                    urllib.request.urlretrieve(varUrlHtml, varFile)
                else:
                    File_PO.newLayerFolder(varPath)  # 强制新增文件夹
                    urllib.request.urlretrieve(varUrlHtml, varPath + "/" + varFile)
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 3.3，下载图片
    def downloadImage(self, varUrlImage, varFilePath='./'):
        # 下载图片，将网上图片保存到本地。
        # Net_PO.downloadPIC("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg","john.jpg")
        try:
            if varFilePath == './':
                varPath, varFile = os.path.split(varUrlImage)
                sess = requests.Session()
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
                    "Connection": "keep-alive"}
                image = sess.get(varUrlImage, headers=headers).content
                with open(varFile, "wb") as f:
                    f.write(image)
            else:
                varPath, varFile = os.path.split(varFilePath)

                if varFile == "":
                    varPath1, varFile = os.path.split(varUrlImage)

                if varPath == "":
                    sess = requests.Session()
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
                        "Connection": "keep-alive"}
                    image = sess.get(varUrlImage, headers=headers).content
                    with open(varFile, "wb") as f:
                        f.write(image)
                else:
                    File_PO.newLayerFolder(varPath)  # 强制新增文件夹
                    sess = requests.Session()
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36","Connection": "keep-alive"}
                    image = sess.get(varUrlImage, headers=headers).content
                    with open(varPath + "/" + varFile, "wb") as f:
                        f.write(image)
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 3.4，异步多线程下载多张图
    def downloadImageAsync(self, varPathList, varFilePath="./"):
        # https://www.cnblogs.com/nigel-woo/p/5700329.html 多进程知识补遗整理
        # http://www.51testing.com/html/73/n-4471673.html  使用 Selenium 实现谷歌以图搜图爬虫（爬取大图）
        # https://blog.csdn.net/S_o_l_o_n/article/details/86066704 python多进程任务拆分之apply_async()和map_async()
        # 通过异步多线程方式将列表中路径文件下载到当前路径, 只能传入1个参数。
        # https://www.cnblogs.com/c-x-a/p/9049651.html  pool.map的第二个参数想传入多个咋整？
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [*] %(processName)s %(message)s")
        start = time.time()

        # 建立一个进程池，cpu_count() 表示cpu核心数，将进程数设置为cpu核心数
        pool = Pool(cpu_count())
        pool.map_async(Net_PO.downloadImage, varPathList)   # map_async（函数，参数）
        pool.close()
        pool.join()

        end = time.time()
        logging.info(f"{str(cpu_count())}核多线程异步下载 {len(varPathList)} 张图片，耗时 {round(end-start,0)}秒")


    # 4， 将图片转换成二进制或字符串
    def image2strOrByte(self, varImageFile, varMode="str"):
        f = open(varImageFile, "rb")
        img = base64.b64encode(f.read())
        if varMode == "str":
            return (img.decode("utf-8"))  # 转换成字符串
        else:
            return(img)


if __name__ == '__main__':

    Net_PO = NetPO()

    # print("1，发送邮件".center(100, "-"))

    # Net_PO.sendEmail(u'令狐冲', 'skducn@163.com', "h.jin@zy-healthtech.com", "今天的测试","您好！\n\n\n    这是本次集成平台自动化测试结果，请查看附件。\n\n" + "tesst" + "\n\n 这是一封自动产生的email，请勿回复 \n测试组 \nBest Regards","","","","")
    # Net_PO.sendEmail(u'令狐冲', 'skducn@163.com', "h.jin@zy-healthtech.com,skducn@163.com", "今天的测试","您好！\n\n\n    这是本次集成平台自动化测试结果，请查看附件。\n\n\n\n\n\n\n\n这是一封自动产生的email，请勿回复 \n测试组 \nBest Regards","NetPO.py")


    # print("2.1，获取网站状态码".center(100, "-"))
    # print(Net_PO.getURLCode("https://www.baidu.com"))

    # print("2.2，获取网站的header".center(100, "-"))
    # print(Net_PO.getHeaders("https://www.baidu.com"))

    # print("2.3，获取网站内容".center(100, "-"))
    # print(Net_PO.getHtml("https://www.baidu.com"))


    # print("3.1，下载程序".center(100, "-"))
    # Net_PO.downloadProgram("https://www.7-zip.org/a/7z1900-x64.exe")  # 默认将文件保存在当前路径，如果当前目录下已存在此文件则不下载。
    # Net_PO.downloadProgram("https://www.7-zip.org/a/7z1900-x64.exe", "d:/1/2/3")  # 下载 d:/1/2/3到指定目录，如果目录不存在则自动新建。
    # Net_PO.downloadProgram("https://www.7-zip.org/a/7z1900-x64.exe", "/1/2/3")  # 同上，/1/2/3 默认定位当前程序盘符，如 d:/1/2/3

    # print("3.2，下载网页/图片".center(100, "-"))
    # Net_PO.downloadFile(u"http://www.jb51.net/Special/636.htm")  # 默认将html网页保存在当前路径。
    # Net_PO.downloadFile(u"https://images.cnblogs.com/cnblogs_com/longronglang/1061549/o_QQ%E6%88%AA%E5%9B%BE20190727112700.png")  # 默认将图片保存在当前路径。
    # Net_PO.downloadFile(u"http://www.jb51.net/Special/636.htm", "1234.html")  # 默认保存到当前路径，另存为1234.html
    # Net_PO.downloadFile(u"http://www.jb51.net/Special/636.htm", "d:/1/2/3/1234.html")  # 将文件保存在/1/2/3/1234.html下，如果目录不存在则自动新建。

    # print("3.3，下载图片".center(100, "-"))
    # Net_PO.downloadImage("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg")  # 将 kaptcha.jpg 下载保存在当前路径。
    # Net_PO.downloadImage("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg", "test.jpg")  # 将 kaptcha.jpg 下载改名为 test.jpg，保存在当前路径。
    # Net_PO.downloadImage("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg", "d:\\11\\")   # 将 kaptcha.jpg 下载保存在 d:\11目录下，如目录不存在则自动创建
    # Net_PO.downloadImage("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg", "d:\\11\\123.jpg")  # 将 kaptcha.jpg 下载改名为123.jpg 保存在 d:\11目录下，如目录不存在则自动创建
    # Net_PO.downloadImage("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg", "/11/123.jpg")  # 同上

    # print("3.4，异步多线程下载图片".center(100, "-"))
    # Net_PO.downloadImageAsync(["http://img.sccnn.com/bimg/341/08062.jpg", "http://img.sccnn.com/bimg/339/21311.jpg","http://img.sccnn.com/bimg/341/23281.jpg", "http://img.sccnn.com/bimg/341/21281.jpg"],"d:\\test\\")
    # Net_PO.downloadImageAsync([["http://img.sccnn.com/bimg/341/08062.jpg"], ["http://img.sccnn.com/bimg/339/21311.jpg"],["http://img.sccnn.com/bimg/341/23281.jpg"], ["http://img.sccnn.com/bimg/341/21281.jpg"]])

    # print("4，将图片转换成二进制或字符串".center(100, "-"))
    # print(Net_PO.image2strOrByte(r"d:\\test\\aaa.png"))
    # print(Net_PO.image2strOrByte(r"d:\\test\\aaa.png", "byte"))
