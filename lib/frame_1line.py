# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-9-19
# Description: python的框架案例
# Python中不存在真正的私有方法。为了实现类似于c++中私有方法，可以在类的方法或属性前加一个“_”单下划线，意味着该方法或属性不应该去调用，它并不属于API。
# *****************************************************************

class Test():
    def __init__(self):
        pass
        print(1212)
    def _one_underline(self):  # 定义私有方法，都只能被类中的函数调用，不能在类外单独调用
        print("_one_underline")
    def __two_underline(self):  # 防止类被覆盖，都只能被类中的函数调用，不能在类外单独调用
        print("__two_underline")
    def output(self):
        self._one_underline()
        self.__two_underline()

if __name__ == "__main__":
    a = Test()   # 1212
    a.output()   # _one_underline ， __two_underline
    a._Test__two_underline()  # __two_underline
    # a._Test__one_underline()  # 报错，AttributeError: 'Test' object has no attribute '_Test__one_underline' , 私有方法不能类直接引用。