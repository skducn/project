# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2017-7-26
# Description   : cetc 接口驱动
# *******************************************************************************************************************************


import os, sys, redis, MySQLdb, requests, xlwt, xlrd, urllib3, random, time, urllib2, MultipartPostHandler, cookielib, string ,datetime, smtplib, json, md5, base64, hashlib, mimetypes, email
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from time import sleep
from pymongo import MongoClient
from xlutils.copy import copy
reload(sys)
sys.setdefaultencoding('utf-8')


'''外部数据源'''
varExcel = os.path.dirname(os.path.abspath("__file__")) + u'/interface.xls'
bk = xlrd.open_workbook(varExcel, formatting_info=True)
newbk = copy(bk)
styleBlue = xlwt.easyxf(u'font: height 340 ,name Times New Roman, color-index blue')
styleRed = xlwt.easyxf(u'font: height 340 ,name Times New Roman, color-index red')
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

for k, v in d_exlSheet.items():  # 获取第一个工作表名
    if format(v) == u"0": exlSheet0 = format(k)

sheet0 = bk.sheet_by_name(exlSheet0)  # 定位第一个工作表名 ,默认main
# exlPhone = sheet0.cell_value(12, 1)
# print exlPhone
# print type(str(exlPhone))

def Icase(vaInterName, exlNo, *params):
    try:
        sheetName = bk.sheet_by_name(exlNo.split("_", 2)[0])  # 定位工作表名
        sheet0 = bk.sheet_by_name(exlSheet0)  # 定位第一个工作表名
    except:
        print u"errorrrrrrrrrr, " + exlNo + u"的格式有误，请检查工作表名！！！"

    exlAllInterfaceNum = exlAllInterfaceNumEmpty = 0
    startCode = endCode = exlIsCancel = 0  #  开始编号、结束编号、
    l_floatExlSerialNum = []  # 序号列表
    l_exlDefaultSerialNum = []  # 默认序号列表
    l_exlParams = []  # 所有参数名称
    exlSerialNum = exlNo.split("_", 2)[1][1:]  # 获取序号
    floatExlSerialNum = float(exlSerialNum)  # 当前序号
    floatExlSerialNum1 = float(int(exlSerialNum)+1)  # 下一个序号

    # 获取接口总数量及接口序号明细
    for i in range(1, sheetName.nrows):
        if sheetName.cell_value(i, 0) != u"":
            exlAllInterfaceNum = exlAllInterfaceNum + 1   # 接口总数量
            l_floatExlSerialNum.append(sheetName.cell_value(i, 0))  # 把所有序列号存入列表
            l_exlDefaultSerialNum.append(exlAllInterfaceNum + exlAllInterfaceNumEmpty + 1)  # 把所有默认序列号存入列表
        else:
            exlAllInterfaceNumEmpty = exlAllInterfaceNumEmpty + 1  # 到最后一行记录为止，序号一列为空的总数量
    d_SerialRow = dict(zip(l_floatExlSerialNum, l_exlDefaultSerialNum))
    # print l_floatExlSerialNum
    # print l_exlDefaultSerialNum
    # print exlAllInterfaceNum  # 接口总数量
    # print d_SerialRow

    if floatExlSerialNum in l_floatExlSerialNum:
        for j in range(0, sheetName.nrows):
            startCode = startCode + 1
            varThirdway = 0
            if sheetName.cell_value(j, 0) == floatExlSerialNum :
                exlInterfaceName = sheetName.cell_value(j, 2)
                exlInterfaceUrl = sheetName.cell_value(j, 3)
                exlInterfaceReturn = sheetName.cell_value(j, 1)
                exlSevendays = sheetName.cell_value(j, 9)

                # if "#" in exlInterfaceUrl :   # 调用第三方函数
                #     exlInterfaceUrl = exlInterfaceUrl.encode("utf-8")
                #     exlInterfaceUrl = exlInterfaceUrl.replace("#", "")
                #     # varNums = len(exlInterfaceUrl.split(","))
                #     # varLists = exlInterfaceUrl.split(",")
                #     varThirdway = 1
                #     varNums = len(exlInterfaceUrl.split(","))
                #     varLists = exlInterfaceUrl.split(",")
                #
                #     # if "http" in exlParams:
                #     #     exlInterfaceUrl = varLists[0] +"," + varLists[1] +","+ varLists[2] +","+ exlParams +","+ varLists[4] +","+ varLists[5]
                #     # varRtnStatus,varJson = eval(varLists[0])(exlInterfaceUrl)
                #     # # varRtnStatus,varJson = eval(varLists[0])(varLists[1],varLists[2],varLists[3],varLists[4],varLists[5])

                # exlInterfaceReturn = exlInterfaceReturn.encode("utf-8")   # unicode 2 str
                exlRow = d_SerialRow.get(floatExlSerialNum, u'not found')  # 序号所对应的默认序号，输出默认序号
                # print exlRow
                break

        # 获取接口的属性名称数量
        if floatExlSerialNum1 in l_floatExlSerialNum:
            for j in range(0, sheetName.nrows):
                endCode = endCode + 1
                if sheetName.cell_value(j, 0) == floatExlSerialNum1:
                    break
        else:
            endCode = sheetName.nrows+1

        varFields = endCode - startCode
        # print varFields

        l_fields = []
        xx = ""

        for i in range(varFields):
            l_fields.append(sheetName.cell_value(exlRow - 1 + i, 5))
        #
        # print l_fields
        # print list(tuple(params))

        if len(l_fields) == len(params) and len(l_fields) > 0:
            for i in range(varFields):
                l_fields.append(sheetName.cell_value(exlRow - 1 + i, 5))
                xx = u"\",\"" + sheetName.cell_value(exlRow - 1 + i, 5) + "\":\"" + params[i] + xx
            yy = u"{" + xx + u"\"}"
            varParam = yy.replace(u'{",', u"{")

            # print varParam
            # sleep(1212)


        if varThirdway == 1 and exlIsCancel != 1:
            pass

        elif exlIsCancel != 1:

            for k in range(startCode-1, endCode-1):
                l_exlParams.append(sheetName.cell_value(k, 3).encode('raw_unicode_escape'))  # 去掉列表中 带u前缀符号

            exlURL = sheet0.cell_value(11, 1)
            exlSheetURL = sheetName.cell_value(exlRow-1, 3)
            varURL = exlURL + exlSheetURL

            try:
                m1 = md5.new()
                m1.update(varParam + u"123456")
            except:
                print u"\nerrorrrrrrrrrr, 表格属性名称数量与测试用例提供的数量不一致！！！"

            values = {"check": m1.hexdigest(), "json": varParam}
            resp = urllib2.urlopen(urllib2.Request(varURL, json.dumps(values))).read()
            for k in d_exlSheet:
                if k == exlNo.split(u"_", 1)[0]:
                    newWs = newbk.get_sheet(d_exlSheet[k])
                    break
            if u"操作成功" in str(resp):
                newWs.write(exlRow - 1, 1, u"OK", styleBlue)
                varResult= 0
                print u"\n[结果] => [OK] " + exlNo + " " + exlInterfaceName
                if sheet0.cell_value(3, 0) == u"Y":
                    print u"[地址] => " + varURL
                    print u"[请求1] => " + str(values)
                    print u"[返回] => " + str(resp)
                    if sheetName.cell_value(exlRow-1, 10) != "":
                        newWs.write(exlRow - 1, 10, u"已修复", styleBlue)
            else:
                newWs.write(exlRow - 1, 1, u"Error", styleRed)
                varResult = 1
                print u"\n[结果] => [Errorrrrrrrrrr] " + exlNo + " " + exlInterfaceName
                print u"[地址] => " + varURL
                print u"[请求2] => " + str(values)
                print u"[返回] => " + str(resp)

                aa = "respCode" + str(resp).split("respCode")[1]
                # unicode(aa, "utf-8")
                newWs.write(exlRow - 1, 10, unicode(aa, "utf-8"), styleRed)

            if sheet0.cell_value(2, 0) == u"Y":
                if varResult == 0:
                    if exlSevendays == u"":
                        exlSevendays = str(datetime.datetime.now().strftime(u'%m%d')) + u"(OK)"
                    else:
                        if exlSevendays.count(u",") == 6:
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
            return resp

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

# def myfunc(n):
#     # varMyGroup4 = "auto" + "".join(myfunc(4))
#     import random
#     ret = []
#     for i in range(n):
#         while 1:
#             number = random.randrange(0, 10)
#             if number not in ret:
#                 ret.append(str(number))
#                 break
#     return ret
