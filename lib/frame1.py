# -*- coding: utf-8 -*-

'''
1.__new__(cls, *args, **kwargs)  创建对象时调用，返回当前对象的一个实例;注意：这里的第一个参数是cls即class本身
2.__init__(self, *args, **kwargs) 创建完对象后调用，对当前对象的实例的一些初始化，无返回值,即在调用__new__之后，根据返回的实例初始化；注意，这里的第一个参数是self即对象本身【注意和new的区别】
3.__call__(self,  *args, **kwargs) 如果类实现了这个方法，相当于把这个类型的对象当作函数来使用，相当于 重载了括号运算符
4.__eq__ 定义了类的等号(==)行为 ， 一般用于类的比较，发回ture
'''

from time import sleep

# ／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／


# class A(object):
#
#     '''__eq__ 定义了类的等号(==)行为 ， 一般用于类的比较，发回ture'''
#
#     def __init__(self, name):
#         self.name = name
#
#     # __eq__ 定义了类的等号(==)行为
#     def __eq__(self, obj):
#         return self.name == obj.name
#
# if __name__ == '__main__':
#     a = A("Leon")
#     b = A("Leon")
#     print(a == b)  # 使用__eq__ 判断两个类比较是否相等


# # ／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／
#
class Obj():

     ''' # is 与 == 的区别：is是内存地址比较，而 == 是值的比较
     # 只有数值型和字符串型的情况下，a is b才为True，其他 tuple，list，dict，set，obj 型时，a is b均为 False '''

     def __init__(self,arg):
         self.x = arg

     def __eq__(self,other):
        return self.x == other.x

if __name__ == '__main__':

     # 只有数值型和字符串型的情况下，a is b才为True，其他 tuple，list，dict，set，obj 型时，a is b均为 False
     a = 1  # a和b为数值类型
     b = 1
     print(a is b) #True

     a = 'cheesezh'  # a和b为字符串类型
     b = 'cheesezh'
     print(a is b)  # True

     a = (1, 2, 3)  # a和b为元组类型
     b = (1, 2, 3)
     print(a is b) # False

     a = [1, 2, 3]  # a和b为list类型
     b = [1, 2, 3]
     print(a is b)  # False

     a = {'cheese': 1, 'zh': 2}  # a和b为dict类型
     b = {'cheese': 1, 'zh': 2}
     print(a is b) # False

     a = set([1, 2, 3])  # a和b为set类型
     b = set([1, 2, 3])
     print(a is b) # False

     obj1 = Obj(1)
     obj2 = Obj(1)
     print(obj1 is obj2) #False
     print(obj1 == obj2) #True
#
# # ／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
#
# class O(object):
#
#     '''
#     1.__new__(cls, *args, **kwargs)  创建对象时调用，返回当前对象的一个实例;注意：这里的第一个参数是cls即class本身
#     2.__init__(self, *args, **kwargs) 创建完对象后调用，对当前对象的实例的一些初始化，无返回值,即在调用__new__之后，根据返回的实例初始化；注意，这里的第一个参数是self即对象本身【注意和new的区别】
#     3.__call__(self,  *args, **kwargs) 如果类实现了这个方法，相当于把这个类型的对象当作函数来使用，相当于 重载了括号运算符
#     '''
#
#     def __init__(self, *args, **kwargs):
#         print "init"
#         super(O, self).__init__(*args, **kwargs)
#
#     def __new__(cls, *args, **kwargs):
#         print "new"
#         return super(O, cls).__new__(cls, *args, **kwargs)
#
#     def __call__(self, *args, **kwargs):
#         print "call"
#
# class Foo(object):
#
#     def __call__(self):
#         print "121212"
#
#
# class Person(object):
#     """Silly Person"""
#
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def __str__(self):
#         return '<Person: %s(%s)>' % (self.name, self.age)
#
#
# if __name__ == '__main__':
#     piglei = Person('piglei', 24)
#     print piglei  # <Person: piglei(24)>
#
#     f = Foo()  # 类Foo可call
#     f()  # 对象f可call,121212
#     f.__call__()  # 结果同上,121212
#
#     oo = O()  # new , init
#     print "________"
#     oo()  # call
#
# # ／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／
#
# # 如果要把一个类的实例变成 str，就需要实现特殊方法__str__()：
#
# class Person(object):
#     def __init__(self, name, gender):
#         self.name = name
#         self.gender = gender
#
# class Student(Person):
#
#     '''' # __str__()用于显示给用户，而__repr__()用于显示给开发人员。'''
#
#     def __init__(self, name, gender, score):
#         super(Student, self).__init__(name, gender)
#         self.score = score
#
#     def __str__(self):
#         return '(Student: %s, %s, %s)' % (self.name, self.gender, self.score)
#
#     # __repr__ = __str__  # 偷懒的办法
#
#
# s = Student('Bob', 'male', 88)
# print s  # (Student: Bob, male, 88)
#
# # ／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／／
#
# animal.py
# class animal(object):
#     '''
#     classdocs
#     '''
#
#     def __init__(self):
#         '''
#         Constructor
#         '''
#         print 'animal init'
#
#     def say(self):
#         print 'animal say'
#
#
# child.py
# from inheritance.base import animal
#
#
# class cat(animal):
#
#     def __init__(self):
#         animal.__init__(self)
#         print 'cat init'
#
#     def say(self):
#         animal.say(self)
#         print 'cat say'
#
#
# if __name__ == '__main__':
#     c = cat()
#     c.say()
#
# # 结果：
# # animal init
# # cat init
# # animal say
# cat say