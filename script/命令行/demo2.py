# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-19
# Description: fire模块 用来自动生成命令行接口（CLI）
# ********************************************************************************************************************

import fire

def greet(name='jinhao',age=15):
    print(f'hello {name},{age}')
# (py308) localhost-2:命令行 linghuchong$ python -m fire demo2.py greet jinhao
# hello jinhao
# (py308) localhost-2:命令行 linghuchong$ python -m fire demo2.py greet --name='333'
# hello 333
# (py308) localhost-2:命令行 linghuchong$ python -m fire demo2.py greet --name="yo" --age=33
# hello yo,33


def add(x,y):
    return x+ y
# (py308) localhost-2:命令行 linghuchong$ python -m fire demo2.py add 3 4
# 7

class Cal():
    def multiply(self,x,y):
        return x*y
# (py308) localhost-2:命令行 linghuchong$ python -m fire demo2.py Cal multiply 4 5
# 20


# if __name__ == '__main__':
#     # fire.Fire(add)
#     fire.Fire(Cal)