# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2022-10-12
# Description: # 定时任务的利器apscheduler
# http://www.51testing.com/html/77/n-7793377.html
# pip3.9 install apscheduler
# apscheduler有四个主要模块，分别是：触发器triggers、任务存储器job_stores、执行器executors、调度器schedulers。
# 触发器指的是任务指定的触发方式，可以选择cron、date、interval中的一个。
# cron表示的是定时任务，类似linux crontab，在指定的时间触发。如：每天7点20分执行一次：task.add_job(func=sch_test, args=('定时任务',), trigger='cron',hour='7', minute='20')
# date表示具体到某个时间的一次性任务
# interval表示的是循环任务，指定一个间隔时间，每过间隔时间执行一次。如：每隔3秒执行一次sch_test任务 　task.add_job(func=sch_test, args=('循环任务',), trigger='interval', seconds=3)。

# 任务存储器是存储任务的地方，有四种存储方式，默认存储在内存中。
# MemoryJobStore 任务存储内存中；
# SQLAlchemyJobStore 使用sqlalchemy存储在数据库；
# MongoDBJobStore存储在mongodb中；
# RedisJobStore 存储在redis中
# 通常默认存储在内存即可，但若程序故障重启的话，会重新拉取任务运行了。

# 执行器的功能就是将任务放到线程池或进程池中运行，有6种执行器类型，默认是线程池执行器。
# ThreadPoolExecutor 线程池执行器;
# ProcessPoolExecutor 进程池执行器; (应用是CPU密集型操作）
# GeventExecutor Gevent程序执行器;
# TornadoExecutor Tornado程序执行器;
# TwistedExecutor Twisted程序执行器;
# AsynclOExector asyncio程序执行器

# 调度器属于apscheduler的核心，它扮演着统筹整个apscheduler系统的角色，存储器、执行器、触发器在它的调度下正常运行。有6种调度器，常用的是BlockingScheduler调度器
# BlockingScheduler 当调度器是应用种唯一要运行的，start开启后会阻塞 (常用)
# BackgroundScheduler 适用于调度程序在应用程序的后台运行，start开启后不会阻塞
# AsyncIOScheduler 当程序使用了asyncio的异步框架是使用。
# GeventScheduler  当程序用了Tordnado的时候用
# TwistedScheduler 当程序用了Twisted的时候用
# QtScheduler 当程序用了QT的时候用

# 异常监听
# 定时任务在运行时，若出现错误，需要设置监听机制，我们通常结合logging模块记录错误信息
# *****************************************************************

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_EXECUTED , EVENT_JOB_ERROR
import logging
import logging.handlers
import os
import datetime
class LoggerUtils():
    def init_logger(self, logger_name):
        # logging.basicConfig(level=logging.INFO,
        #     format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        #     datefmt = '%Y-%m-%d %H:%M:%S',
        #     filename = '{}{}.log'.format('./data/logs/', logger_name)
        # # # filename = 'sche.log',
        #   )

        # 日志格式
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        log_obj = logging.getLogger(logger_name)
        log_obj.setLevel(logging.INFO)
        # 设置log存储位置

        path = './data/logs/'
        filename = '{}{}.log'.format(path, logger_name)
        if not os.path.exists(path):
            os.makedirs(path)
        # 设置日志按照时间分割
        timeHandler = logging.handlers.TimedRotatingFileHandler(
           filename,
           when='D',  # 按照什么维度切割， S:秒，M：分，H:小时，D:天，W:周
           interval=1, # 多少天切割一次
           backupCount=10  # 保留几天
        )
        timeHandler.setLevel(logging.INFO)
        timeHandler.setFormatter(formatter)
        log_obj.addHandler(timeHandler)
        return log_obj


class Scheduler(LoggerUtils):
    def __init__(self):
        # 执行器设置
        executors = {
            'default': ThreadPoolExecutor(10),  # 设置一个名为“default”的ThreadPoolExecutor，其worker值为10
            'processpool': ProcessPoolExecutor(5)  # 设置一个名为“processpool”的ProcessPoolExecutor，其worker值为5
        }
        self.scheduler = BlockingScheduler(timezone="Asia/Shanghai", executors=executors)
        # 存储器设置
        # # 这里使用sqlalchemy存储器,将任务存储在mysql
        # sql_url = 'mysql+pymysql://root:root@localhost:3306/db?charset=utf8'
        # self.scheduler.add_jobstore('sqlalchemy',url=sql_url)
        # self.scheduler.add_jobstore('MemoryJobStore')
        def log_listen(event):
            if event.exception:
                # 日志记录
                # print('任务出错，报错信息：{}'.format(event.exception))
                self.scheduler._logger.error(event.traceback)

        # 配置任务执行完成及错误时的监听
        self.scheduler.add_listener(log_listen, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        # 配置日志监听
        self.scheduler._logger = self.init_logger('sche_test')
    def add_job(self, *args, **kwargs):
        """添加任务"""
        self.scheduler.add_job(*args, **kwargs)
    def start(self):
        """开启任务"""
        self.scheduler.start()


# 测试任务
def sch_test(job_type):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('时间：{}, {}测试apscheduler'.format(now, job_type))
    print(1/0)

sched = Scheduler()
sched.add_job(func=sch_test, args=('定时任务',), trigger='cron', second='*/5')
sched.start()











