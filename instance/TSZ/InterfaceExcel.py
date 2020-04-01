# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: 接口驱动模版
#****************************************************************
# 使用说明:
# 接口调用使用方法: Icase("参数1","参数2","参数3",'"**参数4"')
# 例子:Icase("I251_N28_C1","RtnOK","10001482",'"13","10001577","1577店小二"')
# 参数1 = 接口坐标定位,由三部分组成 "excel工作表_序号_用例编号" , 如"I251_N6_C1" 对应excel中工作表I251序号为6的测试用例1 .
# 参数2 = 测试返回类型
# 参数3 = userID
# **参数4 = 开发接口文档的请求参数列表 (注意:各参数用逗号分隔,且最外层有单引号 ' ,如 '"userid","groupId","memberId"')
# 如果接口的正确返回值是 {"data":null,"errorstr":"","errorcode":0,"success":true} ,请使用 "RtnNullOK" 作为测试返回类型,否则用 RtnOK.
# 如果接口的正确返回值是 {"data":[],"errorstr":"","errorcode":0,"success":true} ,请使用 "RtnNoDATAOK" 作为测试返回类型,否则用 RtnOK.

import os,sys,requests,xlwt,xlrd,MySQLdb,datetime,redis,smtplib
reload(sys)
sys.setdefaultencoding('utf8')
from email.mime.text import MIMEText
from email.header import Header
from time import sleep
from xlutils.copy import copy
ExcelFile = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/excel/InterfaceExcel.xls"
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

def assertEqual(expected,actual,okmessage,errmessage):
    # 功能:用于检查表数据
    # 参数1=预期值 ,参数2=实测值 ,参数3= 输出正确提示,参数4=输出错误提示
    if expected == actual : print okmessage
    else: print errmessage

def Icase(exlNo,RtnStatus,varUserId,exlParams):
    bk = xlrd.open_workbook(ExcelFile,formatting_info=True)
    newbk=copy(bk)
    styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
    styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
    exlSheetNums=len(bk.sheet_names())
    l_exlSheetNames = bk.sheet_names()
    l_exlSheetNames2=[]
    l_exlSheetSingleNum=[]
    for i in range(exlSheetNums):
        l_exlSheetNames2.append(l_exlSheetNames[i].encode('raw_unicode_escape'))
        l_exlSheetSingleNum.append(i)
    d_exlSheet=dict(zip(l_exlSheetNames2,l_exlSheetSingleNum))
    sheetNum = bk.sheet_by_name(exlNo.split("_",1)[0])
    sheetSetup = bk.sheet_by_name("setup")

    exlNo2 =exlNo.split("_",2)[1][1:]  # 获取接口序号
    floatExlNo = float(exlNo2)
    floatExlNoaddone = float(int(exlNo2)+1)
    exlAllInterfaceNum=startCode=endCode=exlAllInterfaceNumEmpty=exlIsCancel=0  # exlAllInterfaceNum = 接口总数量 , 开始编号,结束编号
    l_exlAllInterfaceNum=[]  # 接口序号明细
    l_exlAllInterfaceNumEmpty=[]
    l_exlParams=[]  # 一个接口的所有参数名称

    for i in range(1,sheetNum.nrows): # 获取接口总数量 及 接口序号明细
        if sheetNum.cell_value(i,0) <>"":
            exlAllInterfaceNum=exlAllInterfaceNum+1
            l_exlAllInterfaceNum.append(sheetNum.cell_value(i,0))
            l_exlAllInterfaceNumEmpty.append(exlAllInterfaceNum+exlAllInterfaceNumEmpty+1)  # result
        else: exlAllInterfaceNumEmpty=exlAllInterfaceNumEmpty+1
    d_SerialRow=dict(zip(l_exlAllInterfaceNum,l_exlAllInterfaceNumEmpty))

    if floatExlNo in l_exlAllInterfaceNum:
        for j in range(0,sheetNum.nrows):
            startCode=startCode+1
            if sheetNum.cell_value(j,0) == floatExlNo :
                exlInterfaceName = sheetNum.cell_value(j,1)
                exlInterfaceUrl = sheetNum.cell_value(j,2)
                exlSevendays = sheetNum.cell_value(j,7)

                exlRow = d_SerialRow.get(floatExlNo, 'not found')
                if sheetNum.cell_value(j,6) == "Y" :
                    exlIsCancel = 1
                    break
                break
        if floatExlNoaddone in l_exlAllInterfaceNum:
            for j in range(0,sheetNum.nrows):
                endCode=endCode+1
                if sheetNum.cell_value(j,0) == floatExlNoaddone:
                    break
        else: endCode=sheetNum.nrows+1

        if exlIsCancel <> 1:
            for k in range(startCode-1,endCode-1):
                l_exlParams.append(sheetNum.cell_value(k,3).encode('raw_unicode_escape'))  # 去掉列表中 带u前缀符号
            exlInterfaceUrl = "http://192.168.2.176:9999" + exlInterfaceUrl
            # print exlParams
            if exlParams <>"" :Params = dict(zip(l_exlParams,list(eval(exlParams))))
            # print Params
            r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
            varCode = r.hget("app:verify:"+str(varUserId),"code")
            query1={}
            query1["verifyUserId"] = str(varUserId)
            query1["userId"] = str(varUserId)
            query1["verifyCode"]= varCode
            varRtnStatus = 0
            if exlParams <> "" :
                for x in Params:
                    query1[x] = str(Params[x])

            # print " " * 15 + "[ " + exlNo + " ]" + ">" * 135

            emailIcase = "Icase(" + "\"" + str(exlNo) + "\"""," + "\"" + RtnStatus + "\"""," + "\"" + varUserId + "\""",'""" + exlParams +"')"
            # if sheetSetup.cell_value(5, 1) == "Y":
            #     print "     >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            #     print "     请求链接 = " + exlInterfaceUrl
            #     print "     请求参数 = " + str(query1)
            #     print "     测试用例 = " + str(emailIcase)

            headers = {'cache-control': "no-cache"}
            response = requests.request("GET", exlInterfaceUrl, headers=headers, params=query1)
            try:
                for k in d_exlSheet:
                    if k == exlNo.split("_", 1)[0]:
                        newWs=newbk.get_sheet(d_exlSheet[k])

                if RtnStatus == "RtnNullOK" :  #如:{"data":null,"errorstr":"","errorcode":0,"success":true}
                    if response.json()['success']==True:varRtnStatus = 0
                    else: varRtnStatus = 1

                if RtnStatus == "RtnOK" : #如:{"data":149,"errorstr":"","errorcode":0,"success":true}
                    if response.json()['success']==True and response.json()['data']<>None :
                        varRtnStatus = 0

                    else:varRtnStatus = 1

                if RtnStatus == "RtnNoDATAOK" : # 如:{"data":[],"errorstr":"","errorcode":0,"success":true}
                    if response.json()['success'] == True and response.json()['data'] == []:varRtnStatus = 0
                    else:varRtnStatus = 1

                if RtnStatus=="RtnSysErr" :
                    if response.json()['errorcode']==100001 and response.json()['success']== False:varRtnStatus = 0
                    else:varRtnStatus = 1

                if RtnStatus=="RtnParamErr" :
                    if response.json()['errorcode']==100002 and response.json()['success']== False:varRtnStatus = 0
                    else:varRtnStatus = 1

                if RtnStatus=="RtnDeviceErr" :
                    if response.json()['errorcode']==100003 and response.json()['success']== False:varRtnStatus = 0
                    else:varRtnStatus = 1

                if varRtnStatus == 1:
                    alignment = xlwt.Alignment()
                    alignment.horz = xlwt.Alignment.HORZ_CENTER
                    alignment.vert = xlwt.Alignment.VERT_CENTER
                    styleRed.alignment = alignment
                    newWs.write(exlRow-1,5,"Error",styleRed)
                    print "     ------------------------------------------------------------------------------------------------"
                    print "     请求链接 = " + exlInterfaceUrl
                    print "     请求参数 = " + str(query1)
                    print "     测试用例 = " + str(emailIcase)
                    print "[errorrrrrrrrrr , " + RtnStatus + "] " + exlNo  + ","  + exlInterfaceName + " => " + response.content
                    if sheetSetup.cell_value(2,1)=="Y" :
                        pass
                        # sendemail(exlNo + "," + exlInterfaceName, emailIcase + "\n\n" + "[errorrrrrrrrrr," + RtnStatus + "] => " + response.content)

                if varRtnStatus == 0:
                    alignment = xlwt.Alignment()
                    alignment.horz = xlwt.Alignment.HORZ_CENTER
                    alignment.vert = xlwt.Alignment.VERT_CENTER
                    styleBlue.alignment = alignment
                    newWs.write(exlRow-1,5,"OK",styleBlue)
                    if sheetSetup.cell_value(4,1) <> "Error":

                        print "[OK , " + RtnStatus + "] " + exlNo + "," + exlInterfaceName + " => " + response.content

                    if sheetSetup.cell_value(3,1) == "Y":
                        if exlSevendays == "":
                            exlSevendays = str(datetime.date.today()) + "(OK)"
                        else:
                            if exlSevendays.count("/")==6:
                                exlSevendaysNew=""
                                strlist = exlSevendays.split('/')
                                for i in range(6):
                                    exlSevendaysNew = exlSevendaysNew + "/" + strlist[i]
                                exlSevendays = str(datetime.date.today()) + "(OK)" + exlSevendaysNew
                            else:
                                exlSevendays = str(datetime.date.today()) + "(OK) / " + exlSevendays

                    newWs.write(exlRow-1, 7, exlSevendays, styleBlue)
                    return response.json()['data']

                varRtnStatus = 0
            except Exception,data:
                print Exception,":",data,"\n"
        else:
            for k in d_exlSheet:
                if k == exlNo.split("_",1)[0]:
                    newWs=newbk.get_sheet(d_exlSheet[k])

            alignment = xlwt.Alignment() # Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
            alignment.vert = xlwt.Alignment.VERT_CENTER # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
            style = xlwt.XFStyle() # Create Style
            style.alignment = alignment # Add Alignment to Style
            pattern = xlwt.Pattern() # Create the Pattern
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
            pattern.pattern_fore_colour = 2 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
            style.pattern = pattern # Add Pattern to Style
            newWs.write(exlRow-1,0,int(exlNo2),style)

        newbk.save(ExcelFile)
    else:
        print "[errorrrrrrrrr , 表格中未找到 " + str(exlNo)+ " 序号,请检查... ]"

def Icommon3(param1,param2):
    # 功能: 获取验证码接口
    # 参数: type = 1 登录验证码 \ 2 提现验证码 \ 4 设置提现密码 \ 5 个人或商铺认证密码 ; mobileNum = 手机号 \ 6 第三方绑定手机号
    requests.request("GET", "http://192.168.2.176:9999/WebBusi/personal/2.1/send_mobile_code.do", headers={'cache-control': "no-cache"}, params={"type":param1,"mobileNum":param2})
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    if param1 == "1": varVerifyCode = r.get("app_login_" + str(param2))
    elif param1 == "2": varVerifyCode = r.get("app_securityCode_" + str(param2))
    elif param1 == "4": varVerifyCode = r.get("app_withdrawCode_" + str(param2))
    elif param1 == "5": varVerifyCode = r.get("app_certificationCode_" + str(param2))
    elif param1 == "6": varVerifyCode = r.get("app_bindMobileCode_" + str(param2))
    else:
        varVerifyCode = 0
        print "[errorrrrrrrrr,参数type不存在或错误!]"
    return varVerifyCode

def showDDL(varDatabase,varTable,varFields):
    conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db=varDatabase, port=3306, use_unicode=True)
    conn.set_character_set('utf8')
    cur = conn.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDatabase,varTable))
    list0=[]
    list1=[]
    list2=[]
    x=y=sum=0
    t2=cur.fetchall()
    if varFields=="":
        print "\n[" + varDatabase + " > " + varTable +" > " + str(len(t2)) + "]"
        print "-" * 50
        for i in t2:
            if len(i[0])>x: x=len(i[0])
            if len(i[1])>y: y=len(i[1])
            sum=sum+1

        for i in t2:
            list0.append(i[0] + " "*(x-len(i[0])+1))
            list1.append(i[1]+ " "*(y-len(i[1])+1))
            ii=i[2].replace("\r\n",",")
            list2.append(ii.replace("  ",""))
        for i in range(sum):
            print list0[i],list1[i],list2[i]
    else:
        print "\n[" + varDatabase + " > " + varTable +" > " + str(len(varFields.split(","))) + "]"
        print "-" * 50
        for i in t2:
            if len(i[0])>x: x=len(i[0])
            if len(i[1])>y: y=len(i[1])
        for i in t2:
            for j in range(len(varFields.split(","))):
                if i[0] == varFields.split(",")[j]:
                    list0.append(i[0] + " "*(x-len(i[0])+1))
                    list1.append(i[1]+ " "*(y-len(i[1])+1))
                    ii=i[2].replace("\r\n",",")
                    list2.append(ii.replace("  ",""))
        for i in range(len(varFields.split(","))):
            print list0[i],list1[i],list2[i]


