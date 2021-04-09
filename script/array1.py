# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-19
# Description: 数组 array可以存放放一组相同类型的数字
# 数据array 与列表list 有什么区别?
# array 是数组, 数组只能保存一种类型的数, 在它初始化的时候就决定了数据是什么类型的值，而list 几乎可以放任何对象,如数字、字典、对象、列表、字符串等。
# array 可以紧凑地定义一个基本的数组：字符，整数，浮点数。
# 数组与列表都是序列类型，支持所有跟可变序列有关的操作,包括 pop,insert和extend
# 关于效率，当只对1000万个浮点数进行操作时，数组的效率要比列表要高得多，因为数组在内存中存的不是对象，而是字节。
# 关于效率，如果业务只对数字进行操作，那么数组比列表更高效。
# 如需要频繁对序列做先出先进的操作，collection.deque(双端队列)的速度应该会更快。
# 数组支持从文件读取和写入的方法，如.frombytes和.tofile。
# 创建数组需要一个类型码，这个类型码用来表示在底层的C语言应该存放怎样的数据类型。比如b类型码代表的是有符号的字符（signedchar），array(‘b’)创建出的数组就只能存放一个字节大小的整数，范围从-128到127，这样在序列很大的时候，我们能节省很多空间。
# 参考：https://blog.csdn.net/xc_zhou/article/details/88538793

# array类型码
'''
Type code      C Type     Minimum size in bytes   python Type
     'b'    signed integer           1                int
     'B'    unsigned integer         1                int
     'u'    Unicode character        2                Unicode character
     'h'    signed integer           2                int
     'H'    unsigned integer         2                int
     'i'    signed integer           2                int
     'I'    unsigned integer         2                int
     'l'    signed integer           4                int
     'L'    unsigned integer         4                int
     'q'    signed integer           8                int
     'Q'    unsigned integer         8                int
     'f'    floating point           4                float
     'd'    floating point           8                float
'''



# array 提供的方法如下
# append() -- append a new item to the end of the array
# buffer_info() -- return information giving the current memory info
# byteswap() -- byteswap all the items of the array
# count() -- return number of occurrences of an object
# extend() -- extend array by appending multiple elements from an iterable
# fromfile() -- read items from a file object
# fromlist() -- append items from the list
# frombytes() -- append items from the string
# index() -- return index of first occurrence of an object
# insert() -- insert a new item into the array at a provided position
# pop() -- remove and return item (default last)
# remove() -- remove first occurrence of an object
# reverse() -- reverse the order of the items in the array
# tofile() -- write all items to a file object
# tolist() -- return the array converted to an ordinary list
# tobytes() -- return the array converted to a string
# ********************************************************************************************************************

from array import array
import random


print(array.typecode)  # <attribute 'typecode' of 'array.array' objects>

# 构造方法如下
# array.array(typecode[, initializer])

# 构造一个空的int类型数组
arr = array('i')

arr = array('i', [0, 1, 2, 3, 4, 6, 7, 8, 9, 100])
print(arr.typecode)  # i  //类型代码的字符串
print(arr.itemsize)  # 4  //一个数组项的字节长度。