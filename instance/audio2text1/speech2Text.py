# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-9-2
# Description: ibm cloud 语音转文字
# 流程与步骤：
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

with open(join(dirname(__file__), './.', 'speech2Text.wav'),
               'rb') as audio_file:
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/wav',
        model='zh-CN_BroadbandModel'
        # word_alternatives_threshold=0.9,
        # keywords=['colorado', 'tornado', 'tornadoes'],
        # keywords_threshold=0.5
    ).get_result()
print(speech_recognition_results)   # 字典
print((speech_recognition_results['results'][0]['alternatives'][0]['transcript']).replace(" ", "") + (speech_recognition_results['results'][1]['alternatives'][0]['transcript']).replace(" ", ""))

# print(json.dumps(speech_recognition_results, indent=2))   # 转换Json字符串


# {'result_index': 0, 'results': [{'final': True, 'alternatives': [{'transcript': '就是 加速度 有数 的 舒 勇 大家 好 我 是 媛媛 ', 'confidence': 0.85}]}, {'final': True, 'alternatives': [{'transcript': '马 过年 回家 的 时候 呢 我 妈妈 的 朋友 的 女儿 读 高二 学习 不好 就来 找 我 请教 经验 我 就 问他 我说 你 为什么 学习 不太好 他说 我 觉得 我的 学习 方法 有问题 我 挺 努力 的 但是 我的 成绩 就是 提高 表 然后 就 问 他说 那 你 现在 的 ', 'confidence': 0.88}]}]}
