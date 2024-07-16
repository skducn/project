# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2024-7-12
# Description   : pendulum
# https://www.cnblogs.com/goldsunshine/p/15292216.html
# *********************************************************************

import pendulum

print(pendulum.now())  # 2024-07-12 16:05:34.652028+08:00
print(pendulum.now('Asia/Shanghai'))  # 2024-07-12 16:06:49.326318+08:00
print(pendulum.now().in_timezone('Asia/Shanghai'))  # 2024-07-12 16:07:00.324546+08:00
print(pendulum.now().in_tz('Asia/Shanghai'))  # 2024-07-12 16:07:00.324546+08:00
print(pendulum.now().in_tz('US/Pacific'))  # 2024-07-12 01:07:30.564801-07:00

print(pendulum.today())  # 2024-07-12 00:00:00+08:00
print(pendulum.tomorrow())  # 2024-07-13 00:00:00+08:00
print(pendulum.yesterday())  # 2024-07-11 00:00:00+08:00

# 输出当前时刻的年月日时分秒毫秒
print(pendulum.now().year)  # 2024
print(pendulum.now().month)  # 7
print(pendulum.now().day)  # 12
print(pendulum.now().hour)  # 16
print(pendulum.now().minute)  # 12
print(pendulum.now().second)  # 53
print(pendulum.now().microsecond)  # 796828

print(pendulum.now().to_date_string())  # 2024-07-12
print(pendulum.now().to_datetime_string())  # 2024-07-12 16:14:16
print(pendulum.now().to_day_datetime_string())  # Fri, Jul 12, 2024 4:14 PM
print(pendulum.now().to_formatted_date_string())  # Jul 12, 2024
print(pendulum.now().to_iso8601_string())  # 2024-07-12T16:14:57.674016+08:00
print(pendulum.now().to_time_string())  # 16:15:07
print(pendulum.now().to_rfc2822_string())  # Fri, 12 Jul 2024 16:15:16 +0800

dt = pendulum.now()
# print(dt.timezone_name())
# print(pendulum.now().day_of_year())
# print(pendulum.now().week_of_month())
# print(pendulum.now().week_of_year())
# print(pendulum.now().days_in_month())


# # 获取当前时区信息
print(pendulum.now().timezone_name)  # Asia/Shanghai
sh = pendulum.now('Asia/Shanghai') # 上海时间
print(sh)  # 2024-07-12 16:20:00.525598+08:00
print(sh.in_tz('US/Pacific'))  # 2024-07-12 01:20:00.525598-07:00   //# 转换时区 ,太平洋时间
print(sh.in_tz('US/Eastern'))  # 2024-07-12 04:20:00.525598-04:00  //# 转换时区, 美国东部时间


print(dt.format('YYYY-MM-DD HH:mm:ss'))  # '2021-09-14 15:57:47'
print(dt.format('dddd Do [of] MMMM YYYY-MM-DD HH:mm:ss A'))  # Friday 12th of July 2024-07-12 16:25:02 PM
