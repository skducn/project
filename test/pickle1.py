# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: pickle 序列和反序列化
# http://blog.csdn.net/imzoer/article/details/8637473
# python的pickle模块实现了基本的数据序列和反序列化。
# 通过pickle模块的序列化操作我们能够将程序中运行的对象信息保存到文件中去，永久存储。
# 通过pickle模块的反序列化操作，我们能够从文件中创建上一次程序保存的对象。
# ********************************************************************************************************************

# pickle.dump(obj, file[, protocol]) 序列化对象
# 将结果数据流写入到文件对象中。
# 参数protocol是序列化模式，默认值为0，表示以文本的形式序列化。protocol的值还可以是1或2，表示以二进制的形式序列化。
# pickle.load(file)  反序列化对象。
# 将文件中的数据解析为一个Python对象。
# 注意: 在load(file)的时候，要让python能够找到类的定义(如 Person类)，否则会报错

import pickle

class Person:
    def __init__(self, n, a):
        self.name = n
        self.age = a
    def show(self):
        print(self.name + "_" + str(self.age))

# aa = Person("JGood", 2)
# aa.show()  # JGood_2
# f = open('d:\\p.txt', 'wb')    # p.txt中保存内容是 ccopy_reg_reconstructorp0(c__main__Personp1c__builtin__objectp2Ntp3Rp4(dp5Vnamep6VJGoodp7sVagep8I2sb.
# pickle.dump(aa, f, 0)
# f.close()



f = open('d:\\a.txt', 'rb')
bb = pickle.load("")
f.close()
bb.show()  # JGood_2

