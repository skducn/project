# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2021-7-1
# Description: Html 对象层
# *******************************************************************************************************************************

"""
1.1 获取网站状态码 getCode()
1.2 获取网站请求头 getHeaders()
1.3 获取网页内容 getText()
1.4 获取网页json内容 rspGetJson()
1.5 解析session.get ?????

2.1 生成请求头 getUserAgent()
2.2 生成代理 getProxies()

"""


from PO.DataPO import *

Data_PO = DataPO()

from PO.SysPO import *

Sys_PO = SysPO()


class HtmlPO:

    # def __init__(self):
    # self.userAgent = self.getUserAgent()
    # self.proxies = self.getProxies()

    def getCode(self, varUrl):

        # 1.1 获取网站状态码

        rsp = requests.get(varUrl)
        return rsp.status_code

    def getHeaders(self, varUrl):

        # 1.2 获取网站请求头
        # {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'Keep-Alive',
        #  'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Fri, 20 Sep 2019 07:12:16 GMT',
        #  'Last-Modified': 'Mon, 23 Jan 2017 13:23:55 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18',
        #  'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}'''

        rsp = requests.get(varUrl)
        return rsp.headers

    def getText(self, varUrl, endcoding="utf-8"):

        # 1.3 获取网页内容
        # get请求时，response默认使用iso - 8859 - 1编码对消息体进行编码，如果返回内容出现乱码，可以使用 utf-8 , gb2312
        # 解决方法：查看网页源码找到charset关键字，如 charset=utf-8

        rsp = requests.get(url=varUrl)
        rsp.encoding = endcoding
        return rsp.text

    def rspGetJson(self, varUrl):

        # 1.4 获取网页json内容

        rsp = requests.get(
            url=varUrl, headers=self.getUserAgent(), proxies=self.getProxies()
        )
        return rsp.json()

    def rspGet(self, varUrl):

        # 1.5 解析get

        return requests.get(
            url=varUrl, headers=self.getUserAgent(), proxies=self.getProxies()
        )

    def rspGetByParam(self, varUrl, params):

        # 1.5 解析get

        return requests.get(
            url=varUrl,
            params=params,
            headers=self.getUserAgent(),
            proxies=self.getProxies(),
        )

    def getUserAgent(self):

        # 2.1 生成UserAgent
        # 如报错fake_useragent.errors.FakeUserAgentError: Maximum amount of retries reached，则执行 pip3.9 install -U fake-useragent 更新

        self.userAgent = {"User-Agent": Data_PO.getUserAgent()}
        return self.userAgent

    def getProxies(self):

        # 2.2 生成proxies代理

        varIp = Data_PO.getProxies()
        self.proxies = {str(varIp).split("://")[0]: varIp}
        return self.proxies


if __name__ == "__main__":

    Html_PO = HtmlPO()

    # print("1.1 获取网站状态码".center(100, "-"))
    # print(Html_PO.getCode("http://www.baidu.com"))  # 200
    #
    # print("1.2 获取网站的headers".center(100, "-"))
    # print(Html_PO.getHeaders("https://www.kuaidaili.com/"))  #  {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Fri, 04 Nov 2022 03:24:59 GMT', 'Last-Modified': 'Mon, 23 Jan 2017 13:27:36 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18', 'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}

    # print("1.3 获取网页内容".center(100, "-"))
    # print(Html_PO.getText("http://www.baidu.com"))
    #
    # print("1.4 获取网页json内容".center(100, "-"))
    # print(Html_PO.rspGetJson("https://www.ximalaya.com/revision/album/getTracksList?albumId=13738175&pageNum=1"))  # {'ret': 200, 'msg': '成功', 'data': {'currentUid': 0, 'albumId': 13738175, 'trackTotalCount': 757, 'sort': 1, 'tracks': [{'index': 757, 'trackId': 583196625, 'isPaid': False, 'tag': 0, 'title': '俞老师又上热搜了，其实…', 'playCount': 1041, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '13小时前', 'url': '/sound/583196625', 'duration': 182, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 182, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 756, 'trackId': 581850497, 'isPaid': False, 'tag': 0, 'title': '31岁的我，因为家务挨骂了', 'playCount': 2010, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '1天前', 'url': '/sound/581850497', 'duration': 204, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 204, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 755, 'trackId': 581849993, 'isPaid': False, 'tag': 0, 'title': '我要招人啦！', 'playCount': 2645, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '2天前', 'url': '/sound/581849993', 'duration': 215, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 215, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 754, 'trackId': 581848044, 'isPaid': False, 'tag': 0, 'title': '凌晨4点睡的我，为什么不担心身体垮掉？', 'playCount': 4007, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '3天前', 'url': '/sound/581848044', 'duration': 252, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 252, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 753, 'trackId': 580995848, 'isPaid': False, 'tag': 0, 'title': '又被骂了，但我很开心', 'playCount': 5261, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '5天前', 'url': '/sound/580995848', 'duration': 197, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 197, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 752, 'trackId': 580995384, 'isPaid': False, 'tag': 0, 'title': '看他们也吃瘪，真爽啊！', 'playCount': 5242, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '6天前', 'url': '/sound/580995384', 'duration': 147, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 147, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 751, 'trackId': 579863492, 'isPaid': False, 'tag': 0, 'title': '偷看了员工电脑，对不起！', 'playCount': 5731, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '7天前', 'url': '/sound/579863492', 'duration': 133, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 133, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 750, 'trackId': 579862923, 'isPaid': False, 'tag': 0, 'title': '微博公开催债，苏醒真的很清醒！', 'playCount': 6286, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '8天前', 'url': '/sound/579862923', 'duration': 215, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 215, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 749, 'trackId': 579862480, 'isPaid': False, 'tag': 0, 'title': '王宝钏恋爱脑被群嘲？这不是重点', 'playCount': 7084, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '9天前', 'url': '/sound/579862480', 'duration': 241, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 241, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 748, 'trackId': 578766121, 'isPaid': False, 'tag': 0, 'title': '看了《浪姐》，后悔没早点知道她', 'playCount': 8545, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '11天前', 'url': '/sound/578766121', 'duration': 188, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 188, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 747, 'trackId': 578765923, 'isPaid': False, 'tag': 0, 'title': '同福客栈来了位不速之客，佟湘玉急了', 'playCount': 8000, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '12天前', 'url': '/sound/578765923', 'duration': 251, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 251, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 746, 'trackId': 578765726, 'isPaid': False, 'tag': 0, 'title': '品牌方特别好说话，原因让我惊讶', 'playCount': 7843, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '13天前', 'url': '/sound/578765726', 'duration': 145, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 145, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 745, 'trackId': 577755122, 'isPaid': False, 'tag': 0, 'title': '开窍的人生，好爽！', 'playCount': 10504, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '15天前', 'url': '/sound/577755122', 'duration': 155, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 155, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 744, 'trackId': 577753997, 'isPaid': False, 'tag': 0, 'title': '这段时间，我的心情像坐过山车', 'playCount': 9824, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '16天前', 'url': '/sound/577753997', 'duration': 207, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 207, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 743, 'trackId': 577753394, 'isPaid': False, 'tag': 0, 'title': '谢娜哭了，我为她感到开心', 'playCount': 9629, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '17天前', 'url': '/sound/577753394', 'duration': 216, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 216, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 742, 'trackId': 577126732, 'isPaid': False, 'tag': 0, 'title': '虞书欣和小S，这点简直一模一样', 'playCount': 11002, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '19天前', 'url': '/sound/577126732', 'duration': 293, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 293, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 741, 'trackId': 575798607, 'isPaid': False, 'tag': 0, 'title': '我对象是个什么样的人？', 'playCount': 12073, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '22天前', 'url': '/sound/575798607', 'duration': 133, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 133, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 740, 'trackId': 575798239, 'isPaid': False, 'tag': 0, 'title': '决定了！以后让我老公带孩子', 'playCount': 11616, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '23天前', 'url': '/sound/575798239', 'duration': 285, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 285, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 739, 'trackId': 575797898, 'isPaid': False, 'tag': 0, 'title': '62岁的老爸教会我一个人生真理', 'playCount': 11693, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '24天前', 'url': '/sound/575797898', 'duration': 119, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 119, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 738, 'trackId': 572913929, 'isPaid': False, 'tag': 0, 'title': '为啥总有人问我怀没怀孕啊', 'playCount': 17614, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '2022-09', 'url': '/sound/572913929', 'duration': 378, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 378, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 737, 'trackId': 572913289, 'isPaid': False, 'tag': 0, 'title': '我妈，一个永远都在吃剩饭的女人', 'playCount': 14802, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '2022-09', 'url': '/sound/572913289', 'duration': 271, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 271, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 736, 'trackId': 572912514, 'isPaid': False, 'tag': 0, 'title': '25岁后，一定要具备这几个思维', 'playCount': 16465, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '2022-09', 'url': '/sound/572912514', 'duration': 232, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 232, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 735, 'trackId': 571295315, 'isPaid': False, 'tag': 0, 'title': '大S最新状态曝光，我悟出了这点', 'playCount': 19319, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '2022-09', 'url': '/sound/571295315', 'duration': 225, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 225, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 734, 'trackId': 570692241, 'isPaid': False, 'tag': 0, 'title': '女性价值观测试题！和我一样的举手！', 'playCount': 17268, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '2022-09', 'url': '/sound/570692241', 'duration': 280, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 280, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 733, 'trackId': 570691673, 'isPaid': False, 'tag': 0, 'title': '别骂周迅了', 'playCount': 16052, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '2022-09', 'url': '/sound/570691673', 'duration': 258, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 258, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 732, 'trackId': 570690794, 'isPaid': False, 'tag': 0, 'title': '公司阿姨要离职，我选择加钱', 'playCount': 15194, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '2022-09', 'url': '/sound/570690794', 'duration': 185, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 185, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 731, 'trackId': 569917655, 'isPaid': False, 'tag': 0, 'title': '怀孕一定会影响工作', 'playCount': 16408, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '2022-09', 'url': '/sound/569917655', 'duration': 184, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 184, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 730, 'trackId': 569917207, 'isPaid': False, 'tag': 0, 'title': '彭于晏，卷死了多少男演员？', 'playCount': 17092, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '2022-09', 'url': '/sound/569917207', 'duration': 213, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 213, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 729, 'trackId': 569401554, 'isPaid': False, 'tag': 0, 'title': '最打击人的，其实不是李湘女儿', 'playCount': 18040, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '2022-09', 'url': '/sound/569401554', 'duration': 267, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 267, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}, {'index': 728, 'trackId': 568933371, 'isPaid': False, 'tag': 0, 'title': '今年真的，什么都不顺！', 'playCount': 18777, 'showLikeBtn': True, 'isLike': False, 'showShareBtn': True, 'showCommentBtn': True, 'showForwardBtn': True, 'createDateFormat': '2022-09', 'url': '/sound/568933371', 'duration': 155, 'isVideo': False, 'isVipFirst': False, 'breakSecond': 0, 'length': 155, 'albumId': 13738175, 'albumTitle': '刘媛媛的晚安电台', 'albumCoverPath': 'group41/M00/2D/62/wKgJ8VqfU_uC5hKcAAIQVsseEmk09.jpeg', 'anchorId': 106276229, 'anchorName': '刘媛媛的fm', 'ximiVipFreeType': 0, 'joinXimi': False}], 'pageNum': 1, 'pageSize': 30, 'superior': []}}

    # print("1.5 解析get".center(100, "-"))
    # html = Html_PO.rspGet("https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=7115296924978203919")
    # print(html.text)
    # print(html.url)

    # print("2.1 生成UserAgent".center(100, "-"))
    # print(Html_PO.getUserAgent())  # {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
    print(Html_PO.getUserAgent())
    # print(Html_PO.getUserAgent())

    # print("2.2 生成proxies代理".center(100, "-"))
    # print(Html_PO.getProxies())
    # print(Html_PO.getProxies())
