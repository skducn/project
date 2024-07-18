# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2017-10-26
# Description   : 日期时间 实例
# pendulum https://www.cnblogs.com/goldsunshine/p/15292216.html
# *********************************************************************

from PO.TimePO import *
Time_PO = TimePO()
import pendulum


# todo 获取年、月、日、日期、时间、星期
# print(Time_PO.getYear())  # 2020
# print(Time_PO.getMonth())  # 03
# print(Time_PO.getDay())  # 19
# print(Time_PO.getYearMonth())  # 202003
# print(Time_PO.getMonthDay())  # 0319
# print(Time_PO.getDate())  # 20200319
# print(Time_PO.getDateByMinus())  # 2020-03-19
# print(Time_PO.getDateByDivide())  # 2020/03/19
# print(Time_PO.getDateTime())  # 20200319151928
# print(Time_PO.getDateTimeByDivide())  # 2020/03/19 15:19:28
print(time.strftime("%H:%M:%S"))  # 15:19:28
print(time.strftime("%Y-%m-%d %H:%M:%S.000"))  # 15:19:28
# print(Time_PO.getWeek())  # 星期一
# print(Time_PO.getWeekByEng("", "%A"))  # Monthday
# print(Time_PO.getWeekByEng("", "%a"))  # Mon
# print(Time_PO.getWeek("2019-12-15"))  # 星期日
# print(Time_PO.getWeekByEng("2019-12-15", "%A"))  # Sunday
# print(Time_PO.getWeekByEng("2019-12-15", "%a"))  # Sun

# todo 计算日期、时间
# print(Time_PO.getDateByMinusPeriod(2))  # 2022-12-01  //2天后日期
# print(Time_PO.getDateByMinusPeriod(-3))  # 2022-11-26  //3天前日期
# print(Time_PO.getDateTimeByPeriod(0))  # 2020-03-19 15:19:28   //当前日期时间
# print(Time_PO.getDateTimeByPeriod(0.5))  # 2020-03-19 15:49:28  //当前日期时间晚30分钟
# print(Time_PO.getDateTimeByPeriod(-1))  # 2020-03-19 14:19:28   //当前日期时间早1小时
# print(Time_PO.getNow())  # 2022-11-29 12:48:23.907028  //当前日期时间
# print(Time_PO.getNowByPeriod(0.5))  # 2022-11-29 13:19:37.939408  //比当前日期时间晚30分钟
# print(Time_PO.getNowByPeriod(-1))  # 2022-11-29 11:49:37.939408  //比当前日期时间早1小时
# print(time.strftime("%H:%M:%S"))  # 15:19:28   //当前时间
# print(Time_PO.getTimeByPeriod(0.5))  # 15:49:28  //当前时间晚30分钟
# print(Time_PO.getDateByFirstDay(2019, 7))  # 2019-07-01  //获取某年月的第一天
# print(Time_PO.getDateByLastDay(2019, 7))  # 2019-07-31   //获取某年月的最后一天
# print(Time_PO.getDateByPeriodDate("2019-12-15", -1))   # 2019-12-14   //获取指定日期的前一天
# print(Time_PO.getDateByPeriodDate("2019-12-15", 2))   # 2019-12-17  //获取指定日期的后2天

# todo 区间时间差
# print("求时间差，输出天时分秒".center(100, "-"))
# date_start = pd.to_datetime(datetime.datetime.now())  # Timestamp('2021-05-19 08:06:08.683355')
# sleep(6)  # ----这里是程序执行部分----
# date_end = pd.to_datetime(datetime.datetime.now())  # Timestamp('2021-05-19 08:06:08.683355')
# print(date_end - date_start)  # 0 days 00:00:06.010230
# print("求时间差，输出秒".center(100, "-"))
# time_start = time.time()
# sleep(6)  # ----这里是程序执行部分----
# time_end = time.time()
# time = time_end - time_start
# print('耗时：%s 秒' % time)  # 耗时：6.008593320846558 秒


# # todo 统计月份天数
# print(Time_PO.getDayByYearMonth(2019, 2))  # 28   //统计2019年2月的天数
#
# # todo 格式化月份
# print(Time_PO.addZeroByPrefix(9))  # 09    //自动在 1 - 9 前加上0
#
# # todo 格式转换
# print(Time_PO.now2timestamp())  # 1584603355.0  //当前日期时间转时间戳
# print(Time_PO.datetime2timestamp(Time_PO.getDateTimeByPeriod(0)))  # 1584603355   //日期时间转时间戳
# print(Time_PO.timestamp2datetime(Time_PO.now2timestamp()))  # 2020-03-19 15:35:55  //时间戳转日期时间
# print(Time_PO.sec2hms1(60))  # 输出1分钟
# print(Time_PO.sec2hms2(170))  # 输出2分50

# todo 日期比较
# （日期1晚于日期2，返回True或False）
# print(Time_PO.isDate1GTdate2("2020-1-1", "2020-1-5"))
# print(Time_PO.isDate1GTdate2("2020-4-1", "2020-1-5"))

# todo 时区处理
# # 获取当前时区信息
# current_timezone = pendulum.now().timezone_name
# print(current_timezone)  # Asia/Shanghai
#
# sh = pendulum.now('Asia/Shanghai')  # 上海时间
# print(sh)
#
# print(sh.in_tz('US/Pacific'))  # # 转换时区 ,太平洋时间
# print(sh.in_tz('US/Eastern'))  # # 转换时区, 美国东部时间
# print(sh.in_tz('JP'))  # # 转换时区, 美国东部时间



# ======================================================================================================================
#     以下不可用有待测试

# print(Time_PO.getDateByMonthLastDay(-1))   # 2020-02-29  //获取上月的最后一天。（不支持跨年，如2020-01-01的上个月会报错）
# print(Time_PO.getDateByMonthLastDay(1))  # 2020-02-29  //获取下月的最后一天。（不支持跨年，如2020-12-12 的下个月会报错）
# print(Time_PO.getDateByMonthToday(-1))  # 2020-02-19   //返回上个月的今天
# print(Time_PO.getDateByMonthToday(3))  # 2020-06-19   //返回3个月后的今天
# print(Time_PO.getDateByTuple(1))  # ('2020', '04', '30')    //列表形式返回下个月及最后一天

# cal函数(UserWarning: Support years 2018-2021 currently, need update every year.)
# # 获取2020年法定节假日
# print(cal.holidays(2020))
#
# # 判断某天是否工作日（周一到周五返回True，周六日回False）
# print(cal.is_working_day(date(2020, 12, 18)))
#
# # 获取连续多个月工作日天数（不包括双休日与节假日）
# print(cal.get_working_days_delta(date(2020, 11, 1), date(2020, 12, 31)))
#
# # 获取每月工作日天数（不包括双休日与节假日）
# print(Time_PO.get_weekday("2024-7"))

