# coding: utf-8
#****************************************************************
# Author     : John
# Version    : 1.0.0
# Date       : 2019-1-16
# Description: 文件操作 common/io/io1.py
#****************************************************************

# write(str) 数据的写入（覆盖原内容）
fo = open("test.txt","w")
fo.write ('This is a test.\nReally, it is.')
fo.close()

# # writelines(seq) 数据的写入(覆盖原内容)
# # writelines() 既可以传入字符串又可以传入一个字符序列
# fo = open("test1.txt","w+")
# fo.writelines(["China", "France", "America"])  # 字符序列列表
# fo.writelines("aaa bbb ccc")  # 字符串
# fo.close()

# 数据的追加
fo = open("test.txt","a")
fo.write ('\nBottom line.')
fo.close()

# 数据的读取，read()、readlines()、readline()
# read() 每次读取整个文件，一般将文件内容放到一个字符串变量中。但对于连续的面向行的处理，它却是不必要的，并且如果文件大于可用内存，则不可能实现这种处理。
# readlines() 每次读取整个文件，象read() 一样，它自动将文件内容分析成一个行的列表，该列表可以由for ... in ... 结构进行处理。
# readline() 每次只读取一行，通常比readlines() 慢得多。仅当没有足够内存可以一次读取整个文件时，才应该使用。
# seek(offset)	改变当前文件操作指针的位置，offset含义如下:0 – 文件开头； 1 – 当前位置； 2 – 文件结尾
fo = open ('test.txt')
print(fo.read())  # 读完后光标留在末尾
# 将光标移到开始处
fo.seek(0)
print(fo.read(4))  # 读取4个长度单位是byte ， 结果：This
fo.seek(0)
print(fo.readline())  # This is a test.\n
print(fo.readline(6))  # Really
fo.seek(0)
print(fo.readlines())  # ['This is a test.\n', 'Really, it is.\n', 'Bottom line.']
fo.seek(0)
for fileLine in fo.readlines():
    print('>>', fileLine)  # 注意每次读取一行后最后还有\r\n
fo.seek(0)
print(fo.read(4))  # This
# tell 输出当前光标位置
print(fo.tell())  # 4
print(fo.readline())  # " is a test."
fo.close()

print("~~~~~~~~~~~~")
#****************************************************************


# 二进制方式读与写
# https://www.cnblogs.com/dpf-learn/p/8028121.html
# 在Windows和Macintosh环境下，有时可能需要以二进制方式读写文件，比如图片和可执行文件。
fileHandle = open ('testBinary.txt', 'wb')
s = 'There is no spoon.'
# 将 str 转化为 bytes , 因为b 是二进制文件，不能保存str类型。
fileHandle.write (s.encode(encoding="utf-8"))
fileHandle.close()
fileHandle = open ( 'testBinary.txt', 'rb' )
print(fileHandle.read())  # b'There is no spoon.'
fileHandle.close()

# python 没有二进制类型，通过struct模块将string字符串类型来存储二进制数据，string是以1个字节为单位的。
# 实例：将一个整数转换成二进制
import struct
a = 12
bytes = struct.pack('i',a)  # 转换后bytes就是一个字符串，字符串按字节同a的二进制存储内容相同。
print(bytes)  # b'\x0c\x00\x00\x00'
print(type(bytes))  # <class 'bytes'>

# 实例：将二进制转换成python数据类型
# 注意，unpack返回的是tuple
a, = struct.unpack('i',bytes)  # 只有一个变量的话 ，或 (a,)=struct.unpack('i',bytes)
print(a)  # 12

# 实例：将多个数据类型转换成二进制，并写入二进制文件
a = 'hello'
b = 'world!'
c = 2
d = 45.123
bytes = struct.pack('@5s6sif', a.encode('utf-8'), b.encode('utf-8'), c, d)
print(bytes)  # b'helloworld!\x00\x02\x00\x00\x00\xf4}4B'
# 此时的bytes就是二进制形式的数据了，可以直接写入文件比如binfile.write(bytes)
fileHandle = open ('testBinary123.txt', 'wb')
fileHandle.write (bytes)
fileHandle.close()

# 计算给定的格式(fmt)占用多少字节的内存
print(struct.calcsize('@5s6sif'))  # 20个字节

fileHandle = open ('testBinary123.txt', 'rb')
print(fileHandle.read())  # b'helloworld!\x00\x02\x00\x00\x00\xf4}4B'
x = struct.unpack('5s6sif', bytes)  # unpack解析出来的tuple
print(x)  # (b'hello', b'world!', 2, 45.12300109863281)
fileHandle.close()

# '5s6sif' 这个叫做fmt格式化字符串，由数字加字符构成
# 5s表示占5个字符的字符串，i表示1个整数，f表示1个浮点数。

#****************************************************************

# fp.read([size]) #size为读取的长度，以byte为单位
# fp.readline([size]) #读一行，如果定义了size，有可能返回的只是一行的一部分
# fp.readlines([size]) #把文件每一行作为一个list的一个成员，并返回这个list。其实它的内部是通过循环调用readline()来实现的。如果提供size参数，size是表示读取内容的总长，也就是说可能只读到文件的一部分。
# fp.write(str) #把str写到文件中，write()并不会在str后加上一个换行符
# fp.writelines(seq) #把seq的内容全部写到文件中(多行一次性写入)。这个函数也只是忠实地写入，不会在每行后面加上任何东西。
# fp.close() #关闭文件。python会在一个文件不用后自动关闭文件，不过这一功能没有保证，最好还是养成自己关闭的习惯。 如果一个文件在关闭后还对其进行操作会产生ValueError
# fp.flush() #把缓冲区的内容写入硬盘
# fp.fileno() #返回一个长整型的”文件标签“
# fp.isatty() #文件是否是一个终端设备文件（unix系统中的）
# fp.tell() #返回文件操作标记的当前位置，以文件的开头为原点
# fp.next() #返回下一行，并将文件操作标记位移到下一行。把一个file用于for … in file这样的语句时，就是调用next()函数来实现遍历的。
# fp.seek(offset[,whence]) #将文件打操作标记移到offset的位置。这个offset一般是相对于文件的开头来计算的，一般为正数。但如果提供了whence参数就不一定了，whence可以为0表示从头开始计算，1表示以当前位置为原点计算。2表示以文件末尾为原点进行计算。需要注意，如果文件以a或a+的模式打开，每次进行写操作时，文件操作标记会自动返回到文件末尾。
# fp.truncate([size]) #把文件裁成规定的大小，默认的是裁到当前文件操作标记的位置。如果size比文件的大小还要大，依据系统的不同可能是不改变文件，也可能是用0把文件补到相应的大小，也可能是以一些随机的内容加上去。


# pickle可以存储什么类型的数据呢？
# 所有python支持的原生类型：布尔值，整数，浮点数，复数，字符串，字节，None。
# 由任何原生类型组成的列表，元组，字典和集合。
# 函数，类，类的实例
# pickle 模块 存储的更复杂的数据都是对象，必须使用二进制形式写进文件。
# pickle之 dump 和 load
import pickle
testList = [ 123, { 'Calories' : 190 }, 'Mr. Anderson', [ 1, 2, 7 ] ]  # 存储列表数据到文件
with open ( 'pickleFile.txt', 'wb' ) as fo:
    pickle.dump ( testList, fo )
fo.close()
with open ( 'pickleFile.txt', 'rb' ) as fo:
    x = pickle.load(fo)
print(x)  # [123, {'Calories': 190}, 'Mr. Anderson', [1, 2, 7]]
fo.close()

# pickle之 dumps 和 loads
# dumps 将python对象序列化保存到一个字符串变量中
# loads 从字符串变量中载入python对象
list1 = ['aa', 'bb', 'cc']
list1_str = pickle.dumps(list1)
print(list1_str)  # b'\x80\x03]q\x00(X\x02\x00\x00\x00aaq\x01X\x02\x00\x00\x00bbq\x02X\x02\x00\x00\x00ccq\x03e.'
list2 = pickle.loads(list1_str)
print(list2) # ['aa', 'bb', 'cc']

