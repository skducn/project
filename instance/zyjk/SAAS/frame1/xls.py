# -*- coding: utf-8 -*-
from readConfig import *
localReadConfig = ReadConfig()
import reflection
from PO.OpenpyxlPO import *
from PO.DataPO import *
Data_PO = DataPO()
from datetime import datetime

# 定义全局字典变量
d_var = {}


class XLS:

    def __init__(self):

        # 初始化表格
        if platform.system() == 'Darwin':
            self.varExcel = os.path.dirname(os.path.abspath("__file__")) + u'/config/' + localReadConfig.get_system(
                "excelName")
        if platform.system() == 'Windows':
            self.varExcel = os.path.dirname(os.path.abspath("__file__")) + u'\config\\' + localReadConfig.get_system("excelName")
        self.Openpyxl_PO = OpenpyxlPO(self.varExcel)
        self.Openpyxl_PO.closeExcelPid()   # 关闭所有打开的excel
        l_sheetNames = (self.Openpyxl_PO.wb.sheetnames)   # 所有工作表名列表：如 ['inter', 'case']
        self.sheetInter = l_sheetNames[0]  # inter工作表
        self.sheetCase = l_sheetNames[1]  # case工作表
        self.d_inter = {}
        self.Openpyxl_PO.clsColData(14, self.sheetCase)  # 清空 字典变量Value


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

        ''' step1，获取表格中每条用例（case,url,method,param,check,expected） '''
        d_tmp = {}   # 临时字典变量
        l_case = []
        l_casesuit = []
        sh = self.Openpyxl_PO.sh(self.sheetCase)
        # 从第二行开始遍历
        for i in range(sh.max_row-1):
            if sh.cell(row=i+2, column=1).value == "N" or sh.cell(row=i+2, column=1).value == "n":
                pass
            else:
                l_case.append(i+2)  # excelNO
                l_case.append(sh.cell(row=i+2, column=6).value)  # 接口case
                l_case.append(sh.cell(row=i+2, column=7).value)  # 接口url
                l_case.append(sh.cell(row=i+2, column=8).value)  # 接口method
                l_case.append(sh.cell(row=i+2, column=9).value)  # 接口param
                l_case.append(sh.cell(row=i+2, column=10).value)  # 接口check
                l_case.append(sh.cell(row=i+2, column=11).value)  # 接口expected

                # { 字典变量key : 字典变量value引用 }
                d_key = sh.cell(row=i + 2, column=12).value
                d_value = sh.cell(row=i + 2, column=13).value
                if d_key != None and d_key != None:
                    if len(str(d_key).split(",")) > 1 and len(str(d_key).split(",")) == len(str(d_value).split(",")):
                        # 多个key
                        if len(str(d_key).split(",")) == len(str(d_value).split(",")):
                            for i in range((len(str(d_key).split(",")))):
                                if "{" in str(d_value).split(",")[i] and "}" in str(d_value).split(",")[i]:
                                    d_value = str(str(d_value).split(",")[i]).replace("{", "").replace("}", "")
                                    d_tmp[sh.cell(row=i + 2, column=12).value] = eval(d_value)
                                else:
                                    d_tmp[str(d_key).split(",")[i]] = str(d_value).split(",")[i]
                    else:
                        # 单个key
                        if "{" in d_value and "}" in d_value:
                            d_value = str(d_value).replace("{", "").replace("}", "")
                            d_tmp[sh.cell(row=i + 2, column=12).value] = eval(d_value)  # 字典变量key = 字典变量value引用，如d_tmp['mycode'] = '$.code'
                        else:
                            d_tmp[sh.cell(row=i + 2, column=12).value] = sh.cell(row=i + 2, column=13).value  # 字典变量key = 字典变量value引用，如d_tmp['mycode'] = '$.code'

                else:
                    d_tmp[None] = None
                l_case.append(d_tmp)
                l_casesuit.append(l_case)
                l_case = []
                d_tmp = {}
        # print(l_casesuit)

        return l_casesuit


    def result(self, excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_KeyValueQuote):

        ''' step2，解析 '''

        #  解析{ 字典变量key : 字典变量value引用 }
        sh = self.Openpyxl_PO.sh(self.sheetCase)
        for i in range(sh.max_row-1):
            if sh.cell(row=i + 2, column=1).value == "N" or sh.cell(row=i + 2, column=1).value == "n":
                pass
            else:
                key = sh.cell(row=i + 2, column=12).value
                value = sh.cell(row=i + 2, column=14).value
                # 检查字典变量value是否有值
                if value != None:
                    if "," in str(key) and "," in str(value):
                        # 多个key
                        if len(str(key).split(",")) == len(str(value).split(",")):
                            for i in range((len(str(key).split(",")))):
                                d_var[str(key).split(",")[i]] = str(value).split(",")[i]
                    else:
                        # 单个key
                        d_var[key] = value

        # 解析接口
        jsonres = reflection.run([interCase, interUrl, interMethod, interParam, d_var])
        if jsonres != {}:
            d_jsonres = json.loads(jsonres)

            # 判断接口check是否存在?
            try:
                jsonpathValue = jsonpath.jsonpath(d_jsonres, expr=interCheck)
                jsonpathValue = str(jsonpathValue[0])
                # 判断interCheck值是否与expected相等?
                if jsonpathValue != interExpected:
                    self.Openpyxl_PO.setCellColor(excelNo, 2, "FF0000", self.sheetCase)
                    self.setCaseParam(excelNo, "Fail", d_KeyValueQuote, d_jsonres)
                    assert jsonpathValue == interExpected, "预期值是<" + interExpected + ">，而实测值是<" + jsonpathValue + ">"
                else:
                    self.Openpyxl_PO.setCellColor(excelNo, 2, "00E400", self.sheetCase)
                    self.setCaseParam(excelNo, "OK", d_KeyValueQuote, d_jsonres)
            except Exception as e:
                print(e.__traceback__)
                self.Openpyxl_PO.setCellColor(excelNo, 2, "FF0000", self.sheetCase)
                self.setCaseParam(excelNo, "Fail", d_KeyValueQuote, d_jsonres)
                assert 1 == 0, "接口check " + interCheck + " 不存在!"

    def setCaseParam(self, excelNo, result, d_KeyValueQuote, d_jsonres):

        ''' step3，保存数据 '''

        l_tmp = []
        if [i for i in d_KeyValueQuote.keys()][0] != None:

            try:
                # 遍历字典value引用中的常量
                if "$." not in str([i for i in d_KeyValueQuote.values()][0]):
                    self.Openpyxl_PO.setCellValue(excelNo, 14, str(','.join([i for i in d_KeyValueQuote.values()])), self.sheetCase)  # 保存到字典变量value
                else:
                    if len([i for i in d_KeyValueQuote.keys()]) == len([i for i in d_KeyValueQuote.values()]):
                        if len([i for i in d_KeyValueQuote.values()]) > 1:
                            # 解析多个key
                            for i in range(len([i for i in d_KeyValueQuote.values()])):
                                getDictValue = jsonpath.jsonpath(d_jsonres, expr=[j for j in d_KeyValueQuote.values()][i])
                                l_tmp.append(str(getDictValue[0]))
                            self.Openpyxl_PO.setCellValue(excelNo, 14, str(','.join(l_tmp)), self.sheetCase)  # 保存到字典变量value
                        else:
                            # 解析单个key

                            getDictValue = jsonpath.jsonpath(d_jsonres, expr=[i for i in d_KeyValueQuote.values()][0])  # 如解析 $.code
                            if isinstance(getDictValue[0], (bool)):
                                self.Openpyxl_PO.setCellValue(excelNo, 2, "Fail", self.sheetCase)
                            else:
                                self.Openpyxl_PO.setCellValue(excelNo, 14, getDictValue[0], self.sheetCase)  # 保存到字典变量value

            except Exception as e:
                print(e.__traceback__)
                self.Openpyxl_PO.setCellValue(excelNo, 2, "Fail", self.sheetCase)
                assert 1 == 0, "字典变量value引用 " + d_KeyValueQuote + " 不存在!"

        # result
        if result == "OK":
            self.Openpyxl_PO.setCellColor(excelNo, 2, "00E400", self.sheetCase)
            self.Openpyxl_PO.setCellValue(excelNo, 2, "OK", self.sheetCase)
        else:
            self.Openpyxl_PO.setCellColor(excelNo, 2, "FF0000", self.sheetCase)
            self.Openpyxl_PO.setCellValue(excelNo, 2, "Fail", self.sheetCase)

        # response
        self.Openpyxl_PO.setCellValue(excelNo, 15, str(d_jsonres), self.sheetCase)

        # date
        self.Openpyxl_PO.setCellValue(excelNo, 3, str(datetime.now().strftime("%Y-%m-%d")), self.sheetCase)
        self.Openpyxl_PO.wb.save(self.varExcel)


        # # selectSQL
        # if selectSQL == 0:
        #     self.wSheet.write(excelNo, 14, selectSQL, self.styleRed)
        # else:
        #     self.wSheet.write(excelNo, 14, selectSQL, self.styleBlue)
        #
        # # updateSQL
        # if updateSQL == 'done':
        #     self.wSheet.write(excelNo, 16, updateSQL, self.styleBlue)
        # else:
        #     self.wSheet.write(excelNo, 16, updateSQL, self.styleRed)






if __name__ == '__main__':
    xls = XLS()
