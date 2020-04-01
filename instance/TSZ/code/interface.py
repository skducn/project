# coding: utf-8

# http://blog.csdn.net/alpha5/article/details/24964009
# python requests的安装与简单运用
import requests,redis
from time import sleep

print  "\n====================== 2.3版本_APP接口测试 ======================"
def I23_3(varnum,varstartIndex):
    # 参数1: startIndex = 翻页起始值
    varInterfaceName =  "3 游戏列表接口"

    url = "http://192.168.2.176:9999/game/login/1.0/gameMenu.do"
    querystring = {"varstartIndex":varstartIndex}
    headers = {
        'cache-control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    try:
        if varnum==1 :
            if response.json()['success']:
                print "OK," + varInterfaceName + ",正确返回值"
            else:
                print "Err," + varInterfaceName + ",正确返回值!"
            print response.content +"\n"

        if varnum==2 :
            if response.json()['errorcode']=='100001' and response.json()['success']==False:
                print "OK," + varInterfaceName + ",系统错误"
            else:
                print "Err," + varInterfaceName + ",系统错误!"
            print response.content +"\n"

        if varnum==3 :
            if response.json()['errorcode']=='100002' and response.json()['success']==False:
                print "OK," + varInterfaceName + ",参数错误"
            else:
                print "Err," + varInterfaceName + ",参数错误!"
            print response.content +"\n"
    except Exception,data:
        print Exception,":",data,"\n"

# J23_3(1,1) # 正确返回值
# J23_3(1,"") # 错误返回值
# J23_3(1,-1) # 错误返回值
# J23_3(1,0) # 错误返回值
# 1=正确返回,# 2=系统错误,# 3=参数错误


# 2.3.0 ,4红包比大小游戏登录入口接口
# 1正确返回值,success = true
# 2系统错误,红包比大小游戏入口异常,100001
# 3参数错误,无此用户信息,100002

def redpacketGameLogin(varnum,varuserId,varverifyCode):
    url = "http://192.168.2.176:9999/game/login/1.0/redpacketGameLogin.do"
    querystring1 = {"userId":varuserId,"verifyCode":varverifyCode}
    headers = {
        'cache-control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers, params=querystring1)
    try:
        if varnum==1 :
            if response.json()['success']:
                print "OK,4红包比大小游戏登录入口接口,正确返回值"
            else:
                print "Err,4红包比大小游戏登录入口接口,正确返回值!"
            print response.content +"\n"

        if varnum==2 :
            if response.json()['errorcode']=='100001' and response.json()['success']==False:
                print "OK,4红包比大小游戏登录入口接口,系统错误"
            else:
                print "Err,4红包比大小游戏登录入口接口,系统错误!"
            print response.content +"\n"

        if varnum==3 :
            if response.json()['errorcode']=='100002' and response.json()['success']==False:
                print "OK,4红包比大小游戏登录入口接口,参数错误"
            else:
                print "Err,4红包比大小游戏登录入口接口,参数错误!"
            print response.content +"\n"
    except Exception,data:
        print Exception,":",data,"\n"
redpacketGameLogin(1,"10001755","b17155542ab74f419a202da3091258cb") # 正确返回值
redpacketGameLogin(2,"10001755","b17155542ab74f419a202da3091258cb123") # 红包比大小游戏入口异常,100001
redpacketGameLogin(3,"10001755123","b17155542ab74f419a202da3091258cb123") # 无此用户信息,100002
#
#
# # 2.3.0 ,5红包比大小游戏退出接口
# # 1正确返回值,success = true
# # 2系统错误,红包比大小游戏退出异常,100001
# # 3参数错误,无此用户信息,100002
#
# def redpacketGameQuit(varnum,varuserId,varverifyCode):
#     url = "http://192.168.2.176:9999/game/login/1.0/redpacketGameQuit.do"
#     querystring1 = {"userId":varuserId,"verifyCode":varverifyCode}
#     headers = {
#         'cache-control': "no-cache",
#         }
#     response = requests.request("GET", url, headers=headers, params=querystring1)
#     try:
#         if varnum==1 :
#             if response.json()['success']:
#                 print "OK,5红包比大小游戏退出接口,正确返回值"
#             else:
#                 print "Err,5红包比大小游戏退出接口,正确返回值!"
#             print response.content +"\n"
#
#         if varnum==2 :
#             if response.json()['errorcode']=='100001' and response.json()['success']==False:
#                 print "OK,5红包比大小游戏退出接口,系统错误"
#             else:
#                 print "Err,5红包比大小游戏退出接口,系统错误!"
#             print response.content +"\n"
#
#         if varnum==3 :
#             if response.json()['errorcode']=='100002' and response.json()['success']==False:
#                 print "OK,5红包比大小游戏退出接口,参数错误"
#             else:
#                 print "Err,5红包比大小游戏退出接口,参数错误!"
#             print response.content +"\n"
#     except Exception,data:
#         print Exception,":",data,"\n"
# redpacketGameQuit(1,"10001755","b17155542ab74f419a202da3091258cb") # 正确返回值
# redpacketGameQuit(2,"10001755abc","b17155542ab74f419a202da3091258cb123") # 红包比大小游戏退出异常,100001
# redpacketGameQuit(3,"10001755123","b17155542ab74f419a202da3091258cb123") # 无此用户信息,100002
#

# 100001 红包比大小游戏退出异常
# 100002 用户ID不得为空


# # 2.3.0 游戏列表
# url = "http://192.168.2.176:9999/game/login/1.0/gameMenu.do"
# querystring = {"startIndex":"0"}
# headers = {
#     'cache-control': "no-cache",
#     }
# response = requests.request("GET", url, headers=headers, params=querystring)
#
# # 获取响应内容
# print response.content
# # 获取Json格式
# print response.json()['success']