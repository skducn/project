# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: raise
# https://blog.csdn.net/nanhuaibeian/article/details/86730158buzuo
# ********************************************************************************************************************

# 一个能屏蔽“ZeroDivisionError”（除零错误）的计算器类

class MuffledCalculator:
    muffled = False
    def calc(self,expr):
        try:
            return eval(expr)
        except ZeroDivisionError:
            if self.muffled:
                print("Division by zero is illegal")
            else:
                raise


if __name__ == '__main__':
    calculate = MuffledCalculator()
    x = calculate.calc("10/2")
    print(x)  # 5.0
    calculate.muffled = True
    calculate.calc("10/0")  #  Division by zero is illegal