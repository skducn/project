# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2020-8-27
# Description   : excel 封装包
# *****************************************************************

import os, xlrd, xlwt, json, jsonpath
from datetime import datetime
from xlrd import open_workbook
from xlutils.copy import copy

import instance.zyjk.SAAS.PageObject.ReadConfigPO as readConfig
localReadConfig = readConfig.ReadConfigPO()
import instance.zyjk.SAAS.PageObject.ReflectionPO as reflection

class XlsPO():

    def __init__(self):
        # 初始化表格
        self.varExcel = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + u'\\config\\' + localReadConfig.get_excel("interfaceFile")
        self.rbk = xlrd.open_workbook(self.varExcel, formatting_info=True)
        self.wbk = copy(self.rbk)
        self.wSheet = self.wbk.get_sheet(1)
        self.styleBlue = xlwt.easyxf(u'font: height 260 ,name Times New Roman, color-index blue')
        self.styleRed = xlwt.easyxf(u'font: height 260 ,name Times New Roman, color-index red')
        sheetNums = 0
        l_sheetNames = 0
        l_sheetSerial = []  # 工作表序列
        l_sheetName = []  # 工作表名字
        d_sheetNames = {}
        sheetNums = len(self.rbk.sheet_names())  # 工作表数量：如 2
        l_sheetNames = self.rbk.sheet_names()  # 所有工作表名列表：如 ['inter', 'case']
        for i in range(sheetNums):
            l_sheetSerial.append(i)
            l_sheetName.append(l_sheetNames[i])
        d_sheetNames = dict(zip(l_sheetSerial, l_sheetName))  # 工作表名字典：{0: 'inter', 1: 'case'}
        self.sheetInter = self.rbk.sheet_by_name(d_sheetNames[0])  # 第1个工作表：inter
        self.sheetCase = self.rbk.sheet_by_name(d_sheetNames[1])  # 第2个工作表：case
        self.d_inter = {}

    def getInterIsRun(self):
        """
        :param l_interIsRun: [[2, 3, 5], [], 0] , 3个列表分表表示isRunY,isNoRun,isRunAll
        :param interName: '/inter/HTTP/auth'
        :return: [[2，'获取Token', 'post', '/inter/HTTP/auth', 'None', '$.status','200']]
        判断inter工作表中接口是否执行。isRun一列，y=执行，n=不执行，返回列表如下。
        返回：'[[], [], 3]'  第一个[]表示没有Y，第二个[]标识没有N，3表示3个接口
        返回：[[], [2, 3, 5], 0] 第一个[]表示没有Y，第二个[2,3,5]表示第2第3第5个接口是N
        返回：[[2], [3, 5], 0] 第一个[2]表示有第二个接口是Y，第二个[3,5]表示第3第5个接口是N
        """
        serialNums = 0
        serialNumNull = 0
        l_serialNum = []
        l_excelNum = []
        d_serialRow = {}
        inter_joint = ''
        for i in range(1, self.sheetInter.nrows):  # 当前工作表总行数：如 5
            if self.sheetInter.cell_value(i, 0) != u"":
                serialNums += 1  # 接口总数量：如 3
                l_serialNum.append(int(self.sheetInter.cell_value(i, 0)))  # 接口序列号列表：如 [1,2,3]
                l_excelNum.append(serialNums + serialNumNull + 1)  # excel序列号列表：如 [2,3,5]
            else:
                serialNumNull += 1  # 统计到最后一行记录为止，序号一列为空的总数量
            d_serialRow = dict(zip(l_serialNum, l_excelNum))  #  接口与excel序列号字典：如 {1: 2, 2: 3, 3: 5, 4: 6}

        # 遍历接口数量
        for j in range(len(l_excelNum)):
            # # 判断下一个接口是否是最后一个
            if j == len(l_excelNum)-1:
                # 最后一个接口的一个参数
                if self.sheetInter.nrows == l_excelNum[-1]:
                    self.d_inter[self.sheetInter.cell_value(l_excelNum[j] - 1, 3)] = self.sheetInter.cell_value(l_excelNum[j] - 1, 5)
                else:
                # 最后一个接口的多个参数
                    lastInterParam = self.sheetInter.nrows - l_excelNum[-1]
                    for i in range(lastInterParam+1):
                        inter_joint = inter_joint + ',' + self.sheetInter.cell_value(l_excelNum[j] - 1 + i, 5)
                    self.d_inter[self.sheetInter.cell_value(l_excelNum[j] - 1, 3)] = inter_joint[1:]
                    inter_joint =''
            else:
                # 1个参数
                if l_excelNum[j] + 1 == l_excelNum[j+1]:
                    self.d_inter[self.sheetInter.cell_value(l_excelNum[j]-1, 3)] = self.sheetInter.cell_value(l_excelNum[j]-1, 5)
                else:
                # 多个参数
                    x = l_excelNum[j + 1] - l_excelNum[j]
                    for k in range(x):
                        inter_joint = inter_joint + ',' + self.sheetInter.cell_value(l_excelNum[j] -1 + k, 5)
                    self.d_inter[self.sheetInter.cell_value(l_excelNum[j] - 1, 3)] = inter_joint[1:]
                    inter_joint = ''
        # print(self.d_inter)  # {'/inter/HTTP/auth': 'none', '/inter/HTTP/login': 'username,password', '/inter/HTTP/logout': 'test,hhh'}

        # 遍历接口表的isRun，获取isRunAll,isRunY,isNoRun ,如：[[], [], 5]
        isRunAll = 0
        l_isRunAll = []  # 执行所有接口列表
        l_isRunY = []  # 执行 isRun = Y 接口的列表
        l_isNoRun = []  # 不执行 isRun = N 接口的列表
        l_interName = []  # 接口名列表，通过isRun控制所需测试的接口，如： # ['/inter/HTTP/auth', '/inter/HTTP/login'] 表示只测试这2个接口
        l_isRun = []
        for i in range(1, len(d_serialRow) + 1):
            # 如果isRun为空
            if self.sheetInter.cell_value(d_serialRow.get(i) - 1, 1) == 'Y' or self.sheetInter.cell_value(d_serialRow.get(i) - 1, 1) == 'y':
                l_isRunY.append(d_serialRow.get(i))
                keyword = str(self.sheetInter.cell_value(d_serialRow.get(i) - 1, 3))
                l_interName.append(keyword)
            elif self.sheetInter.cell_value(d_serialRow.get(i) - 1, 1) == 'N' or self.sheetInter.cell_value(d_serialRow.get(i) - 1, 1) == 'n':
                l_isNoRun.append(d_serialRow.get(i))
            else:
                isRunAll += 1
        if isRunAll == len(d_serialRow):
            for k, v in d_serialRow.items():
                l_isRunAll.append(v)
                l_interName.append(str(self.sheetInter.cell_value(int(v-1), 3)))
        l_isRun.append(l_isRunY)
        l_isRun.append(l_isNoRun)
        l_isRun.append(len(l_isRunAll))
        # print(l_isRun)
        return l_isRun

    def getCaseParam(self):

        ''' 遍历case获取参数 '''

        l_case = []
        l_casesuit = []
        for i in range(1, self.sheetCase.nrows):
            if self.sheetCase.cell_value(i, 0) == 'N' or self.sheetCase.cell_value(i, 0) == 'n':
                pass
            else:
                l_case.append(i)  # excelNO
                l_case.append(self.sheetCase.cell_value(i, 3))  # caseName
                l_case.append(self.sheetCase.cell_value(i, 4))  # method
                l_case.append(self.sheetCase.cell_value(i, 5))  # interName
                l_case.append(self.sheetCase.cell_value(i, 6))  # param
                l_case.append(self.sheetCase.cell_value(i, 7))  # jsonpath
                l_case.append(self.sheetCase.cell_value(i, 8))  # expected
                l_case.append(self.sheetCase.cell_value(i, 13))  # selectSQL
                l_case.append(self.sheetCase.cell_value(i, 15))  # updateSQL
                l_casesuit.append(l_case)
                l_case = []
        return l_casesuit

    def setCaseParam(self, excelNo, generation, result, response, selectSQL, updateSQL):

        '''
        保存 generation,result,resposne,date,selectSQL,updateSQL
        :param excelNo: case编号
        :param generation: 生成关键字，如 userid=1 或 为空
        :param result: pass 或 Fail
        :param response: {'status': 200, 'msg': '恭喜您，登录成功', 'userid': '1'}
        '''

        # generation
        self.wSheet.write(excelNo, 9, generation, self.styleBlue)

        # result
        if result == "OK":
            self.wSheet.write(excelNo, 10, result, self.styleBlue)
        if result == "Fail":
            self.wSheet.write(excelNo, 10, result, self.styleRed)

        # response
        self.wSheet.write(excelNo, 11, response, self.styleBlue)

        # date
        self.wSheet.write(excelNo, 12, str(datetime.now().strftime("%Y%m%d%H%M%S")), self.styleBlue)

        # selectSQL
        if selectSQL == 0:
            self.wSheet.write(excelNo, 14, selectSQL, self.styleRed)
        else:
            self.wSheet.write(excelNo, 14, selectSQL, self.styleBlue)

        # updateSQL
        if updateSQL == 'done':
            self.wSheet.write(excelNo, 16, updateSQL, self.styleBlue)
        else:
            self.wSheet.write(excelNo, 16, updateSQL, self.styleRed)

        self.wbk.save(self.varExcel)

    def result(self, excelNo, caseName, method, interName, param, jsonpathKey, expected):

        ''' 解析参数 '''

        # 请求参数
        if param == "":
            print("[无参]")
        else:
            print("[参数] => " + str(param))

        # 响应值
        d_responseValue = reflection.run([caseName, method, interName, param])
        print("[返回值] => " + str(d_responseValue))

        # 检查预期值
        l_expected = jsonpath.jsonpath(d_responseValue, expr=jsonpathKey)
        if l_expected[0] != expected:
            self.setCaseParam(excelNo, "", "Fail", str(d_responseValue), "", "")
            assert l_expected[0] == expected, "预期值是<" + expected + ">, 实测值是<" + l_expected[0] + ">"
            return False
        else:
            self.setCaseParam(excelNo, "", "OK", str(d_responseValue), "", "")
            print("[结果] => ok, 预期值与实测值一致\n")
            return d_responseValue

if __name__ == '__main__':

    Xls_PO = XlsPO()
