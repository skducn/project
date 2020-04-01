# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2018-4-17
# Description   : TerminalC 接口驱动
# python颜色输出规则，www.cnblogs.com/yinjia/p/5559702.html
# *******************************************************************************************************************************
import os, sys, xlwt, xlrd, urllib2, datetime, json, redis, MySQLdb, requests, base64, urllib3, random, time, MultipartPostHandler, cookielib, string , smtplib, md5, base64, hashlib, mimetypes
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from time import sleep
from pymongo import MongoClient
from Crypto.Cipher import DES3
from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5
from xlutils.copy import copy
reload(sys)
sys.setdefaultencoding('utf-8')


# 接口参数excel
varExcel = os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir)) + u"\source\interface.xls"
bk = xlrd.open_workbook(varExcel, formatting_info=True)
newbk = copy(bk)
styleBlue = xlwt.easyxf('font: height 340 ,name Times New Roman, color-index blue')
styleRed = xlwt.easyxf('font: height 340 ,name Times New Roman, color-index red')
# ('font: height 240, name Arial, colour_index black, bold off, italic on; align: wrap on, vert centre, horiz left;')
alignment = xlwt.Alignment()
# alignment.horz = xlwt.Alignment.HORZ_CENTER
# alignment.vert = xlwt.Alignment.VERT_CENTER
# alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
styleRed.alignment = alignment
styleBlue.alignment = alignment
exlSheetNums = len(bk.sheet_names())  # 工作表数量
l_exlSheetNames = bk.sheet_names()
l_exlSheetNames2 = []
l_exlSheetSingleNum = []
for i in range(exlSheetNums):
    l_exlSheetNames2.append(l_exlSheetNames[i].encode('raw_unicode_escape'))
    l_exlSheetSingleNum.append(i)
d_exlSheet = dict(zip(l_exlSheetNames2, l_exlSheetSingleNum))  # 获取工作表的固定位置，从左到右，如0，1，2，3，。。。。{'i1': 2, 'main': 0, 'I1XX': 1, 'I251': 3}

# 获取第一个工作表名
for k, v in d_exlSheet.items():
    if format(v) == "0":
        exlSheet0 = format(k)
# 定位第一个工作表名main
# sheet0 = bk.sheet_by_name(exlSheet0)
# exlPhone = sheet0.cell_value(12, 1)


def iCase(vaInterName, exlNo, *params):
    exlAllInterfaceNum = exlAllInterfaceNumEmpty = 0  # 定义接口总数量、
    startCode = endCode = exlIsCancel = 0  #  开始编号、结束编号、
    l_floatExlSerialNum = []  # 定义序号列表
    l_exlDefaultSerialNum = []  # 定义excel中编号列表
    l_exlParams = []  # 定义参数名称

    try:
        sheetName = bk.sheet_by_name(exlNo.split("_", 2)[0])  # 工作表名 ， 如：i1_N1_C1 中 i1表
        sheet0 = bk.sheet_by_name(exlSheet0)  # 第一个工作表名 main
        exlSerialNum = exlNo.split("_", 2)[1][1:]  # 获取当前序号
        floatExlSerialNum = float(exlSerialNum)  # 浮点化当前序号
        floatExlSerialNum1 = float(int(exlSerialNum) + 1)  # 浮点化下一个序号
    except:
        print u"errorrrrrrrrrr, " + exlNo + u"的格式有误，请检查工作表名！！！"

    # 获取接口总量及序号明细
    for i in range(1, sheetName.nrows):
        if sheetName.cell_value(i, 0) != "":
            exlAllInterfaceNum = exlAllInterfaceNum + 1   # 接口总量
            l_floatExlSerialNum.append(sheetName.cell_value(i, 0))  # 把所有接口序列号存入列表
            l_exlDefaultSerialNum.append(exlAllInterfaceNum + exlAllInterfaceNumEmpty + 1)  # 把excel中编号存入列表
        else:
            exlAllInterfaceNumEmpty = exlAllInterfaceNumEmpty + 1  # 到最后一行记录为止，序号一列为空的总数量
    d_SerialRow = dict(zip(l_floatExlSerialNum, l_exlDefaultSerialNum))
    # print l_floatExlSerialNum
    # print l_exlDefaultSerialNum
    # print exlAllInterfaceNum
    # print d_SerialRow

    # 处理当前接口
    if floatExlSerialNum in l_floatExlSerialNum:
        for j in range(0, sheetName.nrows):
            startCode = startCode + 1
            varThirdway = 0
            if sheetName.cell_value(j, 0) == floatExlSerialNum :
                # exlInterfaceName = sheetName.cell_value(j, 2)
                exlInterfaceName = vaInterName
                exlInterfaceUrl = sheetName.cell_value(j, 3)
                exlInterfaceReturn = sheetName.cell_value(j, 1)
                exlSevendays = sheetName.cell_value(j, 9)
                exlRow = d_SerialRow.get(floatExlSerialNum, 'not found')  # 序号所对应的excel编号，输出编号
                # print exlRow
                break
        # 获取接口的属性名称数量
        if floatExlSerialNum1 in l_floatExlSerialNum:
            for j in range(0, sheetName.nrows):
                endCode = endCode + 1
                if sheetName.cell_value(j, 0) == floatExlSerialNum1:
                    break
        else:
            endCode = sheetName.nrows + 1

        # 将表格中属性名称存入列表
        varFields = endCode - startCode   # 获取两个序号之间参数数量
        l_fields = []   # 定义excel中属性名称列表
        for i in range(varFields):
            l_fields.append(sheetName.cell_value(exlRow - 1 + i, 5))

        # 周肖 定义的 3des 24位 密钥 key ， 及RSA公钥 pub_key_str
        key = 'xUHdKxzVCbsgVIwTnc1jtpWn'
        pub_key_str = """-----BEGIN RSA PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCHp2h4iGAgtAOWvfIzJgSKDTfbDThNW4DeEh15ENrb3ilrI/bnXYeXtEyTodGtU6sQWQpC6/uhI9gdAfuWHr6cYYtoUvPi7QdT/ZRzo1CerkFv/ZbqEZDleoGi7nt8IZrxDV5SEFMnWtTFdup4npWAwxF4sfqZwUaTD3/RkSwQMwIDAQAB
        -----END RSA PUBLIC KEY-----"""
         # *params = '{"userName":"187","passWord":"123"}'

        # 3DES 16位加密
        def init_str(s):
            l = len(s) % 8
            if l != 0:
                c = 8 - l
                s += chr(c) * c
            return s

        # RSA 加密生成 varRSA
        def rsa_long_encrypt(pub_key_str, msg, length=100):
            """
            单次加密串的长度最大为 (key_size/8)-11
            1024bit的证书用100， 2048bit的证书用 200
            """
            pubobj = rsa.importKey(pub_key_str)
            pubobj = PKCS1_v1_5.new(pubobj)
            res = []
            for i in range(0, len(msg), length):
                res.append(pubobj.encrypt(msg[i:i + length]))
            return "".join(res)
        enres = rsa_long_encrypt(pub_key_str, key, 200)
        varRSA = base64.b64encode(enres)

        # print l_fields  # [u'phoneNumber', u'passWord']
        # print list(tuple(params))  # 测试用例中参数值 如：['13816109059', 'e10adc3949ba59abbe56e057f20f883e']
        # 将 属性名称与参数值组合成json格式，如 {"passWord":"e10adc3949ba59abbe56e057f20f883e","phoneNumber":"13816109059"}
        xx = ""
        if len(l_fields) == len(params) :
            for i in range(varFields):
                xx = "\",\"" + sheetName.cell_value(exlRow-1+i, 5) + "\":\"" + params[i] + xx
            yy = "{" + xx + "\"}"
            varParam = yy.replace('{",', "{")
            # print varParam  #{"passWord":"e10adc3949ba59abbe56e057f20f883e","phoneNumber":"13816109059"}

            # 3DES ， 对3DES进行base64处理
            ss = init_str(varParam)
            des3 = DES3.new(key, DES3.MODE_ECB)
            res2 = des3.encrypt(ss)
            var3EDS = base64.b64encode(res2)
            # print des3.decrypt(res2)
            data = varRSA + "|" + var3EDS
            # print data
        else:
            print u"errorrrrrrrrrr, 表格中属性名称数量(" + str(len(l_fields)) + u")与测试用例提供的属性名称数量(" + str(len(params)) + u")不一致！！！"

        if exlIsCancel != 1:
            for k in range(startCode-1, endCode-1):
                l_exlParams.append(sheetName.cell_value(k, 3).encode('raw_unicode_escape'))  # 去掉列表中 带u前缀符号
            exlURL = sheet0.cell_value(11, 1)
            exlSheetURL = sheetName.cell_value(exlRow-1, 3)
            varURL = exlURL + exlSheetURL

            values = {"data":data}
            resp = urllib2.urlopen(urllib2.Request(varURL, json.dumps(values))).read()
            # print resp


            for k in d_exlSheet:
                if k == exlNo.split("_", 1)[0]:
                    newWs = newbk.get_sheet(d_exlSheet[k])
                    break
            if u"操作成功" in str(resp).decode("utf-8"):
                newWs.write(exlRow - 1, 1, "OK", styleBlue)
                varResult = 0
                print u"\033[0;30;46m " + exlSerialNum + " , [OK] " + exlNo + " " + str(exlInterfaceName).decode("utf-8")
                if sheet0.cell_value(3, 0) == "Y":
                    print u"[请求参数] => " + str(varURL).replace("http://","") + u" , " + varParam
                    print u"[加密] => " + str(values)
                    print u"[解密] => " + str(resp).decode("utf-8")  # 返回data解密
                    # 返回原始报文
                    rtnDataEncrypt = resp.split(",")[0].replace('{"data":', "").replace('"', "").replace('\\n', "")  # 去掉加密中的\n
                    # print rtnDataEncrypt
                    if rtnDataEncrypt == "null" or rtnDataEncrypt == "":
                        # print rtnDataEncrypt
                        orgResponse = resp
                    else:
                        des3 = DES3.new(key, DES3.MODE_ECB)
                        orgResponse = des3.decrypt(base64.b64decode(rtnDataEncrypt))  # 先base64解码，再3DES解码。  解码后原始data
                    print u"[返回] => " + orgResponse.decode("utf-8")
                    if sheetName.cell_value(exlRow-1, 10) != "":
                        newWs.write(exlRow - 1, 10, u"已修复", styleBlue)
            else:
                newWs.write(exlRow - 1, 1, "Error", styleRed)
                varResult = 1
                print u"\033[0;30;41m " + exlSerialNum + " , [Errorrrrrrrrrr] " + exlNo + " " + str(exlInterfaceName).decode("utf-8")
                print u"[请求参数] => " + str(varURL).replace("http://","") + u" , " + varParam
                print u"[加密] => " + str(values)
                print u"[解密] => " + str(resp).decode("utf-8")    # 返回data解密
                # 返回原始报文
                rtnDataEncrypt = resp.split(",")[0].replace('{"data":', "").replace('"', "").replace('\\n', "")  # 去掉加密中的\n
                # print rtnDataEncrypt
                if rtnDataEncrypt == "null" or rtnDataEncrypt == "":
                    print rtnDataEncrypt
                    orgResponse = resp
                else:
                    des3 = DES3.new(key, DES3.MODE_ECB)
                    orgResponse = des3.decrypt(base64.b64decode(rtnDataEncrypt))  # 先base64解码，再3DES解码。  解码后原始data
                print u"[返回] => " + orgResponse.decode("utf-8") + "\n"

                # 将错误respCode编号存入备注
                aa = "respCode" + str(resp).split("respCode")[1]
                newWs.write(exlRow - 1, 10, unicode(aa, "utf-8"), styleRed)

            # 设置main
            if sheet0.cell_value(2, 0) == "Y":
                if varResult == 0:
                    if exlSevendays == "":
                        exlSevendays = str(datetime.datetime.now().strftime('%m%d')) + "(OK)"
                    else:
                        if exlSevendays.count(",") == 6:
                            if str(datetime.datetime.now().strftime('%m%d')) not in exlSevendays:
                                exlSevendaysNew = ""
                                strlist = exlSevendays.split(',')
                                for i in range(6):
                                    exlSevendaysNew = exlSevendaysNew + "," + strlist[i]
                                exlSevendays = str(datetime.datetime.now().strftime('%m%d')) + "(OK)" + exlSevendaysNew
                            else:
                                str(exlSevendays).replace(str(datetime.datetime.now().strftime('%m%d')) + "(E)",str(datetime.datetime.now().strftime('%m%d')) + "(OK)")
                        else:
                            if str(datetime.datetime.now().strftime('%m%d')) not in exlSevendays:
                                exlSevendays = str(datetime.datetime.now().strftime('%m%d')) + "(OK) , " + exlSevendays
                            else:
                                str(exlSevendays).replace(str(datetime.datetime.now().strftime('%m%d')) + "(E)", str(datetime.datetime.now().strftime('%m%d')) + "(OK)")
                    newWs.write(exlRow - 1, 9, exlSevendays, styleBlue)
                elif varResult == 1:
                    if exlSevendays == "":
                        exlSevendays = str(datetime.datetime.now().strftime('%m%d')) + "(E)"
                    else:
                        if exlSevendays.count(",") == 6:
                            if str(datetime.datetime.now().strftime('%m%d')) not in exlSevendays:
                                exlSevendaysNew = ""
                                strlist = exlSevendays.split(',')
                                for i in range(6):
                                    exlSevendaysNew = exlSevendaysNew + "," + strlist[i]
                                exlSevendays = str(datetime.datetime.now().strftime('%m%d')) + "(E)" + exlSevendaysNew
                        else:
                            if str(datetime.datetime.now().strftime('%m%d')) not in exlSevendays:
                                exlSevendays = str(datetime.datetime.now().strftime('%m%d')) + "(E) , " + exlSevendays
                    newWs.write(exlRow - 1, 9, exlSevendays, styleRed)
            newbk.save(varExcel)
            return orgResponse
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
            newWs.write(exlRow-1, 0, int(exlSerialNum), style)
        newbk.save(varExcel)
    else:
        print u"[errorrrrrrrrr , 表格中未找到序号" + str(exlSerialNum) + u" ！！！]"

def myfunc(n):
    # varMyGroup4 = "auto" + "".join(myfunc(4))
    import random
    ret = []
    for i in range(n):
        while 1:
            number = random.randrange(0, 10)
            if number not in ret:
                ret.append(str(number))
                break
    return ret
