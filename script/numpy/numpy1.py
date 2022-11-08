# # coding: utf-8
# # *****************************************************************
# # Author     : John
# # Date       : 2020-3-19
# # Description: numpy (Numerical Python) 多维数组对象
# # NumPy 是一个运行速度非常快的数学库，主要用于数组计算
# # ndarray = N-dimensional array 多维度数组
# # 广播功能函数、整合 C/C++/Fortran 代码的工具、线性代数、傅里叶变换、随机数生成等功能
# # NumPy 通常与 SciPy（Scientific Python）和 Matplotlib（绘图库）一起使用， 这种组合广泛用于替代 MatLab，是一个强大的科学计算环境，有助于我们通过 Python 学习数据科学或者机器学习。
# # SciPy 是一个开源的 Python 算法库和数学工具包。
# # SciPy 包含的模块有最优化、线性代数、积分、插值、特殊函数、快速傅里叶变换、信号处理和图像处理、常微分方程求解和其他科学与工程中常用的计算。
# # Matplotlib 是 Python 编程语言及其数值数学扩展包 NumPy 的可视化操作界面。它为利用通用的图形用户界面工具包，如 Tkinter, wxPython, Qt 或 GTK+ 向应用程序嵌入式绘图提供了应用程序接口（API）。
# # NumPy 官网 http://www.numpy.org/
# # NumPy 源代码：https://github.com/numpy/numpy
# # SciPy 官网：https://www.scipy.org/
# # SciPy 源代码：https://github.com/scipy/scipy
# # Matplotlib 官网：https://matplotlib.org/
# # Matplotlib 源代码：https://github.com/matplotlib/matplotlib
# # *****************************************************************
# # https://blog.csdn.net/weixin_40040404/article/details/80776678
# # https://www.cnblogs.com/q735613050/p/9130312.html
# # http://www.voidcn.com/article/p-cylcldlk-btm.html
# # https://zhuanlan.zhihu.com/p/99889912
# # http://www.uml.org.cn/python/201811131.asp  多维数组
# # *****************************************************************
#
# '''
# 1.1 数据源是list时，array和asarray一样，复制一个副本，占用新的内存。
# 1.2 数据源是numpy.ndarray时，array()复制一个副本，占用新的内存，而 asarray() 沿用原数据源内存地址。
# 1.3 asarray() 转换数据类型（float32或int32）
# 1.4 asarray() 判断元素，符合条件更新为1，否则为0"
#
# 2, array() 将数据转为数组
#
# 3.1, arange() 生成序列数组(默认int32)
# 3.2, arange().reshape 生成序列多维数组
#
# 4，np.ones() 返回一个全1的n维数组及运算后的值
#
# 5，维度与维数
#
# 6，N 数组矩阵列相加与行相加
#
# 7，数组统计（平均数、合计、平铺）
# '''
#
import numpy as np
import pandas as pd
#

# #
# #

# #
# #


# #
# #
# print("5，维度与维数".center(100, "-"))
# M = np.array(((np.arange(3)), (np.arange(3))))
# print(M)  # [[0, 1, 2],[0, 1, 2]]
# print(M.shape)  # (2, 3)
# print(M.ndim)  # 2    //二维
#
#
# print("6，N 数组矩阵列相加与行相加".center(100, "-"))
# a = [0, 1, 2]
# b = [2, 1, 3]
# c = [5, 5, 1]
# x = np.array([a, b, c])
# arr_a = np.sum(x, axis=0)  # 列相加
# arr_b = np.sum(x, axis=1)  # 行相加
# print(arr_a)  # [7 7 8]
# print(arr_b)  # [3 6 11]
#
#
# print("7，数组统计（平均数、合计、平铺）".center(100, "-"))
# x = np.array([1, 2, 3])
# print(x.mean())   # 2.0  //平均数
# print(x.sum())   # 6  //合计
# print(np.tile(x, 1))  # [1,2,3]  //不变
# print(np.tile(x, 2))   # [1,2,3,1,2,3]   //维度不变，值扩大2倍
# print(np.tile(x, 4))   # [1 2 3 1 2 3 1 2 3 1 2 3]  //维度不变，值扩大4倍
# print(np.tile(x, (1, 2)))   # [1,2,3,1,2,3]  //维度不变，值扩大2倍
# print(np.tile(x, (2, 2)))   # [1,2,3,1,2,3],[1,2,3,1,2,3]  //维度扩大2倍，值扩大2倍
# print(np.tile(x, (2, 1)))   # [1,2,3],[1,2,3]  //维度扩大2倍，值不变



print("8，随机生成N行M列的二维数组".center(100, "-"))
arr = np.random.rand(4, 4)
# [[0.50398151 0.49137049 0.57337883 0.8637965 ]
#  [0.45352152 0.02176194 0.09520183 0.86945503]
#  [0.56745522 0.65480827 0.02221036 0.90495728]
#  [0.70681986 0.19456123 0.5346386  0.95599382]]
print(arr)

print("9，三维数组（面、直线、点）".center(100, "-"))
x = np.arange(27)
x = np.reshape(x, (3, 3, 3))
print('第1个水平面', x[0])
print('第2个水平面', x[1])
print('第3个水平面', x[2])
print('第1个面的第一个直线 ', x[0][0])
print('第1个面的第二个直线', x[0][1])
print('第1个面的第三个直线', x[0][2])
print("第1个面的第一条直线的第一个点", x[0][0][0])
print("第1个面的第一条直线的第二个点", x[0][0][1])
print("第1个面的第一条直线的第三个点", x[0][0][2])



print("10，empty()并不能保证返回所有是0的数组，某些情况下，会返回为初始化的垃圾数值".center(100, "-"))
print(np.empty(5))  # [5.e-324 5.e-324 5.e-324 5.e-324 5.e-324]


print("11.1，astype()类型转换".center(100, "-"))
a = np.array([1, 2, 3, 432323123123, 5])
print(a.dtype)  # int64
print(a.astype(np.float64))  # [1.00000000e+00 2.00000000e+00 3.00000000e+00 4.32323123e+11 5.00000000e+00]
a = a.astype(np.float64)
print(a.dtype)  # float64


print("11.2，astype() 如果是把float变为int，小数点后的部分会被丢弃".center(100, "-"))
arr = np.array([3.7, -1.2, -2.6, 0.5, 12.9, 10.1])
print(arr.astype(np.int32))  # [ 3 -1 -2  0 12 10]


print("11.3，astype() 把string里的数字变为实际的数字".center(100, "-"))
# numpy.string_类型，这种类型的长度是固定的，所以可能会直接截取部分输入而不给警告。
numeric_strings = np.array(['1.25', '-9.6', '42'], dtype=np.string_)
print(numeric_strings)  # [b'1.25' b'-9.6' b'42']
print(numeric_strings.dtype)  # |S4
print(numeric_strings.astype(float))  # [ 1.25 -9.6  42.  ]


print("11.4，astype() 用其他数组的dtype直接来制定类型".center(100, "-"))
i = np.arange(10)
calibers = np.array([.22, .270, .357, .380, .44, .50], dtype=np.float64)
print(i.astype(calibers.dtype))  # [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]


print("11.5，用类型的缩写，比如u4就代表unit32".center(100, "-"))
empty_unit32 = np.ones(2, dtype='u4')
print(empty_unit32)  # [1 1]

# astype总是会返回一个新的数组。



print("12，数组和标量之间的运算".center(100, "-"))
# 数组可对数据执行批量运算，叫矢量化。
# 大小相等的数组之间的任何算术运算都会将运算应用到元素级
arr = np.array([[1., 2., 3.], [4., 5., 6.]])
print(arr * arr)
# [[ 1.  4.  9.]
#  [16. 25. 36.]]
print(arr + arr)
# [[ 2.  4.  6.]
#  [ 8. 10. 12.]]
print(arr - arr)
# [[0. 0. 0.]
 # [0. 0. 0.]]
# 数组与标量的算术运算也会将那个标量值传播到各个元素
print(1/arr)
# [[1.         0.5        0.33333333]
#  [0.25       0.2        0.16666667]]
# 不同大小的数组之间的运算叫做广播（broadcasting）


print("12，数组的索引和切片".center(100, "-"))
# 当将一个标量值赋给一个切片时（如arr[5:8]=12），该值会自动传播（“广播”）到整个选区。
# 和Python列表不同的是，数组切片是原始数组的视图，数据不会被复制，任何修改都会反应到源数组上。
arr = np.arange(10)
print(arr[5])
print(arr[5:8])  #[5 6 7]
arr[5:8] = 12
print(arr)  # [ 0  1  2  3  4 12 12 12  8  9]
arr_slice = arr[5:8]
arr_slice[1] = 12345
print(arr)  # [    0     1     2     3     4    12 12345    12     8     9]
arr_slice[:] = 64
print(arr)  # [ 0  1  2  3  4 64 64 64  8  9]

# 若想得到ndarray切片的一份副本，就需要显式地进行复制操作，例如arr[5:8].copy()
x = arr[5:8].copy()
x[1] = 100
print(x)  # [ 64 100  64]
print(arr)  # [ 0  1  2  3  4 64 64 64  8  9]

# 对比一下列表，列表不能修改源值
list1 = [0,1,2,3,4,5,6,7,8,9]
print(list1[5])  # 5
print(list1[5:8])  # [5, 6, 7]
# list1[5:8] = 12  # 报错，列表不能修改源值


# 在一个二维数组中，各索引位置上的元素不再是标量而是一维数组
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]
print(arr2d[2])  # [7 8 9]
# 有两种方式可以访问单一元素
print(arr2d[2][1])  # 8
print(arr2d[2, 1])  # 8

# 二维数组的索引方式
# 对于多维数组，如果省略后面的索引，返回的将是一个低纬度的多维数组。例如，一个2 x 2 x 3数组
arr3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
print(arr3d)

print(arr3d[0])
# [[1 2 3]
#  [4 5 6]]
old_values = arr3d[0].copy()
arr3d[0] = 42
print(arr3d)
# [[[42 42 42]
#   [42 42 42]]
#
#  [[ 7  8  9]
#   [10 11 12]]]
arr3d[0] = old_values
print(arr3d)
# [[[ 1  2  3]
#   [ 4  5  6]]
#
#  [[ 7  8  9]
#   [10 11 12]]]

print(arr3d[1, 0])  # [7 8 9]



print("13，数组的索引和切片2".center(100, "-"))
# 高维对象可以在一个或多个轴上进行切片，也可以跟整数索引混合使用
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d[:2])
# [[1 2 3]
#  [4 5 6]]

# 可以一次传入多个切片，就像传入多个索引那样
print(arr2d[:2, 1:])
# [[2 3]
#  [5 6]]

# 只有冒号表示选取整个轴
print(arr2d[:, :1])
# [[1]
#  [4]
#  [7]]

# 对切片表达式的赋值操作也会扩散到整个选区
arr2d[:2, 1:] = 0
print(arr2d)
# [[1 0 0]
#  [4 0 0]
#  [7 8 9]]


print("14，布尔型索引".center(100, "-"))
# 假设我们有一个用于存储数据的数组以及一个存储姓名的数组（含有重复项）
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
print(names)
data = np.random.randn(7, 4)
print(data)
# [[-2.34855984  0.60140943  0.88565013  0.30843226]
#  [-0.52308663 -1.12606964 -2.12439878 -0.02875487]
#  [ 0.88405453  0.68538785 -0.36494087  0.50133198]
#  [ 0.50277154 -0.45819724 -0.071283   -1.29432949]
#  [-0.35414704 -2.00963552 -1.42991937 -1.02512503]
#  [ 0.69890024  0.08899635 -0.4599453  -0.18272094]
#  [ 0.29821388 -0.44016851  0.60537766  0.64073442]]
# 假设每个名字对应data数组中的一行，我们想要选出对应于名字'Bob'的所有行。
# 和算术运算一样，数组的比较运算（如==）也是矢量化的。因此，对names和字符串“Bob”的比较运算会产生一个布尔型数组
print(names == 'Bob')  # [ True False False  True False False False]
print(data[names == 'Bob'])
# [[-2.34855984  0.60140943  0.88565013  0.30843226]
#  [ 0.50277154 -0.45819724 -0.071283   -1.29432949]]

# 布尔型数组的长度必须跟被索引的轴长度一致。还可以将布尔型数组跟切片、整数（或整数序列）混合使用
print(data[names == 'Bob', 2:])
# [[0.88565013  0.30843226]
#  [-0.071283   -1.29432949]]
print(data[names == 'Bob', 3])  # [0.30843226 -1.29432949]

# 选中除了'Bob'外的所有行，可以用!=或者~
print(names != 'Bob')  # [False  True  True False  True  True  True]
print(data[~(names == 'Bob')])
# [[-0.52308663 -1.12606964 -2.12439878 -0.02875487]
#  [ 0.88405453  0.68538785 -0.36494087  0.50133198]
#  [-0.35414704 -2.00963552 -1.42991937 -1.02512503]
#  [ 0.69890024  0.08899635 -0.4599453  -0.18272094]
#  [ 0.29821388 -0.44016851  0.60537766  0.64073442]]

# 选取两个需要组合应用多个布尔条件，如&（与）、|（或）之类的布尔运算符。
mask = (names == 'Bob') | (names == 'Will')
print(mask)  # [ True False  True  True  True False False]
print(data[mask])

# 通过布尔型索引选取数组中的数据，总是创建数据的副本，即使返回一摸一样的数组也是如此。
# 通过布尔型数组设置值是一种常用手段，为了将data中的所有负值设置为0，只需：
data[data<0] = 0
print(data)
# [[0.         1.56369405 1.11394279 0.        ]
#  [0.         0.         1.28624161 0.        ]
#  [0.38986112 0.57910395 0.         0.        ]
#  [0.         0.45989738 0.         0.        ]
#  [0.08456205 0.         0.         0.67110231]
#  [1.02876436 0.49500124 1.92055802 0.        ]
#  [1.47424771 1.53172034 1.62923524 0.        ]]

# 通过一维布尔数组设置整行或列的值也很简单
data[names != 'Joe'] = 7
print(data)
# [[7.         7.         7.         7.        ]
#  [0.11025506 0.         0.02535764 0.68250182]
#  [7.         7.         7.         7.        ]
#  [7.         7.         7.         7.        ]
#  [7.         7.         7.         7.        ]
#  [0.         0.02585592 0.         0.19849679]
#  [0.         0.         0.         1.02212549]]


print("15，花式索引是一个NumPy术语，它指的是利用整数数组进行索引。".center(100, "-"))
# 花式索引跟切片不同，总是将数据复制到新数组中。
arr = np.empty((8, 4))
for i in range(8):
    arr[i] = i
print(arr)
# [[0. 0. 0. 0.]
#  [1. 1. 1. 1.]
#  [2. 2. 2. 2.]
#  [3. 3. 3. 3.]
#  [4. 4. 4. 4.]
#  [5. 5. 5. 5.]
#  [6. 6. 6. 6.]
#  [7. 7. 7. 7.]]

# 为了以特定顺序选取子集，只需传入一个指定顺序的整数列表或ndarray即可
print(arr[[4, 3, 0, 6]])
# [[4. 4. 4. 4.]
#  [3. 3. 3. 3.]
#  [0. 0. 0. 0.]
#  [6. 6. 6. 6.]]

# 使用负数索引将从末尾开始选行
print(arr[[-3, -5, -7]])
# [[5. 5. 5. 5.]
#  [3. 3. 3. 3.]
#  [1. 1. 1. 1.]]

# 一次传入多个索引数组会有一点特别。其返回的是一个一维数组（如：[1, 5, 7, 2]），其中的元素对应各个索引元组（如：[0, 3, 1, 2]）
arr = np.arange(32).reshape((8, 4))
print(arr)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]
#  [12 13 14 15]
#  [16 17 18 19]
#  [20 21 22 23]
#  [24 25 26 27]
#  [28 29 30 31]]
print(arr[[1, 5, 7, 2], [0, 3, 1, 2]])  # [ 4 23 29 10]  //不论数组有多少维，花式索引的结果总是一维。

# 选取矩阵的行列子集,任意排列
# 将每一行元素，按照[0, 3, 1, 2]顺序配列
print(arr[[1, 5, 7, 2]][:, [0, 3, 1, 2]])
# [[ 4  7  5  6]
#  [20 23 21 22]
#  [28 31 29 30]
#  [ 8 11  9 10]]
# 分析：先从arr中选出[1, 5, 7, 2]这四行，然后[:, [0, 3, 1, 2]]表示选中所有行，但是列的顺序要按0,3,1,2来排。


print("16，数组转置和轴对换".center(100, "-"))
# 转置是重塑的一种特殊形式，其返回源数据的视图（不会进行任何复制操作）。有两种方式，一是transpose方法，二是T属性。
arr = np.arange(15).reshape((3, 5))
print(arr)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]]
print(arr.T)
# [[ 0  5 10]
#  [ 1  6 11]
#  [ 2  7 12]
#  [ 3  8 13]
#  [ 4  9 14]]


# arr = np.random.randn(6,3)
# print(arr)
# print(np.dot(arr.T,arr))

# 对于高维数组，transpose需要得到一个由轴编号组成的元组才能对这些轴进行转置（比较费查克拉）
# 分析：https://blog.csdn.net/weixin_42229626/article/details/81700977
# 原理：一级元素2个（arr[0], arr[1]），二级元素4个(arr[0][0],arr[0][1],arr[1][0],arr[1][1])，三级元素16个(arr[0][0][0],arr[0][0][1]...)。
# 也就是说 每个最基层的元素都可以用 3个数字来表达..用一个元祖来表现就是 (X,Y,Z)
# 对每一个基层元素的元祖表达式,即:(X,Y,Z)进行转置.
# 转置方式为:(0,1,2) >>> (1,0,2)
# 也就是每一个元素都是 (X,Y,Z) >>> (Y,X,Z)
arr = np.arange(16).reshape((2, 2, 4))
print(arr)
# [[[ 0  1  2  3]
#   [ 4  5  6  7]]
#
#  [[ 8  9 10 11]
#   [12 13 14 15]]]
print(arr.transpose((1, 0, 2)))
# [[[ 0  1  2  3]
#   [ 8  9 10 11]]
#
#  [[ 4  5  6  7]
#   [12 13 14 15]]]
print(arr.transpose((0, 2, 1)))
# [[[ 0  4]
#   [ 1  5]
#   [ 2  6]
#   [ 3  7]]
#
#  [[ 8 12]
#   [ 9 13]
#   [10 14]
#   [11 15]]]
print(arr.transpose((2, 1, 0)))
# [[[ 0  8]
#   [ 4 12]]
#
#  [[ 1  9]
#   [ 5 13]]
#
#  [[ 2 10]
#   [ 6 14]]
#
#  [[ 3 11]
#   [ 7 15]]]
print(arr.transpose((2, 0, 1)))
# [[[ 0  4]
#   [ 8 12]]
#
#  [[ 1  5]
#   [ 9 13]]
#
#  [[ 2  6]
#   [10 14]]
#
#  [[ 3  7]
#   [11 15]]]


print("17, swapaxes方法，需要接受一对轴编号".center(100, "-"))
# swapaxes也是返回数据的视图（不会进行任何复制操作）。
print(arr.swapaxes(1, 2))  # 等同于 print(arr.transpose((0, 2, 1)))
# [[[ 0  4]
#   [ 1  5]
#   [ 2  6]
#   [ 3  7]]
#
#  [[ 8 12]
#   [ 9 13]
#   [10 14]
#   [11 15]]]
print(arr)


print("18, ones_like(数组)".center(100, "-"))
arr = np.arange(6)  # array([0, 1, 2, 3, 4, 5])
print(np.ones_like(arr))  # array([1, 1, 1, 1, 1, 1])


print("19, reshape() 将ndarray转化为N*M*...的多维ndarray（非copy）".center(100, "-"))
# 通过reshape生成的新数组和原始数组公用一个内存，也就是说，假如更改一个数组的元素，另一个数组也将发生改变

arr = np.arange(8, dtype=np.float64) # [0. 1. 2. 3. 4. 5. 6. 7.]
r = arr.reshape((2,4))
print(r)
# [[0. 1. 2. 3.]
#  [4. 5. 6. 7.]]
arr[1] = 100  # 修改源数组值
print(r)
# [[  0. 100.   2.   3.]
#  [  4.   5.   6.   7.]]

print("20, eye() 生成对角线的矩阵(返回对角线的为1其余为0的二维的数组)".center(100, "-"))
# N:int型，表示的是输出的行数
# M：int型，可选项，输出的列数，如果没有就默认为N
# k：int型，可选项，对角线的下标，默认为0表示的是主对角线，负数表示的是低对角，正数表示的是高对角。
# dtype：数据的类型，可选项，返回的数据的数据类型
a = np.eye(4,2)
print(a)
# [[1. 0.]
#  [0. 1.]
#  [0. 0.]
#  [0. 0.]]

# 如果 N=M 就相当于 np.identity() 创建方阵，也就是N=M
a = np.eye(4)
print(a)
# [[1. 0. 0. 0.]
# #  [0. 1. 0. 0.]
# #  [0. 0. 1. 0.]
# #  [0. 0. 0. 1.]]

# 参数k，int类型可选项，对角线的下标，默认为0表示的是主对角线，负数表示的是低对角，正数表示的是高对角。
b = np.eye(4, k=1)
print(b)
# [[0. 1. 0. 0.]
#  [0. 0. 1. 0.]
#  [0. 0. 0. 1.]
#  [0. 0. 0. 0.]]

b = np.eye(4, k=-1)
print(b)
# [[0. 0. 0. 0.]
#  [1. 0. 0. 0.]
#  [0. 1. 0. 0.]
#  [0. 0. 1. 0.]]


# print("21, 利用numpy 生成one_hot 数组".center(100, "-"))
# # one_hot数组
# test_labels=[1,2,3,4,5,6,7]
# print(test_labels)
# adata = np.array(test_labels)
# print(adata)
# def make_one_hot(data1):
#     return (np.arange(8) == data1[:,None]).astype(np.integer)
#
# my_one_hot = make_one_hot(adata)
# print(my_one_hot)
# # [[0 1 0 0 0 0 0 0]
# #  [0 0 1 0 0 0 0 0]
# #  [0 0 0 1 0 0 0 0]
# #  [0 0 0 0 1 0 0 0]
# #  [0 0 0 0 0 1 0 0]
# #  [0 0 0 0 0 0 1 0]
# #  [0 0 0 0 0 0 0 1]]


print("23, 生成对角线的矩阵方阵".center(100, "-"))
# np.identity(n,dtype=None)
# 参数：n，int型表示的是输出的矩阵的行数和列数都是n
# dtype：表示的是输出的类型，默认是float
print(np.identity(3))
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]


print("24， full() , 创建一个由常数填充的数组,第一个参数是数组的形状，第二个参数是数组中填充的常数".center(100, "-"))
print(np.full((3,2), 5))
# [[5 5]
#  [5 5]
#  [5 5]]



print("25， empty() 创建任意空数组； ramdon() 创建随机数组".center(100, "-"))
# 用法：numpy.empty(shape, dtype=float, order='C')
# 返回：给定shape，dtype 和 order的任意空数组，shape 为整型数据或整型tuple
print(np.empty([3, 2]))
# [[1.         0.5       ]
#  [0.33333333 0.25      ]
#  [0.2        0.16666667]]
print(np.empty([3, 2], dtype=int))
# [[5 5]
#  [5 5]
#  [5 5]]

print(np.random.random((3,2)))
# [[0.69811308 0.20604495]
#  [0.00798681 0.94517262]
#  [0.63325742 0.21761745]]


print("26， linspace()创建等差数列。".center(100, "-"))
# numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
# 产生从start到stop的等差数列，num为元素个数，默认50个
# 多用于模型训练,如：从0到50，生成5个等值
a = np.linspace(0, 50, 5)
print(a)  # [ 0.  12.5 25.  37.5 50. ]

a = np.linspace(0, 50, 5, endpoint=False)  # 不包含 stop
print(a)  # [ 0. 10. 20. 30. 40.]

a = np.linspace(0, 50, 5, endpoint=False,  retstep=True)
print(a)  # (array([ 0., 10., 20., 30., 40.]), 10.0)
print(a[0])  # [ 0. 10. 20. 30. 40.]
print(a[1])  # 10.0  //输出等差间隔数

# import matplotlib.pyplot as plt
# N = 8
# y = np.zeros(N)
# x1 = np.linspace(0, 10, N, endpoint=True)
# x2 = np.linspace(0, 10, N, endpoint=False)
# plt.plot(x1, y, 'o')
# plt.plot(x2, y + 0.5, 'o')
# plt.ylim([-0.5, 1])
# plt.show()


print("27， np.where(condition, x, y) 满足条件(condition)，输出x，不满足输出y".center(100, "-"))
aa = np.arange(10)
print(np.where(aa, 5, -1))  # [-1  5  5  5  5  5  5  5  5  5]   //# 0为False，所以第一个输出-1
print(np.where(aa > 5, 2, -1))  # [-1 -1 -1 -1 -1 -1  2  2  2  2]
print(np.where([[True, False], [True, True]],
               [[1, 2], [3, 4]],
               [[9, 8], [7, 6]]))
# [[1 8]
#  [3 4]]
# 分析：True取 [[1, 2], [3, 4]] ； False取[[9, 8], [7, 6]]
# 分析：[True, False] 从[1, 2][9, 8]中判断，得到[1, 8]；[True, True] 从[3, 4][7, 6]中判断，得到[3, 4]；

a = 10
b = np.where([[a > 5,a < 5], [a == 7, a == 10]],
             [["a1", "apple"], ["b1", "bananan"]],
             [["c1", "cherry"], ["d1", "Damson"]])
print(b)
# [['a1' 'cherry']
#  ['d1' 'bananan']]
# 分析：True取 [["a1", "apple"], ["b1", "bananan"]] ； False取[["c1", "cherry"], ["d1", "Damson"]]
# 分析：[a > 5,a < 5]得到[a1, cherry]；[a == 7, a == 10]得到[d1.banana]；


print("28，np.where(condition) 没有x和y，则输出满足条件 (即非0) 元素的坐标".center(100, "-"))
# 等价于numpy.nonzero, 这里的坐标以tuple的形式给出，通常原数组有多少维，输出的tuple中就包含几个数组，分别对应符合条件元素的各维坐标。
a = np.array([12, 14, 16, 18, 110])
print(np.where(a > 15))  # (array([2, 3, 4], dtype=int64),)   //返回索引
print(a[a > 15])  # [ 16  18 110]  //返回值
print(np.where([[0, 0, 10], [31, 0, 0]]))  # (array([0, 1], dtype=int64), array([2, 0], dtype=int64))
# 分析：
# [[0, 0, 10]    //一维是0
# [31, 0, 0]]    //一维是1
# 先一维坐标，再二维以此类推
# [0, 0, 10] 一维度的非0有效值坐标是2 即
# 0
# 2
# [31, 0, 0]一维度的非0有效值坐标是0 即
# 1
# 0
# 竖列排列在一起：
# 0 1
# 2 0
# 横向组成列表即 [0,1][2,0]

print(np.where([[0, 0, 10, 11], [31, 0, 0, 0]]))  # (array([0, 0, 1], dtype=int64), array([2, 3, 0], dtype=int64))
print(np.where([1, 11, 21, 0]))  # (array([0, 1, 2], dtype=int64),)
print(np.where([[111211, 0], [21, 0]]))  # (array([0, 1], dtype=int64), array([0, 0], dtype=int64))
print(np.where([[1,2,3,0,5], [7,0,0,4,4]]))  # (array([0, 0, 0, 0, 1, 1, 1], dtype=int64), array([0, 1, 2, 4, 0, 3, 4], dtype=int64))
x = np.where([[1,2,3,0,5], [7,0,0,4,4]])
print(x[0])
print(x[1])
print(x[1][2])
print(np.where([[1, 0, 3], [0, 4, 7], [9, 7, 0]]))  # (array([0, 0, 1, 1, 2, 2], dtype=int64), array([0, 2, 1, 2, 0, 1], dtype=int64))
print(np.where([[[1, 0, 3], [0, 4, 7]]]))  # (array([0, 0, 0, 0], dtype=int64), array([0, 0, 1, 1], dtype=int64), array([0, 2, 1, 2], dtype=int64))
print(np.where([[[1, 0, 3], [0, 4, 7], [9, 7, 0]]]))  # (array([0, 0, 0, 0, 0, 0], dtype=int64), array([0, 0, 1, 1, 2, 2], dtype=int64), array([0, 2, 1, 2, 0, 1], dtype=int64))


print("29，np.ogrid() 整数步长".center(100, "-"))
# 1、arange函数产生的是一维数组，而ogrid函数产生的是二维数组
# 2、arange函数产生的是一个数组，而ogrid函数产生的是二个数组
# 3、ogrid函数产生的数组，第一个数组是以纵向产生的，即数组第二维的大小始终为1。第二个数组是以横向产生的，即数组第一维的大小始终为1。

x,y = np.ogrid[:3, :4]
print(x)
# [[0]
#  [1]
#  [2]]
print(np.shape(x))  # (3, 1)
print(y)
# [[0 1 2 3]]
print(np.shape(y))  # (1, 4)

# 第一个数组的步长为1，第二数组的步长为2
x,y = np.ogrid[0:10:1,0:10:2]
print(x,np.shape(x))
print(y,np.shape(y))
# [[0]
#  [1]
#  [2]
#  [3]
#  [4]
#  [5]
#  [6]
#  [7]
#  [8]
#  [9]] (10, 1)
# [[0 2 4 6 8]] (1, 5)


print("29，np.ogrid() 复数步长的设置是通过j进行设置的，复数用几个数值来等分整个区间。 ".center(100, "-"))
x,y = np.ogrid[0:10:6j,0:10:5j]
print(x,np.shape(x))
print(y,np.shape(y))
# [[ 0.]
#  [ 2.]
#  [ 4.]
#  [ 6.]
#  [ 8.]
#  [10.]] (6, 1)
# [[ 0.   2.5  5.   7.5 10. ]] (1, 5)
# 分析：[0:10:6j]，的意思是将[0,10]这个区间等分为5(6-1)个区间，也就是说会产生6个端点位置。


print("29，np.ogrid() ".center(100, "-"))
print(np.ogrid[0:10:2])  # [0 2 4 6 8]
print(np.ogrid[0:10:2j])  # [ 0. 10.]


print("30，np.mgrid[ 第1维，第2维 ，第3维 ， …]  返回多维结构，常见的如2D图形，3D图形".center(100, "-"))
x,y = np.mgrid[0:10:6j,0:10:5j]
print(x)
print(y)
# [[ 0.  0.  0.  0.  0.]
#  [ 2.  2.  2.  2.  2.]
#  [ 4.  4.  4.  4.  4.]
#  [ 6.  6.  6.  6.  6.]
#  [ 8.  8.  8.  8.  8.]
#  [10. 10. 10. 10. 10.]]
# [[ 0.   2.5  5.   7.5 10. ]
#  [ 0.   2.5  5.   7.5 10. ]
#  [ 0.   2.5  5.   7.5 10. ]
#  [ 0.   2.5  5.   7.5 10. ]
#  [ 0.   2.5  5.   7.5 10. ]
#  [ 0.   2.5  5.   7.5 10. ]]

x = np.mgrid[0:10:2]
print(x)


print("31，np.nan 在ndarray中显示时 np.nan会显示nan，如果进行计算 结果会显示为NAN".center(100, "-"))
array = np.array([[1, np.nan, 3], [4, 5, np.nan]])
print(array)
# [[ 1. nan  3.]
#  [ 4.  5. nan]]

print("31.2，pd.isna() 判断缺省值是nan，返回布尔值".center(100, "-"))
print(pd.isna(array))
# [[False  True False]
#  [False False  True]]

print("31.3，pd.notna() 判断缺省值不是nan，返回布尔值".center(100, "-"))
print(pd.notna(array))
# [[ True False  True]
#  [ True  True False]]

print("31.4，np.isnan() 遍历将nan替换成一个默认值".center(100, "-"))
array[np.isnan(array)] = 100
print(array)
# [[  1. 100.   3.]
#  [  4.   5. 100.]]


print("31.5 缺省值判断,NA值如None或np.nan, NaT将映射True值。''或np.inf不被视为NA值".center(100, "-"))
print(pd.isna(None))  # True
print(pd.isna(np.nan))  # True
# 索引，返回一个布尔值的ndarray
index = pd.DatetimeIndex(["2019-12-12", "2021-05-12", None])
print(index)  # DatetimeIndex(['2019-12-12', '2021-05-12', 'NaT'], dtype='datetime64[ns]', freq=None)
print(pd.isna(index))  # [False False  True]

s= pd.Series([1, 2,np.nan,np.inf,''])
print(s)
df = pd.DataFrame([s.tolist()],columns=list('ABCDE'))
print(df)
print(s.isna().tolist())  # [False, False, True, False, False]
print(df.isna().values.tolist())  # [[False, False, True, False, False]]


print(np.nan != np.nan)  # True
