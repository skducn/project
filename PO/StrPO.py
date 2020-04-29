# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-22
# Description   : 字符串对象层
# *********************************************************************


class StrPO():

    def __init__(self):
        pass


    # 1.1，字符串转列表
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
                return None

    # 1.2，字符串转元组
    def str2tuple(self, varStr):
        try:
            return tuple(eval(varStr))
        except:
            return None

    # 1.3，字符串转字典
    def str2dict(self, varStr):
        # 技巧，如果输出结果中是单引号，这一组就是字典,如：{'a': '123', 'b': 456}
        # 技巧，如果输出结果中是双引号，这一组就是字符串，如：{"a": "192.168.1.1", "b": "192.168.1.2"}
        try:
            return dict(eval(varStr))
        except:
            return None


    # 2，判断字符串是否为数字
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


    # 3，判断字符串中是否包含中文
    def isContainChinese(self, varStr):
        for ch in varStr:
            if u'\u4e00' <= ch <= u'\u9fa5':
                return True
        return False


    # 4，判断字符串是否全部是中文
    def isChinese(self, varStr):
        for _char in varStr:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True


if __name__ == "__main__":

    Str_PO = StrPO()


    print("1.1，字符串转列表".center(100, "-"))
    print(Str_PO.str2list("1,2,3"))  # [1, 2, 3]    //列表元素是数字， 默认字符串是数字，转换后仍然是数字作为列表元素。
    print(Str_PO.str2list("a1,2,3"))  # ['a1', '2', '3']
    print(Str_PO.str2list("1,2,3", ""))  # ['1', '2', '3']   //列表元素是字符，第二个空参数表示转换后列表元素是字符。
    print(Str_PO.str2list("123", ""))  # ['123']
    print(Str_PO.str2list("123,"))  # [123]   // 当一个数字元素转列表，且转换后仍然是数字作为列表元素时，需在单个元素最后加上逗号
    print(Str_PO.str2list("123"))  # ['123']
    print(Str_PO.str2list("test"))  # ['test']
    print(Str_PO.str2list(121131313))  # None   //错误参数返回None
    print(Str_PO.str2list())  # None   //无参数返回None


    print("1.2，字符串转元组".center(100, "-"))
    print(Str_PO.str2tuple("1,2,3,4"))  # (1, 2, 3, 4)
    print(Str_PO.str2tuple("1,"))  # (1,)   //一个字符转元组的话，需要再后面添加逗号
    print(Str_PO.str2tuple("1,2,3,[1,2,3]"))  # (1, 2, 3, [1, 2, 3])

    print("1.3，字符串转字典".center(100, "-"))
    print(Str_PO.str2dict("{'a':'123', 'b':456}"))  # {'a': '123', 'b': 456}
    print(Str_PO.str2dict("{'a':'1', 'b':2, 'c'}"))  # None



    print("2，判断字符串是否为数字".center(100, "-"))
    print(Str_PO.isNumberByStr('foo'))  # False
    print(Str_PO.isNumberByStr('1'))  # True
    print(Str_PO.isNumberByStr('1.3'))  # True
    print(Str_PO.isNumberByStr('-1.37'))  # True
    print(Str_PO.isNumberByStr('1e3'))  # True
    print(Str_PO.isNumberByStr('٥'))  # True   //# 阿拉伯语 5
    print(Str_PO.isNumberByStr('๒'))  # True  //# 泰语 2
    print(Str_PO.isNumberByStr('四'))  # True  /# 中文数字
    print(Str_PO.isNumberByStr('©'))  # False  /# 版权号


    print("3，判断字符串中是否包含中文".center(100, "-"))
    print(Str_PO.isContainChinese("123123123"))  # False   //字符串中没有中文
    print(Str_PO.isContainChinese("12312312jin金浩3"))  # True   //字符串中有中文
    print(Str_PO.isContainChinese("测试一下"))  # True   //字符串中有中文


    print("4，判断字符串是否全部是中文".center(100, "-"))
    print(Str_PO.isChinese("测试"))  # True //字符串全部是中文
    print(Str_PO.isChinese("测123试"))  # False //字符串有非中文字符
