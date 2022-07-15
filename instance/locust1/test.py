# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-7-15
# Description: locust
# Locust 则使用 gevent 通过协程的方式模拟并发用户，资源的消耗非常之少.
# RPS 吞吐量
# rt 响应时间是指：系统对请求作出响应的时间（一次请求耗时）。
# 虚拟用户数（并发量）如何计算？计算公式：RPS模式下的虚拟用户数 = RPS x RT（秒）。
# RPS模式以吞吐量作为目标，例如1000 RPS表示一秒内发出1000个请求。在施压过程中，根据被压测接口的RT表现不同，施压引擎为了达到您指定的吞吐量，会自适应调整虚拟用户数（即并发量）。
# QPS峰值时间每秒请求数：( 总PV数 * 80% ) / ( 每天秒数 * 20% ) ；# 原理：每天80%的访问集中在20%的时间里，这20%时间叫做峰值时间。
# TPS：Transactions Per Second（每秒传输的事物处理个数），即服务器每秒处理的事务数。
# 一个事务是指一个客户机向服务器发送请求然后服务器做出反应的过程。客户机在发送请求时开始计时，收到服务器响应后结束计时，以此来计算使用的时间和完成的事务个数。

# 打开浏览器，访问 http://localhost:8089
# 指标参考：https://blog.csdn.net/qq_39416311/article/details/84892625
# 参考：http://www.51testing.com/html/69/n-4474769.html
#***************************************************************

from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    host = "http://test.valval.cool"
    wait_time = between(0, 0)

    @task
    def api1(self):
        self.client.get("/api1")

    @task
    def api2(self):
        self.client.post("/api2", data={'key': 'value'})