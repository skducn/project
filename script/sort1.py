# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: 深入理解python中的排序sort ， https://www.jianshu.com/p/4dd8f1b44704
# 效率比较：  cmp < DSU < key
# ********************************************************************************************************************


# 1，基本排序，使用List内建函数 sorted()
# sorted() 函数不会改变原有的list，而是返回一个新的排好序的list，ta可以接受任何迭代对象，如list,dict,tuple,char, 返回值任然是list。
print(sorted({1: 'D', 2: 'B', 33: 'B', 4: 'E', 5: 'A'}))  # [1, 2, 4, 5, 33]  //字典对象
print(sorted((2, 5, 3, 77, 6)))  # [2, 3, 5, 6, 77]  //元组对象
print(sorted(("g", "a", "c")))  # ['a', 'c', 'g']  //元组对象
print(sorted("This is a test string from andrew".split()))  # ['This', 'a', 'andrew', 'from', 'is', 'string', 'test']  //字符串对象
print(sorted([1,4,3,2,6,54,7]))  # [1, 2, 3, 4, 6, 7, 54]   //列表对象
# list.sort() 就地配列，也就是改变原有的list，无返回对象。


# 2，key函数（key Functions）
# list.sort()和sorted()函数都有一个key参数。
# key参数的值应该是一个函数，这个函数接受一个参数然后返回以一个key，这个key就被用作进行排序。这个方法很高效，因为对于每一个输入的记录只需要调用一次key函数。
# 实例：key用来按大小写优先级顺序排列
print(sorted("This is a test string from andrew".split(), key=str.lower))  # ['a', 'andrew', 'from', 'is', 'string', 'test', 'This']  //字符串对象
print(sorted("This is a test string from andrew".split(), key=str.lower, reverse=True))  # ['This', 'test', 'string', 'is', 'from', 'andrew', 'a']  //降序

# 一般对一个复杂对象的某些属性进行排序时非常好用
# 实例：使用Key和lambda对元组中某个属性排序
student_tuples = [
    ('john', 'A', 15),
    ('jane', 'B', 12),
    ('dave', 'B', 10),]
print(sorted(student_tuples, key=lambda student: student[2]))  # sort by age
# [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

# 继续，封装成对象：
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
    Student('dave', 'B', 20),]
print(sorted(student_objects, key=lambda student: student.age)) # sort by age
# [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]

# 排序的Key-function参数不仅仅可以依赖于排序的对象，也可以依赖于外部的对象.
# 如下例，成绩姓名分开存储。
people = ['dave', 'john', 'jane']
newgrades = {'john': 'F', 'jane':'A', 'dave': 'C'}
print(sorted(people, key=newgrades.__getitem__))  # ['jane', 'dave', 'john']


# 3，operator库函数自定义排序（ Operator Module Functions）
# 这种方法更好理解并且效率更高。
# operator库提供了 itemgetter(), attrgetter(), and a methodcaller()三个函数
from operator import itemgetter, attrgetter
# 对元组第3关键字排序
print(sorted(student_tuples, key=itemgetter(2)))  # [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
print(sorted(student_objects, key=attrgetter('age')))  # [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]
# 多层排序，先对第一关键字排序，在对第二关键字排序
print(sorted(student_tuples, key=itemgetter(1, 2)))  # [('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]
print(sorted(student_objects, key=attrgetter('grade', 'age')))  # [('john', 'A', 25), ('dave', 'B', 20), ('jane', 'B', 22)]
print(sorted(student_tuples, key=itemgetter(2), reverse=True))  # [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)] 对年龄进行降序



# 4，排序的稳定性和复杂排序 （Sort Stability and Complex Sorts）
# 排序的稳定性指，有相同key值的多个记录进行排序之后，原始的前后关系保持不变
data = [('red', 1), ('blue', 122), ('red', 2), ('blue', 2)]
print(sorted(data, key=itemgetter(0)))  # [('blue', 122), ('blue', 2), ('red', 1), ('red', 2)]
# 实例：我们可以利用这个稳定的特性来进行一些复杂的排序步骤，比如，我们将学生的数据先按成绩降序然后年龄升序。当排序是稳定的时候，我们可以先将年龄升序，再将成绩降序会得到相同的结果。
s = sorted(student_objects, key=attrgetter('age'))  # 年龄升序
print(sorted(s, key=attrgetter('grade'), reverse=True))  # 成绩降序
# [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]


# 实例3，对列表中复杂的dict排序，按照dict对象中某一个属性进行排序
lst = [{'level': 19, 'star': 36, 'time': 1},
       {'level': 20, 'star': 40, 'time': 2},
       {'level': 20, 'star': 40, 'time': 3},
       {'level': 20, 'star': 40, 'time': 4},
       {'level': 20, 'star': 40, 'time': 5},
       {'level': 18, 'star': 40, 'time': 1}]

# 需求:
# level越大越靠前;
# level相同, star越大越靠前;
# level和star相同, time越小越靠前;

# 先按time排序
lst.sort(key=lambda k: (k.get('time', 0)))
print(lst)
# [{'level': 19, 'star': 36, 'time': 1}, {'level': 18, 'star': 40, 'time': 1}, {'level': 20, 'star': 40, 'time': 2}, {'level': 20, 'star': 40, 'time': 3}, {'level': 20, 'star': 40, 'time': 4}, {'level': 20, 'star': 40, 'time': 5}]

# 再按照level和star降序
lst.sort(key=lambda k: (k.get('level', 0), k.get('star', 0)), reverse=True)
print(lst)
# [{'level': 20, 'star': 40, 'time': 2}, {'level': 20, 'star': 40, 'time': 3}, {'level': 20, 'star': 40, 'time': 4}, {'level': 20, 'star': 40, 'time': 5}, {'level': 19, 'star': 36, 'time': 1}, {'level': 18, 'star': 40, 'time': 1}]

for idx, r in enumerate(lst):
    print('idx[%d]\tlevel: %d\t star: %d\t time: %d\t' % (idx, r['level'], r['star'],r['time']))
# idx[0]	level: 20	 star: 40	 time: 2
# idx[1]	level: 20	 star: 40	 time: 3
# idx[2]	level: 20	 star: 40	 time: 4
# idx[3]	level: 20	 star: 40	 time: 5
# idx[4]	level: 19	 star: 36	 time: 1
# idx[5]	level: 18	 star: 40	 time: 1



# 5,传统的 DSU(Decorate-Sort-Undecorate)的排序方法
# Decorate，给list添加一个新的值，这个值一般是用来控制排序的顺序
# sort，排序
# Undecorate，将添加的值去掉。
decorated = [(student.grade, i, student) for i, student in enumerate(student_objects)]
decorated.sort()
print([student for grade, i, student in decorated])  # undecorate
# [('john', 'A', 25), ('jane', 'B', 22), ('dave', 'B', 20)]

# 实例
L = [('b', 2), ('a', 1), ('c', 7), ('d',4)]
A = [(x[0], i, x) for i, x in enumerate(L)]  # X[0] 表示对第一关键字升序
A.sort()
L = [s[2] for s in A]
print(L)  # [('a', 1), ('b', 2), ('c', 7), ('d', 4)]
L = [s[0] for s in A]
print(L)  # ['a', 'b', 'c', 'd']

L = [('b', 2), ('a', 1), ('c', 7), ('d',4)]
A = [(x[1], i, x) for i, x in enumerate(L)]  # X[0] 表示对第2关键字升序
A.sort()
L = [s[2] for s in A]
print(L)  # [('a', 1), ('b', 2), ('d', 4), ('c', 7)]
L = [s[0] for s in A]
print(L)  # [1, 2, 4, 7]

# 因为元组是按字典序比较的，比较完grade之后，会继续比较i。
# 添加index的i值不是必须的，但是添加i值有以下好处：
# 可以保证排序的稳定性，如果key值相同，就可以利用i来维持原有的顺序
# 原始对象的item不用进行比较，因为通过key和i的比较就能将数组排序好
# 现在python3提供了key-function，所以DSU方法已经不常用了


# 6，利用cmp方法进行排序的原始方式
# python2.x版本中，是利用cmp参数自定义排序。
# python3.x已经将这个方法移除了，但是我们还是有必要了解一下cmp参数
# cmp参数的使用方法就是指定一个函数，自定义排序的规则，和java等其他语言很类似
from functools import cmp_to_key
L = [2, 3, 1, 4]
L.sort(reverse=True)  # 降序
print(L)  # [4,3,2,1]
L.sort(key=cmp_to_key(lambda a, b: b-a))  # 降序
print(L)  # [4,3,2,1]
L.sort(key=cmp_to_key(lambda a, b: a-b))  # 升序
print(L)  # [1,2,3,4]

# >>> def numeric_compare(x, y):
# ... return x - y
# >>> sorted([5, 2, 4, 1, 3], cmp=numeric_compare)
# [1, 2, 3, 4, 5]
# 也可以反序排列
#
# >>> def reverse_numeric(x, y):
# ... return y - x
# >>> sorted([5, 2, 4, 1, 3], cmp=reverse_numeric)
# [5, 4, 3, 2, 1]
# python3.x中可以用如下方式：
#
# def cmp_to_key(mycmp):
# 'Convert a cmp= function into a key= function'
# class K:
# def __init__(self, obj, *args):
# self.obj = obj
# def __lt__(self, other):
# return mycmp(self.obj, other.obj) < 0
# def __gt__(self, other):
# return mycmp(self.obj, other.obj) > 0
# def __eq__(self, other):
# return mycmp(self.obj, other.obj) == 0
# def __le__(self, other):
# return mycmp(self.obj, other.obj) <= 0
# def __ge__(self, other):
# return mycmp(self.obj, other.obj) >= 0
# def __ne__(self, other):
# return mycmp(self.obj, other.obj) != 0
# return K
# >>> sorted([5, 2, 4, 1, 3], key=cmp_to_key(reverse_numeric))
# [5, 4, 3, 2, 1]


# 7，__It__函数来指定两个对象比较的方式
Student.__lt__ = lambda self, other: self.age < other.age
print(sorted(student_objects)) # [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]










