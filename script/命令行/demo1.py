# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-19
# Description: fire模块 用来自动生成命令行接口（CLI）
# ********************************************************************************************************************

import fire

def hello(name=None):
    if name:
        return 'Hello {0}!'.format(name)
    else:
        return 'Hello World!'


if __name__ == '__main__':
    fire.Fire(hello)

# (py308) localhost-2:命令行 linghuchong$ python demo1.py --name="jinhao"
# Hello jinhao!
# (py308) localhost-2:命令行 linghuchong$ python demo1.py
# Hello World!
