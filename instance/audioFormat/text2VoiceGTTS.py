# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-9-2
# Description: 调用Google提供的TTS服务来实现将文字转语音,因为需要调用Google的服务，所以需要翻墙
# gtts（google text to speech），一个python库和cli工具，用于与google translate text to speech api接口
# 没有测试
#***************************************************************


from gtts import gTTS
import os

from gtts import gTTS
import os
# tts = gTTS(text='您好，您吃早饭了吗？需要我给你推荐些吃的吗？', lang='zh-tw')

# from gtts import gTTS
# tts = gTTS('hello', lang='en')
# tts.save('hello.mp3')


from gtts import gTTS
from io import BytesIO
mp3_fp = BytesIO()
tts = gTTS('hello', lang='en')
tts.write_to_fp(mp3_fp)