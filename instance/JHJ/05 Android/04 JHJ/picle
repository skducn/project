import pickle
class Person:
    def __init__(self,n,a):
        self.name=n
        self.age=a
    def show(self):
        print self.name+"_"+str(self.age)
aa = Person("JGood", 2)
aa.show()
f=open('p.txt','w')
pickle.dump(aa,f,0)
f.close()
#del Person
f=open('p.txt','r')
bb=pickle.load(f)
f.close()
bb.show()