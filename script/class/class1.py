#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Date       : 2020-3-5
# Description: 类与对象（继承，多态，公有私有，多重继承）
# https://blog.csdn.net/weixin_42994525/article/details/86654983
#****************************************************************
# 类是抽象概念，对象是具体实例
# 类中最重要的是类变量和类方法，类成员之间可以相互调用，程序中可以对类增加类变量，可以用del语句删除类变量。
# 实例（构造）方法 __init__（构造函数）里面的是实例变量，程序中可以任何位置（类里面或者类外面）增加实例变量，删除则用del语句。

# # todo: 类与实例变量

# class Bird:
#     eyes = "two"
#     def __init__(self, color, feet):
#         self.color = color
#         self.feet = feet
#     def call(self, name):
#         print("This bird:", name)
#
# b = Bird("green","two")  # 调用类的构造方法创建对象
# b.call("pigeon")  # This bird: pigeon
# print(b.color, b.feet)  # green two    //输出实例变量
# b.color = "brown"  # 对实例变量重新赋值
# b.skin = 'yellow'  # 新增实例变量
# print(b.color, b.feet, b.skin)  # brown two yellow   //输出更新后的实例变量
# b.call("sparrow")  # This bird: sparrow   //call()第一个参数self代表实例本身
# print(b.eyes)  # two   //输出类变量


#****************************************************************

class Person:
    hair = 'black'
    def __init__(self, name="Will", age=8):
        self.name = name   # 用self定义的变量是实例变量
        self.age = age
        sex = 1  # 没用self定义的变量是局部变量，外界无法访问
        self.sex = 0  # 构造方法初始化sex变量为实例变量。
    def say(self, content):
        print(content)
    def run(self, sound):
        self.say(sound)   # 调用实例对象的方法

    def grow(self):
        if hasattr(self, 'age'):    # 判断实例变量 self.age是否存在
            self.age += 1
            print("有age变量")
        else:
            self.age = 22   # 定义 age 实例变量
            print("无age变量")
        return self  # 返回调用该方法的实例对象
    def isnotexist(self):
        # 实例变量不一定非要在构造方法中定义，也可以在类外或者类里的实例方法中定义
        print(self.age)
    def walk(self):
        print(self, '正在慢慢走')

    '''classmethod修饰的是类方法'''
    @classmethod
    def fly(cls):    # 类方法第一个参数为cls，会自动绑定到类
        print('类方法fly:', cls)

    '''staticmethod修饰的是静态方法'''
    @staticmethod
    def info(p):   # 静态方法不会自动绑定到类
        print('静态方法info:', p)

p = Person()
p.skills = ['programming']  # 在__init__中增加成员变量
print(p.name)  # Will
print(p.age)  # 8
print(p.hair)  # black
print(p.skills)  # ['programming']
del p.name  # 删除p对象的name成员变量，
# print(p.name)  # 报错，因为已经被删除了。
# 注意：不影响其他对象对name的调用，再实例化一个p2对象，name实例变量任然会被构造。
p2 = Person()
print(p2.name)  # Will
print(p)  # <__main__.Person object at 0x000001FCE8651FD0>    //


print("动态增加方法".center(100, "-"))
def info(self):
     print("-----info函数-----", self)
     print("动态增加方法")
     print(self.age)    # 8   //
p.foo = info   # foo是新增的实例方法名，info是我们在外面定义的方法，当然二者名字可以相同
p.foo(p)  # 第一个参数并没有绑定给调，用类的对象第一个参数是实例本身，可用实例名代表
# -----info函数----- <__main__.Person object at 0x000001CF46FC1FD0>
# 动态增加方法
# 8    //调用了类中实例变量的值


print("实例方法调用另一个实例方法".center(100, "-"))
p.run("很大")  # 很大


print("self可以作为变量来访问，或者作为实例方法的返回值".center(100, "-"))
print(p.grow().age)  # 9   //之前构造函数中age = 8
p.isnotexist()  # 9
p.grow().grow().isnotexist()   # //可以多次调用实例方法或变量
# 有age变量
# 有age变量
# 11


print("类也能调用实例方法".center(100, "-"))
print(Person.hair)  # black   //类名.变量名
Person("yoyo", 33).isnotexist()  # 33   //类名.method(参数)
# Person.isnotexist()  会报错，因为缺少self.age参数
Person.walk("你好")  # 你好 正在慢慢走 //Python只要求手动为第一个参数绑定参数值


print("类方法和静态方法".center(100, "-"))
Person.fly()  # 类方法fly: <class '__main__.Person'>   //#调用类方法，类会自动绑定到第一个参数cls
Person.info("真麻烦")  # 静态方法info: 真麻烦   //#调用静态方法，不会自动绑定，第一个参数必须手动输入
p.fly()  # 类方法fly: <class '__main__.Person'>  //使用对象p调用fly类方法，其实还是使用类调用
p.info("好开心")  # 静态方法info: 好开心   //使用对象p调用info静态方法，其实还是使用了类调用







#类命名空间
global_fn = lambda p: print("执行lambda表达式，P参数：",p)
class Category:
    cate_fn = lambda p:print("执行lambda表达式，p参数",p)
#调用全局的global_fn，为参数p传入参数值
global_fn('fkit')
c = Category()
c.cate_fn()

# 类变量
class Address:
    detail = '广州'
    post_code = '2019723'
    def info(self):
        #尝试直接访问类变量
        #print(detail) 报错
        print(Address.detail)
        print(Address.post_code)
Address.info(32) #通过类调用方法，需要手动输入第一个参数
#通过类来访问Address类的类变量
print(Address.detail)
addr = Address()
addr.info()
#修改Address的类变量
Address.detail = "佛山"
Address.post_code = '2018723'
addr.info()


print("类变量与实例变量".center(100, "-"))
# 类变量：又叫静态变量，随着类的加载而存在，随着类的消失而消失；可以被对象调用（不建议），还可以被类名调用；它的数据存储在方法区（共享数据区）的静态区，所以也叫对象的共享数据。
# 实例变量：又叫成员变量，随着对象的创建而存在，随着对象的回收而释放；只能被对象调用；它存储在堆内存的对象中，所以也叫对象的特有数据。
class Inventory:
    quantity = 2000   # 类变量,可以直接用类调用，或用实例调用
    item = '鼠标'

    def __init__(self, x, y):
        self.x = x  # 实例变量,在类的构造函数内以self.开头来定义
        self.y = y
        self.fuc(self.x, self.y)

    #定义实例方法
    def change(self, item, quantity):
        total = 2  # 局部变量
        self.vara = 3  # 局部变量，虽是以self.定义，但并没有在构造函数中进行初始化
        self.item = item
        self.quantity = quantity

    def fuc(self, a, b):
        self.varc = a  # 实例变量，在成员函数fuc()中定义
        self.vard = b

iv = Inventory(1,2)
iv.change('显示器', 500)
print(iv.item)  # 显示器  //访问iv的item和quantity实例变量
print(iv.quantity)  # 500  //访问iv的item和quantity实例变量
print(Inventory.item)  # 鼠标  //访问的是类变量
print(Inventory.quantity)  # 2000  //访问的是类变量

print("通过类名和对象输出类变量值：")
print(Inventory.quantity)
print(iv.quantity)

print("通过对象修改类变量：")
iv.quantity = 11
print(iv.quantity)
print(Inventory.quantity)

print("通过类名修改类变量：")
Inventory.quantity = 33
print(iv.quantity)
print(Inventory.quantity)


print("类变量、实例变量、局部变量".center(100, "-"))
# 对于类变量，类的内存空间和类的实例对象内存空间是独立的。
# 对象实例化时，会拷贝当前类变量的值。
# 若通过类名修改了类变量，那么新对象的类变量值就是修改后的值。
# 若是通过其他对象修改类变量，并不会影响新对象的类变量值，其还是之前的类变量值。
# 也就是说，通过类名修改类变量，会影响之后实例化的对象的类变量值；而通过对象修改类变量，只会影响对象自身，不影响之后的实例化对象。

class Base():
    var1 = 0  # 类变量,可以直接用类调用，或用实例对象调用

    def __init__(self,x,y):
        self.x=x  # 实例变量（成员变量）,必须在构造函数内以self.开头来定义
        self.y=y
        self.fuc(self.x,self.y)

    def add(self):
        total=2  # 局部变量
        self.vara=3  # 局部变量，虽然是self.的形式，但并没有在构造函数中进行初始化
        self.varb=4
        fina=(self.x+self.y)*total
        return fina

    def fuc(self,a,b):
        self.varc=a    # 实例变量，原本是局部变量，但在构造函数中进行了调用与传值，因此 self.varc也是实例变量
        self.vard=b

b = Base(1,2)
print(b.var1)  # 100
print(Base.var1)  # 100

b.var1 = 200
print(b.var1)  # 200
print(Base.var1)  # 100    //实例对象方式修改的类变量，不会影响类方式调用的类变量。实际上b.var1在内存区域开辟了一块新的数据，而Base.var1在方法区里是共享数据。

Base.var1 = 300
print(b.var1)  # 200
print(Base.var1)  # 300    //只是修改了方法区里的共享数据，不影响内存区域里对象b.var1的值。

b2 = Base(1,2)
print(b2.var1)  # 300
print(Base.var1)  # 300

# # *************************************************************************************
#
# # 继承，子类共享父类数据和方法的机制
# # 继承列表属性的类
# class Mylist(list):
#     pass
#     # // Mylist类继承了list，因此实例化的list2具有list的特性。
#
# list2 = Mylist()
# print(list2)   # []
# list2.append(5)
# list2.append(6)
# print(list2)  # [5, 6]
#
# # *************************************************************************************
#
# # 多态，多态指的是父类的引用指向子类的对象
#
# class Animal(object):
#     pass
#
# class Cat(Animal):
#     pass
#
# class Pig(Animal):
#     pass
#
# a = list()
# b = Animal()
# c = Cat()
#
# # isinstance(变量,类型)
# print(isinstance(a, list))  # True
# print(isinstance(b, Animal))  # True
# print(isinstance(c, Cat))  # True
# print(isinstance(c, Animal))  # True
# print(isinstance(b, Pig))  # false
#
# # *************************************************************************************
#
# # 使用多态，不同的子类对象可以共用一个函数
# # 需求：饲养员喂养猫和老鼠，老虎等动物
# # 分析：
# # 定义饲养员的类和动物的类
# # 定义老鼠类，猫类等继承动物类
# # 在饲养员中定义类成员函数，喂养
#
# class Person(object):
#     '''
#     def feedCat(self,cat):
#         print("喂养" + cat.name)
#     def feedMouse(self,mouse):
#         print("喂养" + mouse.name)
#     def feedTiger(self,tiger):
#         print("喂养" + tiger.name)
#     '''
#
#     def feedAnimal(self, ani):
#         print("喂养" + ani.name)
#
#
# class Animal(object):
#     def __init__(self, name):
#         self.name = name
#
#     def eat(self):
#         print("eating")
#
#
# class Mouse(Animal):
#     def __init__(self, name):
#         super(Mouse, self).__init__(name)
#
#
# # 1.创建一个饲养员的对象
# p = Person()
# # 2.创建Mouse的对象
# m = Mouse("Tom")
# # 3.饲养员执行自己的行为
# p.feedAnimal(m)  # 喂养To
#
#
# # *************************************************************************************#
#
# # 公有变量，私有变量
# # 1，默认情况对象的属性和方法都是公有的
# # 2，Python内部给出了一个name mangling（名字改编，名字重整）的机制
# # 在python中定义私有变量只需要在变量名或函数名前加上‘’__‘’两个下划线
# class Person():
#     name = '小义'
#     __alise = '小wang'
#     def getname(self):
#         return self.__alise
#
# p = Person()
# print(p.name)  # '小义'
# # print(p.__alise)  # 报错，AttributeError: 'Person' object has no attribute '__alise'，不能用这种方式访问私有变量。
# print(p._Person__alise)  # 小wang
# print(p.getname())  # 小wang  //通过函数调用私有变量。
#
# # # 》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》
# # # 继承，子类继承父类的属性和方法，如果子类调用的函数与父类同名，则优先调用子类自己的函数。
# #
# # # 继承一般函数，如：hello()
# # class Parent:
# #     def hello(self):
# #         print('正在调用父类的方法')
# # class Child(Parent):
# #     pass
# # p = Parent()
# # p.hello()  # 正在调用父类的方法
# # c = Child()
# # c.hello()  # 正在调用父类的方法
# #
# # class Child(Parent):
# #     def hello(self):
# #         print('子类的方法')
# # c = Child()
# # c.hello()  # 子类的方法
# # p.hello()  # 正在调用父类的方法
# #
# # # 继承构造函数,__init__()
# # import random as r
# # class Fish:
# #     def __init__(self):
# #         self.x = r.randint(0, 10)
# #         self.y = r.randint(0, 10)
# #     def move(self):
# #         self.x -= 1
# #         print('我的位置是：', self.x, self.y)
# #
# # class Goldfish(Fish):
# #     pass
# # class Carp(Fish):
# #     pass
# # class Shark(Fish):
# #     def __init__(self):
# #         self.hungry = True
# #
# #     def eat(self):
# #         if self.hungry:
# #             print('饿了，要进食')
# #             self.hungry = False
# #         else:
# #             print("吃饱了")
# #
# # fish = Fish()
# # fish.move()  # 我的位置是： 2 8
# # goldfish = Goldfish()
# # goldfish.move()  # 我的位置是： 9 0
# # shark = Shark()
# # shark.eat()  # 饿了，要进食
# # shark.eat()  # 吃饱了  , 因为__init__构造函数只执行一次。
# # # shark.move()  # 报错，AttributeError: 'Shark' object has no attribute 'x'， 因为子类shark中新定义的__init__()覆盖了父类fish的方法和属性（__init__()）
# # # 解决方法是在shark的__init__()中第一行添加 Fish.__init__(self) 或 super().__init__()
# # # Fish.__init__(self) ，表示执行Fish的__init__(), 这里要写上self。
# # # super().__init__()， 表示执行父类的__init__，说白了就是将父类覆盖了子类的__init__。
# #
# # # 》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》
# # # 多重继承：一个子类可以继承多个父类的属性和方法
# #
# # class Base1:
# #     def fool1(self):
# #         print('我是fool1')
# # class Base2:
# #     def fool2(self):
# #         print('我是fool2')
# #
# # class C(Base1, Base2):
# #     pass
# # c = C()
# # c.fool1()  # 我是fool1
# # c.fool2()  # 我是fool2
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
