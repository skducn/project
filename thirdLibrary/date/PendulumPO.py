# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2023-2-13
# Description   : pendulum 第三方日期库
# *********************************************************************

"""
求时间差，输出天时分秒 pd.to_datetime(datetime.datetime.now())
求时间差，输出秒  time.time()
秒转时分秒1  sec2hms1()
秒转时分秒2  sec2hms2()
"""

import pendulum

class PendulumPO():

    def now(self):
        dt = pendulum.datetime(2022, 3, 28, 20, 10, 30)
        # print(dt.__class__)
        return dt

if __name__ == "__main__":

    Pendulum_PO = PendulumPO()

