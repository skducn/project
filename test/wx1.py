# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-9/23
# Description: 微信撤回功能
# ********************************************************************************************************************

import itchat

itchat.auto_login()

itchat.send('Hello, filehelper', toUserName='filehelper')

# import itchat
# import time
#
# itchat.auto_login(hotReload=True)
# AutoList = ["yoyo"]
# message = "test"
# while True:
#     # time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
#     # if time_now == "21:43:00": #此处设置每天定时的时间
#     for i in AutoList :
#         user2 = itchat.search_friends(name=i)
#         userName = user2[0]['UserName']
#         itchat.send(message,userName)
#         # itchat.send_file(path,userName)
#         time.sleep(1)
#         itchat.run()


# # itchat.auto_login(True)
# #
# # friends = itchat.get_friends()  # 好友列表
# # print(friends)
#
# # 登录
# itchat.login()
# # 发送消息
# itchat.send(u'你好', 'filehelper')