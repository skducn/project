# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-9-2
# Description: ibm cloud 语音转文字 （需要翻墙执行）
# 1，ibm cloud官网（https://cloud.ibm.com/）注册账号获取API密钥和url
# API：Ui7RPYwxGu-BDzKT10rGxMweFAECVJHg97z7WJ41RmoG
# URL：https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/6e18be11-8598-4401-98c3-7622f12d73b6/
# 注意：需要翻墙注册，必须是gmail邮箱
# 2，安装包：
# pip install SpeechRecognition
# pip install ibm_watson
# 3，参数与实例 https://cloud.ibm.com/apidocs/speech-to-text?code=python
# 4，在线ma4转wav  https://www.aconvert.com/cn/audio/m4a-to-mp3/
# 注意：ibm将音频文件上传到服务器进行转换后，将值返回，所以wav文件不能太大，否则会失败。
# curl方法：
# curl -X POST -u "apikey:Ui7RPYwxGu-BDzKT10rGxMweFAECVJHg97z7WJ41RmoG" --header "Content-Type: audio/wav" --data-binary @D:\voice\test.fixed.wav "https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/6e18be11-8598-4401-98c3-7622f12d73b6/v1/recognize?model=zh-CN_BroadbandModel"
#******************************************************************************************************************


from os.path import join, dirname
import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('Ui7RPYwxGu-BDzKT10rGxMweFAECVJHg97z7WJ41RmoG')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)
speech_to_text.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/6e18be11-8598-4401-98c3-7622f12d73b6/')
with open(join(dirname(__file__), 'D://11//家师卫道', '如何培养一个新习惯，就是一个舒适圈走入另一个舒适圈的过程。#家庭教育 #自驱力 #学习方法 #父母课堂 .mp4'), 'rb') as audio_file:
# with open(join(dirname(__file__), 'd:/600/', 'haha_0.wav'), 'rb') as audio_file:
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/wav',
        model='zh-CN_BroadbandModel'
        # word_alternatives_threshold=0.9,
        # keywords=['colorado', 'tornado', 'tornadoes'],
        # keywords_threshold=0.5
    ).get_result()
print(speech_recognition_results)   # 字典
sum = ""
all = len(speech_recognition_results['results'])
for i in range(all):
    text = (speech_recognition_results['results'][i]['alternatives'][0]['transcript']).replace(" ", "")
    sum = sum + text
print(sum)
# print(json.dumps(speech_recognition_results, indent=2))   # 转换Json字符串

# x = {'result_index': 0, 'results': [{'final': True, 'alternatives': [{'transcript': '交易 稳定 盈利 考 得 并不是 什么 指标 攻势 系统 资金 管理 和 风险 控制 这些 只是 辅助 你的 工具 最最 核心 和 关键 的 是 个人 的 理念 和 逻辑思维 从 这个 意义上 说 做 交易 就是 做人 是一个 修身 养性 的 过程 从 一个 吸收 到 顶级 交易员 必须 经历 交易 里面 的 蜕变 以下 是 众多 交易 高手 总结出 来的 交易者 必经 的 十七 个 交易 理念 阶段性 变化 ', 'confidence': 0.93}]}, {'final': True, 'alternatives': [{'transcript': '一个 层次 什么 都 不知道 ', 'confidence': 0.99}]}, {'final': True, 'alternatives': [{'transcript': '看了 几 本书 有了 一些 实盘 经验 头脑 里 都是 几 ', 'confidence': 0.88}]}, {'final': True, 'alternatives': [{'transcript': '开始 从 出来 给 ', 'confidence': 0.74}]}, {'final': True, 'alternatives': [{'transcript': '比如 趋势 资金 管理 严格 侄孙 不 重 仓 不 抓 头 抓捕 ', 'confidence': 0.82}]}, {'final': True, 'alternatives': [{'transcript': '这个 层次 算是 进了 第一个 吗 ', 'confidence': 0.82}]}, {'final': True, 'alternatives': [{'transcript': '幼儿园 毕业 了 第四 个 层次 开始 固定 风格 之 ', 'confidence': 0.94}]}]}
# 交易稳定盈利考得并不是什么指标攻势系统资金管理和风险控制这些只是辅助你的工具最最核心和关键的是个人的理念和逻辑思维从这个意义上说做交易就是做人是一个修身养性的过程从一个吸收到顶级交易员必须经历交易里面的蜕变以下是众多交易高手总结出来的交易者必经的十七个交易理念阶段性变化一个层次什么都不知道
# 到舍弃一些集会形成自己的风格舍弃了一些指标只要少数一些标准第五个层次开始发现资金管理是很重要的事情研究资金管理的学问头寸管理第六个层次给自己制定了一些条条框框风格定位开始发掘执行力世界很重要的事情这个层次算是第二个门槛恭喜你小学毕业了第七个层次慢慢发现预测几乎是不可能的任务开始淡化预测淡化方向发现观察比预测重要控制比分析重要恭喜你你稍微有点开窍比开始用自己的思想来平台市场 第八个层次慢慢发现每套方法美涛系统都有自己的弱点跟优势不再寻求每次都对不再寻求完备的方法尝试找到适合自己性格和思想
# 价值的系统里又进一步了第九个层次终于决定舍弃主观交易舍弃多年的工具唐港和经验事件痛苦的事情但是你不得不放弃因为你发现主观交易太难做到纪律同意性系统性必要准备着手建立自己的交易系统恭喜米米完成了不破不立的关键步骤初中毕业了第十个层次比尝试用自己的经验和知识结构来建立自己的交易系统开始迷惑发现交易原来是门综合性大学问她跟心理学哲学兵法工程控制等等都是相通的比甚至有离开这个市场的年头里终于知道自己不知道的东西太多了这才是你醒悟的开始第十一个层次李开始不断地学习寻找资料经典书籍网络寻找文章寻找对你尤其
# 他的朋友老师来重新解析呢以前的经验和看法重新拼图并试图找到自己的路子积累和学习必不可少交流很重要一个成功的人背后有无数的人在支持因此要懂得感恩回报无论做什么第十二个城市比终于发现一个崇拜者一个大师或者一个偶像或者一个思想以这个思想体系为中心米开始构建自己的交易系统在这个之中你发现你以前对夹藏对资金管理对概率对市场认识对这个游戏列解释那么肤浅发现天外有天人外有人之后你发觉自己的基本功是那么的不足你发现你自己的工具你自己的知识结构是那么的评级在这个阶段能在恰当的时候碰到适合你的好老师和好书是很重要的开源分可遇不可求同时呢有感觉
# 到自己的信心天赋和坚毅的时候兄弟高中毕业了参加高考吧第十三个层次在这个时候比觉得有很多东西要说又说不出来张礼重读经典的时候你的心里经常会蹦出惊喜拍案叫好不断有新的感悟的时候面对吸收你觉得有很多东西要说又觉得没什么好跟他说的米觉得比过去学到了许多东西只是似乎都开始融合起来的时候米通过大一考试了第十四个层次里不断地积累学习筛选开始打造自己的交易工程开始采购各种好的零部件打造自己的黄金战车慢慢地比自己打造出一套使用的交易系统也许你也会觉得照搬人家的一套经典交易系统在运作过程中你慢慢发现其实用这套系统并不是很重要的事情你深深的感觉
# 比最大的财富不是你的交易系统而是你的头脑你的思想你的经验米的素质比甚至不会吝啬把你的交易系统公开灭直到米及时公开了也许没有人会相信相信也不会那么长久地坚持执行米达尔考试通过第十五个层次比可能开始比较不同的交易系统发现他们有共同的地方其实成功的系统并不是那么复杂但是他们都是那么简洁实用有着自己深刻的思想原理甚至你深深感触到那套交易系统之美跟艺术品跟名车陶器青铜器但是呢也不再自大里深深发觉自己不知道的是整个大海而李不过是一个小岛在这个过程中呢不断的交易检查改进学习米大三考试通过第十六个层次里可能开始发掘自己写的
# 一些不足但是你不会感到是问题也不再苛求完美里开始发掘市场是无法战胜李更深地感觉到市场的风险虽然你今年赚了不少比更深层次的考虑市场的风险你担心黑天鹅会飞来米开始不是在一个市场而是多个市场开始交易并未百年一遇的洪水做好准备某同学你大学毕业了恭喜恭喜压的十七个层次也许这个时候你依然继续用着你的交易系统也许这个时候比转变为价值投资者或许这个时候你离开市场去做你喜欢做而年轻时候没有做的事情好了本期视频就到这等因