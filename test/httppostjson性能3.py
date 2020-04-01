#coding=utf-8

import requests
import datetime
import time
# import multiprocessing
import threading
import hashlib


# import cnf
class url_request():
    times = []
    error = []
    success = []
    durtimes = []




    def md5(self, str):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def LPostMsg(self):
        myreq = url_request()

        url = "http://43.254.24.107:8080/dangjian/v1/user/login"
        msg = ''
        senderTag = ''
        msgType = '1'
        contentType = '1'
        sign = ''

        sendData = {"check": "4BC42AADB36F554B87BEBC0CDB4E32C2",'json':"{\"phoneNumber\":\"13816109050\",\"password\":\"F74680162ACCD40CEDDF8F272DE8227E\",\"pushToken\":\"1a0018970a949ad5745|0\"}"}
        while 1:
            try:
                startTime = datetime.datetime.now()

                r = requests.post(url, data=sendData)
                responseTime = float(r.elapsed.microseconds) / 1000  # 获取响应时间，单位ms
                #                print r.content
                myreq.times.append(responseTime)
                #        print 'cc=',myreq.times


                if r.status_code == 200:
                    myreq.success.append("1")
                else:
                    myreq.error.append("0")

                endTime = datetime.datetime.now()

                myreq.durtimes.append(((endTime - startTime).microseconds / 1000))
                #            print myreq.durtimes
                if sum(myreq.durtimes) > 1 * 10 * 1000:
                    break
            except Exception, e:
                myreq.error.append("0")
                print str(e)
            finally:
                r.close()
                r.raw.closed

    def Lrequest(self, ):
        myreq = url_request()

        while 1:
            try:
                startTime = datetime.datetime.now()
                r = requests.get('http://43.254.24.107:8080/dangjian/v1/user/login', headers={"check": "4BC42AADB36F554B87BEBC0CDB4E32C2",'json': "{\"phoneNumber\":\"13816109050\",\"password\":\"F74680162ACCD40CEDDF8F272DE8227E\",\"pushToken\":\"1a0018970a949ad5745|0\"}"})
                responseTime = float(r.elapsed.microseconds) / 1000  # 获取响应时间，单位ms

                myreq.times.append(responseTime)
                #        print 'cc=',myreq.times


                if r.status_code == 200:
                    myreq.success.append("1")
                else:
                    myreq.error.append("0")

                endTime = datetime.datetime.now()

                myreq.durtimes.append(((endTime - startTime).microseconds / 1000))
                #            print myreq.durtimes
                if sum(myreq.durtimes) > 1 * 10 * 1000:
                    break
            except Exception, e:
                myreq.error.append("0")
                print str(e)
            finally:
                r.close()
                r.raw.closed


if __name__ == "__main__":
    myreq = url_request()
    #    for x in range(2):
    #        myreq.Lrequest()
    #    print myreq.times
    threads = []
    startTime = datetime.datetime.now()

    print 'request start time %s' % startTime
    Num = 100
    ThinkTime = 0.5

    for i in range(1, Num + 1):
        t = threading.Thread(target=myreq.LPostMsg)
        threads.append(t)

    for t in threads:
        time.sleep(ThinkTime)
        #        print 'thread %s' % t
        t.setDaemon(True)
        t.start()
    # 销毁线程
    for t in threads:
        t.join()

    endTime = datetime.datetime.now()
    print 'request end time %s' % endTime

    time.sleep(1)
    #    print float(sum(myreq.times))
    AverageTime = "{:.3f}".format(float(sum(myreq.times)) / float(len(myreq.times)))  # 计算平均时间，保留小数点后3位
    print u'平均响应时间Average Response Time %s ms ' % AverageTime

    usertime = str(endTime - startTime)

    hour = usertime.split(':').pop(0)
    minute = usertime.split(':').pop(1)
    second = usertime.split(':').pop(2)

    totalTime = float(hour) * 60 * 60 + float(minute) * 60 + float(second)
    # TPS=U_concurrent / (T_response+T_think)
    tps = Num / (float(AverageTime) / 1000)
    print 'Concurrent processing %s' % Num
    print 'Use total time %s s' % (totalTime - float(Num * ThinkTime))
    print 'Success request %s' % myreq.success.count('1')
    print 'Fail request %s ' % myreq.error.count('0')
    print u'每秒钟事务请求数量Tps %s ' % tps