# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2022-8-16
# Description: # 钉钉开发平台之 自定义机器人接入
# 官网：https://open.dingtalk.com/document/group/custom-robot-access
# ***************************************************************u**

# 自定义机器人
# 获取自定义机器人Webhook
url = "https://oapi.dingtalk.com/robot/send?access_token=528fb490067de67a0bce13c344504aeacd45d268150d86a57b949d75553a9d12"
sign = "SEC31686f219dcb7356c3a4281f8fe4e7cc42bc40cb9f9fa63f7bca29665c06aa9e"

# 消息类型及数据格式
# text类型
json_text = {
    "at": {
        "atMobiles":[
            "13816109050"
        ],
        "atUserIds":[
            "user123"
        ],
        "isAtAll": False
    },
    "text": {
        "content":"@董超，测试机器人推送服务"
    },
    "msgtype":"text"
}


# link类型
json_text = {
    "msgtype": "link",
    "link": {
        "text": "这个即将发布的新版本，测试机器人测试创始人xx称它为红树林。而在此之前，每当面临重大升级，产品经理们都会取一个应景的代号，这一次，为什么是红树林",
        "title": "时代的火车向前开",
        "picUrl": "",
        "messageUrl": "http://192.168.1.105/lock.html"
    }
}

# markdown类型
json_text = {
     "msgtype": "markdown",
     "markdown": {
         "title":"杭州天气",
         "text": "#### 杭州天气 @13816109050 \n > 9度，测试机器人西北风1级，空气良89，相对温度73%\n > ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n > ###### 10点20分发布 [天气](https://www.dingtalk.com) \n"
     },
      "at": {
          "atMobiles": [
              "150XXXXXXXX"
          ],
          "atUserIds": [
              "pnasca6"
          ],
          "isAtAll": False
      }
 }


# 整体跳转ActionCard类型
json_text = {
    "actionCard": {
        "title": "乔布斯 20 年前想打造一间苹果咖啡厅，测试机器人而它正是 Apple Store 的前身",
        "text": "![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png) ,乔布斯 20 年前想打造的苹果咖啡厅 Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划",
        "btnOrientation": "0",
        "singleTitle" : "阅读全文",
        "singleURL" : "https://www.dingtalk.com/"
    },
    "msgtype": "actionCard"
}

json_text = {
    "msgtype": "actionCard",
    "actionCard": {
        "title": "我 测试机器人20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
        "text": "![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png) \n\n #### 乔布斯 20 年前想打造的苹果咖啡厅 \n\n Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划",
        "btnOrientation": "0",
        "btns": [
            {
                "title": "内容不错",
                "actionURL": "https://www.dingtalk.com/"
            },
            {
                "title": "不感兴趣",
                "actionURL": "https://www.dingtalk.com/"
            }
        ]
    }
}

json_text = {
    "msgtype":"feedCard",
    "feedCard": {
        "links": [
            {
                "title": "测试机器人时代的火车向前开1",
                "messageURL": "https://www.dingtalk.com/",
                "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
            },
            {
                "title": "时代的火车向前开2",
                "messageURL": "https://www.dingtalk.com/",
                "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
            }
        ]
    }
}

import requests,json
m = requests.post(url, json.dumps(json_text), headers={"Content-Type":"application/json"}).content
print(m)

# print((m.decode("utf-8", 'strict')))

# requests.post(url, json.dumps(json_text), headers={"Content-Type":"application/json;charset=utf-8"})

