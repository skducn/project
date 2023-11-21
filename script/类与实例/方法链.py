# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-3-19
# Description: 方法链
# 法链（method chaining）是面向对象的编程语言中的一种常见语法，可以让开发者在只引用对象一次的情况下，对同一个对象进行多次方法调用
# 如： foo.bar().baz() 连续执行2个方法
# 注意，方法链的一个限制是，只能用在不需要返回其他值的方法上，因为你需要返回 self 对象。即使Python支持用一个 return 语句返回多个值，也可能无法解决这个问题。
# *****************************************************************
import copy

class Person:
    def name(self, value):
        self.name = value
        return self

    def age(self, value):
        self.age = value
        return self

    def introduce(self):
        print("Hello, my name is", self.name, "and I am", self.age, "years old.")

person = Person()
person.name("EarlGrey").age(21).introduce()  # Hello, my name is EarlGrey and I am 21 years old.


class StringProcessor(object):
    '''
    A 类与实例 to process strings in various ways.
    '''
    def __init__(self, st):
        '''Pass a string for st'''
        self._st = st

    def lowercase(self):
        '''Make lowercase'''
        self._st = self._st.lower()
        return self

    def uppercase(self):
        '''Make uppercase'''
        self._st = self._st.upper()
        return self

    def capitalize(self):
        '''Make first char capital (if letter); make other letters lower'''
        self._st = self._st.capitalize()
        return self

    def delspace(self):
        '''Delete spaces'''
        self._st = self._st.replace(' ', '')
        return self

    def rep(self):
        '''Like Python's repr'''
        return self._st

    def dup(self):
        '''Duplicate the object'''
        return copy.deepcopy(self)

def process_string(s):
    sp = StringProcessor(s)
    print('Original:', sp.rep())
    print('After uppercase:', sp.dup().uppercase().rep())
    print('After lowercase:', sp.dup().lowercase().rep())
    print('After uppercase then capitalize:', sp.dup().uppercase().capitalize().rep())
    print('After delspace:', sp.dup().delspace().rep())

def main():
    print("Demo of method chaining in Python:")
    # Use extra spaces between words to show effect of delspace.
    process_string('hOWz  It     GoInG?')
    process_string('The      QUIck   brOWn         fOx')

main()