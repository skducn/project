# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2021/9/16
# Description: pytest 失败case重复执行
# pip3 install -U pytest
# pip3 install -U pytest-rerunfailures   //pytest-rerunfailures（失败case重复执行）
# 接口测试时，有时会遇到503或短时的网络异常，导致case运行失败，而这并非是我们期望的结果，此时就可以通过重试运行cases的方式来解决。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# NUM：重试次数。
# pytest test_se.py --reruns NUM


