# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
# Description: string - 常见的字符串操作
''' ODO 官网文档：https://docs.python.org/zh-cn/3.8/library/string.html '''
# *****************************************************************

string = "567abcDEF123"

# 格式示例，str.format() 语法的示例以及与旧式 % 格式化的比较
# todo: 按位置访问参数:
print('{0}, {1}, {2}'.format('a', 'b', 'c'))  # a, b, c
print('{}, {}, {}'.format('a', 'b', 'c'))  # a, b, c
print('{2}, {1}, {0}'.format('a', 'b', 'c'))  # c, b, a
# unpacking argument sequence
print('{2}, {1}, {0}'.format(*'a2bc'))  # b, 2, a
print('{2}, {1}, {0}'.format(*string))  # 7,6,5
print('{0}{1}{0}'.format('123', 'cad'))  # 123cad123

# todo:按名称访问参数:
print('Coordinates: {latitude}, {longitude}'.format(latitude='37.24N', longitude='-115.81W'))
coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
print('Coordinates: {latitude}, {longitude}'.format(**coord))  # 字典

# todo:访问参数的属性:
c = 3-5j
print(('The complex number {0} is formed from the real part {0.real} and the imaginary part {0.imag}.').format(c))
# 'The complex number (3-5j) is formed from the real part 3.0 and the imaginary part -5.0.'
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __str__(self):
        return 'Point({self.x}, {self.y})'.format(self=self)
print(Point(4, 2)) # 'Point(4, 2)'

# todo:访问参数的项:
coord = (3, 5)
print('X: {0[0]};  Y: {0[1]}'.format(coord))  # X: 3;  Y: 5
print('X: {0[0]};  Y: {1[1]}'.format(coord, [33, 44]))  # X: 3;  Y: 44

# todo:替代 %s 和 %r:

# %r 它会将后面给的参数原样打印出来。
print("repr() shows quotes: {!r}; str() doesn't: {!s}".format('test1', 'test2'))  # "repr() shows quotes: 'test1'; str() doesn't: test2"








