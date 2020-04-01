# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.0.0
# Date       : 2017-5-16
# Description: 接口参数json，http post json
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import os, urllib, urllib2, re, cookielib,json

headers = values = {}
headers['Content-Type'] = 'application/json; charset=utf-8'
url = 'http://43.254.24.107'
port = '8080'
route = 'dangjian/v1/user/login'


# android json值位置固定格式
values["check"] = "4BC42AADB36F554B87BEBC0CDB4E32C2"
values['json'] = "{\"phoneNumber\":\"13816109050\",\"password\":\"F74680162ACCD40CEDDF8F272DE8227E\",\"pushToken\":\"1a0018970a949ad5745|0\"}"

# # ios json值位置固定格式
# values["check"] = "5b140656cfe0a8427971dc10b673c428"
# values['json'] = "{\"passWord\":\"f74680162accd40ceddf8f272de8227e\",\"pushToken\":\"1114a897929956e3ab3|1\",\"phoneNumber\":\"13816109050\"}"


# 
post_data = urllib.urlencode(values)
print post_data
print "~~~~~~"


def jsonPost(param):
    j_data = json.dumps(values)
    req = urllib2.Request(param, j_data, headers)
    page = urllib2.urlopen(req)
    res = page.read()
    page.close()
    print res

jsonPost("%s:%s/%s" % (url, port, route))


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 结果：
# json格式
# {"json": "{\"phoneNumber\":\"13816109050\",\"password\":\"F74680162ACCD40CEDDF8F272DE8227E\",\"pushToken\":\"1a0018970a949ad5745|0\"}", "check": "4BC42AADB36F554B87BEBC0CDB4E32C2"}

# 接口返回值：
# {"check":"BF33158FA490A4F5F6A45695ADE48C9C","json":{"data":{"bannerList":[{"pictureUrl":"http://43.254.24.107:8080/201704/images/58ed9e690141e523593.jpg","linkUrl":"","newsId":"47"}],"result":"success","videoCount":"0","memo":"0","imageUrl":"http://43.254.24.107:8080/image/user/user821492162570463.jpg","videoTypeList":[{"id":"0","name":"推荐"},{"id":"4","name":"学党规党章"},{"id":"2","name":"学习近平讲话"},{"id":"3","name":"十八届六中全会精神"},{"id":"5","name":"中国电科新闻报道"},{"id":"1","name":"时政新闻"}],"examinationId":"4","imVoipPwd":"JLtV2eUI","messageNum":"0","enCode":"58d0b36363259","bookTypeList":[{"id":"4","name":"学党规党章"},{"id":"2","name":"学习近平讲话"},{"id":"3","name":"十八届六中全会精神"},{"id":"5","name":"中国电科新闻报道"},{"id":"1","name":"时政新闻"}],"userSessionId":"4bf6507fffda51f65b87febe4110b3e8","autoTypeList":[{"id":"0","name":"推荐"},{"id":"4","name":"学党规党章"},{"id":"2","name":"学习近平讲话"},{"id":"3","name":"十八届六中全会精神"},{"id":"5","name":"中国电科新闻报道"},{"id":"1","name":"时政新闻"}],"phoneNumber":"13816109050","email":"jinhao@cetc-ss.com","imVoip":"80002700000086","errMsg":"","userId":"82","name":"金浩","informationCount":0,"userName":"jinhao","headlinesList":[{"id":"0","name":"推荐"},{"id":"1","name":"CETC"}],"ifSign":"0","motto":"开心网和韩国广告红红火火vvfddfyhhhf"},"msgExt":null,"respCode":"0000","respDesc":"操作成功"}}


