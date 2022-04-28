# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-5-9
# Description: python特殊方法之 __getitem__
# __getitem__ 可以让对象实现迭代功能，这样就可以使用for...in... 来迭代该对象了
# *****************************************************************

import re
RE_WORD = re.compile(r'\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)  # re.findall函数返回一个字符串列表，里面的元素是正则表达式的全部非重叠匹配
        print(self.words)  # ['The', 'time', 'has', 'come']
    def __getitem__(self, index):
        return self.words[index]

print("__getitem__1".center(100, "-"))
s = Sentence('The time has come')
print(s[0])  # The
print(s[1])  # time


class Animal:
    def __init__(self, animal_list):
        self.animals_name = animal_list

    def __getitem__(self, index):
        return self.animals_name[index]

print("__getitem__2".center(100, "-"))
animals = Animal(["dog","cat","fish"])
# 在用 for..in.. 迭代对象时，如果对象没有实现 __iter__ __next__ 迭代器协议，Python会去找__getitem__ 来迭代对象，如果连__getitem__ 都没有定义，这解释器就会报对象不是迭代器的错误：
# TypeError: 'Animal' object is not iterable
for animal in animals:
    print(animal)
# dog
# cat
# fish


#如果类把某个属性定义为序列，可以使用__getitem__()输出序列属性中的某个元素.
class FruitShop():
     def __getitem__(self,i):
         return self.fruits[i]#可迭代对象

print("__getitem__3".center(100, "-"))
shop = FruitShop()
shop.fruits = ["apple", "banana"]
for item in shop:
    print(item)


class DataBase:
    '''Python 3 中的类'''

    def __init__(self, id, address):
        '''初始化方法'''
        self.id = id
        self.address = address
        self.d = {self.id: 16,
                  self.address: "192.168.1.1",
                  }

    def __getitem__(self, key):
        return self.d.get(key, "default")

print("__getitem__4".center(100, "-"))
data = DataBase(12, "192.168.2.11")
print(data["test"])  # default  //获取字典中test的值，如无此key默认默认值default
print(data[data.address])  # 192.168.1.1


class DataBase:
    '''Python 3 中的类'''

    def __init__(self, id, address):
        self.id = id
        self.address = address

    def __getitem__(self, key):
        return self.__dict__.get(key, "100")

print("__getitem__5".center(100, "-"))
data = DataBase(1, "192.168.2.11")
print(data["hi"])  # 100
print(data["address"])  # 192.168.2.11




#
#
# name = "igor"
# number = 10
#
# # __len__ 获取变量值字符个数
# print(name.__len__())  # 4    等同于 print(len(name))
#
# # __add__ 只做加法运算，并不会保存结果
# print(number.__add__(20))  # 30
# print(number)  # 10
#
#
# class Room(object):
#     def __init__(self):
#         self.people = []
#
#     def add(self, person):
#         self.people.append(person)
#
#     def __len__(self):
#         return len(self.people)
#
# r = Room()
# r.add("john")
# r.add("titi")
# r.add("yoyo")
# r.add("baba")
# print(r.people)  # ['john', 'titi', 'yoyo', 'baba']
# print(len(r.people))  # 4
# print(len(r))  # 4， 这里必须要有 __len__ 系统函数