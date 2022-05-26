# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: 抖音视频下载（手机端，Web端，支持单个视频、视频列表批量下载
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# https://www.douyin.com/
# 手机版单视频页、列表页 https://v.douyin.com/Jp4GEo6/
# 网页版单视频页 https://www.douyin.com/discover
# 网页版列表页 https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg  全说商业

# 过滤掉非法的多字节序列问题
# b = "型➕换季收纳法🔥叠衣"
# print(b.encode('gbk', 'ignore').decode('gbk') )   # 型换季收纳法叠衣
#***************************************************************



import requests

url = "https://m.mallcoo.cn/api/gift/giftmanager/GetGiftInfoList"
header = {
    "content-type": "application/json",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x18001441) NetType/WIFI Language/zh_CN",
}
data = "{\"mid\":10540,\"pi\":1,\"ps\":4,\"cid\":0,\"bs\":\"\",\"Header\":{\"Token\":\"1w10x6GX5Eis35Hbd8i7AwmqBsLHILqE,15577\",\"systemInfo\":{\"model\":\"iPhone 8 Plus (GSM+CDMA)<iPhone10,2>\",\"SDKVersion\":\"2.24.3\",\"system\":\"iOS 15.0.2\",\"version\":\"8.0.20\",\"miniVersion\":\"DZ.2.5.50.2SBGC.49.M\"}}}"
r = requests.post(url=url,data=data,headers=header)
print(r.text)

# curl -H "Host: m.mallcoo.cn" -H "content-type: application/json" -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x18001441) NetType/WIFI Language/zh_CN" -H
#
# "Referer: https://servicewechat.com/wxd87008fb4d81040e/35/page-frame.html" --data-binary
#
# "{\"mid\":10540,\"pi\":1,\"ps\":4,\"cid\":0,\"bs\":\"\",\"Header\":{\"Token\":\"1w10x6GX5Eis35Hbd8i7AwmqBsLHILqE,15577\",\"systemInfo\":{\"model\":\"iPhone 8 Plus (GSM+CDMA)<iPhone10,2>\",\"SDKVersion\":\"2.24.3\",\"system\":\"iOS 15.0.2\",\"version\":\"8.0.20\",\"miniVersion\":\"DZ.2.5.50.2SBGC.49.M\"}}}" --compressed "https://m.mallcoo.cn/api/gift/giftmanager/GetGiftInfoList"



{"c":13,"m":1,"d":[{"id":184234,"n":"洛斐机械键盘套装","p":"sp_mall/71/5a/lf/0a-98fb-4f1c-9ba7-fc0a8a3a7ca5.jpg","b":40000.0,"sc":3,"ec":0,"rc":0,"mcc":1,"iht":true,"tn":"sp_mall/76/5d/ld/94-077b-4351-9c86-1369a46a3e50.jpg","OrderRank":0,"GiftCategoryID":4485,"CurrencyType":1,"CurrencyValue":0.0,"OnlineTime":"2022-05-25 00:00:00","OfflineTime":"2022-06-30 23:55:00","IsNeedCard":false,"MPPrice":0.0,"IsMPGiftUseNow":false,"IsAdvancedRestriction":false,"AdvancedRestriction":1,"MallCardTypeList":[],"MarketPrice":null,"PayType":0,"PayMoney":0.0,"CouponType":null,"IsNotShowSellStock":false,"ExchangeStartTime":"2022-05-25 00:00:00","ExchangeEndTime":"2022-06-30 23:55:00","IsOpenDiscount":true,"DiscountBonus":35000.0,"DiscountPayMoney":0.0,"IsVipPrice":false,"CurrentTime":"2022-05-25 22:32:36","IsAboutBegin":false,"Remark":""},{"id":183787,"n":"儿童口罩单片装","p":"sp_mall/75/57/h9/56-e9fc-4eda-8daf-f40c47b97479.jpg","b":50.0,"sc":200,"ec":0,"rc":0,"mcc":1,"iht":true,"tn":"sp_mall/72/55/he/a9-28cf-4fb8-acae-73cf86521ad3.jpg","OrderRank":0,"GiftCategoryID":4485,"CurrencyType":1,"CurrencyValue":0.0,"OnlineTime":"2022-05-25 00:00:00","OfflineTime":"2022-06-30 23:55:00","IsNeedCard":false,"MPPrice":0.0,"IsMPGiftUseNow":false,"IsAdvancedRestriction":false,"AdvancedRestriction":1,"MallCardTypeList":[],"MarketPrice":null,"PayType":0,"PayMoney":0.0,"CouponType":null,"IsNotShowSellStock":false,"ExchangeStartTime":"2022-05-25 00:00:00","ExchangeEndTime":"2022-06-30 23:55:00","IsOpenDiscount":true,"DiscountBonus":40.0,"DiscountPayMoney":0.0,"IsVipPrice":false,"CurrentTime":"2022-05-25 22:32:36","IsAboutBegin":false,"Remark":""},{"id":183783,"n":"冰雪奇缘24色彩铅","p":"sp_mall/73/58/h6/63-6ea5-4b62-89a2-33423359c971.jpg","b":500.0,"sc":20,"ec":0,"rc":0,"mcc":1,"iht":true,"tn":"sp_mall/7a/5b/h3/26-f763-4378-9bb5-809b9fbedfcb.jpg","OrderRank":0,"GiftCategoryID":4485,"CurrencyType":1,"CurrencyValue":0.0,"OnlineTime":"2022-05-25 00:00:00","OfflineTime":"2022-06-30 23:55:00","IsNeedCard":false,"MPPrice":0.0,"IsMPGiftUseNow":false,"IsAdvancedRestriction":false,"AdvancedRestriction":1,"MallCardTypeList":[],"MarketPrice":null,"PayType":0,"PayMoney":0.0,"CouponType":null,"IsNotShowSellStock":false,"ExchangeStartTime":"2022-05-25 00:00:00","ExchangeEndTime":"2022-06-30 23:55:00","IsOpenDiscount":true,"DiscountBonus":400.0,"DiscountPayMoney":0.0,"IsVipPrice":false,"CurrentTime":"2022-05-25 22:32:36","IsAboutBegin":false,"Remark":""},{"id":183782,"n":"端午舞龙手工艺品","p":"sp_mall/7f/58/hb/3b-c61a-4a23-ac51-3866ea31c9d8.jpg","b":900.0,"sc":50,"ec":0,"rc":0,"mcc":1,"iht":true,"tn":"sp_mall/7a/52/h2/6f-5341-4abf-9ff5-3cde1a4661c4.jpg","OrderRank":0,"GiftCategoryID":4485,"CurrencyType":1,"CurrencyValue":0.0,"OnlineTime":"2022-05-25 00:00:00","OfflineTime":"2022-06-30 23:55:00","IsNeedCard":false,"MPPrice":0.0,"IsMPGiftUseNow":false,"IsAdvancedRestriction":false,"AdvancedRestriction":1,"MallCardTypeList":[],"MarketPrice":null,"PayType":0,"PayMoney":0.0,"CouponType":null,"IsNotShowSellStock":false,"ExchangeStartTime":"2022-05-25 00:00:00","ExchangeEndTime":"2022-06-30 23:55:00","IsOpenDiscount":true,"DiscountBonus":800.0,"DiscountPayMoney":0.0,"IsVipPrice":false,"CurrentTime":"2022-05-25 22:32:36","IsAboutBegin":false,"Remark":""}],"e":null}
