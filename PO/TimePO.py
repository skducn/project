# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2017-10-26
# Description   : 日期时间格式
# *********************************************************************

from time import strftime, localtime
from datetime import date, datetime, timedelta
import calendar, datetime, time
from workalendar.asia import China
cal = China()

class TimePO():

    def __init__(self):
        self.year = strftime("%Y", localtime())
        self.mon = strftime("%m", localtime())
        self.day = strftime("%d", localtime())
        self.hour = strftime("%H", localtime())
        self.min = strftime("%M", localtime())
        self.sec = strftime("%S", localtime())

    def getDate(self):
        ''' 返回当前日期字符串（年月日），如 20190819 '''
        return self.year + self.mon + self.day

    def getDate_minus(self):
        ''' 返回当天日期（年-月-日），如 2019-09-19 '''
        return str(date.today())

    def getDate_divide(self):
        ''' 返回当天日期（年/月/日），如 2019/09/19 '''
        return time.strftime("%Y/%m/%d", time.strptime(str(date.today()),"%Y-%m-%d"))

    def getDatetime(self):
        ''' 返回当天日期时间字符串（年月日时分秒），如 20190919163619 '''
        return self.year + self.mon + self.day + self.hour + self.min + self.sec

    def getDatetime_minus(self):
        ''' 返回当天日期时间（年-月-日 时：分：秒），如 2019-09-19 16:36:19 '''
        return strftime("%Y-%m-%d %H:%M:%S", localtime())

    def getDatetime_divide(self):
        ''' 返回当天日期时间（年/月/日 时：分：秒），如 2019/09/19 16:36:19 '''
        # return strftime("%Y-%m-%d %H:%M:%S", localtime())
        return time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(strftime("%Y-%m-%d %H:%M:%S", localtime()),"%Y-%m-%d %H:%M:%S"))

    def getDatetimeEditHour(self, n):
        ''' 给当前时间加上或减去 n 小时，并返回日期（年月日时分秒）,如 2017-09-15 10:11:27 '''
        return (datetime.datetime.now() + datetime.timedelta(hours=n)).strftime('%Y-%m-%d %H:%M:%S')

    def getNow(self):
        ''' 返回当前日期（年月日时分秒后及后6位数），如 2017-09-15 09:41:27.336765 '''
        return datetime.datetime.now()

    def getNowEditHour(self, n):
        ''' 给当前时间加上或减去 n 小时，并返回日期（年月日时分秒后及后6位数）,如
        # datetime.datetime.now() + datetime.timedelta(hours = 0.5)  # 如 2017-09-15 10:11:27.336765'''
        # datetime.datetime.now() + datetime.timedelta(hours = -0.5) '''
        return datetime.datetime.now() + datetime.timedelta(hours=n)

    def getYear(self):
        ''' 返回当前年份，如 2019 '''
        return datetime.datetime.now().strftime('%Y')

    def getMonth(self):
        ''' 返回当前月份，如 9 '''
        return datetime.datetime.now().strftime('%m')

    def getDay(self):
        ''' 返回当前日份，如 19 '''
        return datetime.datetime.now().strftime('%d')

    def getYearMonth(self):
        ''' 返回当前年月，如 201909 '''
        return datetime.datetime.now().strftime('%Y%m')

    def getMonthDay(self):
        ''' 返回当前月日，如 0919 '''
        return datetime.datetime.now().strftime('%m%d')


    def get_day_of_day(self, n=0):
        ''' 返回n天前或n天后的日期（年-月-日），如 2019-09-18
          if n>=0, 返回n天后日期
          if n<0, 返回n天前日期
        '''
        if (n < 0):
            n = abs(n)
            return date.today() - timedelta(days=n)
        else:
            return date.today() + timedelta(days=n)

    def get_days_of_month(self, year, mon):
        ''' 返回某年某月的天数 '''
        return calendar.monthrange(year, mon)[1]

    def get_firstday_of_month(self,year, mon):
        ''' 返回某年某月的第一天日期，如 2019-08-01 '''
        days = "01"
        if (int(mon) < 10):
            mon = "0" + str(int(mon))
        arr = (year, mon, days)
        return "-".join("%s" % i for i in arr)

    def get_lastday_of_month(self,year, mon):
        ''' 返回某年某月最后一天日期，如 2019-08-31 '''
        days = calendar.monthrange(year, mon)[1]
        mon = self.addzero(mon)
        arr = (year, mon, days)
        return "-".join("%s" % i for i in arr)

    def get_firstday_month(self, n=0):
        ''' 依据当前月份，返回n月前或n月后的第一天。如：当前9月份，
            n = 2 , 返回 2019-11-1
            n = -1 , 返回 2019-8-1
        '''
        (y, m, d) = self.getDate_tuple(n)
        d = "01"
        arr = (y, m, d)
        return "-".join("%s" % i for i in arr)

    def get_lastday_month(self, n=0):
        ''' 依据当前月份，返回n月前或n月后的最后一天。如：当前9月份，
                   n = 2 , 返回 2019-11-30
                   n = -1 , 返回 2019-8-31
            不支持跨年
        '''
        return "-".join("%s" % i for i in self.getDate_tuple(n))

    def getDate_tuple(self, n=0):
        '''''
          get the year,month,days from today
          befor or after n months
          '''
        thisyear = int(self.year)
        thismon = int(self.mon)
        totalmon = thismon + n
        if (n >= 0):
            if (totalmon <= 12):
                days = str(self.get_days_of_month(thisyear, totalmon))
                totalmon = self.addzero(totalmon)
                return (self.year, totalmon, days)
            else:
                i = totalmon / 12
                j = totalmon % 12
                if (j == 0):
                    i -= 1
                    j = 12
                thisyear += i
                days = str(self.get_days_of_month(thisyear, j))
                j = self.addzero(j)
                return (str(thisyear), str(j), days)
        else:
            if ((totalmon > 0) and (totalmon < 12)):
                days = str(self.get_days_of_month(thisyear, totalmon))
                totalmon = self.addzero(totalmon)
                return (self.year, totalmon, days)
            else:
                i = totalmon / 12
                j = totalmon % 12
                if (j == 0):
                    i -= 1
                    j = 12
                thisyear += i
                days = str(self.get_days_of_month(thisyear, j))
                j = self.addzero(j)
                return (str(thisyear), str(j), days)

    def addzero(self, n):
        ''' 自动在 0-9 前加0，如返回 01-09 '''
        nabs = abs(int(n))
        if (nabs < 10):
            return "0" + str(nabs)
        else:
            return nabs

    def get_today_month(self,n=0):
        '''''
          返回前后N月的当前日期
          if n>0, 获取当前日期前N月的日期
          if n<0, 获取当前日期后N月的日期
          date format = "YYYY-MM-DD"
          '''
        (y, m, d) = self.getDate_tuple(n)
        arr = (y, m, d)
        if (int(self.day) < int(d)):
            arr = (y, m, self.day)
        return "-".join("%s" % i for i in arr)

    def getWeekday(self):
        ''' 返回当天是星期几 '''
        today = datetime.datetime.now()
        if (today.weekday() == 0):  # Monday
            return ("星期一")
        elif (today.weekday() == 1):  # Tuesday
            return("星期二")
        elif (today.weekday() == 2):  # Wednesday
            return("星期三")
        elif (today.weekday() == 3):  # Thursday
            return("星期四")
        elif (today.weekday() == 4):  # Friday
            return("星期五")
        elif (today.weekday() == 5):  # Saturday
            return("星期六")
        else:    # Sunday
            return("星期日")

    def now2timestamp(self):
        import time
        # now时间 转 时间戳'''
        dtime = datetime.datetime.now()  # 2017-09-15 09:41:27.336784
        return time.mktime(dtime.timetuple())  # 1505439687.0

    def datetime2timestamp(self, varDatetime):
        import time
        '''将字符串的时间转换为时间戳'''
        timeArray = time.strptime(varDatetime, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def timestamp2datetime(self, intTimestamp):
        ''' 时间戳 转 时间'''
        return datetime.datetime.fromtimestamp(intTimestamp)

    def getBeforeAfterDate(self, varDate, varDays):
        ''' 获取某个日期的前后日期
        如获取某一个日期的上一天   print(Time_PO.getBeforeAfterDate("2019-12-15", -1))
        如获取某一个日期的后二天   print(Time_PO.getBeforeAfterDate("2019-12-15", 2))
        注意，先将字符串转换成日期格式，
        '''
        from datetime import datetime
        varDate = datetime.strptime(varDate, '%Y-%m-%d').date()
        import datetime
        return (varDate + datetime.timedelta(days=varDays))

    def get_weekday(self,x):
        # 获取每月工作日天数，
        from datetime import datetime
        start_date = x + '-01'
        # start_date
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        start_datetime_2 = datetime.date(start_datetime)
        # 计算每月最后一天的date
        days_in_month = start_datetime_2.replace(day=28) + timedelta(days=4)
        # print( start_datetime_2.replace(day=28))
        end_date = days_in_month - timedelta(days=days_in_month.day)
        # print(start_datetime_2,end_date)
        cal = China()
        data = cal.get_working_days_delta(start_datetime_2, end_date)
        return data

    # # # 计算耗时功能
    # time_start = time.time()
    # # ----这里是程序执行部分----
    # time_end = time.time()
    # time = time_end - time_start
    # print('耗时%s秒' % time)
    # Color_PO.consoleColor("31", "33", "耗时 " + str(round(time, 0)) + " 秒", "")

    # 日期比较，日期1大于日期2，返回True
    def isDate1GTdate2(self ,varDate1, varDate2, fmt='%Y-%m-%d'):
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

    # 日期比较，日期1小于日期2，返回True
    def isDate1LTdate2(self ,varDate1, varDate2, fmt='%Y-%m-%d'):
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

if __name__ == "__main__":

    Time_PO = TimePO()

    print(Time_PO.isDate1GTdate2("2020-1-1", "2019-1-5"))
    print(Time_PO.isDate1LTdate2("2020-1-1", "2019-1-5"))

    # # 获取2020年法定节假日
    # print(cal.holidays(2020))
    #
    # # 判断某天是否工作日（周一到周五返回True，周六日回False）
    # print(cal.is_working_day(date(2020, 12, 18)))
    #
    # # 获取连续多个月工作日天数（不包括双休日与节假日）
    # print(cal.get_working_days_delta(date(2020, 11, 1), date(2020, 12, 31)))
    #
    #
    # # 获取每月工作日天数（不包括双休日与节假日）
    # print(Time_PO.get_weekday("2020-12"))

    # 获取当前日期年月日时分秒
    # print(Time_PO.getDate())  # 20200319
    # print(Time_PO.getDate_minus())  # 2020-03-19
    # print(Time_PO.getDate_divide())  # 2020/03/19
    # print(Time_PO.getDatetime())  # 20200319151928
    # print(Time_PO.getDatetime_divide())  # 2020/03/19 15:19:28
    # print(Time_PO.getDatetimeEditHour(0))  # 2020/03/19 15:19:28
    # print(Time_PO.getDatetimeEditHour(0.5))  # 2020-03-19 15:49:28  //当前时间晚30分钟
    # print(Time_PO.getDatetimeEditHour(-1))  # 2020-03-19 14:19:28   //当前时间早1小时
    # print(Time_PO.getNow())  # 2020/03/19 15:19:28.470652
    # print(Time_PO.getNowEditHour(0.5))  # 2020-03-19 15:49:28 .470652  //当前时间晚30分钟
    # print(Time_PO.getNowEditHour(-1))  # 2020-03-19 14:19:28 .470652  //当前时间早1小时
    # print(Time_PO.getYear())  # 2020
    # print(Time_PO.getMonth())  # 03
    # print(Time_PO.getDay())  # 19
    # print(Time_PO.getYearMonth())  # 202003
    # print(Time_PO.getMonthDay())  # 0319
    # print(Time_PO.getWeekday())  # 星期四
    # print(Time_PO.now2timestamp())  # 1584603355.0  //当前日期时间转时间戳
    # print(Time_PO.datetime2timestamp(Time_PO.getDatetimeEditHour(0)))  # 1584603355   //日期时间转时间戳
    # print(Time_PO.timestamp2datetime(Time_PO.now2timestamp()))  # 2020-03-19 15:35:55  //时间戳转日期时间
    # print(Time_PO.get_day_of_day(20))  # 2020-04-09  //20天后
    # print(Time_PO.get_day_of_day(-3))  # 2020-03-16  //3天前
    # print(Time_PO.get_days_of_month(2019, 2))  # 28   //2019年2月的天数
    # print(Time_PO.get_firstday_of_month(2019, 7))  # 2019-07-01  //获取某年某月的第一天
    # print(Time_PO.get_lastday_of_month(2019, 7))  # 2019-07-31  //获取某年某月的最后一天
    # print(Time_PO.get_lastday_month(-1))   # 2020-02-29  //返回上月的最后一天。（不支持跨年，如2020-01-01的上个月会报错）
    # print(Time_PO.get_lastday_month(1))  # 2020-02-29  //返回下月的最后一天。（不支持跨年，如2020-12-12 的下个月会报错）

    # print(Time_PO.getDate_tuple(1))  # ('2020', '04', '30')    //列表形式返回下个月及最后一天
    # print(Time_PO.addzero(9))  # 09    //自动在 1 - 9 前加上0
    # print(Time_PO.get_today_month(-1))  # 2020-02-19   //返回上个月的今天
    # print(Time_PO.get_today_month(3))  # 2020-06-19   //返回3个月后的今天
    # print(Time_PO.getBeforeAfterDate("2019-12-15", -1))   # 2019-12-14  ，注意第一个参数日期是字符串  //返回指定日期的前一天
    # print(Time_PO.getBeforeAfterDate("2019-12-15", 2))   # 2019-12-17  //返回指定日期的后2天
    # print(Time_PO.getBeforeAfterDate(Time_PO.getDate_minus(), 2))   # 2019-12-17  //返回后天







