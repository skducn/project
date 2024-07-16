# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-22
# Description   : 字符串对象层
# *********************************************************************
"""
# todo 转换

1.1 字符串转列表
1.2 字符串转元组
1.3 字符串转字典
1.4 字符串转换日期 str2date()

# todo 判断
2.0 判断字符串是否为浮点数 isFloat()
2.1 判断字符串是否为数字 isNumber()
2.2 判断字符串是否全部是中文 isChinese()
2.3 判断字符串中是否包含中文 isContainChinese()
2.4 判断复数 isComplex()

# todo 操作
3.1 删除特殊字符 delSpecialChar()
3.2 字符串列表大写转小写  print([str(i).lower() for i in x])
3.3 浮点数四舍五入到整数位（取整）roundInt()

4.1 小数点最后位去0 subZero()
4.2 小数点后统一位数 patchZero()
"""

import sys, re
from time import strptime
from time import strftime


class StrPO:

    def str2list(self, varStr=None, varMode="str"):

        """1.1 字符串转列表"""

        try:
            if varMode != "digit":
                return varStr.split(",")  # ['1', '2', '3']
            else:
                return list(eval(varStr))
        except:
            return None

    def str2tuple(self, varStr=None, varMode="str"):

        """1.2 字符串转元组"""

        try:
            if varMode != "digit":
                return tuple(varStr)
            else:
                func = lambda x: tuple(int(i) for i in x)
                return tuple(func(i) for i in varStr)
        except:
            return None

    def str2dict(self, varStr):

        """1.3 字符串转字典"""
        # {'a': '123', 'b': 456} , 这是字典，用单引号
        # {"a": "192.168.1.1", "b": "192.168.1.2"} ， 这是字符串，用双引号

        return dict(eval(varStr))

    def str2date(self, datestr):

        """1.4 字符串转换成日期"""

        chinesenum = {
            "一": "1",
            "二": "2",
            "三": "3",
            "四": "4",
            "五": "5",
            "六": "6",
            "七": "7",
            "八": "8",
            "九": "9",
            "零": "0",
            "十": "10",
        }
        strdate = ""
        for i in range(len(datestr)):
            temp = datestr[i]
            if temp in chinesenum:
                if temp == "十":
                    if datestr[i + 1] not in chinesenum:
                        strdate += chinesenum[temp]
                    elif datestr[i - 1] in chinesenum:
                        continue
                    else:
                        strdate += "1"
                else:
                    strdate += chinesenum[temp]
            else:
                strdate += temp
        pattern = ("%Y年%m月%d日", "%Y-%m-%d", "%y年%m月%d日", "%y-%m-%d", "%Y/%m/%d")
        output = "%Y-%m-%d"
        for i in pattern:
            try:
                ret = strptime(strdate, i)
                if ret:
                    return strftime(output, ret)
            except:
                continue
        return False


    def isFloat(self, varStr):

        """ 2.0 判断字符串是否为浮点数"""
        s = varStr.split(".")
        if len(s) > 2:
            return False
        else:
            for si in s:
                if not si.isdigit():
                    return False
            return True

    def isNumber(self, varStr):

        """ 2.1 判断字符串是否为数字"""
        # 可识别中文，阿拉伯语，泰语等数字
        # print(Str_PO.isNumber('foo'))  # False
        # print(Str_PO.isNumber('1'))  # True
        # print(Str_PO.isNumber('1.3'))  # True
        # print(Str_PO.isNumber('-1.37'))  # True
        # print(Str_PO.isNumber('1e3'))  # True
        # print(Str_PO.isNumber('٥'))  # True   //# 阿拉伯语 5
        # print(Str_PO.isNumber('๒'))  # True  //# 泰语 2
        # print(Str_PO.isNumber('四'))  # True  /# 中文数字
        # print(Str_PO.isNumber('©'))  # False  /# 版权号
        try:
            float(varStr)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(varStr)
            return True
        except (TypeError, ValueError):
            pass
        return False


    def isChinese(self, varStr):

        """# 2.2 判断字符串是否是中文"""

        for _char in varStr:
            if not "\u4e00" <= _char <= "\u9fa5":
                return False
        return True

    def isContainChinese(self, varStr):

        """# 2.3 判断字符串中是否包含中文"""

        for ch in varStr:
            if "\u4e00" <= ch <= "\u9fa5":
                return True
        return False

    def isComplex(self, varValue):

        """2.4 判断复数"""
        # 支持数字类型：int、float、bool、complex、字符串、long类型（python2中有long类型， python3中没有long类型）
        # print(Str_PO.isComplex(123))  # True
        # print(Str_PO.isComplex(complex(1, 2)))  # True
        # print(Str_PO.isComplex(complex("1")))  # True
        # print(Str_PO.isComplex(complex("1+2j")))  # True
        # print(Str_PO.isComplex((1)))  # True
        # print(Str_PO.isComplex(True))  # True
        # print(Str_PO.isComplex(False))  # True
        # print(Str_PO.isComplex(-123))  # True
        # print(Str_PO.isComplex(123456768567868756756757575675657567567567.77434))  # True
        # print(Str_PO.isComplex(0.23456))  # True
        # print(Str_PO.isComplex(000000.23456))  # True
        # print(Str_PO.isComplex("100"))  # True
        # print(Str_PO.isComplex("1234.56768567868"))  # True
        # print(Str_PO.isComplex("二"))  # False
        # print(Str_PO.isComplex("123Abc"))  # False
        try:
            complex(varValue)
        except ValueError:
            return False
        return True

    def delSpecialChar(self, varStr, *sc):

        """3.1 删除特殊字符"""
        # 文件名不包含以下任何字符：”（双引号）、 * （星号）、 < （小于）、 > （大于）、?（问号）、\（反斜杠）、 | （竖线）、 / (正斜杠)、: (冒号)。
        return str(varStr).replace('"', "").replace('*', "").replace('<', "").replace('>', "").replace('?', "").replace('\\', "").replace('/', "").replace('|', "").replace(':', "").replace(' ', "")

    def roundInt(self, float):

        """3.2 浮点数四舍五入到整数位（取整）
        # 分析：优化round（）函数整数四舍五入缺陷，原round()函数遇偶整数四舍五入时不进位如：round(12.5) =12 ； 遇奇整数则进位如：round(13.5)=14
        """

        ff = int(float)
        if ff % 2 == 0:
            return round(float + 1) - 1
        else:
            return round(float)

    # def addZero(self, varNum, varPatchNum):
    #
    #     """3.3 数字转字符串小数点后补0"""
    #
    #     varStr = ""
    #     try:
    #         if self.isComplex(varNum) == True:
    #             if varNum == True:
    #                 varNum = 1
    #             if varNum == False:
    #                 varNum = 0
    #
    #             if "." not in str(varNum):
    #                 if isinstance(varPatchNum, int):
    #                     if varPatchNum < 0:
    #                         print("error1")
    #                     elif varPatchNum == 0:
    #                         return varNum
    #                     else:
    #                         varStr = str(varNum) + "." + "0" * varPatchNum  # 整数小数位补1个0
    #                 else:
    #                     print("error2")
    #             else:
    #                 if isinstance(varPatchNum, int):
    #                     if varPatchNum < 0:
    #                         dotLen = str(varNum).split(".")[1]
    #                         if len(dotLen) <= int(-varPatchNum):
    #                             return varNum[0 : -(len(dotLen) + 1)]
    #                         else:
    #                             return varNum[0:varPatchNum]
    #                     else:
    #                         dotLen = str(varNum).split(".")[1]  # 小数点后一个0
    #                         if len(dotLen) > 0:
    #                             varStr = str(varNum) + "0" * varPatchNum  # 整数小数位补1个0
    #                 else:
    #                     print("error3")
    #
    #             return varStr
    #         else:
    #             print("error4")
    #     except:
    #         print("error5")

    def subZero(self, varValue):

        """3.3 数字转字符串小数点后去0"""

        return "{:g}".format(float(varValue))

    def patchZero(self, varList, varPatchNum=2):

        """3.4 数字转字符串小数点后不足位数的补零（批量）"""
        # 将列表中所有元素的格式变成.00，如： [11, 22.0, 33.00] => [11.00, 22.0, 33.00]
        # 注意：支持 数字或字符串数字，转换后列表内元素都是字符串。

        list4 = []
        list3 = []
        try:
            for i in varList:
                if self.isComplex(i) == True:
                    if isinstance(i, str):
                        if "." in i:
                            list3.append(float(i))
                        else:
                            list3.append(int(i))
                    else:
                        list3.append(i)

            if varPatchNum == 0:
                for i in list3:
                    list4.append("{:g}".format(i))
                return list4
            elif varPatchNum < 0:
                print("error1")

            for i in list3:
                list4.append("{:g}".format(i))

            for i in range(len(list4)):
                if "." not in list4[i]:  # //整数，在数位后补N个0
                    if list4[i] != "0":
                        list4[i] = list4[i] + "." + "0" * varPatchNum
                    else:
                        list4[i] = "0"
                else:
                    list4[i] = list4[i] + "0" * (
                        varPatchNum - len(list4[i].split(".")[1])
                    )
            return list4
        except:
            print("error2")

