# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-5-20
# Description: collections模块 之 ChainMap 合并字典
# 官网：https://docs.python.org/3.8/library/collections.html
# ********************************************************************************************************************
'''
ChainMap将多个字典或其他映射组合在一起以创建单个可更新视图
原理：ChainMap 不会真的把字典合并在一起，而是在内部储存一个Key到每个字典的映射，当你读取 e[key] 的时候，它先去查询这个key在哪个字典里面，然后再去对应的字典里面查询对应的值。所以使用ChainMap几乎不需要额外的内存空间
1，ChainMap提供了一种多个字典整合的方式，它没有去合并这些字典，而是将这些字典放在一个 maps (一个列表)里，内部实现了很多 dict 的方法，大部分 dict 的方法，ChainMap 都能使用。
2，ChainMap在获取一个key的值时，会遍历 maps ，一旦在其中一个字典里找到了这个 key ，便停止寻找。
3，ChainMap更新原字典key，当设置 ChainMap 的某个key时，只能在第一个字典里寻找这个key，找到则更新，没找到则设置。删除某个key时，也是一样，只会在第一个dict中寻找这个key，如果没有找到会报错 KeyError
4, ChainMap类用于快速链接多个映射，以便将它们视为一个单元。它通常比创建新字典和多次调用update()快得多。
5, 该类可用于模拟嵌套作用域，在模板中很有用。
6，ChainMap 可以把多个字典合并成一个 ChainMap 对象。读写这个对象就像是读字典一样
'''

from collections import ChainMap

d1 = {'a': 1, 'b': 2 }
d2 = {'c': 3, 'd': 4 }
d3 = {'b': 4, 'c': 5 }
d4 = {'d': 6, 'e': 6 }
c = ChainMap(d1,d2,d3,d4)
print(c['b'])  # 2
print(c['c'])  # 3
print(c['e'])  # 6
c['b'] = 55
c['g'] = 22
print(d1)   # 只在第一个字典中更新，修改了 z:5
print(d2)   # 只在第一个字典中更新，添加了 g:2
print(d3)   # 只在第一个字典中更新，添加了 g:2
print(d4)   # 只在第一个字典中更新，添加了 g:2
del c['b']
print(d1)   # 只在第一个字典中更新，修改了 z:5
print(d2)   # 只在第一个字典中更新，添加了 g:2
print(d3)   # 只在第一个字典中更新，添加了 g:2
print(d4)   # 只在第一个字典中更新，添加了 g:2
print(c)

dict4 = {}
for k,v in c.items():
    print(k,v)
    dict4[k] = v

print(dict4)

#
# merged = dict(b)
# merged.update(a)
# print(merged)  # {'y': 2, 'z': 5, 'x': 1, 'g': 2}
# print(a)
# print(b)
# a['x']=100
# print(merged['x'])  # 1



baseline = {'music': 'bach', 'art': 'rembrandt'}
adjustments = {'art': 'van gogh', 'opera': 'carmen'}
print(ChainMap(adjustments, baseline))
print(list(ChainMap(adjustments, baseline)))

print("____________")

def collection_test3():
    import builtins
    from collections import ChainMap
    a = {"name": "leng","age": 20}
    b = {"age": 24}
    c = {"wife": "qian"}
    cm = ChainMap(a,b,c)
    nc1 = cm.new_child()
    nc2 = cm.new_child(m=b)
    print(nc1,sep='\n')  # ChainMap({}, {'name': 'leng', 'age': 20}, {'age': 24}, {'wife': 'qian'})
    print(nc2, sep='\n')  # ChainMap({'age': 24}, {'name': 'leng', 'age': 20}, {'age': 24}, {'wife': 'qian'})
    print("_________")
    print(nc2.parents,nc1.parents,sep='\n')

collection_test3()

user_dict1 = {"a": "111", "b": "222"}
user_dict2 = {"b": "333", "d": "444"}
new_dict = ChainMap(user_dict1, user_dict2)

for key, value in new_dict.items():
    print(key, value)

