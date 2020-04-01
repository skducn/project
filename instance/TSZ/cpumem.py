# coding: utf-8

# __init__其实不是实例化一个类的时候第一个被调用 的方法。当使用 类表达式来实例化一个类时，最先被调用的方法 其实是 __new__ 方法。
# __new__： 对象的创建，是一个静态方法，第一个参数是cls。(想想也是，不可能是self，对象还没创建，哪来的self)
# 先有创建，才有初始化。即先__new__，而后__init__。
# __new__方法在类定义中不是必须写的，如果没定义，默认会调用object.__new__去创建一个对象。如果定义了，就是override,可以custom创建对象的行为。

# __getattr__()方法，动态返回一个属性。
# 当调用不存在的属性时，比如score，Python解释器会试图调用__getattr__(self, 'score')来尝试获得属性，这样，我们就有机会返回score的值
# 注意，只有在没有找到属性的情况下，才调用__getattr__，已有的属性，比如name，不会在__getattr__中查找。
# 注意到任意调用如s.abc都会返回None，这是因为我们定义的__getattr__默认返回就是None。要让class只响应特定的几个属性，我们就要按照约定，抛出AttributeError的错误：
class Student(object):
    def __init__(self, name):
       self.name = name
    def __str__(self):
       return 'Student object (name: %s)' % self.name
    def __getattr__(self, attr):
        if attr=='score':
            return 99
        if attr=='age':
            return lambda:33
	    raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)
    def __call__(self):
        print('My name is %s.' % self.name)

# __call__ ： 对象可call，注意不是类，是对象。


print Student("john") # __str__定义属性返回的格式
# print Student("john")()
print Student("john").name
print Student("john").score  # __getattr__ 动态返回值
print Student("john").age()  # __getattr__ 动态返回函数
print Student("john").peerage212  # 任意调用不存在的属性,__getattr__默认返回None

# 我们需要判断一个对象是否能被调用，能被调用的对象就是一个Callable对象，比如函数和我们上面定义的带有__call()__的类实例：
# 通过callable()函数，我们就可以判断一个对象是否是“可调用”对象。
print callable(Student("john"))  # True
print callable(max)  # True
print callable(None) # False


# __iter__ ,如果一个类想被用于for ... in循环，类似list或tuple那样，就必须实现一个__iter__()方法，该方法返回一个迭代对象，
# 然后，Python的for循环就会不断调用该迭代对象的next()方法拿到循环的下一个值，直到遇到StopIteration错误时退出循环。
# 举例,输出斐波那契数
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b
    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己
    def next(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 1000: # 退出循环的条件
            raise StopIteration();
        return self.a # 返回下一个值

# __getitem__
# 以上Fib实例虽然能作用于for循环，看起来和list有点像，但是，把它当成list来使用还是不行，比如，取第5个元素：
# 使用__getitem__ 来或不下标访问数列的任意一项 ,如下Fib2
class Fib2(object):
	def __getitem__(self, n):
		a, b = 1, 1
		for x in range(n):
			a, b = b, a + b
		return a
# for n in Fib():
# 	print n
f = Fib2()
print "__getitem__ , "+ str(f[6])
print "__getitem__ , "+ str(f[11])
