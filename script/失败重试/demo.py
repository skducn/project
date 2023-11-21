# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: 失败重试机制 retrying
# 51testing.com/html/22/n-7798622.html
# *****************************************************************

from retrying import retry


# @retry(stop_max_attempt_number=2)
# def func():
#     """
#     重试函数，最多尝试两次。
#     """
#     for item in range(0, 100):
#         print(item)
#         """
#         对于每个循环变量item，在0到100之间进行循环。
#         """
#         result = item / 0
#         print(result)
#
#         return result
# func()

import time

# # 每隔三秒执行一次
# @retry(wait_fixed=3000)
# def func():
#     print(f"记录失败重试:",time.strftime("%Y-%m-%d %H:%M:%S"))
#     result=1 / 0
#     print(result)
#     return result
# func()

# 每隔1-9秒执行一次
# @retry(wait_random_min=1000,wait_random_max=9000)


# 每个两秒执行一次，在第五次失败后，发邮件，然后继续执行
@retry(wait_random_min=2000, wait_random_max=2000)
def sendEmail(attempt_number, delay_since_first_attempt_ms):
    if attempt_number == 5:
        print("发邮件")
    return 2000


@retry(wait_func=sendEmail)
def func():
    print(f"记录失败重试:", time.strftime("%Y-%m-%d %H:%M:%S"))
    result = 1 / 0
    print(result)
    return result


func()





