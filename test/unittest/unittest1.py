# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2017-10-25
# Description: unittest用法
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import random
import unittest
from time import sleep

class AAB(unittest.TestCase):

    # def setUp(self):
    #     print "11111"

    def test_a(self):

        print "111"

    def test_choice(self):

        print "333"

    def test_e(self):

        print "444"

    @unittest.skip(u"demonstrating skipping222")
    def test_b(self):
        print "222"

    @unittest.skipIf(1<3,u"not supported in this library version")
    def test_d(self):
        print "444"

    @unittest.skipUnless(True, u"requires Windows")
    def test_f(self):
        print "555"

    @unittest.expectedFailure
    def test_haha(self):
            print "666"


@unittest.skipIf(12 < 3, u"not supported in this library version")
class AAC(unittest.TestCase):
    def test_not_run(self):
        print "1234567890"


# if __name__ == '__main__':
#     unittest.main()

if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(AAB)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试




