# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-07-29
# Description: 重试机制
# http://www.51testing.com/html/86/n-4473086.html
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# # # 1, 无条件重试，重试之间无间隔
# from tenacity import retry
# @retry()
# def test_retry():
#     print("等待重试，重试无间隔执行...")
#     raise Exception
# test_retry()


# # 2,无条件重试，但是在重试之前要等待 2 秒
# from tenacity import retry, wait_fixed
# @retry(wait=wait_fixed(2))
# def test_retry():
#     print("等待重试...")
#     raise Exception
# test_retry()


# # 3,只重试 5 次，每次间隔2秒，最后执行回调函数
from tenacity import *
def return_last_value(retry_state):
    print("执行回调函数")
    return retry_state.outcome.result()  # 表示返回原函数的返回值
def is_false(value):
    return value is False
@retry(wait=wait_fixed(4),stop=stop_after_attempt(5),retry_error_callback=return_last_value,retry=retry_if_result(is_false))
def test_retry():
    print("等待重试中...")
    return False
test_retry()

