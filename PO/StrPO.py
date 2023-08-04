# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-22
# Description   : 字符串对象层
# *********************************************************************

"""
1.1 字符串转列表 str2list()
1.2 字符串转元组 str2tuple()
1.3 字符串转字典 str2dict()
1.4 字符串转换日期 str2date()

2.1 判断字符串是否为数字 isNumber()
2.2 判断字符串是否全部是中文 isChinese()
2.3 判断字符串中是否包含中文 isContainChinese()
2.4 判断复数 isComplex()

3 删除特殊字符 delSpecialChar()

4 字符串列表大写转小写  print([str(i).lower() for i in x])

5.1 浮点数四舍五入到整数位（取整）roundInt()
5.2 数字转字符串 digit2str()
5.3 数字转字符串小数点后补0 addZero()
5.4 数字转字符串小数点后去0 subZero()
5.5 数字转字符串小数点后不足位数的补零（批量）patchZero()

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

    def isNumber(self, varStr):

        """# 2.1 判断字符串是否为数字"""
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

        """3 删除特殊字符"""
        # 文件名不包含以下任何字符：”（双引号）、 * （星号）、 < （小于）、 > （大于）、?（问号）、\（反斜杠）、 | （竖线）、 / (正斜杠)、: (冒号)。

        varStr = str(varStr).replace('"', "").replace('*', "").replace('<', "").replace('>', "").replace('?', "").replace('\\', "").replace('/', "").replace('|', "").replace(':', "")
        return varStr

    def roundInt(self, float):

        """5.1 浮点数四舍五入到整数位（取整）
        # 分析：优化round（）函数整数四舍五入缺陷，原round()函数遇偶整数四舍五入时不进位如：round(12.5) =12 ； 遇奇整数则进位如：round(13.5)=14
        """

        ff = int(float)
        if ff % 2 == 0:
            return round(float + 1) - 1
        else:
            return round(float)

    def addZero(self, varNum, varPatchNum):

        """5.3 数字转字符串小数点后补0"""

        varStr = ""
        try:
            if self.isComplex(varNum) == True:
                if varNum == True:
                    varNum = 1
                if varNum == False:
                    varNum = 0

                if "." not in str(varNum):
                    if isinstance(varPatchNum, int):
                        if varPatchNum < 0:
                            print(
                                "[ERROR], "
                                + sys._getframe(1).f_code.co_name
                                + ", line "
                                + str(sys._getframe(1).f_lineno)
                                + ", in "
                                + sys._getframe(0).f_code.co_name
                                + ", SourceFile '"
                                + sys._getframe().f_code.co_filename
                                + "'"
                            )
                        elif varPatchNum == 0:
                            return varNum
                        else:
                            varStr = str(varNum) + "." + "0" * varPatchNum  # 整数小数位补1个0
                    else:
                        print(
                            "[ERROR], "
                            + sys._getframe(1).f_code.co_name
                            + ", line "
                            + str(sys._getframe(1).f_lineno)
                            + ", in "
                            + sys._getframe(0).f_code.co_name
                            + ", SourceFile '"
                            + sys._getframe().f_code.co_filename
                            + "'"
                        )
                else:
                    if isinstance(varPatchNum, int):
                        if varPatchNum < 0:
                            dotLen = str(varNum).split(".")[1]
                            if len(dotLen) <= int(-varPatchNum):
                                return varNum[0 : -(len(dotLen) + 1)]
                            else:
                                return varNum[0:varPatchNum]
                        else:
                            dotLen = str(varNum).split(".")[1]  # 小数点后一个0
                            if len(dotLen) > 0:
                                varStr = str(varNum) + "0" * varPatchNum  # 整数小数位补1个0
                    else:
                        print(
                            "[ERROR], "
                            + sys._getframe(1).f_code.co_name
                            + ", line "
                            + str(sys._getframe(1).f_lineno)
                            + ", in "
                            + sys._getframe(0).f_code.co_name
                            + ", SourceFile '"
                            + sys._getframe().f_code.co_filename
                            + "'"
                        )

                return varStr
            else:
                print(
                    "[ERROR], "
                    + sys._getframe(1).f_code.co_name
                    + ", line "
                    + str(sys._getframe(1).f_lineno)
                    + ", in "
                    + sys._getframe(0).f_code.co_name
                    + ", SourceFile '"
                    + sys._getframe().f_code.co_filename
                    + "'"
                )
        except:
            print(
                "[ERROR], "
                + sys._getframe(1).f_code.co_name
                + ", line "
                + str(sys._getframe(1).f_lineno)
                + ", in "
                + sys._getframe(0).f_code.co_name
                + ", SourceFile '"
                + sys._getframe().f_code.co_filename
                + "'"
            )

    def subZero(self, varValue):

        """5.4 数字转字符串小数点后去0"""

        return "{:g}".format(float(varValue))

    def patchZero(self, varList, varPatchNum=2):

        """5.5 数字转字符串小数点后不足位数的补零（批量）"""
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
                print(
                    "[ERROR], "
                    + sys._getframe(1).f_code.co_name
                    + ", line "
                    + str(sys._getframe(1).f_lineno)
                    + ", in "
                    + sys._getframe(0).f_code.co_name
                    + ", SourceFile '"
                    + sys._getframe().f_code.co_filename
                    + "'"
                )

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
            print(
                "[ERROR], "
                + sys._getframe(1).f_code.co_name
                + ", line "
                + str(sys._getframe(1).f_lineno)
                + ", in "
                + sys._getframe(0).f_code.co_name
                + ", SourceFile '"
                + sys._getframe().f_code.co_filename
                + "'"
            )


if __name__ == "__main__":

    Str_PO = StrPO()

    # print("1.1，字符串转列表".center(100, "-"))
<<<<<<< HEAD
    print(Str_PO.str2list("a,b"))  # ['a', 'b']
    print(Str_PO.str2list("['q','qwe']"))  # ['a', 'b']
=======
    # print(Str_PO.str2list("a,b"))  # ['a', 'b']
>>>>>>> origin/master
    # print(Str_PO.str2list("a1,2,3"))  # ['a1', '2', '3']
    # print(Str_PO.str2list("1,2,3"))  # ['1', '2', '3']
    # print(Str_PO.str2list("1,2,3", "digit"))  # [1, 2, 3]
    # print(Str_PO.str2list("123"))  # ['123']
    # print(Str_PO.str2list("123,", "digit"))  # [123]   // 当字符串是一个数字元素时，需转数字列表时，要在单个元素最后加上逗号
    # print(Str_PO.str2list())  # None
    #
    # print("1.2，字符串转元组".center(100, "-"))
    # print(Str_PO.str2tuple("1234"))  # ('1', '2', '3', '4')
    # t = Str_PO.str2tuple("1234", "digit")
    # print(t)  # ((1,), (2,), (3,), (4,))
    # print(t[2][0])  # 3
    # print(type(t[2][0]))  # <class 'int'>
    # print(Str_PO.str2tuple("1"))  # ('1',)
    # print(Str_PO.str2tuple("1", "digit"))  # ((1,),)
    # print(Str_PO.str2tuple("ab"))  # ('a', 'b')
    #
    # print("1.3，字符串转字典".center(100, "-"))
    # print(Str_PO.str2dict("{'a':'123', 'b':456}"))  # {'a': '123', 'b': 456}
    # # print(Str_PO.str2dict("{'a':'1', 'b':2, 'c'}"))  # None
    # d = Str_PO.str2dict('{"currPage": 0, "deptId": "", "endTime": "", "pageSize": 120, "searchId": "", "searchName": "", "starTime": ""}')
    # print(d['pageSize'])  # 120
    #
    # print("1.4，字符串转换成日期".center(100, "-"))
    # print(Str_PO.str2date('2020年11月23日'))
    # print(Str_PO.str2date('2020-11-23'))
    # print(Str_PO.str2date('2020/11/23'))
    # print(Str_PO.str2date('二零二零年十一月二十三日'))
    # print(Str_PO.str2date('二零年十一月二三日'))
    # print(Str_PO.str2date('20年1月5日'))
    # print(Str_PO.str2date('20年01月05日'))

    # print("2.1，判断字符串是否为数字".center(100, "-"))
    # print(Str_PO.isNumber('foo'))  # False
    # print(Str_PO.isNumber('1'))  # True
    # print(Str_PO.isNumber('1.3'))  # True
    # print(Str_PO.isNumber('-1.37'))  # True
    # print(Str_PO.isNumber('1e3'))  # True
    # print(Str_PO.isNumber('٥'))  # True   //# 阿拉伯语 5
    # print(Str_PO.isNumber('๒'))  # True  //# 泰语 2
    # print(Str_PO.isNumber('四'))  # True  /# 中文数字
    # print(Str_PO.isNumber('©'))  # False  /# 版权号
    #
    # print("2.2，判断字符串是否是中文".center(100, "-"))
    # print(Str_PO.isChinese("测试"))  # True //字符串全部是中文
    # print(Str_PO.isChinese("测123试"))  # False //字符串有非中文字符
    #
    # print("2.3，判断字符串中是否包含中文".center(100, "-"))
    # print(Str_PO.isContainChinese("123123123"))  # False   //字符串中没有中文
    # print(Str_PO.isContainChinese("12312312jin金浩3"))  # True   //字符串中有中文
    # print(Str_PO.isContainChinese("测试一下"))  # True   //字符串中有中文

    # print("2.4 判断复数".center(100, "-"))
    # print(Str_PO.isComplex(123))  # True
    # print(Str_PO.isComplex(-123))  # True
    # print(Str_PO.isComplex(123456768567868756756757575675657567567567.77434))  # True
    # print(Str_PO.isComplex(0.23456))  # True
    # print(Str_PO.isComplex(000000.23456))  # True
    # print(Str_PO.isComplex(complex(1, 2)))  # True
    # print(Str_PO.isComplex(complex("1")))  # True
    # print(Str_PO.isComplex(complex("1+2j")))  # True
    # print(Str_PO.isComplex(True))  # True
    # print(Str_PO.isComplex(False))  # True
    # print(Str_PO.isComplex("100"))  # True
    # print(Str_PO.isComplex("1234.56768567868"))  # True
    # print(Str_PO.isComplex("二"))  # False
    # print(Str_PO.isComplex("123Abc"))  # False

    # print("3，删除特殊字符".center(100, "-"))
<<<<<<< HEAD
    # print(Str_PO.delSpecialChar('～！@#¥%……&*（）测试1*2《3》4？5/6\\7|8:'))
=======
    print(Str_PO.delSpecialChar('～！@#¥%……&*（）测试1*2《3》4？5/6\\7|8:'))
>>>>>>> origin/master
    # # #创作灵感 只需三招，就能:让你*成为一<个狠>人！#|人生感悟 #智慧人生 #为人处世

    # print("4，字符串列表大写转小写".center(100, "-"))
    # x = ['ADD', 'ANALYZE', 'ASC', 'BETWEEN', 'BLOB', 'CALL', 'CHANGE', 'CHECK', 'CONDITION', 'CONTINUE', 'CROSS', 'CURRENT_TIMESTAMP', 'DATABASE', 'DAY_MICROSECOND', 'DEC', 'DEFAULT', 'DESC', 'DISTINCT', 'DOUBLE', 'EACH', 'ENCLOSED', 'EXIT', 'FETCH', 'FLOAT8', 'FOREIGN', 'GOTO', 'HAVING', 'HOUR_MINUTE', 'IGNORE', 'INFILE', 'INSENSITIVE', 'INT1', 'INT4', 'INTERVAL', 'ITERATE', 'KEYS', 'LEADING', 'LIKE', 'LINES', 'LOCALTIMESTAMP', 'LONGBLOB', 'LOW_PRIORITY', 'MEDIUMINT', 'MINUTE_MICROSECOND', 'MODIFIES', 'NO_WRITE_TO_BINLOG', 'ON', 'OPTIONALLY', 'OUT', 'PRECISION', 'PURGE', 'READ', 'REFERENCES', 'RENAME', 'REQUIRE', 'REVOKE', 'SCHEMA', 'SELECT', 'SET', 'SPATIAL', 'SQLEXCEPTION', 'SQL_BIG_RESULT', 'SSL', 'TABLE', 'TINYBLOB', 'TO', True, 'UNIQUE', 'UPDATE', 'USING', 'UTC_TIMESTAMP', 'VARCHAR', 'WHEN', 'WITH', 'XOR', 'ALL', 'AND', 'ASENSITIVE', 'BIGINT', 'BOTH', 'CASCADE', 'CHAR', 'COLLATE', 'CONNECTION', 'CONVERT', 'CURRENT_DATE', 'CURRENT_USER', 'DATABASES', 'DAY_MINUTE', 'DECIMAL', 'DELAYED', 'DESCRIBE', 'DISTINCTROW', 'DROP', 'ELSE', 'ESCAPED', 'EXPLAIN', 'FLOAT', 'FOR', 'FROM', 'GRANT', 'HIGH_PRIORITY', 'HOUR_SECOND', 'IN', 'INNER', 'INSERT', 'INT2', 'INT8', 'INTO', 'JOIN', 'KILL', 'LEAVE', 'LIMIT', 'LOAD', 'LOCK', 'LONGTEXT', 'MATCH', 'MEDIUMTEXT', 'MINUTE_SECOND', 'NATURAL', 'NULL', 'OPTIMIZE', 'OR', 'OUTER', 'PRIMARY', 'RAID0', 'READS', 'REGEXP', 'REPEAT', 'RESTRICT', 'RIGHT', 'SCHEMAS', 'SENSITIVE', 'SHOW', 'SPECIFIC', 'SQLSTATE', 'SQL_CALC_FOUND_ROWS', 'STARTING', 'TERMINATED', 'TINYINT', 'TRAILING', 'UNDO', 'UNLOCK', 'USAGE', 'UTC_DATE', 'VALUES', 'VARCHARACTER', 'WHERE', 'WRITE', 'YEAR_MONTH', 'ALTER', 'AS', 'BEFORE', 'BINARY', 'BY', 'CASE', 'CHARACTER', 'COLUMN', 'CONSTRAINT', 'CREATE', 'CURRENT_TIME', 'CURSOR', 'DAY_HOUR', 'DAY_SECOND', 'DECLARE', 'DELETE', 'DETERMINISTIC', 'DIV', 'DUAL', 'ELSEIF', 'EXISTS', False, 'FLOAT4', 'FORCE', 'FULLTEXT', 'GROUP', 'HOUR_MICROSECOND', 'IF', 'INDEX', 'INOUT', 'INT', 'INT3', 'INTEGER', 'IS', 'KEY', 'LABEL', 'LEFT', 'LINEAR', 'LOCALTIME', 'LONG', 'LOOP', 'MEDIUMBLOB', 'MIDDLEINT', 'MOD', 'NOT', 'NUMERIC', 'OPTION', 'ORDER', 'OUTFILE', 'PROCEDURE', 'RANGE', 'REAL', 'RELEASE', 'REPLACE', 'RETURN', 'RLIKE', 'SECOND_MICROSECOND', 'SEPARATOR', 'SMALLINT', 'SQL', 'SQLWARNING', 'SQL_SMALL_RESULT', 'STRAIGHT_JOIN', 'THEN', 'TINYTEXT', 'TRIGGER', 'UNION', 'UNSIGNED', 'USE', 'UTC_TIME', 'VARBINARY', 'VARYING', 'WHILE', 'X509', 'ZEROFILL']
    # print([str(i).lower() for i in x])

    # print("5.1 浮点数四舍五入到整数位（取整）".center(100, "-"))
    # print(Str_PO.roundInt(12.523))  # 13
    # print(Str_PO.roundInt(13.523))  # 14

    # print("5.3 数字转字符串小数点后补0".center(100, "-"))
    # print(Str_PO.addZero(123.56, 2))  # 123.5600   //数字，小数位后追加2个0
    # print(Str_PO.addZero(88, 0))  # 88
    # print(Str_PO.addZero(-17, 3))  # -17.000
    # print(Str_PO.addZero((18), 6))  # 18.000000  //元组，小数位后追加6个0
    # print(Str_PO.addZero('15', 1))  # 15.0       //字符串，小数位后追加1个0
    # print(Str_PO.addZero('14', 0))  # 14
    # print(Str_PO.addZero('16', 6))  # 16.000000
    # print(Str_PO.addZero("11.12345", -4))  # 11.0    //去掉小数后4位
    # print(Str_PO.addZero("22.12345", -5))  # 22      //去掉小数后5位（自动去掉.）,也就是返回整数
    # print(Str_PO.addZero("33.00000", -7))  # 33      //去掉小数后7位，但实际只有5为，因为返回整数。
    # print(Str_PO.addZero(True, 6))  # 1.000000      //布尔，True = 1
    # print(Str_PO.addZero(False, 6))  # 0.000000            //False = 0
    # print(Str_PO.addZero(complex(1, 19), 3))  # (1+19j).000      //复数
    # # print(Str_PO.addZero("abc", 2))  # None   //不支持字符串
    # # print(Str_PO.addZero([1, 2, 3], 2))  # None   //不支持列表

    # print("5.4 数字转字符串小数点后去0".center(100, "-"))
    # print(Str_PO.subZero("1.00"))  # 1
    # print(Str_PO.subZero("1.10"))  # 1.1
    # print(Str_PO.subZero("1"))  # 1
    # print(Str_PO.subZero("0"))  # 0
    # print(Str_PO.subZero("0.0"))  # 0
    # print(Str_PO.subZero("123.5"))  # 123.5
    # print(Str_PO.subZero("123.05"))  # 123.05
    # print(Str_PO.subZero(1.00))  # 1
    # print(type(Str_PO.subZero(1.00)))  # <class 'str'>
    # print(Str_PO.subZero(1.10))  # 1.1
    # print(Str_PO.subZero(1))  # 1
    # print(Str_PO.subZero(0))  # 0
    # print(Str_PO.subZero(0.00))  # 0

    # print("5.5 数字转字符串小数点后不足位数的补零（批量）".center(100, "-"))
    # list1 = [0, 1.0, '2.00', 3.000, 4.4400, 5.5000, 6.0006, 0.0007, 0.00008, 8.123456789, 9.90]
    # print(list1)  # [0, 1.0, '2.00', 3.0, 4.44, 5.5, 6.0006, 0.0007, 8e-05, 8.123456789, 9.9]
    # print(Str_PO.patchZero(list1,
    #                             0))  # ['0', '1', '2', '3', '4.44', '5.5', '6.0006', '0.0007', '8e-05', '8.12346', '9.9']
    # print(Str_PO.patchZero(list1,
    #                             1))  # ['0', '1.0', '2.0', '3.0', '4.44', '5.5', '6.0006', '0.0007', '8e-05.0', '8.12346', '9.9']
    # print(Str_PO.patchZero(list1,
    #                             2))  # ['0', '1.00', '2.00', '3.00', '4.44', '5.50', '6.0006', '0.0007', '8e-05.00', '8.12346', '9.90']
    # print(Str_PO.patchZero(
    #     list1))  # ['0', '1.00', '2.00', '3.00', '4.44', '5.50', '6.0006', '0.0007', '8e-05.00', '8.12346', '9.90']
    # print(Str_PO.patchZero(list1,
    #                             4))  # ['0', '1.0000', '2.0000', '3.0000', '4.4400', '5.5000', '6.0006', '0.0007', '8e-05.0000', '8.12346', '9.9000']
    # list2 = [1, 2.0, 3.01, 40.234, 50009]
    # print(Str_PO.patchZero(list2))  # ['1.00', '2.00', '3.01', '40.234', '50009.00']
    #
    # list3 = [11.00, 22.00, 3.00, '4.0', '5.00000', '6.60']
    # print(Str_PO.patchZero(list3))  # ['11.00', '22.00', '3.00', '4.00', '5.00', '6.00']
    # print(Str_PO.patchZero(list3, 0))  # ['11', '22', '3', '4', '5', '6.6']
    # print(Str_PO.patchZero(list3, 1))  # ['11.0', '22.0', '3.0', '4.0', '5.0', '6.6']

<<<<<<< HEAD
    # tmpdict1 = {"abc": "100.00", "ddd": "7.08", "ccc": "5.80"}
    # for k, v in tmpdict1.items():
    #     tmpdict1[k] = str(Str_PO.subZero(v))
    # print(tmpdict1)  # {'abc': '100', 'ddd': '7.08', 'ccc': '5.8'}
    #
    # def isFloat(str):
    #     s = str.split(".")
    #     if len(s) > 2:
    #         return False
    #     else:
    #         for si in s:
    #             if not si.isdigit():
    #                 return False
    #         return True
    #
    # tmpdict2 = {}
    # tuple1 = (
    #     ("门诊药房(新院)", 1565.00),
    #     ("发热门诊药房", 11.10),
    #     ("外科", "1545.00"),
    #     ("外科1", "1a"),
    # )
    # for k, v in tuple1:
    #     # tmpdict2[k] = str(Str_PO.subZero(v))
    #     if v.isdigit():
    #         tmpdict2[k] = int(v)
    #     else:
    #         if isFloat(v):
    #             tmpdict2[k] = float(v)
    #             print(tmpdict2)
    #
    # print(tmpdict2)  # {'门诊药房(新院)': '1565', '发热门诊药房': '11.1', '外科': '1545'}
=======
    tmpdict1 = {"abc": "100.00", "ddd": "7.08", "ccc": "5.80"}
    for k, v in tmpdict1.items():
        tmpdict1[k] = str(Str_PO.subZero(v))
    print(tmpdict1)  # {'abc': '100', 'ddd': '7.08', 'ccc': '5.8'}

    def isFloat(str):
        s = str.split(".")
        if len(s) > 2:
            return False
        else:
            for si in s:
                if not si.isdigit():
                    return False
            return True

    tmpdict2 = {}
    tuple1 = (
        ("门诊药房(新院)", 1565.00),
        ("发热门诊药房", 11.10),
        ("外科", "1545.00"),
        ("外科1", "1a"),
    )
    for k, v in tuple1:
        # tmpdict2[k] = str(Str_PO.subZero(v))
        if v.isdigit():
            tmpdict2[k] = int(v)
        else:
            if isFloat(v):
                tmpdict2[k] = float(v)
                print(tmpdict2)

    print(tmpdict2)  # {'门诊药房(新院)': '1565', '发热门诊药房': '11.1', '外科': '1545'}
>>>>>>> origin/master
