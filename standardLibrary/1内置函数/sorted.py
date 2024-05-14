# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: 对所有可迭代对象(列表、元组、字典、集合、字符串)进行排序，输出列表
# 标准库：https://docs.python.org/zh-cn/3.7/library/functions.html#sorted
# 语法：sorted(iterable, *, key=None, reverse=False)
# 定义：对 iterable 进行排序，生成一个新的序列列表，不改变原值。
# 升序排序规则："空格，特殊字符，大写字母，小写字母，中文"

# todo 参数key的用法
# 规则：key可以是一个函数，将函数结果返回给key，然后对key进行排序

# todo operator库函数
# operator库函数两个类方法 itemgetter(), attrgetter() 自定义排序规则，这种方法更好理解并且效率更高

# todo sorted与 list.sort()区别
# sorted() 对所有可迭代对象(列表、元组、字典、集合、字符串)进行排序，它不改变原值，生成一个新的序列列表，它是内置函数。
# sort() 对列表进行排序，改变列表原值，它是列表的方法。
# ********************************************************************************************************************

from operator import itemgetter, attrgetter

"""
1，对序列进行升序排序
2，对索引位置的元素进行排序
2.2 对类中索引位置的元素进行排序
3，将另一个字典值的顺序，对名字进行排序。
"""


print("1，对所有可迭代对象进行排序".center(100, "-"))
print(sorted([2, 5, 3, 1, 6]))  # [1, 2, 3, 5, 6]  // 对列表升序排序
print(sorted(("b", "a", "c"), reverse=True))  # ['c', 'b', 'a'] // 对元组降序排序，输出列表
print(sorted({2: 200, 1: 100, 4: 300, 3: 400}))  # [1, 2, 3, 4] //对字典键升序排序，输出列表key
print(sorted({'葡萄', '火龙果', '释迦牟尼果', '开心果', '榴莲'}, key=lambda x: len(x)))  # ['葡萄', '榴莲', '开心果', '火龙果', '释迦牟尼果']  //对集合升序排序，输出列表，规则：按照元素长度，字母顺序排序
print(sorted("Meye is测试 S。.kn"))  # [' ', ' ', '.', 'M', 'S', 'e', 'e', 'i', 'k', 'n', 's', 'y', '。', '测', '试']  // 对字符串排序，输出列表


# print("2.1，对字符串中每个单词首字母升序排序，输出每个单词 ？？？".center(100, "-"))
# print(sorted("This is a App andrew".split(), key=str.lower))  # ['a', 'andrew', 'App', 'is', 'This']  //每个单词从a - z 排序，输出原值
# print(sorted("This is a App andrew".split(), key=str.upper))  # ['a', 'andrew', 'App', 'is', 'This']  //每个单词从A - Z 排序，输出原值
# print(sorted("This is a App andrew".split(), key=str.lower, reverse=True))  # ['This', 'is', 'App', 'andrew', 'a']  // 降序


print("2，对索引位置的元素进行排序".center(100, "-"))
list1 = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
# 对所有元组中第3个元素进行升序排列
print(sorted(list1, key=lambda list1: list1[2]))  # [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
# 对所有元组中第3个元素进行升序排列
print(sorted(list1, key=itemgetter(2)))  # [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
# 对所有元组中第1个元素进行升序排列，再对第2个元素进行升序排列
print(sorted(list1, key=itemgetter(1, 2)))  # [('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]
# 对所有元组中第1个元素进行升序排列，再对第2个元素进行降序排列
print(sorted(sorted(list1, key=itemgetter(1)), key=itemgetter(2), reverse=True))  # [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]

list2 = [{'level': 19, 'star': 36, 'time': 1},
       {'level': 20, 'star': 40, 'time': 2},
       {'level': 20, 'star': 40, 'time': 3},
       {'level': 18, 'star': 40, 'time': 1}]

print(sorted(list2, key=lambda k: (k.get('time')))) # [{'level': 19, 'star': 36, 'time': 1}, {'level': 18, 'star': 40, 'time': 1}, {'level': 20, 'star': 40, 'time': 2}, {'level': 20, 'star': 40, 'time': 3}]
s = sorted(list2, key=lambda k: (k.get('time', 0)))
# print(sorted(s,key=lambda k: (k.get('level', 0)),reverse=True))
s = sorted(s, key=lambda k: (k.get('level', 0), k.get('star', 0)), reverse=True)
print(s)

print("2.2 对类中索引位置的元素进行排序".center(100, "-"))
class Student:
    def __init__(self, name, grade, age):
        self.name = name
        self.grade = grade
        self.age = age
    def __repr__(self):
        return repr((self.name, self.grade, self.age))
student_objects = [
    Student('john', 'A', 25),
    Student('jane', 'B', 22),
    Student('dave', 'B', 20)]
# 对age进行升序排列
print(sorted(student_objects, key=lambda student: student.age))  # [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]
# 对age进行升序排列
print(sorted(student_objects, key=attrgetter('age')))  # [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]
# 对grade，age进行升序排列
print(sorted(student_objects, key=attrgetter('grade', 'age')))  # [('john', 'A', 25), ('dave', 'B', 20), ('jane', 'B', 22)]
# 对age升序，再对grade降序
print(sorted(sorted(student_objects, key=attrgetter('age')), key=attrgetter('grade'), reverse=True))  # [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]
# 对grade降序，再对age升序
print(sorted(sorted(student_objects, key=attrgetter('grade'), reverse=True), key=attrgetter('age')))  # [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]


print("3，将另一个字典值的顺序，对名字进行排序。".center(100, "-"))
name = ['dave', 'john', 'YOYO']
score = {'john': 'C', 'YOYO' : 'A', 'dave': 'B', 'steven': 'F'}
print(sorted(name, key=score.__getitem__))  # ['YOYO', 'dave', 'john']






