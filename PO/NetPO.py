# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2017-5-23
# Description: 网络对象（发邮件、下载网页内容、文件、图片
# https://blog.csdn.net/qq_29591261/article/details/120508758  正文表格
# ***************************************************************

'''
1，发送邮件 sendEmail()

2.1，下载程序 downApp()
2.2，下载网页/图片 downFile()
2.3，下载图片  downImage()
2.4，异步多线程下载图片 downImageAsync()

3， 将图片转换成二进制或字符串 image2strOrByte()
'''

import sys, smtplib, os, base64, requests, urllib,json, jsonpath, logging, time
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.application import MIMEApplication
import xlrd
from urllib.request import urlretrieve
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr,formataddr
from multiprocessing import Pool, cpu_count
from PO.FilePO import *
File_PO = FilePO()

class NetPO():

    # 写邮件，读取excel文件内容作为邮件正文
    def mailWrite(self, varExcel):
        # 表格的标题和头
        # header = '<html><head><style type="text/css">table{table-layout: fixed;}td{word-break: break-all; word-wrap:break-word;}</style></head>'
        header = '<style>table{table-layout: fixed;}td{word-break: break-all; word-wrap:break-word;} .mystyle {font-size: 11pt; font-family: Arial;    border-collapse: collapse;     border: 1px solid silver;}.mystyle td, th {    padding: 5px;}.mystyle tr:nth-child(even) {    background: #E0E0E0;}.mystyle tr:hover {    background: silver;    cursor: pointer;}</style><html><head><title>saas高血压接口自动化报告</title></head>'
        # th = '<body text="#000000" ><table border="1" cellspacing="0" cellpadding="3" bordercolor="#000000" width="180" align="left" ><tr bgcolor="#F79646" align="left" ><th>本地地址</th><th>PBU</th></tr>'
        # th = '<body><table cellspacing="0" cellpadding="3" width="100%" border="1">'
        th = '<body><table border="1" class="dataframe mystyle" width="100%">'

        book = xlrd.open_workbook(varExcel)
        sheet = book.sheet_by_index(0)
        nrows = sheet.nrows - 1
        ncols = sheet.ncols
        body = ''
        # 标题
        td = ''
        for j in range(ncols):
            cellData = sheet.cell_value(0, j)
            tip = '<th style="min-width: 100px;"bgcolor="#90d7ec">' + str(cellData) + '</th>'
            td = td + tip
            tr = '<tbody><thead><tr>' + td + '</tr></thead>'
        body = body + tr

        # 内容
        # cellData = 1
        for i in range(1, nrows + 1):
            td = ''
            for j in range(ncols):
                cellData = sheet.cell_value(i, j)
                tip = '<td>' + str(cellData) + '</td>'
                td = td + tip
                tr = '<tr>' + td + '</tr>'
            body = body + tr
        return  header + th  + body + '</tbody></table></body></html>'

    # 1，163邮件发送
    def sendEmail(self, varAddresser, varTo, varCc, varSubject, varMIMEText, varHead, varConent, varFoot, *varAccessory):
        '''

        :param varAddresser:
        :param varTo:
        :param varCc:
        varHead : 页眉
        :param varSubject:
        varFoot ：页脚
        :param varMIMEText: html/plain
        :param varConent:
        :param varAccessory:  文件可以是多个,用逗号分隔。
        :return:
        # 注意：邮件主题为‘test’时会出现错误。
        # 163邮箱密码为授权密码管理，在设置 - POP/SMTP/IMAP - 授权密码管理 - 新增，并在脚本中设置的登录密码为授权码。
        # 参数：发件人昵称，接收人邮箱，抄送人邮箱，主题，正文类型，正文，附件。
        '''

        # try:
        msg = email.mime.multipart.MIMEMultipart()
        # msg['From'] = varFrom   # 发件人：skducn@163.com
        # 自定义处理邮件收发地址的显示内容，如： 令狐冲<skducn@163.com>
        # 将邮件的name转换成utf-8格式，addr如果是unicode，则转换utf-8输出，否则直接输出addr，如：令狐冲<skducn@163.com>
        # name, addr = parseaddr(varAddresser + u' <%s>' % varFrom)
        name, addr = parseaddr(varAddresser + '<skducn@163.com>' )

        # 发件邮箱
        msg['From'] =formataddr((Header(name, 'utf-8').encode(), addr))

        # 收件邮箱
        if "," in varTo:
            # 多个邮箱用逗号分隔
            varTo = [varTo.split(",")[0], varTo.split(",")[1]]
        msg['To'] = ";".join(varTo)

        # 抄送邮箱
        if varCc != None:
            msg['Cc'] = ";".join(varCc)
            # 所有接收邮箱
            reciver = varTo + varCc
        else:
            reciver = varTo

        # 主题
        msg['Subject'] = Header(varSubject, 'utf-8').encode()

        # 正文
        # 调用外部html文件
        if varMIMEText == "htmlFile":
            with open(varConent, 'r', encoding='utf-8') as f:
                varConent = f.read()
            varConent = varHead + varConent + varFoot
            html = MIMEText(varConent, 'html', 'utf-8')
        # html格式的变量
        elif varMIMEText == "htmlContent":
            html = MIMEText(varConent, 'html', 'utf-8')
        # excel转html格式
        elif varMIMEText == "excel":
            varConent = self.mailWrite(varConent)
            # print(varConent)
            # sys.exit(0)
            varConent = varHead + varConent + varFoot
            html = MIMEText(varConent, 'html', 'utf-8')
        # 文本格式
        else:
            varConent = varHead + varConent + varFoot
            html = MIMEText(varConent, 'plain', 'utf-8')
        msg.attach(html)

        # 附件
        for i in range(len(varAccessory)):
            # 获取文件类型
            varType = File_PO.isFileType(varAccessory[i])

            # jpg\png\bmp
            if "image/" in varType:
                sendimagefile = open(varAccessory[i], 'rb').read()
                image = MIMEImage(sendimagefile)
                # image.add_header('Content-ID', '<image1>')  # 默认文件名
                image.add_header("Content-Disposition", "attachment", filename=("utf-8", "", os.path.basename(varAccessory[i])))
                msg.attach(image)

            # html\txt\doc\xlsx\json\mp3\mp4\pdf\xmind
            elif "text/html" or "text/plain" or "application/msword" or "spreadsheetml.sheet" or "application/json" or "audio/mpeg" or "video/mp4" or "application/pdf" \
                    or "application/vnd.xmind.workbook" in varType:
                sendfile = open(varAccessory[i], 'rb').read()
                text_att = MIMEText(sendfile, 'base64', 'utf-8')
                text_att["Content-Type"] = 'application/octet-stream'
                # text_att.add_header('Content-Disposition', 'attachment', filename='interface.xls')   # 不支持中文格式文件名
                text_att.add_header("Content-Disposition", "attachment", filename=("utf-8", "", os.path.basename(varAccessory[i])))  # 支持中文格式文件名
                msg.attach(text_att)

        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com', '25')
        smtp.login("skducn@163.com", "MKOMAGNTQDECWXFI")
        smtp.sendmail("skducn@163.com", reciver, msg.as_string())
        smtp.quit()
        print(u"邮件已发送给：" + str(reciver) + "")



    def data_to_html(self,data, title):
        alarm_html = '<table border="1" cellpadding="5"><tr>'
        for item in title:
            alarm_html += '<td>%s</td>' % item
        alarm_html += '</tr>'

        for row in data:
            alarm_html += '<tr>'
            for item in row:
                alarm_html += '<td>%s</td>' % item
            alarm_html += "</tr>"
        alarm_html += "</table>"
        return alarm_html


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

    print("1.1 发邮件之文本正文".center(100, "-"))
    # Net_PO.sendEmail("测试组", [ 'h.jin@zy-healthtech.com'], ['skducn@163.com'],
    #                  "发邮件之文本正文", "plain", "你好", "\n\n附件是本次自动化接口测试结果，请查阅。",
    #                  "\n\n这是一封自动生成的email，请勿回复，如有打扰请谅解。 \n\n测试组\nBest Regards",
    #                  r'D:\\51\\python\\project\\PO\\data\\report123.html'
    #                 )
    # Net_PO.sendEmail("测试组", ['h.jin@zy-healthtech.com'], None,
    #                  "发邮件之文本正文", "plain", "你好", "\n\n附件是本次自动化接口测试结果，请查阅。",
    #                  "\n\n这是一封自动生成的email，请勿回复，如有打扰请谅解。 \n\n测试组\nBest Regards",
    #                  r'./data/report123.html', r'/Users/linghuchong/Desktop/mac/cetc.png'
    #                  )


    # print("1.2 发邮件之表格正文".center(100, "-"))
    # titles = ['表头1', '表头2', '表头3', '表头4', '表头5']
    # data = [
    #     ['小学', '语文', 1, 1, 3],
    #     ['小学', '数学', 1, 5, 1],
    #     ['小学', '语文', 1, 1, 33],
    #     ['初中', '数学', 13, 1, 15],
    #     ['高中', '数学', 1, 1, 1],
    #     ['小学', '英语', 1, 8, 1],
    #     ['小学汇总', '小学汇总', 1, 1, 1],
    #     ['初中', '数学', 13, 1, 15],
    #     ['小学', '语文', 1, 1, 33],
    #     ['高中汇总', '高中汇总', 13, 1, 15]
    # ]
    # varConent = Net_PO.data_to_html(data, titles)
    # Net_PO.sendEmail("测试组", ['h.jin@zy-healthtech.com'], None,
    #                  "发邮件之表格正文", "html", varHead, varConent, varFoot
    #                  )


    # print("1.3.1 发邮件之html正文(html内容)".center(100, "-"))
    # varConent = """
    #     <html lang = "en"
    #     <body>
    #     <table id="header" bgcolor="#020D3D" cellpadding="5" width="100%" style="background-image: url('https://cloud.ibm.com/avatar/v1/avatar/migrate-bluemix-photos-production/1b0b8d80-6292-11e9-8868-e948ac984fd4.png'); background-position: top right; background-repeat: no-repeat; background-size: cover; background-color: #020D3D;" background="https://cloud.ibm.com/avatar/v1/avatar/migrate-bluemix-photos-production/1b0b8d80-6292-11e9-8868-e948ac984fd4.png">
    #     <tbody>
    #     <tr>
    #     <td><img alt="IBM Cloud" src="https://cloud.ibm.com/avatar/v1/avatar/migrationsegment/IBM_Cloud_Lockup_Rev_RGB.png" style="width: 175px; height: 68px;" width="175"></td>
    #     </tr>
    #     </tbody>
    #     </table>
    #     <h1>您好！<h1>
    #     <h1>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本次项目接口自动化测试已完成，请查看附件。<h1>
    #     <h1>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这是一封自动发送的电子邮件，如有打扰请谅解，请联系我们。<h1>
    #     <h1>智赢测试组<h1>
    #     <h1>Best Regards<h1>
    #     </body>
    #     </html>
    # """
    # Net_PO.sendEmail("测试组", ['h.jin@zy-healthtech.com'], None,
    #           "发送邮件html正文(html内容)", "htmlContent", "", varConent, "",
    #           )


    # print("1.3.2 发邮件之html正文(html文件)".center(100, "-"))
    # varHead = "<h3>您好！</h3>"
    # varFoot = """<br>
    #    <h3>这是一封自动发送的电子邮件，如有打扰请谅解，请联系我们。</h3>
    #    <h3>智赢测试组</h3>
    #    <h3>Best Regards</h3>
    #    """
    # Net_PO.sendEmail("测试组", ['h.jin@zy-healthtech.com'], None,
    #           "发送邮件html正文(html文件)", "htmlFile", varHead, "./data/report.html", varFoot,
    #           )


    print("1.4 发邮件之excel正文".center(100, "-"))
    varHead = "<h3>您好！</h3>"
    varFoot = """<br>
       <h3>这是一封自动发送的电子邮件，如有打扰请谅解，请联系我们。</h3>
       <h3>智赢测试组</h3>
       <h3>Best Regards</h3>
       """
    Net_PO.sendEmail("测试组", ['h.jin@zy-healthtech.com'], None,
                     "发邮件之excel正文", "excel", varHead, "./data/demo.xlsx", varFoot,
                     r"./data/demo.xlsx"
                     )



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


