# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-7-2
# Description: schedule
# pip install schedule
# schedule模块就像一个日程表，让你的Python程序按计划运行。
# *****************************************************************

import schedule
from time import sleep


def job():
    print("定时任务执行啦！")

# 每天早上8点执行
schedule.every().day.at("12:18").do(job)


# 循环脚本，每天12：18执行一次
while True:
    schedule.run_pending()
    sleep(1)









