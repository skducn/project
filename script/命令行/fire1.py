# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-19
# Description: fire命令行接口模块
# ********************************************************************************************************************

import fire

# 命令行执行：python -m fire fire1.py greet jinhao 或 python -m fire fire1.py greet --name='jinhao'
def greet(name):
    print(f'hello {name}')
# hello jinhao


def add(x,y):
    return x+ y

# 命令行执行：python fire1.py multiply 4 5
class Cal():
    def multiply(self,x,y):
        return x*y
# 20

if __name__ == '__main__':
    # fire.Fire(add)
    fire.Fire(Cal)