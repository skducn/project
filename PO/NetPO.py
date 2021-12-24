# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2017-5-23
# Description: 网络对象（发邮件、下载网页内容、文件、图片
# ***************************************************************

'''
1，发送邮件

2.1，下载程序
2.2，下载网页/图片
2.3，下载图片
2.4，异步多线程下载图片

3， 将图片转换成二进制或字符串
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

    # 1，163邮件发送
    def sendEmail(self, varNickNameByFrom, varTo, varCc, varSubject, varConent, *varAccessory):
        '''

        :param varNickNameByFrom:
        :param varTo:
        :param varCc:
        :param varSubject:
        :param varConent:
        :param varAccessory:  文件可以是多个
        :return:
        # 注意：邮件主题为‘test’时会出现错误。
        # 163邮箱密码为授权密码管理，在设置 - POP/SMTP/IMAP - 授权密码管理 - 新增，并在脚本中设置的登录密码为授权码。
        # 参数：发件人昵称，接收人邮箱，抄送人邮箱，主题，邮件正文，附件。
        '''



        # try:
        msg = email.mime.multipart.MIMEMultipart()
        # msg['From'] = varFrom   # 发件人：skducn@163.com
        # 自定义处理邮件收发地址的显示内容，如： 令狐冲<skducn@163.com>
        # 将邮件的name转换成utf-8格式，addr如果是unicode，则转换utf-8输出，否则直接输出addr，如：令狐冲<skducn@163.com>
        # name, addr = parseaddr(varNickNameByFrom + u' <%s>' % varFrom)
        name, addr = parseaddr(varNickNameByFrom + '<skducn@163.com>' )

        # 发件人
        msg['From'] =formataddr((Header(name, 'utf-8').encode(), addr))

        # 收件人
        if "," in varTo:
            # 为多人
            varTo = [varTo.split(",")[0], varTo.split(",")[1]]
        msg['To'] = ";".join(varTo)

        # 抄送人
        msg['Cc'] = ";".join(varCc)

        reciver = varTo + varCc

        # 主题
        msg['Subject'] = Header(varSubject, 'utf-8').encode()

        # 正文
        txt = MIMEText(varConent, 'plain', 'utf-8')
        msg.attach(txt)

        # 附件
        for i in range(len(varAccessory)):
            # 获取文件类型
            varType = File_PO.isFileType(varAccessory[i])

            # jpg\png\bmp 图片类型
            if "image/" in varType:
                sendimagefile = open(varAccessory[i], 'rb').read()
                image = MIMEImage(sendimagefile)
                # image.add_header('Content-ID', '<image1>')  # 默认文件名
                image.add_header("Content-Disposition", "attachment", filename=("utf-8", "", os.path.basename(varAccessory[i])))
                msg.attach(image)

            # txt\doc\xlsx\json\mp3\mp4\pdf\xmind
            elif "text/plain" or "application/msword" or "spreadsheetml.sheet" or "application/json" or "audio/mpeg" or "video/mp4" or "application/pdf" \
                    or "application/vnd.xmind.workbook" in varType:
                sendfile = open(varAccessory[i], 'rb').read()
                text_att = MIMEText(sendfile, 'base64', 'utf-8')
                text_att["Content-Type"] = 'application/octet-stream'
                # text_att.add_header('Content-Disposition', 'attachment', filename='interface.xls')   # 不支持中文格式文件名
                text_att.add_header("Content-Disposition", "attachment", filename=("utf-8", "", os.path.basename(varAccessory[i])))  # 支持中文格式文件名
                msg.attach(text_att)

            # HTML
            elif "text/html" in varType:
                text_html = MIMEText(varAccessory[i], 'html', 'utf-8')
                text_html.add_header("Content-Disposition", "attachment", filename=("utf-8", "", varAccessory[i]))
                msg.attach(text_html)



        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com', '25')
        smtp.login("skducn@163.com", "MKOMAGNTQDECWXFI")
        smtp.sendmail("skducn@163.com", reciver, msg.as_string())
        smtp.quit()
        print(u"[Ok]，邮件已发送至：" + str(varTo))
        # except:
        #     print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    # 2.1，下载程序
    def downApp(self, vApp, toSave='./'):
        # 下载文件（显示下载进度，数据块大小，文件大小）
        # Net_PO.downloadFile("https://www.7-zip.org/a/7z1900-x64.exe", "")
        try:
            def reporthook(a, b, c):
                print("\r下载进度: %5.1f%%" % (a * b * 100.0 / c), end="")
            filename = os.path.basename(vApp)
            File_PO.newLayerFolder(toSave)  # 新增文件夹
            # 判断文件是否存在，如果不存在则下载
            if not os.path.isfile(os.path.join(toSave, filename)):
                print('应用程序：{}'.format(vApp))
                print("保存路径：{}".format(toSave))
                urlretrieve(vApp, os.path.join(toSave, filename), reporthook=reporthook)
                print("已完成")
            else:
                print('[warning] 文件已存在！')

            # 获取文件大小
            # filesize = os.path.getsize(os.path.join(toSave, filename))
            # 文件大小默认以Bytes计， 转换为Mb
            # print('File size = %.2f Mb' % (filesize / 1024 / 1024))
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 2.2，下载网页/图片
    def downFile(self, varUrlHtml, varFilePath='./'):
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

    # 2.3，下载图片
    def downImage(self, varUrlImage, varFilePath='./'):
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

    # 2.4，异步多线程下载多张图
    def downImageAsync(self, varPathList, varFilePath="./"):
        # https://www.cnblogs.com/nigel-woo/p/5700329.html 多进程知识补遗整理
        # http://www.51testing.com/html/73/n-4471673.html  使用 Selenium 实现谷歌以图搜图爬虫（爬取大图）
        # https://blog.csdn.net/S_o_l_o_n/article/details/86066704 python多进程任务拆分之apply_async()和map_async()
        # 通过异步多线程方式将列表中路径文件下载到当前路径, 只能传入1个参数。
        # https://www.cnblogs.com/c-x-a/p/9049651.html  pool.map的第二个参数想传入多个咋整？
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [*] %(processName)s %(message)s")
        start = time.time()

        # 建立一个进程池，cpu_count() 表示cpu核心数，将进程数设置为cpu核心数
        pool = Pool(cpu_count())
        pool.map_async(Net_PO.downImage, varPathList)   # map_async（函数，参数）
        pool.close()
        pool.join()

        end = time.time()
        logging.info(f"{str(cpu_count())}核多线程异步下载 {len(varPathList)} 张图片，耗时 {round(end-start,0)}秒")



    # 3， 将图片转换成二进制或字符串
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


    # print("2.1，下载程序".center(100, "-"))
    # Net_PO.downApp("https://www.7-zip.org/a/7z1900-x64.exe")  # 默认将文件保存在当前路径，文件存在则不覆盖。
    # Net_PO.downApp("https://www.7-zip.org/a/7z1900-x64.exe", "d:/1/2/3")  # 下载文件到指定目录，目录自动生成。
    # Net_PO.downApp("https://www.7-zip.org/a/7z1900-x64.exe", "/1/2/3")  # 同上，/1/2/3 默认定位当前程序盘符，如 d:/1/2/3

    # print("2.2，下载网页/图片".center(100, "-"))
    # Net_PO.downFile(u"http://www.jb51.net/Special/636.htm")  # 默认将html网页保存在当前路径。
    # Net_PO.downFile(u"https://images.cnblogs.com/cnblogs_com/longronglang/1061549/o_QQ%E6%88%AA%E5%9B%BE20190727112700.png")  # 默认将图片保存在当前路径。
    # Net_PO.downFile(u"http://www.jb51.net/Special/636.htm", "1234.html")  # 默认保存到当前路径，另存为1234.html
    # Net_PO.downFile(u"http://www.jb51.net/Special/636.htm", "d:/1/2/3/1234.html")  # 将文件保存在/1/2/3/1234.html下，如果目录不存在则自动新建。

    # print("2.3，下载图片".center(100, "-"))
    # Net_PO.downImage("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg")  # 将 kaptcha.jpg 下载保存在当前路径。
    # Net_PO.downImage("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg", "test.jpg")  # 将 kaptcha.jpg 下载改名为 test.jpg，保存在当前路径。
    # Net_PO.downImage("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg", "d:\\11\\")   # 将 kaptcha.jpg 下载保存在 d:\11目录下，如目录不存在则自动创建
    # Net_PO.downImage("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg", "d:\\11\\123.jpg")  # 将 kaptcha.jpg 下载改名为123.jpg 保存在 d:\11目录下，如目录不存在则自动创建
    # Net_PO.downImage("http://passport.shaphar.com/cas-webapp-server/kaptcha.jpg", "/11/123.jpg")  # 同上

    # print("2.4，异步多线程下载图片".center(100, "-"))
    # Net_PO.downImageAsync(["http://img.sccnn.com/bimg/341/08062.jpg", "http://img.sccnn.com/bimg/339/21311.jpg","http://img.sccnn.com/bimg/341/23281.jpg", "http://img.sccnn.com/bimg/341/21281.jpg"],"d:\\test\\")
    # Net_PO.downImageAsync([["http://img.sccnn.com/bimg/341/08062.jpg"], ["http://img.sccnn.com/bimg/339/21311.jpg"],["http://img.sccnn.com/bimg/341/23281.jpg"], ["http://img.sccnn.com/bimg/341/21281.jpg"]])

    # print("3，将图片转换成二进制或字符串".center(100, "-"))
    # print(Net_PO.image2strOrByte(r"d:\\test\\aaa.png"))
    # print(Net_PO.image2strOrByte(r"d:\\test\\aaa.png", "byte"))

    # Net_PO.sendEmail("测试组", ['skducn@163.com'], [ 'h.jin@zy-healthtech.com'],
    #           "招远防疫接口自动化测试结果",
    #           "你好，\n\n以下是本次自动化接口测试结果，请查阅。\n\n\n\n这是一封自动生成的email，请勿回复，如有打扰请谅解。 \n\n测试组\nBest Regards",
    #           r'D:\\51\\python\\project\\instance\\zyjk\\epidemic\\interfaceDb\\report123.html', r'D:\\a.jpg', "", ""
    #           )

    Net_PO.sendEmail("测试组", ['skducn@163.com'], [],
              "招远防疫接口自动化测试结果",
              "你好，\n\n以下是本次自动化接口测试结果，请查阅。\n\n\n\n这是一封自动生成的email，请勿回复，如有打扰请谅解。 \n\n测试组\nBest Regards",
              r'D:\\线性代数.xmind', r'd:\\a.jpg'
              )