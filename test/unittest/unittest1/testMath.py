# coding: utf-8

import unittest,testReflection
import Math
from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf

# 这是一个单元测试
class testMath(unittest.TestCase):

    @parameterized.expand([
        ['整数相加','add',1,1,2],
        ['小鼠相加','add',1.1, 14.3, 2],
    ])
    def testAdd(self,name,key,x,y,z):
        print(name)
        line = [name,key,x,y,z]
        # res = testReflection.run(line)
        # if res == False:
        #     self.fail(name + '失败')
        self.assertEqual(testReflection.run(line),z)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern='testMath.py',top_level_dir=None)
    runner = bf(suite)
    runner.report(filename='test.html', description='数学的测试报告')