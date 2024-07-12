# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2022-10-12
# Description: # 定时任务 apscheduler
# http://www.51testing.com/html/77/n-7793377.html
# 与日志配置
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




def sch_test(job_type):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('时间：{}, {}测试apscheduler'.format(now, job_type))


sched = Scheduler()
sched.add_job(func=sch_test, args=(), trigger='cron', second='*/2')  # 每隔2s执行一次任务
sched.start()










