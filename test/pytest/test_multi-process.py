# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2021/9/16
# Description: pytest 多进程运行cases
# pip3 install -U pytest
# pip3 install -U pytest-xdist   //pytest-xdist（多CPU分发）
# 当cases量很多时，运行时间也会变的很长，如果想缩短脚本运行的时长，就可以用多进程来运行。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# NUM：并发的进程数
# pytest test_se.py -n NUM


