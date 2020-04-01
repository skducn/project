# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-19
# Description: 数组 array
# 当需要1000万个浮点数的时候，数组（array）的效率要比列表（list）要高得多，因为数组在背后存的并不是float对象，而是数字的机器翻译，也就是字节表述。
# 频繁对序列做先出先进的操作，collection.deque(双端队列)的速度应该会更快。
# 数组支持所有跟可变序列有关的操作,包括.pop,.insert和.extend。
# 数组提供从文件读取和存入文件的更快的方法，如.frombytes和.tofile。
# 创建数组需要一个类型码，这个类型码用来表示在底层的C语言应该存放怎样的数据类型。比如b类型码代表的是有符号的字符（signedchar），array(‘b’)创建出的数组就只能存放一个字节大小的整数，范围从-128到127，这样在序列很大的时候，我们能节省很多空间。
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