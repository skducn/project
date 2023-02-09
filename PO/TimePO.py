# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2017-10-26
# Description   : 日期时间
# *********************************************************************

"""
求时间差，输出天时分秒 pd.to_datetime(datetime.datetime.now())
求时间差，输出秒  time.time()
秒转时分秒1  sec2hms1()
秒转时分秒2  sec2hms2()
"""
from time import strftime, localtime, sleep
from datetime import date, datetime, timedelta
import calendar, datetime, time
from workalendar.asia import China

cal = China()

import pandas as pd


class TimePO:
    def __init__(self):
        self.year = strftime("%Y", localtime())
        self.mon = strftime("%m", localtime())
        self.day = strftime("%d", localtime())
        self.hour = strftime("%H", localtime())
        self.min = strftime("%M", localtime())
        self.sec = strftime("%S", localtime())

    def getDate(self):

        """获取当天日期（年月日），如 20190819"""
        return self.year + self.mon + self.day

    def getDateByMinus(self):

        """获取当天日期（年-月-日），如 2019-09-19"""
        return str(date.today())

    def getDateByDivide(self):

        """获取当天日期（年/月/日），如 2019/09/19"""
        return time.strftime("%Y/%m/%d", time.strptime(str(date.today()), "%Y-%m-%d"))

    def getDateTime(self):

        """获取当天日期时间（年月日时分秒），如 20190919163619"""
        return self.year + self.mon + self.day + self.hour + self.min + self.sec

    def getDateTimeByMinus(self):

        """获取当天日期时间（年-月-日 时：分：秒），如 2019-09-19 16:36:19"""
        return strftime("%Y-%m-%d %H:%M:%S", localtime())

    def getDateTimeByDivide(self):

        """获取当天日期时间（年/月/日 时：分：秒），如 2019/09/19 16:36:19"""
        return time.strftime(
            "%Y/%m/%d %H:%M:%S",
            time.strptime(
                strftime("%Y-%m-%d %H:%M:%S", localtime()), "%Y-%m-%d %H:%M:%S"
            ),
        )

    def getDateTimeByPeriod(self, n):

        """获取指定日期时间的前后时间
        如：getDateTimeByPeriod（0）   //当前时间 2020/03/19 15:19:28
        如：getDateTimeByPeriod（0.5）  //晚30分钟  2020-03-19 15:49:28
        如：getDateTimeByPeriod（-1）  //早1小时  2020-03-19 14:19:28
        """
        return (datetime.datetime.now() + datetime.timedelta(hours=n)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def getNow(self):

        """获取当前日期（年月日时分秒后及后6位数），如 2017-09-15 09:41:27.336765"""
        return datetime.datetime.now()

    def getNowByPeriod(self, n):

        """获取指定日期的前后时间
        如：getNowByPeriod（0）   //当前时间 2020/03/19 15:19:28.470652
        如：getNowByPeriod（0.5）  //晚30分钟  2020/03/19 15:49:28.470652
        如：getNowByPeriod（-1）  //早1小时  2020/03/19 14:19:28.470652
        """
        return datetime.datetime.now() + datetime.timedelta(hours=n)

    def getYear(self):

        """获取当前年份，如 2019"""
        return datetime.datetime.now().strftime("%Y")

    def getMonth(self):

        """获取当前月份，如 9"""
        return datetime.datetime.now().strftime("%m")

    def getDay(self):

        """获取当前日份，如 19"""
        return datetime.datetime.now().strftime("%d")

    def getYearMonth(self):

        """获取当前年月，如 201909"""
        return datetime.datetime.now().strftime("%Y%m")

    def getMonthDay(self):

        """获取当前月日，如 0919"""
        return datetime.datetime.now().strftime("%m%d")

    def getWeek(self, varDate):

        """获取当天/某天是星期几"""

        if varDate == "":
            varDate = datetime.datetime.now()
        else:
            varDate = datetime.datetime(
                int(varDate.split("-")[0]),
                int(varDate.split("-")[1]),
                int(varDate.split("-")[2]),
            )

        if varDate.weekday() == 0:  # Monday
            return "星期一"
        elif varDate.weekday() == 1:  # Tuesday
            return "星期二"
        elif varDate.weekday() == 2:  # Wednesday
            return "星期三"
        elif varDate.weekday() == 3:  # Thursday
            return "星期四"
        elif varDate.weekday() == 4:  # Friday
            return "星期五"
        elif varDate.weekday() == 5:  # Saturday
            return "星期六"
        else:  # Sunday
            return "星期日"

    def getWeekByEng(self, varDate, varStrftime):

        """获取当天/某天是星期几,英文输出 Monthday 或 Mon"""

        if varDate == "":
            varDate = datetime.datetime.now().strftime(varStrftime)

        else:
            varDate = datetime.datetime(
                int(varDate.split("-")[0]),
                int(varDate.split("-")[1]),
                int(varDate.split("-")[2]),
            ).strftime(varStrftime)
        return varDate

    def getDateByMinusPeriod(self, n=0):

        """获取当前日期的前后日期
        （如：当天日期 2022-03-21）
        如：getDateByMinusPeriod（20）  //20天后  2022-03-23
        如：getDateByMinusPeriod（-3）  //3天前   2022-03-18
        """

        if n < 0:
            n = abs(n)
            return date.today() - timedelta(days=n)
        else:
            return date.today() + timedelta(days=n)

    def getDateByFirstDay(self, year, mon):

        """获取某年月的第一天日期，如 2019-08-01"""
        days = "01"
        if int(mon) < 10:
            mon = "0" + str(int(mon))
        arr = (year, mon, days)
        return "-".join("%s" % i for i in arr)

    def getDateByLastDay(self, year, mon):

        """获取某年某月最后一天日期，如 2019-08-31"""
        days = calendar.monthrange(year, mon)[1]
        mon = self.addZeroByPrefix(mon)
        arr = (year, mon, days)
        return "-".join("%s" % i for i in arr)

    def f(self, n=0):
        """依据当前月份，返回n月前或n月后的第一天。如：当前9月份，
        n = 2 , 返回 2019-11-1
        n = -1 , 返回 2019-8-1
        """
        (y, m, d) = self.getDate_tuple(n)
        d = "01"
        arr = (y, m, d)
        return "-".join("%s" % i for i in arr)

    def getDateByMonthLastDay(self, n=0):
        """依据当前月份，返回n月前或n月后的最后一天。如：当前9月份，
               n = 2 , 返回 2019-11-30
               n = -1 , 返回 2019-8-31
        不支持跨年
        """
        return "-".join("%s" % i for i in self.getDate_tuple(n))

    def getDateByMonthToday(self, n=0):
        """''
        返回前后N月的当前日期
        if n>0, 获取当前日期前N月的日期
        if n<0, 获取当前日期后N月的日期
        date format = "YYYY-MM-DD"
        """
        (y, m, d) = self.getDate_tuple(n)
        arr = (y, m, d)
        if int(self.day) < int(d):
            arr = (y, m, self.day)
        return "-".join("%s" % i for i in arr)

    def getDateByPeriodDate(self, varDate, varDays):
        """获取某个日期的前后日期
        如获取某一个日期的上一天   print(Time_PO.getBeforeAfterDate("2019-12-15", -1))
        如获取某一个日期的后二天   print(Time_PO.getBeforeAfterDate("2019-12-15", 2))
        注意，先将字符串转换成日期格式，
        """
        from datetime import datetime

        varDate = datetime.strptime(varDate, "%Y-%m-%d").date()
        import datetime

        return varDate + datetime.timedelta(days=varDays)

    def getDateByTuple(self, n=0):
        """''
        get the year,month,days from today
        befor or after n months
        """
        thisyear = int(self.year)
        thismon = int(self.mon)
        totalmon = thismon + n
        if n >= 0:
            if totalmon <= 12:
                days = str(self.get_days_of_month(thisyear, totalmon))
                totalmon = self.addZeroByPrefix(totalmon)
                return (self.year, totalmon, days)
            else:
                i = totalmon / 12
                j = totalmon % 12
                if j == 0:
                    i -= 1
                    j = 12
                thisyear += i
                days = str(self.get_days_of_month(thisyear, j))
                j = self.addZeroByPrefix(j)
                return (str(thisyear), str(j), days)
        else:
            if (totalmon > 0) and (totalmon < 12):
                days = str(self.get_days_of_month(thisyear, totalmon))
                totalmon = self.addZeroByPrefix(totalmon)
                return (self.year, totalmon, days)
            else:
                i = totalmon / 12
                j = totalmon % 12
                if j == 0:
                    i -= 1
                    j = 12
                thisyear += i
                days = str(self.get_days_of_month(thisyear, j))
                j = self.addZeroByPrefix(j)
                return (str(thisyear), str(j), days)

    def getDayByYearMonth(self, year, mon):

        """获取某年月的天数"""
        return calendar.monthrange(year, mon)[1]

    def addZeroByPrefix(self, n):
        """自动在 0-9 前加0，如返回 01-09"""
        nabs = abs(int(n))
        if nabs < 10:
            return "0" + str(nabs)
        else:
            return nabs

    def now2timestamp(self):
        import time

        # now时间 转 时间戳'''
        dtime = datetime.datetime.now()  # 2017-09-15 09:41:27.336784
        return time.mktime(dtime.timetuple())  # 1505439687.0

    def datetime2timestamp(self, varDatetime):
        import time

        """将字符串的时间转换为时间戳"""
        timeArray = time.strptime(varDatetime, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def timestamp2datetime(self, intTimestamp):
        """时间戳 转 时间"""
        return datetime.datetime.fromtimestamp(intTimestamp)

    # 日期比较（日期1大于日期2，返回True或False）
    def isDate1GTdate2(self, varDate1, varDate2, fmt="%Y-%m-%d"):
        zero = datetime.datetime.fromtimestamp(0)
        try:
            d1 = datetime.datetime.strptime(str(varDate1), fmt)
        except:
            d1 = zero
        try:
            d2 = datetime.datetime.strptime(str(varDate2), fmt)
        except:
            d2 = zero
        return d1 > d2

    # 日期比较（日期1小于日期2，返回True或False）
    def isDate1LTdate2(self, varDate1, varDate2, fmt="%Y-%m-%d"):
        zero = datetime.datetime.fromtimestamp(0)
        try:
            d1 = datetime.datetime.strptime(str(varDate1), fmt)
        except:
            d1 = zero
        try:
            d2 = datetime.datetime.strptime(str(varDate2), fmt)
        except:
            d2 = zero
        return d1 < d2

    def get_weekday(self, x):
        # 获取每月工作日天数，
        from datetime import datetime

        start_date = x + "-01"
        # start_date
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        start_datetime_2 = datetime.date(start_datetime)
        # 计算每月最后一天的date
        days_in_month = start_datetime_2.replace(day=28) + timedelta(days=4)
        # print( start_datetime_2.replace(day=28))
        end_date = days_in_month - timedelta(days=days_in_month.day)
        # print(start_datetime_2,end_date)
        cal = China()
        data = cal.get_working_days_delta(start_datetime_2, end_date)
        return data

    def sec2hms1(self, varSec):

        # "秒转时分秒1"

        # divmod() 函数把除数和余数运算结果结合起来，返回一个包含商和余数的元组(a // b, a % b)。
        m, s = divmod(varSec, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def sec2hms2(self, varSec):

        # "秒转时分秒2"

        from time import strftime
        from time import gmtime

        return strftime("%H:%M:%S", gmtime(170))  # 00:02:50


if __name__ == "__main__":

    Time_PO = TimePO()

    # print(Time_PO.getDate())  # 20200319
    # print(Time_PO.getDateByMinus())  # 2020-03-19
    # print(Time_PO.getDateByDivide())  # 2020/03/19
    # print(Time_PO.getDateTime())  # 20200319151928
    # print(Time_PO.getDateTimeByDivide())  # 2020/03/19 15:19:28
    #
    # print(Time_PO.getDateByMinus())  # 2022-11-29   //当前日期
    # print(Time_PO.getDateByMinusPeriod(2))  # 2022-12-01  //2天后
    print(Time_PO.getDateByMinusPeriod(-3))  # 2022-11-26  //3天前
    print(type(Time_PO.getDateByMinusPeriod(-3)))  # 2022-11-26  //3天前
    # print(Time_PO.getDateTimeByPeriod(0))  # 2020-03-19 15:19:28   //当前时间
    # print(Time_PO.getDateTimeByPeriod(0.5))  # 2020-03-19 15:49:28  //比当前时间晚30分钟
    # print(Time_PO.getDateTimeByPeriod(-1))  # 2020-03-19 14:19:28   //比当前时间早1小时
    # print(Time_PO.getNow())  # 2022-11-29 12:48:23.907028  //当前时间
    # print(Time_PO.getNowByPeriod(0.5))  # 2022-11-29 13:19:37.939408  //比当前时间晚30分钟
    # print(Time_PO.getNowByPeriod(-1))  # 2022-11-29 11:49:37.939408  //比当前时间早1小时
    #
    # print(Time_PO.getYear())  # 2020
    # print(Time_PO.getMonth())  # 03
    # print(Time_PO.getDay())  # 19
    # print(Time_PO.getYearMonth())  # 202003
    # print(Time_PO.getMonthDay())  # 0319
    #
    # print(Time_PO.getWeek(""))  # 星期一
    # print(Time_PO.getWeek("2019-12-15"))  # 星期日
    # print(Time_PO.getWeekByEng("", "%A"))  # Monthday
    # print(Time_PO.getWeekByEng("", "%a"))  # Mon
    # print(Time_PO.getWeekByEng("2019-12-15", "%A"))  # Sunday
    # print(Time_PO.getWeekByEng("2019-12-15", "%a"))  # Sun

    # print(Time_PO.getDateByFirstDay(2019, 7))  # 2019-07-01  //获取某年月的第一天
    # print(Time_PO.getDateByLastDay(2019, 7))  # 2019-07-31   //获取某年月的最后一天
    # print(Time_PO.getDateByPeriodDate("2019-12-15", -1))   # 2019-12-14   //返回指定日期的前一天
    # print(Time_PO.getDateByPeriodDate("2019-12-15", 2))   # 2019-12-17  //返回指定日期的后2天

    # print(Time_PO.getDayByYearMonth(2019, 2))  # 28   //2019年2月的天数
    # print(Time_PO.addZeroByPrefix(9))  # 09    //自动在 1 - 9 前加上0

    # print(Time_PO.now2timestamp())  # 1584603355.0  //当前日期时间转时间戳
    # print(Time_PO.datetime2timestamp(Time_PO.getDateTimeByPeriod(0)))  # 1584603355   //日期时间转时间戳
    # print(Time_PO.timestamp2datetime(Time_PO.now2timestamp()))  # 2020-03-19 15:35:55  //时间戳转日期时间

    # print("求时间差，输出天时分秒".center(100, "-"))
    # date_start = pd.to_datetime(datetime.datetime.now())  # Timestamp('2021-05-19 08:06:08.683355')
    # sleep(6)  # ----这里是程序执行部分----
    # date_end = pd.to_datetime(datetime.datetime.now())  # Timestamp('2021-05-19 08:06:08.683355')
    # print(date_end - date_start)  # 0 days 00:00:06.010230
    #
    #
    # print("求时间差，输出秒".center(100, "-"))
    # time_start = time.time()
    # sleep(6)  # ----这里是程序执行部分----
    # time_end = time.time()
    # time = time_end - time_start
    # print('耗时：%s 秒' % time)  # 耗时：6.008593320846558 秒
    #

    # print("秒转时分秒1".center(100, "-"))
    # print(Time_PO.sec2hms1(170))

    # print("秒转时分秒2".center(100, "-"))
    # print(Time_PO.sec2hms2(170))

    # ======================================================================================================================
    #     以下不可用或有局限

    # # 日期比较（日期1晚于日期2，返回True或False）？
    # print(Time_PO.isDate1GTdate2("2020-1-1", "2020-1-5"))
    # print(Time_PO.isDate1GTdate2("2020-4-1", "2020-1-5"))

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
    # print(Time_PO.get_weekday("2020-12"))
