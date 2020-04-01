# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-9-19
# Description: python的框架案例
# python里特殊方法专用的标识，如 __init__（）代表类的构造函数。
# *****************************************************************
name = "igor"
number = 10

# __len__ 获取变量值字符个数
print(name.__len__())  # 4    等同于 print(len(name))

# __add__ 只做加法运算，并不会保存结果
print(number.__add__(20))  # 30
print(number)  # 10



class Room(object):
    def __init__(self):
        self.people = []

    def add(self, person):
        self.people.append(person)

    def __len__(self):
        return len(self.people)

r = Room()
r.add("john")
r.add("titi")
r.add("yoyo")
r.add("baba")
print(r.people)  # ['john', 'titi', 'yoyo', 'baba']
print(len(r.people))  # 4
print(len(r))  # 4， 这里必须要有 __len__ 系统函数