# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2016-7-29
# Description   : 场景鹿1.0接口驱动
# *******************************************************************************************************************************
from xlutils.copy import copy
from CJLinterfaceParam import *
# *******************************************************************************************************************************



def getCJLverifyCode(mobilephone):
    # 从redis中获取登录验证码
    if connRedis167.exists("login:app:login:" + str(mobilephone)) == True :
        r = connRedis167.get("login:app:login:" + str(mobilephone))
        return r  # 2343
    else:
        print "[errorrrrrrrrr , getCJLverifyCode函数无返回值]"

def getCJLuserID(mobilephone):
    # 获取redis的userId
    if connRedis167.hexists("login:app:user:" + mobilephone, "userId") == True :
        r = connRedis167.hget("login:app:user:" + mobilephone, "userId")
        return r  # 10000022
    else:
        print "[errorrrrrrrrr , getCJLuserID函数无返回值]"

def getCJLsceneDto_310100_id(userId):
    # 获取公共场景ID
    c = db.SceneDto_310100.find({"userId": userId})
    return c[0]['_id']   #  G_10000163

def getCJLsceneAlbumDto_id(userId, sceneId):
    # 获取场景相册mainID
    b = db.sceneAlbumDto.find({"sceneId": sceneId, "userId": userId})
    return b[0]['_id']  # ObjectId("5832b20db13651f5dab52eb4")

def getCJLsceneDto_310101_info(comID):
    # 输出公共场景ID、公共场景名、公共场景地址
    a = db.SceneDto_310100.find({"_id": comID})
    return (a[0]['sceneName'],a[0]['address'])

def assertEqual(expected,actual,okmessage,errmessage):
    # 断言输出提示，参1=预期值 ,参2=实测值 ,参3=正确提示 ,参4=错误提示
    if expected == actual :
        print okmessage
    else:
        print errmessage

def uploadfile(exlString):
    # 文件上传
    varLists = exlString.split(",")
    params = {varLists[2]: varLists[3], varLists[4]:open(varLists[5], 'rb'), 'userId': getCJLuserID(myPhone)}
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler.MultipartPostHandler)
    res = opener.open(testURL + varLists[1], params)
    sleep(2)
    xx = res.read()
    if "success\":true" in xx: return 0,xx
    else: return 1, xx

def sendemail(subject, text, *attachmentFilePaths):
    gmailUser = 'jinhao@mo-win.com.cn'
    gmailPassword = 'Dlhy123456'
    recipient = 'jinhao@mo-win.com.cn'
    # recipient = "'jinhao@mo-win.com.cn', 'guoweiliang@mo-win.com.cn'"
    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'plain', 'utf-8'))
    # 附件是可选项
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
        attachment = MIMEImage(file.read(), subType=subType)
    elif mainType == 'audio':
        attachment = MIMEAudio(file.read(), subType=subType)
    else:
        attachment = MIMEBase(mainType, subType)
    attachment.set_payload(file.read())
    encode_base64(attachment)
    file.close()
    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachmentFilePath))
    return attachment

def Icase(exlNo,RtnStatus,varUserId,exlParams):
    bk = xlrd.open_workbook(varExcel, formatting_info=True)
    newbk = copy(bk)
    styleBlue = xlwt.easyxf('font: height 340 ,name Times New Roman, color-index blue')
    # ('font: height 240, name Arial, colour_index black, bold off, italic on; align: wrap on, vert centre, horiz left;')
    styleRed = xlwt.easyxf('font: height 340 ,name Times New Roman, color-index red')
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT # 自动换行
    styleRed.alignment = alignment
    styleBlue.alignment = alignment
    exlSheetNums = len(bk.sheet_names())
    l_exlSheetNames = bk.sheet_names()
    l_exlSheetNames2 = []
    l_exlSheetSingleNum = []
    for i in range(exlSheetNums):
        l_exlSheetNames2.append(l_exlSheetNames[i].encode('raw_unicode_escape'))
        l_exlSheetSingleNum.append(i)
    d_exlSheet = dict(zip(l_exlSheetNames2,l_exlSheetSingleNum))
    sheetNum = bk.sheet_by_name(exlNo.split("_", 1)[0])
    sheetSetup = bk.sheet_by_name("setup")


    exlNo2 = exlNo.split("_", 2)[1][1:]  # 获取接口序号
    floatExlNo = float(exlNo2)
    floatExlNoaddone = float(int(exlNo2)+1)
    exlAllInterfaceNum = startCode = endCode = exlAllInterfaceNumEmpty = exlIsCancel = 0  # exlAllInterfaceNum = 接口总数量 , 开始编号,结束编号
    l_exlAllInterfaceNum = []  # 接口序号明细
    l_exlAllInterfaceNumEmpty = []
    l_exlParams = []  # 一个接口的所有参数名称

    for i in range(1,sheetNum.nrows): # 获取接口总数量 及 接口序号明细
        if sheetNum.cell_value(i, 0) != "":
            exlAllInterfaceNum = exlAllInterfaceNum+1
            l_exlAllInterfaceNum.append(sheetNum.cell_value(i, 0))
            l_exlAllInterfaceNumEmpty.append(exlAllInterfaceNum+exlAllInterfaceNumEmpty+1)  # result
        else: exlAllInterfaceNumEmpty = exlAllInterfaceNumEmpty + 1
    d_SerialRow=dict(zip(l_exlAllInterfaceNum,l_exlAllInterfaceNumEmpty))

    if floatExlNo in l_exlAllInterfaceNum:
        for j in range(0,sheetNum.nrows):
            startCode = startCode + 1
            varThirdway = 0
            if sheetNum.cell_value(j, 0) == floatExlNo :
                exlInterfaceName = sheetNum.cell_value(j, 1)
                exlInterfaceUrl = sheetNum.cell_value(j, 2)

                if "#" in exlInterfaceUrl :   # 调用第三方函数
                    exlInterfaceUrl = exlInterfaceUrl.encode("utf-8")
                    exlInterfaceUrl = exlInterfaceUrl.replace("#", "")
                    # varNums = len(exlInterfaceUrl.split(","))
                    # varLists = exlInterfaceUrl.split(",")
                    varThirdway = 1
                    varNums = len(exlInterfaceUrl.split(","))
                    varLists = exlInterfaceUrl.split(",")

                    if "http" in exlParams:
                        exlInterfaceUrl = varLists[0] +"," + varLists[1] +","+ varLists[2] +","+ exlParams +","+ varLists[4] +","+ varLists[5]
                    varRtnStatus,varJson = eval(varLists[0])(exlInterfaceUrl)
                    # varRtnStatus,varJson = eval(varLists[0])(varLists[1],varLists[2],varLists[3],varLists[4],varLists[5])

                exlInterfaceReturn = sheetNum.cell_value(j, 7)
                exlInterfaceReturn = exlInterfaceReturn.encode("utf-8")   # unicode 2 str
                exlSevendays = sheetNum.cell_value(j,8)
                exlRow = d_SerialRow.get(floatExlNo, 'not found')
                if sheetNum.cell_value(j, 6) == "Y":
                    exlIsCancel = 1
                    break
                break

        if floatExlNoaddone in l_exlAllInterfaceNum:
            for j in range(0, sheetNum.nrows):
                endCode = endCode + 1
                if sheetNum.cell_value(j, 0) == floatExlNoaddone:
                    break
        else: endCode = sheetNum.nrows+1

        if varThirdway == 1 and exlIsCancel != 1:
            if sheetSetup.cell_value(5, 1) == "Y":
                print "     >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                print "     请求函数1 = " + varLists[0]
                print "     请求参数 = " + varLists[1] + " , " + varLists[2] + " , " + varLists[3]
                # print "[errorrrrrrr , RtnOK] " + exlNo + "," + exlInterfaceName + " => " + varJson

            for k in d_exlSheet:
                if k == exlNo.split("_", 1)[0]:
                    newWs = newbk.get_sheet(d_exlSheet[k])

            if varRtnStatus == 0:
                newWs.write(exlRow-1, 5, "OK", styleBlue)
                if sheetSetup.cell_value(4, 1) != "Error":
                    print "[OK , RtnOK] " + exlNo + "," + exlInterfaceName + " => " + varJson
                varResult = 0
            elif varRtnStatus == 1:
                newWs.write(exlRow-1, 5, "Error", styleRed)
                varResult = 1
                print "     请求函数2 = " + exlInterfaceUrl
                print "[errorrrrrrr , RtnOK] " + exlNo + "," + exlInterfaceName + " => " + varJson

            newbk.save(varExcel)
            return varJson

        elif exlIsCancel != 1:

            for k in range(startCode-1, endCode-1):
                l_exlParams.append(sheetNum.cell_value(k, 3).encode('raw_unicode_escape'))  # 去掉列表中 带u前缀符号

            requestURL = testURL + exlInterfaceUrl

            # print exlParams
            if exlParams != "" : Params = dict(zip(l_exlParams, list(eval(exlParams))))
            # print Params

            query1 = {}
            if len(varUserId) == 4:
                query1["code"] = connRedis167.get("login:app:login:" + exlParams.split(",")[0])
            else:
                if connRedis167.exists("app:verify:"+str(varUserId)):
                    varCode = connRedis167.hget("app:verify:"+str(varUserId), "code")
                else:
                    varCode = connRedis167.hget("login:tmpverify:"+str(varUserId), "code")
                query1["verifyCode"] = varCode
                query1["verifyUserId"] = str(varUserId)
                query1["userId"] = str(varUserId)

            if exlParams != "":
                for x in Params:
                    query1[x] = str(Params[x])

            emailIcase = "Icase(" + "\"" + str(exlNo) + "\"""," + "\"" + RtnStatus + "\"""," + "\"" + varUserId + "\""",'""" + exlParams +"')"

            if sheetSetup.cell_value(5, 1) == "Y":
                print "     测试用例 = " + str(emailIcase)
                print "     请求参数 = " + str(query1)
                sum = ""
                symble = "&"
                for k, v in query1.items():
                    x= ('{}={}'.format(k, v))
                    sum = x + symble + sum
                print "     测试链接 = " + requestURL + "?" + sum

            headers = {'cache-control': "no-cache"}
            requests.packages.urllib3.disable_warnings()
            response = requests.request("GET", requestURL, headers=headers, params=query1, verify=False)
            try:
                for k in d_exlSheet:
                    if k == exlNo.split("_", 1)[0]:
                        newWs = newbk.get_sheet(d_exlSheet[k])

                if RtnStatus == "RtnOK":
                    if response.json()['success'] == True :
                        if exlInterfaceReturn == "" and response.json()['data'] != None :
                            varRtnStatus = 0
                        elif exlInterfaceReturn == "null" and response.json()['data'] == None:
                            varRtnStatus = 0
                        elif exlInterfaceReturn == "dataList" and 'dataList' in response.json()['data']:
                            if response.json()['data']['dataList'] == []:
                                print "[warning , 默认第一次datalist为空]"
                                varRtnStatus = 0   # 暂时设置为正确，
                            else:varRtnStatus = 0
                        else:varRtnStatus = 1
                    else: varRtnStatus = 1

                if RtnStatus == "RtnSysErr":
                    if response.json()['errorcode'] == 100001 and response.json()['success'] == False: varRtnStatus = 0
                    else: varRtnStatus = 1

                if RtnStatus == "RtnParamErr":
                    if response.json()['errorcode'] == 100002 and response.json()['success'] == False: varRtnStatus = 0
                    else: varRtnStatus = 1

                if RtnStatus == "RtnDeviceErr":
                    if response.json()['errorcode'] == 100003 and response.json()['success'] == False: varRtnStatus = 0
                    else: varRtnStatus = 1

                # if RtnStatus == "RtnNoDATAOK" : # 如:{"data":[],"errorstr":"","errorcode":0,"success":true}
                #     if response.json()['success'] == True and response.json()['data'] == []: varRtnStatus = 0
                #     else: varRtnStatus = 1

                if varRtnStatus == 0:
                    newWs.write(exlRow-1, 5, "OK", styleBlue)
                    if sheetSetup.cell_value(4, 1) != "Error":
                        print "[OK , " + RtnStatus + "] " + exlNo + "," + exlInterfaceName + " => " + response.content
                    varResult = 0
                elif varRtnStatus == 1:
                    newWs.write(exlRow-1, 5, "Error", styleRed)
                    varResult = 1
                    print "     测试用例 = " + str(emailIcase)
                    print "     请求参数 = " + str(query1)
                    sum = ""
                    symble = "&"
                    for k, v in query1.items():
                        x = ('{}={}'.format(k,v))
                        sum = x + symble + sum
                    print "     测试链接 = " + requestURL + "?" + sum
                    print "[errorrrrrrrrrr , " + RtnStatus + "] " + exlNo + "," + exlInterfaceName + " => " + response.content
                    # print "[warning , 默认第一次datalist为空]"

                    if sheetSetup.cell_value(2, 1) == "Y":
                        # 带附件
                        sendemail(exlNo + exlInterfaceName + u"报错!!!", u'你好，接口报错了，帮忙看一下吧。\n\n        测试用例 = ' + emailIcase + u'\n\n        请求参数 = ' + str(query1) + u'\n\n        测试链接 = ' + requestURL + u'?' + sum + u'\n\n        返回结果 = ' + response.content + u'\n\n\n本邮件是自动发送，如有打扰请谅解。\n\n', varExcel)
                        # 不带附件
                        # sendemail(exlNo + exlInterfaceName + "报错!!!", "你好，啊呦喂，接口报错了，帮忙看一下吧。\n\n        测试用例 = " + emailIcase + "\n\n        请求参数 = " + str(query1) + "\n\n        测试链接 = " + requestURL + "?" + sum + "\n\n        返回结果 = " + response.content + "\n\n\n本邮件是自动发送，如有打扰请谅解。\n\n", '')

                if sheetSetup.cell_value(3, 1) == "Y":
                    if varResult == 0:
                        if exlSevendays == "":
                            exlSevendays = str(datetime.date.today()) + "(OK)"
                        else:
                            if exlSevendays.count("/") == 6:
                                if str(datetime.date.today()) not in exlSevendays:
                                    exlSevendaysNew = ""
                                    strlist = exlSevendays.split('/')
                                    for i in range(6):
                                        exlSevendaysNew = exlSevendaysNew + "/" + strlist[i]
                                    exlSevendays = str(datetime.date.today()) + "(OK)" + exlSevendaysNew
                            else:
                                if str(datetime.date.today()) not in exlSevendays:
                                    exlSevendays = str(datetime.date.today()) + "(OK) / " + exlSevendays
                        styleBlue = xlwt.easyxf('font: height 260 ,name Times New Roman, color-index blue')
                        alignment = xlwt.Alignment()
                        alignment.horz = xlwt.Alignment.HORZ_CENTER
                        alignment.vert = xlwt.Alignment.VERT_CENTER
                        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT # 自动换行
                        styleBlue.alignment = alignment
                        newWs.write(exlRow-1, 8, exlSevendays, styleBlue)
                    elif varResult == 1:
                        if exlSevendays == "":
                            exlSevendays = str(datetime.date.today()) + "(error)"
                        else:
                            if exlSevendays.count("/") == 6:
                                if str(datetime.date.today()) not in exlSevendays:
                                    exlSevendaysNew = ""
                                    strlist = exlSevendays.split('/')
                                    for i in range(6):
                                        exlSevendaysNew = exlSevendaysNew + "/" + strlist[i]
                                    exlSevendays = str(datetime.date.today()) + "(error)" + exlSevendaysNew
                            else:
                                if str(datetime.date.today()) not in exlSevendays:
                                    exlSevendays = str(datetime.date.today()) + "(error) / " + exlSevendays
                        styleRed = xlwt.easyxf('font: height 260 ,name Times New Roman, color-index red')
                        alignment = xlwt.Alignment()
                        alignment.horz = xlwt.Alignment.HORZ_CENTER
                        alignment.vert = xlwt.Alignment.VERT_CENTER
                        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT # 自动换行
                        styleRed.alignment = alignment
                        newWs.write(exlRow-1, 8, exlSevendays, styleRed)

                newbk.save(varExcel)
                return response.json()['data']
                varRtnStatus = 0
            except Exception, data:
                print Exception, ":", data, "\n"
        else:
            for k in d_exlSheet:
                if k == exlNo.split("_", 1)[0]:
                    newWs = newbk.get_sheet(d_exlSheet[k])
            alignment = xlwt.Alignment() # Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
            alignment.vert = xlwt.Alignment.VERT_CENTER # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
            alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT # 自动换行
            style = xlwt.XFStyle() # Create Style
            style.alignment = alignment # Add Alignment to Style
            pattern = xlwt.Pattern() # Create the Pattern
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
            pattern.pattern_fore_colour = 2 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
            style.pattern = pattern # Add Pattern to Style
            newWs.write(exlRow-1, 0, int(exlNo2), style)
        newbk.save(varExcel)
    else:
        print "[errorrrrrrrrr , 表格中未找到 " + str(exlNo)+ " 序号,请检查... ]"
