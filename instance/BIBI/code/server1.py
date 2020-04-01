# -*- coding: utf-8 -*-

# x= "12345678"
# print x[-4:]

for i in range(5,11):
    print i

class people:
    name=""
    age=0
    __weight =0
    def __init__(self,n,a,w):
        self.name=n
        self.age=a
        self.__weight=w

    def speak(self):
        print("%s is speaking: I am %d years old and weight is %d" %(self.name,self.age,self.__weight))

p = people('tom',10,30)
p.speak()

class student(people):
    grade = ''
    def __init__(self,n,a,w,g):
        #调用父类的构函
        people.__init__(self,n,a,w)
        self.grade = g
    #覆写父类的方法
    def speak(self):
        print("%s is speaking: I am %d years old, and I am in grade %d"%(self.name,self.age,self.grade))

s = student('ken',20,60,3)
s.speak()