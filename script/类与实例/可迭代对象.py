#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Date       : 2023-12-29
# Description: 实现可迭代对象
# https://pythonjishu.com/zifazjnjqupeurz/
# 使用__iter__魔法方法来实现一个可迭代对象。
# 在MyList类中定义了一个__iter__方法，使得对象能够被迭代。
# 使用iter函数将实例转化为一个迭代器，然后在for循环中使用这个迭代器来遍历对象。
#****************************************************************

class Mylist:

    def __init__(self, list):
        self.list = list

    def __iter__(self):
        return iter(self.list)

mylist = Mylist([1,2,3,4,5])

for i in mylist:
    print(i)


