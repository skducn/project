# coding: utf-8

# http://blog.csdn.net/alpha5/article/details/24964009
# python requests的安装与简单运用
import requests

# 红包比大小游戏退出
url = "http://192.168.2.176:9999/game/login/1.0/redpacketGameQuit.do"
querystring = {"userId":"10001679"}
headers = {
    'cache-control': "no-cache",
    }
response = requests.request("GET", url, headers=headers, params=querystring)
# 获取响应内容
print response.content
print(response.text)
# 获取Json格式
print response.json()
print response.json()['success']
# 获取响应状态码
print response.status_code
print response.history
# 响应头内容
print response.headers
# 获取响应头指定Key的值
print response.headers['Date']
# 请求头内容
print response.request.headers
# 设置超时实际, 可用于检查接口性能,超时=1s , 10s内没有打开页面则报错.
requests.get('http://www.baidu.com', timeout=1)

# 百度搜索结果中的302跳转地址
r = requests.get('http://www.baidu.com/link?url=QeTRFOS7TuUQRppa0wlTJJr6FfIYI1DJprJukx4Qy0XnsDO_s9baoO8u1wvjxgqN',allow_redirects = False)
print r.status_code

# 获取网页
r = requests.get('http://www.zhidaow.com')
# r = requests.post("http://httpbin.org/post")
# r = requests.put("http://httpbin.org/put")
# r = requests.delete("http://httpbin.org/delete")
# r = requests.head("http://httpbin.org/get")
# r = requests.options("http://httpbin.org/get")

# r = requests.get('http://www.baidu.com')
# 获取网页编码
# print r.encoding  # 'utf-8'
# # r.encoding = 'ISO-8859-1'
# print r.encoding
# print r.text

# 自定义请求头部
# 伪装请求头部是采集时经常用的，我们可以用这个方法来隐藏：
r = requests.get('http://www.zhidaow.com')
print r.request.headers['User-Agent']
#python-requests/1.2.3 CPython/2.7.3 Windows/XP

headers = {'User-Agent': 'alexkh'}
r = requests.get('http://www.zhidaow.com', headers = headers)
print r.request.headers['User-Agent']
#alexkh