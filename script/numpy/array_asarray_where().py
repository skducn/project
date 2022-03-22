# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-21
# Description: 数组 np.array(), np.asarray(), 条件选取 where()
# 语法：numpy.array(object, dtype=None, *, copy=True, order='K', subok=False, ndmin=0, like=None)
# array()数据源类型列表int&float、元组int&float、字符串<U7、字典object
# 数据源是列表时，array和asarray一样，复制一个副本占用新的内存地址。如 # np.array([1,2,3]) = np.asarray([1,2,3])
# 数据源是ndarray时，array()复制一个副本占用新的内存地址，而 asarray() 引用原数据源的内存地址.
# asarray()数据类型（float32或int32）互转
# asarray()判断元素符合条件改为1，否则为0
# *****************************************************************

import numpy as np


print("1 array()数据源类型列表int&float、元组int&float、字符串<U7、字典object".center(100, "-"))
list1 = [1, 2, 3]  # 列表
print(np.array(list1))  # [1 2 3]
print(np.array(list1).dtype)  # int32

tuple1 = ((9, 10), (11.15, 12))  # 元组
print(np.array(tuple1)) # [[ 9.   10.  ][11.15 12.  ]]
print(np.array(tuple1).dtype)  # float64

str1 = "4,5,678"   # 字符串
print(np.array(str1))  # 4,5,678
print(np.array(str1).dtype)  # <U7

dict1 = {"a": 88, "b": 123}  # 字典
print(np.array(dict1))  # {'a': 88, 'b': 123}
print(np.array(dict1).dtype)  # object



print("2 array（）创建整数int32数组".center(100, "-"))
arr = np.array([1, 2, 3, 4, 5])
print(arr)  # [1 2 3 4 5]
print(arr.dtype)  # int32


print("3 array（）创建浮点型float64数组".center(100, "-"))
arr = np.array([1.1, 3., 3.14, 7.7])
print(arr)  # [1.1  3.   3.14 7.7 ]
print(arr.dtype)  # float64


print("4 array（）创建浮点型float32数组".center(100, "-"))
arr = np.array([1, 3, 5], dtype='float32')
print(arr)  # [1. 3. 5.]
print(arr.dtype)  # float32


print("5 array（）使用dtype创建多类型数据".center(100, "-"))
# 应用：通过dtype动态定义type1,type2两个数据类型，分别应用object对象对应的位置
arr = np.array([(1, 2), (3, 4), (5, 6)], dtype=[('type1', '<i4'), ('type2', 'f4')])
print(arr)  # [(1, 2.) (3, 4.) (5, 6.)]
print(arr['type1'])  # [1 3 5]   // <i4等于int32
print(arr['type2'])  # [2. 4. 6.]  // f4等于float32
print(arr[0])  # (1, 2.)


print("6 array（）使用ndmin创建二维数组".center(100, "-"))
# 应用：将一维列表转换成二维数组
arr = np.array([1, 2, 3], ndmin=2)   # 等同于 np.array([[1,2,3]])
print(arr)  # [[1 2 3]]


print("7 array（）创建一个嵌套列表结果的多维数组".center(100, "-"))
arr = np.array([[i, i * i] for i in [5, 6, 7]])
print(arr)
# [[ 5 25]
#  [ 6 36]
#  [ 7 49]]


print("8 数据源是ndarray时，asarray()引用原数据源内存地址".center(100, "-"))
x = np.zeros((2, 3))  # <class 'numpy.ndarray'>
arr = np.array(x)  # 复制副本
asarr = np.asarray(x)  # 引用源数据地址
x[0][0] = 1   # 修改原数据
print(x)
# [[1. 0. 0.]
#  [0. 0. 0.]]
print(arr)
# [[0. 0. 0.]
#  [0. 0. 0.]]
print(asarr)
# [[1. 0. 0.]
#  [0. 0. 0.]]


print("9 asarray()数据类型（float32或int32）互转".center(100, "-"))
l = [55, 66]
print(np.asarray(l))  # [55 66]
print(np.asarray(l).dtype)  # int32
f = np.asarray(l, "f")
print(f.dtype)  # float32
print(f)  # [55. 66.]
i = np.asarray(l, "i")
print(i.dtype)  # int32
print(i)  # [55 66]



print("10 asarray()判断元素符合条件改为1，否则为0".center(100, "-"))
data = np.asarray([[51, 2], [-3, 0]])
asarr = np.asarray(asarr > 0, "i")
print(asarr)
# [[1 1]
#  [0 0]]
asarr = np.asarray(data < -1, "i")
print(asarr)
# [[0 0]
#  [1 0]]
asarr = np.asarray(data > 0, "f")
print(asarr)
# [[1. 1.]
#  [0. 0.]]



print("11 矩阵乘积".center(100, "-"))
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(A.dot(B))  # 等同于 np.matmul(A,B)
# [[19 22]
#  [43 50]]
# 算法：[1*5+2*7 1*6+2*8][3*5+4*7 3*6+4*8]


print("12 点乘（元素相乘）".center(100, "-"))
print(A*B)  # 等同于 np.multiply(A, B)
# [[ 5 12]
#  [21 32]]
# 算法：[1*5 2*6][3*7 4*8]


print("13 条件选取 where(), 大于0.5的值不处理，其余值替换成0".center(100, "-"))
data = np.random.random([2, 3])
print(data)
# [[0.89637997 0.81094498 0.2752972 ]
#  [0.01304246 0.04711835 0.63449249]]
print(np.where(data > 0.5, data, 0))
# [[0.89637997 0.81094498 0.        ]
#  [0.         0.         0.63449249]]