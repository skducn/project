# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2022-10-12
# Description: # 定时任务 APScheduler
# http://www.51testing.com/html/77/n-7793377.html
# http://www.51testing.com/html/29/n-7799029.html
# pip3.9 install apscheduler
# apscheduler有四个主要模块，分别是：触发器triggers、任务存储器job_stores、执行器executors、调度器schedulers。

# todo 触发器(trigger):
# 定义任务执行的时间表。可基于日期date、时间间隔interval、Cron表达式来定义触发器。可以选择date、interval、cron中的一个。
# date 表示具体任务，指定一个具体时间，在某个具体时间执行任务
# interval 表示循环任务，指定一个间隔时间，每间隔时间执行一次。如：每隔3秒执行一次sch_test任务 　task.add_job(func=sch_test, args=('循环任务',), trigger='interval', seconds=3)。
# cron 表示定时任务，在指定的时间触发，类似linux的crontab。如：每天7点20分执行一次：task.add_job(func=sch_test, args=('定时任务',), trigger='cron',hour='7', minute='20')

# todo 任务存储器（JobStore）：
# 定义存储任务的调度状态，任务可以持久化到数据库或内存中。
# 任务存储器是存储任务的地方，有四种存储方式，默认存储在内存中。
# MemoryJobStore 任务存储内存中；
# SQLAlchemyJobStore 使用sqlalchemy存储在数据库；
# MongoDBJobStore 存储在mongodb中；
# RedisJobStore 存储在redis中
# 通常默认存储在内存即可，但若程序故障重启的话，会重新拉取任务运行了。

# todo 执行器（Executor）：
# 执行已触发的作业。
# 执行器的功能就是将任务放到线程池或进程池中运行，有6种执行器类型，默认是线程池执行器。
# ThreadPoolExecutor 线程池执行器;
# ProcessPoolExecutor 进程池执行器; (应用是CPU密集型操作）
# GeventExecutor Gevent程序执行器;
# TornadoExecutor Tornado程序执行器;
# TwistedExecutor Twisted程序执行器;
# AsynclOExector asyncio程序执行器

# todo 调度器（Scheduler）：
# 负责根据指定的规则触发任务执行的组件。
# 调度器属于apscheduler的核心，它扮演着统筹整个apscheduler系统的角色，触发器、存储器、执行器均在它的调度下正常运行。
# 有6种调度器，常用的是BlockingScheduler调度器
# BlockingScheduler 当调度器是应用中唯一要运行的，start开启后会阻塞 (常用)
# BackgroundScheduler 适用于调度程序在应用程序的后台运行，start开启后不会阻塞
# AsyncIOScheduler 当程序使用了asyncio的异步框架是使用。
# GeventScheduler  当程序用了Tordnado的时候用
# TwistedScheduler 当程序用了Twisted的时候用
# QtScheduler 当程序用了QT的时候用

# 异常监听
# 定时任务在运行时，若出现错误，需要设置监听机制，我们通常结合logging模块记录错误信息
# *****************************************************************

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import datetime,sys


task = BlockingScheduler()
# task = BackgroundScheduler()


def sch_test(var1):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('时间：{}, 测试apscheduler'.format(now))
    # print(var1)


# # 1, 每隔5秒执行
# task.add_job(func=sch_test, trigger='cron', second='*/5')

# # 2, 每隔10秒执行,传递参数a给函数
# task.add_job(func=sch_test, args=('a'), trigger='cron', second='*/10')

# 3，每天7点20分执行
# task.add_job(func=sch_test, args=('定时任务',), trigger='cron',hour='7', minute='20')

# 4，时间到2022-10-9执行
# task.add_job(func=sch_test, trigger='date', run_date=datetime.datetime(2022,10, 12, 9, 26, 19))

# 5，当前时间后3秒执行
# task.add_job(func=sch_test,trigger='date', next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=3))

# 6，循环任务，每隔3秒执行一次
task.add_job(func=sch_test, args=('定时任务',), trigger='interval', seconds=3)

task.start()














