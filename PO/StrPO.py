# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-22
# Description   : 字符串对象层
# *********************************************************************

'''
todo：【转换】
1.1 字符串转列表 str2list()
1.2 字符串转元组 str2tuple()
1.3 字符串转字典 str2dict()
1.4 日期字符串转换成日期 str2date()

2.1 判断字符串是否为数字 isNumber()
2.2 判断字符串是否全部是中文 isChinese()
2.3 判断字符串中是否包含中文 isContainChinese()

3 获取字符串中数字的位置(索引) getNumnberIndex()

4 统计字符串中字符重复的次数 getRepeatCount()

5 删除特殊字符 delSpecialCharacters()



'''

import sys, re
from time import strptime
from time import strftime

class StrPO():

    # 1.1 字符串 转 列表
    def str2list(self, varStr=None, varMode='digit'):
        # print(Str_PO.str2list("actualVisitsNumber,plannedVisitsNumber"))  # [1, 2, 3]    //列表元素是数字， 默认字符串是数字，转换后仍然是数字作为列表元素。
        # print(Str_PO.str2list("a1,2,3"))  # ['a1', '2', '3']
        # print(Str_PO.str2list("1,2,3", ""))  # ['1', '2', '3']   //列表元素是字符，第二个空参数表示转换后列表元素是字符。
        # print(Str_PO.str2list("123", ""))  # ['123']
        # print(Str_PO.str2list("123,"))  # [123]   // 当一个数字元素转列表，且转换后仍然是数字作为列表元素时，需在单个元素最后加上逗号
        # print(Str_PO.str2list("123"))  # ['123']
        # print(Str_PO.str2list("test"))  # ['test']
        # print(Str_PO.str2list(121131313))  # None   //错误参数返回None
        # print(Str_PO.str2list())  # None   //无参数返回None
        try:
            if varMode != "digit":
                return (varStr.split(","))  # ['1', '2', '3']
            else:
                list1 = list(eval(varStr))
                return (list1)  # [1, 2, 3]
        except:
            try:
                return (varStr.split(","))  # ['1', '2', '3']
            except:
                print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 1.2 字符串 转 元组
    def str2tuple(self, varStr):
        try:
            return tuple(eval(varStr))
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 1.3 字符串 转 字典
    def str2dict(self, varStr):
        # 技巧，如果输出结果中是单引号，这一组就是字典,如：{'a': '123', 'b': 456}
        # 技巧，如果输出结果中是双引号，这一组就是字符串，如：{"a": "192.168.1.1", "b": "192.168.1.2"}
        try:
            return dict(eval(varStr))
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 1.4 日期字符串转换成日期
    def str2date(self, datestr):
        chinesenum = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '零': '0', '十': '10'}
        strdate = ''
        for i in range(len(datestr)):
            temp = datestr[i]
            if temp in chinesenum:
                if temp == '十':
                    if datestr[i + 1] not in chinesenum:
                        strdate += chinesenum[temp]
                    elif datestr[i - 1] in chinesenum:
                        continue
                    else:
                        strdate += '1'
                else:
                    strdate += chinesenum[temp]
            else:
                strdate += temp
        pattern = ('%Y年%m月%d日', '%Y-%m-%d', '%y年%m月%d日', '%y-%m-%d', '%Y/%m/%d')
        output = '%Y-%m-%d'
        for i in pattern:
            try:
                ret = strptime(strdate, i)
                if ret:
                    return strftime(output, ret)
            except:
                continue
        return False


    # 2.1 判断字符串是否为数字
    def isNumber(self, varStr):
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

    # 2.2 判断字符串是否是中文
    def isChinese(self, varStr):
        for _char in varStr:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    # 2.3 判断字符串中是否包含中文
    def isContainChinese(self, varStr):
        for ch in varStr:
            if u'\u4e00' <= ch <= u'\u9fa5':
                return True
        return False

    # 3 获取字符串中数字的位置(索引)
    def getNumnberIndex(self, path=''):
        # print(Str_PO.getNumnberIndex("abc1test2ok"))  # [['1', 3], ['2', 8]]  第一个数字在位置3，第二个数字在位置8
        kv = []
        nums = []
        beforeDatas = re.findall('\d', path)
        for num in beforeDatas:
            indexV = []
            times = path.count(num)
            if (times > 1):
                if (num not in nums):
                    indexs = re.finditer(num, path)
                    for index in indexs:
                        iV = []
                        i = index.span()[0]
                        iV.append(num)
                        iV.append(i)
                        kv.append(iV)
                nums.append(num)
            else:
                index = path.find(num)
                indexV.append(num)
                indexV.append(index)
                kv.append(indexV)
        # 根据数字位置排序
        indexSort = []
        resultIndex = []
        for vi in kv:
            indexSort.append(vi[1])
        indexSort.sort()
        for i in indexSort:
            for v in kv:
                if (i == v[1]):
                    resultIndex.append(v)
        return resultIndex


    # 4 统计字符串中字符重复的次数
    def getRepeatCount(self, varStr, varChar):
        return varStr.count(varChar)


    # 5 删除特殊字符
    def delSpecialCharacters(self, varStr, *sc):
        # 对文件和文件夹命名是不能使用以下9个字符： /  \: *" < > | ？
        for i in range(len(sc)):
            varStr = str(varStr).replace(sc[i], "")
        return varStr


if __name__ == "__main__":

    Str_PO = StrPO()

    # print("1.1，字符串转列表".center(100, "-"))
    # print(Str_PO.str2list("actualVisitsNumber,plannedVisitsNumber"))  # [1, 2, 3]    //列表元素是数字， 默认字符串是数字，转换后仍然是数字作为列表元素。
    # print(Str_PO.str2list("a1,2,3"))  # ['a1', '2', '3']
    # print(Str_PO.str2list("1,2,3", ""))  # ['1', '2', '3']   //列表元素是字符，第二个空参数表示转换后列表元素是字符。
    # print(Str_PO.str2list("123", ""))  # ['123']
    # print(Str_PO.str2list("123,"))  # [123]   // 当一个数字元素转列表，且转换后仍然是数字作为列表元素时，需在单个元素最后加上逗号
    # print(Str_PO.str2list("123"))  # ['123']
    # x = "[{'name': 'currentPage', 'in': 'query', 'description': '当前页码(必填)', 'required': True, 'type': 'integer', 'format': 'int32'}, {'name': 'docId', 'in': 'query', 'description': '医生id(当前登录用户id(必填))', 'required': True, 'type': 'integer', 'format': 'int32'}, {'name': 'itemId', 'in': 'query', 'description': '项目id(当前登录用户项目id(必填))', 'required': True, 'type': 'integer', 'format': 'int32'}, {'name': 'pageSize', 'in': 'query', 'description': '每页条数(必填)', 'required': True, 'type': 'integer', 'format': 'int32'}]"
    # print(Str_PO.str2list(x))  #
    # print(Str_PO.str2list(x)[0]['name'])  #



    # print(Str_PO.str2list("test"))  # ['test']
    # print(Str_PO.str2list(121131313))  # None   //错误参数返回None
    # print(Str_PO.str2list())  # None   //无参数返回None
    #
    # print("1.2，字符串转元组".center(100, "-"))
    # print(Str_PO.str2tuple("1,2,3,4"))  # (1, 2, 3, 4)
    # print(Str_PO.str2tuple("1,"))  # (1,)   //一个字符转元组的话，需要再后面添加逗号
    # print(Str_PO.str2tuple("1,2,3,[1,2,3]"))  # (1, 2, 3, [1, 2, 3])
    #
    print("1.3，字符串转字典".center(100, "-"))
    # print(Str_PO.str2dict("{'a':'123', 'b':456}"))  # {'a': '123', 'b': 456}
    # print(Str_PO.str2dict("{'a':'1', 'b':2, 'c'}"))  # None
    x = Str_PO.str2dict('{"currPage": 0, "deptId": "", "endTime": "", "pageSize": 0, "searchId": "", "searchName": "", "starTime": ""}')
    print(x['pageSize'])
    #
    # print("1.4，日期字符串转换成日期".center(100, "-"))
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

    # print("2.2，判断字符串是否是中文".center(100, "-"))
    # print(Str_PO.isChinese("测试"))  # True //字符串全部是中文
    # print(Str_PO.isChinese("测123试"))  # False //字符串有非中文字符

    # print("2.3，判断字符串中是否包含中文".center(100, "-"))
    # print(Str_PO.isContainChinese("123123123"))  # False   //字符串中没有中文
    # print(Str_PO.isContainChinese("12312312jin金浩3"))  # True   //字符串中有中文
    # print(Str_PO.isContainChinese("测试一下"))  # True   //字符串中有中文



    # print("3，获取字符串中数字的位置(索引)".center(100, "-"))
    # print(Str_PO.getNumnberIndex("abc1test2ok"))  #[['1', 3], ['2', 8]]  第一个数字在位置3，第二个数字在位置8


    # print("4，统计字符串中字符重复的次数".center(100, "-"))
    # print(Str_PO.getRepeatCount("123%s1232%s34%", "%s"))  # 2
    # print(Str_PO.getRepeatCount("123%123234%", "?"))  # 0


    # print("5，删除特殊字符".center(100, "-"))
    # print(Str_PO.delSpecialCharacters('#创作灵感/ 只需三\招，就能:让你*成为一<个狠>人！#|人生?感悟 #智慧人生 #为人处世',"/","\\","?"))



