# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-22
# Description   : 字符串对象层
# *********************************************************************

'''
1.1 字符串转列表 str2list()
1.2 字符串转元组 str2tuple()
1.3 字符串转字典 str2dict()
2 判断字符串是否为数字 isNumberByStr()
3 判断字符串中是否包含中文 isContainChinese()
4 判断字符串是否全部是中文 isChinese()
5 判断字符串中数字的位置 indexNumber()
'''

import sys,re

class StrPO():

    def __init__(self):
        pass

    # 1.1 字符串转列表
    def str2list(self, varStr=None, varMode='digit'):
        # print(Str_PO.str2list("1,2,3"))  # [1, 2, 3]    //列表元素是数字， 默认字符串是数字，转换后仍然是数字作为列表元素。
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

    # 1.2 字符串转元组
    def str2tuple(self, varStr):
        try:
            return tuple(eval(varStr))
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 1.3 字符串转字典
    def str2dict(self, varStr):
        # 技巧，如果输出结果中是单引号，这一组就是字典,如：{'a': '123', 'b': 456}
        # 技巧，如果输出结果中是双引号，这一组就是字符串，如：{"a": "192.168.1.1", "b": "192.168.1.2"}
        try:
            return dict(eval(varStr))
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    # 2 判断字符串是否为数字
    def isNumberByStr(self, s):
        # 可识别中文，阿拉伯语，泰语等数字
        # print(Str_PO.isNumberByStr('foo'))  # False
        # print(Str_PO.isNumberByStr('1'))  # True
        # print(Str_PO.isNumberByStr('1.3'))  # True
        # print(Str_PO.isNumberByStr('-1.37'))  # True
        # print(Str_PO.isNumberByStr('1e3'))  # True
        # print(Str_PO.isNumberByStr('٥'))  # True   //# 阿拉伯语 5
        # print(Str_PO.isNumberByStr('๒'))  # True  //# 泰语 2
        # print(Str_PO.isNumberByStr('四'))  # True  /# 中文数字
        # print(Str_PO.isNumberByStr('©'))  # False  /# 版权号
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False


    # 3 判断字符串中是否包含中文
    def isContainChinese(self, varStr):
        for ch in varStr:
            if u'\u4e00' <= ch <= u'\u9fa5':
                return True
        return False


    # 4 判断字符串是否全部是中文
    def isChinese(self, varStr):
        for _char in varStr:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True


    # 5 判断字符串中数字的位置
    def indexNumber(self, path=''):
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


    def nonsupportChar(self, var1):
        # 对文件和文件夹命名是不能使用以下9个字符： /  \: *" < > | ？
        return str(var1).replace("/", "").replace("\\", "").replace(":", "").replace("*", "").replace("\"", "").replace("<", "").replace(">", "").replace("|", "").replace("?", "").replace(" ", "")


if __name__ == "__main__":

    Str_PO = StrPO()

    print(Str_PO.nonsupportChar('#创作灵感 只需三招，就能让你成为一个狠人！#人生感悟 #智慧人生 #为人处世'))

    # print("1.1，字符串转列表".center(100, "-"))
    # print(Str_PO.str2list("1,2,3"))  # [1, 2, 3]    //列表元素是数字， 默认字符串是数字，转换后仍然是数字作为列表元素。
    # print(Str_PO.str2list("a1,2,3"))  # ['a1', '2', '3']
    # print(Str_PO.str2list("1,2,3", ""))  # ['1', '2', '3']   //列表元素是字符，第二个空参数表示转换后列表元素是字符。
    # print(Str_PO.str2list("123", ""))  # ['123']
    # print(Str_PO.str2list("123,"))  # [123]   // 当一个数字元素转列表，且转换后仍然是数字作为列表元素时，需在单个元素最后加上逗号
    # print(Str_PO.str2list("123"))  # ['123']
    # print(Str_PO.str2list("test"))  # ['test']
    # print(Str_PO.str2list(121131313))  # None   //错误参数返回None
    # print(Str_PO.str2list())  # None   //无参数返回None
    #
    #
    # print("1.2，字符串转元组".center(100, "-"))
    # print(Str_PO.str2tuple("1,2,3,4"))  # (1, 2, 3, 4)
    # print(Str_PO.str2tuple("1,"))  # (1,)   //一个字符转元组的话，需要再后面添加逗号
    # print(Str_PO.str2tuple("1,2,3,[1,2,3]"))  # (1, 2, 3, [1, 2, 3])
    #
    # print("1.3，字符串转字典".center(100, "-"))
    # print(Str_PO.str2dict("{'a':'123', 'b':456}"))  # {'a': '123', 'b': 456}
    # print(Str_PO.str2dict("{'a':'1', 'b':2, 'c'}"))  # None
    #
    #
    #
    # print("2，判断字符串是否为数字".center(100, "-"))
    # print(Str_PO.isNumberByStr('foo'))  # False
    # print(Str_PO.isNumberByStr('1'))  # True
    # print(Str_PO.isNumberByStr('1.3'))  # True
    # print(Str_PO.isNumberByStr('-1.37'))  # True
    # print(Str_PO.isNumberByStr('1e3'))  # True
    # print(Str_PO.isNumberByStr('٥'))  # True   //# 阿拉伯语 5
    # print(Str_PO.isNumberByStr('๒'))  # True  //# 泰语 2
    # print(Str_PO.isNumberByStr('四'))  # True  /# 中文数字
    # print(Str_PO.isNumberByStr('©'))  # False  /# 版权号
    #
    #
    # print("3，判断字符串中是否包含中文".center(100, "-"))
    # print(Str_PO.isContainChinese("123123123"))  # False   //字符串中没有中文
    # print(Str_PO.isContainChinese("12312312jin金浩3"))  # True   //字符串中有中文
    # print(Str_PO.isContainChinese("测试一下"))  # True   //字符串中有中文
    #
    #
    # print("4，判断字符串是否全部是中文".center(100, "-"))
    # print(Str_PO.isChinese("测试"))  # True //字符串全部是中文
    # print(Str_PO.isChinese("测123试"))  # False //字符串有非中文字符
    #
    #
    # print("5，判断字符串中数字的位置".center(100, "-"))
    # print(Str_PO.indexNumber("abc1test2ok"))  #[['1', 3], ['2', 8]]
    #
    #
    # print("判断字符串某字符串出现的个数".center(100, "-"))
    # x = "123%123234%"
    # print(x.count("%"))