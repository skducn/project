#!/user/bin/env python
#coding=utf-8
import requests
import datetime
import time
import threading


# android json值位置固定格式
# values["check"] = "4BC42AADB36F554B87BEBC0CDB4E32C2"
# values['json'] = "{\"phoneNumber\":\"13816109050\",\"password\":\"F74680162ACCD40CEDDF8F272DE8227E\",\"pushToken\":\"1a0018970a949ad5745|0\"}"


class url_request():
    times = []
    error = []
    def req(self,AppID,url):
        myreq=url_request()
        headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
        payload = {'check':AppID,'json':url}
        r = requests.post("http://43.254.24.107:8080/dangjian/v1/user/login",headers=headers,data=payload)
        ResponseTime=float(r.elapsed.microseconds)/1000 #获取响应时间，单位ms
        myreq.times.append(ResponseTime) #将响应时间写入数组
        if r.status_code !=200 :
            myreq.error.append("0")

if __name__=='__main__':
    myreq=url_request()
    threads = []
    starttime = datetime.datetime.now()
    print u"请求启动时间： %s" %starttime

    nub = 100  # 设置并发线程数
    ThinkTime = 0.5  # 设置思考时间

    for i in range(1, nub+1):
        t = threading.Thread(target=myreq.req, args=('4BC42AADB36F554B87BEBC0CDB4E32C2',"{\"phoneNumber\":\"13816109050\",\"password\":\"F74680162ACCD40CEDDF8F272DE8227E\",\"pushToken\":\"1a0018970a949ad5745|0\"}"))
        threads.append(t)
    for t in threads:
        time.sleep(ThinkTime)
        #print "thread %s" %t #打印线程
        t.setDaemon(True)
        t.start()
    t.join()
    endtime = datetime.datetime.now()
    print u"请求结束时间：%s" %endtime
    time.sleep(3)
    AverageTime = "{:.3f}".format(float(sum(myreq.times))/float(len(myreq.times))) #计算数组的平均值，保留3位小数
    print u"平均响应时间(Average Response Time) %s ms" %AverageTime #打印平均响应时间
    usetime = str(endtime - starttime)
    hour = usetime.split(':').pop(0)
    minute = usetime.split(':').pop(1)
    second = usetime.split(':').pop(2)
    totaltime = float(hour)*60*60 + float(minute)*60 + float(second) #计算总的思考时间+请求时间
    print u"并发数(Concurrent processing) %s" %nub #打印并发数
    print u"总共消耗的时间(use total time) %s s" %(totaltime-float(nub*ThinkTime)) #打印总共消耗的时间
    print u"错误请求数(fail request)： %s" %myreq.error.count("0") #打印错误请求数