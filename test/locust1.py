# coding: utf-8
# ****************************************************************
# Author     : John
# Date       : 2020-11-24
# Description: 性能测试框架
# ****************************************************************


# from locust import HttpUser, TaskSet, task
#
#
# # 定义用户行为
# class UserBehavior(TaskSet):
#
#     @task
#     def baidu_index(self):
#         self.client.get("/")
#
#
# class WebsiteUser(HttpUser):
#     task_set = UserBehavior
#     # tasks = [UserBehavior]
#     min_wait = 3000
#     max_wait = 6000

from locust import TaskSet, HttpUser, between, task


class TestLogin(TaskSet):

    def setup(self):
        print("开始...")

    def teardown(self):
        print("结束...")

    def _login(self):
        url = '/test_ehr_sys/2.0/app/login'
        body = {
            "username": "shuyang",
            "password": "07497ba923378ceada4a7f6428be9956"
        }
        r = self.client.post(url=url, data=body)
        print(r.text)
        assert "等1" in r.text

    def logout(self):
        print("退出系统")

    @task(1)
    def home(self):
        print("进入主页")

    @task(1)
    def systeminfo(self):
        print("进入系统管理")

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        print("启动")
        self._login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("停止")
        self.logout()


class WebsiteUser(HttpUser):
    task_set = TestLogin

    def setup(self):
        print('locust setup')

    def teardown(self):
        print('locust teardown')

    wait_time = between(5, 6)


if __name__ == '__main__':
    import os

    os.system('locust -f locust1.py --host=https://192.168.0.36:19090')